import pyforms.Utils.tools as tools
from pyforms.web.Controls.ControlBase import ControlBase

class ControlButton(ControlBase):

    def initControl(self): return "new ControlButton('{0}', {1})".format( self._name, str(self.serialize()) )

    def pressed(self): 
        """
        This event is called when the button is pressed.
        The correspondent js event is defined in the framework.js file
        """
        if not isinstance(self._value, (str, unicode)): self._value()

    def serialize(self):
        res = {
            'name':     str(self.__class__.__name__), 
            'label':    str(self._label),
            'help':     str(self._help),
            'visible':  int(self._visible)
        }
        if isinstance(self.value, (str, unicode)) and len(self.value)>0: 
            res.update({'value':self.value})
        else:
            res.update({'value':''})

        return res

    def deserialize(self, properties):
        self._label   = properties.get('label','')
        self._help    = properties.get('help','')
        if properties.get('value',None):
            self.value    = properties.get('value',None)
        self._visible = properties.get('visible',True)