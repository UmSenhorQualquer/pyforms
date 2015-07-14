#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


import pyforms.Utils.tools as tools
from PyQt4 import uic, QtGui, QtCore
from ControlBase import ControlBase

class ControlCheckBoxList(ControlBase):

    def initControl(self):
        control_path = tools.getFileInSameDirectory(__file__,"tree.ui")
        self._form = uic.loadUi( control_path )

        self._form.label.setText(self._label)

    def __add__(self, val):
        print(val)
        if isinstance( val, tuple ):
            item=QtGui.QListWidgetItem(val[0])
            if val[1]: item.setCheckState( QtCore.Qt.Checked)
            else: item.setCheckState( QtCore.Qt.Unchecked)
        else:
            item=QtGui.QListWidgetItem(val )
        
        self._form.listWidget.addItem(item)        
        return self

    def clear(self):
        self._form.listWidget.clear()
        

    ############################################################################
    ############ Properties ####################################################
    ############################################################################

    @property
    def count(self): return self._form.listWidget.count()

    @property
    def checkedIndexes(self): 
        results = []
        for row in range( self.count ):
            item = self._form.listWidget.item(row)
            if item!=None and item.checkState()==QtCore.Qt.Checked : results.append( row )
        return results

    @property
    def value(self):
        results = []
        for row in range( self.count ):
            item = self._form.listWidget.item(row)
            if item!=None and item.checkState()==QtCore.Qt.Checked : results.append( item.text() )
        return results
    
    @value.setter
    def value(self, value): 
        for row in value: self += row

            
        
