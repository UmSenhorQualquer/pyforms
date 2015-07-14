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



class Example1(AutoForm):
	
	def __init__(self):
		super(Example1,self).__init__('Simple example 1')

		#Definition of the forms fields
		self._checkbox 		= ControlCheckBox('Choose a directory')
		self._checkboxList 	= ControlCheckBoxList('Choose a file')
		self._player 		= ControlPlayer('Choose a file')
		self._slider		= ControlSlider('Slider')
		

		self._formset = [  '_slider', ('_checkboxList', '_player'), ('_checkbox',' ') ]


		self._checkboxList.value = [ ('Item 1', True), ('Item 2', False), ('Item 3', True)]







##################################################################################################################
##################################################################################################################
##################################################################################################################

#Execute the application
if __name__ == "__main__":	 app.startApp( Example1 )