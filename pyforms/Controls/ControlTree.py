from pyforms.Controls.ControlBase import ControlBase
from PyQt4 import uic
from PyQt4 import QtGui, QtCore

class ControlTree(ControlBase):

	def initControl(self):
		self._form = QtGui.QTreeWidget()

		view = self._form
		view.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		view.setUniformRowHeights(True)
		view.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
		view.setDragEnabled(True)
		view.setAcceptDrops(True)
		
		view.model().dataChanged.connect(self.__itemChangedEvent)
		
		view.selectionChanged = self.selectionChanged

		self.showHeader = False

	@property
	def showHeader(self): return self.form.header().isVisible()
	@showHeader.setter
	def showHeader(self, value): 
		if value: self.form.header().show()
		else: self.form.header().hide()


	@property
	def model(self): return self._form.model()
	@model.setter
	def model(self, value): 
		self.form.setModel(value)

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
		for row in range(self.model.rowCount()):
			r = []
			for col in range(self.model.columnCount()):
				r.append( self.model.item(row, col) )
				"""
				try:
					r.append( self._model.item(col, row) )
				except:
					r.append( None )
					pass"""
			if len(r)>0: results.append(r)

		return results


	def __add__(self, other):
		if isinstance(other, QtGui.QTreeWidgetItem):
			self.model.invisibleRootItem().appendRow( other )

		elif isinstance(other, list):
			for x in other:
				print x
				item = QtGui.QTreeWidgetItem( x )
				self.form.addTopLevelItem(item)
		else:
			item = QtGui.QTreeWidgetItem( other )
			self.form.addTopLevelItem(item)

		self._form.setFirstColumnSpanned(self.model.rowCount()-1, self._form.rootIndex(), True)
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


	def getAllSceneObjects(self): return self.model.getChildrens()