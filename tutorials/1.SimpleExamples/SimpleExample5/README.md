# Simple example 5

This example shows you how to define the application Main menu using the BaseWidget.mainmenu property.
		
```python
self.mainmenu = [
		{ 'File': [
				{'Open': self.__dummyEvent},
				'-',
				{'Save': self.__dummyEvent},
				{'Save as': self.__dummyEvent}
			]
		},
		{ 'Edit': [
				{'Copy': self.__dummyEvent},
				{'Past': self.__dummyEvent}
			]
		}
	]
```


![Simple example 5](screenshot.png?raw=true "Screen")