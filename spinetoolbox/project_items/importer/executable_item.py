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
Contains Importer's executable item as well as support utilities.

:authors: A. Soininen (VTT)
:date:   1.4.2020
"""
import os
import pathlib
from PySide2.QtCore import QObject, QEventLoop, Signal, Slot
from spinetoolbox.executable_item_base import ExecutableItemBase
from spinetoolbox.spine_io.gdx_utils import find_gams_directory
from . import importer_program
from .item_info import ItemInfo
from .utils import deserialize_mappings
from ..shared.helpers import make_python_process


class ExecutableItem(ExecutableItemBase, QObject):

    importing_finished = Signal()
    """Emitted after the separate import process has finished executing."""

    def __init__(self, name, settings, logs_dir, python_path, gams_path, cancel_on_error, logger):
        """
        Args:
            name (str): Importer's name
            settings (dict): import mappings
            logs_dir (str): path to the directory where logs should be stored
            python_path (str): path to the system's python executable
            gams_path (str): path to system's GAMS executable or empty string for the default path
            cancel_on_error (bool): if True, revert changes on error and quit
            logger (LoggerInterface): a logger
        """
        ExecutableItemBase.__init__(self, name, logger)
        QObject.__init__(self)
        self._settings = settings
        self._logs_dir = logs_dir
        self._python_path = python_path
        self._gams_path = gams_path
        self._cancel_on_error = cancel_on_error
        self._resources_from_downstream = list()
        self._importer_process = None
        self._importer_process_successful = None

    @staticmethod
    def item_type():
        """Returns ImporterExecutable's type identifier string."""
        return ItemInfo.item_type()

    def stop_execution(self):
        """Stops executing this ImporterExecutable."""
        super().stop_execution()
        if self._importer_process is None:
            return
        self._importer_process.kill()

    def _execute_backward(self, resources):
        """See base class."""
        self._resources_from_downstream = resources.copy()
        return True

    def _execute_forward(self, resources):
        """See base class."""
        if not self._settings:
            return True
        absolute_paths = _files_from_resources(resources)
        absolute_path_settings = dict()
        for label in self._settings:
            absolute_path = absolute_paths.get(label)
            if absolute_path is not None:
                absolute_path_settings[absolute_path] = self._settings[label]
        source_settings = {"GdxConnector": {"gams_directory": self._gams_system_directory()}}
        # Collect arguments for the importer_program
        import_args = [
            list(absolute_paths.values()),
            absolute_path_settings,
            source_settings,
            [r.url for r in self._resources_from_downstream if r.type_ == "database"],
            self._logs_dir,
            self._cancel_on_error,
        ]
        if not self._prepare_importer_program(import_args):
            self._logger.msg_error.emit(f"Executing Importer {self.name} failed.")
            return False
        self._importer_process.start_execution()
        loop = QEventLoop()
        self.importing_finished.connect(loop.quit)
        # Wait for finished right here
        loop.exec_()
        # This should be executed after the import process has finished
        if not self._importer_process_successful:
            self._logger.msg_error.emit(f"Executing Importer {self.name} failed.")
        else:
            self._logger.msg_success.emit(f"Executing Importer {self.name} finished")
        return self._importer_process_successful

    def _prepare_importer_program(self, importer_args):
        """Prepares an execution manager instance for running
        importer_program.py in a QProcess.

        Args:
            importer_args (list): Arguments for the importer_program. Source file paths, their mapping specs,
                URLs downstream, logs directory, cancel_on_error

        Returns:
            bool: True if preparing the program succeeded, False otherwise.

        """
        self._importer_process = make_python_process(
            importer_program.__file__, importer_args, self._python_path, self._logger
        )
        if self._importer_process is None:
            return False
        self._importer_process.execution_finished.connect(self._handle_importer_program_process_finished)
        return True

    @Slot(int)
    def _handle_importer_program_process_finished(self, exit_code):
        """Handles the return value from importer program when it has finished.
        Emits a signal to indicate that this Importer has been executed.

        Args:
            exit_code (int): Process return value. 0: success, !0: failure
        """
        self._importer_process.execution_finished.disconnect()
        self._importer_process.deleteLater()
        self._importer_process = None
        self._importer_process_successful = exit_code == 0
        self.importing_finished.emit()

    def _gams_system_directory(self):
        """Returns GAMS system path or None if GAMS default is to be used."""
        path = self._gams_path
        if not path:
            path = find_gams_directory()
        if path is not None and os.path.isfile(path):
            path = os.path.dirname(path)
        return path

    @classmethod
    def from_dict(cls, item_dict, name, project_dir, app_settings, specifications, logger):
        """See base class."""
        settings = deserialize_mappings(item_dict["mappings"], project_dir)
        data_dir = pathlib.Path(project_dir, ".spinetoolbox", "items", item_dict["short name"])
        logs_dir = os.path.join(data_dir, "logs")
        python_path = app_settings.value("appSettings/pythonPath", defaultValue="")
        gams_path = app_settings.value("appSettings/gamsPath", defaultValue=None)
        cancel_on_error = item_dict["cancel_on_error"]
        return cls(name, settings, logs_dir, python_path, gams_path, cancel_on_error, logger)


def _files_from_resources(resources):
    """Returns a list of files available in given resources."""
    files = dict()
    for resource in resources:
        if resource.type_ == "file":
            files[resource.path] = resource.path
        elif resource.type_ == "transient_file":
            files[resource.metadata["label"]] = resource.path
    return files
