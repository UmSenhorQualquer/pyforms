import sys, glob, os
from PyQt4 import uic
from PyQt4 import QtGui, QtCore
import Utils.tools as tools

class Container(object):
	def __init__(self, ClassObject):
		self._algorithm = ClassObject()
		self._algorithm.initForm()
		form_path = os.path.join(tools.get_object_class_path( Container ), 'mainWindow.ui')
		self._form = uic.loadUi( form_path )
		self._form.verticalLayout.addWidget( self._algorithm )
		self._form.verticalLayout.setMargin(10)
		self._form.verticalLayout.setSpacing(0)
		self._form.actionExit.triggered.connect( self.actionExit_triggered )
		self._form.show()
		self._form.setWindowTitle( self._algorithm.title )
		self._form.actionStop.setEnabled(False)
		self._form.actionStop.triggered.connect( self.actionStop_triggered )

		try: 
			getattr(self._algorithm, 'execute')
			self._form.actionRun.triggered.connect( self.actionRun_triggered )
		except:
			self._form.menuAlgorithm.setEnabled(False)
			self._form.actionRun.setEnabled(False) 
			self._form.menuAlgorithm.setVisible(False)
			self._form.actionRun.setVisible(False)


	def actionExit_triggered(self): exit()
	def actionRun_triggered(self): 
		self._algorithm.stop = False
		self._form.actionRun.setEnabled(False)
		self._form.actionStop.setEnabled(True)
		self._algorithm.execute()
		
	def actionStop_triggered(self): 
		self._algorithm.stop = True
		self._form.actionRun.setEnabled(True)
		self._form.actionStop.setEnabled(False)

def startApp(ClassObject):
	app = QtGui.QApplication(sys.argv)
	container = Container(ClassObject)
	app.exec_()