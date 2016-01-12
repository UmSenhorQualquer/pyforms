#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.1"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Production"


from setuptools import setup

setup(

	name				='PyForms',
	version 			='0.1.3',
	description 		="""Pyforms is a Python 2.7 and 3.0 framework to develop GUI application, 
		which promotes modular software design and code reusability with minimal effort.""",
	author  			='Ricardo Ribeiro',
	author_email		='ricardojvr@gmail.com',
	license 			='MIT',

	download_urlname	='https://github.com/UmSenhorQualquer/pyforms',
	url 				='https://github.com/UmSenhorQualquer/pyforms',
	
	packages=[
		'pyforms',
		'pyforms.Utils',
		'pyforms.terminal',
		'pyforms.terminal.Controls', 
		'pyforms.web',
		'pyforms.web.Controls', 
		'pyforms.web.django', 
		'pyforms.web.django.templatetags', 
		'pyforms.gui',
		'pyforms.gui.dialogs',
		'pyforms.gui.Controls', 
		'pyforms.gui.Controls.ControlEventTimeline',
		'pyforms.gui.Controls.ControlEventsGraph',
		'pyforms.gui.Controls.ControlPlayer' ],
	package_data={'pyforms': [
			'web/django/*.js',
			'web/django/chartjs/Chart.min.js',
			'gui/Controls/uipics/*.png', 
			'gui/mainWindow.ui', 'gui/Controls/*.ui', 'gui/Controls/ControlPlayer/*.ui', 
			'gui/Controls/ControlEventTimeline/*.ui']
		},

	install_requires=[
		"pyopengl >= 3.1.0",
		"visvis >= 1.9.1",
		"numpy >= 1.6.1"
	],
)