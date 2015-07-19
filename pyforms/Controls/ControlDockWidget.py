import pyforms.Utils.tools as tools
from PyQt4 import uic, QtGui,QtCore
from pyforms.Controls.ControlEmptyWidget import ControlEmptyWidget

class ControlDockWidget(ControlEmptyWidget):

	SIDE_LEFT 		= 'left'
	SIDE_RIGHT 		= 'right'
	SIDE_TOP 		= 'top'
	SIDE_BOTTOM 	= 'bottom'
	SIDE_DETACHED 	= 'detached'

	def __init__(self, label='', default='', side='left'):
		super(ControlDockWidget, self).__init__(label)
		self.value = default
		self.side = side

	@property
	def label(self): return self._label

	@label.setter
	def label(self, value): 
		self._label = value
		self.dock.setWindowTitle(value)


	def save(self, data):
		data['side']=self.side
		super(ControlDockWidget, self).save(data)

	def load(self, data):
		self.side = data['side']
		print data
		super(ControlDockWidget, self).load(data)

