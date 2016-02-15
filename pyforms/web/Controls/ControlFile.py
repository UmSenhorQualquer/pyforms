from pyforms.web.Controls.ControlBase import ControlBase

class ControlFile(ControlBase):

    def initControl(self):
    	values = ( self._label, self._name, self._value, self.help )
        return "new ControlFile('%s', '%s', '%s', '%s')" % values