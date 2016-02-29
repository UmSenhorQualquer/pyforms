#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.Controls.ControlPlayer.VideoGLWidget

"""

import logging
import pyforms.Utils.tools as tools
import math
from PyQt4 import uic
from PyQt4 import QtGui
from PyQt4.QtOpenGL import QGLWidget
from PyQt4 import QtCore
import OpenGL.GL as GL
import OpenGL.GLU as GLU
try:
    import cv2
except:
    print("Warning: was not possible to import cv2 in ControlPlayer")
from PyQt4.QtGui import QApplication

__author__ = "Ricardo Ribeiro"
__credits__ = ["Ricardo Ribeiro"]
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = "Ricardo Ribeiro"
__email__ = "ricardojvr@gmail.com"
__status__ = "Development"


class VideoGLWidget(QGLWidget):
    
    DRAG_MODE = False
    SHIFT_MODE = False
    ALLOW_ZOOM = True

    def __init__(self, parent=None):
        self.logger = logging.getLogger('pyforms')
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
        self._width = 1.0
        self._height = 1.0
        self._x = 0
        self._y = 0
        self.imgWidth = 1
        self.imgHeight = 1

        self._rotateZ = 0
        self._rotateX = 0

        self._mouseStartDragPoint = None
        # Message to show on the left corner of the screen
        self._helpText = None

        self.setMinimumHeight(100)

        self._point = None
        self._pendingFrames = None

    def initializeGL(self):
        '''
         Sets up the OpenGL rendering context, defines display lists, etc. 
         Gets called once before the first time resizeGL() or paintGL() is called.
        '''
        GL.glClearDepth(1.0)
        GL.glClearColor(0, 0, 0, 1.0)
        GL.glEnable(GL.GL_DEPTH_TEST)

    def resizeGL(self, width, height):
        '''
        Sets up the OpenGL viewport, projection, etc. 
        Gets called whenever the widget has been resized (and also when it is shown for 
        the first time because all newly created widgets get a resize event automatically).
        :param width:
        :param height:
        '''
        GL.glViewport(0, 0, width, height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective(40.0, float(width) / float(height), 0.01, 10.0)

    def drawVideo(self, _width, _height, x, y, z):
        # self.logger.debug("x: %s | y: %s | z: %s", x, y, z)
        GL.glPushMatrix()
        GL.glTranslatef(x, y, z)
        GL.glBegin(GL.GL_QUADS)
        GL.glTexCoord2f(0.0, 1.0)
        GL.glVertex3f(0, -_height / 2.0, 0)  # top left
        GL.glTexCoord2f(0.0, 0.0)
        GL.glVertex3f(0, _height / 2.0, 0)  # bottom left
        GL.glTexCoord2f(1.0, 0.0)
        GL.glVertex3f(_width, _height / 2.0, 0)  # bottom right
        GL.glTexCoord2f(1.0, 1.)
        GL.glVertex3f(_width, -_height / 2.0, 0)  # top right
        GL.glEnd()
        GL.glPopMatrix()

    def drawPyramid(self, size=0.01):
        """Draw a multicolored pyramid"""
        GL.glBegin(GL.GL_TRIANGLES)
        GL.glVertex3f(0.0, size, 0.0)
        GL.glVertex3f(-size, -size, size)
        GL.glVertex3f(size, -size, size)
        GL.glVertex3f(0.0, size, 0.0)
        GL.glVertex3f(size, -size, size)
        GL.glVertex3f(size, -size, -size)
        GL.glVertex3f(0.0, size, 0.0)
        GL.glVertex3f(size, -size, -size)
        GL.glVertex3f(-size, -size, -size)
        GL.glVertex3f(0.0, size, 0.0)
        GL.glVertex3f(-size, -size, -size)
        GL.glVertex3f(-size, -size, size)
        GL.glEnd()

    def paintGL(self):
        '''
        Renders the OpenGL scene. Gets called whenever the widget needs to be updated.
        '''
        GL.glClearColor(0.5, 0.5, 0.5, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

        # Correct a bug related with the overlap of contexts between simultaneous OpenGL windows.
        if self._pendingFrames != None:
            for index, frame in enumerate(self._pendingFrames):
                if len(frame.shape) == 2:
                    color = GL.GL_LUMINANCE
                else:
                    color = GL.GL_BGR

                if len(self.texture) < len(self.image2Display):
                    self.texture.append(GL.glGenTextures(1))

                w = len(frame[0])
                h = len(frame)

                GL.glEnable(GL.GL_TEXTURE_2D)
                GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
                GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture[index])
                GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_BORDER)
                GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_BORDER)
                GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
                GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
                GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, w, h, 0, color, GL.GL_UNSIGNED_BYTE, frame)
            self._pendingFrames = None

        translateX = (len(self.texture) * self._width) / 2

        if len(self.texture) > 0:
            GL.glTranslatef(-translateX, 0, -self.zoom)

            if self._point is not None:
                GL.glColor4f(0, 0, 1, 1.0)
                GL.glPushMatrix()
                GL.glTranslatef(self._point[0], self._point[1], self._point[2])
                self.drawPyramid()
                GL.glPopMatrix()
                GL.glColor4f(1, 1, 1, 1.0)

            GL.glRotatef(self._rotateX, -1, 0, 0)
            GL.glRotatef(self._rotateZ, 0, 0, 1)

            GL.glDisable(GL.GL_TEXTURE_2D)
            GL.glColor4f(0.5, 0.5, 0.5, 1.0)
            GL.glBegin(GL.GL_QUADS)
            GL.glVertex3f(20, -20, -.01)
            GL.glVertex3f(20, 20, -.001)
            GL.glVertex3f(-20, 20, -.001)
            GL.glVertex3f(-20, -20, -.001)
            GL.glEnd()

            GL.glColor4f(1, 1, 1, 1.0)

            if self._mouseDown:
                modelview = GL.glGetDoublev(GL.GL_MODELVIEW_MATRIX)
                projection = GL.glGetDoublev(GL.GL_PROJECTION_MATRIX)
                viewport = GL.glGetIntegerv(GL.GL_VIEWPORT)
                winX = float(self._mouseX)
                winY = float(viewport[3] - self._mouseY)
                winZ = GL.glReadPixels(
                    winX, winY, 1, 1, GL.GL_DEPTH_COMPONENT, GL.GL_FLOAT)
                self._glX, self._glY, self._glZ = GLU.gluUnProject(
                    winX, winY, winZ[0][0], modelview, projection, viewport)
                # self.logger.debug("Paint GL mouse down")
                # self.logger.debug("%s", "GLX: {0} | GLY: {1}".format(self._glX, self._glY))

            GL.glEnable(GL.GL_TEXTURE_2D)
            GL.glDisable(GL.GL_DEPTH_TEST)

            for texture_index in range(0, len(self.texture)):
                if texture_index > 0:
                    GL.glTranslatef(self._width, 0, 0)

                GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture[texture_index])

                if self._mouseRightDown:
                    self.drawVideo(self._width, self._height, self._x - (self._lastGlX - self._glX), self._y - (self._lastGlY - self._glY), 0.0)
                elif self._mouseLeftDown and self.DRAG_MODE:
                    self.drawVideo(self._width, self._height, self._x - (self._lastGlX - self._glX), self._y - (self._lastGlY - self._glY), 0.0)
                else:
                    self.drawVideo(self._width, self._height, self._x, self._y, 0.0)

            GL.glEnable(GL.GL_DEPTH_TEST)

        if self._helpText is not None:
            self.qglColor(QtCore.Qt.white)
            self.renderText(4, 15, self._helpText)

    def reset(self):
        self.texture = []
        self.image2Display = []

    def paint(self, frames):

        if len(self.image2Display) == 0:
            self.imgHeight, self.imgWidth = frames[0].shape[:2]
            if self.imgWidth > self.imgHeight:
                self._width = 1
                self._height = float(self.imgHeight) / float(self.imgWidth)
                self._x = -float(self._width) / 2
                self._y = 0
            else:
                self._height = 1
                self._width = float(self.imgWidth) / float(self.imgHeight)
                self._y = 0.5

        # self._x = -self._width/2
        
        if len(self.texture) > len(frames):
            for i in range(len(self.texture) - len(frames)):
                GL.glDeleteTextures(self.texture.pop())

        self.image2Display = frames
        self._pendingFrames = frames

        self.updateGL()

    def wheelEvent(self, event):
        if self.ALLOW_ZOOM:
            self._mouseX = event.x()
            self._mouseY = event.y()
            zoom_factor = 0.03
            if event.delta() < 0:
                self.zoom -= zoom_factor
            else:
                self.zoom += zoom_factor
            if self.zoom < 0.01:
                self.zoom = 0.02
            # self.logger.debug("Wheel event | Delta: %s | Zoom factor: %s", event.delta(), zoom_factor)
            self.updateGL()

    def mouseDoubleClickEvent(self, event):
        self._mouseX = event.x()
        self._mouseY = event.y()
        self.updateGL()
        if hasattr(self, 'imgWidth'):
            self.onDoubleClick(event, self._get_current_x(), self._get_current_y())

    def mouseReleaseEvent(self, event):
        self._mouseDown = False

        if event.button() == 4:
            self._mouseRightDown = False
            self._x -= self._lastGlX - self._glX
            self._y -= self._lastGlY - self._glY
            self._lastGlX = self._glX
            self._lastGlY = self._glY

        if event.button() == 1:
            if hasattr(self, 'imgWidth') and self._mouseLeftDown:
                if self.DRAG_MODE:
                    pass
                    #self._x -= self._lastGlX - self._glX
                    #self._y -= self._lastGlY - self._glY
                    #self._lastGlX = self._glX
                    #self._lastGlY = self._glY

                self.onEndDrag(self._mouseStartDragPoint, self._get_current_mouse_point())
            self._mouseLeftDown = False

    def mousePressEvent(self, event):
        super(QGLWidget, self).mousePressEvent(event)
        self.setFocus(QtCore.Qt.MouseFocusReason)

        self._mouseDown = True
        # self.logger.debug("%s", "Mouse press (before) event: X ({0}) Y ({1})".format(self._mouseX, self._mouseY))
        # self.logger.debug("OpenGL coordinates: %s", 'X ({0}) Y ({1})'.format(self._glX, self._glY))
        self._mouseX = event.x()
        self._mouseY = event.y()

        self.updateGL()
        # self.logger.debug("%s", "Mouse press (after) event: X ({0}) Y ({1})".format(self._mouseX, self._mouseY))
        # self.logger.debug("OpenGL coordinates: %s", 'X ({0}) Y ({1})'.format(self._glX, self._glY))

        if hasattr(self, 'imgWidth'):
            self.onClick(event, self._get_current_x(), self._get_current_y())

        if event.button() == 1:
            self._mouseLeftDown = True
            # self.logger.debug("glx: %s | x: %s | gly: %s | y: %s | imgWdith: %s | imgHeight: %s | height: %s", self._glX, self._x, self._glY, self._y, self.imgWidth, self.imgHeight, self._height)
            self._mouseStartDragPoint = self._get_current_mouse_point()
            
            if self.DRAG_MODE:
                #self._x -= self._lastGlX - self._glX
                #self._y -= self._lastGlY - self._glY
                self._lastGlX = self._glX
                self._lastGlY = self._glY

            # self.logger.debug("Button 1 pressed")
        if event.button() == 4:
            self._mouseRightDown = True
            self._lastGlX = self._glX
            self._lastGlY = self._glY

    def mouseMoveEvent(self, event):
        self.setFocus(QtCore.Qt.MouseFocusReason)

        self._mouseX = event.x()
        self._mouseY = event.y()
        # self.updateGL()
        if self._mouseLeftDown and self._mouseDown:
            self.updateGL()
            p1 = self._mouseStartDragPoint
            p2 = self._get_current_mouse_point()
            self.onDrag(p1, p2)

        if self._mouseRightDown and self._mouseDown:
            self.updateGL()
            p1 = self._mouseStartDragPoint
            p2 = self._get_current_mouse_point()
            self.onDrag(p1, p2)

            
    def keyPressEvent(self, event):
        super(QGLWidget, self).keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Control:
            self.DRAG_MODE = True
            self.ALLOW_ZOOM = False
            # self.logger.debug("Enabled drag mode")
            
        if event.key() == QtCore.Qt.Key_Shift:
            # self.logger.debug("Enabled shift mode")
            self.SHIFT_MODE = True
            self.ALLOW_ZOOM = False


    def keyReleaseEvent(self, event):
        super(QGLWidget, self).keyReleaseEvent(event)
        # Control video playback using the space bar to Play/Pause
        if event.key() == QtCore.Qt.Key_Space:
            self._control.pausePlay()
        # Jumps 1 frame forward
        if event.key() == QtCore.Qt.Key_D:
            self._control.video_index += 1
            self._control.updateFrame()

        # Jumps 1 frame backwards
        if event.key() == QtCore.Qt.Key_A:
            self._control.video_index -= 1
            self._control.updateFrame()
            
        if event.key() == QtCore.Qt.Key_Control:
            self.DRAG_MODE = False
            self.ALLOW_ZOOM = True
            self._x -= self._lastGlX - self._glX
            self._y -= self._lastGlY - self._glY
            # self.logger.debug("Disabled drag mode")

        if event.key() == QtCore.Qt.Key_Shift:
            self.SHIFT_MODE = False
            self.ALLOW_ZOOM = True
            # self.logger.debug("Disabled shift mode")

        self.onKeyRelease(event)

    def onDoubleClick(self, event, x, y): pass

    def onClick(self, event, x, y): pass

    def onDrag(self, startPoint, endPoint): pass

    def onEndDrag(self, startPoint, endPoint): pass

    def onKeyRelease(self, event): pass

    @property
    def rotateX(self): return self._rotateX

    @rotateX.setter
    def rotateX(self, value):
        self._rotateX = value
        self.updateGL()

    @property
    def rotateZ(self): return self._rotateZ

    @rotateZ.setter
    def rotateZ(self, value):
        self._rotateZ = value
        self.updateGL()
        
    def _get_current_mouse_point(self):
        '''
        
        '''
        return self._get_current_x(), self._get_current_y() 

    def _get_current_x(self):
        return (self._glX - self._x) * float(self.imgWidth)
    
    def _get_current_y(self):
        return (self._height - self._glY + self._y) * float(self.imgWidth) - self.imgHeight / 2.0

    @property
    def point(self): return self._point

    @point.setter
    def point(self, value):
        if hasattr(self, 'imgWidth'):
            x = value[0] / float(self.imgWidth)  # +self._x
            y = -value[1] / float(self.imgWidth)  # -self._y-self._height)
            z = 0.1  # value[2]
            self._point = x, y, z
