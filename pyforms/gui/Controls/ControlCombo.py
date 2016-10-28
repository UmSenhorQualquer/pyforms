#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.Controls.ControlCombo """

import pyforms.utils.tools as tools
from PyQt4 import uic
from pyforms.gui.Controls.ControlBase import ControlBase

__author__ = "Ricardo Ribeiro"
__copyright__ = ""
__credits__ = "Ricardo Ribeiro"
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = ["Ricardo Ribeiro", "Carlos Mão de Ferro"]
__email__ = ["ricardojvr at gmail.com", "cajomferro at gmail.com"]
__status__ = "Development"


class ControlCombo(ControlBase):
    """This class represents a wrapper to the combo box"""

    _items = None

    def initForm(self):
        control_path = tools.getFileInSameDirectory(__file__, "comboInput.ui")
        self._form = uic.loadUi(control_path)

        self._form.comboLabel.setAccessibleName('ControlCombo-label')
        self._form.comboBox.currentIndexChanged.connect(self._currentIndexChanged)
        self._form.comboBox.activated.connect(self._activated)
        self._form.comboBox.highlighted.connect(self._highlighted)
        self._form.comboBox.editTextChanged.connect(self._editTextChanged)
        self._form.comboBox._dataChangedFname = None

        self._items = {}
        self._addingItem = False

        self.label = self._label

    def _currentIndexChanged(self, index):
        if not self._addingItem:
            item = self._form.comboBox.currentText()
            if len(item) >= 1:
                ControlBase.value.fset(self, self._items[str(item)])
                self.currentIndexChanged(index)

    def currentIndexChanged(self, index):
        """Called when the user chooses an item in the combobox and
        the selected choice is different from the last one selected.
        @index: item's index
        """
        pass

    def _activated(self, index):
        if not self._addingItem:
            item = self._form.comboBox.currentText()
            if len(item) >= 1:
                ControlBase.value.fset(self, self._items[str(item)])
                self.activated(index)

    def activated(self, index):
        """Called when the user chooses an item in the combobox.
        Note that this signal happens even when the choice is not changed
        @index: item's index
        """
        func_name = self._form.comboBox._dataChangedFname
        if callable(func_name):
                try:
                        func_name()
                except:
                        import sys
                        print sys.exc_info()[0]
        pass

    def _highlighted(self, index):
        """Called when an item in the combobox popup
         list is highlighted by the user.
         @index: item's index
        """
        self.highlighted(index)

    def highlighted(self, index):
        pass

    def _editTextChanged(self, text):
        self.editTextChanged(text)

    def editTextChanged(self, text):
        pass

    def __add__(self, val):
        if isinstance(val, tuple):
            self.addItem(val[0], val[1])
        else:
            self.addItem(val)

        return self

    def addItem(self, label, value=None):
        self._addingItem = True
        if value is not None:
            if not (value in self._items.values()):
                self._form.comboBox.addItem(label)
        else:
            if not (label in self._items.keys()):
                self._form.comboBox.addItem(label)

        firstValue = False
        if self._items == {}:
            firstValue = True

        if value is None:
            self._items[label] = label
        else:
            self._items[label] = value
        self._addingItem = False

        if firstValue:
            self.value = self._items[label]

    def getItemIndexByName(self, item_name):
        """
        Returns the index of the item containing the given name
        :param item_name: item name in combo box
        :type item_name: string
        """
        return self._form.comboBox.findText(item_name)

    def clearItems(self):
        self._items = {}
        self._value = None
        self._form.comboBox.clear()

    def setCurrentIndex(self, index):
        self._form.comboBox.setCurrentIndex(index)

    def currentIndex(self):
        return self._form.comboBox.currentIndex()

    def count(self):
        return self._form.comboBox.count()

    @property
    def items(self): return self._items.items()

    @property
    def value(self): return self._value

    @value.setter
    def value(self, value):
        for key, val in self.items:
            if value == val:
                index = self._form.comboBox.findText(key)
                self._form.comboBox.setCurrentIndex(index)
                if self._value != value:
                    self.changed()
                self._value = val

    @property
    def text(self): return str(self._form.comboBox.currentText())

    @text.setter
    def text(self, value):
        for key, val in self.items:
            if value == key:
                self.value = val
                break

    @property
    def form(self):
        """
        Returns the Widget of the control. 
        This property will be deprecated in a future version.
        """
        return self._form

    @property
    def label(self):
        return self._form.comboLabel.text()

    @label.setter
    def label(self, value):
        """
        Label of the control, if applies
        @type  value: string
        """
        self._form.comboLabel.setText(value)

    @property
    def dataChangedFunction(self): return self._form.comboBox._dataChangedFname

    @dataChangedFunction.setter
    def dataChangedFunction(self, value):
        self._form.comboBox._dataChangedFname = value

