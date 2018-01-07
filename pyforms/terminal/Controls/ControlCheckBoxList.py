from pyforms.terminal.Controls.ControlBase import ControlBase

class ControlCheckBoxList(ControlBase):

    def __init__(self, *args, **kwargs):
        if 'default' not in kwargs: kwargs['default'] = []
        super(ControlCheckBoxList, self).__init__(*args, **kwargs)


        
    def __add__(self, val):
        self._value.append(val)
        return self

    def __sub__(self, other):
        self._value.remove(other)
        return self