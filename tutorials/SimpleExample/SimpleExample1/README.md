# Simple example 1

This example shows the most simple way of creating a windows form application using pyforms.


```python
class SimpleExample1(AutoForm):
	
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
```

![Simple example 1](screenshot.png?raw=true "Screen")