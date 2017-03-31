#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.Controls.ControlPlayer.VideoGLWidget

"""

import logging
import pyforms.utils.tools as tools
import math
from PyQt4 import uic
from PyQt4 import QtGui
from PyQt4.QtOpenGL import QGLWidget
from PyQt4 import QtCore
import OpenGL.GL as GL
import OpenGL.GLU as GLU
from pysettings import conf
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

	def __init__(self, parent=None):
		self.logger = logging.getLogger('pyforms')
		QGLWidget.__init__(self, parent)
		self.image_2_display = []
		self.textures = []
		self.setMouseTracking(True)
		self.zoom = 0.0
		self._mouseX = 0.0
		self._mouseY = 0.0
		
		#These variable are updated everytime the opengl scene is rendered 
		#and a mouse button is down
		self._glX = 0.0
		self._glY = 0.0
		self._glZ = 0.0

		#Last mouse opengl calculated position
		#This variable is updated everytime the opengl scene is rendered
		#and a mouse button is down
		self._last_mouse_gl_pos = None

		self._lastGlX = 0.0 #Last 
		self._lastGlY = 0.0
		self._mouseDown = False
		self._mouseLeftDown = False
		self._move_img 	= False
		self._width 	= 1.0
		self._height 	= 1.0
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
		self._pending_frames = []

		self._tmp_msg = None

		self._font = QtGui.QFont()
		self._font.setPointSize(conf.PYFORMS_CONTROLPLAYER_FONT)


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

	def draw_video(self, width, height, x, y, z):
		# self.logger.debug("x: %s | y: %s | z: %s", x, y, z)
		GL.glPushMatrix()
		GL.glTranslatef(x, y, z)

		GL.glBegin(GL.GL_QUADS)
		GL.glTexCoord2f(0.0, 1.0)
		GL.glVertex3f(0, -height / 2.0, 0)  # top left
		GL.glTexCoord2f(0.0, 0.0)
		GL.glVertex3f(0, height / 2.0, 0)  # bottom left
		GL.glTexCoord2f(1.0, 0.0)
		GL.glVertex3f(width, height / 2.0, 0)  # bottom right
		GL.glTexCoord2f(1.0, 1.)
		GL.glVertex3f(width, -height / 2.0, 0)  # top right
		GL.glEnd()
		GL.glPopMatrix()

	def draw_pyramid(self, size=0.01):
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
		for index, frame in enumerate(self._pending_frames):

			#if self.zoom>=0:
			#	frame = cv2.resize(frame, (int(frame.shape[0]/(2*(1-self.zoom))),int( frame.shape[1]/(2*(1-self.zoom))) ))
			
			color = GL.GL_LUMINANCE if len(frame.shape) == 2 else GL.GL_BGR
			w, h = len(frame[0]), len(frame) #Size of the image

			if len(self.textures)<len(self.image_2_display): self.textures.append(GL.glGenTextures(1))

			#Load the textures to opengl
			GL.glEnable(GL.GL_TEXTURE_2D)
			GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
			GL.glBindTexture(GL.GL_TEXTURE_2D, self.textures[index])
			GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_BORDER)
			GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_BORDER)
			GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
			GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
			GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, w, h, 0, color, GL.GL_UNSIGNED_BYTE, frame)

		self._pending_frames = []
		
		
		GL.glTranslatef(0, 0, -1)
		GL.glTranslatef(0, 0, -self.zoom)
		
		if len(self.image_2_display)>1: 
			#in case of having more images to display, it centers the images
			translate_x = float( (len(self.image_2_display)-1) * self._width) / 2.0
			GL.glTranslatef(-translate_x, 0, 0)

		if self._point is not None:
			GL.glColor4f(0, 0, 1, 1.0)
			GL.glPushMatrix()
			GL.glTranslatef(self._point[0], self._point[1], self._point[2])
			self.draw_pyramid()
			GL.glPopMatrix()
			GL.glColor4f(1, 1, 1, 1.0)

		GL.glRotatef(self._rotateX, -1, 0, 0)
		GL.glRotatef(self._rotateZ, 0, 0, 1)

		GL.glDisable(GL.GL_TEXTURE_2D)
		GL.glColor4f(0, 0, 0, .0)
		GL.glBegin(GL.GL_QUADS)
		GL.glVertex3f(20, -20, -.01)
		GL.glVertex3f(20, 20, -.001)
		GL.glVertex3f(-20, 20, -.001)
		GL.glVertex3f(-20, -20, -.001)
		GL.glEnd()

		GL.glColor4f(1, 1, 1, 1.0)

		if self._mouseDown:
			modelview 	= GL.glGetDoublev(GL.GL_MODELVIEW_MATRIX)
			projection	= GL.glGetDoublev(GL.GL_PROJECTION_MATRIX)
			viewport 	= GL.glGetIntegerv(GL.GL_VIEWPORT)
			
			winX 		= float(self._mouseX)
			winY 		= float(viewport[3] - self._mouseY)
			winZ 		= GL.glReadPixels( winX, winY, 1, 1, GL.GL_DEPTH_COMPONENT, GL.GL_FLOAT)

			self._glX, self._glY, self._glZ = GLU.gluUnProject( winX, winY, winZ[0][0], modelview, projection, viewport)
			
			if not self._last_mouse_gl_pos: self._last_mouse_gl_pos = self._glX, self._glY, self._glZ
			

		GL.glEnable(GL.GL_TEXTURE_2D)
		GL.glDisable(GL.GL_DEPTH_TEST)

		if self._move_img:
			self._x -= (self._last_mouse_gl_pos[0]-self._glX)
			self._y -= (self._last_mouse_gl_pos[1]-self._glY)

		for texture_index in range(0, len(self.image_2_display)):
			if texture_index>0: GL.glTranslatef(self._width, 0, 0)
			GL.glBindTexture(GL.GL_TEXTURE_2D, self.textures[texture_index])

			self.draw_video(self._width, self._height, self._x, self._y, 0.0)

		GL.glEnable(GL.GL_DEPTH_TEST)

		if self._helpText is not None:
			self.qglColor(QtCore.Qt.black)
			self.renderText(5, 31, self._helpText, font=self._font)
			self.qglColor(QtCore.Qt.white)
			self.renderText(4, 30, self._helpText, font=self._font)
			

		if self._tmp_msg is not None:
			self.qglColor(QtCore.Qt.black)
			self.renderText(5, self.height()-19, self._tmp_msg, font=self._font)
			self.qglColor(QtCore.Qt.white)
			self.renderText(4, self.height()-20, self._tmp_msg, font=self._font)

		if self._move_img: 
			self._last_mouse_gl_pos = self._glX, self._glY, self._glZ

		

	def reset(self):
		self.textures = []
		self._pending_frames = []
		self.image_2_display = []

	def show_tmp_msg(self, msg, timeout=2000):
		self._tmp_msg = msg
		self.updateGL()
		QtCore.QTimer.singleShot(2000, self.__hide_tmp_msg )


	def paint(self, frames):
		if frames is None:
			self.reset()
			self.updateGL()
			return
		elif self.image_2_display is None or len(self.image_2_display) == 0:
			self.imgHeight, self.imgWidth = frames[0].shape[:2]
			if self.imgWidth >= self.imgHeight:
				self._width = 1
				self._height = float(self.imgHeight) / float(self.imgWidth)
				self._x = -float(self._width) / 2
				self._y = 0
			else:
				self._height = 1
				self._width = float(self.imgWidth) / float(self.imgHeight)
				self._y = 0.5

		self.image_2_display = frames
		self._pending_frames = frames
		self.updateGL()

	def wheelEvent(self, event):
		
		if not self._move_img:
			# Zoom the video
			self._mouseX = event.x()
			self._mouseY = event.y()

			zoom_factor = event.delta() / float(1500)

			self.zoom += zoom_factor

			if self.zoom < -.98 and event.delta() < 0:
				self.zoom = -0.98

			if self.zoom > 7 and event.delta() > 0: # zoom limits
				self.zoom = 7

			# self.logger.debug("Wheel event | Current zoom: %s | Delta: %s | Zoom factor: %s", self.zoom, event.delta(), zoom_factor)
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
			self._move_img = False
			

		if event.button() == 1:
			if hasattr(self, 'imgWidth') and self._mouseLeftDown:
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

			# self.logger.debug("Button 1 pressed")
		if event.button() == 4:
			self._move_img = True
			self._last_mouse_gl_pos = None
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

		if self._move_img and self._mouseDown:
			self.updateGL()
			p1 = self._mouseStartDragPoint
			p2 = self._get_current_mouse_point()
			self.onDrag(p1, p2)

	def keyPressEvent(self, event):
		super(QGLWidget, self).keyPressEvent(event)

		#Set the flag move_img to true, for the image position to be updated
		if event.key() == QtCore.Qt.Key_M: self._move_img = True

	def keyReleaseEvent(self, event):
		super(QGLWidget, self).keyReleaseEvent(event)

		# Control video playback using the space bar to Play/Pause
		if event.key() == QtCore.Qt.Key_Space:

			if self._control.is_playing:
				self._control.stop()
			else:
				self._control.play()

		# Jumps 1 frame forward
		if event.key() == QtCore.Qt.Key_D:
			self._control.video_index += 1
			self._control.update_frame()

		# Jumps 1 frame backwards
		if event.key() == QtCore.Qt.Key_A:
			self._control.video_index -= 1
			self._control.update_frame()

		# Jumps 20 seconds forward
		if event.key() == QtCore.Qt.Key_C:
			self._control.video_index += 20*self._control.fps
			self._control.update_frame()

		# Jumps 20 seconds backwards
		if event.key() == QtCore.Qt.Key_Z:
			self._control.video_index -= 20*self._control.fps
			self._control.update_frame()

		if event.key() == QtCore.Qt.Key_M: self._move_img = False

		if event.key() == QtCore.Qt.Key_1: 
			self._control.speed = 1
			self.show_tmp_msg('Speed: 1x')

		if event.key() == QtCore.Qt.Key_2: 
			self._control.speed = 2
			self.show_tmp_msg('Speed: 2x')

		if event.key() == QtCore.Qt.Key_3: 
			self._control.speed = 3
			self.show_tmp_msg('Speed: 3x')

		if event.key() == QtCore.Qt.Key_4: 
			self._control.speed = 4
			self.show_tmp_msg('Speed: 4x')

		if event.key() == QtCore.Qt.Key_5: 
			self._control.speed = 5
			self.show_tmp_msg('Speed: 5x')

		if event.key() == QtCore.Qt.Key_6: 
			self._control.speed = 6
			self.show_tmp_msg('Speed: 6x')

		if event.key() == QtCore.Qt.Key_7: 
			self._control.speed = 7
			self.show_tmp_msg('Speed: 7x')

		if event.key() == QtCore.Qt.Key_8: 
			self._control.speed = 8
			self.show_tmp_msg('Speed: 8x')

		if event.key() == QtCore.Qt.Key_9: 
			self._control.speed = 9
			self.show_tmp_msg('Speed: 9x')

		
		self.on_key_release(event)


	def __hide_tmp_msg(self): 
		self._tmp_msg = None
		self.updateGL()

	def onDoubleClick(self, event, x, y): pass

	def onClick(self, event, x, y): pass

	def onDrag(self, startPoint, endPoint): pass

	def onEndDrag(self, startPoint, endPoint): pass

	def on_key_release(self, event): pass

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
