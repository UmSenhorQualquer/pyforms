#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.Controls.ControlMdiArea"""

import logging

from PyQt4 import QtCore
from PyQt4.QtGui import QMdiArea

from pyforms.gui.Controls.ControlBase import ControlBase

__author__ = "Ricardo Ribeiro"
__copyright__ = ""
__credits__ = "Carlos Mão de Ferro"
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = ["Ricardo Ribeiro", "Carlos Mão de Ferro"]
__email__ = ["ricardojvr at gmail.com", "cajomferro at gmail.com"]
__status__ = "Development"


class ControlMdiArea(ControlBase, QMdiArea):
    """
    The ControlMdiArea wraps a QMdiArea widget which provides
     an area in which MDI windows are displayed.
    """

    def __init__(self, label=""):
        QMdiArea.__init__(self)
        ControlBase.__init__(self, label)
        self._value = []
        self._showCloseButton = True
        self._openWindows = []

        self.logger = logging.getLogger(__name__)

    def initForm(self): pass

    def __flags(self):
        flags = QtCore.Qt.SubWindow

        flags |= QtCore.Qt.WindowTitleHint
        flags |= QtCore.Qt.WindowMinimizeButtonHint
        flags |= QtCore.Qt.WindowMaximizeButtonHint
        if self._showCloseButton:
            flags |= QtCore.Qt.WindowSystemMenuHint
            flags |= QtCore.Qt.WindowCloseButtonHint

        return flags

    def __sub__(self, window):
        if window.title in self._openWindows:
            window.close()
        return self

    def __add__(self, other):
        #check if the window already was added.
        #If yes, show it again
        #If not create it
        if other.title not in self._openWindows and not hasattr(other, 'subwindow'):
            if not other._formLoaded:other.initForm()
            other.subwindow = self.addSubWindow(other)
            other.subwindow.overrideWindowFlags(self.__flags())
            other.show()
            other.closeEvent = lambda x: self._subWindowClosed(x, window=other)

            self.value.append(other)
            self._openWindows.append(other.title)
        else:
            other.subwindow.show()
            other.show()
        other.setFocus()
        return self

    def _subWindowClosed(self, closeEvent, window=None):

        if window:
            activeWidget = window
            window       = window.subwindow
        else:
            window       = self.activeSubWindow()
            activeWidget = self.activeSubWindow().widget()
           
        #If beforeClose return False, will just hide the window.
        #If return True or None remove it from the mdi area
        res = activeWidget.beforeClose() 
        if res is None or res is True:
            if activeWidget in self._value: self._value.remove(activeWidget)
            self.removeSubWindow(window)
            self._openWindows.remove(activeWidget.title)
            closeEvent.accept()
        else:
            closeEvent.ignore()
            window.hide()

    def update_window_title(self, old_title, new_title):
        self._openWindows.remove(old_title)
        self._openWindows.append(new_title)

    ##########################################################################
    ############ Properties ##################################################
    ##########################################################################

    @property
    def showCloseButton(self): return self._showCloseButton

    @showCloseButton.setter
    def showCloseButton(self, value): self._showCloseButton = value

    @property
    def label(self): return self._label

    @label.setter
    def label(self, value): self._label = value

    @property
    def form(self): return self

    @property
    def value(self): return ControlBase.value.fget(self)

    @value.setter
    def value(self, value):
        self.closeAllSubWindows()
        self._value = []

        if isinstance(value, list):
            for w in value:
                self += w
        else:
            self += value

        ControlBase.value.fset(self, self._value)
