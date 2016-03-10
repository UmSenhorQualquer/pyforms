import pyforms.Utils.tools as tools
from pyforms.web.Controls.ControlBase import ControlBase

class ControlCheckBox(ControlBase):

    def initControl(self): return "new ControlCheckBox('{0}', {1})".format( self._name, str(self.serialize()) )