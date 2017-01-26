# BaseWidget

The BaseWidget is used to organise a set of forms Controls. It can be used as a main window, or as a panel that can be included inside of others BaseWidgets.

This class inherit from the PyQt QFrame.

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
		self.formset = ['_firstname','_middlename','_lastname', '_fullname', '_button', ' ']
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

### \_\_init\_\_(title='Untitled', parent_win=None, win_flag=None)

**title** - Title of the window.
**parent_win** - Parent widget. If the win_flag is None and the parent parameters is set, then the flag_win will be QtCore.Qt.Dialog.
**win_flag** - Window type flag. Type of Qt.WindowType.

## **Functions**
***************************
 	
### init_form() 

Initialize the QFrame, the Controls and its events.

### show()

Calls the init_form() function and shows the BaseWidget.

### save_window()

Open a save file dialog, and saves the window's controls data into the selected file, in the JSON format.  

### load_window()

Opens a open file dialog, and calls the function load_form_filename().  

### load_form_filename(filename)

Load the window data from a filename.

**filename** - Path to the file to load.

### save_form(data, path=None)

Receives a dictionary, and stores all the BaseWidget's controls data on it.

**data** - Dictionary with where the of the BaseWidget and their child controls should be stored.
**path** - Path where the basewidget data should be stored.

### load_form(data, path=None)
 	
Load the Window Controls data from a dictionary.

**data** - Dictionary with the data of the BaseWidget and their child controls.
**path** - Path where the basewidget data should be loaded.

## **User interface functions**
***************************

You will probably never use these functions directly, but they are here so you can understand how the BaseWidgets layout is generated.
 	
### generate_tabs(formsetdict)

It is used to interpret a formset dictionary.  
It returns a QTabWidget with the BaseWidget's controls organized in the structure defined by the formsetdict variable.

**formsetdict** -Dictionary describing the organization of the returning QTabWidget.

Example:
```python
{
	"a:Player": ['_threshold', "_player", "=", "_results", "_query"], 
	"b:Background image": [(' ', '_selectBackground', '_paintBackground'), '_image']
}
```

**Note:** To sort the dictionary elements, we can use the format '[some characters]:[Tab name]' to order the tabs. The generate_tabs function will use the component [some characters] to order alphabetically the tabs.
Only the component [Tab name] will be shown in the tab title.

	
### generate_panel(formset) 

It is used to interpret a formset list.  
It returns a QWidget with the controls organized in the structure defined by the formset variable.

**formset** - variable describing the organization of the forms Controls in the QWidget.

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


## **Events**
***************************

### before_close_event()  

Event called before the window is closed.

## **Properties**
***************************

### form_has_loaded

Returns a boolean indicating if the form has called the init_form() function or not.

### formset

This property is used to define the organization of the controls in the BaseWidget.  
When is not defined, the BaseWidget will generate this property automatically.

Example:
```python
self.formset = [
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
 	

### controls

It returns a dictionary with all the controls in the BaseWidget.
 	
### form

It return the main QFrame of the BaseWidget. 
 	
### title

Get or sets the BaseWidget title.
 	
### mainmenu

Get or sets the Application main menu.

Example:

```python
self.mainmenu = [
		{ 'File': [
				{'Save as': self.save_window, 'icon': 'path-to-image.png'},
				{'Open as': self.load_window, 'icon': QtGui.QIcon('path-to-image.png')},
				'-',
				{'Exit': self.__exit},
			]
		}
	]
``` 

**'-'**: Use the minus sign to create a split bar in the menu.

### load_order

It defines the controls that should be saved or loaded by the functions save_form and load_form, and the order in which it should be done.

```python
self.load_order = ['_control1', '_control2']
``` 

### uid

Gets or sets a unique id of the window.

### visible

Gets or sets the window visibility.