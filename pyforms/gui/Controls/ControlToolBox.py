from PyQt4 import uic, QtGui
from pyforms.gui.Controls.ControlBase import ControlBase

class ControlToolBox(ControlBase):

    def initForm(self):
        self._form = QtGui.QToolBox()
        self.form.layout().setMargin(0)
        
    
    @property
    def value(self): return self._value

    @value.setter
    def value(self, value): 
        ControlBase.label.fset(self, value);

        for item in range(self.form.count(),-1, -1): self.form.removeItem(item)
        
        for item in value: 
            if isinstance(item, tuple):
                widget = QtGui.QWidget(self.form); layout = QtGui.QVBoxLayout(); 
                layout.setMargin(0); widget.setLayout( layout )

                for e in item[1]:
                    if isinstance(e, tuple):
                        hwidget = QtGui.QWidget(self.form); hlayout = QtGui.QHBoxLayout(); 
                        hlayout.setMargin(0); hwidget.setLayout( hlayout )
                        for ee in e: hlayout.addWidget( ee.form )
                        widget.layout().addWidget( hwidget )
                    else:
                        widget.layout().addWidget( e.form )
                self.form.addItem(widget, item[0])
            else:
                self.form.addItem(item.form, item.label)


