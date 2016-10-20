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
import inspect, platform
import logging
from PyQt4 import QtGui, QtCore
from pysettings import conf

from pyforms.gui.Controls.ControlDockWidget import ControlDockWidget


__author__ = "Ricardo Ribeiro"
__copyright__ = ""
__credits__ = "Ricardo Ribeiro"
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = ["Ricardo Ribeiro", "Carlos Mão de Ferro"]
__email__ = ["ricardojvr at gmail.com", "cajomferro at gmail.com"]
__status__ = "Development"

logger = logging.getLogger(__name__)

class StandAloneContainer(QtGui.QMainWindow):

	def __init__(self, ClassObject):
		super(QtGui.QMainWindow, self).__init__()

		

		w = ClassObject()
		self._widget = w

		if len(w.mainmenu) > 0:
			w._mainmenu = self.__initMainMenu(w.mainmenu)

		w.initForm()
		w.layout().setMargin(conf.PYFORMS_MAINWINDOW_MARGIN)

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
					widget.form.layout().setMargin(conf.PYFORMS_MAINWINDOW_MARGIN)

					# print dock.objectName(),1
					dock.setWidget(widget.form)
					dock.setWindowTitle(widget.label)
					widget.dock = dock
					if not widget._show: dock.hide()

					self.addDockWidget(side, dock)
			else:
				dock = QtGui.QDockWidget(self)
				dock.setFeatures(QtGui.QDockWidget.DockWidgetFloatable |
								 QtGui.QDockWidget.DockWidgetClosable | QtGui.QDockWidget.DockWidgetMovable)
				# dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
				widget.form.layout().setMargin(conf.PYFORMS_MAINWINDOW_MARGIN)

				# print dock.objectName(), 2
				dock.setObjectName(name)
				dock.setWidget(widget.form)
				self.addDockWidget(side, dock)
				dock.setWindowTitle(widget.label)
				widget.dock = dock
				if not widget._show: dock.hide()
	
		if conf.PYFORMS_STYLESHEET:
			stylesheet_files = [conf.PYFORMS_STYLESHEET]

			p = platform.system()
			if p=='Windows' and conf.PYFORMS_STYLESHEET_WINDOWS:
				stylesheet_files.append(conf.PYFORMS_STYLESHEET_WINDOWS)
			elif p=='Darwin' and conf.PYFORMS_STYLESHEET_DARWIN:
				stylesheet_files.append(conf.PYFORMS_STYLESHEET_DARWIN)
			elif p=='Linux' and conf.PYFORMS_STYLESHEET_LINUX:
				stylesheet_files.append(conf.PYFORMS_STYLESHEET_LINUX)

			logger.debug('Import stylesheets: {0}'.format(stylesheet_files)	)	
			self.loadStyleSheetFile(stylesheet_files)
			
		

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

	def loadStyleSheetFile(self, files):
		content = ''
		for filename in files:
			infile = open(filename, 'r')
			content += infile.read() + '\n'
			infile.close()

		self.setStyleSheet(content)



def execute_test_file(myapp):
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("test_file", help="File with the tests script")
	args = parser.parse_args()
	
	with open(args.test_file) as f:
		global_vars = globals()
		local_vars  = locals()
		code = compile(f.read(), args.test_file, 'exec')
		exec(code, global_vars, local_vars)

def startApp(ClassObject, geometry=None):
	from pysettings import conf

	app = QtGui.QApplication(sys.argv)

	conf += 'pyforms.gui.settings'

	mainwindow = StandAloneContainer(ClassObject)

	myapp = mainwindow.centralWidget()

	if geometry is not None:
		mainwindow.show()
		mainwindow.setGeometry(*geometry)
	else:
		mainwindow.showMaximized()


	if conf.PYFORMS_QUALITY_TESTS_PATH is not None: 
		import argparse
		parser = argparse.ArgumentParser()
		parser.add_argument("--test", help="File with the tests script")
		args = parser.parse_args()
		
		if args.test:
			TEST_PATH 				= os.path.join( conf.PYFORMS_QUALITY_TESTS_PATH, args.test )
			TEST_FILE_PATH 			= os.path.join( TEST_PATH, args.test+'.py')
			DATA_PATH 				= os.path.join( TEST_PATH, 'data', sys.platform)
			INPUT_DATA_PATH 		= os.path.join( DATA_PATH, 'input-data')
			OUTPUT_DATA_PATH 		= os.path.join( DATA_PATH, 'output-data')
			EXPECTED_DATA_PATH 		= os.path.join( DATA_PATH, 'expected-data')

			with open(TEST_FILE_PATH) as f:
				global_vars = {} #globals()
				local_vars  = locals()
				code 		= compile(f.read(), TEST_FILE_PATH, 'exec')

				exec(code, global_vars, local_vars)

	app.exec_()
