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


class SimpleExample(BaseWidget):
	
	
	def __init__(self):
		super(SimpleExample,self).__init__('Simple example')

		#Definition of the forms fields
		self._control 	= ControlCombo('Countries')
		
		self._formset = [' ',(' ', '_control', ' '),' ']
		
		self._control.add_item('Portugal', 'pt')
		self._control.add_item('Angola', 'ao')
		self._control.add_item('Mocambique', 'mz')
		self._control.add_item('Brazil', 'br')
		self._control.add_item('Cabo Verde', 'cv')

		
		self._control.text = 'Brazil'

		self._control.changed_event = self.__print_value

	def __print_value(self):
		print self._control.value

##################################################################################################################
##################################################################################################################
##################################################################################################################

#Execute the application
if __name__ == "__main__":	 pyforms.startApp( SimpleExample )
	