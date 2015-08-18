from pyforms.gui.Controls.ControlBase import ControlBase

try:
	from OpenGL.GL  import *
	from OpenGL.GLU import *
	from PyQt4.QtOpenGL import QGLWidget
except:
	print ("No OpenGL library available")



class OpenglGLWidget(QGLWidget):

	def __init__(self, parent=None):
		QGLWidget.__init__(self, parent)

		self._zoom = 1.0
		self._scene = None
		self._rotation = [0, 0, 0]
		
		self._mouseLeftDown     = False
		self._mouseRightDown    = False

		self._mouseGLPosition       = [0,0,0]
		self._lastMouseGLPosition   = [0,0,0]

		self._mousePosition         = [0,0]  #Current mouse position
		self._lastMousePosition     = [0,0]  #Last mouse position

		self._mouseStartDragPoint   = None
		
		self.setMinimumHeight(100)
		self.setMinimumWidth(100)
		self.setMouseTracking(True)

	def initializeGL(self):
		glClearDepth(1.0)
		glClearColor(0, 0, 0, 1.0)
		#glDisable(GL_CULL_FACE)
		#glEnable(GL_DEPTH_TEST)
		#glDisable(GL_DEPTH_TEST)

		
		#glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		#glBlendFunc(GL_ONE_MINUS_DST_ALPHA,GL_DST_ALPHA)
		glBlendFunc(GL_SRC_ALPHA,GL_ONE)
		glEnable( GL_BLEND )
		
	def resizeGL(self, width, height):
		glViewport(0, 0, width, height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(65.0, float(width)/float(height), 0.01, 800.0)


	def paintGL(self):
		glClearColor(0.0, 0.0, 0.0, 1.0)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		glBlendFunc(GL_SRC_ALPHA,GL_ONE)
		glEnable( GL_BLEND )

		glScalef(1,-1,-1)

		glTranslatef( 0, 0, self._zoom)
		glRotatef( self._rotation[0], 1,0,0 )
		glRotatef( self._rotation[1], 0,1,0 )
		glRotatef( self._rotation[2], 0,0,1 )



		if self._scene!=None: self._scene.DrawGLScene()
			

		if self.mouseDown:
			#Get mouse position
			modelview, projection = glGetDoublev( GL_MODELVIEW_MATRIX ), glGetDoublev( GL_PROJECTION_MATRIX )
			viewport = glGetIntegerv( GL_VIEWPORT )
			winX, winY = float(self._mousePosition[0]), float(viewport[3] - self._mousePosition[1])
			winZ = glReadPixels(winX, winY, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
			self._mouseGLPosition = gluUnProject( winX, winY, winZ[0][0], modelview, projection, viewport)
	 
	def __updateMouse(self, event, pressed = None):
		self._mousePosition[0] = event.x()
		self._mousePosition[1] = event.y()

		if pressed!=None:
			if event.button()==2: self._mouseRightDown = pressed
			if event.button()==1: self._mouseLeftDown  = pressed

	def wheelEvent(self, event):
		if event.delta()<0: self._zoom += 1
		else: self._zoom -= 1

		self.repaint()
	
	def mouseReleaseEvent(self, event):
		self.__updateMouse(event)
		
		if self._mouseRightDown:
			self._lastMouseGLPosition = self._mouseGLPosition
			self._mouseRightDown = False

		if self._mouseLeftDown:
			self.onEndDrag( self._mouseStartDragPoint, self._mouseGLPosition )
			self._mouseLeftDown = False


			
	def mousePressEvent(self, event):
		QGLWidget.mousePressEvent(self, event)
		self.__updateMouse(event, pressed = True)
		self.repaint()

		if self._mouseLeftDown:  self._mouseStartDragPoint = self._mouseGLPosition
		if self._mouseRightDown: self._lastMouseGLPosition = self._mouseGLPosition

		self.onPress( event.button(), self._mousePosition, self._mouseGLPosition )
			
	def mouseMoveEvent(self, event):
		QGLWidget.mouseMoveEvent(self, event)
		self.__updateMouse(event)
		self.repaint()

		self.onMove( (self._mouseGLPosition[0], self._mouseGLPosition[1] ) )

		if self.mouseDown:
			if self._mouseLeftDown:
				#p = self._mouseGLPosition[0] - self._x, self._mouseGLPosition[1] + self._y
				#p = self._mouseGLPosition[0], self._mouseGLPosition[1]
				self.onDrag(self._lastMousePosition, self._mousePosition)
	   
		self._lastMousePosition = list(self._mousePosition)

	def onMove(self, point):
		pass

	def onPress(self, button, point, glpoint=None):
		pass


	def onDrag(self, startPoint, endPoint, startGLPoint=None, endGLPoint=None):
		movX, movY = endPoint[0]-startPoint[0], endPoint[1]-startPoint[1]
		self._rotation[2] -= float(movX)*0.15
		self._rotation[0] += float(movY)*0.15
		
	def onEndDrag(self, startPoint, endPoint, startGLPoint=None, endGLPoint=None):
		pass

	##############################################################################
	###### Properties ############################################################
	##############################################################################

	@property
	def scene(self): return self._scene
	@scene.setter
	def scene(self, value): self._scene = value

	@property
	def mouseDown(self): return self._mouseLeftDown or self._mouseRightDown
	
	
	def resetZoomAndRotation(self): self._zoom, self._rotation = 0.0, [0,0,0]
		 














class ControlOpenGL(ControlBase):


	def initForm(self): self._form = OpenglGLWidget()

	@property
	def value(self): return self._form.scene

	@value.setter
	def value(self, value):  self._form.scene = value; self._form.repaint()

	def repaint(self): self._form.repaint()


	def resetZoomAndRotation(self): self._form.resetZoomAndRotation()


	@property
	def width(self): return self._form.width()
	@property
	def height(self): return self._form.height()
	