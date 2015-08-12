import cv2, base64, numpy as np, StringIO, pyforms.Utils.tools as tools
from pyforms.web.Controls.ControlBase import ControlBase
from PIL import Image

from django.conf import settings

class ControlPlayer(ControlBase):
    _currentFrame = None
    _min = 0
    _max = 0
    _filename = ''        
    
    def initControl(self):
        self._currentFrame = None
        return "controls.push(new ControlPlayer('"+self._name+"','%s'));" % self.help

    def processFrame(self, frame):  pass

    def updateFrame(self):          pass

    def videoPlay_clicked(self):    pass

    def save(self, data):           pass

    def load(self, data):           pass

    def refresh(self):              pass
            
    def convertFrameToTime(self, frame):
        currentMilliseconds = (frame / self.value.videoFrameRate) * 1000
        totalseconds = int(currentMilliseconds/1000)
        minutes = int(totalseconds / 60)
        seconds = totalseconds - (minutes*60)
        milliseconds = currentMilliseconds - (totalseconds*1000)
        return ( minutes, seconds, milliseconds )

    def videoProgress_valueChanged(self):   pass

    def videoProgress_sliderReleased(self): pass

    def videoFrames_valueChanged(self):     pass

    def isPlaying(self):    pass

    def changed(self):      pass

    
    @property
    def value(self): 
        if self._value==None or self._value=='': return None
        result = {
            'min': self._min,
            'max': self._max, 
            'position': self.video_index, 
            'frame': '', 
            'filename': self._filename }
        capture = self._value
        _, image = capture.read()
        
        if isinstance(image, np.ndarray):
            image = self.processFrame(image)

            if isinstance(image, list) or isinstance(image, tuple):
                image = tools.groupImage(image, True)
            
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
            link = self.storage.public_link(value)
            link = "{1}/index.php/s/{0}/download".format(link.token, settings.OWNCLOUD_LINK)
            ControlBase.value.fset(self, cv2.VideoCapture( link ) )
            self._filename = value            
        if isinstance( value, dict ):
            filename = value['filename']
            if len(filename)>0:
                link = self.storage.public_link(value['filename'])
                link = "{1}/index.php/s/{0}/download".format(link.token, settings.OWNCLOUD_LINK)
                ControlBase.value.fset(self, cv2.VideoCapture(link) )
                if 'position' in value.keys(): self.video_index = int(value['position'])
                self._filename = value['filename']
            else:
                self._value = None

        if self._value!=None: 
            self._max = int( self._value.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT) )
        


    @property
    def video_index(self): return int(self._value.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)) if self._value else 0

    @video_index.setter
    def video_index(self, value): 
        self._value.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, float(value))
        

        
    @property
    def startFrame(self): 
        if self._value: return self._value.startFrame
        else: return -1

    @startFrame.setter
    def startFrame(self, value):
        if self._value: self._value.startFrame = value
            
    @property
    def endFrame(self): 
        if self._value: return self._value.startFrame
        else: return -1

    @endFrame.setter
    def endFrame(self, value):        
        if self._value: self._value.endFrame = value

    @property
    def image(self): 
        _, image = self._value.read()
        
        return image

