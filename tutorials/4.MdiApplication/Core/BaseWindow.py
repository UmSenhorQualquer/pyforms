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

		self._textField 		= ControlText("Example")
		self._projectTree  		= ControlDockWidget('Project tree', side=ControlDockWidget.SIDE_RIGHT)
		self._details  			= ControlDockWidget('Details', 		side=ControlDockWidget.SIDE_RIGHT)
		self._addWindow 		= ControlButton('Add window')

		self.formset = [ '_addWindow','_textField', '_mdiArea']

		self._details.value = SimpleExample1()


		#self._mdiArea.showCloseButton = False
		self._addWindow.value = self.__addWindow

		self.mainmenu.append(
				{ 'File': [
						{'Save as': self.saveWindow},
						{'Open as': self.loadWindow},
						'-',
						{'Exit': self.__exit},
					]
				}
			)

	def __addWindow(self):
		self._simple = SimpleExample1(); 
		self._mdiArea += self._simple

	def __exit(self): exit()





##################################################################################################################
##################################################################################################################
##################################################################################################################

#Execute the application
if __name__ == "__main__":	 pyforms.start_app( BaseWindow )