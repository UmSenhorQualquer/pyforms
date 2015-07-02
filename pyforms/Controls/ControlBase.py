# import os
# import pickle
from PyQt4 import uic, QtGui
from PyQt4 import QtCore
import pyforms.Utils.tools as tools


class ControlBase(object):

    _value = None
    _form = None
    _label = None

    def __init__(self, label = "", defaultValue = ""):
        self._value = defaultValue
        self._form = None
        self._parent = 1
        self._label = label
        self._popupMenu = None
        self.initControl()

    def initControl(self):
        control_path = tools.getFileInSameDirectory(__file__,"textInput.ui")
        self._form = uic.loadUi( control_path )
        self.form.label.setText(self._label)
        self.form.lineEdit.setText(self._value)

    def finishEditing(self):
        self.changed()

    def changed(self):
        pass

    def load(self, data):
        if 'value' in data: self.value = data['value']

    def save(self, data):
        if self.value: data['value'] = self.value

    def valueUpdated(self, value):
        pass

    def show(self):
        self.form.show()

    def hide(self):
        self.form.hide()

    def openPopupMenu(self, position):
        if self._popupMenu: self._popupMenu.exec_(self._form.mapToGlobal(position))

    def addPopupSubMenuOption(self, label, options, keys={}):
        if not self._popupMenu:
            self.form.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.form.customContextMenuRequested.connect(self.openPopupMenu)
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


    def addPopupMenuOption(self, label, functionAction = None, key=None):
        if not self._popupMenu:
            self.form.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.form.customContextMenuRequested.connect(self.openPopupMenu)
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

    def aboutToShowContextMenuEvent(self): pass


    def __repr__(self):
        return self.value


    ############################################################################
    ############ Properties ####################################################
    ############################################################################

    @property
    def enabled(self): return self.form.isEnabled()

    @enabled.setter
    def enabled(self, value): self.form.setEnabled(value)

    ############################################################################

    @property
    def value(self): return self._value

    @value.setter
    def value(self, value):
        oldvalue = self._value
        self._value = value
        if oldvalue!=value: self.changed()

    ############################################################################

    @property
    def label(self): return self._label

    @label.setter
    def label(self, value): self._label = value

    ############################################################################

    @property
    def form(self): return self._form

    ############################################################################

    @property
    def parent(self): return self._parent

    @parent.setter
    def parent(self, value): self._parent = value



    @property
    def maxWidth(self): return self.form.maximumWidth()

    @maxWidth.setter
    def maxWidth(self, value): self.form.setMaximumWidth(value)

    @property
    def minWidth(self): return self.form.minimumWidth()

    @minWidth.setter
    def minWidth(self, value): self.form.setMinimumWidth(value)


    @property
    def maxHeight(self): return self.form.MaximumHeight()

    @maxHeight.setter
    def maxHeight(self, value): self.form.setMaximumHeight(value)

    @property
    def minHeight(self): return self.form.minimumHeight()

    @minHeight.setter
    def minHeight(self, value): self.form.setMinimumHeight(value)
