from pyforms.terminal.Controls.ControlBase import ControlBase

class ControlText(ControlBase):

    def initControl(self):
        #return """<label for="id%s">%s</label><input type='text' name='%s' id='id%s' />""" % ( self._name,  self._label, self._name, self._name, )
        return "controls.push(new ControlText('%s','%s'));" % (self._label, self._name)
     

    ############################################################################
    ############ Properties ####################################################
    ############################################################################

    @property
    def value(self): return self._value

    @value.setter
    def value(self, value):
        ControlBase.value.fset(self,value)
        
        
    