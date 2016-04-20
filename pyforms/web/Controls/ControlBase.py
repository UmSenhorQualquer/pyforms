import uuid

class ControlBase(object):

    _value = None
    _label = None
    _controlHTML = ""

    def __init__(self, label = "", defaultValue = "", helptext=''):
        self._name      = ""
        self._help      = helptext
        self._value     = defaultValue
        self._parent    = None
        self._label     = label
        self._visible   = True
        self._popupMenu = None
        self._id = uuid.uuid4()
        self._controlHTML = ""


    def initControl(self):
        self._controlHTML = "<div id='id{0}' ><input type='text' id='{1}' /></div>".format( self._id, self._name )
        return self._controlHTML

    def serialize(self):
        return { 
            'name':     self.__class__.__name__, 
            'value':    str(self.value),
            'label':    self._label if self._label else '',
            'help':     self._help if self._help else '',
            'visible':  int(self._visible)
        }

    def deserialize(self, properties):
        self.value    = properties.get('value',None)
        self._label   = properties.get('label','')
        self._help    = properties.get('help','')
        self._visible = properties.get('visible',True)

    def finishEditing(self): self.updateControl()

    def updateControl(self): pass

    def changed(self): pass

    def load(self, data):
        if 'value' in data: self.value = data['value']

    def save(self, data):
        if self.value: data['value'] = self.value

    def valueUpdated(self, value): pass

    def show(self): pass

    def hide(self): pass

    def openPopupMenu(self, position): pass

    def addPopupSubMenuOption(self, label, options): pass

    def addPopupMenuOption(self, label, functionAction = None): pass

    def __repr__(self): return self.value

    ############################################################################
    ############ Properties ####################################################
    ############################################################################
    
    @property
    def help(self): return self._help.replace('\n', '&#013;') if self._help else ''

    @property
    def enabled(self): pass

    @enabled.setter
    def enabled(self, value): pass

    ############################################################################

    @property
    def value(self): return self._value

    @value.setter
    def value(self, value):
        oldvalue = self._value
        self._value = value
        if oldvalue!=value: self.valueUpdated(value)

    ############################################################################

    @property
    def label(self): return self._label

    @label.setter
    def label(self, value): self._label = value

    ############################################################################

    @property
    def parent(self): return self._parent

    @parent.setter
    def parent(self, value): self._parent = value



    @property
    def maxWidth(self): return -1

    @maxWidth.setter
    def maxWidth(self, value): pass

    @property
    def minWidth(self): return -1

    @minWidth.setter
    def minWidth(self, value): pass


    @property
    def maxHeight(self): return -1

    @maxHeight.setter
    def maxHeight(self, value): pass

    @property
    def minHeight(self): return -1

    @minHeight.setter
    def minHeight(self, value): pass

    def __str__(self): return "<span id='place-{0}-{1}' />".format(self.parent._id, self._name)



    #### Variable connected to the Storage manager of the corrent user
    @property
    def storage(self): return self._storage

    @storage.setter
    def storage(self, value): self._storage = value
    #######################################################

    #### This variable has the current http request #######
    @property
    def httpRequest(self): return self._httpRequest

    @httpRequest.setter
    def httpRequest(self, value): self._httpRequest = value
    #######################################################