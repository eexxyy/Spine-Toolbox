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
Classes for custom QListView.

:author: M. Marin (KTH)
:date:   14.11.2018
"""

from PySide2.QtWidgets import QListView, QApplication
from PySide2.QtGui import QDrag
from PySide2.QtCore import Qt, QMimeData, QSize, Slot


class DragListView(QListView):
    """Custom QListView class with dragging support.

    Attributes:
        parent (QWidget): The parent of this view
    """

    def __init__(self, parent):
        """Initialize the view."""
        super().__init__(parent=parent)
        self.drag_start_pos = None
        self.pixmap = None
        self.mime_data = None

    def mousePressEvent(self, event):
        """Register drag start position"""
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            index = self.indexAt(event.pos())
            if not index.isValid() or not index.model().is_index_draggable(index):
                self.drag_start_pos = None
                self.pixmap = None
                self.mime_data = None
                return
            self.drag_start_pos = event.pos()
            self.pixmap = index.data(Qt.DecorationRole).pixmap(self.iconSize())
            mime_data_text = self.model().get_mime_data_text(index)
            self.mime_data = QMimeData()
            self.mime_data.setText(mime_data_text)

    def mouseMoveEvent(self, event):
        """Start dragging action if needed"""
        if not event.buttons() & Qt.LeftButton:
            return
        if not self.drag_start_pos:
            return
        if (event.pos() - self.drag_start_pos).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        drag.setPixmap(self.pixmap)
        drag.setMimeData(self.mime_data)
        drag.setHotSpot(self.pixmap.rect().center())
        drag.exec_()
        self.drag_start_pos = None
        self.pixmap = None
        self.mime_data = None

    def mouseReleaseEvent(self, event):
        """Forget drag start position"""
        super().mouseReleaseEvent(event)
        self.drag_start_pos = None
        self.pixmap = None
        self.mime_data = None


class ProjectItemDragListView(DragListView):
    def __init__(self, parent):
        super().__init__(parent)
        base_size = QSize(24, 24)
        self.setIconSize(base_size)
        font = self.font()
        font.setPointSize(9)
        self.setFont(font)
        self.setStyleSheet("QListView {background: transparent;}")
        self.setResizeMode(DragListView.Adjust)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.set_orientation(self.parent().orientation())
        self.parent().orientationChanged.connect(self.set_orientation)

    @Slot("Qt.Orientation")
    def set_orientation(self, orientation):
        if orientation == Qt.Horizontal:
            self.setFlow(QListView.LeftToRight)
        elif orientation == Qt.Vertical:
            self.setFlow(QListView.TopToBottom)

    def updateGeometries(self):
        """Resize to contents."""
        super().updateGeometries()
        size = self.contentsSize()
        if not size.isValid():
            size = QSize(0, 0)
        margin = 2 * self.frameWidth()
        size += QSize(margin, margin)
        self.setMaximumSize(size)
