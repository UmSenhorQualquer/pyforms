from pyforms.web.Controls.ControlBase import ControlBase
import cv2
import base64
import numpy as np 
import StringIO
from PIL import Image

class ControlImage(ControlBase):

	def __init__(self, label = "", defaultValue = "", helptext=''):
		self._filename = ''

		ControlBase.__init__(self, label, defaultValue, helptext)

	def initControl(self):
		return "new ControlImage('{0}', {1})".format( self._name, str(self.serialize()) )

	def save(self, data):
		if self.value!=None: data['value'] = self._value

	def load(self, data):
		if 'value' in data: self.value = data['value']

	def repaint(self): pass

	@property
	def value(self): return ControlBase.value.fget(self)

	@value.setter
	def value(self, value):
		if len(value)==0: self._value = ''
		elif isinstance(value, np.ndarray): 			self._value = value
		elif isinstance( value, (str, unicode) ): 	self._value = cv2.imread(value)
		

	def serialize(self):
		data  = ControlBase.serialize(self)
		image = self.value
		if isinstance(image, np.ndarray):
			if len(image.shape)>2: image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
			image = Image.fromarray(image)
			buff = StringIO.StringIO()
			image.save(buff, format="PNG")
			content = buff.getvalue()
			buff.close()
			
			data.update({ 'base64content': base64.b64encode(content) })
		data.update({ 'filename': self._filename })
		return data


	def deserialize(self, properties):
		ControlBase.deserialize(self, properties)
		self._filename = properties['filename']
		self.value = self._filename