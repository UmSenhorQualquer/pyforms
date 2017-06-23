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
import numpy as np

import random

class Example4(BaseWidget):
	
	def __init__(self):
		super(Example4,self).__init__('Simple example 4')

		#Definition of the forms fields
		self._visvis	= ControlVisVis('Visvis')
		

		self.formset = [ '_visvis' ]

		values1 =  [ (i, random.random(), random.random()) for i in range(130) ]
		values2 =  [ (i, random.random(), random.random()) for i in range(130) ]
	
		self._visvis.value = [values1, values2]

##################################################################################################################
##################################################################################################################
##################################################################################################################

#Execute the application
if __name__ == "__main__":	 pyforms.start_app( Example4 )