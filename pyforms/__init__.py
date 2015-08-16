#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


from pyforms import conf




if conf.PYFORMS_MODE in ['GUI','GUI-OPENCSP']:
	
	from pyforms.gui 						import Controls
	from pyforms.gui.BaseWidget				import BaseWidget
	try:
		from pyforms.gui.PyFormsStateMachine	import PyFormsStateMachine, gotoAppState, PyFormsState
	except: 
		print("PyFormsStateMachine is not working")

	
	if conf.PYFORMS_MODE in ['GUI-OPENCSP']: 	from pyforms.gui.appmanager import startApp
	else: 										from pyforms.gui.standaloneManager import startApp



elif conf.PYFORMS_MODE in ['TERMINAL']:

	from pyforms.terminal 				import Controls
	from pyforms.terminal.BaseWidget	import BaseWidget

	try:
		from pyforms.terminal.PyFormsStateMachine	import PyFormsStateMachine, gotoAppState, PyFormsState
	except:
		print("PyFormsStateMachine is not working")

	from pyforms.terminal.appmanager 	import startApp



elif conf.PYFORMS_MODE in ['WEB']:


	from pyforms.web 						import Controls
	from pyforms.web.BaseWidget				import BaseWidget
	try:
		from pyforms.web.PyFormsStateMachine	import PyFormsStateMachine, gotoAppState, PyFormsState
	except:
		print("PyFormsStateMachine is not working")

	from pyforms.web.appmanager 			import startApp
