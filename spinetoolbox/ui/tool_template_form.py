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

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../spinetoolbox/ui/tool_template_form.ui',
# licensing of '../spinetoolbox/ui/tool_template_form.ui' applies.
#
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.ApplicationModal)
        Form.resize(600, 760)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setStyleSheet("")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_name = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_name.sizePolicy().hasHeightForWidth())
        self.lineEdit_name.setSizePolicy(sizePolicy)
        self.lineEdit_name.setMinimumSize(QtCore.QSize(220, 24))
        self.lineEdit_name.setMaximumSize(QtCore.QSize(5000, 24))
        self.lineEdit_name.setClearButtonEnabled(True)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.horizontalLayout.addWidget(self.lineEdit_name)
        self.comboBox_tooltype = QtWidgets.QComboBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_tooltype.sizePolicy().hasHeightForWidth())
        self.comboBox_tooltype.setSizePolicy(sizePolicy)
        self.comboBox_tooltype.setMinimumSize(QtCore.QSize(180, 24))
        self.comboBox_tooltype.setMaximumSize(QtCore.QSize(16777215, 24))
        self.comboBox_tooltype.setCurrentText("")
        self.comboBox_tooltype.setObjectName("comboBox_tooltype")
        self.horizontalLayout.addWidget(self.comboBox_tooltype)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.checkBox_execute_in_work = QtWidgets.QCheckBox(Form)
        self.checkBox_execute_in_work.setChecked(True)
        self.checkBox_execute_in_work.setObjectName("checkBox_execute_in_work")
        self.verticalLayout_5.addWidget(self.checkBox_execute_in_work)
        self.textEdit_description = QtWidgets.QTextEdit(Form)
        self.textEdit_description.setMaximumSize(QtCore.QSize(16777215, 80))
        self.textEdit_description.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.textEdit_description.setTabChangesFocus(True)
        self.textEdit_description.setObjectName("textEdit_description")
        self.verticalLayout_5.addWidget(self.textEdit_description)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.lineEdit_main_program = CustomQLineEdit(Form)
        self.lineEdit_main_program.setClearButtonEnabled(True)
        self.lineEdit_main_program.setObjectName("lineEdit_main_program")
        self.horizontalLayout_6.addWidget(self.lineEdit_main_program)
        self.toolButton_add_main_program = QtWidgets.QToolButton(Form)
        self.toolButton_add_main_program.setMaximumSize(QtCore.QSize(22, 22))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/file.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_add_main_program.setIcon(icon)
        self.toolButton_add_main_program.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.toolButton_add_main_program.setAutoRaise(False)
        self.toolButton_add_main_program.setObjectName("toolButton_add_main_program")
        self.horizontalLayout_6.addWidget(self.toolButton_add_main_program)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.lineEdit_args = QtWidgets.QLineEdit(Form)
        self.lineEdit_args.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_args.sizePolicy().hasHeightForWidth())
        self.lineEdit_args.setSizePolicy(sizePolicy)
        self.lineEdit_args.setMinimumSize(QtCore.QSize(220, 24))
        self.lineEdit_args.setMaximumSize(QtCore.QSize(5000, 24))
        self.lineEdit_args.setClearButtonEnabled(True)
        self.lineEdit_args.setObjectName("lineEdit_args")
        self.verticalLayout_5.addWidget(self.lineEdit_args)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeView_sourcefiles = SourcesTreeView(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeView_sourcefiles.sizePolicy().hasHeightForWidth())
        self.treeView_sourcefiles.setSizePolicy(sizePolicy)
        self.treeView_sourcefiles.setMaximumSize(QtCore.QSize(16777215, 200))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.treeView_sourcefiles.setFont(font)
        self.treeView_sourcefiles.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.treeView_sourcefiles.setAcceptDrops(True)
        self.treeView_sourcefiles.setLineWidth(1)
        self.treeView_sourcefiles.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeView_sourcefiles.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.treeView_sourcefiles.setIndentation(5)
        self.treeView_sourcefiles.setObjectName("treeView_sourcefiles")
        self.verticalLayout.addWidget(self.treeView_sourcefiles)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.toolButton_add_source_files = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_add_source_files.sizePolicy().hasHeightForWidth())
        self.toolButton_add_source_files.setSizePolicy(sizePolicy)
        self.toolButton_add_source_files.setMinimumSize(QtCore.QSize(22, 22))
        self.toolButton_add_source_files.setMaximumSize(QtCore.QSize(22, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.toolButton_add_source_files.setFont(font)
        self.toolButton_add_source_files.setText("")
        self.toolButton_add_source_files.setIcon(icon)
        self.toolButton_add_source_files.setObjectName("toolButton_add_source_files")
        self.horizontalLayout_2.addWidget(self.toolButton_add_source_files)
        self.toolButton_add_source_dirs = QtWidgets.QToolButton(Form)
        self.toolButton_add_source_dirs.setMinimumSize(QtCore.QSize(22, 22))
        self.toolButton_add_source_dirs.setMaximumSize(QtCore.QSize(22, 22))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/folder.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_add_source_dirs.setIcon(icon1)
        self.toolButton_add_source_dirs.setObjectName("toolButton_add_source_dirs")
        self.horizontalLayout_2.addWidget(self.toolButton_add_source_dirs)
        self.toolButton_minus_source_files = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_minus_source_files.sizePolicy().hasHeightForWidth())
        self.toolButton_minus_source_files.setSizePolicy(sizePolicy)
        self.toolButton_minus_source_files.setMinimumSize(QtCore.QSize(22, 22))
        self.toolButton_minus_source_files.setMaximumSize(QtCore.QSize(22, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.toolButton_minus_source_files.setFont(font)
        self.toolButton_minus_source_files.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/menu_icons/trash-alt.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_minus_source_files.setIcon(icon2)
        self.toolButton_minus_source_files.setObjectName("toolButton_minus_source_files")
        self.horizontalLayout_2.addWidget(self.toolButton_minus_source_files)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.treeView_inputfiles = CustomTreeView(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeView_inputfiles.sizePolicy().hasHeightForWidth())
        self.treeView_inputfiles.setSizePolicy(sizePolicy)
        self.treeView_inputfiles.setMaximumSize(QtCore.QSize(16777215, 500))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.treeView_inputfiles.setFont(font)
        self.treeView_inputfiles.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.treeView_inputfiles.setLineWidth(1)
        self.treeView_inputfiles.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeView_inputfiles.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.treeView_inputfiles.setIndentation(5)
        self.treeView_inputfiles.setUniformRowHeights(False)
        self.treeView_inputfiles.setObjectName("treeView_inputfiles")
        self.verticalLayout_3.addWidget(self.treeView_inputfiles)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.toolButton_plus_inputfiles = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_plus_inputfiles.sizePolicy().hasHeightForWidth())
        self.toolButton_plus_inputfiles.setSizePolicy(sizePolicy)
        self.toolButton_plus_inputfiles.setMinimumSize(QtCore.QSize(22, 22))
        self.toolButton_plus_inputfiles.setMaximumSize(QtCore.QSize(22, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.toolButton_plus_inputfiles.setFont(font)
        self.toolButton_plus_inputfiles.setText("")
        self.toolButton_plus_inputfiles.setIcon(icon)
        self.toolButton_plus_inputfiles.setObjectName("toolButton_plus_inputfiles")
        self.horizontalLayout_4.addWidget(self.toolButton_plus_inputfiles)
        self.toolButton_minus_inputfiles = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_minus_inputfiles.sizePolicy().hasHeightForWidth())
        self.toolButton_minus_inputfiles.setSizePolicy(sizePolicy)
        self.toolButton_minus_inputfiles.setMinimumSize(QtCore.QSize(22, 22))
        self.toolButton_minus_inputfiles.setMaximumSize(QtCore.QSize(22, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.toolButton_minus_inputfiles.setFont(font)
        self.toolButton_minus_inputfiles.setText("")
        self.toolButton_minus_inputfiles.setIcon(icon2)
        self.toolButton_minus_inputfiles.setObjectName("toolButton_minus_inputfiles")
        self.horizontalLayout_4.addWidget(self.toolButton_minus_inputfiles)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 1, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.treeView_inputfiles_opt = CustomTreeView(Form)
        self.treeView_inputfiles_opt.setMaximumSize(QtCore.QSize(16777215, 500))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.treeView_inputfiles_opt.setFont(font)
        self.treeView_inputfiles_opt.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.treeView_inputfiles_opt.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeView_inputfiles_opt.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.treeView_inputfiles_opt.setIndentation(5)
        self.treeView_inputfiles_opt.setObjectName("treeView_inputfiles_opt")
        self.verticalLayout_4.addWidget(self.treeView_inputfiles_opt)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.toolButton_plus_inputfiles_opt = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_plus_inputfiles_opt.sizePolicy().hasHeightForWidth())
        self.toolButton_plus_inputfiles_opt.setSizePolicy(sizePolicy)
        self.toolButton_plus_inputfiles_opt.setMinimumSize(QtCore.QSize(22, 22))
        self.toolButton_plus_inputfiles_opt.setMaximumSize(QtCore.QSize(22, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.toolButton_plus_inputfiles_opt.setFont(font)
        self.toolButton_plus_inputfiles_opt.setText("")
        self.toolButton_plus_inputfiles_opt.setIcon(icon)
        self.toolButton_plus_inputfiles_opt.setObjectName("toolButton_plus_inputfiles_opt")
        self.horizontalLayout_5.addWidget(self.toolButton_plus_inputfiles_opt)
        self.toolButton_minus_inputfiles_opt = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_minus_inputfiles_opt.sizePolicy().hasHeightForWidth())
        self.toolButton_minus_inputfiles_opt.setSizePolicy(sizePolicy)
        self.toolButton_minus_inputfiles_opt.setMinimumSize(QtCore.QSize(22, 22))
        self.toolButton_minus_inputfiles_opt.setMaximumSize(QtCore.QSize(22, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.toolButton_minus_inputfiles_opt.setFont(font)
        self.toolButton_minus_inputfiles_opt.setText("")
        self.toolButton_minus_inputfiles_opt.setIcon(icon2)
        self.toolButton_minus_inputfiles_opt.setObjectName("toolButton_minus_inputfiles_opt")
        self.horizontalLayout_5.addWidget(self.toolButton_minus_inputfiles_opt)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.gridLayout.addLayout(self.verticalLayout_4, 1, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.treeView_outputfiles = CustomTreeView(Form)
        self.treeView_outputfiles.setMaximumSize(QtCore.QSize(16777215, 500))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.treeView_outputfiles.setFont(font)
        self.treeView_outputfiles.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.treeView_outputfiles.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeView_outputfiles.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.treeView_outputfiles.setIndentation(5)
        self.treeView_outputfiles.setObjectName("treeView_outputfiles")
        self.verticalLayout_2.addWidget(self.treeView_outputfiles)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.toolButton_plus_outputfiles = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_plus_outputfiles.sizePolicy().hasHeightForWidth())
        self.toolButton_plus_outputfiles.setSizePolicy(sizePolicy)
        self.toolButton_plus_outputfiles.setMinimumSize(QtCore.QSize(22, 22))
        self.toolButton_plus_outputfiles.setMaximumSize(QtCore.QSize(22, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.toolButton_plus_outputfiles.setFont(font)
        self.toolButton_plus_outputfiles.setText("")
        self.toolButton_plus_outputfiles.setIcon(icon)
        self.toolButton_plus_outputfiles.setObjectName("toolButton_plus_outputfiles")
        self.horizontalLayout_3.addWidget(self.toolButton_plus_outputfiles)
        self.toolButton_minus_outputfiles = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_minus_outputfiles.sizePolicy().hasHeightForWidth())
        self.toolButton_minus_outputfiles.setSizePolicy(sizePolicy)
        self.toolButton_minus_outputfiles.setMinimumSize(QtCore.QSize(22, 22))
        self.toolButton_minus_outputfiles.setMaximumSize(QtCore.QSize(22, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.toolButton_minus_outputfiles.setFont(font)
        self.toolButton_minus_outputfiles.setText("")
        self.toolButton_minus_outputfiles.setIcon(icon2)
        self.toolButton_minus_outputfiles.setObjectName("toolButton_minus_outputfiles")
        self.horizontalLayout_3.addWidget(self.toolButton_minus_outputfiles)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 1, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label = QtWidgets.QLabel(Form)
        self.label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_7.addWidget(self.label)
        self.label_mainpath = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_mainpath.sizePolicy().hasHeightForWidth())
        self.label_mainpath.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        font.setBold(True)
        self.label_mainpath.setFont(font)
        self.label_mainpath.setText("")
        self.label_mainpath.setObjectName("label_mainpath")
        self.horizontalLayout_7.addWidget(self.label_mainpath)
        self.verticalLayout_5.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setContentsMargins(-1, -1, -1, 6)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem4)
        self.pushButton_ok = QtWidgets.QPushButton(Form)
        self.pushButton_ok.setDefault(True)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.horizontalLayout_8.addWidget(self.pushButton_ok)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem5)
        self.pushButton_cancel = QtWidgets.QPushButton(Form)
        self.pushButton_cancel.setDefault(True)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout_8.addWidget(self.pushButton_cancel)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem6)
        self.verticalLayout_5.addLayout(self.horizontalLayout_8)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.horizontalLayout_statusbar_placeholder = QtWidgets.QHBoxLayout()
        self.horizontalLayout_statusbar_placeholder.setObjectName("horizontalLayout_statusbar_placeholder")
        self.widget_invisible_dummy = QtWidgets.QWidget(Form)
        self.widget_invisible_dummy.setObjectName("widget_invisible_dummy")
        self.horizontalLayout_statusbar_placeholder.addWidget(self.widget_invisible_dummy)
        self.verticalLayout_6.addLayout(self.horizontalLayout_statusbar_placeholder)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.lineEdit_name, self.comboBox_tooltype)
        Form.setTabOrder(self.comboBox_tooltype, self.checkBox_execute_in_work)
        Form.setTabOrder(self.checkBox_execute_in_work, self.textEdit_description)
        Form.setTabOrder(self.textEdit_description, self.lineEdit_main_program)
        Form.setTabOrder(self.lineEdit_main_program, self.toolButton_add_main_program)
        Form.setTabOrder(self.toolButton_add_main_program, self.lineEdit_args)
        Form.setTabOrder(self.lineEdit_args, self.treeView_sourcefiles)
        Form.setTabOrder(self.treeView_sourcefiles, self.toolButton_add_source_files)
        Form.setTabOrder(self.toolButton_add_source_files, self.toolButton_add_source_dirs)
        Form.setTabOrder(self.toolButton_add_source_dirs, self.toolButton_minus_source_files)
        Form.setTabOrder(self.toolButton_minus_source_files, self.treeView_inputfiles)
        Form.setTabOrder(self.treeView_inputfiles, self.toolButton_plus_inputfiles)
        Form.setTabOrder(self.toolButton_plus_inputfiles, self.toolButton_minus_inputfiles)
        Form.setTabOrder(self.toolButton_minus_inputfiles, self.treeView_inputfiles_opt)
        Form.setTabOrder(self.treeView_inputfiles_opt, self.toolButton_plus_inputfiles_opt)
        Form.setTabOrder(self.toolButton_plus_inputfiles_opt, self.toolButton_minus_inputfiles_opt)
        Form.setTabOrder(self.toolButton_minus_inputfiles_opt, self.treeView_outputfiles)
        Form.setTabOrder(self.treeView_outputfiles, self.toolButton_plus_outputfiles)
        Form.setTabOrder(self.toolButton_plus_outputfiles, self.toolButton_minus_outputfiles)
        Form.setTabOrder(self.toolButton_minus_outputfiles, self.pushButton_ok)
        Form.setTabOrder(self.pushButton_ok, self.pushButton_cancel)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Edit Tool Template", None, -1))
        self.lineEdit_name.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Tool template name (required)</p></body></html>", None, -1))
        self.lineEdit_name.setPlaceholderText(QtWidgets.QApplication.translate("Form", "Type name here...", None, -1))
        self.comboBox_tooltype.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Tool template type</p></body></html>", None, -1))
        self.checkBox_execute_in_work.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>If checked, Tool template is executed in a work directory (default).</p><p>If unchecked, Tool template is executed in main program file directory.</p><p>It is recommended to uncheck this for <span style=\" font-weight:600;\">Executable</span> Tool templates.</p></body></html>", None, -1))
        self.checkBox_execute_in_work.setText(QtWidgets.QApplication.translate("Form", "Execute in work directory", None, -1))
        self.textEdit_description.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Tool template description (optional)</p></body></html>", None, -1))
        self.textEdit_description.setPlaceholderText(QtWidgets.QApplication.translate("Form", "Type description here...", None, -1))
        self.lineEdit_main_program.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Main program file that is used to launch the Tool template (required)</p></body></html>", None, -1))
        self.lineEdit_main_program.setPlaceholderText(QtWidgets.QApplication.translate("Form", "Add main program file here...", None, -1))
        self.toolButton_add_main_program.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Create a new main program or select an existing one</p></body></html>", None, -1))
        self.lineEdit_args.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Command line arguments (space-delimited) for the main program (optional)</p></body></html>", None, -1))
        self.lineEdit_args.setPlaceholderText(QtWidgets.QApplication.translate("Form", "Type command line arguments here...", None, -1))
        self.treeView_sourcefiles.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Other source files and/or directories (in addition to the main program file) <span style=\" font-weight:600;\">required</span> by the program.</p><p><span style=\" font-weight:600;\">Tip</span>: You can Drag &amp; Drop files and/or directories here from File Explorer.</p></body></html>", None, -1))
        self.toolButton_add_source_files.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Add source code <span style=\" font-weight:600;\">files</span> that your program requires in order to run.</p></body></html>", None, -1))
        self.toolButton_add_source_dirs.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Add source code <span style=\" font-weight:600;\">directory</span> and all its contents.</p></body></html>", None, -1))
        self.toolButton_minus_source_files.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Remove selected item(s)</p></body></html>", None, -1))
        self.treeView_inputfiles.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Required</span> data files for the program.</p><p><span style=\" font-weight:600;\">Tip</span>: Double-click or press F2 to edit selected item.</p></body></html>", None, -1))
        self.toolButton_plus_inputfiles.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Add input filenames and/or directories required by the program. Examples:</p><p>\'data.csv\'</p><p>\'input/data.csv\'</p><p>\'input/\'</p><p>\'output/\'</p><p><br/></p></body></html>", None, -1))
        self.toolButton_minus_inputfiles.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Remove selected item(s)</p></body></html>", None, -1))
        self.treeView_inputfiles_opt.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Optional</span> data files for the program.</p><p><span style=\" font-weight:600;\">Tip</span>: Double-click or press F2 to edit selected item.</p></body></html>", None, -1))
        self.toolButton_plus_inputfiles_opt.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Add optional input filenames and/or directories.</p></body></html>", None, -1))
        self.toolButton_minus_inputfiles_opt.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Remove selected item(s)</p></body></html>", None, -1))
        self.treeView_outputfiles.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Output files that may be used by other project items downstream. These files will be archived into a results directory after execution.</p><p><span style=\" font-weight:600;\">Tip</span>: Double-click or press F2 to edit selected item.</p></body></html>", None, -1))
        self.toolButton_plus_outputfiles.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Add output filenames produced by your program that are saved to results after execution.</p></body></html>", None, -1))
        self.toolButton_minus_outputfiles.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Remove selected item(s)</p></body></html>", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "Main program directory", None, -1))
        self.pushButton_ok.setText(QtWidgets.QApplication.translate("Form", "Ok", None, -1))
        self.pushButton_cancel.setText(QtWidgets.QApplication.translate("Form", "Cancel", None, -1))

from widgets.custom_qlineedit import CustomQLineEdit
from widgets.custom_qtreeview import SourcesTreeView, CustomTreeView
import resources_icons_rc
