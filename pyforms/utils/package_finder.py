import importlib, re

#import logging; logger = logging.getLogger(__name__)

def get_module_and_class(plugin_info):
	"""
	:param plugin_info:
	:return:
	"""
	expression = re.compile('(.*)\.(\w*)')
	
	res = re.findall(expression, plugin_info)
	if len(res)>0:
		matches = re.findall(expression, plugin_info)[0]
		plugin_module = matches[0]
		plugin_class = matches[1]
		return plugin_module, plugin_class
	else:
		return None




class PackageFinder(object):

	def __init__(self, plugins = []): 	self._plugins = plugins
	def __add__(self, other): 			self._plugins.append(other); return self
	def __sub__(self, other): 			self._plugins.remove(other); return self

	def find_class(self, class_full_name):
		res = get_module_and_class(class_full_name)
		if res is None: return []

		package_name, class_name = res

		res = []
		for plugin in self._plugins:
			try:		
				module 		= importlib.import_module("."+package_name, plugin)
				class_def 	= getattr(module, class_name)
				res.append(class_def)
			except:
				#logger.error('Error importing model',exc_info=True)
				pass

		return res