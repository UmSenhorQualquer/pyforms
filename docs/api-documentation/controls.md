# Controls

A form Control is a UI interface for the user to interact with the application.  

Bellow we can find the description of all the Controls implemented in the PyForms library.



## ControlBase
***************************

All the Controls inherit from this Control, therefore you can find its functions and properties in all the other controls listed below.

### **Constructer**
***************************

#### \_\_init\_\_(label='', defaultvalue='', helptext='')  

**label** - Control label.  
**defaultvalue** - Initial value of the control.  
**helptext** - Text shown when the mouse is over the control.


### **Functions**
***************************

#### init_form()  

Load the control UI and initiate all the events.
 	
#### load_form(data, path=None)  
Loads the value of the control.  
**data** - It is a dictionary with the required information to load the control.
**path** - Optional parameter that can be used to save the data.
 	
#### save_form(data, path=None)  

Save a value of the control to a dictionary.  
**data** - Dictionary where the control value should be saved.
**path** - Optional parameter that can be used to load the data.
 	
#### show()  

Show the control.
 	
#### hide()  

Hide the control.
 	
#### add_popup_menu_option(label, function_action=None, key=None)  

Add an option to the Control popup menu.
 	
#### add_popup_submenu_option(label, options, keys={})  

Add submenu options to the Control popup menu.
 	
	

### **Events**
***************************
 	
#### about_to_show_contextmenu_event()  

Function called before the Control popup menu is opened.

#### changed_event()  

Function called when ever the Control value is changed.


### **Properties**
***************************

#### enabled  
Returns or set if the control is enable or disable.
 	
#### form  
Returns the QWidget of the control.
 	
#### help  
Returns or set the tip box of the control.
 	
#### label  
Returns or sets the label of the control.
 	
#### name  
This property returns or set the name of the control.
 	
#### parent  
Returns or set the parent basewidget where the Control is.

#### visible
Set and return the control visibility.

#### value  
This property returns or set what the control should manage or store.









## ControlBoundingSlider
***************************

![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlBoundingSlider.png?raw=true "Screen")

### **Constructer**
***************************

#### \_\_init\_\_(label="", defaultvalue=[20,40], min=0, max=100, horizontal=False) 

**defaultvalue** - The default value is a list containing in the first element the lower value and in the second element the upper value.  
**min** - Defines the minimum value that can be selected.  
**max** - Defines the maximum value that can be selected.  
**horizontal** - Flag indicating if the Bounding slider should be draw horizontally or vertically.  

### **Properties**
*************************** 	

#### value

Gets and sets the value of the Control. This value is a list containing in the first element the lower value and in the second element the upper value.

#### min

Gets and sets the the minimum value that can be selected in the bounding slider.
 	
#### max

Gets and sets the the maximum value that can be selected in the bounding slider.

#### convert_2_int

If True the control works only with Integer values. If False the control will return Float values.





## ControlButton
***************************

![Web ready](https://img.shields.io/badge/WEB-READY-green.svg "Screen")
![Terminal ready](https://img.shields.io/badge/TERMINAL-READY-green.svg "Screen")
![Docs updated](https://img.shields.io/badge/UNITARY%20TESTS-OK-green.svg "Screen")

![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlButton.png?raw=true "Screen")

### **Constructer**
***************************

#### \_\_init\_\_(label='', checkable=False, helptext='')

**checkable** - Flag indicating if the button is checkable or not.
 	 	

### **Functions**
***************************

#### load_form(data, path=None)

Because the value of this Control is a function, nothing is loaded
 	
#### save_form(data, path=None)

Because the value of this Control is a function, nothing is saved

#### click()

This function simulates a click of the button.

### **Properties**
***************************

#### checked

In case the button was initiated with the flag checkable=True, it will get and set the checked state of the button.

#### icon

Return or set the button icon. The value should be a path to the icon or a QtGui.QIcon object.

#### value

The value should be a pointer to function, that will be called everytime the button is pressed.






## ControlCheckBox
***************************

![Web ready](https://img.shields.io/badge/WEB-READY-green.svg "Screen")
![Terminal ready](https://img.shields.io/badge/TERMINAL-READY-green.svg "Screen")
![Docs updated](https://img.shields.io/badge/UNITARY%20TESTS-OK-green.svg "Screen")


![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlCheckBox.png?raw=true "Screen")

### **Properties**
***************************

#### value

Gets and sets a boolean indicating the state of the checkbox.








## ControlCheckBoxList
***************************

![Docs updated](https://img.shields.io/badge/UNITARY%20TESTS-OK-green.svg "Screen")

![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlCheckBoxList.png?raw=true "Screen")

### **Functions**
***************************
 	
#### \_\_add\_\_(val)

Add more elements to the list.
Usage:  
```python
controlVar += ('Element', True)  
```  
or  
```python
controlVar += 'Element'
```  

#### clear()

Clear all the elements from the list.

### **Events**
***************************
 	
#### selection_changed_event()  

Function called when the selection changed.

### **Properties**
***************************
 	
#### count

Return how many elements the list have.
 	
#### checked_indexes

Returns the Elements with which have the checkboxes checked.

#### items

Returns a list of tuples with the format [(element, check boolean flag)]

#### selected_row_index

Returns the selected row index.

#### value

It gets and sets all the List values. This property receives a list where each element is a Row in the list.

```python
controlVar.value = [('item1',True), ('item2',False), 'item3']
```







## ControlCodeEditor
***************************
![Docs updated](https://img.shields.io/badge/UNITARY%20TESTS-OK-green.svg "Screen")

![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlCodeEditor.png?raw=true "Screen")

### **Events**
***************************

### key_pressed_event(event)

Function called when a key is pressed.

**event** - Qt event variable.  

### **Properties**
***************************

#### changed

Returns and sets the pointer to the function that is called when the button save is pressed.

#### lexer

Returns and sets the Scintilla lexer. By default the lexer is the QsciLexerPython.

#### value

Returns and sets the code text.









## ControlCombo
***************************

![Web ready](https://img.shields.io/badge/WEB-READY-green.svg "Screen")
![Terminal ready](https://img.shields.io/badge/TERMINAL-READY-green.svg "Screen")
![Docs updated](https://img.shields.io/badge/UNITARY%20TESTS-OK-green.svg "Screen")

![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlCombo.png?raw=true "Screen")

### **Functions**
***************************
 	
#### add_item(text, value=None)

Add an item to the ComboBox. Items may have a value associated to it.

```python
controlVar.add_item('Portugal', 'pt')
controlVar.add_item('Angola', 'ao')
controlVar.add_item('Moçambique', 'mz')
controlVar.add_item('Brazil')
controlVar.add_item('Cabo Verde')
``` 

#### clear()

Clear all the items of the ComboBox.

#### count()

Return the number o items in the combobox.

#### get_item_index_by_name(item_name)

Search the index of an item by the name.

#### \_\_add\_\_(value)

The same of add_item function.

```python
controlVar += ('Portugal', 'pt')
controlVar += ('Angola', 'ao')
controlVar += ('Moçambique', 'mz')
controlVar += 'Brazil'
controlVar += 'Cabo Verde'
``` 

### **Events**
***************************

#### activated_event(index) 

Called when the user select an item in the combobox.
**index** - Activated item's index.

#### current_index_changed_event(index)

Called when the current combobox index is changed.
**index** - current selected index.

#### edittext_changed_event(text)

Called when the text is changed.
**text** - changed text.

#### highlighted_event(index)

Called when the user passes with the mouse over an item in the combobox.
**index** - highlighted item's index.

### **Properties**
***************************

#### current_index

Returns and sets the selected index.

#### items

Returns all the items of the combobox.
 	
#### value

It returns the selected value of the combo box.
 	
#### text

Gets and set the current selected item text.








## ControlDir
***************************

![Web ready](https://img.shields.io/badge/WEB-READY-green.svg "Screen")
![Terminal ready](https://img.shields.io/badge/TERMINAL-READY-green.svg "Screen")
![Docs updated](https://img.shields.io/badge/UNITARY%20TESTS-OK-green.svg "Screen")

![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlDir.png?raw=true "Screen")

This control is used to select a directory.







## ControlDockWidget
***************************

![Docs updated](https://img.shields.io/badge/UNITARY%20TESTS-OK-green.svg "Screen")

![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlDockWidget.png?raw=true "Screen")

This control is used to create DockWidget.

### **Constructer**
***************************

#### \_\_init\_\_(label='', default=None, side='left')

**side** - Side where the dock widget should be initiated. It can assumes the values: left, right, top or bottom.







## ControlEmptyWidget
***************************

![Docs updated](https://img.shields.io/badge/UNITARY%20TESTS-OK-green.svg "Screen")

This Control may be used to display a BaseWidget or another Control inside.

### **Constructer**
***************************

#### \_\_init\_\_(label='') 

The constructer receives only a label.

### **Properties**
***************************

#### value

It may receive an element, or a list of elements from the types BaseWidget or BaseControl.







## ControlEventTimeline
***************************

![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlEventTimeline.png?raw=true "Screen")


### **Constructor**
***************************

#### \_\_init\_\_(label="", defaultValue=0, min=0, max=100, **kwargs)

### **Functions**
***************************
 	 	
#### getExportFilename()
 	
#### addRow(values)
 	
#### addPeriod(value, track=0, color=None)	source code

### **Events**
***************************

#### playVideoEvent()

#### fpsChanged()

#### pointerChanged()
 	
### **Properties**
***************************

#### value

#### max
 	
#### mouseOverLine

 	
 	



## ControlFile
***************************

![Web ready](https://img.shields.io/badge/WEB-READY-green.svg "Screen")
![Terminal ready](https://img.shields.io/badge/TERMINAL-READY-green.svg "Screen")
![Docs updated](https://img.shields.io/badge/UNITARY%20TESTS-OK-green.svg "Screen")

![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlFile.png?raw=true "Screen")

The control may be used to select a file.

### **Properties**
***************************

#### value

Gets and sets a file path.







## ControlFilesTree
***************************

![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlFilesTree.png?raw=true "Screen")

Show the directory files in a tree view

⋅⋅⋅Note Is not fully developed yet.⋅⋅

### **Properties**
***************************

#### value

Gets and sets a directory path.








## ControlImage
***************************

![Web ready](https://img.shields.io/badge/WEB-READY-green.svg "Screen")
![Terminal ready](https://img.shields.io/badge/TERMINAL-READY-green.svg "Screen")
![Docs updated](https://img.shields.io/badge/UNITARY%20TESTS-OK-green.svg "Screen")

![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlImage.png?raw=true "Screen")


Displays an image or a list of images.

	

### **Functions**
***************************

#### repaint()

Redraw the image or set of images

### **Properties**
***************************
 	
#### value

This property receives an image path, a numpy image or a list of numpy images.  

Usage:  
```python
controlVar.value = 'lena_color.png'
```  
or  
```python
controlVar.value = cv2.imread('lena_color.png', 1)
```  
or  
```python
img1 = cv2.imread('lena_color.png', 1)
img2 = cv2.imread('lena_color.png', 1)
controlVar.value = [img1, img2]
```  

**Note:** the value can only be set outside the constructor and the initForm function.


## ControlLabel
***************************

![Docs updated](https://img.shields.io/badge/UNITARY%20TESTS-OK-green.svg "Screen")

![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlLabel.png?raw=true "Screen")


Displays a text.








## ControlList
***************************

![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlList.png?raw=true "Screen")


Displays a list of values.

### **Constructer**
***************************
 	
#### \_\_init\_\_(label="", defaultValue="", plusFunction=None, minusFunction=None)

**defaultValue** - 
**plusFunction** - 
**minusFunction** - 


### **Functions**
***************************

#### clear()

Clear all the values from the list.
 	
#### \_\_add\_\_(values)	source code

Inserts a new row with the list of values.
 	
#### \_\_sub\_\_(index)

Removes the row with the index.

#### setValue(column, row, value)

Set the value of a specific cell.
 	
#### getValue(column, row)	source code

Get the value of a specific cell.

### **Events**
***************************
 	
#### dataChangedEvent(row, col, item)  
 	
#### tableWidgetCellChanged(nextRow, nextCol, previousRow, previousCol) 
 	
#### tableWidgetItemChanged(current, previous) 
 	
#### tableWidgetItemSelectionChanged() 
 	
#### itemSelectionChanged() 
 	
#### currentCellChanged(nextRow, nextCol, previousRow, previousCol) 
 	
#### currentItemChanged(current, previous)

### **Properties**
***************************

#### horizontalHeaders

Get and set the horizontal headers in the table list.
 	
#### selectEntireRow

Accepts a boolean indicating if should allow only the selection of the entire row or not.
 	
#### count

Return the number of rows.
 	
#### value

Get and set the list values.
 	
#### mouseSelectedRowsIndexes

Return the selected indexes.
 	
#### mouseSelectedRowIndex

Return the selected index.
 	
#### iconSize

Gets and sets the icon size.









## ControlMdiArea
***************************

![Docs updated](https://img.shields.io/badge/UNITARY%20TESTS-OK-green.svg "Screen")

![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlMdiArea.png?raw=true "Screen")

### **Constructor**
***************************
	
#### \_\_init\_\_(label='')

The constructer receives only a label.


### **Functions**
***************************

#### \_\_add\_\_(other)

Usage:  
```python
controlVar += baseWidget
```  
or  
```python
controlVar += [baseWidget1 , baseWidget2]
```  

### **Properties**
***************************

#### showCloseButton

Boolean flag, indicating if should show the subwindows close button or not.
 	
#### value

Sets a BaseWidget or a list of BaseWidgets representing the windows.








## ControlNumber
***************************

![Docs updated](https://img.shields.io/badge/UNITARY%20TESTS-OK-green.svg "Screen")

![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlNumber.png?raw=true "Screen")

### **Constructor**
***************************

#### \_\_init\_\_(label="", defaultValue=0, min=0, max=100)

**min** - Defines the minimum value that can be selected.  
**max** - Defines the maximum value that can be selected. 

### **Properties**
***************************

#### min

Defines the minimum value that can be selected.  
 	
#### max

Defines the maximum value that can be selected.  

#### value

Returns the selected number.








## ControlOpenGL
***************************

![Docs updated](https://img.shields.io/badge/UNITARY%20TESTS-OK-green.svg "Screen")

![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlOpenGL.png?raw=true "Screen")


### **Functions**
***************************

#### repaint()

Refresh the GL scene.
 	
#### resetZoomAndRotation()

Reset all the zoom and scene rotations.

### **Properties**
***************************
 	
#### value

Gets and sets a GL scene.
 	
#### width

Gets the GL window width
 	
#### height

Gets the GL window height







## ControlPlayer
***************************

![Web ready](https://img.shields.io/badge/WEB-READY-green.svg "Screen")
![Terminal ready](https://img.shields.io/badge/TERMINAL-READY-green.svg "Screen")
![Docs updated](https://img.shields.io/badge/UNITARY%20TESTS-OK-green.svg "Screen")

![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlPlayer.png?raw=true "Screen")

### **Functions**
***************************

#### pausePlay()

Toggle video play.
 	
#### refresh()	

Refresh the last painted frame.
 	
#### isPlaying()

Returns a boolean indicating if the video is playing.

### **Events**
***************************

#### processFrame(frame)

Function called before the frame is rendered.
 	
### **Properties**
***************************

#### onDoubleClick

Gets and sets the function called on double click event.  
The funtion receives the next parameters: onDoubleClick(event, x, y)
 	
#### onClick

Gets and sets the function called on click event.  
The funtion receives the next parameters: onClick(event, x, y)
 	
#### onDrag

Gets and sets the function called during a drag event.  
The funtion receives the next parameters: onDrag(startPoint, endPoint)
 	
#### onEndDrag

Gets and sets the function called when a drag event ends.  
The funtion receives the next parameters: onEndDrag(startPoint, endPoint)

#### value

When not None, it returns a cv2.VideoCapture object.  
It may receives a video file path, or a cv2.VideoCapture object.

Usage:  
```python
controlVar.value = '~/home/ricardo/video.avi'
```  
or  
```python
controlVar.value = cv2.VideoCapture('~/home/ricardo/video.avi')
```
 	
#### startFrame

Gets and sets the first frame.

#### endFrame

Gets and sets the last frame.
 	
#### video_index

Returns the current frame index.
 	
#### max

Returns the total number of frames of a video.
 	
#### image

Returns and sets the image beeing rendered.
 	
#### fps

Returns and sets the video FPS.
 	
#### helpText

Return and set the help text that should be rendered in the video.




## ControlProgress
***************************

![Terminal ready](https://img.shields.io/badge/TERMINAL-READY-green.svg "Screen")
![Docs updated](https://img.shields.io/badge/UNITARY%20TESTS-OK-green.svg "Screen")

![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlProgress.png?raw=true "Screen")


### **Constructor**
***************************

#### \_\_init\_\_(label="%p%", defaultValue=0, min=0, max=100)

**label** - This is the text that will be shown in the ProgressBar.
**min** - Defines the minimum value that can be selected.  
**max** - Defines the maximum value that can be selected. 


### **Properties**
***************************

#### min

Defines the minimum value that can be selected.  
 	
#### max

Defines the maximum value that can be selected.  
 	
#### value

Current position.


## ControlSlider
***************************

![Web ready](https://img.shields.io/badge/WEB-READY-green.svg "Screen")
![Terminal ready](https://img.shields.io/badge/TERMINAL-READY-green.svg "Screen")
![Docs updated](https://img.shields.io/badge/UNITARY%20TESTS-OK-green.svg "Screen")

![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlSlider.png?raw=true "Screen")


### **Constructor**
***************************

#### \_\_init\_\_(label="", defaultValue=0, min=0, max=100)

**min** - Defines the minimum value that can be selected.  
**max** - Defines the maximum value that can be selected. 

### **Properties**
***************************

#### min

Defines the minimum value that can be selected.  
 	
#### max

Defines the maximum value that can be selected.  







## ControlText
***************************

![Web ready](https://img.shields.io/badge/WEB-READY-green.svg "Screen")
![Terminal ready](https://img.shields.io/badge/TERMINAL-READY-green.svg "Screen")
![Docs updated](https://img.shields.io/badge/UNITARY%20TESTS-OK-green.svg "Screen")

![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlText.png?raw=true "Screen")


### **Events**
***************************

#### finishEditing() 

Event called when the user ends the control edition.





## ControlTextArea
***************************

![Docs updated](https://img.shields.io/badge/UNITARY%20TESTS-OK-green.svg "Screen")

![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlTextArea.png?raw=true "Screen")



## ControlToolBox
***************************

![Docs updated](https://img.shields.io/badge/UNITARY%20TESTS-OK-green.svg "Screen")

![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlToolBox.png?raw=true "Screen")

### **Properties**
***************************

#### value

It returns and receives a list of BaseWidgets.




## ControlTree
***************************

![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlTree.png?raw=true "Screen")


### iconsize


## ControlTreeView
***************************

![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlTreeView.png?raw=true "Screen")






## ControlVisVis
***************************

![Docs updated](https://img.shields.io/badge/UNITARY%20TESTS-OK-green.svg "Screen")


![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlVisVis.png?raw=true "Screen")


### **Functions**
***************************

#### refresh()

Repaint the points
 	
### **Properties**
***************************

#### value

Gets and sets a list of 2D or 3D points to display.

#### legend

Set the graph legend

#### showGrid

(True or False). Show a grid in the graph

#### title

Set the graph title

#### xlabel

Set the x axis label.

#### ylabel

Set the y axis label.

#### zlabel

Set the z axis label.



## ControlVisVisVolume
***************************

![Docs updated](https://img.shields.io/badge/UNITARY%20TESTS-OK-green.svg "Screen")


![Control image](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/tutorials/Controls4Docs/ControlVisVisVolume.png?raw=true "Screen")


### **Functions**
***************************

#### refresh()

Repaint the image.
 	
### **Properties**
***************************

#### value

Gets and sets an numpy array image with volume.

#### colorMap

Gets and sets the color map to display.  
It can receives the next values: CM_BONE, CM_COOL, CM_COPPER, CM_GRAY, CM_HOT, CM_HSV, CM_JET, CM_PINK, CM_AUTUMN, CM_SPRING, CM_SUMMER, CM_WINTER.  
Check out [VisVis documentation](https://code.google.com/p/visvis/wiki/Colormaps).