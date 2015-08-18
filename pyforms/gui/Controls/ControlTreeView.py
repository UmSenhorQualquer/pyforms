from pyforms.gui.Controls.ControlBase import ControlBase
from PyQt4 import uic
from PyQt4 import QtGui, QtCore


class ControlTreeView(ControlBase):

	def initForm(self):
		self._form = QtGui.QTreeView()

		view = self._form
		view.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		view.header().hide()
		view.setUniformRowHeights(True)
		view.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
		view.setDragEnabled(True)
		view.setAcceptDrops(True)
		
		view.setModel(QtGui.QStandardItemModel())
		#self._model = TreeModel()
		#view.setModel(self._model)

		view.model().itemChanged.connect(self.__itemChangedEvent)
		
		view.selectionChanged = self.selectionChanged

		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		# populate data
		"""
		for i in range(3):
			parent1 = QtGui.QStandardItem('Family {}. Some long status text for sp'.format(i))
			for j in range(3):
				child1 = QtGui.QStandardItem('Child {}'.format(i*3+j))
				parent1.appendRow(child1)
			model.appendRow(parent1)
			# span container columns
			view.setFirstColumnSpanned(i, view.rootIndex(), True)
		"""



	@property
	def model(self): return self._form.model()
	@model.setter
	def model(self, value): 
		self._model = value
		self._form.setModel(value)

	def __itemChangedEvent(self, item): self.itemChangedEvent(item)

	def itemChangedEvent(self, item): pass
		

	def itemSelectionChanged(self):pass

	def selectionChanged(self, selected, deselected ):
		super(QtGui.QTreeView, self._form).selectionChanged(selected, deselected)
		self.itemSelectionChanged()

	@property
	def mouseSelectedRowsIndexes(self):
		result = []
		for index in self._form.selectedIndexes():
			result.append( index.row() )
		return list( set(result) )


	@property
	def mouseSelectedRowIndex(self):
		indexes = self.mouseSelectedRowsIndexes
		if len(indexes)>0: return indexes[0]
		else: return None

	@property
	def selectedItem(self):
		for index in self._form.selectedIndexes():
			item = index.model().itemFromIndex(index)
			return item
		else:
			return None

	@property
	def cells(self): 
		results = []
		for row in range(self._model.rowCount()):
			r = []
			for col in range(self._model.columnCount()):
				r.append( self._model.item(row, col) )
			if len(r)>0: results.append(r)
			print r, '---'

		return results


	def __add__(self, other):
		if isinstance(other, TreeItem):
			self._model.invisibleRootItem().appendRow( other )

		elif isinstance(other, list):
			for x in other:
				item = QtGui.QStandardItem( x )
				self._model.appendRow( item )
		else:
			item = QtGui.QStandardItem( other )
			self._model.appendRow( item )

		self._form.setFirstColumnSpanned(self._model.rowCount()-1, self._form.rootIndex(), True)
		return self

	def __sub__(self, other):
		if isinstance(other, int):
			if other < 0:
				indexToRemove = self.mouseSelectedRowIndex
			else:
				indexToRemove = other
			self.model.removeRow(indexToRemove)
		return self

	

	@property
	def value(self):  
		return self._form.model().invisibleRootItem()
		return self.recursivelyReadRoot(root)

	@value.setter
	def value(self, value):
		for row in value: self += row


	def getAllSceneObjects(self): return self._model.getChildrens()