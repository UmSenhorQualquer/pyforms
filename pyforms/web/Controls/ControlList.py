from pyforms.web.Controls.ControlBase import ControlBase

class ControlList(ControlBase):

	def __init__(self, label = "", defaultValue = "", helptext=None):
		self._titles = []
		super(ControlList, self).__init__(label, defaultValue, helptext)


	def initControl(self):
		values = self.json
		return """controls.push(new ControlList('{0}','{1}',{3},'{2}'));""".format(self._label, self._name, self.help, values)



	@property
	def horizontalHeaders(self): return self._titles

	@horizontalHeaders.setter
	def horizontalHeaders(self, value):self._titles = value



	@property
	def json(self):
		res = []
		biggest_row = 0
		for row in self.value:
			biggest_row = biggest_row if len(row)<biggest_row else len(row)
			res.append(row)

		if len(self._titles)<biggest_row:
			self._titles += [str(i) for i in range( biggest_row-len(self._titles) )]

		return [self._titles, res]
		
	@json.setter
	def json(self, value): 
		self.horizontalHeaders = value[0]
		self.value = value[1]
		