# Pyforms


Pyforms is a Python 2.7 framework to develop GUI application, which promotes modular software design and code reusability with minimal effort.
### It offers:
* A Python layer of Windows forms, based on PyQt, OpenGL and other libraries.
* A group of rules and methodologies that help the developer maintaining his code short, clean, reusable and readable. 

## Advantages
* With a minimal API, windows interfaces are easily defined using a short Python code.
* Avoid the constant switching between the PyQt designer and the Python IDE.
* It is designed to allow the coding of advanced functionalities with a minimal effort.
* The code is organized in modules and prepared to be reused by other applications.
* It makes the applications maintenance easier.
* Turn the prototyping much easier and fast.
* Due to its simplicity it has a low learning curve.

## Examples of applications developed in Pyforms
* [Python Video Annotator](https://github.com/UmSenhorQualquer/pythonVideoAnnotator)


## Rationale behind the framework

## Installation

#### Requirements

* [Python 2.7](https://www.python.org/download/releases/2.7/)
* [PyQt4](http://www.riverbankcomputing.co.uk/software/pyqt/download)
* [PyOpenGL](http://pyopengl.sourceforge.net/) [Optional - Only used by some Controls]
* [VisVis](https://code.google.com/p/visvis/) [Optional - Only used by some Controls]
* [Numpy](http://www.numpy.org/) [Optional - Only used by some Controls]

##### Ubuntu 14

* run ```sudo python setup.py install```
* PyQt4: ```sudo apt-get install pyqt4-dev-tools python-qt4```
* PyQt4 OpenGL Widget [Optional]: ```sudo apt-get install python-qt4-gl```

##### Mac OSx

* run ```sudo python setup.py install```
* install pyqt4 with the gl module

## License

Pyforms is open-source library under the MIT license.