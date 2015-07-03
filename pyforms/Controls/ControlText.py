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
from PyQt4 import uic, QtGui
from pyforms.Controls.ControlBase import ControlBase

class ControlText(ControlBase):

    def initControl(self):
        super(ControlText, self).initControl()
        self.form.lineEdit.editingFinished.connect( self.finishEditing )


    def finishEditing(self): 
        """Function called when the lineEdit widget is edited"""
        self.changed()

       
    ############################################################################
    ############ Properties ####################################################
    ############################################################################

    @property
    def value(self): 
        self._value = str(self._form.lineEdit.text())
        return self._value

    @value.setter
    def value(self, value):
        self._form.lineEdit.setText(value)
        ControlBase.value.fset(self,value)
        
        
        
    