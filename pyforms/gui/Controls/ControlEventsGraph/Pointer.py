#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.Controls.ControlEventTimeline.Pointer

"""

from PyQt4 import QtGui, QtCore

__author__ = ["Ricardo Ribeiro", "Hugo Cachitas"]
__credits__ = ["Ricardo Ribeiro", "Hugo Cachitas"]
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = "Ricardo Ribeiro"
__email__ = "ricardojvr@gmail.com"
__status__ = "Development"


class Pointer(object):

    def __init__(self, position, parent, scroll):
        self._position  = position
        self._parent    = parent
        self._scroll    = scroll

    def draw(self, painter, left_shift=0, scale=1):
        x = self.position/scale+left_shift

        painter.setPen(QtGui.QColor(0, 255, 0))
        painter.setBrush(QtGui.QColor(0, 255, 0))
        painter.drawLine(x, 8, x, self._parent.height())
        painter.drawEllipse(QtCore.QPoint(x, 8), 5, 5)
        painter.drawText(x + 8, 8 + 4, str(self.position))

     

    ##########################################################################
    #### HELPERS/FUNCTIONS ###################################################
    ##########################################################################

    def moveEvent(self):
        pass

    def collide(self, x, y):
        return (self.position - 5) <= x <= (self.position + 5) and 3 <= y <= 11

    def canSlideBegin(self, x, y):
        return False

    def canSlideEnd(self, x, y):
        return False

    def move(self, x, y):
        if (self._position - x) >= 0 and (self._position - x) <= (self._parent.width()):
            self._position += x
            self.moveEvent()

    ##########################################################################
    #### PROPERTIES ##########################################################
    ##########################################################################

    @property
    def position(self): return self._position

    @position.setter
    def position(self, value):
        self._position = value 
        self.moveEvent()

    @property
    def frame(self): return self._position
