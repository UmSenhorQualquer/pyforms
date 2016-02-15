import pyforms.Utils.tools as tools
from PyQt4 import uic, QtGui,QtCore
from pyforms.web.Controls.ControlBase import ControlBase


class ControlBoundingSlider(ControlBase):

    _min = 0
    _max = 100

    def __init__(self, label = "", defaultValue=(0,100) , min = 0, max = 100, horizontal=False, **kwargs):
        self._min = min
        self._max = max
        self._horizontal = horizontal
        ControlBase.__init__(self, label, defaultValue, **kwargs)
        
        
    def initControl(self):
        return "new ControlBoundingSlider('{0}', '{1}', [{2}, {3}], {4}, {5}, '{6}','{7}')".format(
            self._label, self._name, self.value[0], self.value[1], 
            self._min,  self._max , self._horizontal, self.help)


    def _update(self, minval, maxval): self.value = minval, maxval
        
    def valueChanged(self, value): self.value = value

    def load(self, data):
        if 'value' in data: self.value = data['value']

    def save(self, data):
        if self.value: data['value'] = self.value

        

    @property
    def min(self): return self._min

    @min.setter
    def min(self, value):  self._min = value

    @property
    def max(self): return self._max

    @max.setter
    def max(self, value): self._max = value