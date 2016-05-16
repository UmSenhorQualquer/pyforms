from pyforms.web.Controls.ControlBase import ControlBase

class ControlLabel(ControlBase):

	def initControl(self):
		return """new ControlLabel('{0}', {1})""".format(
			self._name, 
			str(self.serialize()) 
		)

	@property
	def value(self): return str(ControlBase.value.fget(self))

	@value.setter
	def value(self, value): ControlBase.value.fset(self, value)