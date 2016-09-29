#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


from PyQt4 import QtGui
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebView

from pyforms.gui.Controls.ControlBase import ControlBase

class ControlWeb(ControlBase, QWebView):

    def __init__(self, label = ""):
        QWebView.__init__(self)
        ControlBase.__init__(self, label)

    ############################################################################
    ############ Properties ####################################################
    ############################################################################

    @property
    def value(self): return ControlBase.value.fget(self)
    @value.setter
    def value(self, value):
        ControlBase.value.fset(self, value)
        self.load( QUrl(value) )

    @property
    def form(self): return self