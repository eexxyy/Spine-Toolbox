######################################################################################################################
# Copyright (C) 2017-2019 Spine project consortium
# This file is part of Spine Toolbox.
# Spine Toolbox is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

"""
Parameter indexing settings window for .gdx export.

:author: A. Soininen (VTT)
:date:   26.11.2019
"""

import enum
import functools
from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt, Signal, Slot
from PySide2.QtWidgets import QWidget
from spinetoolbox.spine_io.exporters import gdx
from ..list_utils import move_list_elements


class IndexSettingsState(enum.Enum):
    """An enumeration indicating the state of the settings window."""

    OK = enum.auto()
    DOMAIN_MISSING_INDEXES = enum.auto()
    DOMAIN_NAME_MISSING = enum.auto()
    DOMAIN_NAME_CLASH = enum.auto()


class ParameterIndexSettings(QWidget):
    """A widget showing setting for a parameter with indexed values."""

    def __init__(self, parameter_name, indexing_setting, available_existing_domains, new_domains, parent):
        """
        Args:
            parameter_name (str): parameter's name
            indexing_setting (IndexingSetting): indexing settings for the parameter
            available_existing_domains (dict): a dict from existing domain name to a list of its record keys
            new_domains (dict): a dict from new domain name to a list of its record keys
            parent (QWidget, optional): a parent widget
        """
        from ..ui.parameter_index_settings import Ui_Form  # pylint: disable=import-outside-toplevel

        super().__init__(parent)
        self._indexing_setting = indexing_setting
        self._state = IndexSettingsState.OK
        self._ui = Ui_Form()
        self._ui.setupUi(self)
        self._ui.box.setTitle(parameter_name)
        self._indexing_table_model = _IndexingTableModel(indexing_setting.parameter)
        self._ui.index_table_view.setModel(self._indexing_table_model)
        self._available_domains = available_existing_domains
        for domain_name in sorted(name for name in available_existing_domains.keys()):
            self._ui.existing_domains_combo.addItem(domain_name)
        self._ui.existing_domains_combo.activated.connect(self._existing_domain_changed)
        self._ui.use_existing_domain_radio_button.toggled.connect(self._set_enabled_use_existing_domain_widgets)
        self._ui.create_domain_radio_button.toggled.connect(self._set_enabled_create_domain_widgets)
        self._ui.pick_expression_edit.textChanged.connect(self._update_index_list_selection)
        self._ui.generator_expression_edit.textChanged.connect(self._generate_index)
        self._ui.extract_indexes_button.clicked.connect(self._extract_index_from_parameter)
        self._ui.domain_name_edit.textChanged.connect(self._domain_name_changed)
        self._ui.move_domain_left_button.clicked.connect(self._move_indexing_domain_left)
        self._ui.move_domain_right_button.clicked.connect(self._move_indexing_domain_right)
        indexing_domain = indexing_setting.indexing_domain
        if indexing_domain is not None:
            if indexing_domain.name in available_existing_domains:
                self._ui.existing_domains_combo.setCurrentText(indexing_domain.name)
                self._set_enabled_use_existing_domain_widgets(True)
                self._set_enabled_create_domain_widgets(False)
                self._indexing_table_model.set_selection(list(indexing_domain.pick_list))
            else:
                self._ui.create_domain_radio_button.setChecked(True)
                self._set_enabled_use_existing_domain_widgets(False)
                self._set_enabled_create_domain_widgets(True)
                self._ui.domain_name_edit.setText(indexing_domain.name)
                self._ui.domain_description_edit.setText(indexing_domain.description)
                self._indexing_table_model.set_indexes(
                    new_domains[indexing_domain.name], list(indexing_domain.pick_list)
                )
        else:
            self._set_enabled_use_existing_domain_widgets(True)
            self._set_enabled_create_domain_widgets(False)
        self._check_state()
        self._indexing_table_model.selection_changed.connect(self._check_state)

    @property
    def new_domain_name(self):
        """name of the new domain"""
        return str(self._ui.domain_name_edit.text())

    @property
    def state(self):
        """widget's state"""
        return self._state

    @state.setter
    def state(self, new_state):
        """Sets the state of the widget and possibly shows an error indicator."""
        self._state = new_state
        if self._state == IndexSettingsState.DOMAIN_MISSING_INDEXES:
            self.error_message("Not enough selected indexes to index all values.")
        elif self._state == IndexSettingsState.DOMAIN_NAME_MISSING:
            self.error_message("Domain name missing for the new index domain.")
        elif self._state == IndexSettingsState.DOMAIN_NAME_CLASH:
            self.error_message("Domain name already exists. Choose another name.")
        elif self._state == IndexSettingsState.OK:
            self.notification_message("Parameter successfully indexed.")

    def is_using_domain(self, domain_name):
        """Returns True if the given domain_name is indexing the parameter in the widget."""
        if self._ui.use_existing_domain_radio_button.isChecked():
            return self._ui.existing_domains_combo.currentText() == domain_name
        return self._ui.domain_name_edit.text() == domain_name

    def indexing_domain(self):
        """
        Provides information needed to expand the parameter's indexed values.

        Returns:
            tuple: a tuple of IndexingDomain and a Set if a new domain is needed for indexing, otherwise None
        """
        new_domain = None
        indexes = self._indexing_table_model.indexes
        if self._ui.use_existing_domain_radio_button.isChecked():
            domain_name = self._ui.existing_domains_combo.currentText()
            base_domain = gdx.Set(domain_name)
            base_domain.records = [gdx.Record((index,)) for index in indexes]
        else:
            domain_name = self._ui.domain_name_edit.text()
            domain_description = self._ui.domain_description_edit.text()
            base_domain = gdx.Set(domain_name, domain_description)
            base_domain.records += [gdx.Record((index,)) for index in indexes]
            new_domain = base_domain
        pick_list = self._indexing_table_model.index_selection
        indexing_domain = gdx.IndexingDomain.from_base_domain(base_domain, pick_list)
        return indexing_domain, new_domain

    def notification_message(self, message):
        """Shows a notification message on the widget."""
        self._ui.message_label.setText(message)

    def warning_message(self, message):
        """Shows a warning message on the widget."""
        yellow_message = "<span style='color:#b89e00;white-space: pre-wrap;'>" + message + "</span>"
        self._ui.message_label.setText(yellow_message)

    def error_message(self, message):
        """Shows an error message on the widget."""
        red_message = "<span style='color:#ff3333;white-space: pre-wrap;'>" + message + "</span>"
        self._ui.message_label.setText(red_message)

    def reorder_indexes(self, first, last, target):
        """Moves indexes in the index column around. """
        self._indexing_table_model.reorder_indexes(first, last, target)

    @Slot()
    def _check_state(self):
        """Updated the widget's state."""
        mapped_values_balance = self._indexing_table_model.mapped_values_balance()
        if self._check_errors(mapped_values_balance):
            return
        if self._check_warnings(mapped_values_balance):
            return
        self.state = IndexSettingsState.OK

    def _check_errors(self, mapped_values_balance):
        """Checks if the parameter is correctly indexed."""
        if mapped_values_balance < 0:
            self.state = IndexSettingsState.DOMAIN_MISSING_INDEXES
            return True
        if self._ui.create_domain_radio_button.isChecked():
            new_domain_name = self._ui.domain_name_edit.text()
            if not new_domain_name:
                self.state = IndexSettingsState.DOMAIN_NAME_MISSING
                return True
            if new_domain_name in self._available_domains:
                self.state = IndexSettingsState.DOMAIN_NAME_CLASH
                return True
        return False

    def _check_warnings(self, mapped_values_balance):
        """Checks if there are non-fatal issues with parameter indexing."""
        if mapped_values_balance > 0:
            self._state = IndexSettingsState.OK
            self.warning_message("Too many indexes selected. The excess indexes will not be used.")
            return True
        return False

    def _update_indexing_domains_name(self, domain_name=None):
        """
        Updates the model's header and the label showing the indexing domains.

        Args:
            domain_name (str): indexing domain's name or None to read it from the other widgets.
        """
        parameter = self._indexing_setting.parameter
        index_position = self._indexing_setting.index_position
        if domain_name is None:
            if self._ui.use_existing_domain_radio_button.isChecked():
                domain_name = self._ui.existing_domains_combo.currentText()
            else:
                domain_name = self._ui.domain_name_edit.text()
        self._indexing_table_model.set_index_name(domain_name)
        name = "<b>{}</b>".format(domain_name if domain_name else "unnamed")
        label = (
            "("
            + ", ".join(parameter.domain_names[:index_position] + [name] + parameter.domain_names[index_position:])
            + ")"
        )
        self._ui.indexing_domains_label.setText(label)

    @Slot(str)
    def _domain_name_changed(self, text):
        """Reacts to changes in indexing domain name."""
        if text:
            if self._state in (IndexSettingsState.DOMAIN_NAME_MISSING, IndexSettingsState.DOMAIN_NAME_CLASH):
                self._check_state()
            elif self._state == IndexSettingsState.OK and text in self._available_domains:
                self.state = IndexSettingsState.DOMAIN_NAME_CLASH
        elif not text and self._state == IndexSettingsState.OK:
            self.state = IndexSettingsState.DOMAIN_NAME_MISSING
        self._update_indexing_domains_name(text)

    @Slot(bool)
    def _set_enabled_use_existing_domain_widgets(self, enabled):
        """Enables and disables controls used to set up indexing based on an existing domain."""
        self._ui.existing_domains_combo.setEnabled(enabled)
        self._ui.pick_expression_edit.setEnabled(enabled)
        self._ui.pick_expression_label.setEnabled(enabled)
        if enabled:
            self._existing_domain_changed(self._ui.existing_domains_combo.currentIndex())
            self._update_index_list_selection(self._ui.pick_expression_edit.text(), False)
        self._update_indexing_domains_name()

    @Slot(bool)
    def _set_enabled_create_domain_widgets(self, enabled):
        """Enables and disables controls used to set up indexing based on a new domain."""
        self._ui.domain_name_label.setEnabled(enabled)
        self._ui.domain_name_edit.setEnabled(enabled)
        self._ui.domain_description_label.setEnabled(enabled)
        self._ui.domain_description_edit.setEnabled(enabled)
        self._ui.generator_expression_label.setEnabled(enabled)
        self._ui.generator_expression_edit.setEnabled(enabled)
        self._ui.extract_indexes_button.setEnabled(enabled)
        if enabled:
            expression = self._ui.generator_expression_edit.text()
            if expression:
                self._generate_index(expression)
            else:
                self._indexing_table_model.clear()

    @Slot(int)
    def _existing_domain_changed(self, index):
        """Reacts to changes in existing domains combo box."""
        selected_domain_name = self._ui.existing_domains_combo.itemText(index)
        self._indexing_table_model.set_indexes(self._available_domains[selected_domain_name])
        self._update_indexing_domains_name()

    @Slot("QString")
    def _update_index_list_selection(self, expression, clear_selection_if_expression_empty=True):
        """Updates selection according to changed selection expression."""
        if not expression:
            self._indexing_table_model.select_all()
            return
        selected_domain_name = self._ui.existing_domains_combo.currentText()
        length = len(self._available_domains[selected_domain_name])
        is_selected = functools.partial(eval, expression, {})
        try:
            pick_list = [bool(is_selected({"i": i})) for i in range(1, length + 1)]  # pylint: disable=eval-used
        except (AttributeError, NameError, SyntaxError):
            return
        self._indexing_table_model.set_selection(pick_list)

    @Slot(str)
    def _generate_index(self, expression):
        """Builds indexes according to given expression."""
        length = len(next(iter(self._indexing_setting.parameter.values)))
        generate_index = functools.partial(eval, expression, {})
        try:
            indexes = [generate_index({"i": i}) for i in range(1, length + 1)]  # pylint: disable=eval-used
        except (AttributeError, NameError, SyntaxError, ValueError):
            return
        self._indexing_table_model.set_indexes(indexes)

    @Slot(bool)
    def _extract_index_from_parameter(self, _=True):
        """Assigns indexes from the parameter to the model."""
        self._ui.generator_expression_edit.blockSignals(True)
        self._ui.generator_expression_edit.clear()
        self._ui.generator_expression_edit.blockSignals(False)
        indexes = [str(index) for index in next(iter(self._indexing_setting.parameter.values)).indexes]
        self._indexing_table_model.set_indexes(indexes)

    @Slot(bool)
    def _move_indexing_domain_left(self, _):
        """Moves the indexing domain name left on the indexing label."""
        if self._indexing_setting.index_position > 0:
            self._indexing_setting.index_position -= 1
            self._update_indexing_domains_name()

    @Slot(bool)
    def _move_indexing_domain_right(self, _):
        """Moves the indexing domain name right on the indexing label."""
        if self._indexing_setting.index_position < len(self._indexing_setting.parameter.domain_names):
            self._indexing_setting.index_position += 1
            self._update_indexing_domains_name()


class _IndexingTableModel(QAbstractTableModel):
    """
    A table model for parameter value indexing.

    First column contains the proposed new index keys.
    The rest of the columns contain the parameter values for each set of existing index keys.
    Only selected new index keys are used for indexing.
    Unselected rows are left empty.
    """

    selection_changed = Signal()
    """Emitted after the values have been spread over the selected indexes."""

    def __init__(self, parameter):
        """
        Args:
            parameter (Parameter): a parameter to model
        """
        super().__init__()
        self._indexes = list()
        self._index_name = ""
        self._parameter_values = list(parameter.values)
        self._parameter_nonexpanded_indexes = list(parameter.indexes)
        self._selected = list()
        self._rows_shown = 0
        self._values = [list() for _ in range(len(self._parameter_values))]

    @property
    def indexes(self):
        """a string list of all new indexing keys"""
        return self._indexes

    @property
    def index_selection(self):
        """a boolean list of selected index keys, so called pick list"""
        return self._selected

    def canFetchMore(self, parent):
        """Returns True if more rows are available to show."""
        return self._rows_shown < len(self._indexes)

    def clear(self):
        """Clears the model."""
        self.beginResetModel()
        self._indexes = list()
        self._selected = list()
        self._values = [list() for _ in range(len(self._parameter_values))]
        self._rows_shown = 0
        self.endResetModel()
        self.selection_changed.emit()

    def columnCount(self, parent=QModelIndex()):
        """Returns the number of columns."""
        return len(self._parameter_values) + 1

    def data(self, index, role=Qt.DisplayRole):
        """Returns data associated with given model index and role."""
        if role in (Qt.DisplayRole, Qt.ToolTipRole):
            row = index.row()
            column = index.column()
            if column == 0:
                return self._indexes[row]
            return self._values[column - 1][row]
        if index.column() == 0 and role == Qt.CheckStateRole:
            return Qt.Checked if self._selected[index.row()] else Qt.Unchecked
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """Returns header data."""
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Vertical:
            return section + 1
        if section == 0:
            return self._index_name
        return ", ".join(self._parameter_nonexpanded_indexes[section - 1])

    def fetchMore(self, parent):
        """Inserts a number of new rows to the table."""
        remainder = len(self._indexes) - self._rows_shown
        fetch_size = min(remainder, 100)
        end = self._rows_shown + fetch_size
        self.beginInsertRows(parent, self._rows_shown, end - 1)
        for column in self._values:
            column += fetch_size * [None]
        start = self._rows_shown
        self._rows_shown = end
        self._spread_values_over_selected_rows(start)
        self.endInsertRows()

    def flags(self, index):
        """Returns flags for given index."""
        flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled
        if index.column() == 0:
            flags = flags | Qt.ItemIsUserCheckable
        return flags

    def mapped_values_balance(self):
        """
        Returns the balance between available indexes and parameter values.

        Zero means that there is as many indexes available as there are values,
        i.e. the parameter is 'perfectly' indexed.
        A positive value means there are more indexes than values
        while a negative value means there are not enough indexes for all values.

        Returns:
            int: mapped values' balance
        """
        count = sum(1 for selected in self._selected if selected)
        return count - len(self._parameter_values[0].values) if self._parameter_values else 0

    def reorder_indexes(self, first, last, target):
        """
        Moves indexes around.

        Args:
            first (int): first index to move
            last (int): last index to move (inclusive)
            target (int): where to move the first index
        """
        self._indexes = move_list_elements(self._indexes, first, last, target)
        top_left = self.index(first, 0)
        bottom_right = self.index(target, 0)
        self.dataChanged.emit(top_left, bottom_right, [Qt.DisplayRole, Qt.ToolTipRole])

    def rowCount(self, parent=QModelIndex()):
        """Return the number of rows."""
        return self._rows_shown

    def select_all(self):
        """Selects all indexes."""
        self._selected = len(self._indexes) * [True]
        top_left = self.index(0, 0)
        bottom_right = self.index(self._rows_shown - 1, 0)
        self.dataChanged.emit(top_left, bottom_right, [Qt.CheckStateRole])
        self._spread_values_over_selected_rows(0)
        self.selection_changed.emit()

    def setData(self, index, value, role=Qt.EditRole):
        """Sets the checked state for given index."""
        if role != Qt.CheckStateRole:
            return False
        row = index.row()
        self._selected[row] = value == Qt.Checked
        self.dataChanged.emit(index, index, [Qt.CheckStateRole])
        self._spread_values_over_selected_rows(row)
        self.selection_changed.emit()
        return True

    def set_index_name(self, name):
        """Sets the indexing domain name."""
        self._index_name = name
        self.headerDataChanged.emit(Qt.Horizontal, 0, 0)

    def set_indexes(self, indexes, pick_list=None):
        """Overwrites all new indexes."""
        self.beginResetModel()
        self._indexes = indexes
        self._selected = pick_list if pick_list is not None else len(indexes) * [True]
        self._values = [list() for _ in range(len(self._parameter_values))]
        self._rows_shown = 0
        self.selection_changed.emit()
        self.endResetModel()

    def set_selection(self, pick_list):
        """Selects the indexes specified by ``pick_list``"""
        self._selected = pick_list
        top_left = self.index(0, 0)
        bottom_right = self.index(self._rows_shown - 1, 0)
        self.dataChanged.emit(top_left, bottom_right, [Qt.CheckStateRole])
        self._spread_values_over_selected_rows(0)
        self.selection_changed.emit()

    def _spread_values_over_selected_rows(self, first_row):
        """Repopulates the table according to selected indexes."""
        value_start = sum(1 for is_selected in self._selected[:first_row] if is_selected)
        for i, parameter_value in enumerate(self._parameter_values):
            value_index = value_start
            value_length = len(parameter_value)
            values = list(parameter_value.values)
            column = self._values[i]
            for j in range(first_row, self._rows_shown):
                is_selected = self._selected[j]
                if is_selected and value_index < value_length:
                    column[j] = str(values[value_index])
                    value_index += 1
                else:
                    column[j] = None
        top_left = self.index(first_row, 1)
        bottom_right = self.index(self._rows_shown - 1, len(self._values))
        self.dataChanged.emit(top_left, bottom_right, [Qt.DisplayRole, Qt.ToolTipRole])
