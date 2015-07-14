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
from pyforms.Controls.ControlBase import ControlBase

from visvis import Point, Pointset    
import visvis as vv
import numpy as np

class ControlVisVis(ControlBase):

    def initControl(self):        
        self._form = QtGui.QWidget();layout = QtGui.QVBoxLayout();layout.setMargin(0);self._form.setLayout( layout )
        self._app = vv.use('pyqt4')

        Figure = self._app.GetFigureClass()
        self._fig = Figure(self._form)

        policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        widget = self._fig._widget
        widget.setSizePolicy(policy)

        layout.addWidget(widget)

    

    def refresh(self):
        vv.figure(self._fig.nr)
        self._app = vv.use()
        self.paint(vv)

        
        
    def paint(self, visvis):
        visvis.clf()  
        a = visvis.gca()
        a.cameraType = '3d'
        a.daspectAuto = True

        colors = ['r','g','b','c','m','y','k','w']
        for index, dataset in enumerate(self._value):
            l = visvis.plot(dataset, ms='.', mc=colors[ index % len(colors) ], mw='3', ls='', mew=0 )
            l.alpha = 0.3


        

    ############################################################################
    ############ Properties ####################################################
    ############################################################################






    @property
    def value(self): return None

    @value.setter
    def value(self, value):
        self._value = []
        for dataset in value:
            if len(dataset)>0:
                if isinstance(dataset[0], list) or isinstance(dataset[0], tuple) :
                    self._value.append( Pointset( np.array(dataset) ) )
                else:
                    self._value.append( dataset )

        self.refresh()
        
        