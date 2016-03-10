from pyforms.web.Controls.ControlBase import ControlBase

class ControlDir(ControlBase):

    def initControl(self):
    	return "new ControlDir('{0}', {1})".format( self._name, str(self.serialize()) )