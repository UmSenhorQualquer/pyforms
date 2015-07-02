
from Controls.ControlBase import ControlBase
from datetime import datetime, timedelta
from PyQt4 import uic, QtGui, QtCore
from BaseWidget import BaseWidget
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