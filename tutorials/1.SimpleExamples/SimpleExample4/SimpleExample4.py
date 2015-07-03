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



class SimpleExample4(AutoForm):
	
	def __init__(self):
		super(SimpleExample4,self).__init__('Simple example 4')

		#Definition of the forms fields
		self._firstname 	= ControlText('First name', 'Default value')
		self._middlename 	= ControlText('Middle name')
		self._lastname 		= ControlText('Lastname name')
		self._fullname 		= ControlText('Full name')
		self._button 		= ControlButton('Press this button')

		#Define the organization of the forms
		self._formset = [ {
						  	'Tab1':['_firstname','||','_middlename','||','_lastname'], 
						  	'Tab2': ['_fullname']
						  },
						  '=',(' ','_button', ' ') ]
		#Use dictionaries for tabs
		#Use the sign '=' for a vertical splitter
		#Use the signs '||' for a horizontal splitter

		#Define the button action
		self._button.value = self.__buttonAction


	def __buttonAction(self):
		"""Button action event"""
		self._fullname.value = self._firstname.value +" "+ self._middlename.value + \
		" "+ self._lastname.value



##################################################################################################################
##################################################################################################################
##################################################################################################################

#Execute the application
if __name__ == "__main__":	 app.startApp( SimpleExample4 )
	