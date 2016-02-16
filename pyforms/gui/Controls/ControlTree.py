# !/usr/bin/python
# -*- coding: utf-8 -*-

""""pyforms.gui.Controls.Control Tree"""

from pyforms.gui.Controls.ControlBase import ControlBase
from PyQt4.QtGui import QTreeWidget, QTreeWidgetItem, QTreeView, QStandardItem
from PyQt4.QtGui import QAbstractItemView
from PyQt4.QtCore import QSize
from PyQt4 import QtGui

__author__ = "Ricardo Ribeiro"
__copyright__ = ""
__credits__ = "Ricardo Ribeiro"
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = ["Ricardo Ribeiro", "Carlos Mão de Ferro"]
__email__ = ["ricardojvr at gmail.com", "cajomferro at gmail.com"]
__status__ = "Development"


class ControlTree(ControlBase, QTreeWidget):

    """This class represents a wrapper to the QTreeWidget"""

    def __init__(self, label='', default=''):
        QTreeWidget.__init__(self)
        ControlBase.__init__(self, label, default)

    def initForm(self):
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setUniformRowHeights(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)

        self.model().dataChanged.connect(self.__itemChangedEvent)
        self.itemDoubleClicked.connect(self.__itemDoubleClicked)

        self.selectionChanged = self.selectionChanged
        self._items = {}

    def __repr__(self): return QTreeWidget.__repr__(self)

    @property
    def showHeader(self):
        return self.header().isVisible()

    @showHeader.setter
    def showHeader(self, value):
        if value:
            self.header().show()
        else:
            self.header().hide()

    def __itemChangedEvent(self, item): self.itemChangedEvent(item)

    def itemChangedEvent(self, item): pass

    def itemSelectionChanged(self): pass

    def rowsInsertedEvent(self, parent, start, end):
        """ This event is called every time a new row is added to the tree"""
        pass

    def rowsInserted(self, parent, start, end):
        super(ControlTree, self).rowsInserted(parent, start, end)
        self.rowsInsertedEvent(parent, start, end)

    def selectionChanged(self, selected, deselected):
        super(QTreeView, self).selectionChanged(selected, deselected)
        self.itemSelectionChanged()

    @property
    def mouseSelectedRowsIndexes(self):
        result = []
        for index in self.selectedIndexes():
            result.append(index.row())
        return list(set(result))

    @property
    def mouseSelectedRowIndex(self):
        indexes = self.mouseSelectedRowsIndexes
        if len(indexes) > 0:
            return indexes[0]
        else:
            return None

    @property
    def selectedItem(self):
        if len(self.selectedItems())>0: return self.selectedItems()[0]
        return None

    @property
    def cells(self):
        results = []
        for row in range(self.model().rowCount()):
            r = []
            for col in range(self.model().columnCount()):
                kker.append(self.model.item(row, col))

            if len(r) > 0:
                results.append(r)

        return results

    def __add__(self, other):
        if isinstance(other, QTreeWidgetItem):
            self.invisibleRootItem().addChild(other)
        elif isinstance(other, str):
            item = QTreeWidgetItem(other)
            self.invisibleRootItem().addChild(item)
        elif isinstance(other, list):
            for x in other:
                if isinstance(x, str):
                    item = QTreeWidgetItem(x)
                    self.invisibleRootItem().addChild(item)
                else:
                    self.invisibleRootItem().addChild(x)
        else:
            item = QTreeWidgetItem(other)
            self.invisibleRootItem().addChild(item)

        #self.setFirstColumnSpanned( self.model().rowCount() - 1, self.rootIndex(), True)
        return self

    def __sub__(self, other):
        if isinstance(other, int):
            if other < 0:
                indexToRemove = self.mouseSelectedRowIndex
            else:
                indexToRemove = other
            self.model().removeRow(indexToRemove)
        return self

    @property
    def form(self): return self

    @property
    def value(self):
        return [self.child(i) for i in range(self.invisibleRootItem().childCount())]

    @value.setter
    def value(self, value):
        if isinstance(value, list):
            for x in value:
                self += x
        else:
            self += value

    def save(self, data): pass

    def load(self, data): pass

    @property
    def iconsize(self):
        size = self.iconSize()
        return size.width(), self.height()

    @iconsize.setter
    def iconsize(self, value):
        self.setIconSize(QSize(*value))

    def addPopupMenuOption(self, label='', functionAction=None, key=None, item=None, icon=None):
        """
        Add an option to the Control popup menu
        @param label:           label of the option.
        @param functionAction:  function called when the option is selected.
        @param key:             shortcut key
        @param key:             shortcut key
        """
        action = super(ControlTree, self).addPopupMenuOption(
            label, functionAction, key)

        if item is not None:
            action = QtGui.QAction(label, self.form)
            if icon is not None:
                action.setIconVisibleInMenu(True)
                action.setIcon(QtGui.QIcon(icon))
            if key is not None:
                action.setShortcut(QtGui.QKeySequence(key))
            if functionAction:
                action.triggered.connect(functionAction)
                # Associate action to the item.
                if id(item) not in self._items.keys():
                    self._items.update({id(item): []})
                self._items[id(item)].append(action)
                ##########################
            return action
        return action

    def __itemDoubleClicked(self, item, column):
        if hasattr(item, 'double_clicked'): item.double_clicked()
        self.item_double_clicked(item)

    def item_double_clicked(self, item): pass

    def keyPressEvent(self, event):
        QTreeView.keyPressEvent(self, event)
        item = self.selectedItem
        if hasattr(item, 'key_pressed'): item.key_pressed(event)
        self.key_press_event(event)


    def key_press_event(self, event): pass

        

    def aboutToShowContextMenuEvent(self):
        """
        Function called before open the Control popup menu
        """
        if len(self._items) > 0:  # Reset the menu and construct a new one only if there are actions for the items.
            self._popupMenu.clear()
            itemSelected = self.selectedItems()[0]

            if id(itemSelected) in self._items:
                for action in self._items[id(itemSelected)]:
                    self._popupMenu.addAction(action)
                    # print("Adding action {action} to {item}".format(
                    #    action=action.text(), item=itemSelected))

    def clear(self):
        super(ControlTree, self).clear()
        if self._popupMenu:
            self._popupMenu.clear()
        self._items = {}

    def expand_item(self, item, expand=True, parents=True):
        item.setExpanded(expand)
        if parents:
            parent = item.parent()
            while(True):
                try:
                    parent.setExpanded(expand)
                    parent = parent.parent()
                except AttributeError:
                    break

    def createChild(self, name, parent=None, icon=None):
        """
        Create a new child for to the parent item.
        If the parent is None it add to the root.
        """
        item = QTreeWidgetItem(self, [name]) if(
            parent is None) else QTreeWidgetItem(parent, [name])
        if icon is not None:
            item.setIcon(0, QtGui.QIcon(icon))
        return item
