# Pyforms

**[ Checkout Github for the source code ](https://github.com/UmSenhorQualquer/pyforms)**

<!-- Posicione esta tag no cabeçalho ou imediatamente antes da tag de fechamento do corpo. -->
<script src="https://apis.google.com/js/platform.js" async defer></script>

<!-- Posicione esta tag onde você deseja que o widget apareça. -->
<div class="g-follow" data-annotation="bubble" data-height="24" data-rel="publisher"></div>


Pyforms is a Python 2.7.x and 3.x cross-enviroment framework to develop GUI applications, which promotes modular software design and code reusability with minimal effort.

### It offers
* A Python layer of Desktop forms, based on PyQt, OpenGL and other libraries.
* A Python layer that allow applications to run on Desktop GUI, Web and terminal without requiring code modifications.
* A group of rules and methodologies that help the developer maintain short, clean, reusable and readable code. 

![Diagram](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/v1.0.beta/docs/pyforms.png?raw=true "Screen")

Example of an application running in the Desktop, Web and Terminal enviroments:

![Application-Example](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/v1.0.beta/docs/example.png?raw=true "Screen")


## Installation

Run in the terminal:
```bash
pip install pyforms
```

### Requirements

* [setuptools] (https://pypi.python.org/pypi/setuptools)
* [Python 2.7](https://www.python.org/download/releases/2.7/)
* [pysettings](https://github.com/UmSenhorQualquer/pysettings.git)
* [PyQt4](http://www.riverbankcomputing.co.uk/software/pyqt/download)
* [PyOpenGL](http://pyopengl.sourceforge.net/) [Optional - Only used by some Controls]
* [VisVis](https://code.google.com/p/visvis/) [Optional - Only used by some Controls]
* [Numpy](http://www.numpy.org/) [Optional - Only used by some Controls]
* [Python opencv](http://opencv.org/) [Optional - Only used by some Controls]


### Ubuntu 14

* setuptools: ```sudo apt-get install python-setuptools```
* pysettings: ```sudo pip install git+https://github.com/UmSenhorQualquer/pysettings.git```
* Opengl: ```sudo apt-get install python-opengl```
* OpenCV: ```sudo apt-get install python-opencv```
* PyQt4: ```sudo apt-get install pyqt4-dev-tools python-qt4```
* PyQt4 OpenGL Widget [Optional]: ```sudo apt-get install python-qt4-gl```
* Pyforms: ```sudo pip install pyforms```
* VisVis: ```sudo pip install visvis```

### Mac OSx

* Install python and its tools using [Homebrew] (http://brew.sh)
* [Scientific Python on Mac OS X 10.9+ with homebrew | Jörn's Blog](https://joernhees.de/blog/2014/02/25/scientific-python-on-mac-os-x-10-9-with-homebrew/)
* [Installing scientific Python on Mac OS X | Lowin Data Company](http://www.lowindata.com/2013/installing-scientific-python-on-mac-os-x/)
* run ```sudo python setup.py install```

