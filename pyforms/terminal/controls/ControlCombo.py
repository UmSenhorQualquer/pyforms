from pyforms.terminal.controls.ControlBase import ControlBase

class ControlCombo(ControlBase):

    def __init__(self, *args, **kwargs):
        super(ControlCombo, self).__init__(*args, **kwargs)
        self._items = None
            
    def add_item(self, label, value = None):
        if self._items==None: self._items={}
        
        first_value = (len(self._items)==0)

        if value==None:
            self._items[label] = label
        else:
            self._items[label] = value
        
        if first_value: self.value = self._items[label]


    def clear(self):
        self._items = {}
        self._value = None
        #self._form.comboBox.clear()

    @property
    def items(self): return self._items.values()

    @property
    def values(self): return self._items.items()

    @property
    def value(self): return self._value

    @value.setter
    def value(self, value):
        for key, val in self._items.items():
            if value == val:
                if self._value!=value:
                    self.changed_event()
                self._value = val

    @property
    def text(self): return "";

    @text.setter
    def text(self, value):
        for key, val in self._items.items():
            if value == key:
                self.value = val
                break
    