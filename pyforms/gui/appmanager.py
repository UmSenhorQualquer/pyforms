#!/usr/bin/python
# -*- coding: utf-8 -*-
from pyforms.gui.controls.ControlDockWidget import ControlDockWidget
from AnyQt.QtWidgets import QMainWindow, QDockWidget, QAction, QApplication
from AnyQt 			 import QtCore, _api
from AnyQt.QtGui 	 import QIcon

from pyforms.utils.settings_manager import conf
import sys, os, platform, logging

logger = logging.getLogger(__name__)

class StandAloneContainer(QMainWindow):
	def __init__(self, ClassObject):
		super(QMainWindow, self).__init__()

		w = ClassObject()
		w.app_main_window = self
		self._widget = w

		if len(w.mainmenu) > 0:
			w._mainmenu = self.__initMainMenu(w.mainmenu)

		w.init_form()

		if _api.USED_API == _api.QT_API_PYQT5:
			self.layout().setContentsMargins(conf.PYFORMS_MAINWINDOW_MARGIN,conf.PYFORMS_MAINWINDOW_MARGIN,conf.PYFORMS_MAINWINDOW_MARGIN,conf.PYFORMS_MAINWINDOW_MARGIN)
		elif _api.USED_API == _api.QT_API_PYQT4:
			self.layout().setMargin(conf.PYFORMS_MAINWINDOW_MARGIN)

		self.setCentralWidget(w)
		self.setWindowTitle(w.title)

		docks = {}
		for name, item in w.controls.items():
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
					dock = QDockWidget(self)
					dock.setFeatures(
						QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetMovable)
					dock.setObjectName(name)
						
					if _api.USED_API == _api.QT_API_PYQT5:
						dock.setContentsMargins(0,0,0,0)
						widget.form.layout().setContentsMargins(widget.margin,widget.margin,widget.margin,widget.margin)
					elif _api.USED_API == _api.QT_API_PYQT4:
						dock.setMargin(0)
						widget.form.layout().setMargin(widget.margin)

					# print dock.objectName(),1
					dock.setWidget(widget.form)
					dock.setWindowTitle(widget.label)
					widget.dock = dock
					if not widget._show: dock.hide()

					self.addDockWidget(side, dock)
			else:
				dock = QDockWidget(self)
				dock.setFeatures(
					QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetMovable)
				# dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
				
				if _api.USED_API == _api.QT_API_PYQT5:
					widget.form.layout().setContentsMargins(widget.margin,widget.margin,widget.margin,widget.margin)
				elif _api.USED_API == _api.QT_API_PYQT5:
					widget.form.layout().setMargin(widget.margin)

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
			if p == 'Windows' and conf.PYFORMS_STYLESHEET_WINDOWS:
				stylesheet_files.append(conf.PYFORMS_STYLESHEET_WINDOWS)
			elif p == 'Darwin' and conf.PYFORMS_STYLESHEET_DARWIN:
				stylesheet_files.append(conf.PYFORMS_STYLESHEET_DARWIN)
			elif p == 'Linux' and conf.PYFORMS_STYLESHEET_LINUX:
				stylesheet_files.append(conf.PYFORMS_STYLESHEET_LINUX)

			logger.debug('Import stylesheets: {0}'.format(stylesheet_files))
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
								action = QAction(text, self)
								if 'icon' in m1.keys():
									action.setIconVisibleInMenu(True)
									action.setIcon(QIcon(m1['icon']))
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
		local_vars = locals()
		code = compile(f.read(), args.test_file, 'exec')
		exec(code, global_vars, local_vars)


def start_app(ClassObject, geometry=None):
	from pyforms.utils.settings_manager import conf

	app = QApplication(sys.argv)

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
			TEST_PATH = os.path.join(conf.PYFORMS_QUALITY_TESTS_PATH, args.test)
			TEST_FILE_PATH = os.path.join(TEST_PATH, args.test + '.py')
			DATA_PATH = os.path.join(TEST_PATH, 'data', sys.platform)
			INPUT_DATA_PATH = os.path.join(DATA_PATH, 'input-data')
			OUTPUT_DATA_PATH = os.path.join(DATA_PATH, 'output-data')
			EXPECTED_DATA_PATH = os.path.join(DATA_PATH, 'expected-data')

			with open(TEST_FILE_PATH) as f:
				global_vars = {}  # globals()
				local_vars = locals()
				code = compile(f.read(), TEST_FILE_PATH, 'exec')

				exec(code, global_vars, local_vars)

	app.exec_()
	return myapp
