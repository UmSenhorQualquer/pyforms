# Simple example 2

In the previous example the forms were not properly ordered. 
On this example we show you how to organize the forms using the variable "self._formset".
		
```python
	#Add this line to the constructor and you will be able to organize the forms.
	self._formset = ['_firstname','_middlename','_lastname', '_fullname', '_button', ' ']
```



**Notes:**
You can you use the value ' ' in the self._formset to force the Windows Form to give a blank space on the window.




![Simple example 2](screenshot.png?raw=true "Screen")