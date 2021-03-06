######################################################################################################################
# Copyright (C) 2017-2020 Spine project consortium
# This file is part of Spine Toolbox.
# Spine Toolbox is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

"""
For exporting a database to GAMS .gdx file.

Currently, this module supports databases that are "GAMS-like", that is, they follow the EAV model
but the object classes, objects, relationship classes etc. directly reflect the GAMS data
structures. Conversions e.g. from Spine model to TIMES are not supported at the moment.

This module contains low level functions for reading a database into an intermediate format and
for writing that intermediate format into a .gdx file. A higher lever function
to_gdx_file() that does basically everything needed for exporting is provided for convenience.

:author: A. Soininen (VTT)
:date:   30.8.2019
"""

import enum
import itertools
import math
import os
import os.path
import sys
from gdx2py import GAMSSet, GAMSScalar, GAMSParameter, GdxFile
from spinedb_api import from_database, IndexedValue, Map, ParameterValueFormatError

if sys.platform == 'win32':
    import winreg


class GdxExportException(Exception):
    """An exception raised when something goes wrong within the gdx module."""

    def __init__(self, message):
        """
        Args:
            message (str): a message detailing the cause of the exception
        """
        super().__init__()
        self._message = message

    @property
    def message(self):
        """A message detailing the cause of the exception."""
        return self._message

    def __str__(self):
        """Returns the message detailing the cause of the exception."""
        return self._message


class GdxUnsupportedValueTypeException(GdxExportException):
    """An exception raised when an unsupported parameter type is read from the database."""


class Set:
    """
    Represents a GAMS domain, set or a subset.

    Attributes:
        description (str): set's explanatory text
        domain_names (list): a list of superset (domain) names, None if the Set is a domain
        name (str): set's name
        records (list): set's elements as a list of Record objects
    """

    def __init__(self, name, description="", domain_names=None):
        """
        Args:
            name (str): set's name
            description (str): set's explanatory text
            domain_names (list): a list of indexing domain names
        """
        self.description = description if description is not None else ""
        self.domain_names = domain_names if domain_names is not None else [None]
        self.name = name
        self.records = list()

    @property
    def dimensions(self):
        """Number of dimensions of this Set."""
        return len(self.domain_names)

    def is_domain(self):
        """Returns True if this set is a domain set."""
        return self.domain_names[0] is None

    def to_dict(self):
        """Stores Set to a dictionary."""
        set_dict = dict()
        set_dict["name"] = self.name
        set_dict["description"] = self.description
        set_dict["domain_names"] = self.domain_names
        set_dict["records"] = [record.to_dict() for record in self.records]
        return set_dict

    @staticmethod
    def from_dict(set_dict):
        """Restores Set from a dictionary."""
        name = set_dict["name"]
        description = set_dict["description"]
        domain_names = set_dict["domain_names"]
        restored = Set(name, description, domain_names)
        restored.records = [Record.from_dict(record_dict) for record_dict in set_dict["records"]]
        return restored


class Record:
    """
    Represents a GAMS set element in a :class:`Set`.

    Attributes:
        keys (tuple): a tuple of record's keys
    """

    def __init__(self, keys):
        """
        Args:
            keys (tuple): a tuple of record's keys
        """
        self.keys = keys

    def __eq__(self, other):
        """
        Returns True if other is equal to self.

        Args:
            other (Record):  a record to compare to
        """
        if not isinstance(other, Record):
            return NotImplemented
        return other.keys == self.keys

    @property
    def name(self):
        """Record's 'name' as a comma separated list of its keys."""
        return ",".join(self.keys)

    def to_dict(self):
        """Stores Record to a dictionary."""
        record_dict = dict()
        record_dict["keys"] = self.keys
        return record_dict

    @staticmethod
    def from_dict(record_dict):
        """Restores Record from a dictionary."""
        keys = record_dict["keys"]
        restored = Record(tuple(keys))
        return restored


class Parameter:
    """
    Represents a GAMS parameter.

    Attributes:
        domain_names (list): indexing domain names (currently Parameters can be indexed by domains only)
        data (dict): a map from index tuples to parsed values
    """

    def __init__(self, domain_names, indexes, values):
        """
        Args:
            domain_names (list): indexing domain names (currently Parameters can be indexed by domains only)
            indexes (list): parameter's indexes
            values (list): parameter's values
        """
        self.domain_names = domain_names
        if len(indexes) != len(values):
            raise GdxExportException("Parameter index and value length mismatch.")
        if values and not all([isinstance(value, type(values[0])) for value in values[1:]]):
            raise GdxExportException("Not all values are of the same type.")
        self.data = dict(zip(indexes, values))

    def __eq__(self, other):
        if not isinstance(other, Parameter):
            return NotImplemented
        return other.domain_names == self.domain_names and other.data == self.data

    @property
    def indexes(self):
        """list: indexing key tuples"""
        return self.data.keys()

    @property
    def values(self):
        """list: parsed values"""
        return self.data.values()

    def is_consistent(self):
        """Checks that all values are :class:`IndexedValue` objects or scalars."""
        if not self.data:
            return True
        if all(value is None or isinstance(value, IndexedValue) for value in self.data.values()):
            return True
        return all(value is None or isinstance(value, float) for value in self.data.values())

    def slurp(self, parameter):
        """
        Appends the indexes and values from another parameter.

        Args:
            parameter (Parameter): a parameter to append from
        """
        self.data.update(parameter.data)

    def is_scalar(self):
        """Returns True if this parameter seems to contain scalars."""
        return all(not isinstance(value, IndexedValue) for value in self.data.values())

    def is_indexed(self):
        """Returns True if this parameter seems to contain indexed values."""
        return all(isinstance(value, IndexedValue) for value in self.data.values())

    def expand_indexes(self, indexing_setting):
        """
        Expands indexed values to scalars in place by adding a new dimension (index).

        The indexes and values attributes are resized to accommodate all scalars in the indexed values.
        A new indexing domain is inserted to domain_names and the corresponding keys into indexes.
        Effectively, this increases parameter's dimensions by one.

        Args:
            indexing_setting (IndexingSetting): description of how the expansion should be done
        """
        index_position = indexing_setting.index_position
        indexing_domain = indexing_setting.indexing_domain
        self.domain_names = (
            self.domain_names[:index_position] + [indexing_domain.name] + self.domain_names[index_position:]
        )
        new_data = dict()
        for parameter_index, parameter_value in self.data.items():
            if parameter_value is None:
                values = len(indexing_domain.indexes) * [None]
            elif isinstance(parameter_value, IndexedValue):
                values = parameter_value.values
            else:
                raise GdxExportException("Cannot expand indexes of a scalar value.")
            for new_index, new_value in zip(indexing_domain.indexes, values):
                expanded_index = tuple(parameter_index[:index_position] + new_index + parameter_index[index_position:])
                new_data[expanded_index] = new_value
        self.data = new_data


class IndexingDomain:
    """
    This class holds the indexes that should be used for indexed parameter value expansion.

    Attributes:
        name (str): indexing domain's name
        description (str): domain's description
    """

    def __init__(self, name, description, indexes, pick_list):
        """
        Picks the keys from base_domain for which the corresponding element in pick_list holds True.

        Args:
            name (str): indexing domain's name
            description (str): domain's description
            indexes (list): a list of indexing key tuples
            pick_list (list): a list of booleans
        """
        self.name = name
        self.description = description
        self._picked_indexes = None
        self._all_indexes = indexes
        self._pick_list = pick_list

    @property
    def indexes(self):
        """a list of picked indexing key tuples"""
        if self._picked_indexes is None:
            picked = list()
            for index, pick in zip(self._all_indexes, self._pick_list):
                if pick:
                    picked.append(index)
            self._picked_indexes = picked
        return self._picked_indexes

    @property
    def all_indexes(self):
        """a list of all indexing key tuples"""
        return self._all_indexes

    @property
    def pick_list(self):
        """list of boolean values where True means the corresponding index should be picked"""
        return self._pick_list

    def sort_indexes(self, set_settings):
        """
        Sorts the indexes according to settings.

        Args:
            set_settings (SetSettings): export settings for GAMS sets
        """
        self._all_indexes = set_settings.sorted_record_key_lists(self.name)
        self._picked_indexes = None

    def to_dict(self):
        """Stores IndexingDomain to a dictionary."""
        domain_dict = dict()
        domain_dict["name"] = self.name
        domain_dict["description"] = self.description
        domain_dict["indexes"] = self._all_indexes
        domain_dict["pick_list"] = self._pick_list
        return domain_dict

    @staticmethod
    def from_dict(domain_dict):
        """Restores IndexingDomain from a dictionary."""
        indexes = [tuple(index) for index in domain_dict["indexes"]]
        pick_list = domain_dict["pick_list"]
        return IndexingDomain(domain_dict["name"], domain_dict["description"], indexes, pick_list)

    @staticmethod
    def from_base_domain(base_domain, pick_list):
        """
        Builds a new IndexingDomain from an existing Set.

        Args:
            base_domain (Set): a domain set that holds the indexes
            pick_list (list): a list of booleans
        """
        indexes = list()
        for record in base_domain.records:
            indexes.append(record.keys)
        return IndexingDomain(base_domain.name, base_domain.description, indexes, pick_list)


def sort_indexing_domain_indexes(indexing_settings, set_settings):
    """
    Sorts the index keys of an indexing domain in place.

    Args:
        indexing_settings (dict): a mapping from parameter name to IndexingSetting
        set_settings (SetSettings): export settings for GAMS sets
    """
    for indexing_setting in indexing_settings.values():
        indexing_domain = indexing_setting.indexing_domain
        if indexing_domain is not None:
            indexing_domain.sort_indexes(set_settings)


def _python_interpreter_bitness():
    """Returns 64 for 64bit Python interpreter or 32 for 32bit interpreter."""
    # As recommended in Python's docs:
    # https://docs.python.org/3/library/platform.html#cross-platform
    return 64 if sys.maxsize > 2 ** 32 else 32


def _read_value(value_in_database):
    """Converts a parameter from its database representation to a value object."""
    try:
        value = from_database(value_in_database)
    except ParameterValueFormatError:
        raise GdxExportException("Failed to read parameter value.")
    if value is not None and not isinstance(value, (float, IndexedValue)):
        raise GdxUnsupportedValueTypeException(f"Unsupported parameter value type '{type(value).__name__}'.")
    if isinstance(value, Map):
        if value.is_nested():
            raise GdxUnsupportedValueTypeException("Nested maps are not supported.")
        if not all(isinstance(x, float) for x in value.values):
            raise GdxUnsupportedValueTypeException("Exporting non-numerical values in map is not supported.")
    return value


def _windows_dlls_exist(gams_path):
    """Returns True if required DLL files exist in given GAMS installation path."""
    bitness = _python_interpreter_bitness()
    # This DLL must exist on Windows installation
    dll_name = "gdxdclib{}.dll".format(bitness)
    dll_path = os.path.join(gams_path, dll_name)
    return os.path.isfile(dll_path)


def find_gams_directory():
    """
    Returns GAMS installation directory or None if not found.

    On Windows systems, this function looks for `gams.location` in registry;
    on other systems the `PATH` environment variable is checked.

    Returns:
        a path to GAMS installation directory or None if not found.
    """
    if sys.platform == "win32":
        try:
            with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "gams.location") as gams_location_key:
                gams_path, _ = winreg.QueryValueEx(gams_location_key, None)
                if not _windows_dlls_exist(gams_path):
                    return None
                return gams_path
        except FileNotFoundError:
            return None
    executable_paths = os.get_exec_path()
    for path in executable_paths:
        if "gams" in path.casefold():
            return path
    return None


def expand_indexed_parameter_values(parameters, indexing_settings):
    """
    Expands the dimensions of indexed parameter values.

    Args:
        parameters (dict): a map from parameter names to Parameters.
        indexing_settings (dict): mapping from parameter name to IndexingSetting
    """
    for parameter_name, parameter in parameters.items():
        try:
            indexing_setting = indexing_settings[parameter_name]
        except KeyError:
            continue
        parameter.expand_indexes(indexing_setting)


class MergingSetting:
    """
    Holds settings needed to merge a single parameter.

    Attributes:
        parameter_names (list): parameters to merge
        new_domain_name (str): name of the additional domain that contains the parameter names
        new_domain_description (str): explanatory text for the additional domain
        previous_set (str): name of the set containing the parameters before merging;
            not needed for the actual merging but included here to make the parameters' origing traceable
    """

    def __init__(self, parameter_names, new_domain_name, new_domain_description, previous_set, previous_domain_names):
        """
        Args:
            parameter_names (list): parameters to merge
            new_domain_name (str): name of the additional domain that contains the parameter names
            new_domain_description (str): explanatory text for the additional domain
            previous_set (str): name of the set containing the parameters before merging
            previous_domain_names (list): list of parameters' original indexing domains
        """
        self.parameter_names = parameter_names
        self.new_domain_name = new_domain_name
        self.new_domain_description = new_domain_description
        self.previous_set = previous_set
        self._previous_domain_names = previous_domain_names
        self.index_position = len(previous_domain_names)

    def domain_names(self):
        """
        Composes a list of merged parameter's indexing domains.

        Returns:
            list: a list of indexing domains including the new domain containing the merged parameters' names
        """
        return (
            self._previous_domain_names[: self.index_position]
            + [self.new_domain_name]
            + self._previous_domain_names[self.index_position :]
        )

    def to_dict(self):
        """Stores the settings to a dictionary."""
        return {
            "parameters": self.parameter_names,
            "new_domain": self.new_domain_name,
            "domain_description": self.new_domain_description,
            "previous_set": self.previous_set,
            "previous_domains": self._previous_domain_names,
            "index_position": self.index_position,
        }

    @staticmethod
    def from_dict(setting_dict):
        """Restores settings from a dictionary."""
        parameters = setting_dict["parameters"]
        new_domain = setting_dict["new_domain"]
        description = setting_dict["domain_description"]
        previous_set = setting_dict["previous_set"]
        previous_domains = setting_dict["previous_domains"]
        index_position = setting_dict["index_position"]
        setting = MergingSetting(parameters, new_domain, description, previous_set, previous_domains)
        setting.index_position = index_position
        return setting


def update_merging_settings(merging_settings, set_settings, db_map):
    """
    Returns parameter merging settings updated according to new export settings.

    Args:
        merging_settings (dict): old merging settings
        set_settings (SetSettings): new set settings
        db_map (spinedb_api.DatabaseMapping): a database map
    Returns:
        dict: updated merging settings
    """
    updated = dict()
    for merged_parameter_name, setting in merging_settings.items():
        if setting.previous_set not in itertools.chain(set_settings.sorted_domain_names, set_settings.sorted_set_names):
            continue
        entity_class_sq = db_map.entity_class_sq
        entity_class = db_map.query(entity_class_sq).filter(entity_class_sq.c.name == setting.previous_set).first()
        class_id = entity_class.id
        type_id = entity_class.type_id
        type_name = (
            db_map.query(db_map.entity_class_type_sq).filter(db_map.entity_class_type_sq.c.id == type_id).first().name
        )
        if type_name == "object":
            parameters = db_map.parameter_definition_list(object_class_id=class_id)
        elif type_name == "relationship":
            parameters = db_map.parameter_definition_list(relationship_class_id=class_id)
        else:
            raise GdxExportException(f"Unknown entity class type '{type_name}'")
        defined_parameter_names = [parameter.name for parameter in parameters]
        if not defined_parameter_names:
            continue
        setting.parameter_names = defined_parameter_names
        updated[merged_parameter_name] = setting
    return updated


def merging_domain(merging_setting):
    """Constructs the additional indexing domain which contains the merged parameters' names."""
    new_domain = Set(merging_setting.new_domain_name, merging_setting.new_domain_description)
    new_domain.records = [Record((name,)) for name in merging_setting.parameter_names]
    return new_domain


def merge_parameters(parameters, merging_settings):
    """
    Merges multiple parameters into a single parameter.

    Note, that the merged parameters will be removed from the parameters dictionary.

    Args:
        parameters (dict): a mapping from existing parameter name to its Parameter object
        merging_settings (dict): a mapping from the merged parameter name to its merging settings
    Returns:
        dict: a mapping from merged parameter name to its Parameter object
    """
    merged = dict()
    for parameter_name, setting in merging_settings.items():
        indexes = list()
        values = list()
        index_position = setting.index_position
        merged_domain_names = setting.domain_names()
        for name in setting.parameter_names:
            parameter = parameters.pop(name)
            if len(merged_domain_names) < len(parameter.domain_names) + 1:
                raise GdxExportException(
                    f"Merged parameter '{parameter_name}' contains indexed values and therefore cannot be merged."
                )
            for value, base_index in zip(parameter.values, parameter.indexes):
                expanded_index = base_index[:index_position] + (name,) + base_index[index_position:]
                indexes.append(expanded_index)
                values.append(value)
        merged[parameter_name] = Parameter(merged_domain_names, indexes, values)
    return merged


def sets_to_gams(gdx_file, sets, omitted_set=None):
    """
    Writes Set objects to .gdx file as GAMS sets.

    Records and Parameters contained within the Sets are written as well.

    Args:
        gdx_file (GdxFile): a target file
        sets (list): a list of Set objects
        omitted_set (Set): prevents writing this set even if it is included in given sets
    """
    for current_set in sets:
        if omitted_set is not None and current_set.name == omitted_set.name:
            continue
        record_keys = list()
        for record in current_set.records:
            if record is None:
                raise RuntimeError()
            record_keys.append(record.keys)
        gams_set = GAMSSet(record_keys, current_set.domain_names, expl_text=current_set.description)
        try:
            gdx_file[current_set.name] = gams_set
        except NotImplementedError as error:
            raise GdxExportException(f"Failed to write to .gdx file: {error}.")


def parameters_to_gams(gdx_file, parameters):
    """
    Writes parameters to .gdx file as GAMS parameters.

    Args:
        gdx_file (GdxFile): a target file
        parameters (dict): a list of Parameter objects
    """
    for parameter_name, parameter in parameters.items():
        indexed_values = dict()
        for index, value in zip(parameter.indexes, parameter.values):
            if index is None:
                continue
            if isinstance(value, IndexedValue):
                raise GdxExportException(
                    f"Cannot write parameter '{parameter_name}':"
                    + " parameter contains indexed values but indexing domain information is missing."
                )
            if value is None:
                value = math.nan
            if not isinstance(value, float) and index is not None:
                raise GdxExportException(
                    f"Cannot write parameter '{parameter_name}':"
                    + f" parameter contains unsupported values of type '{type(value).__name__}'."
                )
            indexed_values[tuple(index)] = value
        try:
            gams_parameter = GAMSParameter(indexed_values, domain=parameter.domain_names)
        except ValueError as error:
            raise GdxExportException(f"Failed to create GAMS parameter: {error}")
        try:
            gdx_file[parameter_name] = gams_parameter
        except NotImplementedError as error:
            raise GdxExportException(f"Failed to write .gdx: {error}")


def domain_parameters_to_gams_scalars(gdx_file, parameters, domain_name):
    """
    Adds the parameter from given domain as a scalar to .gdx file.

    The added parameters are erased from parameters.

    Args:
        gdx_file (GdxFile): a target file
        parameters (dict): a map from parameter name to Parameter object
        domain_name (str): name of domain whose parameters to add
    Returns:
        a list of non-scalar parameters
    """
    erase_parameters = list()
    for parameter_name, parameter in parameters.items():
        if parameter.domain_names == [domain_name]:
            if len(parameter.data) != 1 or not parameter.is_scalar():
                raise GdxExportException("Parameter {} is not suitable as GAMS scalar.")
            gams_scalar = GAMSScalar(next(iter(parameter.values)))
            try:
                gdx_file[parameter_name] = gams_scalar
            except NotImplementedError as error:
                raise GdxExportException(f"Failed to write to .gdx: {error}")
            erase_parameters.append(parameter_name)
    return erase_parameters


def object_classes_to_domains(db_map, domain_names):
    """
    Converts object classes and objects from a database to the intermediate format.

    Object classes get converted to :class:`Set` objects
    while objects are stored as :class:`Record` objects in the :class:`Set` objects.

    Args:
        db_map (DatabaseMapping or DiffDatabaseMapping): a database map
        domain_names (set): names of domains to convert
    Returns:
         dict: a map from object class id to corresponding :class:`Set`.
    """
    domains = dict()
    for object_class_row in db_map.object_class_list():
        if object_class_row.name not in domain_names:
            continue
        class_id = object_class_row.id
        domain = Set(object_class_row.name, object_class_row.description)
        domains[class_id] = domain
        for object_row in db_map.object_list(class_id=class_id):
            domain.records.append(Record((object_row.name,)))
    return domains


def object_parameters(db_map, domains_with_ids, logger):
    """
    Converts object parameters from database to :class:`Parameter` objects.

    Args:
        db_map (DatabaseMapping or DiffDatabaseMapping): a database map
        domains_with_ids (dict): mapping from object class ids to corresponding :class:`Set` objects
        logger (LoggingInterface, optional): a logger; if not None, some errors are logged and ignored instead of
            raising an exception
    Returns:
        dict: a map from parameter name to corresponding :class:`Parameter`
    """
    classes_with_ignored_parameters = set() if logger is not None else None
    parameters = _object_parameter_default_values(db_map, domains_with_ids, classes_with_ignored_parameters)
    _update_using_existing_object_parameter_values(
        parameters, db_map, domains_with_ids, classes_with_ignored_parameters
    )
    for name, parameter in parameters.items():
        if not parameter.is_consistent():
            raise GdxExportException(f"Parameter '{name}' contains a mixture of different value types.")
    if classes_with_ignored_parameters:
        class_list = ", ".join(classes_with_ignored_parameters)
        logger.msg_warning.emit(
            "Some object parameter values were of unsupported types and were ignored."
            f" The values were from these object classes: {class_list}"
        )
    return parameters


def _object_parameter_default_values(db_map, domains_with_ids, classes_with_ignored_parameters):
    """
    Constructs an initial parameters dict from object parameter definitions.

    Args:
        db_map (DatabaseMapping or DiffDatabaseMapping): a database map
        domains_with_ids (dict): mapping from object class ids to corresponding :class:`Set` objects
        classes_with_ignored_parameters (set, optional): a set of problematic object class names; if not None,
            object class names are added to this set in case of errors instead of raising an exception
    Returns:
        dict: a map from parameter name to corresponding :class:`Parameter`
    """
    parameters = dict()
    for definition_row in db_map.object_parameter_definition_list():
        domain = domains_with_ids.get(definition_row.object_class_id)
        if domain is None:
            continue
        name = definition_row.parameter_name
        if name in parameters:
            raise GdxExportException(f"Duplicate parameter name '{name}' found in different object classes.")
        try:
            parsed_default_value = _read_value(definition_row.default_value)
        except GdxUnsupportedValueTypeException:
            if classes_with_ignored_parameters is not None:
                class_name = domains_with_ids[definition_row.object_class_id].name
                classes_with_ignored_parameters.add(class_name)
                continue
            raise
        domain = domains_with_ids[definition_row.object_class_id]
        indexes = [record.keys for record in domain.records]
        values = len(domain.records) * [parsed_default_value]
        parameters[name] = Parameter([domain.name], indexes, values)
    return parameters


def _update_using_existing_object_parameter_values(
    parameters, db_map, domains_with_ids, classes_with_ignored_parameters
):
    """
    Updates an existing object parameter dict using actual parameter values.

    Args:
        parameters (dict): a mapping from object parameter names to :class:`Parameter` objects to update
        db_map (DatabaseMapping or DiffDatabaseMapping): a database map
        domains_with_ids (dict): mapping from object class ids to corresponding :class:`Set` objects
        classes_with_ignored_parameters (set, optional): a set of problematic object class names; if not None,
            object class names are added to this set in case of errors instead of raising an exception
    """
    for parameter_row in db_map.object_parameter_value_list():
        name = parameter_row.parameter_name
        parameter = parameters.get(name)
        if parameter is None:
            continue
        try:
            parsed_value = _read_value(parameter_row.value)
        except GdxUnsupportedValueTypeException:
            if classes_with_ignored_parameters is not None:
                class_name = domains_with_ids[parameter_row.object_class_id].name
                classes_with_ignored_parameters.add(class_name)
                continue
            raise
        parameter.data[(parameter_row.object_name,)] = parsed_value


def relationship_classes_to_sets(db_map, domain_names, set_names):
    """
    Converts relationship classes and relationships from a database to the intermediate format.

    Relationship classes get converted to :class:`Set` objects
    while relationships are stored as :class:`Record` objects in corresponding :class:`Set` objects.

    Args:
        db_map (DatabaseMapping or DiffDatabaseMapping): a database map
        domain_names (set): names of domains (a.k.a object classes) the relationships connect
        set_names (set): names of sets to convert
    Returns:
         dict: a map from relationship class ids to the corresponding :class:`Set` objects
    """
    sets = dict()
    for relationship_class_row in db_map.wide_relationship_class_list():
        if relationship_class_row.name not in set_names:
            continue
        object_class_names = relationship_class_row.object_class_name_list.split(",")
        if not all([name in domain_names for name in object_class_names]):
            continue
        set_ = Set(relationship_class_row.name, relationship_class_row.description, object_class_names)
        class_id = relationship_class_row.id
        sets[class_id] = set_
        for relationship_row in db_map.wide_relationship_list(class_id=class_id):
            keys = tuple(relationship_row.object_name_list.split(","))
            set_.records.append(Record(keys))
    return sets


def relationship_parameters(db_map, sets_with_ids, logger):
    """
    Converts relationship parameters from database to :class:`Parameter` objects.

    Args:
        db_map (DatabaseMapping or DiffDatabaseMapping): a database map
        sets_with_ids (dict): mapping from relationship class ids to corresponding :class:`Set` objects
        logger (LoggingInterface, optional): a logger; if not None, some errors are logged and ignored instead of
            raising an exception
    Returns:
        dict: a map from parameter name to corresponding :class:`Parameter`
    """
    classes_with_ignored_parameters = set() if logger is not None else None
    parameters = _relationship_parameter_default_values(db_map, sets_with_ids, classes_with_ignored_parameters)
    _update_using_existing_relationship_parameter_values(
        parameters, db_map, sets_with_ids, classes_with_ignored_parameters
    )
    for name, parameter in parameters.items():
        if not parameter.is_consistent():
            raise GdxExportException(f"Parameter '{name}' contains a mixture of different value types.")
    if classes_with_ignored_parameters:
        class_list = ", ".join(classes_with_ignored_parameters)
        logger.msg_warning.emit(
            "Some relationship parameter values were of unsupported types and were ignored."
            f" The values were from these relationship classes: {class_list}"
        )
    return parameters


def _relationship_parameter_default_values(db_map, sets_with_ids, classes_with_ignored_parameters):
    """
    Constructs an initial parameters dict from relationship parameter definitions.

    Args:
        db_map (DatabaseMapping or DiffDatabaseMapping): a database map
        sets_with_ids (dict): mapping from relationship class ids to corresponding :class:`Set` objects
        classes_with_ignored_parameters (set, optional): a set of problematic relationship class names; if not None,
            relationship class names are added to this set in case of errors instead of raising an exception
    Returns:
        dict: a map from parameter name to corresponding :class:`Parameter`
    """
    parameters = dict()
    for definition_row in db_map.relationship_parameter_definition_list():
        set_ = sets_with_ids.get(definition_row.relationship_class_id)
        if set_ is None:
            continue
        name = definition_row.parameter_name
        if name in parameters:
            raise GdxExportException(f"Duplicate parameter name '{name}' found in different relationship classes.")
        try:
            parsed_default_value = _read_value(definition_row.default_value)
        except GdxUnsupportedValueTypeException:
            if classes_with_ignored_parameters is not None:
                class_name = sets_with_ids[definition_row.relationship_class_id].name
                classes_with_ignored_parameters.add(class_name)
                continue
            raise
        set_ = sets_with_ids[definition_row.relationship_class_id]
        indexes = [record.keys for record in set_.records]
        values = len(set_.records) * [parsed_default_value]
        parameters[name] = Parameter(set_.domain_names, indexes, values)
    return parameters


def _update_using_existing_relationship_parameter_values(
    parameters, db_map, sets_with_ids, classes_with_ignored_parameters
):
    """
    Updates an existing relationship parameter dict using actual parameter values.

    Args:
        parameters (dict): a mapping from relationship parameter names to :class:`Parameter` objects to update
        db_map (DatabaseMapping or DiffDatabaseMapping): a database map
        sets_with_ids (dict): mapping from relationship class ids to corresponding :class:`Set` objects
        classes_with_ignored_parameters (set, optional): a set of problematic relationship class names; if not None,
            class names are added to this set in case of errors instead of raising an exception
    """
    for parameter_row in db_map.relationship_parameter_value_list():
        name = parameter_row.parameter_name
        parameter = parameters.get(name)
        if parameter is None:
            continue
        try:
            parsed_value = _read_value(parameter_row.value)
        except GdxUnsupportedValueTypeException:
            if classes_with_ignored_parameters is not None:
                class_name = sets_with_ids[parameter_row.relationship_class_id].name
                classes_with_ignored_parameters.add(class_name)
                continue
            raise
        keys = tuple(parameter_row.object_name_list.split(","))
        parameter.data[keys] = parsed_value


def domain_names_and_records(db_map):
    """
    Returns a list of domain names and a map from a name to list of record keys.

    Args:
        db_map (DatabaseMapping or DiffDatabaseMapping): a database map

    Returns:
         tuple: a tuple containing list of domain names and a dict from domain name to its records
    """
    domain_names = list()
    domain_records = dict()
    class_list = db_map.object_class_list().all()
    for object_class in class_list:
        domain_name = object_class.name
        domain_names.append(domain_name)
        records = list()
        for set_object in db_map.object_list(class_id=object_class.id):
            records.append((set_object.name,))
        domain_records[domain_name] = records
    return domain_names, domain_records


def set_names_and_records(db_map):
    """
    Returns a list of set names and a map from a name to list of record keys.

    Args:
        db_map (spinedb_api.DatabaseMapping or spinedb_api.DiffDatabaseMapping): a database map

    Returns:
         tuple: a tuple containing list of set names and a dict from set name to its records
    """
    names = list()
    set_records = dict()
    for relationship_class in db_map.wide_relationship_class_list():
        set_name = relationship_class.name
        names.append(set_name)
        records = list()
        for relationship in db_map.wide_relationship_list(class_id=relationship_class.id):
            records.append(tuple(relationship.object_name_list.split(",")))
        set_records[set_name] = records
    return names, set_records


class IndexingSetting:
    """
    Settings for indexed value expansion for a single Parameter.

    Attributes:
        parameter (Parameter): a parameter containing indexed values
        indexing_domain (IndexingDomain): indexing info
        index_position (int): where to insert the new index when expanding a parameter
        set_name (str): name of the domain or set to which this parameter belongs
    """

    def __init__(self, indexed_parameter, set_name):
        """
        Args:
            indexed_parameter (Parameter): a parameter containing indexed values
            set_name (str): name of the original entity class to which this parameter belongs
        """
        self.parameter = indexed_parameter
        self.indexing_domain = None
        self.index_position = len(indexed_parameter.domain_names)
        self.set_name = set_name

    def append_parameter(self, parameter):
        """Adds indexes and values from another parameter."""
        self.parameter.slurp(parameter)


def make_indexing_settings(db_map, logger):
    """
    Constructs skeleton indexing settings for parameter indexed value expansion.

    Args:
        db_map (spinedb_api.DatabaseMapping or spinedb_api.DiffDatabaseMapping): a database mapping
        logger (LoggerInterface, optional): a logger
    Returns:
        dict: a mapping from parameter name to IndexingSetting
    """
    settings = _object_indexing_settings(db_map, logger)
    settings.update(_relationship_indexing_settings(db_map, logger))
    return settings


def _object_indexing_settings(db_map, logger):
    """
    Constructs skeleton indexing settings from object parameters.

    Args:
        db_map (spinedb_api.DatabaseMapping or spinedb_api.DiffDatabaseMapping): a database mapping
        logger (LoggingInterface, optional): a logger
    Returns:
        dict: a mapping from parameter name to IndexingSetting
    """
    settings = dict()
    classes_with_unsupported_value_types = set() if logger is not None else None
    parameter_names_to_skip_on_second_pass = set()
    for parameter_row in db_map.object_parameter_value_list():
        value = _read_value(parameter_row.value)
        if isinstance(value, IndexedValue):
            object_class_name = parameter_row.object_class_name
            dimensions = [object_class_name]
            index_keys = (parameter_row.object_name,)
            _add_to_indexing_settings(
                settings,
                parameter_row.parameter_name,
                object_class_name,
                dimensions,
                value,
                index_keys,
                classes_with_unsupported_value_types,
            )
            parameter_names_to_skip_on_second_pass.add(parameter_row.parameter_name)
        elif value is None:
            name = parameter_row.parameter_name
            for definition_row in db_map.object_parameter_definition_list(parameter_row.object_class_id):
                if definition_row.parameter_name != name:
                    continue
                parameter_names_to_skip_on_second_pass.add(name)
                value = _read_value(definition_row.default_value)
                if not isinstance(value, IndexedValue):
                    break
                object_class_name = parameter_row.object_class_name
                dimensions = [object_class_name]
                index_keys = (parameter_row.object_name,)
                _add_to_indexing_settings(
                    settings,
                    name,
                    object_class_name,
                    dimensions,
                    value,
                    index_keys,
                    classes_with_unsupported_value_types,
                )
                break
    for definition_row in db_map.object_parameter_definition_list():
        if definition_row.parameter_name in parameter_names_to_skip_on_second_pass:
            continue
        value = _read_value(definition_row.default_value)
        if not isinstance(value, IndexedValue):
            continue
        object_class_name = definition_row.object_class_name
        dimensions = [object_class_name]
        for object_row in db_map.object_list(class_id=definition_row.object_class_id):
            index_keys = (object_row.name,)
            _add_to_indexing_settings(
                settings,
                definition_row.parameter_name,
                object_class_name,
                dimensions,
                value,
                index_keys,
                classes_with_unsupported_value_types,
            )
    if classes_with_unsupported_value_types:
        class_list = ', '.join(classes_with_unsupported_value_types)
        logger.msg_warning.emit(
            f"The following object classes have parameter values of unsupported types: {class_list}"
        )
    return settings


def _relationship_indexing_settings(db_map, logger):
    """
    Constructs skeleton indexing settings from relationship parameters.

    Args:
        db_map (spinedb_api.DatabaseMapping or spinedb_api.DiffDatabaseMapping): a database mapping
        logger (LoggingInterface, optional): a logger
    Returns:
        dict: a mapping from parameter name to IndexingSetting
    """
    settings = dict()
    classes_with_unsupported_value_types = set() if logger is not None else None
    parameter_names_to_skip_on_second_pass = set()
    for parameter_row in db_map.relationship_parameter_value_list():
        value = _read_value(parameter_row.value)
        if isinstance(value, IndexedValue):
            dimensions = parameter_row.object_class_name_list.split(",")
            index_keys = tuple(parameter_row.object_name_list.split(","))
            _add_to_indexing_settings(
                settings,
                parameter_row.parameter_name,
                parameter_row.relationship_class_name,
                dimensions,
                value,
                index_keys,
                classes_with_unsupported_value_types,
            )
            parameter_names_to_skip_on_second_pass.add(parameter_row.parameter_name)
        elif value is None:
            name = parameter_row.parameter_name
            for definition_row in db_map.relationship_parameter_definition_list(parameter_row.relationship_class_id):
                if definition_row.parameter_name != name:
                    continue
                parameter_names_to_skip_on_second_pass.add(name)
                value = _read_value(definition_row.default_value)
                if not isinstance(value, IndexedValue):
                    break
                dimensions = parameter_row.object_class_name_list.split(",")
                index_keys = tuple(parameter_row.object_name_list.split(","))
                _add_to_indexing_settings(
                    settings,
                    name,
                    parameter_row.relationship_class_name,
                    dimensions,
                    value,
                    index_keys,
                    classes_with_unsupported_value_types,
                )
                break
    for definition_row in db_map.relationship_parameter_definition_list():
        if definition_row.parameter_name in parameter_names_to_skip_on_second_pass:
            continue
        value = _read_value(definition_row.default_value)
        if not isinstance(value, IndexedValue):
            continue
        dimensions = definition_row.object_class_name_list.split(",")
        for relationship_row in db_map.wide_relationship_list(class_id=definition_row.relationship_class_id):
            index_keys = tuple(relationship_row.object_name_list.split(","))
            _add_to_indexing_settings(
                settings,
                definition_row.parameter_name,
                definition_row.relationship_class_name,
                dimensions,
                value,
                index_keys,
                classes_with_unsupported_value_types,
            )
    if classes_with_unsupported_value_types:
        class_list = ', '.join(classes_with_unsupported_value_types)
        logger.msg_warning.emit(
            f"The following relationship classes have parameter values of unsupported types: {class_list}"
        )
    return settings


def _add_to_indexing_settings(
    settings,
    parameter_name,
    entity_class_name,
    dimensions,
    parsed_value,
    index_keys,
    classes_with_unsupported_value_types,
):
    """
    Adds parameter to indexing settings.

    Parameters:
        settings (dict): indexing settings
        parameter_name (str): parameter's name
        entity_class_name (str): name of the object or relationship class the parameter belongs to
        dimensions (list): a list of parameter's domain names
        parsed_value (IndexedValue): parsed parameter value
        index_keys (tuple): parameter's keys
        classes_with_unsupported_value_types (set, optional): entity class names with unsupported value types
    """
    try:
        parameter = Parameter(dimensions, [index_keys], [parsed_value])
    except GdxUnsupportedValueTypeException:
        if classes_with_unsupported_value_types is not None:
            classes_with_unsupported_value_types.add(entity_class_name)
            return
        raise
    setting = settings.get(parameter_name, None)
    if setting is not None:
        setting.append_parameter(parameter)
    else:
        settings[parameter_name] = IndexingSetting(parameter, entity_class_name)


def update_indexing_settings(old_indexing_settings, new_indexing_settings, set_settings):
    """
    Returns new indexing settings merged from old and new ones.

    Entries that do not exist in old settings will be removed.
    If entries exist in both settings the old one will be chosen if both entries are 'equal',
    otherwise the new entry will override the old one.
    Entries existing in new settings only will be added.

    Args:
        old_indexing_settings (dict): settings to be updated
        new_indexing_settings (dict): settings used for updating
        set_settings (SetSettings): new set settings
    Returns:
        dict: merged old and new indexing settings
    """
    updated = dict()
    for parameter_name, setting in new_indexing_settings.items():
        old_setting = old_indexing_settings.get(parameter_name, None)
        if old_setting is None:
            updated[parameter_name] = setting
            continue
        if setting.parameter != old_setting.parameter:
            updated[parameter_name] = setting
            continue
        if old_setting.indexing_domain is not None:
            if old_setting.indexing_domain.name in set_settings.sorted_domain_names:
                new_records = set_settings.sorted_record_key_lists(old_setting.indexing_domain.name)
                indexes = old_setting.indexing_domain.indexes
                if all(index in new_records for index in indexes):
                    updated[parameter_name] = old_setting
                else:
                    updated[parameter_name] = setting
                continue
        updated[parameter_name] = old_setting
    return updated


def indexing_settings_to_dict(settings):
    """
    Stores indexing settings to a JSON compatible dictionary.

    Args:
        settings (dict): a mapping from parameter name to IndexingSetting.
    Returns:
        dict: a JSON serializable dictionary
    """
    settings_dict = dict()
    for parameter_name, setting in settings.items():
        parameter_dict = dict()
        parameter_dict["indexing_domain"] = (
            setting.indexing_domain.to_dict() if setting.indexing_domain is not None else None
        )
        parameter_dict["index_position"] = setting.index_position
        settings_dict[parameter_name] = parameter_dict
    return settings_dict


def indexing_settings_from_dict(settings_dict, db_map, logger):
    """
    Restores indexing settings from a json compatible dictionary.

    Args:
        settings_dict (dict): a JSON compatible dictionary representing parameter indexing settings.
        db_map (DatabaseMapping): database mapping
        logger (LoggerInterface, optional): a logger
    Returns:
        dict: a dictionary mapping parameter name to IndexingSetting.
    """
    settings = dict()
    for parameter_name, setting_dict in settings_dict.items():
        parameter, entity_class_name = _find_indexed_parameter(parameter_name, db_map, logger)
        if parameter is None:
            continue
        setting = IndexingSetting(parameter, entity_class_name)
        indexing_domain_dict = setting_dict["indexing_domain"]
        if indexing_domain_dict is not None:
            setting.indexing_domain = IndexingDomain.from_dict(indexing_domain_dict)
        setting.index_position = setting_dict["index_position"]
        settings[parameter_name] = setting
    return settings


def _find_indexed_parameter(parameter_name, db_map, logger=None):
    """Searches for parameter_name in db_map and returns Parameter and its entity class name."""
    object_classes_with_unsupported_parameter_types = set() if logger is not None else None
    relationship_classes_with_unsupported_parameter_types = set()
    definition = (
        db_map.parameter_definition_list().filter(db_map.parameter_definition_sq.c.name == parameter_name).first()
    )
    if definition is None:
        raise GdxExportException(f"Cannot find parameter '{parameter_name}' in the database.")
    if definition.object_class_id is not None:
        class_id = definition.object_class_id
        class_name = db_map.object_class_list(id_list=[class_id], ordered=False).first().name
        try:
            parsed_default_value = _read_value(definition.default_value)
        except GdxUnsupportedValueTypeException:
            if object_classes_with_unsupported_parameter_types is not None:
                object_classes_with_unsupported_parameter_types.add(class_name)
                return None, class_name
            raise
        if isinstance(parsed_default_value, IndexedValue):
            key_list = [(object_row.name,) for object_row in db_map.object_list(class_id=class_id)]
            value_list = len(key_list) * [parsed_default_value]
            parameter = Parameter([class_name], key_list, value_list)
        else:
            parameter = Parameter([class_name], [], [])
        for parameter_row in db_map.object_parameter_value_list(parameter_name=parameter_name):
            try:
                parsed_value = _read_value(parameter_row.value)
            except GdxUnsupportedValueTypeException:
                if object_classes_with_unsupported_parameter_types is not None:
                    object_classes_with_unsupported_parameter_types.add(class_name)
                    return None, class_name
                raise
            parameter.data[(parameter_row.object_name,)] = parsed_value
    else:
        class_id = definition.relationship_class_id
        relationship_class_row = db_map.wide_relationship_class_list(id_list=[class_id]).first()
        class_name = relationship_class_row.name
        try:
            parsed_default_value = _read_value(definition.default_value)
        except GdxUnsupportedValueTypeException:
            if relationship_classes_with_unsupported_parameter_types is not None:
                relationship_classes_with_unsupported_parameter_types.add(class_name)
                return None, class_name
            raise
        if isinstance(parsed_default_value, IndexedValue):
            key_list = [
                tuple(relationship_row.object_name_list.split(","))
                for relationship_row in db_map.wide_relationship_list(class_id=class_id)
            ]
            value_list = len(key_list) * [parsed_default_value]
            parameter = Parameter(relationship_class_row.object_class_name_list.split(","), key_list, value_list)
        else:
            parameter = Parameter(relationship_class_row.object_class_name_list.split(","), [], [])
        for parameter_row in db_map.relationship_parameter_value_list(parameter_name=parameter_name):
            try:
                parsed_value = _read_value(parameter_row.value)
            except GdxUnsupportedValueTypeException:
                if relationship_classes_with_unsupported_parameter_types is not None:
                    relationship_classes_with_unsupported_parameter_types.add(class_name)
                    return None, class_name
                raise
            parameter.data[tuple(parameter_row.object_name_list.split(","))] = parsed_value
    if parameter is None:
        raise GdxExportException(f"Cannot find values for parameter '{parameter_name}' in the database.")
    if logger is not None:
        if object_classes_with_unsupported_parameter_types:
            class_list = ", ".join(object_classes_with_unsupported_parameter_types)
            logger.msg_warning.emit(
                f"The following object classes contain parameter values of unsupported types: {class_list}"
            )
        if relationship_classes_with_unsupported_parameter_types:
            class_list = ", ".join(relationship_classes_with_unsupported_parameter_types)
            logger.msg_warning.emit(
                f"The following relationship classes contain parameter values of unsupported types: {class_list}"
            )
    return parameter, class_name


def _exported_set_names(names, metadatas):
    """Returns a set of names of the domains that are marked for exporting."""
    return {name for name, metadata in zip(names, metadatas) if metadata.is_exportable()}


def sort_sets(sets, sorted_names):
    """
    Sorts a list of sets according to ``sorted_names``

    Args:
        sets (list): a list of :class:`Set` objects to be sorted
        sorted_names (list): a list of set names in the sorted order

    Returns:
        list: sorted :class:`Set` objects
    """
    sort_indexes = {name: index for index, name in enumerate(sorted_names)}
    try:
        sorted_sets = sorted(sets, key=lambda set_: sort_indexes[set_.name])
    except KeyError as error:
        raise GdxExportException(f"Cannot sort sets: missing set '{error}' in settings.")
    return sorted_sets


def sort_records_inplace(sets, set_settings):
    """
    Sorts the record lists of given domains according to the order given in settings.

    Args:
        sets (list): a list of :class:`Set` objects whose records are to be sorted
        set_settings (SetSettings): settings that define the sorting order
    """
    for current_set in sets:
        sorted_keys = set_settings.sorted_record_key_lists(current_set.name)
        sort_indexes = {key: index for index, key in enumerate(sorted_keys)}
        sorted_records = len(sort_indexes) * [None]
        for record in current_set.records:
            sorted_records[sort_indexes[record.keys]] = record
        current_set.records = sorted_records


def extract_domain(domains, name_to_extract):
    """
    Extracts the domain with given name from a list of domains.

    Args:
        domains (list): a list of Set objects
        name_to_extract (str): name of the domain to be extracted

    Returns:
        a tuple (list, Set) of the modified domains list and the extracted Set object
    """
    for index, domain in enumerate(domains):
        if domain.name == name_to_extract:
            del domains[index]
            return domains, domain
    return domains, None


def to_gdx_file(
    database_map,
    file_name,
    additional_domains,
    set_settings,
    indexing_settings,
    merging_settings,
    gams_system_directory=None,
    logger=None,
):
    """
    Exports given database map into .gdx file.

    Args:
        database_map (spinedb_api.DatabaseMapping or spinedb_api.DiffDatabaseMapping): a database to export
        file_name (str): output file name
        additional_domains (list): a list of extra domains not in the database
        set_settings (SetSettings): export settings
        indexing_settings (dict): a dictionary containing settings for indexed parameter expansion
        merging_settings (dict): a list of merging settings for parameter merging
        gams_system_directory (str, optional): path to GAMS system directory or None to let GAMS choose one for you
        logger (LoggingInterface, optional): a logger; if None given all error conditions raise GdxExportException
            otherwise some errors are logged and ignored
    """
    exported_domain_names = _exported_set_names(set_settings.sorted_domain_names, set_settings.domain_metadatas)
    if set_settings.global_parameters_domain_name:
        exported_domain_names.add(set_settings.global_parameters_domain_name)
    domains_with_ids = object_classes_to_domains(database_map, exported_domain_names)
    domains = list(domains_with_ids.values())
    domain_parameters = object_parameters(database_map, domains_with_ids, logger)
    domains, global_parameters_domain = extract_domain(domains, set_settings.global_parameters_domain_name)
    domains += additional_domains
    domains = sort_sets(domains, set_settings.sorted_domain_names)
    sort_records_inplace(domains, set_settings)
    sort_indexing_domain_indexes(indexing_settings, set_settings)
    expand_indexed_parameter_values(domain_parameters, indexing_settings)
    exported_set_names = _exported_set_names(set_settings.sorted_set_names, set_settings.set_metadatas)
    sets_with_ids = relationship_classes_to_sets(database_map, exported_domain_names, exported_set_names)
    sets = list(sets_with_ids.values())
    sets = sort_sets(sets, set_settings.sorted_set_names)
    sort_records_inplace(sets, set_settings)
    set_parameters = relationship_parameters(database_map, sets_with_ids, logger)
    expand_indexed_parameter_values(set_parameters, indexing_settings)
    parameters = {**domain_parameters, **set_parameters}
    merged_parameters = merge_parameters(parameters, merging_settings)
    parameters.update(merged_parameters)
    with GdxFile(file_name, mode='w', gams_dir=gams_system_directory) as output_file:
        sets_to_gams(output_file, domains, global_parameters_domain)
        sets_to_gams(output_file, sets)
        deletable_parameter_names = list()
        if global_parameters_domain is not None:
            deletable_parameter_names = domain_parameters_to_gams_scalars(
                output_file, domain_parameters, global_parameters_domain.name
            )
        for name in deletable_parameter_names:
            del parameters[name]
        parameters_to_gams(output_file, parameters)


def make_set_settings(database_map):
    """
    Builds a :class:`SetSettings` object from given database.

    Args:
        database_map (spinedb_api.DatabaseMapping or spinedb_api.DiffDatabaseMapping): a database from which
            domains, sets, records etc are extracted

    Returns:
        SetSettings: settings needed for exporting the entities and class from the given ``database_map``
    """
    domain_names, domain_records = domain_names_and_records(database_map)
    set_names, set_records = set_names_and_records(database_map)
    records = domain_records
    records.update(set_records)
    return SetSettings(domain_names, set_names, records)


class SetSettings:
    """
    This class holds the settings for domains, sets and records needed by `to_gdx_file()` for .gdx export.

    :class:`SetSettings` keeps track which domains, sets and records are exported into the .gdx file
    and in which order they are written to the file.
    This order is paramount for some models, like TIMES.
    """

    def __init__(
        self,
        domain_names,
        set_names,
        records,
        domain_metadatas=None,
        set_metadatas=None,
        global_parameters_domain_name="",
    ):
        """
        Args:
            domain_names (list): a list of Set names
            set_names (list): a list of Set names
            records (dict): a mapping from Set names to record key tuples
            domain_metadatas (list): a list of SetMetadata objects, one for each domain
            set_metadatas (list): a list of SetMetadata objects, one for each set
            global_parameters_domain_name (str): name of the Set whose parameters to export as GAMS scalars
        """
        self._domain_names = domain_names
        self._set_names = set_names
        self._records = records
        if domain_metadatas is None:
            domain_metadatas = [SetMetadata() for _ in range(len(domain_names))]
        self._domain_metadatas = domain_metadatas
        if set_metadatas is None:
            set_metadatas = [SetMetadata() for _ in range(len(set_names))]
        self._set_metadatas = set_metadatas
        self._global_parameters_domain_name = global_parameters_domain_name

    @property
    def sorted_domain_names(self):
        """this list defines the order in which domains are exported into the .gdx file."""
        return self._domain_names

    @property
    def domain_metadatas(self):
        """this list contains SetMetadata objects for each name in `domain_names`"""
        return self._domain_metadatas

    @property
    def sorted_set_names(self):
        """this list defines the order in which sets are exported into the .gdx file."""
        return self._set_names

    @property
    def set_metadatas(self):
        """this list contains SetMetadata objects for each name in `set_names`"""
        return self._set_metadatas

    @property
    def global_parameters_domain_name(self):
        """the name of the domain, parameters of which should be exported as GAMS scalars"""
        return self._global_parameters_domain_name

    @global_parameters_domain_name.setter
    def global_parameters_domain_name(self, name):
        """Sets the global_parameters_domain_name and declares that domain FORCED_NON_EXPORTABLE."""
        if self._global_parameters_domain_name:
            i = self._domain_names.index(self._global_parameters_domain_name)
            self._domain_metadatas[i].exportable = ExportFlag.EXPORTABLE
        if name:
            i = self._domain_names.index(name)
            self._domain_metadatas[i].exportable = ExportFlag.FORCED_NON_EXPORTABLE
        self._global_parameters_domain_name = name

    def is_exportable(self, set_name):
        """Returns True if the domain or set with the given name is exportable, False otherwise."""
        try:
            index = self._domain_names.index(set_name)
            return self._domain_metadatas[index].is_exportable()
        except ValueError:
            index = self._set_names.index(set_name)
            return self._set_metadatas[index].is_exportable()

    def add_or_replace_domain(self, domain, metadata):
        """
        Adds a new domain or replaces an existing domain's records and metadata.

        Args:
            domain (Set): a domain to add/replace
            metadata (SetMetadata): domain's metadata
        Returns:
            True if a new domain was added, False if an existing domain was replaced
        """
        self._records[domain.name] = [record.keys for record in domain.records]
        try:
            i = self._domain_names.index(domain.name)
        except ValueError:
            self._domain_names.append(domain.name)
            self._domain_metadatas.append(metadata)
            return True
        self._domain_metadatas[i] = metadata
        return False

    def domain_index(self, domain):
        """Returns an integral index to the domain's name in sorted domain names."""
        return self._domain_names.index(domain.name)

    def del_domain_at(self, index):
        """Erases domain name at given integral index."""
        domain_name = self._domain_names[index]
        del self._domain_names[index]
        del self._domain_metadatas[index]
        del self._records[domain_name]
        if domain_name == self._global_parameters_domain_name:
            self._global_parameters_domain_name = ""

    def update_domain(self, domain):
        """Updates domain's records."""
        self._records[domain.name] = [record.keys for record in domain.records]

    def sorted_record_key_lists(self, name):
        """
        Returns a list of record keys for given domain or set name.

        The list defines the order in which the records are exported into the .gdx file.

        Args:
            name (str): domain or set name

        Returns:
            an ordered list of record key lists
        """
        return self._records[name]

    def update(self, updating_settings):
        """
        Updates the settings by merging with another one.

        All domains, sets and records that are in both settings (common)
        or in `updating_settings` (new) are retained.
        Common elements are ordered the same way they were ordered in the original settings.
        New elements are appended to the common ones in the order they were in `updating_settings`

        Args:
            updating_settings (SetSettings): settings to merge with
        """
        self._domain_names, self._domain_metadatas = self._update_names(
            self._domain_names,
            self._domain_metadatas,
            updating_settings._domain_names,
            updating_settings._domain_metadatas,
        )
        self._set_names, self._set_metadatas = self._update_names(
            self._set_names, self._set_metadatas, updating_settings._set_names, updating_settings._set_metadatas
        )
        if self._global_parameters_domain_name not in self._domain_names:
            self._global_parameters_domain_name = ""
        new_records = dict()
        updating_records = dict(updating_settings._records)
        for set_name, record_names in self._records.items():
            updating_record_names = updating_records.get(set_name, None)
            if updating_record_names is None:
                continue
            new_record_names = list()
            for name in record_names:
                try:
                    updating_record_names.remove(name)
                    new_record_names.append(name)
                except ValueError:
                    pass
            new_record_names += updating_record_names
            new_records[set_name] = new_record_names
            del updating_records[set_name]
        new_records.update(updating_records)
        self._records = new_records

    @staticmethod
    def _update_names(names, metadatas, updating_names, updating_metadatas):
        """Updates a list of domain/set names and exportable flags based on reference names and flags."""
        new_names = list()
        new_metadatas = list()
        updating_names = list(updating_names)
        updating_metadatas = list(updating_metadatas)
        for name, metadata in zip(names, metadatas):
            try:
                index = updating_names.index(name)
                del updating_names[index]
                del updating_metadatas[index]
                new_names.append(name)
                new_metadatas.append(metadata)
            except ValueError:
                # name not found in updating_names -- skip it
                continue
        new_names += updating_names
        new_metadatas += updating_metadatas
        return new_names, new_metadatas

    def to_dict(self):
        """Serializes the this object to a dict."""
        as_dictionary = {
            "domain_names": self._domain_names,
            "domain_metadatas": [metadata.to_dict() for metadata in self._domain_metadatas],
            "set_names": self._set_names,
            "set_metadatas": [metadata.to_dict() for metadata in self._set_metadatas],
            "records": self._records,
            "global_parameters_domain_name": self._global_parameters_domain_name,
        }
        return as_dictionary

    @staticmethod
    def from_dict(dictionary):
        """Deserializes ``SetSettings`` from a dict."""
        domain_names = dictionary.get("domain_names", list())
        domain_metadatas = dictionary.get("domain_metadatas", None)
        if domain_metadatas is not None:
            domain_metadatas = [SetMetadata.from_dict(metadata_dict) for metadata_dict in domain_metadatas]
        set_names = dictionary.get("set_names", list())
        set_metadatas = dictionary.get("set_metadatas", None)
        if set_metadatas is not None:
            set_metadatas = [SetMetadata.from_dict(metadata_dict) for metadata_dict in set_metadatas]
        records = {
            set_name: [tuple(key) for key in keys] for set_name, keys in dictionary.get("records", dict()).items()
        }
        global_parameters_domain_name = dictionary.get("global_parameters_domain_name", "")
        settings = SetSettings(
            domain_names, set_names, records, domain_metadatas, set_metadatas, global_parameters_domain_name
        )
        return settings


class ExportFlag(enum.Enum):
    """Options for exporting Set objects."""

    EXPORTABLE = enum.auto()
    """User has declared that the set should be exported."""
    NON_EXPORTABLE = enum.auto()
    """User has declared that the set should not be exported."""
    FORCED_EXPORTABLE = enum.auto()
    """Set must be exported no matter what."""
    FORCED_NON_EXPORTABLE = enum.auto()
    """Set must never be exported."""


class SetMetadata:
    """
    This class holds some additional configuration for Sets.

    Attributes:
        exportable (ExportFlag): set's export flag
        is_additional (bool): True if the domain does not exist in the database but is supplied separately.
    """

    def __init__(self, exportable=ExportFlag.EXPORTABLE, is_additional=False):
        """
        Args:
            exportable (ExportFlag): set's export flag
            is_additional (bool): True if the domain does not exist in the database but is supplied separately.
        """
        self.exportable = exportable
        self.is_additional = is_additional

    def __eq__(self, other):
        """Returns True if other is equal to this metadata."""
        if not isinstance(other, SetMetadata):
            return NotImplemented
        return self.exportable == other.exportable and self.is_additional == other.is_additional

    def is_exportable(self):
        """Returns True if Set should be exported."""
        return self.exportable in [ExportFlag.EXPORTABLE, ExportFlag.FORCED_EXPORTABLE]

    def is_forced(self):
        """Returns True if user's export choices should be overriden."""
        return self.exportable in [ExportFlag.FORCED_EXPORTABLE, ExportFlag.FORCED_NON_EXPORTABLE]

    def to_dict(self):
        """Serializes metadata to a dictionary."""
        metadata_dict = dict()
        metadata_dict["exportable"] = self.exportable.value
        metadata_dict["is_additional"] = self.is_additional
        return metadata_dict

    @staticmethod
    def from_dict(metadata_dict):
        """Deserializes metadata from a dictionary."""
        metadata = SetMetadata()
        metadata.exportable = ExportFlag(metadata_dict["exportable"])
        metadata.is_additional = metadata_dict["is_additional"]
        return metadata
