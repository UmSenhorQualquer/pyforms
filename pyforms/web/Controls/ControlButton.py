import pyforms.Utils.tools as tools
from pyforms.web.Controls.ControlBase import ControlBase

class ControlButton(ControlBase):

    def initControl(self): return "new ControlButton('{0}', {1})".format( self._name, str(self.serialize()) )

    def pressed(self): 
        """
        This event is called when the button is pressed.
        The correspondent js event is defined in the framework.js file
        """
        self._value()

    def serialize(self):
        return { 
            'name':     self.__class__.__name__, 
            'label':    self._label,
            'help':     self._help,
            'visible':  int(self._visible)
        }

    def deserialize(self, properties):
        self._label   = properties.get('label','')
        self._help    = properties.get('help','')
        self._visible = properties.get('visible',True)