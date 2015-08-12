
from pyforms.terminal.Controls.ControlBase import ControlBase

class ControlCheckBox(ControlBase):

    def initControl(self):
        self._items = {}
        self._addingItem = False
        return "controls.push(new ControlCheckBox('%s','%s'));" % (self._label, self._name)

   
    def isChecked(self): return self._value

    def checkedToggle(self, value):  self._value=value

    @property
    def value(self): return self._value

    @value.setter
    def value(self, value): ControlBase.value.fset(self, (value=='True' or value==True) )