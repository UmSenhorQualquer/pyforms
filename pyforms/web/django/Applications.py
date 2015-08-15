import inspect, sys

class ApplicationsLoader:

	def __init__(self, applicationsPath):
		sys.path.append(applicationsPath)
		self._storage = {}


	def __getitem__(self, moduleclassname):
		if moduleclassname not in self._storage:
			modulename = '.'.join( [moduleclassname.lower(), moduleclassname] )
			moduleclass = __import__(modulename, fromlist=[moduleclassname])
			moduleclass =  getattr(moduleclass, moduleclassname)
			self._storage[moduleclassname] = moduleclass
		else:
			moduleclass = self._storage[moduleclassname]
		return moduleclass

	def createInstance(self, moduleclassname):
		app = self[moduleclassname]()
		#app.initForm()
		return app

	def moduleClassPath(self, moduleclassname):
		return inspect.getfile(self[moduleclassname])