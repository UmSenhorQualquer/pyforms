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
PYFORMS_LOG_LEVEL = logging.INFO

CONTROL_CODE_EDITOR_DEFAULT_FONT_SIZE = '12'
CONTROL_EVENTS_GRAPH_DEFAULT_SCALE = 1


def setup_pyforms_logger():
    """ Setup logger for this app """
    # create logger
    logger = logging.getLogger('pyforms')
    logger.setLevel(PYFORMS_LOG_LEVEL)

    # create file handler which logs even debug messages
    # fh = logging.FileHandler('{0}.log'.format(APP_NAME))
    # fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(PYFORMS_LOG_LEVEL)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(module)s | %(message)s', datefmt='%d/%m/%Y %I:%M:%S')
    # fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    # logger.addHandler(fh)
    logger.addHandler(ch)

try:
	from settings import *
except:
	pass

setup_pyforms_logger()


