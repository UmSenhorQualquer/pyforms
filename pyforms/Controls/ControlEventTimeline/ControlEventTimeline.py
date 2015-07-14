#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = ["Ricardo Ribeiro", "Hugo Cachitas"]
__credits__     = ["Ricardo Ribeiro", "Hugo Cachitas"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


import csv, os

from PyQt4 import QtGui, QtCore

from pyforms.Controls.ControlBase import ControlBase
from TimelineWidget import TimelineWidget
from TimelinePopupWindow import TimelinePopupWindow


class ControlEventTimeline(ControlBase, QtGui.QWidget):
    """
        Timeline events editor
    """

    def __init__(self, label = "", defaultValue = 0, min = 0, max = 100, **kwargs):
        QtGui.QWidget.__init__(self)
        ControlBase.__init__(self, label, defaultValue, **kwargs)
        self._max = 100

        # Popup menus that only show when clicking on a TIMELINEDELTA object
        self._deltaLockAction = self.addPopupMenuOption("Lock", self.__lockSelected, key='L')
        self._deltaColorAction = self.addPopupMenuOption("Pick a color", self.__pickColor)
        self._deltaRemoveAction = self.addPopupMenuOption("Remove", self.__removeSelected, key='Delete')
        self._deltaActions = [self._deltaLockAction,
                              self._deltaColorAction,
                              self._deltaRemoveAction]
                              
        for action in self._deltaActions:
            action.setVisible(False)
        self.addPopupMenuOption("-")

        # General righ click popup menus
        self.addPopupMenuOption("Set track properties...", self.__setLinePropertiesEvent)
        self.addPopupMenuOption("-")
        self.addPopupSubMenuOption("Import/Export", {'Export to CSV': self.__export, 'Import to CSV': self.__import })
        self.addPopupMenuOption("-")
        self.addPopupSubMenuOption("Clean", {'Current line': self.__cleanLine, 'Everything': self.__clean, 'Charts': self.__cleanCharts })

    def initControl(self):
        #Get the current path of the file
        rootPath = os.path.dirname(__file__)

        vlayout = QtGui.QVBoxLayout()
        hlayout = QtGui.QHBoxLayout()
        self.setLayout(vlayout)

        

        #Add scroll area
        scrollarea = QtGui.QScrollArea()
        scrollarea.setMinimumHeight(140)
        scrollarea.setWidgetResizable(True);
        scrollarea.keyPressEvent = self.__scrollAreaKeyPressEvent
        scrollarea.keyReleaseEvent = self.__scrollAreaKeyReleaseEvent
        vlayout.addWidget(scrollarea)

        # The timeline widget
        widget = TimelineWidget()
        widget._scroll = scrollarea
        # widget.setMinimumHeight(54)
        scrollarea.setWidget(widget)

        #TODO Options buttons
        # btn_1 = QtGui.QPushButton("?")
        # btn_2 = QtGui.QPushButton("?")
        # vlayout_options = QtGui.QVBoxLayout()
        # vlayout_options.addWidget(btn_1)
        # vlayout_options.addWidget(btn_2)
        # hlayout.addLayout(vlayout_options)
        # hlayout.addWidget(btn_1)
        # hlayout.addWidget(btn_2)

        # Timeline zoom slider
        slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        slider.setFocusPolicy(QtCore.Qt.NoFocus)
        slider.setMinimum(1)
        slider.setMaximum(100)
        slider.setValue(10)
        slider.setPageStep(1)
        slider.setTickPosition(QtGui.QSlider.NoTicks)  # TicksBothSides
        slider.valueChanged.connect(self.__scaleSliderChange)
        slider_icon_zoom_in = QtGui.QPixmap(os.path.join(rootPath, "..","uipics","zoom_in.png"))
        slider_icon_zoom_out = QtGui.QPixmap(os.path.join(rootPath, "..","uipics","zoom_out.png"))
        slider_label_zoom_in = QtGui.QLabel()
        slider_label_zoom_out = QtGui.QLabel()
        slider_label_zoom_in.setPixmap(slider_icon_zoom_in)
        slider_label_zoom_out.setPixmap(slider_icon_zoom_out)
        # slider_vlayout = QtGui.QVBoxLayout()
        # slider_hlayout = QtGui.QHBoxLayout()
        # slider_hlayout.addWidget(slider_label_zoom_out)
        # slider_hlayout.addStretch()
        # slider_hlayout.addWidget(QtGui.QLabel("Zoom"))
        # slider_hlayout.addStretch()
        # slider_hlayout.addWidget(slider_label_zoom_in)
        # slider_vlayout.addWidget(slider)
        # slider_vlayout.addLayout(slider_hlayout)
        # hlayout.addLayout(slider_vlayout)
        self._zoomLabel = QtGui.QLabel("100%")
        hlayout.addWidget(self._zoomLabel)
        hlayout.addWidget(slider_label_zoom_out)
        hlayout.addWidget(slider)
        hlayout.addWidget(slider_label_zoom_in)



        # Import/Export Buttons
        btn_import = QtGui.QPushButton("Import")
        btn_import_icon = QtGui.QIcon(os.path.join(rootPath, "..","uipics","page_white_get.png"))
        btn_import.setIcon(btn_import_icon)
        btn_import.clicked.connect(self.__import)
        btn_export = QtGui.QPushButton("Export")
        btn_export_icon = QtGui.QIcon(os.path.join(rootPath, "..","uipics","page_white_put.png"))
        btn_export.setIcon(btn_export_icon)
        btn_export.clicked.connect(self.__export)
        # importexport_vlayout = QtGui.QVBoxLayout()
        # importexport_vlayout.addWidget(btn_import)
        # importexport_vlayout.addWidget(btn_export)
        # hlayout.addLayout(importexport_vlayout)
        hlayout.addWidget(btn_import)
        hlayout.addWidget(btn_export)

        vlayout.addLayout(hlayout)

        self._time = widget
        self._scrollArea = scrollarea

    ######################################################################################
    #### HELPERS/PUBLIC FUNCTIONS ########################################################
    ######################################################################################

    def getExportFilename(self):
        return "untitled.csv"

    def addRow(self, values):
        for v in values: self.addPeriod(v, track = 0)

    def addPeriod(self, value, track=0, color=None):
        self._time.addPeriod(value, track, color)

    ######################################################################################
    #### EVENTS ##########################################################################
    ######################################################################################

    def aboutToShowContextMenuEvent(self):
        for action in self._deltaActions:
            action.setVisible(True) if self._time._selected is not None else action.setVisible(False)

    def __setLinePropertiesEvent(self):
        """
        This controls makes possible the edition of a track in the
        timeline, based on the position of the mouse.

        Updates:
        - Track label
        - Track default color
        """
        current_track = self.mouseOverLine
        parent = self._time

        # Tracks info dict and index
        d = parent._tracks_info
        i = current_track

        # Save current default color to override with selected track color
        timeline_default_color = parent.color
        try:
            parent.color = d[i][1]
        except KeyError, e:
            error_message = ("You tried to edit an empty track.",
                             "\n",
                             "Initialize it by creating an event first.")
            QtGui.QMessageBox.warning(parent, "Attention!", "".join(error_message))
            return e

        # Create dialog
        dialog = TimelinePopupWindow(parent, i)
        dialog.setModal(True)  # to disable main application window

        # If dialog is accepted, update dict info
        if dialog._ui.exec_() == dialog.Accepted:
            # Update label
            if dialog.behavior is not None:
                d[i][0] = dialog.behavior

            # Update color
            if d[i][1] != dialog.color:
                for delta in d[i][2]:
                    if delta.color == d[i][1]:
                        delta.color = dialog.color
            d[i][1] = dialog.color
        else:
            pass

        # Restore timeline default color
        parent.color = timeline_default_color

        # Update track info
        parent._update_tracks_info()

    def __lockSelected(self): self._time.lockSelected()

    def __removeSelected(self): self._time.removeSelected()

    def __import(self):
        """Import annotations from a file."""

        filename = QtGui.QFileDialog.getOpenFileName(parent=self,
                                                     caption="Import annotations file",
                                                     directory="",
                                                     filter="*.csv",
                                                     options=QtGui.QFileDialog.DontUseNativeDialog)
        if filename=='': return

        with open(filename, 'rb') as csvfile:
            csvfile = csv.reader(csvfile, dialect='excel')
            row = next(csvfile)

        if len(row)==2:
            with open(filename, 'rb') as csvfile:
                csvfile = csv.reader(csvfile, dialect='excel')
                self._time.importchart_csv(csvfile)
        else:
            #FIXME Get directory from where the video was loaded

            # If there are annotation in the timeline, show a warning
            if self._time._tracks_info:  # dict returns True if not empty
                message = ["You are about to import new data. ",
                           "If you proceed, current annotations will be erased. ",
                           "Make sure to export current annotations first to save.",
                           "\n",
                           "Are you sure you want to proceed?"]
                reply = QtGui.QMessageBox.question(self,
                                                   "Warning!",
                                                   "".join(message),
                                                   QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                                   QtGui.QMessageBox.No)
                if reply != QtGui.QMessageBox.Yes: return

            with open(filename, 'rb') as csvfile:
                csvfile = csv.reader(csvfile, dialect='excel')
                self._time.import_csv(csvfile)
            print("Annotations file imported: {:s}".format(filename))

        # Update info after importing from a file
        self._time._update_tracks_info()

    def __export(self):
        """Export annotations to a file."""

        # Update info right before exporting
        self._time._update_tracks_info()

        filename = QtGui.QFileDialog.getSaveFileName(parent=self,
                                                     caption="Export annotations file",
                                                     directory=self.getExportFilename(),
                                                     filter="CSV Files (*.csv)",
                                                     options=QtGui.QFileDialog.DontUseNativeDialog)
        if filename != "":
            with open(filename, 'wb') as csvfile:
                # spamwriter = csv.writer(csvfile, delimiter=';', quotechar='"')
                spamwriter = csv.writer(csvfile, dialect='excel')
                self._time.export_csv(spamwriter)
            print("Annotations file exported: {:s}".format(filename))

    def __cleanLine(self):
        reply = QtGui.QMessageBox.question(self, 'Confirm',
            "Are you sure you want to clean all the events?", QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes: self._time.cleanLine()

    def __cleanCharts(self):
        reply = QtGui.QMessageBox.question(self, 'Confirm',
            "Are you sure you want to clean all the charts?", QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes: self._time.cleanCharts()


    def __clean(self):
        reply = QtGui.QMessageBox.question(self, 'Confirm',
            "Are you sure you want to clean all the events?", QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes: self._time.clean()


    def __pickColor(self):
        self._time.color = QtGui.QColorDialog.getColor(self._time.color)
        if self._time._selected != None:
            self._time._selected.color = self._time.color
            self._time.repaint()

    def __scaleSliderChange(self, value):
        scale = 0.1 * value
        self._time.setMinimumWidth(scale * self._max)
        self._time.scale = scale
        self._zoomLabel.setText( str( value*10 ).zfill(3)+"%" )


    def __scrollAreaKeyReleaseEvent(self, event):
        modifiers = int(event.modifiers())
        self._time.keyReleaseEvent(event)
        if  modifiers!=QtCore.Qt.ControlModifier and \
            modifiers!=int(QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier) and \
            modifiers!=QtCore.Qt.ShiftModifier:
            QtGui.QScrollArea.keyReleaseEvent(self._scrollArea, event)

    def __scrollAreaKeyPressEvent(self, event):
        modifiers = int(event.modifiers())
        if  modifiers!=QtCore.Qt.ControlModifier and \
            modifiers!=int(QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier) and \
            modifiers!=QtCore.Qt.ShiftModifier:
            QtGui.QScrollArea.keyPressEvent(self._scrollArea, event)


    ######################################################################################
    #### PROPERTIES ######################################################################
    ######################################################################################

    @property
    def pointerChanged(self):
        return self._time._pointer.moveEvent
    @pointerChanged.setter
    def pointerChanged(self, value):
        self._time._pointer.moveEvent = value

    @property
    def value(self):  return self._time.position

    @value.setter
    def value(self, value): ControlBase.value.fset(self, value); self._time.position = value

    @property
    def max(self): return self._time.minimumWidth()

    @max.setter
    def max(self, value): self._max = value; self._time.setMinimumWidth(value); self.repaint()

    @property
    def mouseOverLine(self):
        globalPos = QtGui.QCursor.pos()
        widgetPos = self._time.mapFromGlobal(globalPos)
        return self._time.trackInPosition(widgetPos.x(), widgetPos.y())


    # Video playback properties
    @property
    def isPlaying(self):
        return self._time.playVideoEvent
    @isPlaying.setter
    def isPlaying(self, value):
        self._time.playVideoEvent = value

    @property
    def fpsChanged(self): return self._time.fpsChangeEvent
    @fpsChanged.setter
    def fpsChanged(self, value): self._time.fpsChangeEvent = value


    @property
    def form(self): return self
