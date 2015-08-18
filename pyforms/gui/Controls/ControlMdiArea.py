#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.Controls.ControlMdiArea"""

from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from pyforms.gui.Controls.ControlBase import ControlBase

__author__ = "Carlos Mão de Ferro"
__copyright__ = ""
__credits__ = "Carlos Mão de Ferro"
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = ["Ricardo Ribeiro", "Carlos Mão de Ferro"]
__email__ = ["ricardojvr at gmail.com", "cajomferro at gmail.com"]
__status__ = "Development"


class ControlMdiArea(ControlBase):
    """
    The ControlMdiArea wraps a QMdiArea widget which provides
     an area in which MDI windows are displayed.
    """

    def initForm(self):
        self._form = QtGui.QMdiArea()
        ControlBase.value.fset(self, [])

    ##########################################################################
    ############ Properties ##################################################
    ##########################################################################

    @property
    def value(self): return ControlBase.value.fget(self)

    @value.setter
    def value(self, value):
        """" @value: list of widgets to be added as subwindows"""
        # if isinstance(self._value, list):
        #    for w in self._value:

        #        if w is not None and w != "":
        #            self._form.addSubWindow(w.form)
        # else:
        #    if self._value is not None and self._value != "":
        #        self._form.addSubWindow(value.form)
        for widget in value:
            if widget not in self._value:
                subWindow = QtGui.QMdiSubWindow()
                subWindow.setWidget(widget.form)
                subWindow.setAttribute(Qt.WA_DeleteOnClose)
                self._form.addSubWindow(subWindow)
                subWindow.hide()

                #subWindow.closeEvent = self._subWindowClosed

        ControlBase.value.fset(self, value)

    def showSubWindow(self, widget):
        for subWindow in self._form.subWindowList():
            if subWindow.widget() == widget:
                subWindow.show()

    # def _subWindowClosed(self, closeEvent):
    #    activeWidget = self._form.activeSubWindow().widget()
    #    if activeWidget in self._value:
    #        self._value.remove(activeWidget)
    #    closeEvent.accept()
