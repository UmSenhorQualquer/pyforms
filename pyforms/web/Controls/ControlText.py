from pyforms.web.Controls.ControlBase import ControlBase

class ControlText(ControlBase):

    def initControl(self):
        val = self.value.replace("{","&#123;").replace("}","&#125;")
        values = self._label, self._name,val, self.help
        return """new ControlText('%s','%s', "%s",'%s')""" % values