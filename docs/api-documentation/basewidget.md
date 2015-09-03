# Base widget


## \_\_init\_\_(title)

### **Functions**
***************************
 	
## initForm() 

Generate the module Form
 	
## generateTabs(formsetDict) 

Generate QTabWidget for the module form
 	
## generatePanel(formset) 

Generate a panel for the module form with all the controls formset format example:

```python
[
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
 	
## show()

OTModuleProjectItem.show reimplementation

## saveWindow()

Open a Save file dialog, and saves the Window Controls data to the selected file in the JSON format.

## save(data)

Receives a dictionary, and stores all the Window Controls data on it.
 	
**data** - dict where the data will be stored.

## loadWindow()

Opens a Open file dialog, and calls the function loadWindowData() 

## loadWindowData(filename)

Loads the json data from a file and calls the function load()
 	
## load(data)
 	
Load the Window Controls data from a dictionary.

### **Properties**
***************************

## formControls

Returns a dictionary of all Controls in the Window.
 	
## form

Return QWidget representing the Window and the Controls. 
 	
## title

Get and sets the Window title.
 	
## mainmenu

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
