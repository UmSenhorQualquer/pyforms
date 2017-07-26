from pyforms.gui.Controls.ControlPlayer.AbstractGLWidget import AbstractGLWidget


from PyQt5 import QtGui
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5 import QtCore


class VideoQt5GLWidget(AbstractGLWidget, QOpenGLWidget):

	def initializeGL(self):
		self.gl = self.context().versionFunctions()
		self.gl.initializeOpenGLFunctions()

		
		'''
		 Sets up the OpenGL rendering context, defines display lists, etc. 
		 Gets called once before the first time resizeGL() or paintGL() is called.
		'''
		self.gl.glClearDepth(1.0)
		self.gl.glClearColor(0, 0, 0, 1.0)
		self.gl.glEnable(self.gl.GL_DEPTH_TEST)

	def perspective(self, fovy, aspect, zNear, zFar):
		ymax = zNear * math.tan( fovy * math.pi / 360.0 );
		ymin = -ymax;
		xmin = ymin * aspect;
		xmax = ymax * aspect;

		self.gl.glFrustum( xmin, xmax, ymin, ymax, zNear, zFar )

	def resizeGL(self, width, height):
		self.setupViewport(width, height)

	def setupViewport(self, width, height):
		side = min(width, height)
		self.gl.glViewport((width - side) // 2, (height - side) // 2, side,
				side)

		self.gl.glMatrixMode(self.gl.GL_PROJECTION)
		self.gl.glLoadIdentity()
		#self.gl.glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
		self.perspective(40.0, float(width) / float(height), 0.01, 10.0)
		self.gl.glMatrixMode(self.gl.GL_MODELVIEW)