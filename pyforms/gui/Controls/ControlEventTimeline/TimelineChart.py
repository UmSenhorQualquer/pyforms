#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.Controls.ControlEventTimeline.TimelineChart

"""

from PyQt4 import QtGui

__author__ = ["Ricardo Ribeiro", "Hugo Cachitas"]
__credits__ = ["Ricardo Ribeiro", "Hugo Cachitas"]
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = "Ricardo Ribeiro"
__email__ = "ricardojvr@gmail.com"
__status__ = "Development"


class TimelineChart(object):

    def __init__(self, timeLineWidget, csvfileobject, color=QtGui.QColor(255, 0, 0)):
        self._data = []
        self._firstFrame    = None
        self._graphMax      = None
        self._graphMin      = None
        self._widget        = timeLineWidget
        self._color         = color
        self._zoom          = 1.0
        self._top           = 0
        self._name          = 'undefined'

        data = [map(float, row) for row in csvfileobject]

        self._graphMax = 0
        self._graphMin = 100000000000
        self._data = []
        last_x = 0
        for x, y in data:
            if y > self._graphMax: self._graphMax = y
            if y < self._graphMin: self._graphMin = y

            if int(x - last_x) > 1:
                for i in range(0, int(x - last_x) + 1): self._data.append( (last_x + i, y) )
            else:
                self._data.append((x, y))
            last_x = x

        """
        if self._graphMin < 0:
            min2Zero = 0 - self._graphMin
            
            newData = []
            for f, y in self._data:
                newData.append((f, y + min2Zero))

            self._data = newData
        """

    def draw(self, painter, left, right, top, bottom):
        painter.setPen(self._color)
        painter.setOpacity(0.7)

        fov_height      = (bottom - top)*self._zoom
        start           = self._widget.x2frame(left)
        end             = self._widget.x2frame(right)
        end             = len(self._data) if end > len(self._data) else end
        diff_max_min    = (self._graphMax - self._graphMin)

        top = (-self._graphMin if self._graphMin>0 else abs(self._graphMin))*self._zoom

        if diff_max_min <= 0: diff_max_min = 1
        
        last_coordenate = None

        for pos1 in self._data[start:end]:
            if pos1:
                x, y = pos1

                y   = self._top + ((top+y) * fov_height)  // diff_max_min

                if last_coordenate: painter.drawLine( last_coordenate[0], last_coordenate[1], self._widget.frame2x(x), fov_height-y)

                last_coordenate = self._widget.frame2x(x), fov_height-y

       

        painter.setOpacity(1.0)

    @property
    def name(self): return self._name
    @name.setter
    def name(self, value): self._name = value
    
