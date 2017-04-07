# !/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from pysettings import conf

logger = logging.getLogger(__name__)

from pyforms.gui.Controls.ControlBase import ControlBase
from pyforms.utils import tools

try:
	import cv2
except:
	logger.warning("OpenCV not available")

if conf.PYFORMS_USE_QT5:
	from PyQt5 import uic

	try:
		import OpenGL.GL  as GL
		import OpenGL.GLU as GLU
		from PyQt5.QtOpenGL import QGLWidget
	except:
		logger.warning("No OpenGL library available")

else:
	from PyQt4 import uic

	try:
		import OpenGL.GL  as GL
		import OpenGL.GLU as GLU
		from PyQt4.QtOpenGL import QGLWidget
	except:
		logger.warning("No OpenGL library available")


class ImageGLWidget(QGLWidget):
	_image2Display = None
	_texture = None  #: Opengl texture variable
	_zoom = 1.0
	_mouseX = 0.0
	_mouseY = 0.0
	_width = 1.0
	_height = 1.0
	_glX = 0.0
	_glY = 0.0
	_glZ = 0.0
	_x = 0.0
	_y = 0.0
	_lastGlX = 0.0
	_lastGlY = 0.0
	_mouseDown = False
	_mouseLeftDown = False
	_mouseRightDown = False

	def __init__(self, parent=None):
		QGLWidget.__init__(self, parent)

		self._image2Display = []
		self._texture = []  #: Opengl texture variable
		self._zoom = 1.0
		self._mouseX = 0.0
		self._mouseY = 0.0
		self._width = 1.0
		self._height = 1.0
		self._glX = 0.0
		self._glY = 0.0
		self._glZ = 0.0
		self._x = 0.0
		self._y = 0.0
		self._lastGlX = 0.0
		self._lastGlY = 0.0
		self._mouseDown = False
		self._mouseLeftDown = False
		self._mouseRightDown = False

		self._mouseStartDragPoint = None

		self.setMinimumHeight(100)
		self.setMouseTracking(True)

	def initializeGL(self):
		GL.glClearDepth(1.0)
		GL.glClearColor(0, 0, 0, 1.0)
		GL.glEnable(GL.GL_DEPTH_TEST)

	def resizeGL(self, width, height):
		GL.glViewport(0, 0, width, height)
		GL.glMatrixMode(GL.GL_PROJECTION)
		GL.glLoadIdentity()
		if height>0: GLU.gluPerspective(40.0, float(width) / float(height), 0.01, 10.0)

	def drawVideo(self, width, height, x, y, z):
		GL.glPushMatrix()
		GL.glTranslatef(x, y, z)
		GL.glBegin(GL.GL_QUADS)
		GL.glTexCoord2f(0.0, 1.0);
		GL.glVertex3f(0, 0, 0);  # top left
		GL.glTexCoord2f(0.0, 0.0);
		GL.glVertex3f(0, height, 0);  # bottom left
		GL.glTexCoord2f(1.0, 0.0);
		GL.glVertex3f(width, height, 0);  # bottom right
		GL.glTexCoord2f(1.0, 1.);
		GL.glVertex3f(width, 0, 0);  # top right
		GL.glEnd()
		GL.glPopMatrix()

	def paintGL(self):
		GL.glClearColor(0.5, 0.5, 0.5, 1.0)
		GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
		GL.glMatrixMode(GL.GL_MODELVIEW)
		GL.glLoadIdentity()

		translateX = (len(self._texture) * self._width) / 2

		if len(self._texture) > 0:
			GL.glTranslatef(-translateX, -self._height / 2, -self._zoom)

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

			for texture_index in range(0, len(self._texture)):
				if texture_index > 0: GL.glTranslatef(self._width, 0, 0)

				GL.glBindTexture(GL.GL_TEXTURE_2D, self._texture[texture_index])

				if self._mouseRightDown:
					self.drawVideo(self._width, self._height, self._x - (self._lastGlX - self._glX),
					               self._y - (self._lastGlY - self._glY), 0.0)
				else:
					self.drawVideo(self._width, self._height, self._x, self._y, 0.0)

			if self._mouseDown:
				modelview = GL.glGetDoublev(GL.GL_MODELVIEW_MATRIX)
				projection = GL.glGetDoublev(GL.GL_PROJECTION_MATRIX)
				viewport = GL.glGetIntegerv(GL.GL_VIEWPORT)
				winX = float(self._mouseX);
				winY = float(viewport[3] - self._mouseY)
				winZ = GL.glReadPixels(winX, winY, 1, 1, GL.GL_DEPTH_COMPONENT, GL.GL_FLOAT)
				self._glX, self._glY, self._glZ = GLU.gluUnProject(winX, winY, winZ[0][0], modelview, projection,
				                                                   viewport)

	def reset(self):
		self._texture = []
		self._image2Display = []

	def paint(self, frames):
		if len(frames) == 0: return

		if len(self._image2Display) == 0:
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

		if len(self._texture) > len(frames):
			for i in range(len(self._texture) - len(frames)):
				GL.glDeleteTextures(self._texture.pop())

		self._image2Display = frames

		for index, frame in enumerate(frames):
			if len(frame.shape) == 2:
				color = GL.GL_LUMINANCE
			else:
				color = GL.GL_BGR

			if len(self._texture) < len(self._image2Display): self._texture.append(GL.glGenTextures(1))

			w = len(frame[0])
			h = len(frame)

			GL.glEnable(GL.GL_TEXTURE_2D)
			GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
			GL.glBindTexture(GL.GL_TEXTURE_2D, self._texture[index])
			GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_BORDER)
			GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_BORDER)
			GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
			GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
			GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, w, h, 0, color, GL.GL_UNSIGNED_BYTE, frame)

		self.repaint()

	def wheelEvent(self, event):
		if event.delta() < 0:
			self._zoom += 0.1
		else:
			self._zoom -= 0.1
		if self._zoom < 0.01: self._zoom = 0.02
		self.repaint()

	def mouseReleaseEvent(self, event):
		self._mouseDown = False

		if event.button() == 2:
			self._mouseRightDown = False
			self._x -= self._lastGlX - self._glX
			self._y -= self._lastGlY - self._glY
			self._lastGlX = self._glX
			self._lastGlY = self._glY

		if event.button() == 1:
			if self._mouseLeftDown:
				self.onEndDrag(self._mouseStartDragPoint, (self._glX - self._x, self._height - self._glY + self._y))
			self._mouseLeftDown = False

	def mousePressEvent(self, event):
		QGLWidget.mousePressEvent(self, event)
		self._mouseDown = True
		self._mouseX = event.x()
		self._mouseY = event.y()
		self.repaint()

		if event.button() == 1:
			self._mouseLeftDown = True
			self._mouseStartDragPoint = (self._glX - self._x, self._height - self._glY + self._y)

		if event.button() == 2:
			self._mouseRightDown = True
			self._lastGlX = self._glX
			self._lastGlY = self._glY

		self.onPress(event.button(), (self._glX - self._x, self._height - self._glY + self._y))

	def mouseMoveEvent(self, event):
		QGLWidget.mouseMoveEvent(self, event)
		self._mouseX = event.x()
		self._mouseY = event.y()
		self.repaint()
		self.onMove((self._glX - self._x, self._height - self._glY + self._y))

		if self._mouseDown:
			if self._mouseLeftDown:
				self.onDrag(self._mouseStartDragPoint, (self._glX - self._x, self._height - self._glY + self._y))

	def onMove(self, point):
		pass

	def onPress(self, button, point):
		pass

	def onDrag(self, startPoint, endPoint):
		pass

	def onEndDrag(self, startPoint, endPoint):
		pass


class ControlImage(ControlBase):
	_imageWidget = None

	def init_form(self):
		control_path = tools.getFileInSameDirectory(__file__, "image.ui")
		self._form = uic.loadUi(control_path)
		self._imageWidget = ImageGLWidget()
		self._form.imageLayout.addWidget(self._imageWidget)

	def save_form(self, data, path=None):
		if self.value != None: data['value'] = self._value

	def load_form(self, data, path=None):
		if 'value' in data: self.value = data['value']

	def repaint(self):
		self._imageWidget.repaint()

	@property
	def value(self):
		return ControlBase.value.fget(self)

	@value.setter
	def value(self, value):

		if isinstance(value, str):
			self._value = cv2.imread(value, 1)
		else:
			self._value = value

		if value is not None:
			if isinstance(self._value, list) or isinstance(self._value, tuple):
				self._imageWidget.paint(self._value)
			else:
				self._imageWidget.paint([self._value])

		self.changed_event()
