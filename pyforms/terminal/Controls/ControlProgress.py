from pyforms.terminal.Controls.ControlBase import ControlBase

class ControlProgress(ControlBase):

    _min = 0
    _max = 100

    def __init__(self, label = "%p%", defaultValue = 0, min = 0, max = 100, helptext=None):
        self._updateSlider = True
        self._min = min
        self._max = max
        ControlBase.__init__(self, label, defaultValue)
        
        
    def initControl(self):
        #return """<div id='id%s' class='progressbar' ></div>""" %  ( self._name )
        return "controls.push(new ControlProgress('"+self._name+"'));"

    @property
    def value(self): return self._value

    @value.setter
    def value(self, value): self._form.horizontalSlider.setValue( value )

    @property
    def min(self): return self._form.horizontalSlider.minimum()

    @min.setter
    def min(self, value): self._form.horizontalSlider.setMinimum(value)

    @property
    def max(self): return self._form.horizontalSlider.maximum()

    @max.setter
    def max(self, value): self._form.horizontalSlider.setMaximum(value)
        