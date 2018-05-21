#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ 		= "Ricardo Ribeiro"
__credits__ 	= ["Ricardo Ribeiro"]
__license__ 	= "MIT"
__version__ 	= '4.0'
__maintainer__ 	= ["Ricardo Ribeiro"]
__email__ 		= ["ricardojvr@gmail.com"]
__status__ 		= "Production"


from confapp import conf

conf += 'pyforms.settings'

try:
	import settings
	conf += settings
except:
	pass