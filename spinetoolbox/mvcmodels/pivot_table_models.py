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
Provides pivot table models for the Tabular View.

:author: P. Vennström (VTT)
:date:   1.11.2018
"""

import enum
from PySide2.QtCore import Qt, Slot, QTimer, QAbstractTableModel, QModelIndex, QSortFilterProxyModel
from PySide2.QtGui import QColor, QFont
from .pivot_model import PivotModel
from .shared import PARSED_ROLE
from ..config import PIVOT_TABLE_HEADER_COLOR


class IndexId(enum.IntEnum):
    PARAMETER = -1
    PARAMETER_INDEX = -3


class PivotTableModel(QAbstractTableModel):

    _V_HEADER_WIDTH = 5
    _FETCH_STEP_COUNT = 64
    _MIN_FETCH_COUNT = 512
    _FETCH_DELAY = 0

    def __init__(self, parent):
        """
        Args:
            parent (TabularViewForm)
        """
        super().__init__()
        self._parent = parent
        self.db_mngr = parent.db_mngr
        self.db_map = parent.db_map
        self.model = PivotModel()
        self._plot_x_column = None
        self._data_row_count = 0
        self._data_column_count = 0
        self.rowsInserted.connect(lambda *args: QTimer.singleShot(self._FETCH_DELAY, self.fetch_more_rows))
        self.columnsInserted.connect(lambda *args: QTimer.singleShot(self._FETCH_DELAY, self.fetch_more_columns))
        self.modelAboutToBeReset.connect(self.reset_data_count)
        self.modelReset.connect(lambda *args: QTimer.singleShot(self._FETCH_DELAY, self.start_fetching))

    @property
    def item_type(self):
        """Returns the item type, always parameter value, for the ParameterValueEditor"""
        return "parameter value"

    @Slot()
    def reset_data_count(self):
        self._data_row_count = 0
        self._data_column_count = 0

    @Slot()
    def start_fetching(self):
        self.fetch_more_rows()
        self.fetch_more_columns()

    @Slot()
    def fetch_more_rows(self):
        max_count = max(self._MIN_FETCH_COUNT, len(self.model.rows) // self._FETCH_STEP_COUNT + 1)
        count = min(max_count, len(self.model.rows) - self._data_row_count)
        if not count:
            return
        first = self.headerRowCount() + self.dataRowCount()
        self.beginInsertRows(QModelIndex(), first, first + count - 1)
        self._data_row_count += count
        self.endInsertRows()

    @Slot()
    def fetch_more_columns(self):
        max_count = max(self._MIN_FETCH_COUNT, len(self.model.rows) // self._FETCH_STEP_COUNT + 1)
        count = min(max_count, len(self.model.columns) - self._data_column_count)
        if not count:
            return
        first = self.headerColumnCount() + self.dataColumnCount()
        self.beginInsertColumns(QModelIndex(), first, first + count - 1)
        self._data_column_count += count
        self.endInsertColumns()

    def reset_model(self, data, index_ids, rows=(), columns=(), frozen=(), frozen_value=()):
        self.beginResetModel()
        self.model.reset_model(data, index_ids, rows, columns, frozen, frozen_value)
        self.endResetModel()
        self._plot_x_column = None

    def clear_model(self):
        self.beginResetModel()
        self.model.clear_model()
        self.endResetModel()
        self._plot_x_column = None

    def update_model(self, data):
        if not data:
            return
        self.model.update_model(data)

    def add_to_model(self, data):
        if not data:
            return
        row_count, column_count = self.model.add_to_model(data)
        if row_count > 0:
            first = self.headerRowCount() + self.dataRowCount()
            self.beginInsertRows(QModelIndex(), first, first + row_count - 1)
            self._data_row_count += row_count
            self.endInsertRows()
        if column_count > 0:
            first = self.headerColumnCount() + self.dataColumnCount()
            self.beginInsertColumns(QModelIndex(), first, first + column_count - 1)
            self._data_column_count += column_count
            self.endInsertColumns()

    def remove_from_model(self, data):
        if not data:
            return
        row_count, column_count = self.model.remove_from_model(data)
        if row_count > 0:
            first = self.headerRowCount()
            self.beginRemoveRows(QModelIndex(), first, first + row_count - 1)
            self._data_row_count -= row_count
            self.endRemoveRows()
        if column_count > 0:
            first = self.headerColumnCount()
            self.beginRemoveColumns(QModelIndex(), first, first + column_count - 1)
            self._data_column_count -= column_count
            self.endRemoveColumns()

    def set_pivot(self, rows, columns, frozen, frozen_value):
        self.beginResetModel()
        self.model.set_pivot(rows, columns, frozen, frozen_value)
        self.endResetModel()

    def set_frozen_value(self, frozen_value):
        self.beginResetModel()
        self.model.set_frozen_value(frozen_value)
        self.endResetModel()

    def set_plot_x_column(self, column, is_x):
        """Sets or clears the Y flag on a column"""
        if is_x:
            self._plot_x_column = column
        elif column == self._plot_x_column:
            self._plot_x_column = None
        self.headerDataChanged.emit(Qt.Horizontal, column, column)

    @property
    def plot_x_column(self):
        """Returns the index of the column designated as Y values for plotting or None."""
        return self._plot_x_column

    def first_data_row(self):
        """Returns the row index to the first data row."""
        # Last row is an empty row, exclude it.
        return self.headerRowCount()

    def headerRowCount(self):
        """Returns number of rows occupied by header."""
        return len(self.model.pivot_columns) + bool(self.model.pivot_rows)

    def headerColumnCount(self):
        """Returns number of columns occupied by header."""
        return max(bool(self.model.pivot_columns), len(self.model.pivot_rows))

    def dataRowCount(self):
        """Returns number of rows that contain actual data."""
        if self.model.pivot_columns and not self.model.pivot_rows:
            return 1
        return self._data_row_count

    def dataColumnCount(self):
        """Returns number of columns that contain actual data."""
        if self.model.pivot_rows and not self.model.pivot_columns:
            return 1
        return self._data_column_count

    def emptyRowCount(self):
        return 1 if self.model.pivot_rows else 0

    def emptyColumnCount(self):
        return 1 if self.model.pivot_columns else 0

    def rowCount(self, parent=QModelIndex()):
        """Number of rows in table, number of header rows + datarows + 1 empty row"""
        return self.headerRowCount() + self.dataRowCount() + self.emptyRowCount()

    def columnCount(self, parent=QModelIndex()):
        """Number of columns in table, number of header columns + datacolumns + 1 empty columns"""
        return self.headerColumnCount() + self.dataColumnCount() + self.emptyColumnCount()

    def flags(self, index):
        """Roles for data"""
        if index.row() < self.headerRowCount() and index.column() < self.headerColumnCount():
            return ~Qt.ItemIsEnabled
        if self.model.pivot_rows and index.row() == len(self.model.pivot_columns):
            # empty line between column headers and data
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled
        if self._parent.is_index_expansion_input_type():
            # Disable editing the pivot table while in expanded index mode.
            if index.row() == self.rowCount() - 1 or index.column() == self.columnCount() - 1:
                return Qt.NoItemFlags
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def top_left_indexes(self):
        """Returns indexes in the top left area.

        Returns
            list(QModelIndex): top indexes (horizontal headers, associated to rows)
            list(QModelIndex): left indexes (vertical headers, associated to columns)
        """
        pivot_column_count = len(self.model.pivot_columns)
        pivot_row_count = len(self.model.pivot_rows)
        top_indexes = []
        left_indexes = []
        for column in range(pivot_row_count):
            index = self.index(pivot_column_count, column)
            top_indexes.append(index)
        column = max(pivot_row_count - 1, 0)
        for row in range(pivot_column_count):
            index = self.index(row, column)
            left_indexes.append(index)
        return top_indexes, left_indexes

    def index_in_top(self, index):
        return index.row() == len(self.model.pivot_columns) and index.column() < len(self.model.pivot_rows)

    def index_in_left(self, index):
        return index.column() == self.headerColumnCount() - 1 and index.row() < len(self.model.pivot_columns)

    def index_in_top_left(self, index):
        """Returns whether or not the given index is in top left corner, where pivot names are displayed"""
        return self.index_in_top(index) or self.index_in_left(index)

    def index_in_column_headers(self, index):
        """Returns whether or not the given index is in column headers (horizontal) area"""
        return (
            index.row() < len(self.model.pivot_columns)
            and self.headerColumnCount() <= index.column() < self.headerColumnCount() + self.dataColumnCount()
        )

    def index_in_row_headers(self, index):
        """Returns whether or not the given index is in row headers (vertical) area"""
        return (
            index.column() < len(self.model.pivot_rows)
            and self.headerRowCount() <= index.row() < self.headerRowCount() + self.dataRowCount()
        )

    def index_in_headers(self, index):
        return self.index_in_column_headers(index) or self.index_in_row_headers(index)

    def index_in_empty_column_headers(self, index):
        """Returns whether or not the given index is in empty column headers (vertical) area"""
        return index.row() < len(self.model.pivot_columns) and index.column() == self.columnCount() - 1

    def index_in_empty_row_headers(self, index):
        """Returns whether or not the given index is in empty row headers (vertical) area"""
        return index.column() < len(self.model.pivot_rows) and index.row() == self.rowCount() - 1

    def index_in_data(self, index):
        """Returns whether or not the given index is in data area"""
        return (
            self.headerRowCount() <= index.row() < self.rowCount() - self.emptyRowCount()
            and self.headerColumnCount() <= index.column() < self.columnCount() - self.emptyColumnCount()
        )

    def column_is_index_column(self, column):
        """Returns True if column is the column containing expanded parameter value indexes."""
        return self._parent.is_index_expansion_input_type() and column == self.headerColumnCount() - 1

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section == self._plot_x_column:
                return "(X)"
            return None
        if role == Qt.DisplayRole and orientation == Qt.Vertical:
            return self._V_HEADER_WIDTH * " "
        return None

    def map_to_pivot(self, index):
        """Returns a tuple of row and column in the pivot model that corresponds to the given model index.

        Args:
            index (QModelIndex)

        Returns:
            int: row
            int: column
        """
        return index.row() - self.headerRowCount(), index.column() - self.headerColumnCount()

    def _top_left_id(self, index):
        """Returns the id of the top left header corresponding to the given header index.

        Args:
            index (QModelIndex)
        Returns:
            int, NoneType
        """
        if self.index_in_row_headers(index):
            return self.model.pivot_rows[index.column()]
        if self.index_in_column_headers(index):
            return self.model.pivot_columns[index.row()]
        return None

    def _header_id(self, index):
        """Returns the id of the given row or column header index.

        Args:
            index (QModelIndex)
        Returns:
            int, NoneType
        """
        if self.index_in_row_headers(index):
            row, _ = self.map_to_pivot(index)
            return self.model._row_data_header[row][index.column()]
        if self.index_in_column_headers(index):
            _, column = self.map_to_pivot(index)
            return self.model._column_data_header[column][index.row()]
        return None

    def _header_ids(self, row, column):
        """Returns the ids for the headers at given row *and* column.

        Args:
            row (int)
            column (int)

        Returns:
            tuple(int)
        """
        row_key = self.model.row_key(max(0, row))
        column_key = self.model.column_key(max(0, column))
        return self.model._key_getter(row_key + column_key + self.model.frozen_value)

    def _header_name(self, top_left_id, header_id):
        """Returns the name of the header given by top_left_id and header_id.

        Args:
            top_left_id (int): The id of the top left header
            header_id (int): The header id

        Returns
            str
        """
        if top_left_id == IndexId.PARAMETER:
            return self.db_mngr.get_item(self.db_map, "parameter definition", header_id).get("parameter_name")
        return self.db_mngr.get_item(self.db_map, "object", header_id)["name"]

    def header_name(self, index):
        """Returns the name corresponding to the given header index.

        Args:
            index (QModelIndex)

        Returns:
            str
        """
        header_id = self._header_id(index)
        top_left_id = self._top_left_id(index)
        return self._header_name(top_left_id, header_id)

    def header_data(self, index, role=Qt.DisplayRole):
        """Returns the data corresponding to the given header index based on role enum.

        Args:
            index (QModelIndex)
            role (enum Qt.ItemDataRole)

        Returns:
            str: a string role-dependent string representation of the cell's contents.
        """

        def fetch_from_db(fetch_name, name_field):
            item = self.db_mngr.get_item(self.db_map, fetch_name, header_id)
            if role in (Qt.DisplayRole, Qt.EditRole):
                return item.get(name_field)
            if role == Qt.ToolTipRole:
                description = item.get("description")
                return description if description else item.get(name_field)

        header_id = self._header_id(index)
        top_left_id = self._top_left_id(index)
        if top_left_id == IndexId.PARAMETER:
            return fetch_from_db("parameter definition", "parameter_name")
        if top_left_id == IndexId.PARAMETER_INDEX:
            # header_id contains the index value already
            return str(header_id)
        return fetch_from_db("object", "name")

    def header_names(self, index):
        """Returns the header names corresponding to the given data index.

        Args:
            index (QModelIndex)

        Returns:
            list(str): object names
            str: parameter name
        """
        row, column = self.map_to_pivot(index)
        header_ids = self._header_ids(row, column)
        last_object_id = -1 if not self._parent.is_index_expansion_input_type() else -2
        objects_ids, parameter_id = header_ids[:last_object_id], header_ids[-1]
        object_names = [self.db_mngr.get_item(self.db_map, "object", id_)["name"] for id_ in objects_ids]
        parameter_name = self.db_mngr.get_item(self.db_map, "parameter definition", parameter_id).get(
            "parameter_name", ""
        )
        return object_names, parameter_name

    def index_name(self, index):
        """Returns a string that concatenates the header names corresponding to the given data index.

        Args:
            index (QModelIndex)

        Returns:
            str
        """
        if not self.index_in_data(index):
            return ""
        object_names, parameter_name = self.header_names(index)
        return self.db_mngr._GROUP_SEP.join(object_names) + " - " + parameter_name

    def column_name(self, column):
        """Returns a string that concatenates the header names corresponding to the given column.

        Args:
            column (int)

        Returns:
            str
        """
        header_names = []
        column -= self.headerColumnCount()
        for row, top_left_id in enumerate(self.model.pivot_columns):
            header_id = self.model._column_data_header[column][row]
            header_names.append(self._header_name(top_left_id, header_id))
        return self.db_mngr._GROUP_SEP.join(header_names)

    def _color_data(self, index):
        if index.row() < self.headerRowCount() and index.column() < self.headerColumnCount():
            return QColor(PIVOT_TABLE_HEADER_COLOR)

    def data(self, index, role=Qt.DisplayRole):
        if role in (Qt.DisplayRole, Qt.EditRole, Qt.ToolTipRole, PARSED_ROLE):
            if self.index_in_top(index):
                return self.model.pivot_rows[index.column()]
            if self.index_in_left(index):
                return self.model.pivot_columns[index.row()]
            if self.index_in_headers(index):
                return self.header_data(index, role)
            if self.index_in_data(index):
                row, column = self.map_to_pivot(index)
                data = self.model.get_pivoted_data([row], [column])
                if not data:
                    return None
                value = data[0][0]
                if value is None:
                    return None
                if self._parent.is_value_input_type():
                    value = self.db_mngr.get_value(self.db_map, "parameter value", value, "value", role)
                    return value
                if self._parent.is_index_expansion_input_type():
                    index = self._header_ids(row, column)[-2]
                    return self.db_mngr.get_value_index(self.db_map, "parameter value", value, "value", index, role)
                return bool(value)
            return None
        if role == Qt.FontRole and self.index_in_top_left(index):
            font = QFont()
            font.setBold(True)
            return font
        if role == Qt.BackgroundColorRole:
            return self._color_data(index)
        if role == Qt.TextAlignmentRole and self.index_in_data(index) and not self._parent.is_value_input_type():
            return Qt.AlignHCenter
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if role != Qt.EditRole:
            return False
        return self.batch_set_data([index], [value])

    def batch_set_data(self, indexes, values):
        inner_data = []
        header_data = []
        empty_row_header_data = []
        empty_column_header_data = []
        for index, value in zip(indexes, values):
            if self.index_in_data(index):
                inner_data.append((index, value))
            elif self.index_in_headers(index):
                header_data.append((index, value))
            elif self.index_in_empty_row_headers(index):
                empty_row_header_data.append((index, value))
            elif self.index_in_empty_column_headers(index):
                empty_column_header_data.append((index, value))
        result = self._batch_set_inner_data(inner_data)
        result |= self._batch_set_header_data(header_data)
        result |= self._batch_set_empty_header_data(empty_row_header_data, lambda i: self.model.pivot_rows[i.column()])
        result |= self._batch_set_empty_header_data(
            empty_column_header_data, lambda i: self.model.pivot_columns[i.row()]
        )
        return result

    def _batch_set_inner_data(self, inner_data):
        row_map = set()
        column_map = set()
        values = {}
        for index, value in inner_data:
            row, column = self.map_to_pivot(index)
            row_map.add(row)
            column_map.add(column)
            values[row, column] = value
        row_map = list(row_map)
        column_map = list(column_map)
        data = self.model.get_pivoted_data(row_map, column_map)
        if not data:
            return False
        if self._parent.is_value_input_type():
            return self._batch_set_parameter_value_data(row_map, column_map, data, values)
        return self._batch_set_relationship_data(row_map, column_map, data, values)

    def get_set_data_delayed(self, index):
        """Returns a function that ParameterValueEditor can call to set data for the given index at any later time,
        even if the model changes.

        Args:
            index (QModelIndex)

        Returns:
            function
        """
        row, column = self.map_to_pivot(index)
        data = self.model.get_pivoted_data([row], [column])
        header_ids = self._header_ids(row, column)
        if data[0][0] is None:
            parameter_value_to_add = self._make_parameter_value_to_add()
            return lambda value, parameter_value_to_add=parameter_value_to_add, header_ids=header_ids: self._add_parameter_values(
                [parameter_value_to_add(header_ids, value)]
            )
        return lambda value, id_=data[0][0], header_ids=header_ids: self._update_parameter_values(
            [self._parameter_value_to_update(id_, header_ids, value)]
        )

    def _object_parameter_value_to_add(self, header_ids, value):
        return dict(
            entity_class_id=self._parent.current_class_id,
            entity_id=header_ids[0],
            parameter_definition_id=header_ids[-1],
            value=value,
        )

    def _relationship_parameter_value_to_add(self, header_ids, value, rel_id_lookup):
        object_id_list = ",".join([str(id_) for id_ in header_ids[:-1]])
        relationship_id = rel_id_lookup[object_id_list]
        return dict(
            entity_class_id=self._parent.current_class_id,
            entity_id=relationship_id,
            parameter_definition_id=header_ids[-1],
            value=value,
        )

    def _make_parameter_value_to_add(self):
        if self._parent.current_class_type == "object class":
            return self._object_parameter_value_to_add
        if self._parent.current_class_type == "relationship class":
            relationships = self.db_mngr.get_items_by_field(
                self.db_map, "relationship", "class_id", self._parent.current_class_id
            )
            rel_id_lookup = {x["object_id_list"]: x["id"] for x in relationships}
            return lambda header_ids, value, rel_id_lookup=rel_id_lookup: self._relationship_parameter_value_to_add(
                header_ids, value, rel_id_lookup
            )

    def _parameter_value_to_update(self, id_, header_ids, value):
        item = {"id": id_, "value": value}
        if self._parent.is_index_expansion_input_type():
            item["index"] = header_ids[-2]
        else:
            item["parameter_definition_id"] = header_ids[-1]
        return item

    def _batch_set_parameter_value_data(self, row_map, column_map, data, values):
        """Sets parameter values in batch."""
        to_add = []
        to_update = []
        parameter_value_to_add = self._make_parameter_value_to_add()
        for i, row in enumerate(row_map):
            for j, column in enumerate(column_map):
                if (row, column) not in values:
                    continue
                header_ids = self._header_ids(row, column)
                if data[i][j] is None:
                    item = parameter_value_to_add(header_ids, values[row, column])
                    to_add.append(item)
                else:
                    item = self._parameter_value_to_update(data[i][j], header_ids, values[row, column])
                    to_update.append(item)
        if not to_add and not to_update:
            return False
        if to_add:
            self._add_parameter_values(to_add)
        if to_update:
            self._update_parameter_values(to_update)
        return True

    def _checked_parameter_values(self, items):
        value_lists = {}
        par_def_ids = {item["parameter_definition_id"] for item in items}
        for par_def_id in par_def_ids:
            param_val_list_id = self.db_mngr.get_item(self.db_map, "parameter definition", par_def_id).get(
                "parameter_value_list_id"
            )
            if not param_val_list_id:
                continue
            param_val_list = self.db_mngr.get_item(self.db_map, "parameter value list", param_val_list_id)
            value_list = param_val_list.get("value_list")
            if not value_list:
                continue
            value_lists[par_def_id] = value_list.split(",")
        checked_items = []
        for item in items:
            par_def_id = item["parameter_definition_id"]
            value_list = value_lists.get(par_def_id)
            if value_list and item["value"] not in value_list:
                continue
            checked_items.append(item)
        return checked_items

    def _add_parameter_values(self, items):
        items = self._checked_parameter_values(items)
        self.db_mngr.add_checked_parameter_values({self.db_map: items})

    def _update_parameter_values(self, items):
        items = self._checked_parameter_values(items)
        self.db_mngr.update_checked_parameter_values({self.db_map: items})

    def _batch_set_relationship_data(self, row_map, column_map, data, values):
        def relationship_to_add(header_ids):
            rel_cls_name = self.db_mngr.get_item(self.db_map, "relationship class", self._parent.current_class_id)[
                "name"
            ]
            object_names = [self.db_mngr.get_item(self.db_map, "object", id_)["name"] for id_ in header_ids]
            name = rel_cls_name + "_" + "__".join(object_names)
            return dict(object_id_list=list(header_ids), class_id=self._parent.current_class_id, name=name)

        to_add = []
        to_remove = []
        for i, row in enumerate(row_map):
            for j, column in enumerate(column_map):
                header_ids = self._header_ids(row, column)
                if data[i][j] is None and values[row, column]:
                    item = relationship_to_add(header_ids)
                    to_add.append(item)
                elif data[i][j] is not None and not values[row, column]:
                    item = self.db_mngr.get_item(self.db_map, "relationship", data[i][j])
                    to_remove.append(item)
        if not to_add and not to_remove:
            return False
        if to_add:
            self.db_mngr.add_relationships({self.db_map: to_add})
        if to_remove:
            self.db_mngr.remove_items({self.db_map: {"relationship": to_remove}})
        return True

    def _batch_set_header_data(self, header_data):
        objects = []
        param_defs = []
        for index, value in header_data:
            header_id = self._header_id(index)
            top_left_id = self._top_left_id(index)
            item = dict(id=header_id, name=value)
            if top_left_id == IndexId.PARAMETER:
                param_defs.append(item)
            else:
                objects.append(item)
        if not objects and not param_defs:
            return False
        if objects:
            self.db_mngr.update_objects({self.db_map: objects})
        if param_defs:
            self.db_mngr.update_parameter_definitions({self.db_map: param_defs})
        return True

    def _batch_set_empty_header_data(self, header_data, get_top_left_id):
        objects = []
        param_defs = []
        for index, value in header_data:
            top_left_id = get_top_left_id(index)
            item = dict(name=value)
            if top_left_id == IndexId.PARAMETER:
                class_key = (
                    "object_class_id" if self._parent.current_class_type == "object class" else "relationship_class_id"
                )
                item[class_key] = self._parent.current_class_id
                param_defs.append(item)
            else:
                item["class_id"] = self._parent.current_object_class_id_list()[top_left_id]
                objects.append(item)
        if not objects and not param_defs:
            return False
        if objects:
            self.db_mngr.add_objects({self.db_map: objects})
        if param_defs:
            self.db_mngr.add_parameter_definitions({self.db_map: param_defs})
        return True


class PivotTableSortFilterProxy(QSortFilterProxyModel):
    def __init__(self, parent=None):
        """Initialize class."""
        super().__init__(parent)
        self.setDynamicSortFilter(False)  # Important so we can edit parameters in the view
        self.index_filters = {}

    def set_filter(self, identifier, filter_value):
        """Sets filter for a given index (object class) name.

        Args:
            identifier (int): index identifier
            filter_value (set, None): A set of accepted values, or None if no filter (all pass)
        """
        self.index_filters[identifier] = filter_value
        self.invalidateFilter()  # trigger filter update

    def clear_filter(self):
        self.index_filters = {}
        self.invalidateFilter()  # trigger filter update

    def accept_index(self, index, index_ids):
        for i, identifier in zip(index, index_ids):
            valid = self.index_filters.get(identifier)
            if valid is not None and i not in valid:
                return False
        return True

    def filterAcceptsRow(self, source_row, source_parent):
        """Returns true if the item in the row indicated by the given source_row
        and source_parent should be included in the model; otherwise returns false.
        """

        if source_row < self.sourceModel().headerRowCount() or source_row == self.sourceModel().rowCount() - 1:
            return True
        if self.sourceModel().model.pivot_rows:
            index = self.sourceModel().model._row_data_header[source_row - self.sourceModel().headerRowCount()]
            return self.accept_index(index, self.sourceModel().model.pivot_rows)
        return True

    def filterAcceptsColumn(self, source_column, source_parent):
        """Returns true if the item in the column indicated by the given source_column
        and source_parent should be included in the model; otherwise returns false.
        """
        if (
            source_column < self.sourceModel().headerColumnCount()
            or source_column == self.sourceModel().columnCount() - 1
        ):
            return True
        if self.sourceModel().model.pivot_columns:
            index = self.sourceModel().model._column_data_header[source_column - self.sourceModel().headerColumnCount()]
            return self.accept_index(index, self.sourceModel().model.pivot_columns)
        return True

    def batch_set_data(self, indexes, values):
        indexes = [self.mapToSource(index) for index in indexes]
        return self.sourceModel().batch_set_data(indexes, values)
