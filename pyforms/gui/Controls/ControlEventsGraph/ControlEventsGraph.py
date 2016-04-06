#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.Controls.ControlEventTimeline.ControlEventTimeline

"""

import csv
from PyQt4 import QtGui, QtCore
from pyforms.gui.Controls.ControlBase import ControlBase
from pyforms.gui.Controls.ControlEventsGraph.EventsWidget import EventsWidget


__author__ = ["Ricardo Ribeiro", "Hugo Cachitas"]
__credits__ = ["Ricardo Ribeiro", "Hugo Cachitas"]
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = "Ricardo Ribeiro"
__email__ = "ricardojvr@gmail.com"
__status__ = "Development"


class ControlEventsGraph(ControlBase, QtGui.QWidget):
    """
        Timeline events editor
    """

    def __init__(self, label="", defaultValue=0, min=0, max=100, **kwargs):
        QtGui.QWidget.__init__(self)
        ControlBase.__init__(self, label, defaultValue, **kwargs)
        self.addPopupMenuOption('Export to CSV', self.__export)

    def initForm(self):
        vlayout = QtGui.QVBoxLayout()
        vlayout.setMargin(0)
        self.setLayout(vlayout)

        self._scroll = QtGui.QScrollBar(QtCore.Qt.Horizontal)

        scrollarea = QtGui.QScrollArea()
        scrollarea.setMinimumHeight(140)
        scrollarea.setWidgetResizable(True)

        self._events_widget = EventsWidget(scroll=self._scroll)
        scrollarea.setWidget(self._events_widget)

        self._scroll.actionTriggered.connect(self.__scroll_changed)

        vlayout.addWidget(scrollarea)   # The timeline widget
        vlayout.addWidget(self._scroll)  # Add scroll

        self._scroll.setMaximum(0)
        self._scroll.setSliderPosition(0)

    ##########################################################################
    #### HELPERS/PUBLIC FUNCTIONS ############################################
    ##########################################################################

    def add_event(self, begin, end, title='', track=0, color='#FFFF00'): self._events_widget.add_event(begin, end, title, track, color)

    ##########################################################################
    #### EVENTS ##############################################################
    ##########################################################################

    def __scroll_changed(self, change): self.repaint()

    def get_export_filename(self): return "untitled.csv"

    def __export(self):
        """Export annotations to a file."""
        filename = QtGui.QFileDialog.getSaveFileName(parent=self,
                                                     caption="Export annotations file",
                                                     directory=self.get_export_filename(),
                                                     filter="CSV Files (*.csv)",
                                                     options=QtGui.QFileDialog.DontUseNativeDialog)
        if filename != '':
            self.export_csv(filename)

    def export_csv(self, filename):
        """Export annotations to a file."""
        with open(filename, 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, dialect='excel')
            self._events_widget.export_csv(spamwriter)

    def repaint(self): self._events_widget.repaint()

    ##########################################################################
    #### PROPERTIES ##########################################################
    ##########################################################################
    """
    Overwrite the changed event from the ControlBase
    """
    @property
    def changed(self): return self._events_widget._pointer.moveEvent

    @changed.setter
    def changed(self, value): self._events_widget._pointer.moveEvent = value

    @property
    def value(self): return self._events_widget.position

    @value.setter
    def value(self, value): self._events_widget.position = value

    @property
    def form(self): return self

    @property
    def tracks(self): return self._events_widget.tracks

    @property
    def tracks_height(self): return self._events_widget.tracks_height

    @tracks_height.setter
    def tracks_height(self, value): self._events_widget.tracks_height = value

    @property
    def scale(self): return self._events_widget.scale

    @scale.setter
    def scale(self, value): self._events_widget.scale = value
