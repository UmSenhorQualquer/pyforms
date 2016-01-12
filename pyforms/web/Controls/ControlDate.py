import datetime
from pyforms.web.Controls.ControlBase import ControlBase

class ControlDate(ControlBase):

	def __init__(self, label = "", defaultValue = "", helptext=None):
		super(ControlDate, self).__init__(label, defaultValue, helptext)

	def initControl(self):
		return """controls.push(new ControlDate('{0}','{1}','{3}','{2}'));""".format(self._label, self._name, self.help, self.value)
