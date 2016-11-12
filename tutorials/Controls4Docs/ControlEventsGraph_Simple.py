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
import random, time
from PyQt4 import QtCore

class SimpleExample(BaseWidget):

	def __init__(self):
		super(SimpleExample,self).__init__('Simple example')

		#Definition of the forms fields
		self._control = ControlEventsGraph('Check me')

		self._txt = ControlText('Time')

		self._btn = ControlButton('Click')
		self._btn1 = ControlButton('Click 1')
		
		self.formset = [
			'_btn',
			'_control',
			'_txt']
			
		self._btn.value = self.__btn

		self._control.scale = 4

		self._control.add_event( 100, 200, track=0 )

	def __btn(self):
		#self._control.value = 10
		
		for i in range(1):
			s = random.randint( 100,  1000 )
			o = random.randint( 1000, 10000 )
			self._control.add_event( s, s+o, track=random.randint(0,4) )
			self._control.value = s+o

			print('Add event', s, s+o)
		
		self._control.repaint()
		#self._control.value = 5013

		

##################################################################################################################
##################################################################################################################
##################################################################################################################

#Execute the application
if __name__ == "__main__":	 pyforms.start_app( SimpleExample )
	