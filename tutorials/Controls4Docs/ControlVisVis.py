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
		self._control 	= ControlVisVis('VisVis')
		
		self._formset = [' ',(' ', '_control', ' '),' ']

		self._control.value = [ [(10,20,10), (30,40,10)], [(10,20,3)] ]

		
		



##################################################################################################################
##################################################################################################################
##################################################################################################################

#Execute the application
if __name__ == "__main__":	 pyforms.startApp( SimpleExample )
	