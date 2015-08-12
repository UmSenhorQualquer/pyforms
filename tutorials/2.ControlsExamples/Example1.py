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



class Example1(BaseWidget):
	
	def __init__(self):
		super(Example1,self).__init__('Simple example 1')

		#Definition of the forms fields
		self._directory 	= ControlDir('Choose a directory')
		self._file 			= ControlFile('Choose a file')
		self._filetree 		= ControlFilesTree('Choose a file')
		self._boundaries	= ControlBoundingSlider('Bounding', horizontal=True)

		self._formset = ['_directory', '_file', '_boundaries', '_filetree' ]


		self._filetree.value = '/'







##################################################################################################################
##################################################################################################################
##################################################################################################################

#Execute the application
if __name__ == "__main__":	 pyforms.startApp( Example1 )