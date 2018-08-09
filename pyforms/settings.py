# !/usr/bin/python3
# -*- coding: utf-8 -*-


import logging, os, sys

if 'terminal_mode' in sys.argv:
	PYFORMS_MODE = 'TERMINAL'
else:
	PYFORMS_MODE = os.environ.get('PYFORMS_MODE', 'GUI')

PYFORMS_LOG_FILENAME 				= 'pyforms.log'
PYFORMS_LOG_HANDLER_FILE_LEVEL 		= logging.INFO
PYFORMS_LOG_HANDLER_CONSOLE_LEVEL 	= logging.INFO