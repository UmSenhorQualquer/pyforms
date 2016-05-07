# !/usr/bin/python3
# -*- coding: utf-8 -*-

""" pyForms

"""

import logging
import importlib
import os

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

def load_everything_from(module_names):
    """
    Load all
    :param module_names: modules to be imported
    :type module_names: list of strings
    """
    g = globals()
    for module_name in module_names:
        m = importlib.import_module(module_name)
        names = getattr(m, '__all__', None)
        if names is None:
            names = [name for name in dir(m) if not name.startswith('_')]
        for name in names:
            g[name] = getattr(m, name)

try:
    from settings import *
except:
    pass


try:
    # print(os.environ.get('PYFORMS_APP_SETTINGS'))
    module_name = os.getenv('PYFORMS_APP_SETTINGS', '')
    if module_name:
        print('loading PYFORMS_APP_SETTINGS',module_name)
        load_everything_from([module_name])
        

    # user_settings = importlib.import_module(os.environ.get('APP_USER_SETTINGS'))
    # from user_settings import *
    # from pythonvideoannotator.settings import *
except Exception as err:
    print(err)

