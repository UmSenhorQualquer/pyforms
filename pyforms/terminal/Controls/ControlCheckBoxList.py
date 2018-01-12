from pyforms.terminal.Controls.ControlBase import ControlBase

class ControlCheckBoxList(ControlBase):

    def __init__(self, *args, **kwargs):
        if 'default' not in kwargs: kwargs['default'] = []
        super(ControlCheckBoxList, self).__init__(*args, **kwargs)

    def clear(self):
        self._value = []
        
    def __add__(self, val):
        self._value.append(val)
        return self

    def __sub__(self, other):
        self._value.remove(other)
        return self

    def load_form(self, data, path=None):
        results = data['selected']
        for row in range(self.count):
            item = self._value[row][0]
            if item != None and  str(item) in results:
                self._value[row] = [item, True]
            else:
                self._value[row] = [item, False]
        self.changed_event()

    @property
    def count(self):
        return len(self._value)

    @property
    def selected_row_index(self):
        return -1

    @property
    def value(self):
        results = []
        for item, checked in self._value:
            if checked:
                results.append(item)
        return results

    @value.setter
    def value(self, value):
        self.clear()
        for row in value: self += row
        self.changed_event()

    @property
    def items(self):
        for item, checked in self._value:
            yield (item, checked)