import os, pickle,uuid


class ControlBase(object):

    _value          = None
    _label          = None
    _controlHTML    = ""

    def __init__(self, label = "", defaultValue = "", helptext=None):
        self._name = ""
        self._id = uuid.uuid4()
        self._value = defaultValue
        self._parent = 1
        self._label = label
        self._popupMenu = None
        self._controlHTML  = ""


    def initControl(self):
        self._controlHTML = "<div id='id%s' ><input type='text' id='%s' /></div>" % ( self._id, self._name )
        return self._controlHTML

    def finishEditing(self): self.updateControl()

    def updateControl(self): pass

    def load(self, data):
        if 'value' in data: self.value = data['value']

    def save(self, data):
        if self.value: data['value'] = self.value

    def valueUpdated(self, value): pass

    def show(self):pass

    def hide(self):pass

    def openPopupMenu(self, position): pass
        

    def addPopupSubMenuOption(self, label, options): pass
        

    def addPopupMenuOption(self, label, functionAction = None): pass

    def __repr__(self):
        return self.value
    ############################################################################
    ############ Properties ####################################################
    ############################################################################

    @property
    def enabled(self): return True

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
    def form(self): return None

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


    def __str__(self): return "<span id='place%s' />" % self._name