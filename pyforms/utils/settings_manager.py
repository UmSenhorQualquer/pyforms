
import logging; logger = logging.getLogger(__name__)

class SettingsManager(object):

	def __init__(self):
		self._modules = []
		self._loaded_modules = {}

	def __load_module(self, module_name):
		if module_name in self._loaded_modules.keys(): return self._loaded_modules[module_name]

		modules = module_name.split('.')
		moduleclass = __import__( '.'.join(modules[:-1]) , fromlist=[modules[-1]] )

		module = getattr(moduleclass, modules[-1])
		self._loaded_modules[module_name] = module

		return module

	def __add__(self, other):
		if isinstance(other, str): other = self.__load_module(other)

		modules = object.__getattribute__(self, '_modules')
		if other not in modules:
			logger.info('added settings: {0}'.format(other.__name__))
			modules.append(other)
			self._modules = sorted(modules, key=lambda x: (x.SETTINGS_PRIORITY if hasattr(x, 'SETTINGS_PRIORITY') else 999999999)  )
		return self

	def __sub__(self, other):
		self._modules.remove(other)
		return self
	
	def __getattribute__(self, name):
		for module in object.__getattribute__(self, '_modules'):
			if hasattr(module, name): return getattr(module, name)

		return object.__getattribute__(self, name)


conf = SettingsManager()