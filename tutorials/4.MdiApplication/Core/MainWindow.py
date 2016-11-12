from Core.BaseWindow import BaseWindow

class MainWindow(BaseWindow):
	

	def __init__(self):
		super(MainWindow, self).__init__()

		#self.loadWindowData('teste.txt')


##################################################################################################################
##################################################################################################################
##################################################################################################################

#Execute the application
if __name__ == "__main__":	 
	import pyforms
	pyforms.start_app( MainWindow )