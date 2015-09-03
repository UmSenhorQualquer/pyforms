# Base widget


## \_\_init\_\_(title)
 	
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
 	
## formControls()

Return all the form controls from the the module
 	
## form
 	
## title
 	
## mainmenu
 	
## docks
 	
## save(data)
 	
## saveWindow()
 	
## loadWindowData(filename)
 	
## load(data)
 	
## loadWindow()