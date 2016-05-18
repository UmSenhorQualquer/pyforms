import pyforms.Utils.tools as tools
from pyforms.web.Controls.ControlBase import ControlBase

class ControlCheckBox(ControlBase):

	def initControl(self): return "new ControlCheckBox('{0}', {1})".format( self._name, str(self.serialize()) )

	

	def serialize(self):
		return { 
			'name':     str(self.__class__.__name__), 
			'value':    str(self.value),
			'label':    str(self._label if self._label else ''),
			'help':     str(self._help if self._help else ''),
			'visible':  int(self._visible)
		}

	def deserialize(self, properties):
		self.value    = properties.get('value',None)=='True'
		self._label   = properties.get('label','')
		self._help    = properties.get('help','')
		self._visible = properties.get('visible',True)