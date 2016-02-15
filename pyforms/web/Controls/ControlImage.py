from pyforms.web.Controls.ControlBase import ControlBase
import cv2
import base64
import numpy as np 
import StringIO
from PIL import Image

class ControlImage(ControlBase):

    def __init__(self, label = "", defaultValue = "", helptext=None):
        super(ControlImage,self).__init__(label, defaultValue, helptext)
        self._filename = ''

    def initControl(self):
        return "new ControlImage('"+self._name+"','%s')" %  self.help 
        
    def save(self, data):
        if self.value!=None: data['value'] = self._value

    def load(self, data):
        if 'value' in data: self.value = data['value']

    def repaint(self): pass

    @property
    def value(self):
        result = { 'image': '', 'filename': self._filename }
        image = ControlBase.value.fget(self)
        if isinstance(image, np.ndarray):
            if len(image.shape)>2: image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            buff = StringIO.StringIO()
            image.save(buff, format="PNG")
            content = buff.getvalue()
            buff.close()
            result['image'] = base64.b64encode(content)
        return result


    @value.setter
    def value(self, value):
        if isinstance(value, np.ndarray):
            self._value = value
            
        if isinstance( value, (str, unicode) ):
            self._value = cv2.imread(value) 
            self._filename = value
        if isinstance( value, dict ): 
            self._value =  cv2.imread(value['filename'] )
            self._filename = value['filename']
        
