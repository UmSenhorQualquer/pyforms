from pyforms.terminal.Controls.ControlBase import ControlBase

class ControlCombo(ControlBase):

    _items = None

    def initControl(self):
        self._items = {}
        self._addingItem = False
        return "controls.push(new ControlCombo('%s','%s', []));" % (self._label, self._name)

    def currentIndexChanged(self, index):
        #if not self._addingItem:
            #item = self._form.comboBox.currentText()
        #    if len(item)>=1: OTControlBase.value.fset(self, self._items[str(item)])
        return 0
            
    def addItem(self, label, value = None):
        if self._items==None: self._items={}
        self._addingItem = True
        #if not (label in self._items.keys()):
        #    self._form.comboBox.addItem( label )

        firstValue = False
        if self._items=={}: firstValue = True

        if value==None:
            self._items[label] = label
        else:
            self._items[label] = value
        self._addingItem = False

        if firstValue: self.value = self._items[label]


    def clearItems(self):
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
                if self._value!=value: self.value_updated(value)
                self._value = val

    @property
    def text(self): return "";#str(self._form.comboBox.currentText())

    @text.setter
    def text(self, value):
        for key, val in self._items.items():
            if value == key:
                self.value = val
                break
    