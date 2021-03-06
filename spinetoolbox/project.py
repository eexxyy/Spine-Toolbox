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
Spine Toolbox project class.

:authors: P. Savolainen (VTT), E. Rinne (VTT)
:date:   10.1.2018
"""

import os
import json
from PySide2.QtCore import Slot, Signal
from PySide2.QtWidgets import QMessageBox
from spine_engine import SpineEngine, SpineEngineState
from .category import CATEGORIES
from .metaobject import MetaObject
from .helpers import create_dir, inverted, erase_dir
from .config import LATEST_PROJECT_VERSION, PROJECT_FILENAME
from .dag_handler import DirectedGraphHandler
from .project_tree_item import LeafProjectTreeItem
from .spine_db_manager import SpineDBManager
from .project_commands import (
    SetProjectNameCommand,
    SetProjectDescriptionCommand,
    AddProjectItemsCommand,
    RemoveProjectItemCommand,
    RemoveAllProjectItemsCommand,
)


class SpineToolboxProject(MetaObject):
    """Class for Spine Toolbox projects."""

    dag_execution_finished = Signal()
    dag_execution_about_to_start = Signal("QVariant")
    """Emitted just before an engine runs. Provides a reference to the engine."""
    project_execution_about_to_start = Signal()
    """Emitted just before the entire project is executed."""

    def __init__(
        self,
        toolbox,
        name,
        description,
        p_dir,
        project_item_model,
        settings,
        embedded_julia_console,
        embedded_python_console,
        logger,
    ):

        """

        Args:
            toolbox (ToolboxUI): toolbox of this project
            name (str): Project name
            description (str): Project description
            p_dir (str): Project directory
            project_item_model (ProjectItemModel): project item tree model
            settings (QSettings): Toolbox settings
            embedded_julia_console (JuliaREPLWidget): a Julia console widget for execution in the embedded console
            embedded_python_console (PythonReplWidget): a Python console widget for execution in the embedded console
            logger (LoggerInterface): a logger instance
        """
        super().__init__(name, description)
        self._toolbox = toolbox
        self._project_item_model = project_item_model
        self._logger = logger
        self._settings = settings
        self._embedded_julia_console = embedded_julia_console
        self._embedded_python_console = embedded_python_console
        self.dag_handler = DirectedGraphHandler()
        self.db_mngr = SpineDBManager(settings, logger, self)
        self.engine = None
        self._execution_stopped = True
        self._dag_execution_list = None
        self._dag_execution_permits_list = None
        self._dag_execution_index = None
        self.project_dir = None  # Full path to project directory
        self.config_dir = None  # Full path to .spinetoolbox directory
        self.items_dir = None  # Full path to items directory
        self.config_file = None  # Full path to .spinetoolbox/project.json file
        self._toolbox.undo_stack.clear()
        if not self._create_project_structure(p_dir):
            self._logger.msg_error.emit("Creating project directory " "structure to <b>{0}</b> failed".format(p_dir))

    def connect_signals(self):
        """Connect signals to slots."""
        self.dag_handler.dag_simulation_requested.connect(self.notify_changes_in_dag)
        self.dag_execution_finished.connect(self.execute_next_dag)

    def _create_project_structure(self, directory):
        """Makes the given directory a Spine Toolbox project directory.
        Creates directories and files that are common to all projects.

        Args:
            directory (str): Abs. path to a directory that should be made into a project directory

        Returns:
            bool: True if project structure was created successfully, False otherwise
        """
        self.project_dir = directory
        self.config_dir = os.path.abspath(os.path.join(self.project_dir, ".spinetoolbox"))
        self.items_dir = os.path.abspath(os.path.join(self.config_dir, "items"))
        self.config_file = os.path.abspath(os.path.join(self.config_dir, PROJECT_FILENAME))
        try:
            create_dir(self.project_dir)  # Make project directory
        except OSError:
            self._logger.msg_error.emit("Creating directory {0} failed".format(self.project_dir))
            return False
        try:
            create_dir(self.config_dir)  # Make project config directory
        except OSError:
            self._logger.msg_error.emit("Creating directory {0} failed".format(self.config_dir))
            return False
        try:
            create_dir(self.items_dir)  # Make project items directory
        except OSError:
            self._logger.msg_error.emit("Creating directory {0} failed".format(self.items_dir))
            return False
        return True

    def call_set_name(self, name):
        self._toolbox.undo_stack.push(SetProjectNameCommand(self, name))

    def call_set_description(self, description):
        self._toolbox.undo_stack.push(SetProjectDescriptionCommand(self, description))

    def set_name(self, name):
        """Changes project name.

        Args:
            name (str): New project name
        """
        super().set_name(name)
        self._toolbox.update_window_title()
        # Remove entry with the old name from File->Open recent menu
        self._toolbox.remove_path_from_recent_projects(self.project_dir)
        # Add entry with the new name back to File->Open recent menu
        self._toolbox.update_recent_projects()
        self._logger.msg.emit("Project name changed to <b>{0}</b>".format(self.name))

    def set_description(self, description):
        super().set_description(description)
        msg = "Project description "
        if description:
            msg += f"changed to <b>{description}</b>"
        else:
            msg += "cleared"
        self._logger.msg.emit(msg)

    @staticmethod
    def get_connections(links):
        connections = list()
        for link in links:
            src_connector = link.src_connector
            src_anchor = src_connector.position
            src_name = src_connector.parent_name()
            dst_connector = link.dst_connector
            dst_anchor = dst_connector.position
            dst_name = dst_connector.parent_name()
            conn = {"from": [src_name, src_anchor], "to": [dst_name, dst_anchor]}
            connections.append(conn)
        return connections

    def save(self, spec_paths):
        """Collects project information and objects
        into a dictionary and writes it to a JSON file.

        Args:
            spec_paths (list): List of absolute paths to specification files

        Returns:
            bool: True or False depending on success
        """
        project_dict = dict()  # Dictionary for storing project info
        project_dict["version"] = LATEST_PROJECT_VERSION
        project_dict["name"] = self.name
        project_dict["description"] = self.description
        project_dict["tool_specifications"] = spec_paths
        # Compute connections directly from Links on scene
        project_dict["connections"] = self.get_connections(self._toolbox.ui.graphicsView.links())
        items_dict = dict()  # Dictionary for storing project items
        # Traverse all items in project model by category
        for category_item in self._project_item_model.root().children():
            category = category_item.name
            category_dict = items_dict[category] = dict()
            for item in self._project_item_model.items(category):
                category_dict[item.name] = item.project_item.item_dict()
        # Save project to file
        saved_dict = dict(project=project_dict, objects=items_dict)
        # Write into JSON file
        with open(self.config_file, "w") as fp:
            json.dump(saved_dict, fp, indent=4)
        return True

    def load(self, objects_dict):
        """Populates project item model with items loaded from project file.

        Args:
            objects_dict (dict): Dictionary containing all project items in JSON format

        Returns:
            bool: True if successful, False otherwise
        """
        self._logger.msg.emit("Loading project items...")
        empty = True
        for category_name, category_dict in objects_dict.items():
            if category_name not in CATEGORIES:
                self._logger.msg_warning.emit(
                    f"The project contains an unknown project item category: '{category_name}'. " "Moving on..."
                )
                continue
            items_in_category = dict()
            for name, item_dict in category_dict.items():
                item_dict.pop("short name", None)
                item_dict["name"] = name
                try:
                    item_type = item_dict.pop("type")
                except KeyError:
                    item_type = _legacy_type_from_category(category_name)
                items_in_category.setdefault(item_type, list()).append(item_dict)
                empty = False
            for item_type, items in items_in_category.items():
                if not self.make_and_add_project_items(item_type, items, verbosity=False):
                    return False
        if empty:
            self._logger.msg_warning.emit("Project has no items")
        return True

    def add_project_items(self, item_type, *items, set_selected=False, verbosity=True):
        """Pushes an AddProjectItemsCommand to the toolbox undo stack.
        """
        if not items:
            return
        self._toolbox.undo_stack.push(
            AddProjectItemsCommand(self, item_type, items, set_selected=set_selected, verbosity=verbosity)
        )

    def make_project_tree_items(self, item_type, items):
        """Creates and returns a dictionary mapping category indexes to a list of corresponding LeafProjectTreeItem instances.

        Args:
            item_type (str): item type
            items (list): one or more dicts of items to add

        Returns:
            dict(QModelIndex, list(LeafProjectTreeItem))
        """
        factory = self._toolbox.item_factories.get(item_type)
        if factory is None:
            self._logger.msg_error.emit(f"Unknown item type <b>{item_type}</b>")
            for item in items:
                self._logger.msg_error.emit(f"Loading project item <b>{item['name']}</b> failed")
            return {None: None}
        project_items_by_category = {}
        for item_dict in items:
            try:
                project_item = factory.make_item(self._toolbox, self, self._logger, **item_dict)
            except TypeError:
                self._logger.msg_error.emit(
                    f"Creating <b>{item_type}</b> project item <b>{item_dict['name']}</b> failed. "
                    "This is most likely caused by an outdated project file."
                )
                continue
            except KeyError as error:
                self._logger.msg_error.emit(
                    f"Creating <b>{item_type}</b> project item <b>{item_dict['name']}</b> failed. "
                    f"This is most likely caused by an outdated or corrupted project file "
                    f"(missing JSON key: {str(error)})."
                )
                continue
            project_items_by_category.setdefault(project_item.item_category(), list()).append(project_item)
        project_tree_items = {}
        for category, project_items in project_items_by_category.items():
            category_ind = self._project_item_model.find_category(category)
            # NOTE: category_ind might be None, and needs to be handled caller side
            project_tree_items[category_ind] = [
                LeafProjectTreeItem(project_item, self._toolbox) for project_item in project_items
            ]
        return project_tree_items

    def do_add_project_tree_items(self, category_ind, *project_tree_items, set_selected=False, verbosity=True):
        """Adds LeafProjectTreeItem instances to project.

        Args:
            category_ind (QModelIndex): The category index
            project_tree_items (LeafProjectTreeItem): one or more LeafProjectTreeItem instances to add
            set_selected (bool): Whether to set item selected after the item has been added to project
            verbosity (bool): If True, prints message
        """
        for project_tree_item in project_tree_items:
            project_item = project_tree_item.project_item
            self._project_item_model.insert_item(project_tree_item, category_ind)
            factory = self._toolbox.item_factories[project_item.item_type()]
            factory.activate_project_item(self._toolbox, project_item)
            # Append new node to networkx graph
            self.add_to_dag(project_item.name)
            if verbosity:
                self._logger.msg.emit(
                    "{0} <b>{1}</b> added to project".format(project_item.item_type(), project_item.name)
                )
        if set_selected:
            item = list(project_tree_items)[-1]
            self.set_item_selected(item)

    def set_item_selected(self, item):
        """
        Selects the given item.

        Args:
            item (LeafProjectTreeItem)
        """
        ind = self._project_item_model.find_item(item.name)
        self._toolbox.ui.treeView_project.setCurrentIndex(ind)

    def make_and_add_project_items(self, item_type, items, set_selected=False, verbosity=True):
        """Adds items to project at loading.

        Args:
            item_type (str): Item type e.g. "Tool"
            items (list): one or more dict of items to add
            set_selected (bool): Whether to set item selected after the item has been added to project
            verbosity (bool): If True, prints message
        """
        for category_ind, project_tree_items in self.make_project_tree_items(item_type, items).items():
            if not category_ind:
                continue
            self.do_add_project_tree_items(
                category_ind, *project_tree_items, set_selected=set_selected, verbosity=verbosity
            )
        return True

    def add_to_dag(self, item_name):
        """Add new node (project item) to the directed graph."""
        self.dag_handler.add_dag_node(item_name)

    def remove_all_items(self):
        """Pushes a RemoveAllProjectItemsCommand to the toolbox undo stack.
        """
        items_per_category = self._project_item_model.items_per_category()
        if not any(v for v in items_per_category.values()):
            self._logger.msg.emit("No project items to remove")
            return
        delete_data = int(self._settings.value("appSettings/deleteData", defaultValue="0")) != 0
        msg = "Remove all items from project?"
        if not delete_data:
            msg += "Item data directory will still be available in the project directory after this operation."
        else:
            msg += "<br><br><b>Warning: Item data will be permanently lost after this operation.</b>"
        message_box = QMessageBox(
            QMessageBox.Question,
            "Remove All Items",
            msg,
            buttons=QMessageBox.Ok | QMessageBox.Cancel,
            parent=self._toolbox,
        )
        message_box.button(QMessageBox.Ok).setText("Remove Items")
        answer = message_box.exec_()
        if answer != QMessageBox.Ok:
            return
        links = self._toolbox.ui.graphicsView.links()
        self._toolbox.undo_stack.push(
            RemoveAllProjectItemsCommand(self, items_per_category, links, delete_data=delete_data)
        )

    def remove_item(self, name, check_dialog=False):
        """Pushes a RemoveProjectItemCommand to the toolbox undo stack.

        Args:
            name (str): Item's name
            check_dialog (bool): If True, shows 'Are you sure?' message box
        """
        delete_data = int(self._settings.value("appSettings/deleteData", defaultValue="0")) != 0
        if check_dialog:
            msg = "Remove item <b>{}</b> from project? ".format(name)
            if not delete_data:
                msg += "Item data directory will still be available in the project directory after this operation."
            else:
                msg += "<br><br><b>Warning: Item data will be permanently lost after this operation.</b>"
            msg += "<br><br>Tip: Remove items by pressing 'Delete' key to bypass this dialog."
            # noinspection PyCallByClass, PyTypeChecker
            message_box = QMessageBox(
                QMessageBox.Question,
                "Remove Item",
                msg,
                buttons=QMessageBox.Ok | QMessageBox.Cancel,
                parent=self._toolbox,
            )
            message_box.button(QMessageBox.Ok).setText("Remove Item")
            answer = message_box.exec_()
            if answer != QMessageBox.Ok:
                return
        self._toolbox.undo_stack.push(RemoveProjectItemCommand(self, name, delete_data=delete_data))

    def do_remove_item(self, name):
        """Removes item from project given its name.
        This method is used when closing the existing project for opening a new one.

        Args:
            name (str): Item's name
        """
        ind = self._project_item_model.find_item(name)
        category_ind = ind.parent()
        item = self._project_item_model.item(ind)
        self._remove_item(category_ind, item)

    def _remove_item(self, category_ind, item, delete_data=False):
        """
        Removes LeafProjectTreeItem from project.

        Args:
            category_ind (QModelIndex): The category index
            item (LeafProjectTreeItem): the item to remove
            delete_data (bool): If set to True, deletes the directories and data associated with the item
        """
        try:
            data_dir = item.project_item.data_dir
        except AttributeError:
            data_dir = None
        # Remove item from project model
        if not self._project_item_model.remove_item(item, parent=category_ind):
            self._logger.msg_error.emit("Removing item <b>{0}</b> from project failed".format(item.name))
        # Remove item icon and connected links (QGraphicsItems) from scene
        icon = item.project_item.get_icon()
        self._toolbox.ui.graphicsView.remove_icon(icon)
        self.dag_handler.remove_node_from_graph(item.name)
        item.project_item.tear_down()
        if delete_data:
            if data_dir:
                # Remove data directory and all its contents
                self._logger.msg.emit("Removing directory <b>{0}</b>".format(data_dir))
                try:
                    if not erase_dir(data_dir):
                        self._logger.msg_error.emit("Directory does not exist")
                except OSError:
                    self._logger.msg_error.emit("[OSError] Removing directory failed. Check directory permissions.")
            self._logger.msg.emit("Item <b>{0}</b> removed from project".format(item.name))

    def execute_dags(self, dags, execution_permits):
        """Executes given dags.

        Args:
            dags (Sequence(DiGraph))
            execution_permits (Sequence(dict))
        """
        self._execution_stopped = False
        self._dag_execution_list = list(dags)
        self._dag_execution_permits_list = list(execution_permits)
        self._dag_execution_index = 0
        self.execute_next_dag()

    @Slot()
    def execute_next_dag(self):
        """Executes next dag in the execution list."""
        if self._execution_stopped:
            return
        try:
            dag = self._dag_execution_list[self._dag_execution_index]
            execution_permits = self._dag_execution_permits_list[self._dag_execution_index]
        except IndexError:
            return
        dag_identifier = f"{self._dag_execution_index + 1}/{len(self._dag_execution_list)}"
        self.execute_dag(dag, execution_permits, dag_identifier)
        self._dag_execution_index += 1
        self.dag_execution_finished.emit()

    def execute_dag(self, dag, execution_permits, dag_identifier):
        """Executes given dag.

        Args:
            dag (DiGraph): Executed DAG
            execution_permits (dict): Dictionary, where keys are node names in dag and value is a boolean
            dag_identifier (str): Identifier number for printing purposes
        """
        node_successors = self.dag_handler.node_successors(dag)
        if not node_successors:
            self._logger.msg_warning.emit("<b>Graph {0} is not a Directed Acyclic Graph</b>".format(dag_identifier))
            self._logger.msg.emit("Items in graph: {0}".format(", ".join(dag.nodes())))
            edges = ["{0} -> {1}".format(*edge) for edge in self.dag_handler.edges_causing_loops(dag)]
            self._logger.msg.emit(
                "Please edit connections in Design View to execute it. "
                "Possible fix: remove connection(s) {0}.".format(", ".join(edges))
            )
            return
        items = [self._project_item_model.get_item(name).project_item.execution_item() for name in node_successors]
        self.engine = SpineEngine(items, node_successors, execution_permits)
        self.engine.dag_node_execution_finished.connect(self._notify_item_for_finished_execution)
        self.dag_execution_about_to_start.emit(self.engine)
        self._logger.msg.emit("<b>Starting DAG {0}</b>".format(dag_identifier))
        self._logger.msg.emit("Order: {0}".format(" -> ".join(list(node_successors))))
        self.engine.run()
        outcome = {
            SpineEngineState.USER_STOPPED: "stopped by the user",
            SpineEngineState.FAILED: "failed",
            SpineEngineState.COMPLETED: "completed successfully",
        }[self.engine.state()]
        self._logger.msg.emit("<b>DAG {0} {1}</b>".format(dag_identifier, outcome))
        self.engine.dag_node_execution_finished.disconnect(self._notify_item_for_finished_execution)

    def execute_selected(self):
        """Executes DAGs corresponding to all selected project items."""
        if not self.dag_handler.dags():
            self._logger.msg_warning.emit("Project has no items to execute")
            return
        # Get selected item
        selected_indexes = self._toolbox.ui.treeView_project.selectedIndexes()
        if not selected_indexes:
            self._logger.msg_warning.emit("Please select a project item and try again.")
            return
        dags = set()
        executable_item_names = list()
        for ind in selected_indexes:
            item = self._project_item_model.item(ind)
            executable_item_names.append(item.name)
            dag = self.dag_handler.dag_with_node(item.name)
            if not dag:
                self._logger.msg_error.emit(
                    "[BUG] Could not find a graph containing {0}. "
                    "<b>Please reopen the project.</b>".format(item.name)
                )
                continue
            dags.add(dag)
        execution_permit_list = list()
        for dag in dags:
            execution_permits = dict()
            for item_name in dag.nodes:
                execution_permits[item_name] = item_name in executable_item_names
            execution_permit_list.append(execution_permits)
        self._logger.msg.emit("")
        self._logger.msg.emit("-------------------------------------------------")
        self._logger.msg.emit("<b>Executing Selected Directed Acyclic Graphs</b>")
        self._logger.msg.emit("-------------------------------------------------")
        self.execute_dags(dags, execution_permit_list)
        for name in executable_item_names:
            # Make sure transient files and file pattern resources get updated throughout the DAG
            self.notify_changes_in_containing_dag(name)

    def execute_project(self):
        """Executes all dags in the project."""
        self.project_execution_about_to_start.emit()
        dags = self.dag_handler.dags()
        if not dags:
            self._logger.msg_warning.emit("Project has no items to execute")
            return
        execution_permit_list = list()
        for dag in dags:
            execution_permit_list.append({item_name: True for item_name in dag.nodes})
        self._logger.msg.emit("")
        self._logger.msg.emit("--------------------------------------------")
        self._logger.msg.emit("<b>Executing All Directed Acyclic Graphs</b>")
        self._logger.msg.emit("--------------------------------------------")
        self.execute_dags(dags, execution_permit_list)

    def stop(self):
        """Stops execution. Slot for the main window Stop tool button in the toolbar."""
        if self._execution_stopped:
            self._logger.msg.emit("No execution in progress")
            return
        self._logger.msg.emit("Stopping...")
        self._execution_stopped = True
        if self.engine:
            self.engine.stop()

    def export_graphs(self):
        """Exports all valid directed acyclic graphs in project to GraphML files."""
        if not self.dag_handler.dags():
            self._logger.msg_warning.emit("Project has no graphs to export")
            return
        i = 0
        for g in self.dag_handler.dags():
            fn = str(i) + ".graphml"
            path = os.path.join(self.project_dir, fn)
            if not self.dag_handler.export_to_graphml(g, path):
                self._logger.msg_warning.emit("Exporting graph nr. {0} failed. Not a directed acyclic graph".format(i))
            else:
                self._logger.msg.emit("Graph nr. {0} exported to {1}".format(i, path))
            i += 1

    @Slot("QVariant")
    def notify_changes_in_dag(self, dag):
        """Notifies the items in given dag that the dag has changed."""
        node_successors = self.dag_handler.node_successors(dag)
        if not node_successors:
            # Not a dag, invalidate workflow
            edges = self.dag_handler.edges_causing_loops(dag)
            for node in dag.nodes():
                ind = self._project_item_model.find_item(node)
                project_item = self._project_item_model.item(ind).project_item
                project_item.invalidate_workflow(edges)
            return
        # Make resource map and run simulation
        node_predecessors = inverted(node_successors)
        for rank, item_name in enumerate(node_successors):
            item = self._project_item_model.get_item(item_name).project_item
            resources = []
            for parent_name in node_predecessors.get(item_name, set()):
                parent_item = self._project_item_model.get_item(parent_name).project_item
                resources += parent_item.resources_for_direct_successors()
            item.handle_dag_changed(rank, resources)

    def notify_changes_in_all_dags(self):
        """Notifies all items of changes in all dags in the project."""
        for g in self.dag_handler.dags():
            self.notify_changes_in_dag(g)

    def notify_changes_in_containing_dag(self, item):
        """Notifies items in dag containing the given item that the dag has changed."""
        dag = self.dag_handler.dag_with_node(item)
        # Some items trigger this method while they are being initialized
        # but before they have been added to any DAG.
        # In those cases we don't need to notify other items.
        if dag:
            self.notify_changes_in_dag(dag)

    @property
    def settings(self):
        return self._settings

    @Slot(str, "QVariant", "QVariant")
    def _notify_item_for_finished_execution(self, item_name, execution_direction, engine_state):
        """Notifies a project item that its execution counterpart has been executed successfully."""
        item = self._project_item_model.get_item(item_name)
        if item is None:
            return
        item.project_item.executed_successfully(execution_direction, engine_state)

    def direct_successors(self, item):
        """Returns a list of direct successor nodes for given project item."""
        item_name = item.name
        dags = self.dag_handler.dags()
        for dag in dags:
            successors = self.dag_handler.node_successors(dag)
            items_successors = successors.get(item_name)
            if items_successors is not None:
                return [self._project_item_model.get_item(successor).project_item for successor in items_successors]
        return []


def _legacy_type_from_category(category_name):
    """
    Returns an item type for a project item in given category if item_type is missing from item dict.

    This is for backwards compatibility with old .proj files where the project items did not store their type
    in the item dict.

    Args:
        category_name (str): category name
    Returns:
        str: item type
    """
    category_to_item_type = {
        "Data Connections": "Data Connection",
        "Data Stores": "Data Store",
        "Exporters": "Exporter",
        "Importers": "Importer",
        "Tools": "Tool",
        "Views": "View",
    }
    return category_to_item_type[category_name]
