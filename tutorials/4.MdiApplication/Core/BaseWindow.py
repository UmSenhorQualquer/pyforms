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

		self._formset = [ '_textField', '_mdiArea']

		self._details.value = SimpleExample1()
		
		simple = SimpleExample1(); simple.initForm()
		self._mdiArea.value = simple


		self.mainmenu.append(
				{ 'File': [
						{'Save as': self.saveWindow},
						{'Open as': self.loadWindow},
						'-',
						{'Exit': self.__exit},
					]
				}
			)

	def __exit(self): exit()





##################################################################################################################
##################################################################################################################
##################################################################################################################

#Execute the application
if __name__ == "__main__":	 pyforms.startApp( BaseWindow )