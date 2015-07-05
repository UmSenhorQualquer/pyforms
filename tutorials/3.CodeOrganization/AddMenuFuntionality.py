from PyQt4 import QtGui

class AddMenuFuntionality(object):

	def initForm(self):
		self.mainmenu.append(
				{ 'File': [
						{'Save as': self.__savePeople},
						{'Open as': self.__loadPeople},
						'-',
						{'Exit': self.__exit},
					]
				}
			)

		super(AddMenuFuntionality,self).initForm()

	def __savePeople(self):
		filename = QtGui.QFileDialog.getSaveFileName(parent=self,
			caption="Save file",
			directory=".",
			filter="*.dat")

		if filename!=None and filename!='': self.save(filename)

	def __loadPeople(self):
		filename = QtGui.QFileDialog.getOpenFileName(parent=self,
			caption="Import file",
			directory=".",
			filter="*.dat")

		if filename!=None and filename!='': 
			self.load(filename)
			for person in self._people:
				self._peopleList += [person._firstName, person._middleName, person._lastName]


	def __exit(self):
		exit()