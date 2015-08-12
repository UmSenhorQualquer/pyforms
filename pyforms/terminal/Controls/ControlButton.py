from pyforms.terminal.Controls.ControlBase import ControlBase

class ControlButton(ControlBase):

    def initControl(self): return "controls.push(new ControlButton('%s', '%s'));" % ( self._label, self._name )


    def load(self, data):
        pass

    def save(self, data):
        pass

    def pressed(self): self._value()

    ############################################################################

    @property
    def label(self): return ControlBase.lable.fget(self)

    @label.setter
    def label(self, value):  ControlBase.label.fset(self, value)

    ############################################################################
    
    @property
    def value(self): return None

    @value.setter
    def value(self, value):  self._value = value
        
