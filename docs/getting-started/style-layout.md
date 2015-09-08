# Style and layout with CSS

*This page was based on the examples available at the github folder: [Tutorial - Code Organization](https://github.com/UmSenhorQualquer/pyforms/tree/master/tutorials/3.CodeOrganization)*

By adding to same folder of the application the CSS file style.css, we can change the layout of the Application.

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
