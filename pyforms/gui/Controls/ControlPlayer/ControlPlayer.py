#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.Controls.ControlPlayer.ControlPlayer

"""

import math
import os
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
        super(ControlPlayer, self).__init__(*args)

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

        # Define the icon for the Show/Hide markers button
        icon = QtGui.QIcon()
        pixmapOff = QtGui.qApp.style().standardPixmap(
            QtGui.QStyle.SP_DialogYesButton)
        pixmapOn = QtGui.qApp.style().standardPixmap(
            QtGui.QStyle.SP_DialogNoButton)
        icon.addPixmap(
            pixmapOff, mode=QtGui.QIcon.Normal, state=QtGui.QIcon.Off)
        icon.addPixmap(pixmapOn, mode=QtGui.QIcon.Normal, state=QtGui.QIcon.On)
        self.videoHideMarkers.setIcon(icon)

        self._videoWidget = VideoGLWidget()
        self._videoWidget._control = self
        self.videoLayout.addWidget(self._videoWidget)
        self.videoHideMarkers.clicked.connect(self.videoHideMarkers_clicked)
        self.videoPlay.clicked.connect(self.videoPlay_clicked)
        self.videoFPS.valueChanged.connect(self.videoFPS_valueChanged)
        self.videoFrames.valueChanged.connect(self.videoFrames_valueChanged)
        self.videoProgress.valueChanged.connect(
            self.videoProgress_valueChanged)
        self.videoProgress.sliderReleased.connect(
            self.videoProgress_sliderReleased)
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.updateFrame)

        self.form.horizontalSlider.valueChanged.connect(self.__rotateZ)
        self.form.verticalSlider.valueChanged.connect(self.__rotateX)

        self._currentFrame = None
        # Controls if anything is drawn on the video
        self._draw_on_video = True
        self._videoFPS = None  # Sets the FPS rate at which the video is played

        self.view3D = False

    def __rotateX(self):
        self._videoWidget.rotateX = self.form.verticalSlider.value()
        self.refresh()

    def __rotateZ(self):
        self._videoWidget.rotateZ = self.form.horizontalSlider.value()
        self.refresh()

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
    def view3D(self): return self._videoWidget.onEndDrag

    @view3D.setter
    def view3D(self, value):
        self.form.horizontalSlider.setVisible(value)
        self.form.verticalSlider.setVisible(value)

    @property
    def onKeyRelease(self): return self._videoWidget.onKeyRelease

    @onKeyRelease.setter
    def onKeyRelease(self, value): self._videoWidget.onKeyRelease = value

    @property
    def isPainted(self): return self._draw_on_video

    def processFrame(self, frame):
        return frame

    def updateFrame(self):
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

    def videoHideMarkers_clicked(self):
        """ Slot to hide or show stuff drawn on the video."""
        if self.videoHideMarkers.isChecked():
            self._draw_on_video = True
        else:
            self._draw_on_video = False
        self.refresh()
        # print "--->", self._draw_on_video

    def videoPlay_clicked(self):
        """Slot for Play/Pause functionality."""
        if self.videoPlay.isChecked():
            timeout_interval = (1000 / self._videoFPS)
            self._timer.start(timeout_interval)
        else:
            self._timer.stop()

    def pausePlay(self):
        if not self.videoPlay.isChecked():
            self.videoPlay.setChecked(True)
            timeout_interval = (1000 / self._videoFPS)
            self._timer.start(timeout_interval)
        else:
            self.videoPlay.setChecked(False)
            self._timer.stop()

    def videoFPS_valueChanged(self):
        """Get FPS rate from loaded video."""
        self._videoFPS = self.videoFPS.value()
        timeout_interval = (1000 / self._videoFPS)
        self._timer.setInterval(timeout_interval)

    def save(self, data):
        if self.value:
            data['value'] = self.value.captureFrom

    def load(self, data):
        # if 'value' in data: self.value = data['value']
        pass

    def refresh(self):
        if self._currentFrame != None:
            frame = self.processFrame(self._currentFrame.copy())
            if isinstance(frame, list) or isinstance(frame, tuple):
                self._videoWidget.paint(frame)
            else:
                self._videoWidget.paint([frame])

    def convertFrameToTime(self, totalMilliseconds):
        # totalMilliseconds = totalMilliseconds*(1000.0/self._value.get(cv2.cv.CV_CAP_PROP_FPS))

        totalseconds = int(totalMilliseconds / 1000)
        minutes = int(totalseconds / 60)
        seconds = totalseconds - (minutes * 60)
        milliseconds = totalMilliseconds - (totalseconds * 1000)
        return (minutes, seconds, milliseconds)

    def videoProgress_valueChanged(self):
        milli = self._value.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
        milli -= 1000.0 / self._value.get(cv2.cv.CV_CAP_PROP_FPS)
        (minutes, seconds, milliseconds) = self.convertFrameToTime(milli)
        self.videoTime.setText(
            "%02d:%02d:%03d" % (minutes, seconds, milliseconds))

    _updateVideoFrame = True

    def videoProgress_sliderReleased(self):
        jump2Frame = self.videoProgress.value()
        self._value.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, jump2Frame)
        self._updateVideoFrame = False
        self.videoFrames.setValue(jump2Frame)
        self._value.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, jump2Frame)
        self._updateVideoFrame = True

    def videoFrames_valueChanged(self, i):
        if not self.isPlaying():
            jump2Frame = self.videoProgress.value()
            diff = jump2Frame - i

            self._value.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, jump2Frame - diff)
            self._updateVideoFrame = False
            self.updateFrame()
            self._updateVideoFrame = True

    def isPlaying(self):
        return self._timer.isActive()

    def updateControl(self):

        if self._value:
            self.videoControl.setEnabled(True)
            self.videoProgress.setMinimum(self._value.startFrame)
            self.videoProgress.setValue(self._value.startFrame)
            self.videoProgress.setMaximum(self._value.endFrame)
            self.videoFrames.setMinimum(self._value.startFrame)
            self.videoFrames.setValue(self._value.startFrame)
            self.videoFrames.setMaximum(self._value.endFrame)

    @property
    def value(self): return ControlBase.value.fget(self)

    @value.setter
    def value(self, value):
        self._videoWidget.reset()

        if value == 0:
            self._value = cv2.OTVideoInput(0)
        elif isinstance(value, str) and value:
            self._value = cv2.VideoCapture(value)
            self.fps = self._value.get(cv2.cv.CV_CAP_PROP_FPS)
            # print("Open video with", self._value.get(
            #    cv2.cv.CV_CAP_PROP_FPS), 'fps')
        else:
            self._value = None

        if self._value and value != 0:
            self.videoProgress.setMinimum(0)
            self.videoProgress.setValue(0)
            self.videoProgress.setMaximum(
                self._value.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
            self.videoFrames.setMinimum(0)
            self.videoFrames.setValue(0)
            self.videoFrames.setMaximum(
                self._value.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))

        if self._value:
            self.videoControl.setEnabled(True)

        self.refresh()

    @property
    def startFrame(self):
        if self._value:
            return self._value.startFrame
        else:
            return -1

    @startFrame.setter
    def startFrame(self, value):
        if self._value:
            self._value.startFrame = value
            self.videoProgress.setMinimum(value)

    @property
    def endFrame(self):
        if self._value:
            return self._value.startFrame
        else:
            return -1

    @endFrame.setter
    def endFrame(self, value):

        if self._value:
            self._value.endFrame = value
            self.videoProgress.setValue(self._value.startFrame)
            self.videoProgress.setMaximum(value)

    @property
    def video_index(self): return int(
        self._value.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)) - 1

    @video_index.setter
    def video_index(self, value): self._value.set(
        cv2.cv.CV_CAP_PROP_POS_FRAMES, value)

    @property
    def max(self): return int(self._value.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))

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
    def fps(self): return self._videoFPS

    @fps.setter
    def fps(self, value):
        self._videoFPS = value
        if math.isnan(self._videoFPS):
            self._videoFPS = 15.0

    @property
    def show_markers(self): return self._draw_on_video

    @property
    def helpText(self): return self._videoWidget._helpText

    @fps.setter
    def helpText(self, value): self._videoWidget._helpText = value

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
