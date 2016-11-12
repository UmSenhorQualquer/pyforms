# Simple example 2

In the previous example the forms were not properly ordered. 
This example shows you how to organize the forms using the variable "self.formset".
		
```python
	#Add this line to the constructor and you will be able to organize the forms.
	self.formset = ['_firstname','_middlename','_lastname', '_fullname', '_button', ' ']
```



**Notes:**
You can you use the value ' ' in the self.formset to force the Windows Form to give a blank space on the window.




![Simple example 2](screenshot.png?raw=true "Screen")