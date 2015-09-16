# !/usr/bin/python
# -*- coding: utf-8 -*-

""""pyforms.gui.Controls.Control Tree"""

from pyforms.gui.Controls.ControlBase import ControlBase
from PyQt4.QtGui import QTreeWidget, QTreeWidgetItem, QTreeView
from PyQt4.QtGui import QAbstractItemView
from PyQt4 import QtGui, QtCore

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

        self.selectionChanged = self.selectionChanged

        self._items = {}

        self._actions = []

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
        for index in self.selectedIndexes():
            item = index.model().itemFromIndex(index)
            return item
        else:
            return None

    @property
    def cells(self):
        results = []
        for row in range(self.model().rowCount()):
            r = []
            for col in range(self.model().columnCount()):
                r.append(self.model.item(row, col))

            if len(r) > 0:
                results.append(r)

        return results

    def __add__(self, other):
        if isinstance(other, QTreeWidgetItem):
            self.model().invisibleRootItem().appendRow(other)

        elif isinstance(other, list):
            item = QTreeWidgetItem(other)
            self.form.addTopLevelItem(item)
        else:
            item = QTreeWidgetItem(other)
            self.form.addTopLevelItem(item)

        self.setFirstColumnSpanned(
            self.model().rowCount() - 1, self.rootIndex(), True)
        return self

    def __sub__(self, other):
        if isinstance(other, int):
            if other < 0:
                indexToRemove = self.mouseSelectedRowIndex
            else:
                indexToRemove = other
            self.model().removeRow(indexToRemove)
        return self

    def addMenuAction(self, label='', functionAction=None, key=None, item=None):
        """
        Add an option to the Control popup menu
        @param label:           label of the option.
        @param functionAction:  function called when the option is selected.
        @param key:             shortcut key
        """
        if not self._popupMenu:
            self.form.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.form.customContextMenuRequested.connect(self._openPopupMenu)
            self._popupMenu = QtGui.QMenu()
            self._popupMenu.aboutToShow.connect(
                self.aboutToShowContextMenuEvent)

        if label == "-":
            pass
            #action = self._popupMenu.addSeparator()
            # self._actions.append(action)
            #self._addActionToItem(action, item)

        else:
            action = QtGui.QAction(label, self.form)
            if key is not None:
                action.setShortcut(QtGui.QKeySequence(key))
            if functionAction:
                action.triggered.connect(functionAction)
                self._actions.append(action)
                self._addActionToItem(action, item)
            return action

    def _addActionToItem(self, action, item):
        if item not in self._items.keys():
            self._items.update({item: []})
        self._items[item].append(action)
        print("Appending action {action} to item {item}".format(
            item=item, action=action.text()))

    def _openPopupMenu(self, position):
        if self._popupMenu:
            self._popupMenu.exec_(self.form.mapToGlobal(position))

    def aboutToShowContextMenuEvent(self):
        """
        Function called before open the Control popup menu
        """
        self._popupMenu.clear()
        itemSelected = self.selectedItems()[0].text(0)
        if itemSelected in self._items:
            for action in self._items[itemSelected]:
                self._popupMenu.addAction(action)
                print("Adding action {action} to {item}".format(
                    action=action.text(), item=itemSelected))

    def resetMenu(self):
        self._popupMenu.clear()
        self._items = {}
        self._actions = []

    def addItem(self, name, parent=None):
        newItem = None
        if parent is None:
            newItem = QTreeWidgetItem(self, [name])
        else:
            newItem = QTreeWidgetItem(parent, [name])
        return newItem

    @property
    def form(self): return self

    @property
    def value(self): return self

    @value.setter
    def value(self, value): self.addTopLevelItem(value)

    def save(self, data): pass

    def load(self, data): pass
