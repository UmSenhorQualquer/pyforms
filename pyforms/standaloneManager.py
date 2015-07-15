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


class StandAloneContainer(QtGui.QMainWindow):

    def __init__(self, ClassObject):
        super(QtGui.QMainWindow, self).__init__()
        w = ClassObject()
        w.initForm()
        self.setCentralWidget(w)
        self.setWindowTitle(w.title)

        for key, item in w.docks.items():
            side = QtCore.Qt.RightDockWidgetArea
            if key == 'left':
                side = QtCore.Qt.LeftDockWidgetArea
            elif key == 'right':
                side = QtCore.Qt.RightDockWidgetArea
            elif key == 'top':
                side = QtCore.Qt.TopDockWidgetArea
            elif key == 'bottom':
                side = QtCore.Qt.BottomDockWidgetArea
            if isinstance(item, list):
                for x in item:
                    dock = QtGui.QDockWidget(self)
                    dock.setWidget(x.form)
                    dock.setWindowTitle(x.label)
                    self.addDockWidget(side, dock)
            else:
                dock = QtGui.QDockWidget(self)
                dock.setWidget(item.form)
                self.addDockWidget(side, dock)
                dock.setWindowTitle(item.label)

        if len(w.mainmenu) > 0:
            self.__initMainMenu(w.mainmenu)

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


def startApp(ClassObject):
    app = QtGui.QApplication(sys.argv)
    w = StandAloneContainer(ClassObject)
    w.showMaximized()
    app.exec_()
