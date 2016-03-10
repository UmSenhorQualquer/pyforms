import cv2, base64, numpy as np, StringIO, pyforms.Utils.tools as tools
from pyforms.web.Controls.ControlBase import ControlBase
from PIL import Image

from django.conf import settings

class ControlPlayer(ControlBase):

	def __init__(self, label = "", defaultValue = "", helptext=''):
		self._filename = ''
		ControlBase.__init__(self, label, defaultValue, helptext)

	def initControl(self): 
		return "new ControlPlayer('{0}', {1})".format( self._name, str(self.serialize()) )

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
	def value(self): return self._value

	@value.setter
	def value(self, value):
		if isinstance( value, (str, unicode) ):
			link = self.storage.public_link(value)
			link = "{1}/index.php/s/{0}/download".format(link.token, settings.OWNCLOUD_LINK)
			ControlBase.value.fset(self, cv2.VideoCapture( link ) )
			self._filename = value
		else:
			self._value = value

	


	def serialize(self):
		data    = ControlBase.serialize(self)

		if self.value:
			capture = self.value
			_, image = capture.read()
			
			if isinstance(image, np.ndarray):
				image = self.processFrame(image)
				if isinstance(image, list) or isinstance(image, tuple): image = tools.groupImage(image, True)
				
				if len(image.shape)>2: image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
				image = Image.fromarray(image)
				buff = StringIO.StringIO()
				image.save(buff, format="PNG")
				content = buff.getvalue()
				buff.close()
				data.update({ 'base64content': base64.b64encode(content) })

		data.update({ 'filename':       self._filename      })
		data.update({ 'startFrame':     self.startFrame     })
		data.update({ 'endFrame':       self.endFrame       })
		data.update({ 'video_index':    self.video_index    })
		return data


	def deserialize(self, properties):
		ControlBase.deserialize(self, properties)
		self._filename   = properties['filename']
		self.startFrame  = properties['startFrame']
		self.endFrame    = properties['endFrame']
		self.video_index = properties['video_index']
		self.value       = self._filename



	@property
	def video_index(self): return int(self._value.get(1)) if self._value else 0

	@video_index.setter
	def video_index(self, value):  self._value.set(1, float(value))
		

		
	@property
	def startFrame(self): 
		return self._value.startFrame if self._value else -1

	@startFrame.setter
	def startFrame(self, value):
		if self._value: self._value.startFrame = value
			
	@property
	def endFrame(self): 
		return self._value.endFrame if self._value else -1

	@endFrame.setter
	def endFrame(self, value):        
		if self._value: self._value.endFrame = value

	@property
	def image(self): 
		_, image = self._value.read()
		return image