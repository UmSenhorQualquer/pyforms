#!/usr/bin/python
# -*- coding: utf-8 -*-

from confapp import conf

conf += 'pyforms.settings'

try:
	import settings
	conf += settings
except:
	pass

__author__ 		= "Ricardo Ribeiro"
__credits__ 	= ["Ricardo Ribeiro"]
__license__ 	= "MIT"
__version__ 	= '3.0.1'
__maintainer__ 	= ["Ricardo Ribeiro", "Carlos Mão de Ferro"]
__email__ 		= ["ricardojvr@gmail.com", "cajomferro@gmail.com"]
__status__ 		= "Production"

print(conf.PYFORMS_MODE)

if conf.PYFORMS_MODE in ['GUI', 'GUI-OPENCSP']:

	from pyforms.gui import controls
	from pyforms.gui.basewidget import BaseWidget
	from pyforms.gui.appmanager import start_app
	from pyforms.gui.basewidget import vsplitter, hsplitter, segment, no_columns

elif conf.PYFORMS_MODE in ['TERMINAL']:

	from pyforms.terminal import controls
	from pyforms.terminal.basewidget import BaseWidget
	from pyforms.terminal.appmanager import start_app


elif conf.PYFORMS_MODE in ['WEB']:

	from pyforms_web.basewidget import BaseWidget, no_columns, segment
	from pyforms_web.modeladmin import ModelAdmin
	from pyforms_web.modeladmin import ViewFormAdmin
	from pyforms_web.modeladmin import EditFormAdmin
