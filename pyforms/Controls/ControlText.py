import pyforms.Utils.tools as tools
from PyQt4 import uic, QtGui
from pyforms.Controls.ControlBase import ControlBase

class ControlText(ControlBase):

    def initControl(self):
        super(ControlText, self).initControl()
        self.form.lineEdit.editingFinished.connect( self.finishEditing )


    def finishEditing(self): 
        """Function called when the lineEdit widget is edited"""
        self.changed()

       
    ############################################################################
    ############ Properties ####################################################
    ############################################################################

    @property
    def value(self): 
        self._value = str(self._form.lineEdit.text())
        return self._value

    @value.setter
    def value(self, value):
        self._form.lineEdit.setText(value)
        ControlBase.value.fset(self,value)
        
        
        
    