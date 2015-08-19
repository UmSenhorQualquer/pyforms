from pyforms.gui.Controls.ControlEmptyWidget import ControlEmptyWidget


class ControlDockWidget(ControlEmptyWidget):

    SIDE_LEFT = 'left'
    SIDE_RIGHT = 'right'
    SIDE_TOP = 'top'
    SIDE_BOTTOM = 'bottom'
    SIDE_DETACHED = 'detached'

    def __init__(self, label='', default=None, side='left'):
        super(ControlDockWidget, self).__init__(label)
        self.side = side
        if default is not None:
            self.value = default

    @property
    def label(self): return self._label

    @label.setter
    def label(self, value):
        self._label = value
        self.dock.setWindowTitle(value)

    def save(self, data):
        data['side'] = self.side
        super(ControlDockWidget, self).save(data)

    def load(self, data):
        self.side = data['side']
        # print(data)
        super(ControlDockWidget, self).load(data)

    def show(self):
        """
        Show the control
        """
        self.dock.show()

    def hide(self):
        """
        Hide the control
        """
        self.dock.hide()