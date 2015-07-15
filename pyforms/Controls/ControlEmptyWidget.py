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

class ControlEmptyWidget(ControlBase):

    def initControl(self):
        
        self._form = QtGui.QWidget()
        layout = QtGui.QVBoxLayout()
        layout.setMargin(0)
        self._form.setLayout( layout )

    ############################################################################
    ############ Properties ####################################################
    ############################################################################

    @property
    def value(self): return ControlBase.value.fget(self)

    @value.setter
    def value(self, value):
        if isinstance( self._value, list ):
            for w in self._value:
                if w!=None and w!="": self._form.layout().removeWidget( w.form )
        else:
            if self._value!=None and self._value!="": self._form.layout().removeWidget( self._value.form )

        if isinstance( value, list ):
            for w in value:
                self._form.layout().addWidget( w.form )
        else:
            self._form.layout().addWidget( value.form )

        ControlBase.value.fset(self,value)
        
        
    