#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.Controls.ControlPlayer.ControlPlayer

"""

import math
import os
import logging
from PyQt4 import uic
from PyQt4 import QtCore, QtGui
from pyforms.gui.Controls.ControlBase import ControlBase
import pyforms.Utils.tools as tools

try:
	import cv2
except:
	print("Warning: was not possible to import cv2 in ControlPlayer")

from PyQt4.QtGui import QApplication
from pyforms.gui.Controls.ControlPlayer.VideoGLWidget import VideoGLWidget


__author__ = "Ricardo Ribeiro"
__credits__ = ["Ricardo Ribeiro"]
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = "Ricardo Ribeiro"
__email__ = "ricardojvr@gmail.com"
__status__ = "Development"


class ControlPlayer(ControlBase, QtGui.QFrame):

	_videoWidget = None
	_currentFrame = None

	def __init__(self, *args):
		QtGui.QFrame.__init__(self)
		ControlBase.__init__(self, *args)
		
		self.speed = 1
		self.logger = logging.getLogger('pyforms')

	def initForm(self):
		# Get the current path of the file
		rootPath = os.path.dirname(__file__)

		# Load the UI for the self instance
		uic.loadUi(os.path.join(rootPath, "video.ui"), self)


		# Define the icon for the Play button
		icon = QtGui.QIcon()
		pixmapOff = QtGui.qApp.style().standardPixmap(
			QtGui.QStyle.SP_MediaPlay)
		pixmapOn = QtGui.qApp.style().standardPixmap(
			QtGui.QStyle.SP_MediaPause)
		icon.addPixmap(
			pixmapOff, mode=QtGui.QIcon.Normal, state=QtGui.QIcon.Off)
		icon.addPixmap(pixmapOn, mode=QtGui.QIcon.Normal, state=QtGui.QIcon.On)
		self.videoPlay.setIcon(icon)

		
		
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
		# Controls if anything is drawn on the video
		self._draw_on_video = True
	
		self.view_in_3D = False



	def __rotateX(self):
		self._videoWidget.rotateX = self.form.verticalSlider.value()
		self.refresh()

	def __rotateZ(self):
		self._videoWidget.rotateZ = self.form.horizontalSlider.value()
		self.refresh()

	@property
	def speed(self): return self._speed
	@speed.setter
	def speed(self, value): self._speed = value

	@property
	def onDoubleClick(self): return self._videoWidget.onDoubleClick

	@onDoubleClick.setter
	def onDoubleClick(self, value): self._videoWidget.onDoubleClick = value

	@property
	def onClick(self): return self._videoWidget.onClick

	@onClick.setter
	def onClick(self, value):  self._videoWidget.onClick = value

	@property
	def onDrag(self): return self._videoWidget.onDrag

	@onDrag.setter
	def onDrag(self, value): self._videoWidget.onDrag = value

	@property
	def onEndDrag(self): return self._videoWidget.onEndDrag

	@onEndDrag.setter
	def onEndDrag(self, value): self._videoWidget.onEndDrag = value

	@property
	def view_in_3D(self):
		return self._videoWidget.onEndDrag

	@view_in_3D.setter
	def view_in_3D(self, value):
		self.form.horizontalSlider.setVisible(value)
		self.form.verticalSlider.setVisible(value)

	@property
	def on_key_release(self):
		return self._videoWidget.onKeyRelease

	@on_key_release.setter
	def on_key_release(self, value):
		self._videoWidget.onKeyRelease = value

	@property
	def isPainted(self): return self._draw_on_video

	def processFrame(self, frame):
		return frame

	def update_frame(self):
		if self.speed>1:  self.video_index += self.speed
		(success, frame) = self.value.read()

		if frame is not None:
			self._currentFrame = frame

		frame = self.processFrame(self._currentFrame.copy())
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

	def play(self): 
		self.videoPlay.setChecked(True)
		self._timer.start( 1000.0/float(self.fps+1) )

	def stop(self):
		self.videoPlay.setChecked(False)
		self._timer.stop()

	def refresh(self):
		if self._currentFrame is not None:
			frame = self.processFrame(self._currentFrame.copy())
			if isinstance(frame, list) or isinstance(frame, tuple):
				self._videoWidget.paint(frame)
			else:
				self._videoWidget.paint([frame])

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

	_updateVideoFrame = True

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

	@property
	def is_playing(self): return self._timer.isActive()


	def updateControl(self):
		if self._value:
			self.videoControl.setEnabled(True)
			self.videoProgress.setMinimum(0)
			self.videoProgress.setValue(0)
			self.videoProgress.setMaximum(self._value.get(7))
			self.videoFrames.setMinimum(0)
			self.videoFrames.setValue(0)
			self.videoFrames.setMaximum(self._value.get(7))

	@property
	def value(self): return ControlBase.value.fget(self)

	@value.setter
	def value(self, value):
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



	@property
	def video_index(self): return int(self._value.get(1)) - 1

	@video_index.setter
	def video_index(self, value): self._value.set(1, value)

	@property
	def max(self): return int(self._value.get(7))

	@property
	def image(self): return self._currentFrame

	@image.setter
	def image(self, value):
		if isinstance(value, list) or isinstance(value, tuple):
			self._videoWidget.paint(value)
		else:
			self._videoWidget.paint([value])
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
	def point(self): return self._videoWidget.point

	@point.setter
	def point(self, value): self._videoWidget.point = value

	def hide(self):
		QtGui.QFrame.hide(self)

	def show(self):
		QtGui.QFrame.show(self)

	@property
	def image_width(self): return self._value.get(3)

	@property
	def image_height(self): return self._value.get(4)
