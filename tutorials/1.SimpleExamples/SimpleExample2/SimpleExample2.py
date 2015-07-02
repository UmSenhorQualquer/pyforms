from __init__ import *



class SimpleExample2(AutoForm):
	
	def __init__(self):
		super(SimpleExample2,self).__init__('Simple example 2')

		#Definition of the forms fields
		self._firstname 	= ControlText('First name', 'Default value')
		self._middlename 	= ControlText('Middle name')
		self._lastname 		= ControlText('Lastname name')
		self._fullname 		= ControlText('Full name')
		self._button 		= ControlButton('Press this button')

		#Define the organization of the forms
		self._formset = ['_firstname','_middlename','_lastname', '_fullname', '_button', ' ']
		#The ' ' is used to indicate that a empty space should be placed at the bottom of the window
		#If you remove the ' ' the forms will occupy the entire window

		#Define the button action
		self._button.value = self.__buttonAction


	def __buttonAction(self):
		"""Button action event"""
		self._fullname.value = self._firstname.value +" "+ self._middlename.value + \
		" "+ self._lastname.value




##################################################################################################################
##################################################################################################################
##################################################################################################################

#Execute the application
if __name__ == "__main__":	 app.startApp( SimpleExample2 )
	