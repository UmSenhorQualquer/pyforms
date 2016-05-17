from pyforms.web.Controls.ControlBase import ControlBase
from django.utils 	import timezone
from datetime 		import datetime, timedelta

class ControlTimeout(ControlBase):

	def __init__(self, label = "", defaultValue = "", helptext=''):
		self._last_trigger 	= timezone.now()
		super(ControlTimeout, self).__init__(label, defaultValue, helptext)

	def initControl(self):
		return """new ControlTimeout('{0}', {1})""".format(
			self._name, 
			str(self.serialize()) 
		)

	def trigger(self): pass

	def serialize(self):
		data 			= ControlBase.serialize(self)
		total_milliseconds 	= int(round(( (self._last_trigger+timedelta(0,self.value))-timezone.now() ).total_seconds(), 0))
		data.update({ 'last_trigger':  self._last_trigger.strftime("%Y-%m-%d %H:%M:%S")})
		data.update({ 'total_milliseconds': total_milliseconds})
		return data
		
	def deserialize(self, properties):
		ControlBase.deserialize(self,properties)		
		self._last_trigger 	= datetime.strptime(properties['last_trigger'], "%Y-%m-%d %H:%M:%S")