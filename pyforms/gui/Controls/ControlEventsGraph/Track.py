from PyQt4 import QtGui, QtCore
import bisect

class Track(object):

    DEFAULT_COLOR = QtGui.QColor(100, 100, 255)

    def __init__(self, parent):
        self._title   = ''
        self._color   = self.DEFAULT_COLOR
        self._parent  = parent
        self._periods = []

    #Functions needed for the bisect module
    def __len__(self):              return len(self._periods)
    def __getitem__(self, index):
        if isinstance(index, slice):
            return [self._periods[x].end for x in range(*index.indices(len(self)))]
        return self._periods[index].end

    def add_period(self, period ):
        """
        The periods are added in a sorted way for rendering optimization
        """
        start_index = bisect.bisect(self, period.end)
        insert_index = start_index
        for index in range(start_index, len(self._periods)):
            p = self._periods[index]
            if period.begin<=p.begin: insert_index = index

        self.periods.insert(insert_index, period)

    def whichTrack(self, y): return (y - 20) // self._parent.tracks_height

    def whichTop(self, track): return track * self._parent.tracks_height + 20


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

    def draw(self, painter, start, end, track_index):
        y = (track_index*self._parent.tracks_height) + 18
        painter.drawLine(start, y, end, y)

    def drawPeriods(self, painter, start, end, track_index, left_shift=0):
        top = track_index*self._parent.tracks_height + 20

        first_index = bisect.bisect(self, start)
        for period in self._periods[first_index:]:
            if period.begin>end: break
            painter.setBrush(period.color)
            period.draw(painter, top=top, left_shift=left_shift)

    def drawLabels(self, painter, track_index):
        painter.setPen(QtCore.Qt.black)
        painter.setOpacity(0.5)

        x0          = self._parent.visibleRegion().boundingRect().x()
        xmax        = self._parent.visibleRegion().boundingRect().width()
        text_length = painter.fontMetrics().width(self.title)
        x = 10
        y = (track_index * self._parent.tracks_height) + 30
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