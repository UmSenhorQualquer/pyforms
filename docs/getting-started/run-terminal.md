# Convert the application to run in the terminal

The next code produces this Window:

![Person applications](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/docs/imgs/getting-started-10.png?raw=true "Screen")

```python
import pyforms
from pyforms 			import BaseWidget
from pyforms.Controls 	import ControlText
from pyforms.Controls 	import ControlButton
from Person 			import Person

class PersonWindow(Person, BaseWidget):

	def __init__(self):
		Person.__init__(self, '', '', '')
		BaseWidget.__init__(self,'Person window')
		self.parent = None

		#Definition of the forms fields
		self._firstnameField 	= ControlText('First name')
		self._middlenameField  	= ControlText('Middle name')
		self._lastnameField  	= ControlText('Lastname name')
		self._fullnameField  	= ControlText('Full name')
		self._buttonField  		= ControlButton('Press this button')

		#Define the button action
		self._buttonField.value = self.buttonAction

		self._formset = ['_firstnameField', '_middlenameField', '_lastnameField', 
			'_fullnameField', 
			(' ','_buttonField', ' '), ' ']


	def buttonAction(self):
		self._firstName  = self._firstnameField.value
		self._middleName = self._middlenameField.value
		self._lastName  = self._lastnameField.value
		self._fullnameField.value = self.fullName
		
		#In case the window has a parent
		if self.parent!=None: self.parent.addPerson(self)


#Execute the application
if __name__ == "__main__":	 pyforms.startApp( PersonWindow )
```

But if we create the file **settings.py** in the same directory of the application, and we add to it the next code:
```python
PYFORMS_MODE = 'TERMINAL'
```

The application will behave as a terminal application where the parameters are the names of the variables in the application class.

Type the next code in the terminal: *python PersonWindow.py --help*

You will obtain the next screen:  
![People applications](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/docs/imgs/getting-started-11.png?raw=true "Screen")


Now we can set the parameters and use the parameter exec to define the functions and the execution order we want:

On this case: *python PersonWindow.py --_firstnameField "Jonh" --_middlenameField "Middle" --_lastnameField "White"  --exec "buttonAction|printFullName"*

The function **buttonAction** is called first and the function **printFullName** is called after.

Check out the result:  
![People applications](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/docs/imgs/getting-started-9.png?raw=true "Screen")

**Note:** Not all the Controls are implemented for the TERMINAL mode. Please check the sign ![Terminal ready](https://img.shields.io/badge/TERMINAL-READY-green.svg "Screen") in the API to know which ones are.