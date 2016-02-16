#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.Controls.ControlEventTimeline.ControlEventTimeline

"""

import csv
import os
from PyQt4 import QtGui, QtCore
from pyforms.gui.Controls.ControlBase import ControlBase
from pyforms.gui.Controls.ControlEventsGraph.EventsWidget import EventsWidget


__author__      = ["Ricardo Ribeiro", "Hugo Cachitas"]
__credits__     = ["Ricardo Ribeiro", "Hugo Cachitas"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


class ControlEventsGraph(ControlBase, EventsWidget):
    """
        Timeline events editor
    """

    def __init__(self, label="", defaultValue=0, min=0, max=100, **kwargs):
        EventsWidget.__init__(self)
        ControlBase.__init__(self, label, defaultValue, **kwargs)
      
            

    ##########################################################################
    #### PROPERTIES ##########################################################
    ##########################################################################

    @property
    def value(self): return self._value
    @value.setter
    def value(self, value): self._value

    @property
    def form(self): return self

 