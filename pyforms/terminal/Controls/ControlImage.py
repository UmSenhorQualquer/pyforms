from pyforms.terminal.Controls.ControlBase import ControlBase

class ControlImage(ControlBase):

    _filename = ''

    def initControl(self): pass
        
    def save(self, data):
        if self.value!=None: data['value'] = self._value

    def load(self, data):
        if 'value' in data: self.value = data['value']

    def repaint(self): pass

    @property
    def value(self): pass

    @value.setter
    def value(self, value): pass
