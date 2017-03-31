#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import loggingbootstrap
from pysettings import conf;

conf += 'pyforms.settings'

__author__ = "Ricardo Ribeiro"
__credits__ = ["Ricardo Ribeiro"]
__license__ = "MIT"
__version__ = 'v1.0.beta'
__maintainer__ = "Ricardo Ribeiro"
__email__ = "ricardojvr@gmail.com"
__status__ = "Production"

logger = logging.getLogger(__name__)

if conf.PYFORMS_MODE in ['GUI', 'GUI-OPENCSP']:

	from pyforms.gui import Controls
	from pyforms.gui.BaseWidget import BaseWidget

	if conf.PYFORMS_MODE in ['GUI-OPENCSP']:
		from pyforms.gui.appmanager import start_app
	else:
		from pyforms.gui.standaloneManager import start_app

elif conf.PYFORMS_MODE in ['TERMINAL']:

	from pyforms.terminal import Controls
	from pyforms.terminal.BaseWidget import BaseWidget
	from pyforms.terminal.appmanager import start_app


elif conf.PYFORMS_MODE in ['WEB']:

	from pyforms_web.web import Controls
	from pyforms_web.web.BaseWidget import BaseWidget
	from pyforms_web.web.appmanager import start_app

# loggingbootstrap.create_double_logger(
# 	"pyforms",
# 	conf.PYFORMS_LOG_HANDLER_CONSOLE_LEVEL,
# 	conf.PYFORMS_LOG_FILENAME,
# 	conf.PYFORMS_LOG_HANDLER_FILE_LEVEL
# )