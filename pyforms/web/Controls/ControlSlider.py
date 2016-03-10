from pyforms.web.Controls.ControlBase import ControlBase


class ControlSlider(ControlBase):

	_min = 0
	_max = 100

	def __init__(self, label = "", defaultValue = 0, min = 0, max = 100):
		self._updateSlider = True
		self._min = min
		self._max = max
		
		ControlBase.__init__(self, label, defaultValue)
		
	def initControl(self): return "new ControlSlider('{0}', {1})".format( self._name, str(self.serialize()) )

	def valueChanged(self, value):
		self._updateSlider = False
		self.value = value
		self._updateSlider = True


	def changed(self): pass
	

	@property
	def min(self): return self._min

	@min.setter
	def min(self, value):  self._min = value

	@property
	def max(self):  return  self._max

	@max.setter
	def max(self, value):  self._max = value


	def serialize(self):
		data = ControlBase.serialize(self)
		data.update({ 'max': self.max, 'min': self.min })
		return data
		
	def deserialize(self, properties):
		ControlBase.deserialize(self,properties)
		self.max = properties[u'max']
		self.min = properties[u'min']
		