# Style and layout with CSS

*This page was based on the examples available at the github folder: [Tutorial - Code Organization](https://github.com/UmSenhorQualquer/pyforms/tree/master/tutorials/3.CodeOrganization)*


PyForms takes advantage of the Qt framework to split the layout from the implementation of the functionalities.
It is possible to configure the settings to import a stylesheet file which will change the application layout.

To do it, you need to add to your settings file the variable PYFORMS_STYLESHEET with the path to the css file you want to use:

```python
PYFORMS_STYLESHEET = 'style.css'
```

You may would like also to adapt the layout for a specific operating system. 

The next variables will allow to do this. You can complement the style configured in PYFORMS_STYLESHEET with a stylesheet for a specific operating system.

```python
PYFORMS_STYLESHEET_DARWIN = 'style_darwin.css'
PYFORMS_STYLESHEET_LINUX = 'style_linux.css'
PYFORMS_STYLESHEET_WINDOWS = 'style_window.css'
```

**Check the example:** style.css
```css
QMainWindow{
	background-color: white;
}

QLabel{
	min-width: 110px;
}

QLineEdit{
	min-width: 200px;
	border: 1px solid #CCC;
	height: 30px;
	padding-left: 10px;
}

QPushButton{
	background: #3498db;
	color: #ffffff;
	padding: 10px 20px 10px 20px;

    border-radius: 6px;
}

QPushButton:hover {
  background: #3cb0fd;
}

/*Use the # and the name of the variable to access to a specific the Control*/
#_firstnameField QLineEdit{
	color:red;
}
```

![People applications](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/docs/imgs/getting-started-8.png?raw=true "Screen")
