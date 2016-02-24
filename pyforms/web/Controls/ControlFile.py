from pyforms.web.Controls.ControlBase import ControlBase

class ControlFile(ControlBase):

    def initControl(self):
    	return "new ControlFile('{0}', {1})".format( self._name, str(self.serialize()) )