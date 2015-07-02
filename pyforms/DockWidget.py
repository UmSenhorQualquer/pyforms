from Controls.ControlBase import ControlBase
from datetime import datetime, timedelta
from PyQt4 import uic, QtGui, QtCore
import time, subprocess, os

class DockWidget(QtGui.QDockWidget):

    _formset = None
    _splitters = None
    _tabs = None

    def __init__(self, title):
        QtGui.QWidget.__init__(self)
        layout = QtGui.QVBoxLayout(); self.setLayout(layout)
        
        self._splitters = []
        self._tabs = []

        self._title = title
        self.setWindowTitle(title)

        self._formLoaded = False
        layout.setMargin(0)
        layout.setSpacing(0)

        


    ############################################################################
    ############ Module functions  #############################################
    ############################################################################

    def initForm(self):
        """
        Generate the module Form
        """
        if not self._formLoaded:
            
            if self._formset != None:
                control = self.generatePanel(self._formset)
                self.layout().addWidget( control )
            else:
                allparams = self.formControls
                for param in allparams.values():
                    param.parent = self
                    self.layout().addWidget( param.form )
            self._formLoaded = True

    def generateTabs(self, formsetDict):
        """
        Generate QTabWidget for the module form
        @param formset: Tab form configuration
        @type formset: dict
        """
        tabs = QtGui.QTabWidget(self)
        for key, item in formsetDict.items():
            ctrl = self.generatePanel(item)
            tabs.addTab(ctrl, key)
        return tabs

    def generatePanel(self, formset):
        """
        Generate a panel for the module form with all the controls
        formset format example: [('_video', '_arenas', '_run'), {"Player":['_threshold', "_player", "=", "_results", "_query"], "Background image":[(' ', '_selectBackground', '_paintBackground'), '_image']}, "_progress"]
        tuple: will display the controls in the same horizontal line
        list: will display the controls in the same vertical line
        dict: will display the controls in a tab widget
        '||': will plit the controls in a horizontal line
        '=': will plit the controls in a vertical line
        @param formset: Form configuration
        @type formset: list
        """
        control = None
        if '=' in formset:
            control = QtGui.QSplitter(QtCore.Qt.Vertical)
            tmp = list( formset )
            index = tmp.index('=')
            firstPanel = self.generatePanel(formset[0:index])
            secondPanel = self.generatePanel(formset[index+1:])
            control.addWidget(firstPanel)
            control.addWidget(secondPanel)
            self._splitters.append( control )
            return control
        elif '||' in formset:
            control = QtGui.QSplitter(QtCore.Qt.Horizontal)
            tmp = list( formset )
            rindex=lindex=index = tmp.index('||'); rindex-=1; rindex+=2
            if isinstance(formset[lindex-1], int): lindex = lindex-1
            if len(formset)>rindex and isinstance(formset[index+1], int): rindex += 1
            firstPanel = self.generatePanel(formset[0:lindex])
            secondPanel = self.generatePanel(formset[rindex:])
            if isinstance(formset[index-1], int): firstPanel.setMaximumWidth( formset[index-1] )
            if isinstance(formset[index+1], int): secondPanel.setMaximumWidth( formset[index+1] )
            control.addWidget(firstPanel)
            control.addWidget(secondPanel)
            self._splitters.append( control )
            return control
        control = QtGui.QWidget()
        layout = None
        if type(formset) is tuple:
            layout = QtGui.QHBoxLayout()
            for row in formset:
                if isinstance(row, (list, tuple)):
                    panel = self.generatePanel( row )
                    layout.addWidget( panel )
                elif row == " ":
                    spacer = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
                    layout.addItem( spacer )
                elif type(row) is dict:
                    c = self.generateTabs(row)
                    layout.addWidget( c )
                    self._tabs.append(c)
                else:
                    param = self.formControls[row]
                    param.parent = self
                    layout.addWidget( param.form )
        elif type(formset) is list:
            layout = QtGui.QVBoxLayout()
            for row in formset:
                if isinstance(row, (list, tuple)):
                    panel = self.generatePanel( row )
                    layout.addWidget( panel )
                elif row == " ":
                    spacer = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
                    layout.addItem( spacer )
                elif type(row) is dict:
                    c = self.generateTabs(row)
                    layout.addWidget( c )
                    self._tabs.append(c)
                else:
                    param = self.formControls[row]
                    param.parent = self
                    layout.addWidget( param.form )
        layout.setMargin(0)
        control.setLayout(layout)
        return control

    ############################################################################
    ############ Parent class functions reemplementation #######################
    ############################################################################

    def show(self):
        """
        OTModuleProjectItem.show reimplementation
        """
        self.initForm()
        super(DockWidget, self).show()

    ############################################################################
    ############ Properties ####################################################
    ############################################################################
    
    @property
    def formControls(self):
        """
        Return all the form controls from the the module
        """
        result = {}
        for name, var in vars(self).items():
            if isinstance(var, ControlBase): result[name] = var
        return result

  