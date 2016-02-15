from pyforms.web.Controls.ControlBase import ControlBase


class ControlSlider(ControlBase):

    _min = 0
    _max = 100

    def __init__(self, label = "", defaultValue = 0, min = 0, max = 100):
        self._updateSlider = True
        self._min = min
        self._max = max
        
        ControlBase.__init__(self, label, defaultValue)
        
    def initControl(self):
        values = self._label, self._name, self._value, self._min, self._max , self.help
        return "new ControlSlider('%s', '%s', %d, %d, %d,'%s')" % values

    def valueChanged(self, value):
        self._updateSlider = False
        self.value = value
        self._updateSlider = True

    def load(self, data):
        if 'value' in data: self.value = data['value']
        
    def changed(self): pass

    def save(self, data):
        if self.value: data['value'] = self.value        

    @property
    def value(self): return self._value

    @value.setter
    def value(self, value): 
        if isinstance(value, int): ControlBase.value.fset(self, value)
        else: ControlBase.value.fset(self, value['position'])
        

    @property
    def min(self): return self._min

    @min.setter
    def min(self, value):  self._min = value

    @property
    def max(self):  return  self._max

    @max.setter
    def max(self, value):  self._max = value