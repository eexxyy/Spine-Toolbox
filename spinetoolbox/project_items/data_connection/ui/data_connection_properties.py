# -*- coding: utf-8 -*-
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

# Form implementation generated from reading ui file 'C:\data\GIT\SPINETOOLBOX\bin\..\spinetoolbox\project_items\data_connection\ui\data_connection_properties.ui',
# licensing of 'C:\data\GIT\SPINETOOLBOX\bin\..\spinetoolbox\project_items\data_connection\ui\data_connection_properties.ui' applies.
#
# Created: Thu Dec  5 16:38:27 2019
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(294, 524)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_dc_name = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_dc_name.sizePolicy().hasHeightForWidth())
        self.label_dc_name.setSizePolicy(sizePolicy)
        self.label_dc_name.setMinimumSize(QtCore.QSize(0, 20))
        self.label_dc_name.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(50)
        font.setBold(False)
        self.label_dc_name.setFont(font)
        self.label_dc_name.setStyleSheet("background-color: #ecd8c6;")
        self.label_dc_name.setFrameShape(QtWidgets.QFrame.Box)
        self.label_dc_name.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_dc_name.setAlignment(QtCore.Qt.AlignCenter)
        self.label_dc_name.setWordWrap(True)
        self.label_dc_name.setObjectName("label_dc_name")
        self.verticalLayout.addWidget(self.label_dc_name)
        self.scrollArea_2 = QtWidgets.QScrollArea(Form)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 292, 502))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.treeView_dc_references = ReferencesTreeView(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeView_dc_references.sizePolicy().hasHeightForWidth())
        self.treeView_dc_references.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.treeView_dc_references.setFont(font)
        self.treeView_dc_references.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView_dc_references.setAcceptDrops(True)
        self.treeView_dc_references.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeView_dc_references.setTextElideMode(QtCore.Qt.ElideLeft)
        self.treeView_dc_references.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.treeView_dc_references.setIndentation(5)
        self.treeView_dc_references.setUniformRowHeights(True)
        self.treeView_dc_references.setObjectName("treeView_dc_references")
        self.treeView_dc_references.header().setStretchLastSection(True)
        self.verticalLayout_16.addWidget(self.treeView_dc_references)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.toolButton_plus = QtWidgets.QToolButton(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_plus.sizePolicy().hasHeightForWidth())
        self.toolButton_plus.setSizePolicy(sizePolicy)
        self.toolButton_plus.setMinimumSize(QtCore.QSize(22, 22))
        self.toolButton_plus.setMaximumSize(QtCore.QSize(22, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.toolButton_plus.setFont(font)
        self.toolButton_plus.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/plus.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_plus.setIcon(icon)
        self.toolButton_plus.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.toolButton_plus.setObjectName("toolButton_plus")
        self.horizontalLayout_2.addWidget(self.toolButton_plus)
        self.toolButton_minus = QtWidgets.QToolButton(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_minus.sizePolicy().hasHeightForWidth())
        self.toolButton_minus.setSizePolicy(sizePolicy)
        self.toolButton_minus.setMinimumSize(QtCore.QSize(22, 22))
        self.toolButton_minus.setMaximumSize(QtCore.QSize(22, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.toolButton_minus.setFont(font)
        self.toolButton_minus.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/minus.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_minus.setIcon(icon1)
        self.toolButton_minus.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.toolButton_minus.setObjectName("toolButton_minus")
        self.horizontalLayout_2.addWidget(self.toolButton_minus)
        self.toolButton_add = QtWidgets.QToolButton(self.scrollAreaWidgetContents_2)
        self.toolButton_add.setMinimumSize(QtCore.QSize(22, 22))
        self.toolButton_add.setMaximumSize(QtCore.QSize(22, 22))
        self.toolButton_add.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/file-download.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_add.setIcon(icon2)
        self.toolButton_add.setIconSize(QtCore.QSize(16, 16))
        self.toolButton_add.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.toolButton_add.setObjectName("toolButton_add")
        self.horizontalLayout_2.addWidget(self.toolButton_add)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_16.addLayout(self.horizontalLayout_2)
        self.treeView_dc_data = DataTreeView(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeView_dc_data.sizePolicy().hasHeightForWidth())
        self.treeView_dc_data.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.treeView_dc_data.setFont(font)
        self.treeView_dc_data.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView_dc_data.setAcceptDrops(True)
        self.treeView_dc_data.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeView_dc_data.setTextElideMode(QtCore.Qt.ElideLeft)
        self.treeView_dc_data.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.treeView_dc_data.setIndentation(5)
        self.treeView_dc_data.setUniformRowHeights(True)
        self.treeView_dc_data.setObjectName("treeView_dc_data")
        self.treeView_dc_data.header().setStretchLastSection(True)
        self.verticalLayout_16.addWidget(self.treeView_dc_data)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_datapackage = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_datapackage.sizePolicy().hasHeightForWidth())
        self.pushButton_datapackage.setSizePolicy(sizePolicy)
        self.pushButton_datapackage.setMinimumSize(QtCore.QSize(91, 23))
        self.pushButton_datapackage.setMaximumSize(QtCore.QSize(16777215, 23))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/datapkg.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_datapackage.setIcon(icon3)
        self.pushButton_datapackage.setObjectName("pushButton_datapackage")
        self.horizontalLayout_3.addWidget(self.pushButton_datapackage)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.horizontalLayout_3.setStretch(1, 1)
        self.verticalLayout_16.addLayout(self.horizontalLayout_3)
        self.line_3 = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_16.addWidget(self.line_3)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem2)
        self.toolButton_dc_open_dir = QtWidgets.QToolButton(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_dc_open_dir.sizePolicy().hasHeightForWidth())
        self.toolButton_dc_open_dir.setSizePolicy(sizePolicy)
        self.toolButton_dc_open_dir.setMinimumSize(QtCore.QSize(22, 22))
        self.toolButton_dc_open_dir.setMaximumSize(QtCore.QSize(22, 22))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/menu_icons/folder-open-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_dc_open_dir.setIcon(icon4)
        self.toolButton_dc_open_dir.setObjectName("toolButton_dc_open_dir")
        self.horizontalLayout_7.addWidget(self.toolButton_dc_open_dir)
        self.verticalLayout_16.addLayout(self.horizontalLayout_7)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout.addWidget(self.scrollArea_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.label_dc_name.setText(QtWidgets.QApplication.translate("Form", "Name", None, -1))
        self.treeView_dc_references.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Drag-and-drop files here, they will be added as references.</p></body></html>", None, -1))
        self.toolButton_plus.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Add references</p></body></html>", None, -1))
        self.toolButton_minus.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Remove selected references or all if nothing is selected</p></body></html>", None, -1))
        self.toolButton_add.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Add references to project. Copies files to Data connection\'s directory.</p></body></html>", None, -1))
        self.treeView_dc_data.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Drag-and-drop files here, they will be copied to the data directory.</p></body></html>", None, -1))
        self.pushButton_datapackage.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Open Spine datapackage editor</p></body></html>", None, -1))
        self.pushButton_datapackage.setText(QtWidgets.QApplication.translate("Form", "Datapackage", None, -1))
        self.toolButton_dc_open_dir.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Open this Data Connection\'s project directory in file browser</p></body></html>", None, -1))

from spinetoolbox.widgets.custom_qtreeview import DataTreeView, ReferencesTreeView
from spinetoolbox import resources_icons_rc
