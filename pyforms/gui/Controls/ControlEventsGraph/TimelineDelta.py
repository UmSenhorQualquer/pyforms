#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.Controls.ControlEventTimeline.TimelineDelta

"""

from PyQt4 import QtGui
from pyforms.gui.Controls.ControlEventsGraph.Track import Track

__author__ = ["Ricardo Ribeiro", "Hugo Cachitas"]
__credits__ = ["Ricardo Ribeiro", "Hugo Cachitas"]
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = "Ricardo Ribeiro"
__email__ = "ricardojvr@gmail.com"
__status__ = "Development"


class TimelineDelta(object):

    def __init__(self, begin, end=30, title=None, parentWidget=None, color='#FFFF00'):
        self._parentWidget  = parentWidget
        self._title         = title
        self._begin         = begin
        self._end           = end
        self.color          = color

    ##########################################################################
    #### HELPERS/FUNCTIONS ###################################################
    ##########################################################################

    def draw(self, painter, top=20, showvalues=False, left_shift=0):
        start, width = left_shift+self.begin, self.end-self.begin

        painter.setPen(QtGui.QColor(0, 0, 0))
        painter.setOpacity(0.5)
        painter.drawRect(start, top, width, self._parentWidget.tracks_height-4)
        painter.setOpacity(1.0)

        """
        painter.drawText(left_shift+start + 3, top + self._parentWidget.tracks_height/2+2, self._title)
        if showvalues:
            painter.drawText( 
                left_shift+start, top + self._parentWidget.tracks_height+4, 
                "[{0};{1}] delta:{2}".format(self._begin, self._end, self._end - self._begin)
            )"""

    def remove(self):
        try:
            self._parentWidget._tracks[self.track].periods.remove(self)
        except:pass

    ##########################################################################
    #### PROPERTIES ##########################################################
    ##########################################################################

    @property
    def title(self): return self._title


    @property
    def begin(self): return self._begin

    @begin.setter
    def begin(self, value):
        self._begin = value
        if self._begin < 0: self._begin = 0

    @property
    def end(self): return self._end

    @end.setter
    def end(self, value):
        self._end = value
        if self._end > (self._parentWidget.width()):
            self._end = (self._parentWidget.width())

    @property
    def color(self): return self._defautcolor

    @color.setter
    def color(self, value): self._defautcolor = QtGui.QColor(value) if (type(value) == str) else value