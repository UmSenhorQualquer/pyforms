#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = '4.0'
__maintainer__  = ["Ricardo Ribeiro"]
__email__       = ["ricardojvr@gmail.com"]
__status__      = "Production"


from confapp import conf

conf += 'pyforms.settings'

try:
    import local_settings
    conf += local_settings
except:
    pass


if conf.PYFORMS_MODE == 'GUI':

    from pyforms_gui.appmanager import start_app

elif conf.PYFORMS_MODE == 'TERMINAL':

    from pyforms_terminal.appmanager import start_app