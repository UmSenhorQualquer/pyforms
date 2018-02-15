#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyforms.utils.settings_manager import conf

conf += 'pyforms.settings'

__author__ 		= "Ricardo Ribeiro"
__credits__ 	= ["Ricardo Ribeiro"]
__license__ 	= "MIT"
__version__ 	= '3.0.0'
__maintainer__ 	= ["Ricardo Ribeiro", "Carlos Mão de Ferro"]
__email__ 		= ["ricardojvr@gmail.com", "cajomferro@gmail.com"]
__status__ 		= "Production"

if conf.PYFORMS_MODE in ['GUI', 'GUI-OPENCSP']:

	from pyforms.gui import controls
	from pyforms.gui.basewidget import BaseWidget
	from pyforms.gui.appmanager import start_app

elif conf.PYFORMS_MODE in ['TERMINAL']:

	from pyforms.terminal import controls
	from pyforms.terminal.basewidget import BaseWidget
	from pyforms.terminal.appmanager import start_app


elif conf.PYFORMS_MODE in ['WEB']:

	from pyforms_web.web import Controls
	from pyforms_web.web.BaseWidget import BaseWidget
	from pyforms_web.web.appmanager import start_app

	from pyforms_web.web.django_pyforms.model_admin import ModelAdmin
	from pyforms_web.web.django_pyforms.model_admin import ViewFormAdmin
	from pyforms_web.web.django_pyforms.model_admin import EditFormAdmin
