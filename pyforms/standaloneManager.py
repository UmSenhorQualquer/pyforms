#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


import sys, glob, os
from PyQt4 import uic
from PyQt4 import QtGui, QtCore
import pyforms.Utils.tools as tools

class StandAloneContainer(QtGui.QMainWindow):
	def __init__(self, ClassObject):
		super(QtGui.QMainWindow, self).__init__()
		w = ClassObject()
		w.initForm()
		self.setCentralWidget(w)
		self.setWindowTitle( w.title )

		for key, dock in w.docks.items():
			side = QtCore.Qt.RightDockWidgetArea
			if key=='left':
				side = QtCore.Qt.LeftDockWidgetArea
			elif key=='right':
				side = QtCore.Qt.RightDockWidgetArea
			elif key=='top':
				side = QtCore.Qt.TopDockWidgetArea
			elif key=='bottom':
				side = QtCore.Qt.BottomDockWidgetArea
			if isinstance(dock,list):
				for x in dock: self.addDockWidget( side , x.form )
			else:
				self.addDockWidget( side , dock.form )


		if len(w.mainmenu)>0: self.__initMainMenu( w.mainmenu )

		
	def __initMainMenu(self, options, keys={}):
		menubar = self.menuBar()
		for m in options:
			for key, menus in m.items():
				menu = menubar.addMenu( key )
				for m1 in menus:
					if isinstance(m1, str) and m1=="-":
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