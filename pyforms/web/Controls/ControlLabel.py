from pyforms.web.Controls.ControlBase import ControlBase

class ControlLabel(ControlBase):

	def __init__(self, label = "", defaultValue = "", helptext=''):
		self._css = ''
		super(ControlLabel, self).__init__(label, defaultValue, helptext)

	def initControl(self):
		return """new ControlLabel('{0}', {1})""".format(
			self._name, 
			str(self.serialize()) 
		)

	@property
	def css(self): return self._css

	@css.setter
	def css(self, value): self._css = value

	def serialize(self):
		data = ControlBase.serialize(self)
		data.update({ 'css': self.css })
		return data
		
	def deserialize(self, properties):
		ControlBase.deserialize(self,properties)
		self.css = properties[u'css']
