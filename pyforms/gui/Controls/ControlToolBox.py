from PyQt4 import uic, QtGui
from pyforms.gui.Controls.ControlBase import ControlBase

class ControlToolBox(ControlBase):

    def initForm(self):
        self._form = QtGui.QToolBox()
        #self._form.setStyleSheet("""font-width: bold;border-radius: 3px;""")
        #self._form.setStyleSheet("""QWidget{background-color:black;}""")
        self.form.layout().setMargin(0)
        try:
            self.loadStyleSheetFile('style.css')
        except:pass
        
    
    @property
    def value(self): return self._value

    @value.setter
    def value(self, value): 
        ControlBase.label.fset(self, value);

        for item in range(self.form.count(),-1, -1): self.form.removeItem(item)
        
        for item in value: 
            if isinstance(item, tuple):
                widget = QtGui.QWidget(); 
                layout = QtGui.QVBoxLayout(); 
                layout.setMargin(0); 
                widget.setLayout( layout )
                for e in item[1:]: widget.layout().addWidget( e.form )
                self.form.addItem(widget, item[0])
            else:
                self.form.addItem(item.form, item.label)


