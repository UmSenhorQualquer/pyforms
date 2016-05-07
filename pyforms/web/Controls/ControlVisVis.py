import datetime, numpy as np
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
		return rows

	@value.setter
	def value(self, value): ControlBase.value.fset(self, value)


	def serialize(self):
		data  = ControlBase.serialize(self)
		data.update({ 
			'legend': 	self.legend, 
			'value': 	self._value 
		})
		return data


	def deserialize(self, properties):
		ControlBase.deserialize(self, properties)
		self.legend = properties[u'legend']
		self.value 	= properties[u'value']
		