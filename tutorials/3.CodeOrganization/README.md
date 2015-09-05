# Code organization example

On this example it will be shown how to modularize your code, in a in MVC way.

## 1. Implement the model.

Person.py
```python
class Person(object):
	...
```

People.py
```python
class People(object):
	...
```

## 2. Implement the GUI to manage ther Person model.

PersonWindow.py
```python
class PersonWindow(Person, BaseWidget):
	...
```

**Note**: *Test the window by executing the file.*

## 3. Implement the GUI to manage ther People model.

PeopleWindow.py
```python
class PeopleWindow(People, BaseWidget):
	...
```

## 4. Implement the module that will give the Main Menu and the options save and load to the application.

AddMenuFuntionality.py
```python
class AddMenuFuntionality(object):
	...
```

## 5. Add the AddMenuFuntionality module to the PeopleWindow application, and the new functionalities will be added.

PeopleWindow.py
```python
class PeopleWindow(AddMenuFuntionality, People, BaseWidget):
	...
```
