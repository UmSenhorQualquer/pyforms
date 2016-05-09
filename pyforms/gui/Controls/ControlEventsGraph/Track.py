from PyQt4 import QtGui
import bisect


class Track(object):

    DEFAULT_COLOR = QtGui.QColor(100, 100, 255)

    def __init__(self, parent):
        self._title = ''
        self._color = self.DEFAULT_COLOR
        self._parent = parent
        self._periods = []

    # Functions needed for the bisect insertion ############################
    def __len__(self): return len(self._periods)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return [self._periods[x] for x in range(*index.indices(len(self)))]
        return self._periods[index]

    def insert(self, item, index): self._periods.insert(item, index)
    ########################################################################

    def add_period(self, period):
        """
        The periods are added in a sorted way for rendering optimization
        """
        bisect.insort_right(self, period)
        return period

    def draw(self, painter, start, end, track_index):
        y = (track_index * self._parent.tracks_height) + 18
        painter.drawLine(start, y, end, y)

    def draw_periods(self, painter, start, end, track_index, left_shift=0, scale=1.0):
        top = track_index * self._parent.tracks_height + 20

        first_index = bisect.bisect(self, start)

        for period in self._periods[first_index:]:
            if period.begin > end:
                continue
            painter.setBrush(period.color)
            period.draw(painter, top=top, left_shift=left_shift, scale=scale)

    def clear(self):
        del self._periods[:]
        self._periods = []

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
    def properties(self): return ['T', self.title, self.color.name()]

    @properties.setter
    def properties(self, value):
        self.title = value[1]
        self.color = QtGui.QColor(value[2])
