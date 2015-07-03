from PyQt4 import uic, QtGui, QtCore
import pyforms.Utils.tools as tools


class ControlBase(object):
    """
    Implements a base control
    The control has a lineEdit widget
    """

    def __init__(self, label = "", defaultValue = ""):
        self._value     = defaultValue
        self._form      = None  #Qt widget
        self._parent    = None  #Parent window
        self._label     = label #Label
        self._popupMenu = None

        self.initControl()

    def initControl(self):
        """
        Load Control and initiate the events
        """
        control_path = tools.getFileInSameDirectory(__file__,"textInput.ui")
        self._form = uic.loadUi( control_path )
        self.form.label.setText(self._label)
        self.form.lineEdit.setText(self._value)

        self.form.lineEdit.editingFinished.connect( self.finishEditing )

    def __repr__(self): return self.value

    ############################################################################
    ############ Funcions ######################################################
    ############################################################################

    def load(self, data):
        """
        Load a value from the dict variable
        @param data: dictionary with the value of the Control
        """
        if 'value' in data: self.value = data['value']

    def save(self, data): 
        """
        Save a value to dict variable
        @param data: dictionary with to where the value of the Control will be added
        """
        if self.value: data['value'] = self.value

    def show(self): 
        """
        Show the control
        """
        self.form.show()

    def hide(self): 
        """
        Hide the control
        """
        self.form.hide()

    


    def addPopupMenuOption(self, label, functionAction=None, key=None):
        """
        Add an option to the Control popup menu
        @param label:           label of the option.
        @param functionAction:  function called when the option is selected.
        @param key:             shortcut key
        """
        if not self._popupMenu:
            self.form.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.form.customContextMenuRequested.connect(self.__openPopupMenu)
            self._popupMenu = QtGui.QMenu()
            self._popupMenu.aboutToShow.connect(self.aboutToShowContextMenuEvent)

        if label=="-":
            return self._popupMenu.addSeparator()
        else:
            action = QtGui.QAction(label, self.form)
            if key!=None: action.setShortcut(QtGui.QKeySequence(key))
            if functionAction:
                action.triggered.connect(functionAction)
                self._popupMenu.addAction(action)
            return action


    def addPopupSubMenuOption(self, label, options, keys={}):
        """
        Add submenu options to the Control popup menu
        @param label:   submenu label of the option.
        @param options: dictionary representing the submenu. ex: { 'Example': event function, ... }. 
        @param keys:    shortcut keys. ex: { 'Example': shortcut key, ... }. 
        """
        if not self._popupMenu:
            self.form.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.form.customContextMenuRequested.connect(self.__openPopupMenu)
            self._popupMenu = QtGui.QMenu()
            self._popupMenu.aboutToShow.connect(self.aboutToShowContextMenuEvent)

        submenu = QtGui.QMenu(label, self._popupMenu)
        for text, func in options.items():
            if text=="-":
                submenu.addSeparator()
            else:
                action = QtGui.QAction(text, self.form)
                if text in keys: action.setShortcut(QtGui.QKeySequence(keys[text]))

                if func:
                    action.triggered.connect(func)
                    submenu.addAction(action)
        self._popupMenu.addMenu(submenu)







    ############################################################################
    ############ Events ########################################################
    ############################################################################

    
    def changed(self): 
        """
        Function called when ever the Control value is changed
        """
        pass

    def aboutToShowContextMenuEvent(self): 
        """
        Function called before open the Control popup menu
        """
        pass


    def __openPopupMenu(self, position):
        if self._popupMenu: self._popupMenu.exec_(self._form.mapToGlobal(position))







    ############################################################################
    ############ Properties ####################################################
    ############################################################################

    ############################################################################
    # Set the Control enabled or disabled

    @property
    def enabled(self): return self.form.isEnabled()

    @enabled.setter
    def enabled(self, value): self.form.setEnabled(value)

    ############################################################################
    # Return or update the value of the Control

    @property
    def value(self): return self._value

    @value.setter
    def value(self, value):
        oldvalue = self._value
        self._value = value
        if oldvalue!=value: self.changed()

    ############################################################################
    # Return or update the label of the Control 

    @property
    def label(self): return self._label

    @label.setter
    def label(self, value): self._label = value

    ############################################################################
    # Return the QT widget

    @property
    def form(self): return self._form

    ############################################################################
    # Parent window

    @property
    def parent(self): return self._parent

    @parent.setter
    def parent(self, value): self._parent = value

    ############################################################################
    # Return or define the max Width

    @property
    def maxWidth(self): return self.form.maximumWidth()

    @maxWidth.setter
    def maxWidth(self, value): self.form.setMaximumWidth(value)

    ############################################################################
    # Return or define the min Width

    @property
    def minWidth(self): return self.form.minimumWidth()

    @minWidth.setter
    def minWidth(self, value): self.form.setMinimumWidth(value)

    ############################################################################
    # Return or define the max Height

    @property
    def maxHeight(self): return self.form.MaximumHeight()

    @maxHeight.setter
    def maxHeight(self, value): self.form.setMaximumHeight(value)

    ############################################################################
    # Return or define the min Height

    @property
    def minHeight(self): return self.form.minimumHeight()

    @minHeight.setter
    def minHeight(self, value): self.form.setMinimumHeight(value)
