# Getting started

This page was based in the examples available on the github folder: [Tutorial - SimpleExamples](https://github.com/UmSenhorQualquer/pyforms/tree/master/tutorials/1.SimpleExamples)


## **Prepare the application class**
***************************

### Create the Python file that will store your applications. Example: SimpleExample.py
### After import pyforms, the BaseWidget and Controls classes you will need:
```python
import pyforms
from   pyforms 			import BaseWidget
from   pyforms.Controls import ControlText
from   pyforms.Controls import ControlButton
```
### Create your application class. This class should inherit from the class BaseWidget.
```python
class SimpleExample1(BaseWidget):
	
	def __init__(self):
		super(SimpleExample1,self).__init__('Simple example 1')

		#Definition of the forms fields
		self._firstname 	= ControlText('First name', 'Default value')
		self._middlename 	= ControlText('Middle name')
		self._lastname 		= ControlText('Lastname name')
		self._fullname 		= ControlText('Full name')
		self._button 		= ControlButton('Press this button')


#Execute the application
if __name__ == "__main__":	 pyforms.startApp( SimpleExample1 )
```

If you run this file, it will produce the next window.

![SimpleExample1](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/docs/imgs/getting-started-1.png?raw=true "Screen")


## **Add an action to the button**
***************************
### Create the class function that will work as the button action.
```python
def __buttonAction(self):
	"""Button action event"""
	self._fullname.value = self._firstname.value +" "+ self._middlename.value +" "+self._lastname.value
```
### Set the function to be executed when the button is pressed. Inside the class constructor add the code:
```python
#Define the button action
self._button.value = self.__buttonAction
```
### The final code should look like:
```python
import pyforms
from   pyforms 			import BaseWidget
from   pyforms.Controls import ControlText
from   pyforms.Controls import ControlButton

class SimpleExample1(BaseWidget):
	
	def __init__(self):
		super(SimpleExample1,self).__init__('Simple example 1')

		#Definition of the forms fields
		self._firstname 	= ControlText('First name', 'Default value')
		self._middlename 	= ControlText('Middle name')
		self._lastname 		= ControlText('Lastname name')
		self._fullname 		= ControlText('Full name')
		self._button 		= ControlButton('Press this button')

		#Define the button action
		self._button.value = self.__buttonAction

	def __buttonAction(self):
		"""Button action event"""
		self._fullname.value = self._firstname.value +" "+ self._middlename.value + \
		" "+ self._lastname.value

#Execute the application
if __name__ == "__main__":	 pyforms.startApp( SimpleExample1 )
```

This previews code will produce the next window, after you press the button:

![SimpleExample1](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/docs/imgs/getting-started-2.png?raw=true "Screen")

