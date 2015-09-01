# Controls

Controls implements UI interfaces for the user to interact with the applications.  
A BaseWidget is formed by a set of forms.

Bellow we can find the description of all the Controls implemented in the PyForms library.

## ControlBase
***************************

All the Controls inherit from this Control, therefore you can find its functions and properties in all the other controls listed bellow.

### Constructer
***************************

#### \_\_init\_\_(label='', defaultValue='', helptext='')

Control constructer.  
**label** - Control label.  
**defaultValue** - Initial value of the control.  
**helptext** - Text shown when the mouse is over the control.

### Functions
***************************

#### initForm()

Load the control UI and initiate all the events.
 	
#### load(data)

Function used to load the value of the control.  
**data** - Contains a dictionary with the required information to load the control.
 	
#### save(data)

Save a value of the control to a dictionary variable.  
**data** - Dictionary where the control value should be saved.
 	
#### show()

Show the control
 	
#### hide()

Hide the control
 	
#### addPopupMenuOption(label, functionAction=None, key=None)

Add an option to the Control popup menu
 	
#### addPopupSubMenuOption(label, options, keys={})

Add submenu options to the Control popup menu
 	
	

### Events
***************************

#### changed() 

Function called when ever the Control value is changed
 	
#### aboutToShowContextMenuEvent()

Function called before open the Control popup menu
 

### Properties
***************************

#### value

This property return and set what the control should manage or store.
 	
#### name

This property return and set the name of the control
 	
#### label

Label of the control, if applies
 	
#### form

Returns the Widget of the control.
 	
#### parent

Returns or set the parent basewidget where the Control is
 	
#### help

Return and set the tip box of the control

#### enabled

Returns and set the control to enable or disable state.



## ControlBoundingSlider
***************************

### Constructer
***************************

#### \_\_init\_\_(label="", defaultValue=[20,40], min=0, max=100, horizontal=False, **kwargs) 

**defaultValue** - The default value is a list containing in the first element the lower value and in the second element the upper value.
**min** - Defines the minimum value that can be selected.
**max** - Defines the maximum value that can be selected.
**horizontal** - Flag indicating if the Bounding slider should be draw horizontally or vertically.

### Properties
*************************** 	

#### value

Gets and sets the value of the Control. This value is a list containing in the first element the lower value and in the second element the upper value.

#### min

Gets and sets the the minimum value that can be selected in the bounding slider.
 	
#### max

Gets and sets the the maximum value that can be selected in the bounding slider.

## ControlButton
***************************

### Constructer
***************************

#### \_\_init\_\_(label='', defaultValue='', checkable=False)

**checkable** - Flag indicating if the button is checkable or not.
 	 	
### Functions
***************************

#### load(data)

Because the value of this Control is a function, nothing is loaded
 	
#### save(data)

Because the value of this Control is a function, nothing is saved

#### click(self)

This function simulates a click in the button.

### Properties
***************************

 	
#### value

The value should be a pointer to function, that will be called everytime the button is pressed.

#### checked

In case the button was initiated with the flag checkable=True, it will get and set the checked state of the button.


## ControlCheckBoxList
***************************

## ControlCheckBox
***************************

## ControlCombo
***************************

## ControlDir
***************************

## ControlDockWidget
***************************

## ControlEmptyWidget
***************************

## ControlFile
***************************

## ControlFilesTree
***************************

## ControlHidden
***************************

## ControlImage
***************************

## ControlLabel
***************************

## ControlList
***************************

## ControlMdiArea
***************************

## ControlNumber
***************************

## ControlOpenGL
***************************

## ControlProgress
***************************

## ControlSlider
***************************

## ControlTextArea
***************************

## ControlText
***************************

## ControlToolBox

## ControlTree

## ControlTreeView

## ControlVisVis

## ControlVisVisVolume