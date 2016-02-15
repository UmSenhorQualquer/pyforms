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
		self._control0 = ControlEventsGraph('Check me')
		self._control1 = ControlEventsGraph('Check me')
		self._control2 = ControlEventsGraph('Check me')
		self._control3 = ControlEventsGraph('Check me')

		self._txt = ControlText('Time')

		self._btn = ControlButton('Click')
		self._btn1 = ControlButton('Click 1')
		
		self._formset = [
			('_btn','_btn1'),
			('_control0','_control1'),
			('_control2','_control3'),
			'_txt']
			
		self._btn.value = self.__btn
		self._btn1.value = self.__btn1

		self._start = time.time()

		self.INTERVAL = 1
		

	def __btn(self):		
		for i in range(1000):
			s = random.randint( 0, 10000 )
			o = random.randint( 0, 1000  )
			self._control0.add_period( s, s+o, track=random.randint(0,30) )
			self._control0.add_period( random.randint(0, 10000), s+o, track=random.randint(0,30), color="#00FFDD")

		self._control0.value = 5000

	def __addEvent0(self):
		b = self._control0.value
		e = b+self.INTERVAL
		self._control0.add_period( b, e, track=random.randint(0,10) )
		self._control0.value = e

	def __addEvent1(self):
		b = self._control1.value
		e = b+self.INTERVAL
		self._control1.add_period( b, e, track=random.randint(0,10) )
		self._control1.value = e

	def __addEvent2(self):
		b = self._control2.value
		e = b+self.INTERVAL
		self._control2.add_period( b, e, track=random.randint(0,10) )
		self._control2.value = e

	def __addEvent3(self):
		b = self._control3.value
		e = b+self.INTERVAL
		self._control3.add_period( b, e, track=random.randint(0,10) )
		self._control3.value = e

		self._txt.value = str(time.time() - self._start)

	def __btn1(self):

		self._start = time.time()
		
		timer = QtCore.QTimer(self.form)
		timer.timeout.connect(self.__addEvent0)
		timer.start(self.INTERVAL)
		
		timer = QtCore.QTimer(self.form)
		timer.timeout.connect(self.__addEvent1)
		timer.start(self.INTERVAL)

		timer = QtCore.QTimer(self.form)
		timer.timeout.connect(self.__addEvent2)
		timer.start(self.INTERVAL)

		timer = QtCore.QTimer(self.form)
		timer.timeout.connect(self.__addEvent3)
		timer.start(self.INTERVAL)

		

##################################################################################################################
##################################################################################################################
##################################################################################################################

#Execute the application
if __name__ == "__main__":	 pyforms.startApp( SimpleExample )
	