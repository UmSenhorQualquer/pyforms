#!/usr/bin/python
# -*- coding: utf-8 -*-


import pyforms.utils.tools as tools

from pysettings import conf

from AnyQt.QtWidgets import QLabel, QWidget, QComboBox, QHBoxLayout, QSizePolicy

from pyforms.gui.controls.ControlBase import ControlBase


class ControlCombo(ControlBase, QWidget):
	"""This class represents a wrapper to the combo box"""

	def __init__(self, *args, **kwargs):		
		QWidget.__init__(self)
		ControlBase.__init__(self, *args, **kwargs)
		
	##########################################################################
	############ Functions ###################################################
	##########################################################################

	def init_form(self):

		self._layout = QHBoxLayout()
		self._combo  = QComboBox(self.form)
		
		if self._label is not None:
			self._combolabel = QLabel(self.form)
			self._layout.addWidget( self._combolabel )
			self._combolabel.setAccessibleName('ControlCombo-label')
			self.label = self._label
		else:
			self._combolabel = None

		self._layout.addWidget( self._combo )
		self.form.setLayout( self._layout )


		self._combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		self._layout.setContentsMargins(0,0,0,0)
		self.form.setContentsMargins(0,0,0,0)
		self.form.setMinimumHeight(38)
		self.form.setMaximumHeight(38)
		self.form.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
		
		self._combo.currentIndexChanged.connect(self._currentIndexChanged)
		self._combo.activated.connect(self._activated)
		self._combo.highlighted.connect(self._highlighted)
		self._combo.editTextChanged.connect(self._editTextChanged)
		
		self._items = {}
		self._addingItem = False

		

	def clear(self):
		self._items = {}
		self._value = None
		self._combo.clear()

	def add_item(self, label, value=None):
		self._addingItem = True
		if value is not None:
			if not (value in self._items.values()):
				self._combo.addItem(label)
		else:
			if not (label in self._items.keys()):
				self._combo.addItem(label)

		firstValue = False
		if self._items == {}:
			firstValue = True

		if value is None:
			self._items[str(label)] = label
		else:
			self._items[str(label)] = value
		self._addingItem = False

		if firstValue:
			self.value = self._items[label]

	def __add__(self, val):
		if isinstance(val, tuple):
			self.add_item(val[0], val[1])
		else:
			self.add_item(val)

		return self

	def get_item_index_by_name(self, item_name):
		"""
		Returns the index of the item containing the given name
		:param item_name: item name in combo box
		:type item_name: string
		"""
		return self._combo.findText(item_name)

	def count(self):
		return self._combo.count()

	def show(self):
		"""
		Show the control
		"""
		QWidget.show(self)

	def hide(self):
		"""
		Hide the control
		"""
		QWidget.hide(self)


	##########################################################################
	############ Events ######################################################
	##########################################################################

	def current_index_changed_event(self, index):
		"""Called when the user chooses an item in the combobox and
		the selected choice is different from the last one selected.
		@index: item's index
		"""
		pass

	def activated_event(self, index):
		"""Called when the user chooses an item in the combobox.
		Note that this signal happens even when the choice is not changed
		@index: item's index
		"""
		pass

	def highlighted_event(self, index):
		pass

	def edittext_changed_event(self, text):
		pass

	##########################################################################
	############ PROPERTIES ##################################################
	##########################################################################

	@property
	def form(self):
		return self

	@property
	def current_index(self):
		return self._combo.currentIndex()

	@current_index.setter
	def current_index(self, value):
		self._combo.setCurrentIndex(value)

	@property
	def items(self):
		return self._items.items()

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, value):
		for key, val in self.items:
			if value == val:
				index = self._combo.findText(key)
				self._combo.setCurrentIndex(index)
				if self._value != value:
					self.changed_event()
				self._value = val

	@property
	def text(self):
		return str(self._combo.currentText())

	@text.setter
	def text(self, value):
		for key, val in self.items:
			if value == key:
				self.value = val
				break

	@property
	def label(self):
		if self._combolabel:
			return self._combolabel.text()
		else:
			return None

	@label.setter
	def label(self, value):
		"""
		Label of the control, if applies
		@type  value: string
		"""
		if self._combolabel:
			self._combolabel.setText(value)
		

	##########################################################################
	############ Private functions ###########################################
	##########################################################################

	def _activated(self, index):
		if not self._addingItem:
			item = self._combo.currentText()
			if len(item) >= 1:
				ControlBase.value.fset(self, self._items[str(item)])
				self.activated_event(index)

	def _highlighted(self, index):
		"""Called when an item in the combobox popup
		 list is highlighted by the user.
		 @index: item's index
		"""
		self.highlighted_event(index)

	def _editTextChanged(self, text):
		self.edittext_changed_event(text)

	def _currentIndexChanged(self, index):
		if not self._addingItem:
			item = self._combo.currentText()
			if len(item) >= 1:
				ControlBase.value.fset(self, self._items[str(item)])
				self.current_index_changed_event(index)
