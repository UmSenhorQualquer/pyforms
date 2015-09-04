#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


import pyforms.Utils.tools as tools
from PyQt4 import uic, QtGui,QtCore
from pyforms.gui.Controls.ControlBase import ControlBase

class GaugeWidgetVertical(ControlBase, QtGui.QWidget):

    def __init__(self, *args, **kwargs):
        super(GaugeWidgetVertical, self).__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.setMinimumWidth(30)

        self._lower = 0
        self._higher = 100
        self._minVal = 0
        self._maxVal = 75
        self._lastMouseY = None
        self._moving = False
        self._resizingBottom = False
        self._resizingTop = False


    def paintEvent(self,e):
        # call the base implementation to paint normal interface
        super(GaugeWidgetVertical, self).paintEvent(e)

        draw = QtGui.QPainter()
        draw.begin(self)

        w = self.width()-1
        diff = self._higher-self._lower
        self._step = float(self.height()) / float(diff)
        y_start = self.height()-(self._minVal-self._lower) * self._step
        y_end   = self.height()-(self._maxVal-self._lower) * self._step
        draw.setBrush(QtGui.QColor(100,100,255))
        draw.setPen(QtCore.Qt.NoPen )
        draw.drawRect(0, y_start, w, y_end-y_start)

        draw.setBrush(QtCore.Qt.NoBrush)
        draw.setPen(QtGui.QColor(200,200,255) )

        for i in range(self.height()/5,(self.height()-self.height()/5)+1, self.height()/5 ): 
            draw.drawLine(0,i,w,i)

        draw.setFont(QtGui.QFont('Decorative', 8))    
        draw.setPen(QtGui.QColor(30,30,30) )
        draw.drawText(3,self.height()-3, "%d" % self._lower )
        draw.drawText(3,10, "%d" % self._higher )

        draw.drawText(3, y_start+11, "%d" % self._minVal )
        draw.drawText(3, y_end-4, "%d" % self._maxVal )
    
        draw.end()




    def mousePressEvent(self, event):
        self._moving = False
        self._resizingBottom = False
        self._resizingTop = False

        y_start = self.height()-(self._minVal-self._lower) * self._step
        y_end   = self.height()-(self._maxVal-self._lower) * self._step
        
        if event.buttons()==QtCore.Qt.LeftButton:
            if y_start>event.y()>y_end: self._moving = True
            elif event.y()<y_end:       self._resizingTop = True
            elif y_start<event.y():     self._resizingBottom = True

    def mouseReleaseEvent(self, event):
        self._moving = False
        self._resizingBottom = False
        self._resizingTop = False        

    def mouseMoveEvent(self, event):
        super(GaugeWidgetVertical, self).mouseMoveEvent(event)
        
        y_start = self.height()-(self._minVal-self._lower) * self._step
        y_end   = self.height()-(self._maxVal-self._lower) * self._step
        
        if y_start<event.y() or event.y()<y_end:
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor ))
        else:
            self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor ))

        if event.buttons()==QtCore.Qt.LeftButton:
            if self._lastMouseY!=None:
                diff = self._lastMouseY - event.y()
                if diff!=0:
                    if self._moving:
                        new_min = self._minVal + diff * 1/self._step
                        new_max = self._maxVal + diff * 1/self._step
                        if new_min<new_max:
                            self._minVal = new_min
                            self._maxVal = new_max
                    elif self._resizingTop: 
                        new_max = self._maxVal + diff * 1/self._step
                        if self._minVal<new_max: self._maxVal = new_max
                    elif self._resizingBottom: 
                        new_min = self._minVal + diff * 1/self._step
                        if new_min<self._maxVal: self._minVal = new_min


                    #if self._maxVal>self._higher: self._higher=self._maxVal
                    #if self._minVal<self._lower:  self._lower=self._minVal

                    self.repaint()

                    self.changed()

            self._lastMouseY = event.y()

    def mouseReleaseEvent(self, event):
        self._lastMouseY = None








class GaugeWidgetHorizontal(GaugeWidgetVertical):

    def __init__(self, *args, **kwargs):
        super(GaugeWidgetHorizontal, self).__init__(*args, **kwargs)
        self.setMinimumHeight(30)



    def paintEvent(self,e):
        # call the base implementation to paint normal interface
        QtGui.QWidget.paintEvent(self,e); draw = QtGui.QPainter();draw.begin(self)
        
        h = self.height()-1
        diff = self._higher-self._lower
        self._step = float(self.width()) / float(diff)
        x_start = (self._minVal-self._lower) * self._step
        x_end   = (self._maxVal-self._lower) * self._step
        draw.setBrush(QtGui.QColor(100,100,255))
        draw.setPen(QtCore.Qt.NoPen )
        draw.drawRect(x_start, 0, x_end-x_start, h)

        draw.setBrush(QtCore.Qt.NoBrush)
        draw.setPen(QtGui.QColor(200,200,255) )

        for i in range(self.width()/5,(self.width()-self.width()/5)+1, self.width()/5 ): draw.drawLine(i,0,i,h)

        draw.setFont(QtGui.QFont('Decorative', 8))    
        draw.setPen(QtGui.QColor(30,30,30) )

        boundtext = draw.boundingRect( QtCore.QRectF(), "%d" % self._higher ) 
        draw.drawText(self.width()-boundtext.width(),15, "%d" % self._higher )
        draw.drawText(0,15, "%d" % self._lower )
        
        boundtext = draw.boundingRect( QtCore.QRectF(), "%d" % self._minVal ) 
        draw.drawText(x_start-2-boundtext.width(), 15, "%d" % self._minVal )
        draw.drawText(x_end + 2, 15, "%d" % self._maxVal )

    
        draw.end()


    def mousePressEvent(self, event):
        self._moving = False
        self._resizingBottom = False
        self._resizingTop = False

        x_start = (self._minVal-self._lower) * self._step
        x_end   = (self._maxVal-self._lower) * self._step
        
        if event.buttons()==QtCore.Qt.LeftButton:
            if x_start<event.x()<x_end: self._moving = True
            elif event.x()>x_end:       self._resizingTop = True
            elif x_start>event.x():     self._resizingBottom = True
    

    def mouseMoveEvent(self, event):
        super(GaugeWidgetVertical, self).mouseMoveEvent(event)
        
        x_start = (self._minVal-self._lower) * self._step
        x_end   = (self._maxVal-self._lower) * self._step
        
        if x_start>event.x() or event.x()>x_end: self.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor ))
        else:  self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor ))

        if event.buttons()==QtCore.Qt.LeftButton:
            if self._lastMouseY!=None:
                diff = self._lastMouseY - event.x()
                if diff!=0:
                    if self._moving:
                        new_min = self._minVal - diff * 1/self._step
                        new_max = self._maxVal - diff * 1/self._step
                        if new_min<new_max:
                            self._minVal = new_min
                            self._maxVal = new_max
                    elif self._resizingTop: 
                        new_max = self._maxVal - diff * 1/self._step
                        if self._minVal<new_max: self._maxVal = new_max
                    elif self._resizingBottom: 
                        new_min = self._minVal - diff * 1/self._step
                        if new_min<self._maxVal: self._minVal = new_min

                    self.repaint()
                    self.changed()

            self._lastMouseY = event.x()


















class ControlBoundingSlider(ControlBase):

    _min = 0
    _max = 100

    def __init__(self, label = "", defaultValue = [20,40], min = 0, max = 100, horizontal=False, **kwargs):
        #self._min = min
        #self._max = max
        #self.value = defaultValue
        self._horizontal = horizontal
        ControlBase.__init__(self, label, defaultValue, **kwargs)
        
    def initForm(self):
        if self._horizontal: self._form = GaugeWidgetHorizontal()
        else: self._form = GaugeWidgetVertical()

    def _update(self, minval, maxval):
        self.value = minval, maxval
        

    @property
    def value(self): 
        return self._form._minVal, self._form._maxVal

    @value.setter
    def value(self, value):
        ControlBase.value.fset(self, value)
        self._form._minVal, self._form._maxVal = value[0], value[1]
        

    @property
    def min(self): return self._form._lower

    @min.setter
    def min(self, value): 
        self._form._lower = value
        self._form.repaint()

    @property
    def max(self): return self._form._higher

    @max.setter
    def max(self, value): 
        self._form._higher = value
        self._form.repaint()