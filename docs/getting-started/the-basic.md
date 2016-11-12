# The basic

*This page was based on the examples available at the github folder: [Tutorial - SimpleExamples](https://github.com/UmSenhorQualquer/pyforms/tree/master/tutorials/1.SimpleExamples)*


## **Prepare the application class**
***************************

### Create the Python file that will store your applications. 

Example: **SimpleExample.py**

### Import the library.

Import the pyforms library, the BaseWidget and the Controls classes that you will need:
```python
import pyforms
from   pyforms 			import BaseWidget
from   pyforms.Controls import ControlText
from   pyforms.Controls import ControlButton
```

### Create your application class.

This class should inherit from the class BaseWidget.
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
if __name__ == "__main__":	 pyforms.start_app( SimpleExample1 )
```

If you run this file, it will produce the next window.

![SimpleExample1](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/docs/imgs/getting-started-1.png?raw=true "Screen")


## **Add an action to the button**
***************************

### Create the action

Create the class function that will work as the button action.
```python
def __buttonAction(self):
	"""Button action event"""
	self._fullname.value = self._firstname.value +" "+ self._middlename.value +" "+self._lastname.value
```
### Set the button action

Configure the button to execute your function when pressed.  
Inside the class constructor add the code:
```python
#Define the button action
self._button.value = self.__buttonAction
```

The final code should look like:
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
if __name__ == "__main__":	 pyforms.start_app( SimpleExample1 )
```

The previous code produces the next window, after you had pressed the button:

![SimpleExample1](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/docs/imgs/getting-started-2.png?raw=true "Screen")





## **Organize your form Controls**
***************************

Use the BaseWidget._formset variable to organize the Controls inside the Window.  
[Find here more details about the _formset variable](http://pyforms.readthedocs.org/en/latest/api-documentation/basewidget/#important-variables)


```python
...

class SimpleExample1(BaseWidget):
	
	def __init__(self):
		...

		#Define the organization of the forms
		self._formset = [ ('_firstname','_middlename','_lastname'), '_button', '_fullname', ' ']
		#The ' ' is used to indicate that a empty space should be placed at the bottom of the window
		#If you remove the ' ' the forms will occupy the entire window

	...
```

Result:

![SimpleExample1](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/docs/imgs/getting-started-3.png?raw=true "Screen")

Try now:
```python
self._formset = [ {
		'Tab1':['_firstname','||','_middlename','||','_lastname'], 
		'Tab2': ['_fullname']
	},
	'=',(' ','_button', ' ') ]
#Use dictionaries for tabs
#Use the sign '=' for a vertical splitter
#Use the signs '||' for a horizontal splitter
```

## **Add a main menu**
***************************

To add a main menu to your application, first you need to define the functions that will work as the options actions.

```python
...

class SimpleExample1(BaseWidget):
	...

	def __openEvent(self):
		...

	def __saveEvent(self):
		...

	def __editEvent(self):
		...

	def __pastEvent(self):
		...
```

After you just need to set the BaseWidget.mainmenu property inside your application class constructor as the example bellow.

```python
...

class SimpleExample1(BaseWidget):
	
	def __init__(self):
		...
		self.mainmenu = [
			{ 'File': [
					{'Open': self.__openEvent},
					'-',
					{'Save': self.__saveEvent},
					{'Save as': self.__saveAsEvent}
				]
			},
			{ 'Edit': [
					{'Copy': self.__editEvent},
					{'Past': self.__pastEvent}
				]
			}
		]

	...
```

## **Add popup menu to the Controls**
***************************

Create the functions that will work as the popup menu options actions, as you have than in the main menu chapter. After use the functions **addPopupMenuOption** or **addPopupSubMenuOption** to add a popup menu or a popup submenu to your Control.

[Find here more details about the functions addPopupMenuOption and addPopupSubMenuOption.](http://pyforms.readthedocs.org/en/latest/api-documentation/controls/#controlbase)

```python
...

class SimpleExample1(BaseWidget):
	
	def __init__(self):
		...

		self._fullname.addPopupSubMenuOption('Path', 
			{
				'Delete':           self.__dummyEvent, 
				'Edit':             self.__dummyEvent,
				'Interpolate':      self.__dummyEvent
			})
	...
```	

Result:

![SimpleExample1](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/docs/imgs/getting-started-4.png?raw=true "Screen")


## **What next?**
***************************

### Move to the [next chapter](http://pyforms.readthedocs.org/en/latest/getting-started/multiple-windows/)


### Find out what you can do with other Controls [here](http://pyforms.readthedocs.org/en/latest/api-documentation/controls/)


![Example 1](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/2.ControlsExamples/Example1.png?raw=true "Screen")

![Example 2](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/2.ControlsExamples/Example2.png?raw=true "Screen")

![Example 3](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/2.ControlsExamples/Example3.png?raw=true "Screen")