from ControlText import ControlText
import pyforms.Utils.tools as tools
from PyQt4 import uic
from PyQt4 import QtGui

class ControlDir(ControlText):

    def initControl(self):
        control_path = tools.getFileInSameDirectory(__file__,"fileInput.ui")
        self._form = uic.loadUi( control_path )
        self._form.label.setText(self._label)

    def pushButton_clicked(self):
        value = str(QtGui.QFileDialog.getExistingDirectory(self._form, 'Choose a directory', self.value) )
        if value: self.value = value

    @property
    def parent(self): return ControlText.parent.fget(self, value)

    @parent.setter
    def parent(self, value):
        ControlText.parent.fset(self, value)
        self._form.pushButton.clicked.connect(self.pushButton_clicked)
