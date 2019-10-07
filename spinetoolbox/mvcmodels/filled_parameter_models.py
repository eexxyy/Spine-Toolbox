######################################################################################################################
# Copyright (C) 2017 - 2019 Spine project consortium
# This file is part of Spine Toolbox.
# Spine Toolbox is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

"""
Filled models for parameter definitions and values (as in 'filled with data').

:authors: M. Marin (KTH)
:date:   28.6.2019
"""

from PySide2.QtCore import Qt, QModelIndex
from PySide2.QtGui import QGuiApplication
from mvcmodels.minimal_table_model import MinimalTableModel
from mvcmodels.parameter_mixins import ParameterAutocompleteMixin, ParameterDefinitionAutocompleteMixin
from mvcmodels.parameter_value_formatting import format_for_DisplayRole, format_for_ToolTipRole


class FilledParameterModel(ParameterAutocompleteMixin, MinimalTableModel):
    """A parameter model filled with data."""

    def __init__(self, parent):
        """Initialize class.

        Args:
            parent (ParameterModel): the parent object
        """
        super().__init__(parent)
        self._parent = parent
        self.header = parent.header
        self.db_name_to_map = parent.db_name_to_map
        self._gray_brush = QGuiApplication.palette().button()
        self.error_log = []
        self.updated_count = 0
        self._fetched = False

    def removeRows(self, row, count, parent=QModelIndex()):
        """This model doesn't support column removal."""
        return False

    def insertRows(self, row, count, parent=QModelIndex()):
        """This model doesn't support column insertion."""
        return False

    @staticmethod
    def do_update_items_in_db(db_map, *args, **kwargs):
        """Update items in the given database.
        Must be reimplemented in subclasses.
        """
        raise NotImplementedError()

    def get_data_from_db(self):
        raise NotImplementedError()

    def flags(self, index):
        """Make fixed indexes non-editable."""
        flags = super().flags(index)
        if self.header[index.column()] in self._parent.fixed_fields:
            return flags & ~Qt.ItemIsEditable
        return flags

    def data(self, index, role=Qt.DisplayRole):
        """Paint background of fixed indexes gray and apply custom format to JSON fields."""
        column = index.column()
        if self.header[column] in self._parent.fixed_fields and role == Qt.BackgroundRole:
            return self._gray_brush
        if self.header[column] in self._parent.json_fields:
            if role == Qt.ToolTipRole:
                return format_for_ToolTipRole(super().data(index, Qt.EditRole))
            if role == Qt.DisplayRole:
                return format_for_DisplayRole(super().data(index, Qt.EditRole))
        return super().data(index, role)

    def batch_set_data(self, indexes, data):
        """Sets data for indexes in batch.
        Set data in model first, then set internal data for modified items.
        Finally update successfully modified items in the db.
        """
        self.error_log.clear()
        self.updated_count = 0
        if not super().batch_set_data(indexes, data):
            return False
        rows = {ind.row(): self._main_data[ind.row()] for ind in indexes}
        self.batch_autocomplete_data(rows)
        self.update_items_in_db(rows)
        return True

    def update_items_in_db(self, rows):
        """Updates items in database.

        Args:
            rows (dict): A dict mapping row numbers to items that should be updated in the db
        """
        for row, item in rows.items():
            database = item.database
            db_map = self.db_name_to_map.get(database)
            if not db_map:
                continue
            item_for_update = item.for_update()
            if not item_for_update:
                continue
            upd_items, error_log = self.do_update_items_in_db(db_map, item_for_update)
            if error_log:
                self.error_log.extend(error_log)
                item.revert()
                # TODO: emit dataChanged
            item.clear_cache()
            self.updated_count += 1

    def canFetchMore(self, parent=None):
        """Return True if the model hasn't been fetched."""
        return not self._fetched

    def fetchMore(self, parent=None):
        """Get all data from the database and use it to reset the model."""
        data = self.get_data_from_db()
        self.reset_model(data)

    def get_data_from_db(self):
        """Returns parameter data corresponding to the associated entity class from the database.
        Used when fetching data for populating the model.
        Must be reimplemented in subclasses.
        """
        raise NotImplementedError()

    def reset_model(self, data):
        """Resets model."""
        super().reset_model(data)
        self._fetched = True

    def clear_model(self):
        """Clears model."""
        super().clear_model()
        self._fetched = False


class FilledParameterDefinitionModel(ParameterDefinitionAutocompleteMixin, FilledParameterModel):
    """A parameter definition model filled with data."""

    @staticmethod
    def do_update_items_in_db(db_map, *args, **kwargs):
        """Update items in the given database."""
        return db_map.update_parameter_definitions(*args, **kwargs)

    def update_items_in_db(self, rows):
        """Updates items in database.
        Call the super method to update parameter definitions, then the method to set tags.

        Args:
            rows (dict): A dict mapping row numbers to items that should be updated in the db
        """
        super().update_items_in_db(rows)
        self.set_parameter_definition_tags_in_db(rows)

    def rename_parameter_tags(self, parameter_tags):
        """Rename parameter tags.

        Args:
            parameter_tags (dict): maps id to new tag
        """
        for item in self._main_data:
            if not item.parameter_tag_id_list:
                continue
            split_parameter_tag_id_list = [int(id_) for id_ in item.parameter_tag_id_list.split(",")]
            matches = [(k, id_) for k, id_ in enumerate(split_parameter_tag_id_list) if id_ in parameter_tags]
            if not matches:
                continue
            split_parameter_tag_list = item.parameter_tag_list.split(",")
            for k, id_ in matches:
                new_tag = parameter_tags[id_]
                split_parameter_tag_list[k] = new_tag
            item.parameter_tag_list = ",".join(split_parameter_tag_list)

    def remove_parameter_tags(self, parameter_tag_ids):
        """Remove parameter tags from model.

        Args:
            parameter_tag_ids (set): set of ids to remove
        """
        for item in self._main_data:
            if not item.parameter_tag_id_list:
                continue
            split_parameter_tag_id_list = [int(id_) for id_ in item.parameter_tag_id_list.split(",")]
            matches = [k for k, id_ in enumerate(split_parameter_tag_id_list) if id_ in parameter_tag_ids]
            if not matches:
                continue
            split_parameter_tag_list = item.parameter_tag_list.split(",")
            for k in sorted(matches, reverse=True):
                del split_parameter_tag_list[k]
            item.parameter_tag_list = ",".join(split_parameter_tag_list)


class FilledParameterValueModel(FilledParameterModel):
    """A parameter value model filled with data."""

    @staticmethod
    def do_update_items_in_db(db_map, *args, **kwargs):
        """Update items in the given database."""
        return db_map.update_parameter_values(*args, **kwargs)
