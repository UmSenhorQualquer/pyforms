# !/usr/bin/python
# -*- coding: utf-8 -*-

""""pyforms.gui.Controls.Control Tree"""

from pyforms.gui.Controls.ControlBase import ControlBase
from PyQt4.QtGui import QTreeWidget, QTreeWidgetItem, QTreeView, QStandardItem
from PyQt4.QtGui import QAbstractItemView
from PyQt4.QtCore import QSize
from PyQt4 import QtGui

__author__ = "Ricardo Ribeiro"
__copyright__ = ""
__credits__ = "Ricardo Ribeiro"
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = ["Ricardo Ribeiro", "Carlos Mão de Ferro"]
__email__ = ["ricardojvr at gmail.com", "cajomferro at gmail.com"]
__status__ = "Development"


class ControlTree(ControlBase, QTreeWidget):

	"""This class represents a wrapper to the QTreeWidget"""

	def __init__(self, label='', default=''):
		QTreeWidget.__init__(self)
		ControlBase.__init__(self, label, default)

	def init_form(self):
		self.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.setUniformRowHeights(True)
		self.setDragDropMode(QAbstractItemView.NoDragDrop)
		self.setDragEnabled(False)
		self.setAcceptDrops(False)

		self.model().dataChanged.connect(self.__itemChangedEvent)
		self.itemDoubleClicked.connect(self.__itemDoubleClicked)

		self.selectionChanged = self.selectionChanged
		self._items = {}

	def __repr__(self): return QTreeWidget.__repr__(self)

	##########################################################################
	############ FUNCTIONS ###################################################
	##########################################################################

	def __add__(self, other):
		if isinstance(other, QTreeWidgetItem):
			self.invisibleRootItem().addChild(other)
		elif isinstance(other, str):
			item = QTreeWidgetItem(other)
			self.invisibleRootItem().addChild(item)
		elif isinstance(other, list):
			for x in other:
				if isinstance(x, str):
					item = QTreeWidgetItem(x)
					self.invisibleRootItem().addChild(item)
				else:
					self.invisibleRootItem().addChild(x)
		else:
			item = QTreeWidgetItem(other)
			self.invisibleRootItem().addChild(item)

		#self.setFirstColumnSpanned( self.model().rowCount() - 1, self.rootIndex(), True)
		return self

	def __sub__(self, other):
		if isinstance(other, int):
			if other < 0:
				indexToRemove = self.selected_row_index
			else:
				indexToRemove = other
			self.model().removeRow(indexToRemove)
		else:
			try:
				self.invisibleRootItem().removeChild(other)
			except: pass
		return self

	def save_form(self, data, path=None): pass

	def load_form(self, data, path=None): pass

	

	def add_popup_menu_option(self, label='', function_action=None, key=None, item=None, icon=None):
		"""
		Add an option to the Control popup menu
		@param label:           label of the option.
		@param functionAction:  function called when the option is selected.
		@param key:             shortcut key
		@param key:             shortcut key
		"""
		action = super(ControlTree, self).add_popup_menu_option(
			label, functionAction, key)

		if item is not None:
			action = QtGui.QAction(label, self.form)
			if icon is not None:
				action.setIconVisibleInMenu(True)
				action.setIcon(QtGui.QIcon(icon))
			if key is not None:
				action.setShortcut(QtGui.QKeySequence(key))
			if functionAction:
				action.triggered.connect(function_action)
				# Associate action to the item.
				if id(item) not in self._items.keys():
					self._items.update({id(item): []})
				self._items[id(item)].append(action)
				##########################
			return action
		return action


	def clear(self):
		super(ControlTree, self).clear()
		if self._popup_menu:
			self._popup_menu.clear()
		self._items = {}

	def expand_item(self, item, expand=True, parents=True):
		item.setExpanded(expand)
		if parents:
			parent = item.parent()
			while(True):
				try:
					parent.setExpanded(expand)
					parent = parent.parent()
				except AttributeError:
					break



	def create_child(self, name, parent=None, icon=None):
		"""
		Create a new child for to the parent item.
		If the parent is None it add to the root.
		"""
		item = QTreeWidgetItem(self, [name]) if(
			parent is None) else QTreeWidgetItem(parent, [name])
		if icon is not None:
			if isinstance(icon, str):
				item.setIcon(0, QtGui.QIcon(icon))
			elif isinstance(icon, QtGui.QIcon):
				item.setIcon(0, icon)
		return item


	##########################################################################
	############ EVENTS ######################################################
	##########################################################################

	def item_changed_event(self, item): 		pass
	def item_selection_changed_event(self): 	pass
	def item_double_clicked_event(self, item): 	pass
	def key_press_event(self, event): 			pass
	def rows_inserted_event(self, parent, start, end):
		""" This event is called every time a new row is added to the tree"""
		pass

	##########################################################################
	############ PROPERTIES ##################################################
	##########################################################################

	@property
	def show_header(self): return self.header().isVisible()

	@show_header.setter
	def show_header(self, value):
		self.header().show() if value else self.header().hide()

	@property
	def selected_rows_indexes(self):
		result = []
		for index in self.selectedIndexes():
			result.append(index.row())
		return list(set(result))

	@property
	def selected_row_index(self):
		indexes = self.mouseSelectedRowsIndexes
		if len(indexes) > 0:
			return indexes[0]
		else:
			return None

	@property
	def selected_item(self):
		if len(self.selectedItems())>0: return self.selectedItems()[0]
		return None

	@property
	def form(self): return self

	@property
	def value(self):
		root = self.invisibleRootItem()
		return [root.child(i) for i in range(root.childCount())]

	@value.setter
	def value(self, value):
		if isinstance(value, list):
			for x in value:
				self += x
		else:
			self += value

	@property
	def icon_size(self):
		size = self.iconSize()
		return size.width(), size.height()

	@icon_size.setter
	def icon_size(self, value): self.setIconSize(QSize(*value))


	##########################################################################
	############ PRIVATE FUNCTIONS ###########################################
	##########################################################################

	def __itemChangedEvent(self, item): self.item_changed_event(item)

	def rowsInserted(self, parent, start, end):
		super(ControlTree, self).rowsInserted(parent, start, end)
		self.rows_inserted_event(parent, start, end)

	def selectionChanged(self, selected, deselected):
		super(QTreeView, self).selectionChanged(selected, deselected)
		self.item_selection_changed_event()

	def __itemDoubleClicked(self, item, column):
		if hasattr(item, 'double_clicked'): item.double_clicked()
		self.item_double_clicked_event(item)

	

	def keyPressEvent(self, event):
		QTreeView.keyPressEvent(self, event)
		item = self.selectedItem
		if hasattr(item, 'key_pressed'): item.key_pressed(event)
		self.key_press_event(event)



	def about_to_show_contextmenu_event(self):
		"""
		Function called before open the Control popup menu
		"""
		if len(self._items) > 0:  # Reset the menu and construct a new one only if there are actions for the items.
			self._popup_menu.clear()
			itemSelected = self.selectedItems()[0]

			if id(itemSelected) in self._items:
				for action in self._items[id(itemSelected)]:
					self._popup_menu.addAction(action)
					# print("Adding action {action} to {item}".format(
					#    action=action.text(), item=itemSelected))