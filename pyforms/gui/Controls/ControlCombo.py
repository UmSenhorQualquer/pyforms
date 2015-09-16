#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.Controls.ControlCombo """

import pyforms.Utils.tools as tools
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
        self._form.label.setText(self._label)
        self._form.comboBox.currentIndexChanged.connect(
            self._currentIndexChanged)
        self._form.comboBox.activated.connect(
            self._activated)
        self._form.comboBox.highlighted.connect(
            self._highlighted)

        self._items = {}

        self._addingItem = False

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
        self.activated(index)

    def activated(self, index):
        """Called when the user chooses an item in the combobox.
        Note that this signal happens even when the choice is not changed
        @index: item's index
        """
        pass

    def _highlighted(self, index):
        """Called when an item in the combobox popup
         list is highlighted by the user.
         @index: item's index
        """
        self.highlighted(index)

    def highlighted(self, index):
        pass

    def addItem(self, label, value=None):
        self._addingItem = True
        if value!=None:
            if not (value in self._items.values()): self._form.comboBox.addItem(label)
        else:
            if not (label in self._items.keys()): self._form.comboBox.addItem(label)

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
