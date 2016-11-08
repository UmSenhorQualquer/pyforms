#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


import pyforms.utils.tools as tools
from PyQt4 import uic, QtGui, QtCore
from pyforms.gui.Controls.ControlBase import ControlBase

from visvis import Point, Pointset    
import visvis as vv
import numpy as np

class ControlVisVis(ControlBase):

    def init_form(self):        
        self._form = QtGui.QWidget();layout = QtGui.QVBoxLayout();layout.setMargin(0);self._form.setLayout( layout )
        self._app = vv.use('pyqt4')
        self._app.Create()
        
        Figure = self._app.GetFigureClass()
        self._fig = Figure(self._form)

        policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        widget = self._fig._widget
        widget.setSizePolicy(policy)

        layout.addWidget(widget)

        
    def refresh(self):
        vv.figure(self._fig.nr)
        #self._app = vv.use()
        self.paint(vv)

        
        
    def paint(self, visvis):
        vv.clf()  
        
        colors = ['r','g','b','c','m','y','k']
        for index, dataset in enumerate(self._value):
            l = visvis.plot(dataset, ms='o', mc=colors[ index % len(colors) ], mw='3', ls='', mew=0 )
            l.alpha = 0.3

        self._a = vv.gca()
        self._a.daspectAuto = True



    ############################################################################
    ############ Properties ####################################################
    ############################################################################

    @property
    def legend(self):return self._a.legend
    @legend.setter
    def legend(self, value): self._a.legend = value

    @property
    def showGrid(self):return self._a.axis.showGrid
    @showGrid.setter
    def showGrid(self, value): self._a.axis.showGrid = value

    @property
    def title(self):return ''
    @title.setter
    def title(self, value): vv.title(value)

    @property
    def xlabel(self):return self._a.axis.xlabel
    @xlabel.setter
    def xlabel(self, value): self._a.axis.xlabel = value

    @property
    def ylabel(self):return self._a.axis.ylabel
    @ylabel.setter
    def ylabel(self, value): self._a.axis.ylabel = value

    @property
    def zlabel(self):return self._a.axis.zlabel
    @ylabel.setter
    def zlabel(self, value): self._a.axis.zlabel = value

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
        
