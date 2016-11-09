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
		self._control 	= ControlBoundingSlider('Threshold', default=[80, 255], min=0, max=255, 
			horizontal=True, helptext='help text example')
		
		self._formset = [' ','_control',' ']




		# IO test
		data = self._control.save_form({})
		data['value'] = 200, 255
		self._control.load_form(data)

		self._control.hide()
		self._control.show()
		
		self._control.add_popup_menu_option('option 0', function_action=lambda x: x)

		submenu1 = self._control.add_popup_submenu('menu 1')
		submenu2 = self._control.add_popup_submenu('menu 2', submenu=submenu1)

		self._control.add_popup_menu_option('option 1', function_action=lambda x: x, key='Control+Q', submenu=submenu2)

		self._control.changed_event = self.__control_changed_event

	def __control_changed_event(self):
		print self._control.value




##################################################################################################################
##################################################################################################################
##################################################################################################################

#Execute the application
if __name__ == "__main__":	 pyforms.startApp( SimpleExample )
	