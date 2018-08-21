#############################################################################
# Copyright (C) 2017 - 2018 VTT Technical Research Centre of Finland
#
# This file is part of Spine Toolbox.
#
# Spine Toolbox is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#############################################################################

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../spinetoolbox/ui/settings.ui',
# licensing of '../spinetoolbox/ui/settings.ui' applies.
#
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_SettingsForm(object):
    def setupUi(self, SettingsForm):
        SettingsForm.setObjectName("SettingsForm")
        SettingsForm.setWindowModality(QtCore.Qt.ApplicationModal)
        SettingsForm.resize(700, 500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SettingsForm.sizePolicy().hasHeightForWidth())
        SettingsForm.setSizePolicy(sizePolicy)
        SettingsForm.setMinimumSize(QtCore.QSize(700, 500))
        SettingsForm.setMaximumSize(QtCore.QSize(700, 500))
        SettingsForm.setMouseTracking(False)
        SettingsForm.setFocusPolicy(QtCore.Qt.StrongFocus)
        SettingsForm.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        SettingsForm.setAutoFillBackground(False)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(SettingsForm)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setContentsMargins(9, 9, 9, 9)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_general = QtWidgets.QGroupBox(SettingsForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_general.sizePolicy().hasHeightForWidth())
        self.groupBox_general.setSizePolicy(sizePolicy)
        self.groupBox_general.setMinimumSize(QtCore.QSize(0, 164))
        self.groupBox_general.setAutoFillBackground(False)
        self.groupBox_general.setFlat(False)
        self.groupBox_general.setObjectName("groupBox_general")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_general)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.checkBox_open_previous_project = QtWidgets.QCheckBox(self.groupBox_general)
        self.checkBox_open_previous_project.setObjectName("checkBox_open_previous_project")
        self.verticalLayout_6.addWidget(self.checkBox_open_previous_project)
        self.checkBox_exit_prompt = QtWidgets.QCheckBox(self.groupBox_general)
        self.checkBox_exit_prompt.setTristate(False)
        self.checkBox_exit_prompt.setObjectName("checkBox_exit_prompt")
        self.verticalLayout_6.addWidget(self.checkBox_exit_prompt)
        self.checkBox_debug_messages = QtWidgets.QCheckBox(self.groupBox_general)
        self.checkBox_debug_messages.setObjectName("checkBox_debug_messages")
        self.verticalLayout_6.addWidget(self.checkBox_debug_messages)
        self.checkBox_datetime = QtWidgets.QCheckBox(self.groupBox_general)
        self.checkBox_datetime.setObjectName("checkBox_datetime")
        self.verticalLayout_6.addWidget(self.checkBox_datetime)
        self.label = QtWidgets.QLabel(self.groupBox_general)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_6.addWidget(self.label)
        self.lineEdit_project_dir = QtWidgets.QLineEdit(self.groupBox_general)
        self.lineEdit_project_dir.setFocusPolicy(QtCore.Qt.NoFocus)
        self.lineEdit_project_dir.setReadOnly(True)
        self.lineEdit_project_dir.setObjectName("lineEdit_project_dir")
        self.verticalLayout_6.addWidget(self.lineEdit_project_dir)
        self.verticalLayout.addWidget(self.groupBox_general)
        self.groupBox_gams = QtWidgets.QGroupBox(SettingsForm)
        self.groupBox_gams.setObjectName("groupBox_gams")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_gams)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.groupBox_gams)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.lineEdit_gams_path = QtWidgets.QLineEdit(self.groupBox_gams)
        self.lineEdit_gams_path.setClearButtonEnabled(True)
        self.lineEdit_gams_path.setObjectName("lineEdit_gams_path")
        self.gridLayout.addWidget(self.lineEdit_gams_path, 2, 0, 1, 1)
        self.pushButton_browse_gams = QtWidgets.QPushButton(self.groupBox_gams)
        self.pushButton_browse_gams.setMaximumSize(QtCore.QSize(50, 20))
        self.pushButton_browse_gams.setObjectName("pushButton_browse_gams")
        self.gridLayout.addWidget(self.pushButton_browse_gams, 2, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_gams)
        self.groupBox_julia = QtWidgets.QGroupBox(SettingsForm)
        self.groupBox_julia.setObjectName("groupBox_julia")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_julia)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.checkBox_use_repl = QtWidgets.QCheckBox(self.groupBox_julia)
        self.checkBox_use_repl.setObjectName("checkBox_use_repl")
        self.gridLayout_2.addWidget(self.checkBox_use_repl, 1, 0, 1, 1)
        self.lineEdit_julia_path = QtWidgets.QLineEdit(self.groupBox_julia)
        self.lineEdit_julia_path.setClearButtonEnabled(True)
        self.lineEdit_julia_path.setObjectName("lineEdit_julia_path")
        self.gridLayout_2.addWidget(self.lineEdit_julia_path, 3, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_julia)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 2, 0, 1, 1)
        self.pushButton_browse_julia = QtWidgets.QPushButton(self.groupBox_julia)
        self.pushButton_browse_julia.setMaximumSize(QtCore.QSize(50, 20))
        self.pushButton_browse_julia.setObjectName("pushButton_browse_julia")
        self.gridLayout_2.addWidget(self.pushButton_browse_julia, 3, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_julia)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_project = QtWidgets.QGroupBox(SettingsForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_project.sizePolicy().hasHeightForWidth())
        self.groupBox_project.setSizePolicy(sizePolicy)
        self.groupBox_project.setMinimumSize(QtCore.QSize(250, 300))
        self.groupBox_project.setObjectName("groupBox_project")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_project)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox_project)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.lineEdit_project_name = QtWidgets.QLineEdit(self.groupBox_project)
        self.lineEdit_project_name.setCursor(QtCore.Qt.ArrowCursor)
        self.lineEdit_project_name.setFocusPolicy(QtCore.Qt.NoFocus)
        self.lineEdit_project_name.setReadOnly(True)
        self.lineEdit_project_name.setClearButtonEnabled(False)
        self.lineEdit_project_name.setObjectName("lineEdit_project_name")
        self.verticalLayout_2.addWidget(self.lineEdit_project_name)
        self.label_3 = QtWidgets.QLabel(self.groupBox_project)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.textEdit_project_description = QtWidgets.QTextEdit(self.groupBox_project)
        self.textEdit_project_description.setProperty("cursor", QtCore.Qt.IBeamCursor)
        self.textEdit_project_description.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.textEdit_project_description.setStyleSheet(":focus {border: 1px solid black;}")
        self.textEdit_project_description.setTabChangesFocus(True)
        self.textEdit_project_description.setReadOnly(False)
        self.textEdit_project_description.setAcceptRichText(False)
        self.textEdit_project_description.setPlaceholderText("")
        self.textEdit_project_description.setObjectName("textEdit_project_description")
        self.verticalLayout_2.addWidget(self.textEdit_project_description)
        self.label_6 = QtWidgets.QLabel(self.groupBox_project)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lineEdit_work_dir = QtWidgets.QLineEdit(self.groupBox_project)
        self.lineEdit_work_dir.setClearButtonEnabled(True)
        self.lineEdit_work_dir.setObjectName("lineEdit_work_dir")
        self.horizontalLayout_3.addWidget(self.lineEdit_work_dir)
        self.pushButton_browse_work = QtWidgets.QPushButton(self.groupBox_project)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_browse_work.sizePolicy().hasHeightForWidth())
        self.pushButton_browse_work.setSizePolicy(sizePolicy)
        self.pushButton_browse_work.setMaximumSize(QtCore.QSize(50, 20))
        self.pushButton_browse_work.setObjectName("pushButton_browse_work")
        self.horizontalLayout_3.addWidget(self.pushButton_browse_work)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.addWidget(self.groupBox_project)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(-1, 6, -1, 6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_ok = QtWidgets.QPushButton(SettingsForm)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.horizontalLayout.addWidget(self.pushButton_ok)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButton_cancel = QtWidgets.QPushButton(SettingsForm)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout_7.addLayout(self.horizontalLayout)
        self.horizontalLayout_statusbar_placeholder = QtWidgets.QHBoxLayout()
        self.horizontalLayout_statusbar_placeholder.setSpacing(0)
        self.horizontalLayout_statusbar_placeholder.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_statusbar_placeholder.setObjectName("horizontalLayout_statusbar_placeholder")
        self.widget_invisible_dummy = QtWidgets.QWidget(SettingsForm)
        self.widget_invisible_dummy.setMinimumSize(QtCore.QSize(0, 20))
        self.widget_invisible_dummy.setMaximumSize(QtCore.QSize(0, 20))
        self.widget_invisible_dummy.setObjectName("widget_invisible_dummy")
        self.horizontalLayout_statusbar_placeholder.addWidget(self.widget_invisible_dummy)
        self.verticalLayout_7.addLayout(self.horizontalLayout_statusbar_placeholder)

        self.retranslateUi(SettingsForm)
        QtCore.QMetaObject.connectSlotsByName(SettingsForm)
        SettingsForm.setTabOrder(self.checkBox_open_previous_project, self.checkBox_exit_prompt)
        SettingsForm.setTabOrder(self.checkBox_exit_prompt, self.checkBox_debug_messages)
        SettingsForm.setTabOrder(self.checkBox_debug_messages, self.checkBox_datetime)
        SettingsForm.setTabOrder(self.checkBox_datetime, self.lineEdit_project_dir)
        SettingsForm.setTabOrder(self.lineEdit_project_dir, self.lineEdit_gams_path)
        SettingsForm.setTabOrder(self.lineEdit_gams_path, self.pushButton_browse_gams)
        SettingsForm.setTabOrder(self.pushButton_browse_gams, self.checkBox_use_repl)
        SettingsForm.setTabOrder(self.checkBox_use_repl, self.lineEdit_julia_path)
        SettingsForm.setTabOrder(self.lineEdit_julia_path, self.pushButton_browse_julia)
        SettingsForm.setTabOrder(self.pushButton_browse_julia, self.lineEdit_project_name)
        SettingsForm.setTabOrder(self.lineEdit_project_name, self.textEdit_project_description)
        SettingsForm.setTabOrder(self.textEdit_project_description, self.lineEdit_work_dir)
        SettingsForm.setTabOrder(self.lineEdit_work_dir, self.pushButton_browse_work)
        SettingsForm.setTabOrder(self.pushButton_browse_work, self.pushButton_ok)
        SettingsForm.setTabOrder(self.pushButton_ok, self.pushButton_cancel)

    def retranslateUi(self, SettingsForm):
        SettingsForm.setWindowTitle(QtWidgets.QApplication.translate("SettingsForm", "Settings", None, -1))
        self.groupBox_general.setTitle(QtWidgets.QApplication.translate("SettingsForm", "General", None, -1))
        self.checkBox_open_previous_project.setToolTip(QtWidgets.QApplication.translate("SettingsForm", "<html><head/><body><p>If checked, Application opens the project at startup that was open the last time the application was exited</p></body></html>", None, -1))
        self.checkBox_open_previous_project.setText(QtWidgets.QApplication.translate("SettingsForm", "Open previous project at startup", None, -1))
        self.checkBox_exit_prompt.setToolTip(QtWidgets.QApplication.translate("SettingsForm", "<html><head/><body><p>If checked, confirm exit prompt is shown. If unchecked, application exits without prompt.</p></body></html>", None, -1))
        self.checkBox_exit_prompt.setText(QtWidgets.QApplication.translate("SettingsForm", "Show confirm exit prompt", None, -1))
        self.checkBox_debug_messages.setToolTip(QtWidgets.QApplication.translate("SettingsForm", "<html><head/><body><p>If checked, debug messages are shown in console. If unchecked, only error messages are shown.</p></body></html>", None, -1))
        self.checkBox_debug_messages.setText(QtWidgets.QApplication.translate("SettingsForm", "Show Debug messages", None, -1))
        self.checkBox_datetime.setToolTip(QtWidgets.QApplication.translate("SettingsForm", "<html><head/><body><p>If checked, date and time string is appended into Event Log messages</p></body></html>", None, -1))
        self.checkBox_datetime.setText(QtWidgets.QApplication.translate("SettingsForm", "Show date and time in Event Log messages", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("SettingsForm", "Project directory", None, -1))
        self.groupBox_gams.setTitle(QtWidgets.QApplication.translate("SettingsForm", "GAMS", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("SettingsForm", "Path to GAMS executable", None, -1))
        self.lineEdit_gams_path.setToolTip(QtWidgets.QApplication.translate("SettingsForm", "<html><head/><body><p>Path to directory where GAMS and GAMSIDE executables are found</p></body></html>", None, -1))
        self.lineEdit_gams_path.setPlaceholderText(QtWidgets.QApplication.translate("SettingsForm", "Using GAMS executable in system path", None, -1))
        self.pushButton_browse_gams.setText(QtWidgets.QApplication.translate("SettingsForm", "Browse", None, -1))
        self.groupBox_julia.setTitle(QtWidgets.QApplication.translate("SettingsForm", "JULIA", None, -1))
        self.checkBox_use_repl.setText(QtWidgets.QApplication.translate("SettingsForm", "Run Julia Scripts in REPL", None, -1))
        self.lineEdit_julia_path.setToolTip(QtWidgets.QApplication.translate("SettingsForm", "<html><head/><body><p>Path where julia executable is found</p></body></html>", None, -1))
        self.lineEdit_julia_path.setPlaceholderText(QtWidgets.QApplication.translate("SettingsForm", "Using Julia executable in system path", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("SettingsForm", "Path to Julia executable", None, -1))
        self.pushButton_browse_julia.setText(QtWidgets.QApplication.translate("SettingsForm", "Browse", None, -1))
        self.groupBox_project.setTitle(QtWidgets.QApplication.translate("SettingsForm", "Project", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("SettingsForm", "Name", None, -1))
        self.lineEdit_project_name.setToolTip(QtWidgets.QApplication.translate("SettingsForm", "<html><head/><body><p>You can rename project from main window menu <span style=\" font-weight:600;\">File -&gt; Save As...</span></p></body></html>", None, -1))
        self.lineEdit_project_name.setPlaceholderText(QtWidgets.QApplication.translate("SettingsForm", "No project open", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("SettingsForm", "Description", None, -1))
        self.textEdit_project_description.setToolTip(QtWidgets.QApplication.translate("SettingsForm", "Project Description", None, -1))
        self.textEdit_project_description.setHtml(QtWidgets.QApplication.translate("SettingsForm", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("SettingsForm", "Work directory", None, -1))
        self.lineEdit_work_dir.setToolTip(QtWidgets.QApplication.translate("SettingsForm", "<html><head/><body><p>Work directory location. Leave this empty to use default (\\work).</p></body></html>", None, -1))
        self.lineEdit_work_dir.setPlaceholderText(QtWidgets.QApplication.translate("SettingsForm", "Using default directory", None, -1))
        self.pushButton_browse_work.setText(QtWidgets.QApplication.translate("SettingsForm", "Browse", None, -1))
        self.pushButton_ok.setToolTip(QtWidgets.QApplication.translate("SettingsForm", "<html><head/><body><p>Saves changes and closes the window</p></body></html>", None, -1))
        self.pushButton_ok.setText(QtWidgets.QApplication.translate("SettingsForm", "Ok", None, -1))
        self.pushButton_cancel.setToolTip(QtWidgets.QApplication.translate("SettingsForm", "<html><head/><body><p>Closes the window without saving changes</p></body></html>", None, -1))
        self.pushButton_cancel.setText(QtWidgets.QApplication.translate("SettingsForm", "Cancel", None, -1))

