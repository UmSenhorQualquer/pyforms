import datetime
from pyforms.web.Controls.ControlBase import ControlBase

class ControlDate(ControlBase):

	def initControl(self): return "new ControlDate('{0}', {1})".format( self._name, str(self.serialize()) )
