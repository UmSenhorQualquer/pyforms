#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.controls.ControlPlayer.ControlPlayer

"""
__author__ = "Ricardo Ribeiro"
__credits__ = ["Ricardo Ribeiro"]
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = "Ricardo Ribeiro"
__email__ = "ricardojvr@gmail.com"
__status__ = "Development"

import logging, platform, os, math, cv2

from pyforms.utils.settings_manager 	 import conf
from AnyQt 			 import uic, _api
from AnyQt 			 import QtCore
from AnyQt.QtWidgets import QFrame	
from AnyQt.QtWidgets import QApplication
from pyforms.gui.controls.ControlBase import ControlBase

if _api.USED_API == _api.QT_API_PYQT5:
	import platform
	if platform.system() == 'Darwin':
		from pyforms.gui.controls.control_player.VideoQt5GLWidget import VideoQt5GLWidget as VideoGLWidget
	else:
		from pyforms.gui.controls.control_player.VideoGLWidget 	 import VideoGLWidget

elif _api.USED_API == _api.QT_API_PYQT4:	
	from pyforms.gui.controls.control_player.VideoGLWidget 		 import VideoGLWidget



class ControlPlayer(ControlBase, QFrame):

	_videoWidget = None
	_currentFrame = None

	def __init__(self, *args):
		QFrame.__init__(self)
		ControlBase.__init__(self, *args)
		
		self._speed = 1
		self.logger = logging.getLogger('pyforms')

		self._updateVideoFrame = True

	def init_form(self):
		# Get the current path of the file
		rootPath = os.path.dirname(__file__)

		# Load the UI for the self instance
		uic.loadUi(os.path.join(rootPath, "video.ui"), self)


		# Define the icon for the Play button
		
		self.videoPlay.setIcon(conf.PYFORMS_ICON_VIDEOPLAYER_PAUSE_PLAY)

		self._videoWidget = VideoGLWidget()
		self._videoWidget._control = self
		self.videoLayout.addWidget(self._videoWidget)
		self.videoPlay.clicked.connect(self.videoPlay_clicked)
		self.videoFrames.valueChanged.connect(self.videoFrames_valueChanged)
		self.videoProgress.valueChanged.connect(self.videoProgress_valueChanged)
		self.videoProgress.sliderReleased.connect(self.videoProgress_sliderReleased)
		self._timer = QtCore.QTimer(self)
		self._timer.timeout.connect(self.update_frame)

		self.form.horizontalSlider.valueChanged.connect(self.__rotateZ)
		self.form.verticalSlider.valueChanged.connect(self.__rotateX)

		self._currentFrame = None
	
		self.view_in_3D = False

	##########################################################################
	############ FUNCTIONS ###################################################
	##########################################################################

	def play(self): 
		self.videoPlay.setChecked(True)
		self._timer.start( 1000.0/float(self.fps+1) )

	def stop(self):
		self.videoPlay.setChecked(False)
		self._timer.stop()

	def hide(self): QFrame.hide(self)

	def show(self): QFrame.show(self)

	def refresh(self):
		if self._currentFrame is not None:
			frame = self.process_frame_event(self._currentFrame.copy())
			if isinstance(frame, list) or isinstance(frame, tuple):
				self._videoWidget.paint(frame)
			else:
				self._videoWidget.paint([frame])
		else:
			self._videoWidget.paint(None)

	def save_form(self, data, path=None): return data

	def load_form(self, data, path=None): pass


	##########################################################################
	############ EVENTS ######################################################
	##########################################################################

	def process_frame_event(self, frame): return frame

	@property
	def double_click_event(self): return self._videoWidget.onDoubleClick
	@double_click_event.setter
	def double_click_event(self, value): self._videoWidget.onDoubleClick = value

	@property
	def click_event(self): return self._videoWidget.onClick
	@click_event.setter
	def click_event(self, value):  self._videoWidget.onClick = value

	@property
	def drag_event(self): return self._videoWidget.onDrag
	@drag_event.setter
	def drag_event(self, value): self._videoWidget.onDrag = value

	@property
	def end_drag_event(self): return self._videoWidget.onEndDrag
	@end_drag_event.setter
	def end_drag_event(self, value): self._videoWidget.onEndDrag = value

	@property
	def key_release_event(self): return self._videoWidget.on_key_release
	@key_release_event.setter
	def key_release_event(self, value): self._videoWidget.on_key_release = value

	##########################################################################
	############ PROPERTIES ##################################################
	##########################################################################

	@property
	def next_frame_step(self): return self._speed
	@next_frame_step.setter
	def next_frame_step(self, value): self._speed = value

	@property
	def view_in_3D(self): return self._videoWidget.onEndDrag
	@view_in_3D.setter
	def view_in_3D(self, value):
		self.form.horizontalSlider.setVisible(value)
		self.form.verticalSlider.setVisible(value)

	@property
	def video_index(self): return int(self._value.get(1)) if self._value else None

	@video_index.setter
	def video_index(self, value): self._value.set(1, value)

	@property
	def max(self): return int(self._value.get(7))

	@property
	def frame(self): return self._currentFrame

	@frame.setter
	def frame(self, value):
		if isinstance(value, list) or isinstance(value, tuple):
			self._videoWidget.paint(value)
		elif value is not None:
			self._videoWidget.paint([value])
		else:
			self._videoWidget.paint(None)
		QApplication.processEvents()

	@property
	def fps(self): 
		"""
			Return the video frames per second
		"""
		return self._value.get(5)

	@property
	def help_text(self): return self._videoWidget._helpText

	@help_text.setter
	def help_text(self, value): self._videoWidget._helpText = value

	@property
	def form(self): return self

	@property
	def frame_width(self): return self._value.get(3)

	@property
	def frame_height(self): return self._value.get(4)

	@property
	def is_playing(self): return self._timer.isActive()

	@property
	def value(self): return ControlBase.value.fget(self)

	@value.setter
	def value(self, value):
		if value is None: 
			self.stop()
			self.videoControl.setEnabled(False)
			self.refresh()
		self._videoWidget.reset()

		if value == 0:
			self._value = cv2.VideoCapture(0)
		elif isinstance(value, str) and value:
			self._value = cv2.VideoCapture(value)
		else:
			self._value = value

		if self._value and value != 0:
			self.videoProgress.setMinimum(0)
			self.videoProgress.setValue(0)
			self.videoProgress.setMaximum(
				self._value.get(7))
			self.videoFrames.setMinimum(0)
			self.videoFrames.setValue(0)
			self.videoFrames.setMaximum(
				self._value.get(7))

		if self._value:
			self.videoControl.setEnabled(True)

		self.refresh()


	##########################################################################
	############ PRIVATE FUNCTIONS ###########################################
	##########################################################################

	def __rotateX(self):
		self._videoWidget.rotateX = self.form.verticalSlider.value()
		self.refresh()

	def __rotateZ(self):
		self._videoWidget.rotateZ = self.form.horizontalSlider.value()
		self.refresh()

	

	

	def update_frame(self):
		if not self.visible: self.stop()

		if self.value is None: 
			self._currentFrame = None
			return
		if self.next_frame_step>1:  self.video_index += self.next_frame_step
		(success, frame) = self.value.read()

		if not success: self.stop()
		if frame is not None: self._currentFrame = frame

		if self._currentFrame is not None:
			frame = self.process_frame_event(self._currentFrame.copy())
			if isinstance(frame, list) or isinstance(frame, tuple):
				self._videoWidget.paint(frame)
			else:
				self._videoWidget.paint([frame])

			if not self.videoProgress.isSliderDown():
				currentFrame = self.video_index

				self.videoProgress.setValue(currentFrame)
				if self._updateVideoFrame:
					self.videoFrames.setValue(currentFrame)


	def videoPlay_clicked(self):
		"""Slot for Play/Pause functionality."""
		if self.is_playing:
			self.stop()
		else:
			self.play()

	def convertFrameToTime(self, totalMilliseconds):
		# totalMilliseconds = totalMilliseconds*(1000.0/self._value.get(5))
		if math.isnan(totalMilliseconds): return 0, 0, 0
		totalseconds = int(totalMilliseconds / 1000)
		minutes = int(totalseconds / 60)
		seconds = totalseconds - (minutes * 60)
		milliseconds = totalMilliseconds - (totalseconds * 1000)
		return (minutes, seconds, milliseconds)

	def videoProgress_valueChanged(self):
		milli = self._value.get(0)
		(minutes, seconds, milliseconds) = self.convertFrameToTime(milli)
		self.videoTime.setText(
			"%02d:%02d:%03d" % (minutes, seconds, milliseconds))

	

	def videoProgress_sliderReleased(self):
		jump2Frame = self.videoProgress.value()
		self._value.set(1, jump2Frame)
		self._updateVideoFrame = False
		self.videoFrames.setValue(jump2Frame)
		self._value.set(1, jump2Frame)
		self._updateVideoFrame = True

	def videoFrames_valueChanged(self, i):
		if not self.is_playing:
			jump2Frame = self.videoProgress.value()
			diff = jump2Frame - i

			self._value.set(1, jump2Frame - diff)
			self._updateVideoFrame = False
			self.update_frame()
			self._updateVideoFrame = True