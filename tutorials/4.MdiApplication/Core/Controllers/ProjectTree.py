import pyforms
from pyforms.basewidget import BaseWidget


from PyQt4 import QtGui, QtCore
from pyforms.controls import ControlText
from pyforms.controls import ControlButton
from pyforms.controls import ControlTree


class ProjectTree(BaseWidget):


	def __init__(self):
		super(ProjectTree, self).__init__('Project')

		self._addButton 	= ControlButton('Add')
		self._projectTree	= ControlTree('Project tree')

		root = QtGui.QTreeWidgetItem(self._projectTree, ["root"])
		A = QtGui.QTreeWidgetItem(root, ["A"])
		barA = QtGui.QTreeWidgetItem(A, ["bar", "i", "ii"])
		bazA = QtGui.QTreeWidgetItem(A, ["baz", "a", "b"])

		self._projectTree.showHeader = False
		

		self.formset = [ (' ','_addButton'), '_projectTree']

		
##################################################################################################################
##################################################################################################################
##################################################################################################################

#Execute the application
if __name__ == "__main__":	 pyforms.start_app( ProjectTree )