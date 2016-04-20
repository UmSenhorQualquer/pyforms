import datetime
from pyforms.web.Controls.ControlBase import ControlBase

class ControlVisVis(ControlBase):

	def __init__(self, label = "", defaultValue = "", helptext=None):
		self._legend = []
		super(ControlVisVis, self).__init__(label, defaultValue, helptext)

	def initControl(self): return "new ControlVisVis('{0}', {1})".format( self._name, str(self.serialize()) )



	@property
	def legend(self):return self._legend
	@legend.setter
	def legend(self, value): 
		self._legend = value


	@property
	def value(self):
		rows = []
		for row in self._value:
			new_row = []
			for value in row:
				if value is None or len(value)==0: break
				if isinstance(value[0], datetime.datetime): value[0] = unicode(value[0])
				if isinstance(value[0], datetime.date): value[0] = unicode(value[0])
				if isinstance(value[0], unicode): value[0] = str(value[0])
				if isinstance(value[1], unicode): value[1] = str(value[1])
				new_row.append(value)
			rows.append(new_row)

		return {'legend': self.legend, 'data': rows}

	@value.setter
	def value(self, value): 
		if isinstance(value, dict):
			self.legend = value['legend']
			data   	    = value['data']
		else:
			data = value
		ControlBase.value.fset(self, data)


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