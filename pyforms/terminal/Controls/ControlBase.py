import os, pickle,uuid


class ControlBase(object):

    _value          = None
    _label          = None
    _controlHTML    = ""

    def __init__(self, label = "", defaultValue = "", helptext=None):
        self._id = uuid.uuid4()
        self._value = defaultValue
        self._parent = 1
        self._label = label

    def init_form(self): pass

    def load_form(self, data, path=None):
        if 'value' in data: self.value = data['value']

    def save_form(self, data, path=None):
        if self.value: data['value'] = self.value

    def value_updated(self, value): pass

    def show(self):pass

    def hide(self):pass

    def open_popup_menu(self, position): pass
        

    def add_popup_submenu_option(self, label, options): pass
        

    def add_popup_menu_option(self, label, functionAction = None): pass

    def __repr__(self): return self.value
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
        if oldvalue!=value: self.value_updated(value)

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
