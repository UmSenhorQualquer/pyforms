from __init__ import *
from Person import Person

class PersonWindow(Person, BaseWidget):


	def __init__(self):
		Person.__init__(self, '', '', '')
		BaseWidget.__init__(self,'Person window')

		#Definition of the forms fields
		self._firstnameField 	= ControlText('First name')
		self._middlenameField  	= ControlText('Middle name')
		self._lastnameField  	= ControlText('Lastname name')
		self._fullnameField  	= ControlText('Full name')
		self._buttonField  		= ControlButton('Press this button')

		#Define the button action
		self._buttonField.value = self.__buttonAction


	def __buttonAction(self):
		self._firstName  = self._firstnameField.value
		self._middleName = self._middlenameField.value
		self._lastName  = self._lastnameField.value
		self._fullnameField.value = self.fullName
		
		#In case the window has a parent
		if self.parent!=None: self.parent.addPerson(self)





##################################################################################################################
##################################################################################################################
##################################################################################################################

#Execute the application
if __name__ == "__main__":	 pyforms.startApp( PersonWindow )