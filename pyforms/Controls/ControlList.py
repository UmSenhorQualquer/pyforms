#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


from pyforms.Controls.ControlBase import ControlBase
import pyforms.Utils.tools as tools
from PyQt4 import uic, QtGui


class ControlList(ControlBase):

    def __init__(self, label = "", defaultValue = "", plusFunction=None, minusFunction=None):
        ControlBase.__init__(self, label, defaultValue)

        if plusFunction==None and minusFunction==None:
            self.form.bottomBar.hide()
        elif plusFunction==None:
            self.form.plusButton.hide()
            self.form.minusButton.pressed.connect(minusFunction)
        elif minusFunction==None:
            self.form.minusButton.hide()
            self.form.plusButton.pressed.connect(plusFunction)
        else:
            self.form.plusButton.pressed.connect(plusFunction)
            self.form.minusButton.pressed.connect(minusFunction)



    def initControl(self):
        control_path = tools.getFileInSameDirectory(__file__,"list.ui")
        self._form = uic.loadUi( control_path )
        self._form.label.setText(self.label)
        self._form.tableWidget.currentCellChanged.connect( self.tableWidgetCellChanged )
        self._form.tableWidget.itemSelectionChanged.connect( self.tableWidgetItemSelectionChanged )

    def tableWidgetCellChanged(self, nextRow, nextCol, previousRow, previousCol):
        self.currentCellChanged(nextRow, nextCol, previousRow, previousCol)

    def tableWidgetItemSelectionChanged(self):
        self.itemSelectionChanged()

    def itemSelectionChanged(self):pass

    def currentCellChanged(self, nextRow, nextCol, previousRow, previousCol):pass
       
    def clear(self):
        self._form.tableWidget.clear()
        self._form.tableWidget.setColumnCount(3)
        self._form.tableWidget.setRowCount(0)

    def __add__(self, other):
        
        index = self._form.tableWidget.rowCount()
        self._form.tableWidget.insertRow( index )
        self._form.tableWidget.setColumnCount(len(other))
        for i in range(0, len(other)):
            self._form.tableWidget.setItem( index, i, QtGui.QTableWidgetItem( str(other[i]) ) )

        self._form.tableWidget.resizeColumnsToContents()
        return self

    def __sub__(self, other):

        if isinstance(other, int):
            if other < 0:
                indexToRemove = self._form.tableWidget.currentRow()
            else:
                indexToRemove = other
            self._form.tableWidget.removeRow(indexToRemove)
        return self

    def setValue(self, column, row, value):
        self._form.tableWidget.item(row,column).setText( str(value) )

    def getValue(self, column, row):
        return str(self._form.tableWidget.item(row,column).text() )

    ############################################################################
    ############ Properties ####################################################
    ############################################################################

    @property
    def selectEntireRow(self): 
        return self._form.tableWidget.selectionBehavior()

    @selectEntireRow.setter
    def selectEntireRow(self, value): 
        if value: self._form.tableWidget.setSelectionBehavior( QtGui.QAbstractItemView.SelectRows )
        else: self._form.tableWidget.setSelectionBehavior( QtGui.QAbstractItemView.SelectItems )

    @property
    def count(self): return self._form.tableWidget.rowCount()

    @property
    def value(self):
        results = []
        for row in range(self._form.tableWidget.rowCount()):
            r = []
            for col in range(self._form.tableWidget.columnCount()):
                try:
                    r.append( self.getValue(col, row) )
                except:
                    r.append("")
            results.append(r)
        return results
    
    @value.setter
    def value(self, value):
        for row in value: self += row

    @property
    def mouseSelectedRowsIndexes(self):
        result = []
        for index in self._form.tableWidget.selectedIndexes(): 
            result.append( index.row() )
        return list( set(result) )

    @property
    def mouseSelectedRowIndex(self):
        indexes = self.mouseSelectedRowsIndexes
        if len(indexes)>0: return indexes[0]
        else: return None