# Simple example 4

On this example we show you how to organize the forms side by side using the variable "self._formset".
		
```python
	#Add the name of the forms variables inside tuples organize these forms side by side
	self._formset = [ ('_firstname','_middlename', '_lastname'), 
			'_fullname', (' ' ,'_button', ' '), ' ']
```

Note:
- Forms vertically organized - use list.
- Forms horizontally organized - use a tuple.

![Simple example 3](screenshot.png?raw=true "Screen")