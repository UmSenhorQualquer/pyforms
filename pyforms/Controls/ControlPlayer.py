#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


from ControlBase import ControlBase
import pyforms.Utils.tools as tools
from PyQt4 import uic
from PyQt4.QtOpenGL import QGLWidget
from PyQt4 import QtCore
import OpenGL.GL  as GL
import OpenGL.GLU as GLU
import cv2, math
from PyQt4.QtGui import QApplication


class VideoGLWidget(QGLWidget):

    image2Display = []
    texture = []
    _x = 0.0
    _y = 0.0
    zoom = 1.0
    _width = 1.0
    _height = 1.0
    _mouseX = 0.0
    _mouseY = 0.0
    _mouseDown = False
    _glX = 0.0
    _glY = 0.0
    _glZ = 0.0
    _lastGlX = 0.0
    _lastGlY = 0.0

    def __init__(self, parent=None):
        QGLWidget.__init__(self, parent)
        self.image2Display = []
        self.texture = []
        self.setMouseTracking(True)
        self.zoom = 1.0
        self._mouseX = 0.0
        self._mouseY = 0.0
        self._glX = 0.0
        self._glY = 0.0
        self._glZ = 0.0
        self._lastGlX = 0.0
        self._lastGlY = 0.0
        self._mouseDown = False
        self._mouseLeftDown = False
        self._mouseRightDown = False

        self._mouseStartDragPoint = None
        self._helpText = None #Message to show on the left corner of the screen

        self.setMinimumHeight(100)


    def initializeGL(self):
        GL.glClearDepth(1.0)
        GL.glClearColor(0, 0, 0, 1.0)
        GL.glEnable(GL.GL_DEPTH_TEST)

    def resizeGL(self, width, height):
        GL.glViewport(0, 0, width, height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective(40.0, float(width)/float(height), 0.01, 10.0)

    def drawVideo(self, _width, _height, x , y, z):

        GL.glPushMatrix()
        GL.glTranslatef(x , y, z)
        GL.glBegin(GL.GL_QUADS )
        GL.glTexCoord2f( 0.0, 1.0 );
        GL.glVertex3f( 0, 0, 0 );#top left
        GL.glTexCoord2f( 0.0, 0.0 );
        GL.glVertex3f( 0, _height, 0 ); #bottom left
        GL.glTexCoord2f( 1.0, 0.0 );
        GL.glVertex3f( _width, _height, 0 );	#bottom right
        GL.glTexCoord2f( 1.0, 1. );
        GL.glVertex3f( _width, 0, 0 ); #top right
        GL.glEnd()
        GL.glPopMatrix()

    def paintGL(self):
        GL.glClearColor(0.5, 0.5, 0.5, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

        
        translateX = ( len(self.texture) * self._width ) / 2

        if len(self.texture) > 0:
            GL.glTranslatef( -translateX, -self._height/2, -self.zoom)

            GL.glDisable(GL.GL_TEXTURE_2D)
            GL.glColor4f(0.5, 0.5, 0.5, 1.0)
            GL.glBegin(GL.GL_QUADS)
            GL.glVertex3f(20, -20, -.001)
            GL.glVertex3f(20, 20, -.001)
            GL.glVertex3f(-20, 20, -.001)
            GL.glVertex3f(-20, -20, -.001)
            GL.glEnd()

            GL.glColor4f(1, 1, 1, 1.0)

            GL.glEnable(GL.GL_TEXTURE_2D)

            for texture_index in range(0, len(self.texture) ):
                if texture_index>0: GL.glTranslatef( self._width,  0, 0)

                GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture[ texture_index ])

                if self._mouseRightDown:
                    self.drawVideo( self._width, self._height, self._x- (self._lastGlX - self._glX) , self._y - (self._lastGlY - self._glY), 0.0)
                else:
                    self.drawVideo( self._width, self._height, self._x , self._y, 0.0)

            if self._mouseDown:
                modelview = GL.glGetDoublev( GL.GL_MODELVIEW_MATRIX )
                projection = GL.glGetDoublev( GL.GL_PROJECTION_MATRIX )
                viewport = GL.glGetIntegerv( GL.GL_VIEWPORT )
                winX = float(self._mouseX);
                winY = float(viewport[3] - self._mouseY)
                winZ = GL.glReadPixels(winX, winY, 1, 1, GL.GL_DEPTH_COMPONENT, GL.GL_FLOAT)
                self._glX, self._glY, self._glZ = GLU.gluUnProject( winX, winY, winZ[0][0], modelview, projection, viewport)
        
        if self._helpText!=None: 
            self.qglColor(QtCore.Qt.white)
            self.renderText( 4,15, self._helpText)



    def reset(self):
        self.texture = []
        self.image2Display = []

    def paint(self, frames):

        if len(self.image2Display) == 0:
            self.imgHeight, self.imgWidth = frames[0].shape[:2]
            if self.imgWidth>self.imgHeight:
                self._width = 1
                self._height = float(self.imgHeight) / float(self.imgWidth)
                self._x = -float(self._width)/2
                self._y = 0
            else:
                self._height = 1
                self._width = float(self.imgWidth) / float(self.imgHeight)
                self._y = 0.5

        #self._x = -self._width/2


        if len(self.texture)>len(frames):
            for i in range( len(self.texture)-len(frames) ):
                GL.glDeleteTextures( self.texture.pop() )

        self.image2Display = frames

        for index, frame in enumerate(frames):
            if len(frame.shape)==2:
                color = GL.GL_LUMINANCE
            else:
                color = GL.GL_BGR

            if len(self.texture)<len(self.image2Display): self.texture.append( GL.glGenTextures(1) )

            w = len(frame[0])
            h = len(frame)

            GL.glEnable(GL.GL_TEXTURE_2D)
            GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT,1)
            GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture[index])
            GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_BORDER)
            GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_BORDER)
            GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
            GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
            GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, w, h, 0, color, GL.GL_UNSIGNED_BYTE, frame)

        self.repaint()

    def wheelEvent(self, event):
        if event.delta()<0: self.zoom += 0.1
        else: self.zoom -= 0.1
        if self.zoom<0.01: self.zoom = 0.02
        self.repaint()

    def mouseDoubleClickEvent(self, event):
        self._mouseX = event.x()
        self._mouseY = event.y()
        self.repaint()
        if hasattr(self, 'imgWidth'):
            self.onDoubleClick(event, (self._glX-self._x)*float(self.imgWidth), (self._height-self._glY+self._y)*float(self.imgWidth) )

    def mouseReleaseEvent(self, event):
        self._mouseDown = False

        if event.button()==4:
            self._mouseRightDown = False
            self._x -= self._lastGlX - self._glX
            self._y -= self._lastGlY - self._glY
            self._lastGlX = self._glX
            self._lastGlY = self._glY

        if event.button()==1:
            if hasattr(self, 'imgWidth') and self._mouseLeftDown:
                self.onEndDrag( self._mouseStartDragPoint, ( (self._glX - self._x)*float(self.imgWidth), (self._height-self._glY + self._y)*float(self.imgWidth) ) )
            self._mouseLeftDown = False

    def mousePressEvent(self, event):
        super(QGLWidget, self).mousePressEvent(event)
        self.setFocus( QtCore.Qt.MouseFocusReason)

        self._mouseDown = True
        self._mouseX = event.x()
        self._mouseY = event.y()
        self.repaint()

        if hasattr(self, 'imgWidth'):
            self.onClick(event, (self._glX-self._x)*float(self.imgWidth), (self._height-self._glY+self._y)*float(self.imgWidth) )


        if event.button()==1:
            self._mouseLeftDown = True
            self._mouseStartDragPoint = (self._glX  - self._x, self._height-self._glY + self._y )

        if event.button()==4:
            self._mouseRightDown = True
            self._lastGlX = self._glX
            self._lastGlY = self._glY

    def mouseMoveEvent(self, event):
        self._mouseX = event.x()
        self._mouseY = event.y()
        self.repaint()
        if self._mouseLeftDown and self._mouseDown:
            self.onDrag( self._mouseStartDragPoint, ( (self._glX - self._x)*float(self.imgWidth), (self._height-self._glY + self._y)*float(self.imgWidth) ) )

    def keyReleaseEvent(self, event):
        super(QGLWidget, self).keyReleaseEvent(event)
        # Control video playback using the space bar to Play/Pause
        if event.key() == QtCore.Qt.Key_Space: self._control.pausePlay()
        # Jumps 1 frame forward
        if event.key() == QtCore.Qt.Key_D:
            self._control.video_index += 1
            self._control.updateFrame()

        # Jumps 1 frame backwards
        if event.key() == QtCore.Qt.Key_A:
            self._control.video_index -= 1
            self._control.updateFrame()

        self.onKeyRelease(event)

    def onDoubleClick(self, event, x, y): pass
    def onClick(self, event, x, y): pass
    def onDrag(self, startPoint, endPoint): pass
    def onEndDrag(self, startPoint, endPoint): pass
    def onKeyRelease(self, event): pass




















class ControlPlayer(ControlBase):

    _videoWidget = None
    _currentFrame = None

    def initControl(self):

        control_path = tools.getFileInSameDirectory(__file__, "video.ui")
        self._form = uic.loadUi(control_path)
        self._videoWidget = VideoGLWidget()
        self._videoWidget._control = self
        self._form.videoLayout.addWidget(self._videoWidget)
        self._form.videoHideMarkers.clicked.connect(self.videoHideMarkers_clicked)
        self._form.videoPlay.clicked.connect(self.videoPlay_clicked)
        self._form.videoFPS.valueChanged.connect(self.videoFPS_valueChanged)
        self._form.videoFrames.valueChanged.connect(self.videoFrames_valueChanged)
        self._form.videoProgress.valueChanged.connect(self.videoProgress_valueChanged)
        self._form.videoProgress.sliderReleased.connect(self.videoProgress_sliderReleased)
        self._timer = QtCore.QTimer(self._form)
        self._timer.timeout.connect(self.updateFrame)

        self._currentFrame = None
        self._draw_on_video = True  # Controls if anything is drawn on the video
        self._videoFPS = None  # Sets the FPS rate at which the video is played
        


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
    def onKeyRelease(self): return self._videoWidget.onKeyRelease
    @onKeyRelease.setter
    def onKeyRelease(self, value): self._videoWidget.onKeyRelease = value

    @property
    def isPainted(self): return self._draw_on_video


    def processFrame(self, frame):
        return frame

    def updateFrame(self):
        (success, frame) = self.value.read()

        if frame!=None: self._currentFrame = frame

        frame = self.processFrame( self._currentFrame.copy() )
        if isinstance(frame, list) or isinstance(frame, tuple):
            self._videoWidget.paint( frame )
        else:
            self._videoWidget.paint( [frame] )

        if not self._form.videoProgress.isSliderDown():
            currentFrame = self.video_index

            self._form.videoProgress.setValue( currentFrame )
            if self._updateVideoFrame: self._form.videoFrames.setValue( currentFrame )

    def videoHideMarkers_clicked(self):
        """ Slot to hide or show stuff drawn on the video."""
        if self._form.videoHideMarkers.isChecked():
            self._draw_on_video = True
        else:
            self._draw_on_video = False
        self.refresh()
        # print "--->", self._draw_on_video

    def videoPlay_clicked(self):
        """Slot for Play/Pause functionality."""
        if self._form.videoPlay.isChecked():
            timeout_interval = (1000 / self._videoFPS)
            print "VIDEO PLAYING @", self._videoFPS, "FPS"
            self._timer.start(timeout_interval)
        else:
            print "VIDEO STOPPED"
            self._timer.stop()

    def pausePlay(self):
        if not self._form.videoPlay.isChecked():
            self._form.videoPlay.setChecked(True)
            timeout_interval = (1000 / self._videoFPS)
            print "VIDEO PLAYING @", self._videoFPS, "FPS"
            self._timer.start(timeout_interval)
        else:
            self._form.videoPlay.setChecked(False)
            print "VIDEO STOPPED"
            self._timer.stop()

    def videoFPS_valueChanged(self):
        """Get FPS rate from loaded video."""
        self._videoFPS = self._form.videoFPS.value()
        timeout_interval = (1000 / self._videoFPS)
        self._timer.setInterval(timeout_interval)
        print "VIDEO PLAYING @", self._videoFPS, "FPS"
    
    def save(self, data):
        if self.value: data['value'] = self.value.captureFrom

    def load(self, data):
        #if 'value' in data: self.value = data['value']
        pass

    def refresh(self):
        if self._currentFrame!=None:
            frame = self.processFrame( self._currentFrame.copy() )
            if isinstance(frame, list) or isinstance(frame, tuple):
                self._videoWidget.paint( frame )
            else:
                self._videoWidget.paint( [frame] )


    def convertFrameToTime(self, frame):
        currentMilliseconds = (frame / self.fps ) * 1000
        totalseconds = int(currentMilliseconds/1000)
        minutes = int(totalseconds / 60)
        seconds = totalseconds - (minutes*60)
        milliseconds = currentMilliseconds - (totalseconds*1000)
        return ( minutes, seconds, milliseconds )

    def videoProgress_valueChanged(self):
        ( minutes, seconds, milliseconds ) = self.convertFrameToTime( self._form.videoProgress.value() )
        self._form.videoTime.setText( "%02d:%02d:%03d" % ( minutes, seconds, milliseconds ) )

    _updateVideoFrame = True

    def videoProgress_sliderReleased(self):
        jump2Frame = self._form.videoProgress.value()
        self._value.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, jump2Frame)
        self._updateVideoFrame = False
        self._form.videoFrames.setValue( jump2Frame )
        self._value.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, jump2Frame)
        self._updateVideoFrame = True

    def videoFrames_valueChanged(self, i):
        if not self.isPlaying():
            jump2Frame = self._form.videoProgress.value()
            diff = jump2Frame-i

            self._value.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, jump2Frame-diff)
            self._updateVideoFrame = False
            self.updateFrame()
            self._updateVideoFrame = True

    def isPlaying(self):
        return self._timer.isActive()

    def updateControl(self):
        if self._value:
            self._form.videoControl.setEnabled(True)
            self._form.videoProgress.setMinimum(self._value.startFrame)
            self._form.videoProgress.setValue(self._value.startFrame)
            self._form.videoProgress.setMaximum(self._value.endFrame)
            self._form.videoFrames.setMinimum(self._value.startFrame)
            self._form.videoFrames.setValue(self._value.startFrame)
            self._form.videoFrames.setMaximum(self._value.endFrame)

    @property
    def value(self): return ControlBase.value.fget(self)

    @value.setter
    def value(self, value):
        self._videoWidget.reset()

        if value==0:
            self._value = cv2.OTVideoInput(0)
        elif isinstance(value, str) and value:
            self._value = cv2.VideoCapture(value)
            self.fps = self._value.get(cv2.cv.CV_CAP_PROP_FPS)
        else:
            self._value = None

        if self._value and value != 0:
            self._form.videoProgress.setMinimum( 0 )
            self._form.videoProgress.setValue( 0 )
            self._form.videoProgress.setMaximum( self._value.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT) )
            self._form.videoFrames.setMinimum( 0 )
            self._form.videoFrames.setValue( 0 )
            self._form.videoFrames.setMaximum( self._value.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT) )

        if self._value:
            self._form.videoControl.setEnabled(True)

        self.refresh()


    @property
    def startFrame(self):
        if self._value: return self._value.startFrame
        else: return -1

    @startFrame.setter
    def startFrame(self, value):
        if self._value:
            self._value.startFrame = value
            self._form.videoProgress.setMinimum(value)

    @property
    def endFrame(self):
        if self._value: return self._value.startFrame
        else: return -1

    @endFrame.setter
    def endFrame(self, value):

        if self._value:
            self._value.endFrame = value
            self._form.videoProgress.setValue(self._value.startFrame)
            self._form.videoProgress.setMaximum(value)

    @property
    def video_index(self):  return int(self._value.get(cv2.cv.CV_CAP_PROP_POS_FRAMES))-1

    @video_index.setter
    def video_index(self, value): self._value.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, value)

    @property
    def max(self): return int(self._value.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))


    @property
    def image(self): return self._currentFrame

    @image.setter
    def image(self, value):
        if isinstance(value, list) or isinstance(value, tuple):
            self._videoWidget.paint( value )
        else:
            self._videoWidget.paint( [value] )
        QApplication.processEvents()

    @property
    def fps(self): return self._videoFPS
    @fps.setter
    def fps(self, value):
        self._videoFPS = value
        if math.isnan(self._videoFPS): self._videoFPS = 15.0


    @property 
    def show_markers(self): return self._draw_on_video

    @property
    def helpText(self): return self._videoWidget._helpText
    @fps.setter
    def helpText(self, value): self._videoWidget._helpText = value