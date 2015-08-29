# BaseWidget

## __init__(title)
 	
## initForm() 

Generate the module Form
 	
## generateTabs(formsetDict) 

Generate QTabWidget for the module form
 	
## generatePanel(formset) 

Generate a panel for the module form with all the controls formset format example: [('_video', '_arenas', '_run'), {"Player":['_threshold', "_player", "=", "_results", "_query"], "Background image":[(' ', '_selectBackground', '_paintBackground'), '_image']}, "_progress"] tuple: will display the controls in the same horizontal line list: will display the controls in the same vertical line dict: will display the controls in a tab widget '||': will plit the controls in a horizontal line '=': will plit the controls in a vertical line
 	
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