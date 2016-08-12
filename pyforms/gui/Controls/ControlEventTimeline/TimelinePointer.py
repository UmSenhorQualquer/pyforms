#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.Controls.ControlEventTimeline.TimelinePointer

"""

from PyQt4 import QtGui, QtCore

__author__ = ["Ricardo Ribeiro", "Hugo Cachitas"]
__credits__ = ["Ricardo Ribeiro", "Hugo Cachitas"]
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = "Ricardo Ribeiro"
__email__ = "ricardojvr@gmail.com"
__status__ = "Development"


class TimelinePointer(object):

    def __init__(self, position, parent):
        self._position = position
        self._parent = parent

    def draw(self, painter, showvalues=False):
        painter.setPen(QtGui.QColor(0, 255, 0))
        painter.setBrush(QtGui.QColor(0, 255, 0))
        painter.drawLine(
            self.xposition, 8, self.xposition, self._parent.height())
        painter.drawEllipse(QtCore.QPoint(self.xposition, 8), 5, 5)
        painter.drawText(self.xposition + 8, 8 + 4, str(self._position))

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
        x = int(round(x / self._parent._scale))
        if (self._position - x) >= 0 and (self._position - x) <= (self._parent.width() / self._parent._scale):
            self._position += x
            self.moveEvent()

    ##########################################################################
    #### PROPERTIES ##########################################################
    ##########################################################################
    @property
    def xposition(self):
        return self._parent.frame2x(self.position)
    

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
        self.moveEvent()
        

    @property
    def frame(self): return self._position
