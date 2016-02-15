from pyforms.web.Controls.ControlBase import ControlBase

class ControlCombo(ControlBase):


    def __init__(self, label = "", defaultValue = "", helptext=None):
        super(ControlCombo, self).__init__(label, defaultValue,helptext)
        self._items = {}

    def initControl(self):
        if self._items==None: self._items={}
        self._addingItem = False
        values = [list(x) for x in sorted(self._items.items(), key=lambda x: x[1]) ]
        for v in values:
            if v[1]==self._value: 
                values.remove(v)
                values.insert(0, v)

        return "new ControlCombo('%s','%s', %s,'%s')" % (self._label, self._name, values ,self.help )

    def currentIndexChanged(self, index):
        if not self._addingItem:
            if len(item)>=1: 
                OTControlBase.value.fset(self, self._items[str(item)])
            
    def addItem(self, label, value = None):
        if self._items==None: self._items={}
        self._addingItem = True
        
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
                if self._value!=value: self.valueUpdated(value)
                self._value = val

    @property
    def text(self): return ""

    @text.setter
    def text(self, value):
        for key, val in self._items.items():
            if value == key:
                self.value = val
                break
    