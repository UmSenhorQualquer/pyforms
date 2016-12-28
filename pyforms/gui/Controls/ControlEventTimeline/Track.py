from PyQt4 import QtGui, QtCore

class Track(object):

    DEFAULT_COLOR = QtGui.QColor(100, 100, 255)

    def __init__(self, parent):
        self._title   = ''
        self._color   = self.DEFAULT_COLOR
        self._parent  = parent
        self._periods = []

    def __len__(self): return len(self._periods)

    @staticmethod
    def whichTrack(y): return (y - 20) // 34

    @staticmethod
    def whichTop(track): return track * 34 + 20


    @property
    def periods(self): return self._periods

    @property
    def color(self): return self._color
    @color.setter
    def color(self, value): self._color = value
    
    @property
    def title(self): return self._title
    @title.setter
    def title(self, value): self._title = value

    @property
    def events(self): return self._events

    def draw(self, painter, start, end, index):
        y = (index*34) + 18
        painter.drawLine(start, y, end, y)

    def drawPeriods(self, painter, start, end):
        for time in self._periods:
            painter.setBrush(time.color)
            time.draw(painter)

    def drawLabels(self, painter, index):
        painter.setPen(QtCore.Qt.black)
        painter.setOpacity(0.5)

        x0          = self._parent.visibleRegion().boundingRect().x()
        xmax        = self._parent.visibleRegion().boundingRect().width()
        text_length = painter.fontMetrics().width(self.title)
        x = 10
        y = (index * 34) + 30
        painter.drawText(x, y, self.title)
            
        painter.setOpacity(1.0)

    def selectDelta(self, x, y):
        for delta in self._periods:
            if delta.collide(x,y): return delta
        return None

    def clear(self): 
        del self._periods[:]
        self._periods = []


    @property
    def properties(self):
        return ['T',self.title,self.color.name()]

    @properties.setter
    def properties(self,value):
        self.title = value[1]
        self.color = QtGui.QColor(value[2])

    @property
    def track_index(self):
        for i, track in enumerate(self._parent._tracks):
            if track==self: return i
        return -1
    