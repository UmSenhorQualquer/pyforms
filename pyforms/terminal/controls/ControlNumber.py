from pyforms.terminal.controls.ControlBase import ControlBase

class ControlNumber(ControlBase):

	def __init__(self, label = "", default = 0, minimum = 0, maximum = 100):
		self._min = minimum
		self._max = maximum
		
		ControlBase.__init__(self, label, default)


	@property
	def min(self): return self._min

	@min.setter
	def min(self, value):  self._min = value

	@property
	def max(self):  return  self._max

	@max.setter
	def max(self, value):  self._max = value