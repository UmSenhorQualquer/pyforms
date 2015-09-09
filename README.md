![Important](https://img.shields.io/badge/Important-Note-red.svg "Screen")  
If you find this project useful, please ![star it](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/master/docs/imgs/start.png?raw=true "Screen") it. It will motivate me to continue improving it.

![New version available](https://img.shields.io/badge/New%20version%20available-0.1-green.svg "Screen")



# Pyforms

<!-- Posicione esta tag no cabeçalho ou imediatamente antes da tag de fechamento do corpo. -->
<script src="https://apis.google.com/js/platform.js" async defer></script>

<!-- Posicione esta tag onde você deseja que o widget apareça. -->
<div class="g-follow" data-annotation="bubble" data-height="24" data-rel="publisher"></div>

Pyforms is a Python 2.7.x and 3.x cross-enviroment framework to develop GUI applications, which promotes modular software design and code reusability with minimal effort.

### It offers:
* A Python layer of Desktop forms, based on PyQt, OpenGL and other libraries.
* A Python layer that allow applications to run on Desktop GUI, Web and terminal without requiring code modifications.
* A group of rules and methodologies that help the developer maintaining his code short, clean, reusable and readable. 

![Diagram](docs/pyforms.png?raw=true "Screen")

Example of an application running in the Desktop, Web and Terminal enviroments:

![Application-Example](docs/example.png?raw=true "Screen")

## Advantages
* With a minimal API, interfaces are easily defined using a short Python code.
* Avoid the constant switching between the GUI designers and the Python IDE.
* It is designed to allow the coding of advanced functionalities with a minimal effort.
* The code is organized in modules and prepared to be reused by other applications.
* It makes the applications maintenance easier.
* Turn the prototyping much easier and fast.
* Due to its simplicity it has a low learning curve.

## Examples of applications developed in Pyforms
* [Python Video Annotator](https://github.com/UmSenhorQualquer/pythonVideoAnnotator)

## Documentation

The documentation is still in development, but you can find a preview on [pyforms.readthedocs.org](http://pyforms.readthedocs.org)

## Installation


##### Requirements

* [setuptools] (https://pypi.python.org/pypi/setuptools)
* [Python 2.7](https://www.python.org/download/releases/2.7/)
* [PyQt4](http://www.riverbankcomputing.co.uk/software/pyqt/download)
* [PyOpenGL](http://pyopengl.sourceforge.net/) [Optional - Only used by some Controls]
* [VisVis](https://code.google.com/p/visvis/) [Optional - Only used by some Controls]
* [Numpy](http://www.numpy.org/) [Optional - Only used by some Controls]
* [Python opencv](http://opencv.org/) [Optional - Only used by some Controls]


##### Ubuntu 14

* setuptools: ```sudo apt-get install python-setuptools```
* Opengl: ```sudo apt-get install python-opengl```
* OpenCV: ```sudo apt-get install python-opencv```
* PyQt4: ```sudo apt-get install pyqt4-dev-tools python-qt4```
* PyQt4 OpenGL Widget [Optional]: ```sudo apt-get install python-qt4-gl```
* Pyforms: ```sudo pip install pyforms```
* VisVis: ```sudo pip install visvis```

##### Mac OSx

* Install python and its tools using [Homebrew] (http://brew.sh)
* [Scientific Python on Mac OS X 10.9+ with homebrew | Jörn's Blog](https://joernhees.de/blog/2014/02/25/scientific-python-on-mac-os-x-10-9-with-homebrew/)
* [Installing scientific Python on Mac OS X | Lowin Data Company](http://www.lowindata.com/2013/installing-scientific-python-on-mac-os-x/)
* run ```sudo python setup.py install```

## License

Pyforms is open-source library under the MIT license.

## Rationale behind the framework

The development of this library started with the necessity of allowing users with low programming skills to edit parameters of my python scripts.
The idea was to transform scripts which had already been developed into GUI applications with a low effort and in a short time.

For example in my computer vision applications in the majority of the times there were variables that had to be set manually in the scripts for each video, to adjust the thresholds, blobs sizes, and other parameters to the environment light conditions... To test each set of parameters the script had to be executed.
With GUI applications, users would be able to set the parameters using an GUI interface and visualize the results instantly without needing to restart the script. That was the idea.

After looking into the several python options for GUI interfaces, PyQt was the one that offered the best tool for a fast development with the QtDesigner, but after a while developing in Qt, switching between the designer and the python IDE was becoming too costly in terms of time, because the interfaces were constantly evolving, and tedious, because GUI controls were repeated too many times.

Being a Django developer, I did get inspiration on it for this framework. In the [Django](https://www.djangoproject.com/) Models we just need to define the type of variables and their disposition in the form (in ModelAdmin) to generate a HTML form for data edition.
For the GUIs that I wanted to build for my python scripts, I would like to have the same simplicity, because I did wanted to focus on the algorithms and not on GUIs developing.

The result was the simplicity that we can see in the example below:

```python
class ComputerVisionAlgorithm(BaseWidget):
	
	def __init__(self):
		super(ComputerVisionAlgorithm,self).__init__('Computer vision algorithm example')

		#Definition of the forms fields
		self._videofile 	= ControlFile('Video')
		self._outputfile 	= ControlText('Results output file')
		self._threshold 	= ControlSlider('Threshold', 114, 0,255)
		self._blobsize 		= ControlSlider('Minimum blob size', 100, 100,2000)
		self._player 		= ControlPlayer('Player')
		self._runbutton 	= ControlButton('Run')

		#Define the function that will be called when a file is selected
		self._videofile.changed 	= self.__videoFileSelectionEvent
		#Define the event that will be called when the run button is processed
		self._runbutton.value 		= self.__runEvent
		#Define the event called before showing the image in the player
		self._player.processFrame 	= self.__processFrame

		#Define the organization of the Form Controls
		self._formset = [ 
			('_videofile', '_outputfile'), 
			'_threshold', 
			('_blobsize', '_runbutton'), 
			'_player'
		]


	def __videoFileSelectionEvent(self):
		"""
		When the videofile is selected instanciate the video in the player
		"""
		self._player.value = self._videofile.value

	def __processFrame(self, frame):
		"""
		Do some processing to the frame and return the result frame
		"""
		return frame

	def __runEvent(self):
		"""
		After setting the best parameters run the full algorithm
		"""
		pass
```

![ScreenShot](tutorials/1.SimpleExamples/ComputerVisionAlgorithmExample/screenshot.png?raw=true "Screen")
