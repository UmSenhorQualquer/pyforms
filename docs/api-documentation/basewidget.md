# BaseWidget

The BaseWidget is used to create a set of forms Controls. It can works as a main window or a panel that can be included in others BaseWidgets.

This class inherit from the Qt QWidget.

Usage example:
```python
class SimpleExample(BaseWidget):
	
	def __init__(self):
		super(SimpleExample,self).__init__('Simple example')

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
```

## **Constructor**
***************************

### \_\_init\_\_(title='Untitled')

The constructer receives the title of the window.

## **Important variables**
***************************

### _formset

This variable is used to define the organization of the forms Controls in the BaseWidget.  
When not defined it BaseWidget will assume generate this variable automatically.

Example:
```python
self._formset = [
	'info:Some title',
	'h1:Some title',
	'h2:Some title',
	'h3:Some title',
	'h4:Some title',
	'h5:Some title',
	(' ','free text', ' '),
	('_video', '_arenas', '_run'), 
	{
		"Player": ['_threshold', "_player", "=", "_results", "_query"], 
		"Background image": [(' ', '_selectBackground', '_paintBackground'), '_image']
	}, 
	"_progress"
] 
```

**Tuple**: Displays the controls horizontally.  
**List**: Displays the controls vertically.  
**Dict**: Displays the controls in a tab widget.  
**'||'**: Split the controls horizontally.  
**'='**: Split the controls vertically.  
**' '**: It creates an empty space. It can be used to align Controls to one expecific side.  
**info:, h1:, h2:, h3:, h4:, h5:**: Is used to write some text in the interface with diferent sizes.  
**free text** - It is possible also to write some free text.
 	

## **Functions**
***************************
 	
### initForm() 

Initialize the QWidget and its events with the set of form Controls.
 	
### generateTabs(formsetDict)

Used when a dictionary is present in the the BaseWidget._formset variable.  
Returns a QTabWidget with the forms Controls organization described in the parameter formsetDict.
Example:
```python
{
	"a:Player": ['_threshold', "_player", "=", "_results", "_query"], 
	"b:Background image": [(' ', '_selectBackground', '_paintBackground'), '_image']
}
```

**Note:** Because a Python dictionary does not support order, we may use the format '[some characters]:[Tab name]' to order tabs. The generateTabs function will use the component [some characters] to order alfabetically the tabs.  
Only the component [Tab name] will be shown in the tab.

	
### generatePanel(formset) 

Used to construct a panel with forms Controls organization described in the BaseWidget._formset variable.  
Returns a QWidget with the forms Controls organization described in the parameter formset.

**formset** - variable describing the organization of the forms Controls in the BaseWidget.  
Example:
```python
[
	'info:Some title',
	'h1:Some title',
	'h2:Some title',
	'h3:Some title',
	'h4:Some title',
	'h5:Some title',
	(' ','free text', ' '),
	('_video', '_arenas', '_run'), 
	{
		"Player": ['_threshold', "_player", "=", "_results", "_query"], 
		"Background image": [(' ', '_selectBackground', '_paintBackground'), '_image']
	}, 
	"_progress"
] 
```


### show()

Calls the initForm() function and shows the BaseWidget.

### saveWindow()

Open a Save file dialog, and saves the Window Controls data to the selected file in the JSON format.

### save(data)

Receives a dictionary, and stores all the Window Controls data on it.

**data** - dict where the data will be stored.

### loadWindow()

Opens a Open file dialog, and calls the function loadWindowData() 

### loadWindowData(filename)

Loads the json data from a file and calls the function load()
 	
### load(data)
 	
Load the Window Controls data from a dictionary.

## **Properties**
***************************

### formControls

Returns a dictionary of all Controls in the Window.
 	
### form

Return QWidget representing the Window and the Controls. 
 	
### title

Get and sets the Window title.
 	
### mainmenu

Get and sets the Application main menu.

Example:

```python
self.mainmenu = [
		{ 'File': [
				{'Save as': self.saveWindow},
				{'Open as': self.loadWindow},
				'-',
				{'Exit': self.__exit},
			]
		}
	]
``` 

**'-'**: Use the minus sign to create a split bar in the menu.
