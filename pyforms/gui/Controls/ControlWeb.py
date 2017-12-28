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
    from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView
    from PyQt5.QtCore import QUrl
else:
    from PyQt4.QtCore import QUrl
    from PyQt4.QtWebKit import QWebView

from pyforms.gui.Controls.ControlBase import ControlBase


class ControlWeb(ControlBase, QWebView):
    def __init__(self, *args, **kwargs):
        QWebView.__init__(self)
        if 'load_finnished_event' in kwargs: 
            self.load_finnished_event=kwargs['load_finnished_event']
        self.loadFinished.connect(self.__load_finnished_evt)
        ControlBase.__init__(self, *args, **kwargs)

        
    def init_form(self):
        """
        Load Control and initiate the events
        """
        ControlBase.init_form(self)
        if self._value: QWebView.load(self, QUrl(self._value))
        if self.help: self.form.setToolTip(self.help)
    ############################################################################
    ############ Properties ####################################################
    ############################################################################

    def __load_finnished_evt(self, ok):
        self.load_finnished_event(ok)

    def load_finnished_event(self,ok):
        pass

    @property
    def value(self): return ControlBase.value.fget(self)

    @value.setter
    def value(self, value):
        ControlBase.value.fset(self, value)
        QWebView.load(self, QUrl(value))

    @property
    def form(self):
        return self
