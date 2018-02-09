from pyforms.terminal.controls.ControlBase import ControlBase

class ControlButton(ControlBase):

    def __init__(self, *args, **kwargs):
        super(ControlButton, self).__init__(*args, **kwargs)
        self.checked = False

    @property
    def value(self): return None

    @value.setter
    def value(self, value):  self._value = value
        


    