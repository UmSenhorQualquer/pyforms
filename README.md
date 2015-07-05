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


## Installation

##### Requirements

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


## Rationale behind the framework

The development of this library started with the necessity of allowing users with low programming skills to edit parameters of computer vision applications implemented in python scripts.
The idea was to transform scripts which were already developed and running in the terminal into GUI applications with low affort and in a short time.

In the computer vision applications at the majority of the times there were varibles that had to be set manually in the scripts for each video to adjust the threshols, blobs sizes, to the enviroment light conditions.. To test each set of parameters the script had to be executed.
With GUIs applications, users would be able to set the parameters using an GUI interface and visualize the results instantly without needing to restart the script. That was the idea.

After looking into the several python options for GUI interfaces, pyqt was the one that offered the best tools for a fast development with the QtDesign, but after a while programming with Qt, switching between the designer and the python IDE was becoming to costly in terms of time, because the interfaces were constantly evoluting, and tedius because GUI controls were repeating many times.

Being a Django developer I did got inspiration on it for this framework. In the [Django](https://www.djangoproject.com/) Models we just need to define the type of variables and their disposition in the form (in ModelAdmin) to generate a HTML form for data edition.

The result was the design of an interface like this:


What we had were:

```python
class ComputerVisionAlgorithm(AutoForm):
	
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