from pyforms.terminal.Controls.ControlBase import ControlBase

class ControlEmptyWidget(ControlBase):
        

    def load_form(self, data, path=None):
        if 'value' in data and self.value is not None and self.value != '':
            self.value.load_form(data['value'], path)