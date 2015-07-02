import pyforms.Utils.tools as tools
from PyQt4 import uic, QtGui, QtCore
from ControlBase import ControlBase

from visvis import Point, Pointset    
import visvis as vv
import numpy as np

class ControlVisVisVolume(ControlBase):

    def initControl(self):
        self._form = QtGui.QWidget();layout = QtGui.QVBoxLayout();layout.setMargin(0);self._form.setLayout( layout )
        self._app = vv.use('pyqt4')
        self._first=True

        Figure = self._app.GetFigureClass()
        self._fig = Figure(self._form)
        vv.figure(self._fig.nr)
        
        policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        widget = self._fig._widget
        widget.setSizePolicy(policy)

        layout.addWidget(widget)


    ############################################################################
    ############ Properties ####################################################
    ############################################################################


    @property
    def value(self): return None

    @value.setter
    def value(self, value):

        a = vv.gca()
        view = a.GetView()
        a.Clear()
        vv.volshow3(value, renderStyle='mip')
        if not self._first:
            a = vv.gca()
            a.SetView(view)

        self._first=False
        

        
