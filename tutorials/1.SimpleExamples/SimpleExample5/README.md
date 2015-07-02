# Simple example 5

On this example we show you how to define the application Main menu using the AutoForm.mainmenu property.
		
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