from PyQt4 import QtGui


class TimelineDelta(object):
    def __init__(self, begin, end=30, title=None, height=30, top=0, parent=None):
        self._top = top
        self._height = height
        self._parent = parent
        self._title = title
        self._lock = False
        if self.track not in parent._tracks_info.keys():
            self._defautcolor = parent._defautcolor
        else:
            self._defautcolor = parent._tracks_info[self.track][1]
        self._begin = begin
        self._end = end

        if self.track >= self._parent.numberoftracks:
            self._parent.numberoftracks = self.track + 1


    ######################################################################################
    #### HELPERS/FUNCTIONS ###############################################################
    ######################################################################################

    def collide(self, x, y):
        return self.begin <= x <= self.end and self._top <= y<= (self._top + self._height)

    def canSlideBegin(self, x, y):
        return not self._lock and x == int(round(self.begin)) and self._top <= y <= (self._top + self._height)

    def canSlideEnd(self, x, y):
        return not self._lock and int(round(self.end)) == x and self._top <= y <= (self._top + self._height)

    def moveEnd(self, x):
        """Move the right edge of the event rectangle."""
        # Do nothing if locked
        if self._lock:
            return

        #  Do nothing if trying to go over the pther edge
        if self._end <= self._begin - x and x < 0:
            return

        # Increment accordingly
        self._end += x / self._parent._scale

        # Minimum begin position is at 0
        if self._end > (self._parent.width() / self._parent._scale):
            self._end = (self._parent.width() / self._parent._scale)

    def moveBegin(self, x):
        """Move the left edge of the event rectangle."""
        # Do nothing if locked
        if self._lock:
            return

        #  Do nothing if trying to go over the other edge
        if self._begin >= self._end - x and x > 0:
            return

        # Increment accordingly
        self._begin += x / self._parent._scale

        # Minimum begin position is at 0
        if self._begin < 0:
            self._begin = 0

    def move(self, x, y):
        if self._lock: return
        if (self.begin + x) >= 0 and (self.end + x) <= self._parent.width():
            self._begin += x / self._parent._scale
            self._end += x / self._parent._scale
        current_track = self.track
        new_track = (y - 20) // 34
        if current_track != new_track and new_track >= 0 and new_track <= self._parent.numberoftracks:
            self.track = new_track
            if new_track >= self._parent.numberoftracks: self._parent.numberoftracks += 1

    def showEditWindow(self):
        text, ok = QtGui.QInputDialog.getText(self._parent, 'Edit event',  'Comment:', text=self._title)
        if ok: self._title = str(text)

    def draw(self, painter, showvalues = False):
        start, end = self.begin, self.end
        if self._lock:
            transparency = 0.1
        else:
            transparency = 0.5
        painter.setPen(QtGui.QColor(0, 0, 0))
        painter.setOpacity(transparency)
        painter.drawRoundedRect(start, self._top, end-start, self._height, 3,3)
        painter.setOpacity(1.0)

        painter.drawText(start+3, self._top+19, self._title )
        if showvalues:
            painter.drawText(start, self._top+44, "[%d;%d] delta:%d" % (self._begin, self._end, self._end-self._begin))


    ######################################################################################
    #### PROPERTIES ######################################################################
    ######################################################################################

    @property
    def lock(self): return self._lock
    @lock.setter
    def lock(self, value): self._lock = value

    @property
    def begin(self): return self._begin*self._parent._scale
    @begin.setter
    def begin(self, value):
        if self._lock: return
        self._begin = value/self._parent._scale
        if self._begin<0: self._begin=0

    @property
    def end(self): return self._end*self._parent._scale
    @end.setter
    def end(self, value):
        if self._lock: return
        self._end = value/self._parent._scale
        if self._end>(self._parent.width()/self._parent._scale):
            self._end=(self._parent.width()/self._parent._scale)

    @property
    def track(self):
        return (self._top - 20) // 34
    @track.setter
    def track(self, value):
        #FIXME This was preventing assigning a track when importing ingo locked
        # Is it needed?
        # if self._lock: return
        self._top = value * 34 + 20

    @property
    def color(self): return self._defautcolor
    @color.setter
    def color(self, value):
        if type(value)==str: self._defautcolor = QtGui.QColor(value)
        else: self._defautcolor = value

    # @property
    # def row(self):
    #     return [    int(round(self._begin)),
    #                 int(round(self._end)),
    #                 self._title,
    #                 self.track,
    #                 self._defautcolor.name(),
    #                 self._lock ]

    # @row.setter
    # def row(self, value):
    #     self._begin = int(value[0])
    #     self._end = int(value[1])
    #     self._title = value[2]
    #     self.track = int(value[3])
    #     self._defautcolor = QtGui.QColor(value[4])
    #     self._lock = value[5]=='True'

    #     if self.track>=self._parent.numberoftracks: self._parent.numberoftracks = self.track+1


    #TODO redefinition of the property above to write to file in the new format
    # This is a bad idea, better to access these individually
    @property
    def properties(self):
        return [self._lock,
                int(round(self._begin)),
                int(round(self._end)),
                self._title,
                self._defautcolor.name(),
                self.track]

    @properties.setter
    def properties(self, value):
        self._lock = value[0]=='True'
        self._begin = int(value[1])
        self._end = int(value[2])
        self._title = value[3]
        self._defautcolor = QtGui.QColor(value[4])
        self.track = int(value[5])

        if self.track >= self._parent.numberoftracks:
            self._parent.numberoftracks = self.track + 1














