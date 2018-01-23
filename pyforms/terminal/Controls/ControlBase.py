import os, pickle,uuid


class ControlBase(object):

    _value          = None
    _label          = None
    _controlHTML    = ""

    def __init__(self, *args, **kwargs):
        self._id = uuid.uuid4()
        self._value = kwargs.get('default', None)
        self._parent = 1
        self._label = kwargs.get('label', args[0] if len(args)>0 else '')

    def init_form(self): pass

    def load_form(self, data, path=None):
        oldvalue = self.value
        self.value = data.get('value', None)
        if oldvalue!=self.value: self.changed_event()

    def changed_event(self):
        """
        Function called when ever the Control value is changed
        """
        return True

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
        if oldvalue!=value: self.changed_event()

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



    