# Multiple windows

*This page was based on the examples available at the github folder: [Tutorial - Code Organization](https://github.com/UmSenhorQualquer/pyforms/tree/master/tutorials/3.CodeOrganization)*

The application described on this page will allow us to add People details to a list.

## **Create the Model**
***************************

Instead of starting by showing you how to develop the GUI I will suggest first how to modularize the code in a Model View Control (MVC) style.

First we will create our data model which may be used outside the GUI.

### Data model

Start by creating the file Person.py where we will implement the model responsible for storing the a person information.

```python
class Person(object):

	def __init__(self, firstName, middleName, lastName):
		self._firstName 	= firstName
		self._middleName 	= middleName
		self._lastName 		= lastName

	@property 
	def fullName(self):
		return "{0} {1} {2}".format(self._firstName, self._middleName, self._lastName)
```

After, create the file People.py and implement the People class which will keep and manage the list of people.

```python
import pickle

class People(object):

	def __init__(self):
		self._people = []

	def addPerson(self, person):
		self._people.append(person)

	def removePerson(self, index):
		return self._people.pop(index)

	def save(self, filename):
		output = open(filename, 'wb')
		pickle.dump(self._people, output)

	def load(self, filename):
		pkl_file = open(filename, 'rb')
		self._people = pickle.load(pkl_file)
```
  

## **Let's go for the GUI**
***************************

To make our code modular and easy to navigate we will split the edition of the 2 Models in 2 different windows.

### Implement the GUI to manage the Person Model.

Create the file PersonWindow.py and implement the window that will allow us the edit the Person Model.  
This window should inherit from the BaseWidget and Person classes.

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

		#Definition of the forms fields
		self._firstnameField 	= ControlText('First name')
		self._middlenameField  	= ControlText('Middle name')
		self._lastnameField  	= ControlText('Lastname name')
		self._fullnameField  	= ControlText('Full name')
		self._buttonField  		= ControlButton('Press this button')

		#Define the button action
		self._buttonField.value = self.__buttonAction


	def __buttonAction(self):
		self._firstName  			= self._firstnameField.value
		self._middleName 			= self._middlenameField.value
		self._lastName  			= self._lastnameField.value
		self._fullnameField.value 	= self.fullName
		
		#In case the window has a parent
		if self.parent!=None: self.parent.addPerson(self)

#Execute the application
if __name__ == "__main__":	 pyforms.start_app( PersonWindow )
```

**Note**: *Test the window by executing the file.*

### Implement the GUI to manage the People model.

Create the file PeopleWindow.py and implement the window that will allow us the manager the People Model.  
This window should inherit from the BaseWidget and People classes.

```python
import pyforms
from pyforms 				import BaseWidget
from pyforms.Controls  		import ControlList
from People 				import People
from PersonWindow 			import PersonWindow
from AddMenuFuntionality 	import AddMenuFuntionality

class PeopleWindow(AddMenuFuntionality, People, BaseWidget):
	"""
	This applications is a GUI implementation of the People class
	"""

	def __init__(self):
		People.__init__(self)
		BaseWidget.__init__(self,'People window')

		#Definition of the forms fields
		self._peopleList	= ControlList('People', 
			plusFunction	= self.__addPersonBtnAction, 
			minusFunction	= self.__rmPersonBtnAction)

		self._peopleList.horizontalHeaders = ['First name', 'Middle name', 'Last name']

	def addPerson(self, person):
		"""
		Reimplement the addPerson function from People class to update the GUI 
		everytime a new person is added.
		"""
		super(PeopleWindow, self).addPerson(person)
		self._peopleList += [person._firstName, person._middleName, person._lastName]
		person.close() #After adding the person close the window

	def removePerson(self, index):
		"""
		Reimplement the removePerson function from People class to update the GUI 
		everytime a person is removed.
		"""
		super(PeopleWindow, self).removePerson(index)
		self._peopleList -= index

	def __addPersonBtnAction(self):
		"""
		Add person button event. 
		"""
		# A new instance of the PersonWindow is opened and shown to the user.
		win = PersonWindow() 
		win.parent = self
		win.show()

	def __rmPersonBtnAction(self):
		"""
		Remove person button event
		"""
		self.removePerson( self._peopleList.selected_row_index ) 
	
#Execute the application
if __name__ == "__main__":	 pyforms.start_app( PeopleWindow )
```

The application will look like:

![People applications](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/docs/imgs/getting-started-5.png?raw=true "Screen")


## **EmptyWidget Control**
***************************

Instead of opening a new window everytime we want to add a new Person, we will change the Application to open the PersonWindow inside the PeopleWindow. For this we will use the ControlEmptyWidget.

```python
from pyforms.Controls		import ControlEmptyWidget
...

	def __init__(self):
		...
		self._panel	= ControlEmptyWidget()

	def __addPersonBtnAction(self):
		"""
		Add person button event. 
		"""
		# A new instance of the PersonWindow is opened and shown to the user.
		win = PersonWindow() 
		win.parent = self
		self._panel.value = win

...

```

## **DockWidget Control**
***************************

A DockWidget works like the EmptyWidget but can be detached or moved around the sides of the main Window.

```python
from pyforms.Controls		import ControlDockWidget
...

	def __init__(self):
		...
		self._panel	= ControlDockWidget()

...

```

![People applications](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/docs/imgs/getting-started-6.png?raw=true "Screen")

![People applications](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/docs/imgs/getting-started-7.png?raw=true "Screen")
