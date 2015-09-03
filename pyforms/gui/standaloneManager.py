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
from PyQt4 import QtGui, QtCore

from pyforms.gui.Controls.ControlDockWidget import ControlDockWidget


class StandAloneContainer(QtGui.QMainWindow):

    def __init__(self, ClassObject):
        super(QtGui.QMainWindow, self).__init__()
        w = ClassObject()

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
                for name, widget in widgets:
                    dock = QtGui.QDockWidget(self)
                    dock.setFeatures(QtGui.QDockWidget.DockWidgetFloatable |
                                     QtGui.QDockWidget.DockWidgetClosable | QtGui.QDockWidget.DockWidgetMovable)
                    dock.setObjectName(name)

                    # print dock.objectName(),1
                    dock.setWidget(widget.form)
                    dock.setWindowTitle(widget.label)
                    widget.dock = dock

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

        if len(w.mainmenu) > 0:
            self.__initMainMenu(w.mainmenu)

        try:
            self.loadStyleSheetFile('style.css')
        except:
            pass

    def __initMainMenu(self, options, keys={}):
        menubar = self.menuBar()
        for m in options:
            for key, menus in m.items():
                menu = menubar.addMenu(key)
                for m1 in menus:
                    if isinstance(m1, str) and m1 == "-":
                        menu.addSeparator()
                    else:
                        for text, func in m1.items():
                            action = QtGui.QAction(text, self)
                            if func:
                                action.triggered.connect(func)
                                menu.addAction(action)

    def loadStyleSheetFile(self, filename):
        infile = open(filename, 'r')
        text = infile.read()
        infile.close()
        self.setStyleSheet(text)


def startApp(ClassObject):
    app = QtGui.QApplication(sys.argv)
    w = StandAloneContainer(ClassObject)
    w.showMaximized()
    app.exec_()
