#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Ricardo Ribeiro"
__credits__ = ["Ricardo Ribeiro"]
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = "Ricardo Ribeiro"
__email__ = "ricardojvr@gmail.com"
__status__ = "Development"

from pysettings import conf

if conf.PYFORMS_USE_QT5:
	from PyQt5.QtWebEngineWidgets import QWebEngineView
	from PyQt5.QtCore import QUrl
else:
	from PyQt4.QtCore import QUrl
	from PyQt4.QtWebKit import QWebView

from pyforms.gui.Controls.ControlBase import ControlBase


class ControlWeb(ControlBase, QWebEngineView):
	def __init__(self, label=""):
		QWebEngineView.__init__(self)
		ControlBase.__init__(self, label)

	############################################################################
	############ Properties ####################################################
	############################################################################

	@property
	def value(self): return ControlBase.value.fget(self)

	@value.setter
	def value(self, value):
		ControlBase.value.fset(self, value)
		QWebEngineView.load(self, QUrl(value))

	@property
	def form(self):
		return self
