import pyforms.standaloneManager as app
from pyforms.BaseWidget import BaseWidget


from PyQt4 import QtGui, QtCore
from pyforms.Controls.ControlText 		import ControlText
from pyforms.Controls.ControlButton 	import ControlButton
from pyforms.Controls.ControlTree import ControlTree


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
		

		self._formset = [ (' ','_addButton'), '_projectTree']

		
##################################################################################################################
##################################################################################################################
##################################################################################################################

#Execute the application
if __name__ == "__main__":	 app.startApp( BaseWindow )