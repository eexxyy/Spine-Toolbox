######################################################################################################################
# Copyright (C) 2017 - 2018 Spine project consortium
# This file is part of Spine Toolbox.
# Spine Toolbox is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../spinetoolbox/ui/graph_view_form.ui',
# licensing of '../spinetoolbox/ui/graph_view_form.ui' applies.
#
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(944, 768)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.graphicsView = GraphViewGraphicsView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setMouseTracking(True)
        self.graphicsView.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout_2.addWidget(self.graphicsView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 944, 28))
        self.menubar.setObjectName("menubar")
        self.menuGraph = QtWidgets.QMenu(self.menubar)
        self.menuGraph.setObjectName("menuGraph")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuDock_Widgets = QtWidgets.QMenu(self.menuView)
        self.menuDock_Widgets.setObjectName("menuDock_Widgets")
        self.menuToolbars = QtWidgets.QMenu(self.menuView)
        self.menuToolbars.setObjectName("menuToolbars")
        self.menuSession = QtWidgets.QMenu(self.menubar)
        self.menuSession.setObjectName("menuSession")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget_item_palette = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_item_palette.setObjectName("dockWidget_item_palette")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.splitter_object_relationship_class = QtWidgets.QSplitter(self.dockWidgetContents)
        self.splitter_object_relationship_class.setOrientation(QtCore.Qt.Vertical)
        self.splitter_object_relationship_class.setObjectName("splitter_object_relationship_class")
        self.frame = QtWidgets.QFrame(self.splitter_object_relationship_class)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.listView_object_class = DragListView(self.frame)
        self.listView_object_class.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.listView_object_class.setFont(font)
        self.listView_object_class.setMouseTracking(True)
        self.listView_object_class.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listView_object_class.setProperty("showDropIndicator", False)
        self.listView_object_class.setDragEnabled(False)
        self.listView_object_class.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.listView_object_class.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.listView_object_class.setIconSize(QtCore.QSize(32, 32))
        self.listView_object_class.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.listView_object_class.setMovement(QtWidgets.QListView.Static)
        self.listView_object_class.setFlow(QtWidgets.QListView.LeftToRight)
        self.listView_object_class.setProperty("isWrapping", True)
        self.listView_object_class.setResizeMode(QtWidgets.QListView.Adjust)
        self.listView_object_class.setGridSize(QtCore.QSize(128, 64))
        self.listView_object_class.setViewMode(QtWidgets.QListView.IconMode)
        self.listView_object_class.setUniformItemSizes(False)
        self.listView_object_class.setWordWrap(True)
        self.listView_object_class.setSelectionRectVisible(True)
        self.listView_object_class.setObjectName("listView_object_class")
        self.verticalLayout_4.addWidget(self.listView_object_class)
        self.frame_2 = QtWidgets.QFrame(self.splitter_object_relationship_class)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(50)
        font.setBold(False)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_5.addWidget(self.label_2)
        self.listView_relationship_class = DragListView(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.listView_relationship_class.setFont(font)
        self.listView_relationship_class.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listView_relationship_class.setProperty("showDropIndicator", False)
        self.listView_relationship_class.setDragEnabled(False)
        self.listView_relationship_class.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.listView_relationship_class.setIconSize(QtCore.QSize(32, 32))
        self.listView_relationship_class.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.listView_relationship_class.setMovement(QtWidgets.QListView.Static)
        self.listView_relationship_class.setFlow(QtWidgets.QListView.LeftToRight)
        self.listView_relationship_class.setProperty("isWrapping", True)
        self.listView_relationship_class.setResizeMode(QtWidgets.QListView.Adjust)
        self.listView_relationship_class.setGridSize(QtCore.QSize(128, 64))
        self.listView_relationship_class.setViewMode(QtWidgets.QListView.IconMode)
        self.listView_relationship_class.setUniformItemSizes(False)
        self.listView_relationship_class.setWordWrap(True)
        self.listView_relationship_class.setObjectName("listView_relationship_class")
        self.verticalLayout_5.addWidget(self.listView_relationship_class)
        self.verticalLayout_3.addWidget(self.splitter_object_relationship_class)
        self.dockWidget_item_palette.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_item_palette)
        self.dockWidget_object_tree = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_object_tree.setObjectName("dockWidget_object_tree")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeView_object = QtWidgets.QTreeView(self.dockWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeView_object.sizePolicy().hasHeightForWidth())
        self.treeView_object.setSizePolicy(sizePolicy)
        self.treeView_object.setEditTriggers(QtWidgets.QAbstractItemView.EditKeyPressed)
        self.treeView_object.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeView_object.setObjectName("treeView_object")
        self.treeView_object.header().setVisible(False)
        self.verticalLayout.addWidget(self.treeView_object)
        self.dockWidget_object_tree.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_object_tree)
        self.dockWidget_parameter = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_parameter.setObjectName("dockWidget_parameter")
        self.dockWidgetContents_parameter = QtWidgets.QWidget()
        self.dockWidgetContents_parameter.setObjectName("dockWidgetContents_parameter")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.dockWidgetContents_parameter)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.splitter_object_relationship_parameter = QtWidgets.QSplitter(self.dockWidgetContents_parameter)
        self.splitter_object_relationship_parameter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_object_relationship_parameter.setObjectName("splitter_object_relationship_parameter")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter_object_relationship_parameter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_11.addWidget(self.label_3)
        self.tabWidget_object_parameter = QtWidgets.QTabWidget(self.verticalLayoutWidget)
        self.tabWidget_object_parameter.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget_object_parameter.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget_object_parameter.setObjectName("tabWidget_object_parameter")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tab_5)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.tableView_object_parameter_value = QtWidgets.QTableView(self.tab_5)
        self.tableView_object_parameter_value.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableView_object_parameter_value.setObjectName("tableView_object_parameter_value")
        self.tableView_object_parameter_value.verticalHeader().setVisible(False)
        self.verticalLayout_8.addWidget(self.tableView_object_parameter_value)
        self.tabWidget_object_parameter.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_6)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.tableView_object_parameter_definition = QtWidgets.QTableView(self.tab_6)
        self.tableView_object_parameter_definition.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableView_object_parameter_definition.setObjectName("tableView_object_parameter_definition")
        self.tableView_object_parameter_definition.verticalHeader().setVisible(False)
        self.verticalLayout_6.addWidget(self.tableView_object_parameter_definition)
        self.tabWidget_object_parameter.addTab(self.tab_6, "")
        self.verticalLayout_11.addWidget(self.tabWidget_object_parameter)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.splitter_object_relationship_parameter)
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_7.addWidget(self.label_4)
        self.tabWidget_relationship_parameter = QtWidgets.QTabWidget(self.verticalLayoutWidget_2)
        self.tabWidget_relationship_parameter.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget_relationship_parameter.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget_relationship_parameter.setObjectName("tabWidget_relationship_parameter")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.tab_7)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.tableView_relationship_parameter_value = QtWidgets.QTableView(self.tab_7)
        self.tableView_relationship_parameter_value.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableView_relationship_parameter_value.setObjectName("tableView_relationship_parameter_value")
        self.tableView_relationship_parameter_value.verticalHeader().setVisible(False)
        self.verticalLayout_9.addWidget(self.tableView_relationship_parameter_value)
        self.tabWidget_relationship_parameter.addTab(self.tab_7, "")
        self.tab_8 = QtWidgets.QWidget()
        self.tab_8.setObjectName("tab_8")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.tab_8)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.tableView_relationship_parameter_definition = QtWidgets.QTableView(self.tab_8)
        self.tableView_relationship_parameter_definition.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableView_relationship_parameter_definition.setObjectName("tableView_relationship_parameter_definition")
        self.tableView_relationship_parameter_definition.verticalHeader().setVisible(False)
        self.verticalLayout_10.addWidget(self.tableView_relationship_parameter_definition)
        self.tabWidget_relationship_parameter.addTab(self.tab_8, "")
        self.verticalLayout_7.addWidget(self.tabWidget_relationship_parameter)
        self.verticalLayout_12.addWidget(self.splitter_object_relationship_parameter)
        self.dockWidget_parameter.setWidget(self.dockWidgetContents_parameter)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget_parameter)
        self.dockWidget_parameter_enum = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_parameter_enum.setObjectName("dockWidget_parameter_enum")
        self.dockWidgetContents_3 = QtWidgets.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.dockWidgetContents_3)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.treeView_parameter_enum = QtWidgets.QTreeView(self.dockWidgetContents_3)
        self.treeView_parameter_enum.setObjectName("treeView_parameter_enum")
        self.verticalLayout_13.addWidget(self.treeView_parameter_enum)
        self.dockWidget_parameter_enum.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget_parameter_enum)
        self.actionGraph_reinstate_pruned = QtWidgets.QAction(MainWindow)
        self.actionGraph_reinstate_pruned.setObjectName("actionGraph_reinstate_pruned")
        self.actionDock_widgets = QtWidgets.QAction(MainWindow)
        self.actionDock_widgets.setObjectName("actionDock_widgets")
        self.actiontodos = QtWidgets.QAction(MainWindow)
        self.actiontodos.setObjectName("actiontodos")
        self.actionRefresh = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRefresh.setIcon(icon)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionCommit = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/ok.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCommit.setIcon(icon1)
        self.actionCommit.setObjectName("actionCommit")
        self.actionRollback = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/nok.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRollback.setIcon(icon2)
        self.actionRollback.setObjectName("actionRollback")
        self.actionClose = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClose.setIcon(icon3)
        self.actionClose.setObjectName("actionClose")
        self.actionGraph_hide_selected = QtWidgets.QAction(MainWindow)
        self.actionGraph_hide_selected.setObjectName("actionGraph_hide_selected")
        self.actionGraph_show_hidden = QtWidgets.QAction(MainWindow)
        self.actionGraph_show_hidden.setObjectName("actionGraph_show_hidden")
        self.actionGraph_prune_selected = QtWidgets.QAction(MainWindow)
        self.actionGraph_prune_selected.setObjectName("actionGraph_prune_selected")
        self.menuGraph.addAction(self.actionGraph_hide_selected)
        self.menuGraph.addAction(self.actionGraph_show_hidden)
        self.menuGraph.addSeparator()
        self.menuGraph.addAction(self.actionGraph_prune_selected)
        self.menuGraph.addAction(self.actionGraph_reinstate_pruned)
        self.menuView.addAction(self.menuToolbars.menuAction())
        self.menuView.addAction(self.menuDock_Widgets.menuAction())
        self.menuSession.addAction(self.actionRefresh)
        self.menuSession.addAction(self.actionCommit)
        self.menuSession.addAction(self.actionRollback)
        self.menuFile.addAction(self.actionClose)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuGraph.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuSession.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget_object_parameter.setCurrentIndex(0)
        self.tabWidget_relationship_parameter.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.menuGraph.setTitle(QtWidgets.QApplication.translate("MainWindow", "Graph", None, -1))
        self.menuView.setTitle(QtWidgets.QApplication.translate("MainWindow", "View", None, -1))
        self.menuDock_Widgets.setTitle(QtWidgets.QApplication.translate("MainWindow", "Dock Widgets", None, -1))
        self.menuToolbars.setTitle(QtWidgets.QApplication.translate("MainWindow", "Toolbars", None, -1))
        self.menuSession.setTitle(QtWidgets.QApplication.translate("MainWindow", "Session", None, -1))
        self.menuFile.setTitle(QtWidgets.QApplication.translate("MainWindow", "File", None, -1))
        self.dockWidget_item_palette.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Item palette", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "Object class", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "Relationship class", None, -1))
        self.dockWidget_object_tree.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Object tree", None, -1))
        self.dockWidget_parameter.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Parameter dock", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("MainWindow", "Object parameter", None, -1))
        self.tabWidget_object_parameter.setTabText(self.tabWidget_object_parameter.indexOf(self.tab_5), QtWidgets.QApplication.translate("MainWindow", "value", None, -1))
        self.tabWidget_object_parameter.setTabText(self.tabWidget_object_parameter.indexOf(self.tab_6), QtWidgets.QApplication.translate("MainWindow", "definition", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("MainWindow", "Relationship parameter", None, -1))
        self.tabWidget_relationship_parameter.setTabText(self.tabWidget_relationship_parameter.indexOf(self.tab_7), QtWidgets.QApplication.translate("MainWindow", "value", None, -1))
        self.tabWidget_relationship_parameter.setTabText(self.tabWidget_relationship_parameter.indexOf(self.tab_8), QtWidgets.QApplication.translate("MainWindow", "definition", None, -1))
        self.dockWidget_parameter_enum.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Parameter enum", None, -1))
        self.actionGraph_reinstate_pruned.setText(QtWidgets.QApplication.translate("MainWindow", "Reinstate pruned items", None, -1))
        self.actionDock_widgets.setText(QtWidgets.QApplication.translate("MainWindow", "Dock Widgets", None, -1))
        self.actiontodos.setText(QtWidgets.QApplication.translate("MainWindow", "todos", None, -1))
        self.actionRefresh.setText(QtWidgets.QApplication.translate("MainWindow", "Refresh", None, -1))
        self.actionRefresh.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+Shift+Return", None, -1))
        self.actionCommit.setText(QtWidgets.QApplication.translate("MainWindow", "Commit", None, -1))
        self.actionCommit.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+Return", None, -1))
        self.actionRollback.setText(QtWidgets.QApplication.translate("MainWindow", "Rollback", None, -1))
        self.actionRollback.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+Backspace", None, -1))
        self.actionClose.setText(QtWidgets.QApplication.translate("MainWindow", "Close", None, -1))
        self.actionClose.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+W", None, -1))
        self.actionGraph_hide_selected.setText(QtWidgets.QApplication.translate("MainWindow", "Hide selected items", None, -1))
        self.actionGraph_show_hidden.setText(QtWidgets.QApplication.translate("MainWindow", "Show hidden items", None, -1))
        self.actionGraph_prune_selected.setText(QtWidgets.QApplication.translate("MainWindow", "Prune selected items", None, -1))

from widgets.custom_qgraphicsview import GraphViewGraphicsView
from widgets.custom_qlistview import DragListView
import resources_icons_rc
