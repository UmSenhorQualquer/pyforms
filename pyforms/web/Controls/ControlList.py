from pyforms.web.Controls.ControlBase import ControlBase

class ControlList(ControlBase):

	def __init__(self, label = "", defaultValue = "", helptext=''):
		self._titles 			= []
		self._selectEntireRow 	= False
		self._read_only 		= False
		self._selected_index 	= -1
		super(ControlList, self).__init__(label, defaultValue, helptext)


	def initControl(self): return "new ControlList('{0}', {1})".format( self._name, str(self.serialize()) )



	@property
	def horizontalHeaders(self): return self._titles

	@horizontalHeaders.setter
	def horizontalHeaders(self, value): self._titles = value

	@property
	def selectEntireRow(self): return self._selectEntireRow

	@selectEntireRow.setter
	def selectEntireRow(self, value): self._selectEntireRow = value

	@property
	def readOnly(self): return self._read_only

	@readOnly.setter
	def readOnly(self, value): self._read_only = value

	@property
	def mouseSelectedRowIndex(self): return self._selected_index


	def serialize(self):
		data 	= ControlBase.serialize(self)
		
		data.update({ 
			'horizontal_headers': 	self._titles,
			'read_only':			1 if self._read_only else 0,
			'selected_index':		self._selected_index,
			'select_entire_row': 	1 if self._selectEntireRow else 0,
		})
		return data
		
	def deserialize(self, properties):
		ControlBase.deserialize(self,properties)
		
		self.horizontalHeaders 	= properties['horizontal_headers']
		self._read_only 		= properties['read_only']==1
		self._selected_index 	= properties['selected_index']
		self._selectEntireRow 	= properties['select_entire_row']==1