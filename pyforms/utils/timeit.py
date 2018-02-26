#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"



import time
from datetime import datetime as datetime_dt, timedelta

def timeit(method):
	def timed(*args, **kw):
		ts = time.time()
		result = method(*args, **kw)
		te = time.time()
		time_elapsed = datetime_dt(1,1,1) + timedelta(seconds=(te-ts) )
		print("%s: %d:%d:%d:%d;%d" % (method.__name__, time_elapsed.day-1, time_elapsed.hour, time_elapsed.minute, time_elapsed.second, time_elapsed.microsecond))
		return result
	return timed