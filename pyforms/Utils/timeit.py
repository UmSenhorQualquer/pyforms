
import time
from datetime import datetime, timedelta

def timeit(method):
	def timed(*args, **kw):
		ts = time.time()
		result = method(*args, **kw)
		te = time.time()
		time_elapsed = datetime(1,1,1) + timedelta(seconds=(te-ts) )
		print "%s: %d:%d:%d:%d;%d" % (method.__name__, time_elapsed.day-1, time_elapsed.hour, time_elapsed.minute, time_elapsed.second, time_elapsed.microsecond)
		return result
	return timed