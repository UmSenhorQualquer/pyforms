from pyforms.terminal.Controls.ControlBase import ControlBase
import numpy


import numpy as np 
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


try:
    import cv2
except:
    print( "cv2 not present. ControlPlayer not working")


try:
    from PIL import Image
except:
    print( "PIL not present. ControlPlayer not working")


try:
   import base64
except:
    print( "base64 not present. ControlPlayer not working")




class ControlPlayer(ControlBase):
    _currentFrame = None
    _min = 0
    _max = 0
    _filename = ''        
    _position = 0
    
    def process_frame_event(self, frame): pass

    def play(self): pass

    def stop(self): pass

    def refresh(self): pass

    def update_frame(self): pass

    def double_click_event(self, event, x, y): pass

    def click_event(self, event, x, y): pass

    def drag_event(self, start_point, end_point): pass

    def end_drag_event(self, start_point, end_point): pass

    def key_release_event(self, event): pass

    def process_frame_event(self, frame): pass

    def save_Form(self, data): pass

    def load_form(self, data): pass
    
    @property
    def value(self): 
        result = {'min': self._min, 'max': self._max, 'position': self.video_index, 'frame': '', 'filename': self._filename }
        capture = self._value

        _, image = capture.read()
        if isinstance(image, numpy.ndarray):
            image = self.processFrame(image)

            if isinstance(image, list) or isinstance(image, tuple):
                image = groupImage(image, True)
            

            if len(image.shape)>2: image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            buff = StringIO.StringIO()
            image.save(buff, format="PNG")
            content = buff.getvalue()
            buff.close()
            result['frame'] = base64.b64encode(content)

        return result

    @value.setter
    def value(self, value):
        if value:
            if isinstance( value, str ):
                ControlBase.value.fset(self, cv2.VideoCapture( value ) )
                self._filename = value
            if isinstance( value, dict ): 
                ControlBase.value.fset(self, cv2.VideoCapture( value['filename'] ) )
                if 'position' in value.keys(): self.video_index = int(value['position'])
                self._filename = value['filename']

            if isinstance(value, cv2.VideoCapture):
                ControlBase.value.fset(self, value )
            
            self._max = int(self._value.get(7))
        else:
            self._filename = None
            self._value = None
        


    @property
    def video_index(self): return self._position

    @video_index.setter
    def video_index(self, value): self._position = value


 

    @property
    def image(self): return self._currentFrame

    @image.setter
    def image(self, value): pass
        

