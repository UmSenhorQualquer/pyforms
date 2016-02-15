import pyforms.Utils.tools as tools
from pyforms.web.Controls.ControlBase import ControlBase

class ControlCheckBox(ControlBase):

    def initControl(self):
        return "new ControlCheckBox('%s','%s','%s','%s')" % (self._label, self._name, self._value, self.help )