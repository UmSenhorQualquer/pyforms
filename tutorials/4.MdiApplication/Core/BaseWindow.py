import pyforms
from pyforms import BaseWidget

from pyforms.Controls	import ControlText
from pyforms.Controls	import ControlButton
from pyforms.Controls 	import ControlDockWidget
from pyforms.Controls	import ControlMdiArea

from Core.SimpleExample1 import SimpleExample1
from Core.Controllers.ProjectTree import ProjectTree

class BaseWindow(BaseWidget):


	def __init__(self):
		super(BaseWindow, self).__init__('Test')

		#Definition of the forms fields
		self._mdiArea 			= ControlMdiArea()

		self._textField 		= ControlText("EXample")
		self._projectTree  		= ControlDockWidget('Project tree', side=ControlDockWidget.SIDE_RIGHT)
		self._details  			= ControlDockWidget('Details', 		side=ControlDockWidget.SIDE_RIGHT)
		self._addWindow 		= ControlButton('Add window')
		self._open2Window 		= ControlButton('Show window')

		self._formset = [ '_addWindow','_open2Window','_textField', '_mdiArea']

		self._details.value = SimpleExample1()
		
		self._mdiArea.showCloseButton = False
		self._addWindow.value = self.__addWindow		
		self._open2Window.value = self.__open2Windows

		self.mainmenu.append(
				{ 'File': [
						{'Save as': self.saveWindow},
						{'Open as': self.loadWindow},
						'-',
						{'Exit': self.__exit},
					]
				}
			)

	def __open2Windows(self):
		self._mdiArea.value = [ SimpleExample1(),  SimpleExample1()]

	def __addWindow(self):
		self._simple = SimpleExample1(); 
		self._mdiArea += self._simple

		print self._simple.subwindow

	def __exit(self): exit()





##################################################################################################################
##################################################################################################################
##################################################################################################################

#Execute the application
if __name__ == "__main__":	 pyforms.startApp( BaseWindow )