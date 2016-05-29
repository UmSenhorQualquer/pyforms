#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
from pyforms import conf


__author__ = "Ricardo Ribeiro"
__credits__ = ["Ricardo Ribeiro"]
__license__ = "MIT"
__version__ = '0.1.6'
__maintainer__ = "Ricardo Ribeiro"
__email__ = "ricardojvr@gmail.com"
__status__ = "Production"

# create logger
logger = logging.getLogger("pyforms")
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('{0}.log'.format(conf.LOG_FILENAME))
fh.setLevel(conf.PYFORMS_LOG_HANDLER_FILE_LEVEL)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(conf.PYFORMS_LOG_HANDLER_CONSOLE_LEVEL)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(module)s | %(message)s', datefmt='%d/%m/%Y %I:%M:%S')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.debug("log pyforms is now set up")


if conf.PYFORMS_MODE in ['GUI', 'GUI-OPENCSP']:

    from pyforms.gui import Controls
    from pyforms.gui.BaseWidget import BaseWidget

    if conf.PYFORMS_MODE in ['GUI-OPENCSP']:
        from pyforms.gui.appmanager import startApp
    else:
        from pyforms.gui.standaloneManager import startApp


elif conf.PYFORMS_MODE in ['TERMINAL']:

    from pyforms.terminal import Controls
    from pyforms.terminal.BaseWidget import BaseWidget
    from pyforms.terminal.appmanager import startApp


elif conf.PYFORMS_MODE in ['WEB']:

    from pyforms_web.web import Controls
    from pyforms_web.web.BaseWidget import BaseWidget
    from pyforms_web.web.appmanager import startApp
