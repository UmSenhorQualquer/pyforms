#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.Controls.ControlEventsGraph.EventsWidget

"""

from PyQt4 import QtGui, QtCore
from pyforms.gui.Controls.ControlEventsGraph.Track import Track
from pyforms.gui.Controls.ControlEventsGraph.TimelinePointer import TimelinePointer
from pyforms.gui.Controls.ControlEventsGraph.TimelineDelta import TimelineDelta


__author__  = ["Ricardo Ribeiro"]
__credits__ = ["Ricardo Ribeiro"]
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = "Ricardo Ribeiro"
__email__ = "ricardojvr@gmail.com"
__status__ = "Development"


class EventsWidget(QtGui.QWidget):
    """
    Timeline widget definition to be used in the ControlEventTimeline
    """

    _defautcolor = QtGui.QColor(100, 100, 255)

    def __init__(self, scroll):
        super(EventsWidget, self).__init__()
        self._scroll    = scroll

        # Timeline background color
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtCore.Qt.white)
        self.setPalette(palette)

        self._tracks        = [Track(parent=self)]      # List of tracks
        self._pointer       = TimelinePointer(0, self)  # Timeline ( greenline )
        self.tracks_height  = 60
        self._first_track   = self._tracks[0]


    ##########################################################################
    #### HELPERS/FUNCTIONS ###################################################
    ##########################################################################


    def __drawTrackLines(self, painter, start, end):
        # Draw only from pixel start to end
        painter.setPen(QtCore.Qt.DashLine)
        painter.setOpacity(0.3)
        # Draw horizontal lines
        for i, track in enumerate(self._tracks): track.draw(painter, start,end, i)


        # Draw vertical lines
        for x in range(start - (start % 100), end, 100):
            painter.drawLine(x, 20, x, self.height())
            string = "%d" % x
            boundtext = painter.boundingRect(QtCore.QRectF(), string)
            painter.drawText(x - boundtext.width() / 2, 15, string)
        painter.setOpacity(1.0)

        for index, track in enumerate(self._tracks): track.drawLabels(painter, index)
    


    def import_csv(self, csvfileobject):
        """
        Extracts info from a file object and stores it in memory in
        order to display it on the timeline.

        Refer to the `export` method to learn about input file format
        and structure.
        """
        # Clear previously stored info
        self._tracks = []
        self._selected = None

        for row in csvfileobject:
            if row[0] == "T":
                track = self.addTrack()
                track.properties = row
            elif row[0] == "P":
                period = self.add_period(0,1,'-')
                period.properties = row
                
            

    def export_csv(self, csvfileobject):
        """
        Processes all timeline data in an arranged format to be written
        in a CSV file.


        Current file structure:
        =======================

        --- CSV FILE BEGIN ---
        Track info line
        Event info line
        Event info line
        ...
        Track info line
        Event info line
        Event info line
        ...
        Track info line
        Event info line
        Event info line
        ...
        --- CSV FILE END ---


        Track info line format:
        =======================

        | T | Total # of events in this track |  |  | Color | Label |


        Event info line format:
        =======================

        | P | Lock status | Begin frame | End frame | Comment | Color |  |
        """
        for index, track in enumerate(self._tracks):
            csvfileobject.writerow(track.properties)
            for delta in track.periods: 
                csvfileobject.writerow(delta.properties)

    def clean(self):
        self._charts = []
        self._selected = None
        for track in self._tracks: track.clear()
        del self._tracks[:]
        self._tracks = []
        self.repaint()

    def addTrack(self):
        t = Track(parent=self)
        self._tracks.append(t)
        self.setMinimumHeight( self._first_track.whichTop( len(self._tracks) ) )
        return t

    def add_period(self, begin, end, title='', track=0, color="#FFFF00"):
        """Adds an annotated interval."""
        if self.width()<end: self.setMinimumWidth(end+100)
            
        
        period = TimelineDelta(begin, end, 
            title         =   title, 
            parentWidget  =   self,
            color         =   color
        )
        # Create new tracks in case the variable track does not exists
        if len(self._tracks)<=track:
            for i in range( len(self._tracks), track+1 ):  self.addTrack()
        #################################################
        self._tracks[track].add_period(period)
        return period


    ##########################################################################
    #### EVENTS ##############################################################
    ##########################################################################

    def paintEvent(self, e):
        super(EventsWidget, self).paintEvent(e)

        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setFont(QtGui.QFont('Decorative', 8))

        start   = self._scroll.horizontalScrollBar().sliderPosition()-100
        end     = start+self.parent().width()+100

        self.__drawTrackLines(painter, start, end)
        
        for i, track in enumerate(self._tracks): 
            track.drawPeriods(painter, start, end, track_index=i)

        self._pointer.draw(painter) #Draw the time pointer
        painter.end()




    ##########################################################################
    #### PROPERTIES ##########################################################
    ##########################################################################

    def __check_current_time_is_visible(self, current_time):
        """
        This function check if the current_time is visible to the user.
        """
        scrollLimit = self._scroll.horizontalScrollBar().sliderPosition() + self.parent().width() - 50

        if current_time > scrollLimit:
            if self.width()<current_time: self.setMinimumWidth(current_time+100)
            self._scroll.horizontalScrollBar().setSliderPosition(current_time)
        if current_time < self._scroll.horizontalScrollBar().sliderPosition():
            self._scroll.horizontalScrollBar().setSliderPosition(current_time)

    @property
    def scroll(self): return self._scroll.horizontalScrollBar()

    @property
    def position(self): return self._pointer._position

    @position.setter
    def position(self, position):
        self._pointer._position = position
        #######################################################################
        # Check if the current time position is inside the scroll
        # if is not in, update the scroll position
        self.__check_current_time_is_visible(position)
        #######################################################################
        self.repaint()

    @property
    def color(self): return self._defautcolor

    @color.setter
    def color(self, value): self._defautcolor = value

    @property
    def tracks_height(self): return self._tracks_height
    @tracks_height.setter
    def tracks_height(self, value):
        self._tracks_height = value
        new_height = len(self._tracks)*value + 20
        if new_height>self.height(): self.setMinimumHeight(new_height)
        self.repaint()
    

    @property
    def tracks(self): return self._tracks


    
    

    @property
    def numberoftracks(self): return len(self._tracks)

    @numberoftracks.setter
    def numberoftracks(self, value):        
        if value<len(self._tracks):
            for i in range(value, self._tracks+1): self.addTrack()
        y = value * self.tracks_height + 20
        if (y + 40) > self.height():
            self.setMinimumHeight(y + 40)
