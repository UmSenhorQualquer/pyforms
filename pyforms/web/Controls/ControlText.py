from pyforms.web.Controls.ControlBase import ControlBase

class ControlText(ControlBase):

	def initControl(self):
		return """new ControlText('{0}', {1})""".format(
			self._name, 
			str(self.serialize()) 
		)
