from pyforms.web.Controls.ControlBase import ControlBase

class ControlList(ControlBase):

	def __init__(self, label = "", defaultValue = "", helptext=None):
		self._titles = []
		self._selectEntireRow = False
		self._read_only = False
		self._selected_index = -1
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

	@property
	def json(self):
		res = []
		biggest_row = 0
		for row in self.value:
			biggest_row = biggest_row if len(row)<biggest_row else len(row)
			res.append(row)

		if len(self._titles)<biggest_row:
			self._titles += [str(i) for i in range( biggest_row-len(self._titles) )]

		return [
			self._titles, 
			res, 
			1 if self.selectEntireRow else 0,
			1 if self.readOnly else 0,
			self._selected_index] 
		
	@json.setter
	def json(self, value): 
		self.horizontalHeaders = value[0]
		self.value = value[1]
		self.selectEntireRow = value[2]
		self.readOnly = value[3]
		self._selected_index = value[4]
		