#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.Controls.ControlList

"""

from pyforms.Controls.ControlBase import ControlBase
from PyQt4 import uic, QtCore
from PyQt4.QtGui import QWidget, QIcon, QTableWidgetItem, QAbstractItemView
import os

__author__ = "Ricardo Ribeiro"
__copyright__ = ""
__credits__ = "Ricardo Ribeiro"
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = ["Ricardo Ribeiro", "Carlos Mão de Ferro"]
__email__ = ["ricardojvr at gmail.com", "cajomferro at gmail.com"]
__status__ = "Development"


class ControlList(ControlBase, QWidget):
    """ This class represents a wrapper to the table widget
        It allows to implement a list view
    """

    def __init__(self, label="", defaultValue="", plusFunction=None,
                 minusFunction=None):
        QWidget.__init__(self)

        self._plusFunction = plusFunction
        self._minusFunction = minusFunction
        ControlBase.__init__(self, label, defaultValue)
        
    def __repr__(self): return "ControlList "+str(self._value)



    def initForm(self):
        plusFunction = self._plusFunction
        minusFunction = self._minusFunction

        # Get the current path of the file
        rootPath = os.path.dirname(__file__)
        # Load the UI for the self instance
        uic.loadUi(os.path.join(rootPath, "list.ui"), self)

        self.label = self._label

        self.tableWidget.currentCellChanged.connect(
            self.tableWidgetCellChanged)
        self.tableWidget.currentItemChanged.connect(
            self.tableWidgetItemChanged)
        self.tableWidget.itemSelectionChanged.connect(
            self.tableWidgetItemSelectionChanged)
        self.tableWidget.model().dataChanged.connect(self._dataChangedEvent)

        if plusFunction is None and minusFunction is None:
            self.bottomBar.hide()
        elif plusFunction is None:
            self.plusButton.hide()
            self.minusButton.pressed.connect(minusFunction)
        elif minusFunction is None:
            self.minusButton.hide()
            self.plusButton.pressed.connect(plusFunction)
        else:
            self.plusButton.pressed.connect(plusFunction)
            self.minusButton.pressed.connect(minusFunction)

    def _dataChangedEvent(self, item):
        self.dataChangedEvent(
            item.row(), item.column(), self.tableWidget.model().data(item))
        self.changed()

    def dataChangedEvent(self, row, col, item): pass

    def tableWidgetCellChanged(self, nextRow, nextCol, previousRow,
                               previousCol):
        self.currentCellChanged(nextRow, nextCol, previousRow, previousCol)
        self.changed()

    def tableWidgetItemChanged(self, current, previous): 
        self.currentItemChanged(current, previous)
        self.changed()

    def tableWidgetItemSelectionChanged(self): self.itemSelectionChanged()

    def itemSelectionChanged(self): pass

    def currentCellChanged(self, nextRow, nextCol, previousRow, previousCol): pass

    def currentItemChanged(self, current, previous): pass

    def clear(self):
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        
    def __add__(self, other):

        index = self.tableWidget.rowCount()

        self.tableWidget.insertRow( index )
        if self.tableWidget.currentColumn()<len(other):
            self.tableWidget.setColumnCount(len(other))
 
        for i in range(0, len(other)):
            v = other[i]
            args = [str(v)] if not hasattr(
                v, 'icon') else [QIcon(v.icon), str(v)]
            self.tableWidget.setItem(index, i, QTableWidgetItem(*args))

        self.tableWidget.resizeColumnsToContents()
        return self

    def __sub__(self, other):

        if isinstance(other, int):
            if other < 0:
                indexToRemove = self.tableWidget.currentRow()
            else:
                indexToRemove = other
            self.tableWidget.removeRow(indexToRemove)
        return self

    @property
    def horizontalHeaders(self):
        return self._horizontalHeaders

    @horizontalHeaders.setter
    def horizontalHeaders(self, horizontalHeaders):
        """Set horizontal headers in the table list."""

        self._horizontalHeaders = horizontalHeaders

        self.tableWidget.setColumnCount(len(horizontalHeaders))
        self.tableWidget.horizontalHeader().setVisible(True)

        for idx, header in enumerate(horizontalHeaders):
            item = QTableWidgetItem()
            item.setText(header)
            self.tableWidget.setHorizontalHeaderItem(idx, item)

    def setValue(self, column, row, value):
        self.tableWidget.item(row, column).setText(str(value))

    def getValue(self, column, row):
        return str(self.tableWidget.item(row, column).text())

    @property
    def selectEntireRow(self):
        return self.tableWidget.selectionBehavior()

    @selectEntireRow.setter
    def selectEntireRow(self, value):
        if value:
            self.tableWidget.setSelectionBehavior(
                QAbstractItemView.SelectRows)
        else:
            self.tableWidget.setSelectionBehavior(
                QAbstractItemView.SelectItems)

    @property
    def count(self): return self.tableWidget.rowCount()


    @property
    def allItems(self):
        """
        Return all the Tree Items of the list, organized by row, col
        """ 
        rows = []
        for row in range(self.tableWidget.rowCount()):
            rows.append( [self.tableWidget.item(row, col) for col in range(self.tableWidget.columnCount())] )
        return rows

    @property
    def value(self):
        if hasattr(self, 'tableWidget'):
            results = []
            for row in range(self.tableWidget.rowCount()):
                r = []
                for col in range(self.tableWidget.columnCount()):
                    try:
                        r.append(self.getValue(col, row))
                    except:
                        r.append("")
                results.append(r)
            return results
        return self._value

    @value.setter
    def value(self, value):
        self.clear()
        for row in value:
            self += row
    # TODO: implement += on self.value? I want to add a list of tuples to
    # self.value

    @property
    def mouseSelectedRowsIndexes(self):
        result = []
        for index in self.tableWidget.selectedIndexes():
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
    def label(self): return self.labelWidget.getText()

    @label.setter
    def label(self, value):
        if value != '':
            self.labelWidget.setText(value)
        else:
            self.labelWidget.hide()

    @property
    def form(self): return self

    @property
    def iconSize(self): return self.tableWidget.iconSize()

    @iconSize.setter
    def iconSize(self, value):
        if isinstance(value, (tuple, list)):
            self.tableWidget.setIconSize(QtCore.QSize(*value))
        else:
            self.tableWidget.setIconSize(QtCore.QSize(value, value))
