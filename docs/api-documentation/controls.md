# Controls

Controls implements UI interfaces for the user to interact with the applications.
A BaseWidget is formed by a set of forms.

Bellow we can find the description of all the Controls implemented in the PyForms library.

## ControlBase
***************************

All the Controls inherit from this Control, therefore you can find its functions and properties in all the other controls listed bellow.

### Functions

#### __init__(label='', defaultValue='', helptext='')

Control constructer.
*label* - Control label.
*defaultValue* - Initial value of the control.
*helptext* - Text shown when the mouse is over the control.

#### initForm()

Load the control UI and initiate all the events.
 	
#### load(data)

Function used to load the value of the control.
*data* - Contains a dictionary with the required information to load the control.
 	
#### save(data)

Save a value of the control to a dictionary variable.
*data* - Dictionary where the control value should be saved.
 	
#### show()

Show the control
 	
#### hide()

Hide the control
 	
#### addPopupMenuOption(label, functionAction=None, key=None)

Add an option to the Control popup menu
 	
#### addPopupSubMenuOption(label, options, keys={})

Add submenu options to the Control popup menu
 	
#### changed() 

Function called when ever the Control value is changed
 	
#### aboutToShowContextMenuEvent()

Function called before open the Control popup menu
 	

### Properties 	

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

#### enabled





## ControlBoundingSlider
***************************

## ControlButton
***************************

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