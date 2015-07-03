#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"



from pyforms.Controls.ControlBase import ControlBase
from datetime import datetime, timedelta
from PyQt4 import uic, QtGui, QtCore
from pyforms.BaseWidget import BaseWidget
import time, subprocess, os

class AutoForm(BaseWidget):

	def __init__(self, title):
		super(AutoForm, self).__init__(title)
		self.layout().setMargin(0)

	def initForm(self):
		"""
		Generate the module Form
		"""


		super(AutoForm,self).initForm()