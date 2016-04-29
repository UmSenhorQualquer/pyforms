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
        lastX = 0
        for x, y in data:
            if y > self._graphMax:
                self._graphMax = y
            if y < self._graphMin:
                self._graphMin = y

            if int(x - lastX) > 1:
                for i in range(0, int(x - lastX) + 1):
                    self._data.append((lastX + i, y))
                    # self._data.append( None )
            self._data.append((x, y))
            lastX = x

        if self._graphMin < 0:
            min2Zero = 0 - self._graphMin
            
            newData = []
            for f, y in self._data:
                newData.append((f, y + min2Zero))

            self._data = newData

    def draw(self, painter, left, right, top, bottom):
        painter.setPen(self._color)
        painter.setOpacity(0.7)

        maxPixelsHeight = (bottom - top)
        start = self._widget.x2frame(left)
        end = self._widget.x2frame(right)
        end = len(self._data) if end > len(self._data) else end

        diffMinMaxValue = (self._graphMax - self._graphMin)
        if diffMinMaxValue <= 0:
            diffMinMaxValue = 1

        
        for pos1, pos2 in zip(self._data[start + 1:end], self._data[start:end]):
            if pos1 and pos2:
                x,  y = pos1
                xx, yy = pos2

                y   = self._top + (y * maxPixelsHeight) // diffMinMaxValue
                yy  = self._top + (yy * maxPixelsHeight) // diffMinMaxValue

                if y>yy: 
                    y += (y-yy)*self._zoom - (y-yy)
                    yy-= (y-yy)*self._zoom - (y-yy)
                   
                elif y<yy:
                    y -= (y-yy)*self._zoom - (y-yy)
                    yy+= (y-yy)*self._zoom - (y-yy)

                painter.drawLine( self._widget.frame2x(xx), yy, self._widget.frame2x(x), y)

       

        painter.setOpacity(1.0)

    @property
    def name(self): return self._name
    @name.setter
    def name(self, value): self._name = value
    
