from pyforms.web.Controls.ControlBase import ControlBase
from django.utils 	import timezone
from datetime 		import datetime, timedelta
import time
import dateutil.parser


class ControlTimeout(ControlBase):

	def __init__(self, label = "", defaultValue = "", helptext=''):
		super(ControlTimeout, self).__init__(label, defaultValue, helptext)
		self._last_trigger 	= timezone.now()
		self._play = True
		self._update_value = True
		self.value = 10000
		self._update_interval = 1000

	def initControl(self):
		return """new ControlTimeout('{0}', {1})""".format(
			self._name, 
			str(self.serialize()) 
		)

	def trigger_event(self):
		self._last_trigger 	= timezone.now()
		self._update_value  = True
		self.trigger()

	def trigger(self): pass

	def serialize(self):
		data = { 
			'name':     	str(self.__class__.__name__), 
			'label':    	str(self._label if self._label else ''),
			'help':     	str(self._help  if self._help  else ''),
			'visible':  	int(self._visible),
			'play': 		str(self._play),
			'update_interval': 	self._update_interval,
			'last_trigger': self._last_trigger.isoformat()
		}
		if self._update_value: data.update({'value': self.value, 'update_value': str(False) })
			
		return data
		
	def deserialize(self, properties):
		self.value    = int(properties.get('value',None))
		self._label   = properties.get('label','')
		self._help    = properties.get('help','')
		self._visible = properties.get('visible',True)
		self._update_interval = properties.get('update_interval',1000)
		self._play 			  = properties.get('play','True')=='True' or properties.get('play','True')==True
		self._update_value 	  = properties.get('update_value', 'False')=='True' or properties.get('update_value', 'False')==True

		self._last_trigger = dateutil.parser.parse(properties.get('last_trigger'))
		

	@property
	def value(self): return ControlBase.value.fget(self)

	@value.setter
	def value(self, value):
		ControlBase.value.fset(self, value )
		self._update_value = True

	def play(self): 
		self._update_value = True
		self._play 		   = True
	def stop(self): 
		self._update_value = True
		self._play 		   = False

	def toggle_pause(self): 
		self._play 		   = not self._play
		