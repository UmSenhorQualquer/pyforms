#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


from setuptools import setup

setup(

	name				='PyForms',
	version 			='0.0',
	description 		="""Pyforms is a Python 2.7 framework to develop GUI application, 
		which promotes modular software design and code reusability with minimal effort.""",
	author  			='Ricardo Ribeiro',
	author_email		='ricardojvr@gmail.com',
	license 			='MIT',

	download_urlname	='https://github.com/UmSenhorQualquer/pyforms',
	url 				='https://github.com/UmSenhorQualquer/pyforms',
	
	packages=[
		'pyforms',
		'pyforms.Controls', 
		'pyforms.Utils',
		'pyforms.Controls.ControlEventTimeline' ],
	package_data={'pyforms': ['uipics/*.png', '*.ui', 'Controls/*.ui',]},

	install_requires=[
		"pyopengl >= 3.1.0",
		"visvis >= 1.9.1",
		"numpy >= 1.6.1"
	],
)