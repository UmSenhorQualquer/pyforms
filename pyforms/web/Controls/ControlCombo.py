from pyforms.web.Controls.ControlBase import ControlBase

class ControlCombo(ControlBase):


    def __init__(self, label = "", defaultValue = "", helptext=''):
        super(ControlCombo, self).__init__(label, defaultValue,helptext)
        self._items = {}

    def initControl(self): return "new ControlCombo('{0}', {1})".format( self._name, str(self.serialize()) )

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

    def __add__(self, val):
        if isinstance( val, tuple ):
            self.addItem(val[0], val[1])
        else:
            self.addItem(val)
        
        return self


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
            print "----", value, val
            if value == val:
                print "----", val
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
    

    def serialize(self):
        data = ControlBase.serialize(self)
        items = []
        for key, value in self._items.items():
            items.append({'label': key, 'value': value}) 

        data.update({ 'items': items, 'value': self._value })
        return data
        
    def deserialize(self, properties):
        ControlBase.deserialize(self,properties)
        self._items = {}

        for item in properties['items']:
            self.addItem(item['label'], item['value'])

        self.value = properties['value']

