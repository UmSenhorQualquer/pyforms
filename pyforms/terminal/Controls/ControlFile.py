from pyforms.terminal.Controls.ControlBase import ControlBase

class ControlFile(ControlBase):

    def initControl(self): return "controls.push(new ControlFile('%s', '%s'));" % ( self._label, self._name )


    def load(self, data):
        pass

    def save(self, data):
        pass

    ############################################################################

    @property
    def label(self): return ControlBase.label.fget(self)

    @label.setter
    def label(self, value):  ControlBase.label.fset(self, value)

    ############################################################################
    
    @property
    def value(self): return self._value

    @value.setter
    def value(self, value): self._value = value
