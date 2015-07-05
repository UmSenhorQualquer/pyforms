from __init__ import *
from People import People
from PersonWindow import PersonWindow
from AddMenuFuntionality import AddMenuFuntionality

class PeopleWindow(AddMenuFuntionality, People, AutoForm):
	"""
	This applications is a GUI implementation of the People class
	"""

	def __init__(self):
		People.__init__(self)
		AutoForm.__init__(self,'People window')

		#Definition of the forms fields
		self._peopleList 	= ControlList('People')
		self._addPersonBtn  = ControlButton('Add person')
		self._rmPersonBtn   = ControlButton('Remove person')

		self._peopleList.selectEntireRow = True

		self._formset = ['_peopleList', (' ','_rmPersonBtn','_addPersonBtn') ]

		#Define the button action
		self._addPersonBtn.value = self.__addPersonBtnAction
		self._rmPersonBtn.value  = self.__rmPersonBtnAction
		

	def addPerson(self, person):
		"""
		Redifines the addPerson function from People class to update the GUI everytime a new person is added.
		"""
		super(PeopleWindow, self).addPerson(person)
		self._peopleList += [person._firstName, person._middleName, person._lastName]


	def __addPersonBtnAction(self):
		"""
		Add person button event
		"""
		win = PersonWindow()
		win.parent = self
		win.show()

	def __rmPersonBtnAction(self):
		"""
		Remove person button event
		"""
		self.removePerson( self._peopleList.mouseSelectedRowIndex )
		self._peopleList -= self._peopleList.mouseSelectedRowIndex
		




##################################################################################################################
##################################################################################################################
##################################################################################################################

#Execute the application
if __name__ == "__main__":	 app.startApp( PeopleWindow )