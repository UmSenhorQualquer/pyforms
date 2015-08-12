import pyforms.Utils.tools as tools
from pyforms.web.Controls.ControlBase import ControlBase

class ControlButton(ControlBase):

    def initControl(self): return "controls.push(new ControlButton('%s', '%s','%s'));" % ( self._label, self._name, self.help )

    def pressed(self): 
        """
        This event is called when the button is pressed.
        The correspondent js event is defined in the framework.js file
        """
        self._value()