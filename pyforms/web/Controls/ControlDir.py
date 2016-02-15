from pyforms.web.Controls.ControlBase import ControlBase

class ControlDir(ControlBase):

    def initControl(self):
    	values = ( self._label, self._name, self._value, self.help )
        return "new ControlDir('%s', '%s', '%s', '%s')" % values