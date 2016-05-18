import datetime
from pyforms.web.Controls.ControlBase import ControlBase

class ControlDate(ControlBase):

	def initControl(self): return "new ControlDate('{0}', {1})".format( self._name, str(self.serialize()) )

	@property
	def value(self): 
		if isinstance(self._value, str):
			return self._value
		elif self._value==None:
			return ''
		else:
			return self._value.strftime("%Y-%m-%d")
			

	@value.setter
	def value(self, value):
		if len(value)>0:
			oldvalue = self._value
			value = datetime.datetime.strptime(value, "%Y-%m-%d")
			print value
			self._value = value
			if oldvalue!=value: self.valueUpdated(value)

