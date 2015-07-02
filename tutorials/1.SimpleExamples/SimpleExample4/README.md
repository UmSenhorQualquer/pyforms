# Simple example 4

On this example we show you how to define tabs using dictionaries in the variable "self._formset".
		
```python
	#Use dictionaries for tabs
	self._formset = [ {
					  	'Tab1':['_firstname','||','_middlename','||','_lastname'], 
						'Tab2': ['_fullname']
					  },
					  '=',(' ','_button', ' ') ]
```



**Notes:**
Take a look between the First name, Middle name, and Last name controls, you will find a splitter which you can move. 
The same between the Tabs and the Button.
- Use the sign '=' for a vertical splitter
- Use the signs '||' for a horizontal splitter



![Simple example 4](screenshot.png?raw=true "Screen")