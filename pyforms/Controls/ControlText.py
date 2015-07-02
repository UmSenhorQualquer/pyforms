import pyforms.Utils.tools as tools
from PyQt4 import uic, QtGui
from pyforms.Controls.ControlBase import ControlBase

class ControlText(ControlBase):

    def initControl(self):
        control_path = tools.getFileInSameDirectory(__file__,"textInput.ui")
        self._form = uic.loadUi( control_path )
        self._form.label.setText(self._label)
        self._form.lineEdit.setText(self._value)

        self._form.lineEdit.editingFinished.connect( self.finishEditing )

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
        
        
        
    