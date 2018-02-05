#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


from __init__ import *

class ComputerVisionAlgorithm(BaseWidget):
	
	def __init__(self):
		super(ComputerVisionAlgorithm,self).__init__('Computer vision algorithm example')

		#Definition of the forms fields
		self._videofile  = ControlFile('Video')
		self._outputfile = ControlText('Results output file')
		self._threshold  = ControlSlider('Threshold', default=114, 0,255)
		self._blobsize 	 = ControlSlider('Minimum blob size', default=100, 100,2000)
		self._player 	 = ControlPlayer('Player')
		self._runbutton  = ControlButton('Run')

		#Define the function that will be called when a file is selected
		self._videofile.changed_event   = self.__videoFileSelectionEvent
		#Define the event that will be called when the run button is processed
		self._runbutton.value 	  = self.__runEvent
		#Define the event called before showing the image in the player
		self._player.process_frame_event = self.__process_frame

		#Define the organization of the Form Controls
		self.formset = [ 
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

	def __process_frame(self, frame):
		"""
		Do some processing to the frame and return the result frame
		"""
		return frame

	def __runEvent(self):
		"""
		After setting the best parameters run the full algorithm
		"""
		pass



##################################################################################################################
##################################################################################################################
##################################################################################################################

#Execute the application
if __name__ == "__main__":	 pyforms.start_app( ComputerVisionAlgorithm )