# Controls

## ControlBase

### Functions

#### __init__(label='', defaultValue='', helptext='')

#### initForm()

Load Control and initiate the events
 	
#### load(self, data)

Load a value from the dict variable
 	
#### save(self, data)

Save a value to dict variable
 	
#### show(self)

Show the control
 	
#### hide(self)

Hide the control
 	
#### addPopupMenuOption(self, label, functionAction=None, key=None)

Add an option to the Control popup menu
 	
#### addPopupSubMenuOption(self, label, options, keys={})

Add submenu options to the Control popup menu
 	
#### changed(self) 

Function called when ever the Control value is changed
 	
#### aboutToShowContextMenuEvent(self)

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

### enabled

source code



## ControlBoundingSlider

## ControlButton

## ControlCheckBoxList

## ControlCheckBox

## ControlCombo

## ControlDir

## ControlDockWidget

## ControlEmptyWidget

## ControlFile

## ControlFilesTree

## ControlHidden

## ControlImage

## ControlLabel

## ControlList

## ControlMdiArea

## ControlNumber

## ControlOpenGL

## ControlProgress

## ControlSlider

## ControlTextArea

## ControlText

## ControlToolBox

## ControlTree

## ControlTreeView

## ControlVisVis

## ControlVisVisVolume