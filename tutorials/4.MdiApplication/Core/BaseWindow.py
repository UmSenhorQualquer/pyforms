import pyforms.standaloneManager as app
from pyforms.BaseWidget import BaseWidget

from pyforms.Controls.ControlText 		import ControlText
from pyforms.Controls.ControlButton 	import ControlButton
from pyforms.Controls.ControlDockWidget import ControlDockWidget
from pyforms.Controls.ControlMdiArea 	import ControlMdiArea

from Core.Controllers.ProjectTree import ProjectTree

class BaseWindow(BaseWidget):


	def __init__(self):
		super(BaseWindow, self).__init__('Test')

		#Definition of the forms fields
		self._mdiArea 			= ControlMdiArea()

		self._projectTree  		= ControlDockWidget('Project tree', side=ControlDockWidget.SIDE_RIGHT)
		self._details  			= ControlDockWidget('Details', 		side=ControlDockWidget.SIDE_RIGHT)

		self._formset = ['_details','_projectTree']

		self._projectTree.value = ProjectTree()

		



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
if __name__ == "__main__":	 app.startApp( BaseWindow )