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
from PyQt4 import uic, QtGui, QtCore
import os


class ControlList(ControlBase, QtGui.QWidget):

    def __init__(self, label = "", defaultValue = "", plusFunction=None, minusFunction=None):
        QtGui.QWidget.__init__(self)
        
        self._plusFunction = plusFunction
        self._minusFunction = minusFunction
        ControlBase.__init__(self, label, defaultValue)
        


    def initControl(self):
        plusFunction=self._plusFunction
        minusFunction=self._minusFunction
        
        #Get the current path of the file
        rootPath = os.path.dirname(__file__)
        #Load the UI for the self instance
        uic.loadUi( os.path.join(rootPath, "list.ui") , self)
        
        self.label = self._label
        
        self.tableWidget.currentCellChanged.connect( self.tableWidgetCellChanged )
        self.tableWidget.itemSelectionChanged.connect( self.tableWidgetItemSelectionChanged )

        if plusFunction==None and minusFunction==None:
            self.bottomBar.hide()
        elif plusFunction==None:
            self.plusButton.hide()
            self.minusButton.pressed.connect(minusFunction)
        elif minusFunction==None:
            self.minusButton.hide()
            self.plusButton.pressed.connect(plusFunction)
        else:
            self.plusButton.pressed.connect(plusFunction)
            self.minusButton.pressed.connect(minusFunction)


    def tableWidgetCellChanged(self, nextRow, nextCol, previousRow, previousCol):
        self.currentCellChanged(nextRow, nextCol, previousRow, previousCol)

    def tableWidgetItemSelectionChanged(self):
        self.itemSelectionChanged()

    def itemSelectionChanged(self):pass

    def currentCellChanged(self, nextRow, nextCol, previousRow, previousCol):pass
       
    def clear(self):
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)

    def __add__(self, other):
        
        index = self.tableWidget.rowCount()
        self.tableWidget.insertRow( index )
        self.tableWidget.setColumnCount(len(other))
        for i in range(0, len(other)):
            v = other[i]
            args = [str(v)] if not hasattr(v, 'icon') else [QtGui.QIcon(v.icon), str(v)]
            self.tableWidget.setItem( index, i, QtGui.QTableWidgetItem( *args ) )

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

    def setValue(self, column, row, value):
        self.tableWidget.item(row,column).setText( str(value) )

    def getValue(self, column, row):
        return str(self.tableWidget.item(row,column).text() )

    ############################################################################
    ############ Properties ####################################################
    ############################################################################

    @property
    def selectEntireRow(self): 
        return self.tableWidget.selectionBehavior()

    @selectEntireRow.setter
    def selectEntireRow(self, value): 
        if value: self.tableWidget.setSelectionBehavior( QtGui.QAbstractItemView.SelectRows )
        else: self.tableWidget.setSelectionBehavior( QtGui.QAbstractItemView.SelectItems )

    @property
    def count(self): return self.tableWidget.rowCount()

    @property
    def value(self):
        if hasattr(self, 'tableWidget'):
            results = []
            for row in range(self.tableWidget.rowCount()):
                r = []
                for col in range(self.tableWidget.columnCount()):
                    try:
                        r.append( self.getValue(col, row) )
                    except:
                        r.append("")
                results.append(r)
            return results
        return self._value
    
    @value.setter
    def value(self, value):
        for row in value: self += row

    @property
    def mouseSelectedRowsIndexes(self):
        result = []
        for index in self.tableWidget.selectedIndexes(): 
            result.append( index.row() )
        return list( set(result) )

    @property
    def mouseSelectedRowIndex(self):
        indexes = self.mouseSelectedRowsIndexes
        if len(indexes)>0: return indexes[0]
        else: return None


    
    @property
    def label(self): return self.labelWidget.getText()
    @label.setter
    def label(self, value): 
        if value!='': 
            self.labelWidget.setText(value)
        else:
            self.labelWidget.hide()

    @property
    def form(self): return self


    @property 
    def iconSize(self): return self.tableWidget.iconSize()
    @iconSize.setter
    def iconSize(self,value): 
        if isinstance(value, (tuple, list)):
            self.tableWidget.setIconSize( QtCore.QSize(*value) )
        else:
            self.tableWidget.setIconSize( QtCore.QSize(value, value) )
 