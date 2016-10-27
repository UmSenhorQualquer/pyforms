import importlib, re, os

import logging; logger = logging.getLogger(__name__)

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
				"""
				package_relative_path 	= os.path.join( *package_name.split('.') )
				plugin_path 			= os.path.dirname(plugin.__file__)
				filepath 				= os.path.join(plugin_path, package_relative_path)+'.py'
				print('checking file:', filepath)
				"""
				#if os.path.isfile(filepath):
				module 		= importlib.import_module("."+package_name, plugin)
				class_def 	= getattr(module, class_name)
				res.append(class_def)
			except ImportError:
				pass
			except:
				logger.error('Error importing model {0} {1} {2}'.format(str(plugin), str(package_name), str(class_name)),exc_info=True)
				pass

		return res