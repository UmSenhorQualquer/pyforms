#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


import pyforms.utils.tools as tools
from PyQt4 import uic, QtGui, QtCore
from pyforms.gui.Controls.ControlBase import ControlBase

class ControlCheckBoxList(ControlBase):

	def init_form(self):
		control_path = tools.getFileInSameDirectory(__file__,"tree.ui")
		self._form = uic.loadUi( control_path )

		self._form.label.setText(self._label)

		self._form.listWidget.itemChanged.connect(self.item_changed)

		self._form.listWidget.itemSelectionChanged.connect(self.__itemSelectionChanged)

		if self.help: self.form.setToolTip(self.help)

	def item_changed(self, item):
		self.changed_event()

	def __add__(self, val):
		if isinstance( val, (tuple, list) ):
			item=QtGui.QListWidgetItem(str(val[0]))
			item.value = val[0]
			if val[1]: 
				item.setCheckState( QtCore.Qt.Checked)
			else: 
				item.setCheckState( QtCore.Qt.Unchecked)
		else:
			item=QtGui.QListWidgetItem(str(val))
			item.value = val
		
		self._form.listWidget.addItem(item)        
		return self

	def __sub__(self, other):
		if isinstance(other, int):
			if other < 0:
				indexToRemove = self._form.listWidget.currentRow()
			else:
				indexToRemove = other
			self._form.listWidget.takeItem(indexToRemove)
		else:
			for row in range( self.count ):
				item = self._form.listWidget.item(row)
				if item!=None and hasattr(item, 'value') and item.value==other:
					self._form.listWidget.takeItem(row)
		return self

	def clear(self): self._form.listWidget.clear()

	def refresh(self):
		for row in range( self.count ):
			item = self._form.listWidget.item(row)
			if hasattr(item, 'value'): item.setText(str(item.value))

	############################################################################
	############ Events ########################################################
	############################################################################

	def __itemSelectionChanged(self): self.selection_changed_event()

	def selection_changed_event(self): pass

		

	############################################################################
	############ Properties ####################################################
	############################################################################

	@property
	def count(self): return self._form.listWidget.count()

	@property
	def checked_indexes(self): 
		results = []
		for row in range( self.count ):
			item = self._form.listWidget.item(row)
			if item!=None and item.checkState()==QtCore.Qt.Checked : results.append( row )
		return results

	@property
	def value(self):
		results = []
		for row in range( self.count ):
			item = self._form.listWidget.item(row)
			if item!=None and item.checkState()==QtCore.Qt.Checked : 
				results.append( item.value if hasattr(item, 'value') else str(item.text()) )
		return results
	
	@value.setter
	def value(self, value): 
		for row in value: self += row


	@property
	def selected_row_index(self):
		return self.form.listWidget.currentRow()


	@property
	def items(self):
		results = []
		for row in range( self.count ):
			item = self._form.listWidget.item(row)
			results.append( [item.value if hasattr(item, 'value') else str(item.text()),  item.checkState()==QtCore.Qt.Checked] )
		return results
	
			
		
