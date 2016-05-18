from pyforms.web.Controls.ControlBase import ControlBase

class ControlFile(ControlBase):

	def __init__(self, label = "", defaultValue = "", helptext=''):
		self._filename = ''
		ControlBase.__init__(self, label, defaultValue, helptext)

	def initControl(self):
		return "new ControlFile('{0}', {1})".format( self._name, str(self.serialize()) )

	@property
	def value(self): return str(ControlBase.value.fget(self))

	@value.setter
	def value(self, value): ControlBase.value.fset(self, value)
