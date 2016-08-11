#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
@author: Ricardo Ribeiro
@credits: Ricardo Ribeiro
@license: MIT
@version: 0.0
@maintainer: Ricardo Ribeiro
@email: ricardojvr@gmail.com
@status: Development
@lastEditedBy: Carlos Mão de Ferro (carlos.maodeferro@neuro.fchampalimaud.org)
'''

import sys
import os
import inspect
import logging
from PyQt4 import QtGui, QtCore

from pyforms.gui.Controls.ControlDockWidget import ControlDockWidget

__author__ = "Ricardo Ribeiro"
__copyright__ = ""
__credits__ = "Ricardo Ribeiro"
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = ["Ricardo Ribeiro", "Carlos Mão de Ferro"]
__email__ = ["ricardojvr at gmail.com", "cajomferro at gmail.com"]
__status__ = "Development"


class StandAloneContainer(QtGui.QMainWindow):

    def __init__(self, ClassObject):
        super(QtGui.QMainWindow, self).__init__()

        self.logger = logging.getLogger(__name__)

        self.logger.debug("Loading window as standalone container...")

        w = ClassObject()
        self._widget = w

        if len(w.mainmenu) > 0:
            w._mainmenu = self.__initMainMenu(w.mainmenu)

        w.initForm()
        self.setCentralWidget(w)
        self.setWindowTitle(w.title)

        docks = {}
        for name, item in w.formControls.items():
            if isinstance(item, ControlDockWidget):
                if item.side not in docks:
                    docks[item.side] = []
                docks[item.side].append((name, item))

        for key, widgets in docks.items():
            side = QtCore.Qt.RightDockWidgetArea
            if key == 'left':
                side = QtCore.Qt.LeftDockWidgetArea
            elif key == 'right':
                side = QtCore.Qt.RightDockWidgetArea
            elif key == 'top':
                side = QtCore.Qt.TopDockWidgetArea
            elif key == 'bottom':
                side = QtCore.Qt.BottomDockWidgetArea
            else:
                side = QtCore.Qt.LeftDockWidgetArea

            if isinstance(widgets, list):
                widgets = sorted(widgets, key=lambda x: x[1].order)

                for name, widget in widgets:
                    dock = QtGui.QDockWidget(self)
                    dock.setFeatures(QtGui.QDockWidget.DockWidgetFloatable |
                                     QtGui.QDockWidget.DockWidgetClosable | QtGui.QDockWidget.DockWidgetMovable)
                    dock.setObjectName(name)

                    # print dock.objectName(),1
                    dock.setWidget(widget.form)
                    dock.setWindowTitle(widget.label)
                    widget.dock = dock
                    if not widget._show:
                        dock.hide()

                    self.addDockWidget(side, dock)
            else:
                dock = QtGui.QDockWidget(self)
                dock.setFeatures(QtGui.QDockWidget.DockWidgetFloatable |
                                 QtGui.QDockWidget.DockWidgetClosable | QtGui.QDockWidget.DockWidgetMovable)
                # dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
                # dock.layout().setMargin(0)

                # print dock.objectName(), 2
                dock.setObjectName(name)
                dock.setWidget(widget.form)
                self.addDockWidget(side, dock)
                dock.setWindowTitle(widget.label)
                widget.dock = dock
                if not widget._show:
                    dock.hide()

        try:
            directory = os.path.dirname(inspect.getfile(w.__class__))
            self.loadStyleSheetFile(os.path.join(directory, 'style.css'))
        except:
            pass

    def closeEvent(self, event):
        self._widget.closeEvent(event)

    def __initMainMenu(self, options, keys={}):
        menubar = self.menuBar()
        for menuIndex, m in enumerate(options):
            for key, menus in m.items():
                menu = menubar.addMenu(key)
                for subMenuIndex, m1 in enumerate(menus):
                    if isinstance(m1, str) and m1 == "-":
                        menu.addSeparator()
                    else:
                        for text, func in m1.items():
                            if text != 'icon':
                                action = QtGui.QAction(text, self)
                                if 'icon' in m1.keys():
                                    action.setIconVisibleInMenu(True)
                                    action.setIcon(QtGui.QIcon(m1['icon']))
                                if func:
                                    action.triggered.connect(func)
                                    menu.addAction(action)
                                options[menuIndex][key][subMenuIndex][text] = action
                                break
        return options

    def loadStyleSheetFile(self, filename):
        infile = open(filename, 'r')
        text = infile.read()
        infile.close()
        self.setStyleSheet(text)

MAIN_APP = None

def startApp(ClassObject, geometry=None):
    global MAIN_APP

    app = QtGui.QApplication(sys.argv)
    w = StandAloneContainer(ClassObject)

    MAIN_APP = w.centralWidget()

    if geometry is not None:
        w.show()
        w.setGeometry(*geometry)
    else:
        w.showMaximized()

    app.exec_()
