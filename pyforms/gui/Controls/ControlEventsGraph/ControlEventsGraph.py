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


class ControlEventsGraph(ControlBase, QtGui.QWidget):
    """
        Timeline events editor
    """

    def __init__(self, label="", defaultValue=0, min=0, max=100, **kwargs):
        QtGui.QWidget.__init__(self)
        ControlBase.__init__(self, label, defaultValue, **kwargs)
        self.addPopupMenuOption('Export to CSV', self.__export)


    def initForm(self):
        vlayout = QtGui.QVBoxLayout(); vlayout.setMargin(0); self.setLayout(vlayout)

        scroll      = QtGui.QScrollBar(QtCore.Qt.Horizontal)
        scrollarea  = QtGui.QScrollArea(); scrollarea.setMinimumHeight(140); scrollarea.setWidgetResizable(True)
        widget      = EventsWidget(scroll=scroll); scrollarea.setWidget(widget)

        scroll.actionTriggered.connect(self.__scroll_changed)

        vlayout.addWidget(scrollarea)   # The timeline widget
        vlayout.addWidget(scroll)       # Add scroll
        
        scroll.setMaximum(0)
        scroll.setSliderPosition(0)
              
        self._time   = widget
        self._scroll = scroll

    ##########################################################################
    #### HELPERS/PUBLIC FUNCTIONS ############################################
    ##########################################################################

    def add_period(self, begin, end, title='', track=0, color='#FFFF00'):
        self._time.add_period(begin, end, title, track, color)

    ##########################################################################
    #### EVENTS ##############################################################
    ##########################################################################

    def __scroll_changed(self, change): self.repaint()


    def getExportFilename(self): return "untitled.csv"

    def __export(self):
        """Export annotations to a file."""
        filename = QtGui.QFileDialog.getSaveFileName(parent=self,
                                                     caption="Export annotations file",
                                                     directory=self.getExportFilename(),
                                                     filter="CSV Files (*.csv)",
                                                     options=QtGui.QFileDialog.DontUseNativeDialog)
        if filename!='': self.export_csv(filename)

    def export_csv(self, filename):
        """Export annotations to a file."""
        with open(filename, 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, dialect='excel')
            self._time.export_csv(spamwriter)

    def repaint(self): self._time.repaint()
            

    ##########################################################################
    #### PROPERTIES ##########################################################
    ##########################################################################

    """
    Overwrite the changed event from the ControlBase
    """
    @property
    def changed(self): return self._time._pointer.moveEvent
    @changed.setter
    def changed(self, value): self._time._pointer.moveEvent = value

    @property
    def value(self): return self._time.position
    @value.setter
    def value(self, value): self._time.position = value

    @property
    def max(self): return self._time.minimumWidth()
    @max.setter
    def max(self, value): self._time.setMinimumWidth(value); self.repaint()

    @property
    def form(self): return self

    @property
    def tracks(self): return self._time.tracks

    @property
    def tracks_height(self): return self._time.tracks_height
    @tracks_height.setter
    def tracks_height(self, value): self._time.tracks_height = value
   