from pyforms.web.Controls.ControlBase import ControlBase

class ControlBoundingSlider(ControlBase):

	_min = 0
	_max = 100

	def __init__(self, label = "", defaultValue=(0,100) , min = 0, max = 100, horizontal=False, helpText=''):
		self._min = min
		self._max = max
		self._horizontal = horizontal
		super(ControlBase, self).__init__(label, defaultValue, helpText)
		
		
	def initControl(self):
		return "new ControlDir('{0}', {1})".format( self._name, str(self.serialize()) )


	def _update(self, minval, maxval): self.value = minval, maxval
		
	def valueChanged(self, value): self.value = value

	def load(self, data):
		if 'value' in data: self.value = data['value']

	def save(self, data):
		if self.value: data['value'] = self.value

		

	@property
	def min(self): return self._min

	@min.setter
	def min(self, value):  self._min = value

	@property
	def max(self): return self._max

	@max.setter
	def max(self, value): self._max = value




	def serialize(self):
		data = super(ControlBase, self).serialize()
		return data.update({ 'max': self.max, 'min': self.min })

	def deserialize(self, properties):
		super(ControlBase, self).deserialize(properties)
		self.max = properties['max']
		self.min = properties['min']