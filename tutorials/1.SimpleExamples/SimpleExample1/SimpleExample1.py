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




class SimpleExample1(BaseWidget):
	
	
	def __init__(self):
		super(SimpleExample1,self).__init__('Simple example 1')

		#Definition of the forms fields
		self._firstname 	= ControlText('First name', 'Default value')
		self._middlename 	= ControlText('Middle name')
		self._lastname 		= ControlText('Lastname name')
		self._fullname 		= ControlText('Full name')
		self._button 		= ControlButton('Press this button')
		self._graph 		= ControlMatplotlib('Graph')

		#Define the button action
		self._button.value = self.__buttonAction

		self._graph.value = self.__on_draw



	def __on_draw(self, figure):
		""" Redraws the figure
		"""
		data = [1,2,1,4]
		x 	 = range(len(data))
		
		axes = figure.add_subplot(111)
		axes.bar(left=x, height=data)

		
		axes = figure.add_subplot(222, projection='3d')
		#axes.clear(); 
		pts = axes.scatter(x, data, data, c=x)
		figure.colorbar(pts)


	def __buttonAction(self):
		"""Button action event"""
		self._fullname.value = self._firstname.value +" "+ self._middlename.value + \
		" "+ self._lastname.value







##################################################################################################################
##################################################################################################################
##################################################################################################################

#Execute the application
if __name__ == "__main__":	 pyforms.start_app( SimpleExample1 )
	