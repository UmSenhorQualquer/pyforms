# !/usr/bin/python3
# -*- coding: utf-8 -*-

""" pyForms

"""
import logging

__author__ = "Ricardo Ribeiro"
__copyright__ = "Copyright 2016 Champalimaud Foundation"
__credits__ = "Ricardo Ribeiro"
__license__ = "MIT"
__maintainer__ = ["Ricardo Ribeiro", "Carlos Mão de Ferro"]
__email__ = ["ricardojvr at gmail.com", "cajomferro at gmail.com"]
__status__ = "Development"

PYFORMS_MODE = 'GUI'
PYFORMS_LOG_HANDLER_FILE_LEVEL = logging.DEBUG
PYFORMS_LOG_HANDLER_CONSOLE_LEVEL = logging.INFO
LOG_FILENAME = "pyforms"

CONTROL_CODE_EDITOR_DEFAULT_FONT_SIZE = '12'
CONTROL_EVENTS_GRAPH_DEFAULT_SCALE = 1

try:
	from settings import *
except:
	pass

