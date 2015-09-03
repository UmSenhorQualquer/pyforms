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
import cv2

class SimpleExample(BaseWidget):
	
	
	def __init__(self):
		super(SimpleExample,self).__init__('Simple example')

		#Definition of the forms fields
		self._control 	= ControlImage('Image')
		self._open 	= ControlButton('Open')
		
		self._formset = [' ',(' ', '_control', ' '),'_open']

		self._open.value = self.__open
		
	def initForm(self):
		super(SimpleExample, self).initForm()

	def __open(self):
		self._control.value = '/home/ricardo/Desktop/lena_color.png'



##################################################################################################################
##################################################################################################################
##################################################################################################################

#Execute the application
if __name__ == "__main__":	 pyforms.startApp( SimpleExample )
	