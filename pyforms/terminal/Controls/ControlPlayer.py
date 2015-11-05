from pyforms.terminal.Controls.ControlBase import ControlBase
import numpy
import cv2
import base64
import numpy as np 
import StringIO
from PIL import Image



class ControlPlayer(ControlBase):
    _currentFrame = None
    _min = 0
    _max = 0
    _filename = ''        
    _position = 0
    
    def initControl(self):
        self._currentFrame = None
        return "controls.push(new ControlPlayer('"+self._name+"'));"

    def processFrame(self, frame): pass

    def updateFrame(self): pass

    def videoPlay_clicked(self): pass

    def save(self, data): pass

    def load(self, data): pass

    def refresh(self): pass
            
    def convertFrameToTime(self, frame):
        currentMilliseconds = (frame / self.value.videoFrameRate) * 1000
        totalseconds = int(currentMilliseconds/1000)
        minutes = int(totalseconds / 60)
        seconds = totalseconds - (minutes*60)
        milliseconds = currentMilliseconds - (totalseconds*1000)
        return ( minutes, seconds, milliseconds )

    def videoProgress_valueChanged(self): pass

    def videoProgress_sliderReleased(self): pass

    def videoFrames_valueChanged(self): pass

    def isPlaying(self): pass

    def changed(self): pass

    
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
        if isinstance( value, (str, unicode) ):
            ControlBase.value.fset(self, cv2.VideoCapture( value ) )
            self._filename = value
        if isinstance( value, dict ): 
            ControlBase.value.fset(self, cv2.VideoCapture( value['filename'] ) )
            if 'position' in value.keys(): self.video_index = int(value['position'])
            self._filename = value['filename']
        self._max = int(self._value.get(7))
        


    @property
    def video_index(self): return self._position

    @video_index.setter
    def video_index(self, value): self._position = value


        
    @property
    def startFrame(self): 
        if self._value: return self._value.startFrame
        else: return -1

    @startFrame.setter
    def startFrame(self, value): pass
            
    @property
    def endFrame(self): 
        if self._value: return self._value.startFrame
        else: return -1

    @endFrame.setter
    def endFrame(self, value): pass



    @property
    def image(self): return self._currentFrame

    @image.setter
    def image(self, value): pass
        

