#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = ["Ricardo Ribeiro", "Hugo Cachitas"]
__credits__     = ["Ricardo Ribeiro", "Hugo Cachitas"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


from PyQt4 import QtGui, QtCore

from TimelinePointer import TimelinePointer
from TimelineDelta import TimelineDelta
from TimelineChart import TimelineChart


class TimelineWidget(QtGui.QWidget):
    """
    Timeline widget definition to be used in the ControlEventTimeline
    """

    _defautcolor = QtGui.QColor(100,100,255)

    def __init__(self, *args, **kwargs):
        super(TimelineWidget, self).__init__(*args, **kwargs)

        # self.setFocusPolicy(QtCore.Qt.StrongFocus)
        #self.grabKeyboard()
        self.setMouseTracking(True)
        self.setMinimumWidth(30)
        # self.setMinimumHeight(30)

        # Timeline background color
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtCore.Qt.white)
        self.setPalette(palette)

        self._chartsColors = [ 
            QtGui.QColor(255,0,0), QtGui.QColor(0,255,0), 
            QtGui.QColor(0,0,255), QtGui.QColor(100,100,0), 
            QtGui.QColor(100,0,100), QtGui.QColor(0,100,100)
        ]
        self._charts = []
        self._data = []
        
        self._scale = 1.0
        self._lastMouseY = None

        self._moving = False
        self._resizingBegin = False
        self._resizingEnd = False
        self._creating_event = False
        self._creating_event_start = None
        self._creating_event_end = None
        self._n_tracks = 1

        self._selected = None
        self._selected_track = 0
        self._pointer = TimelinePointer(0, self)

        self._tracks_info = {}  # collects all info on the current timeline state

        # Video playback controls
        self._video_playing = False
        self._video_fps = None
        self._video_fps_min = None
        self._video_fps_max = None
        self._video_fps_inc = None

        # TESTING
        # self._data = [
        #         TimelineDelta(29, 50, 'Teste', top=20, parent=self), TimelineDelta(70, 120, 'Teste', top=20, parent=self),
        #         TimelineDelta(29, 50, 'Ricardo', top=54, parent=self), TimelineDelta(70, 120, 'Ricardo', top=54, parent=self)
        #     ]

        self._update_tracks_info()


    ######################################################################################
    #### HELPERS/FUNCTIONS ###############################################################
    ######################################################################################

    def x2frame(self, x): return int(x/self._scale)

    def frame2x(self, frame): return int(frame*self._scale)

    def removeSelected(self):
        if self._selected != None and not self._selected.lock:
            self._data.remove(self._selected)
            self._selected = None
            self._update_tracks_info()
            self.repaint()

    def lockSelected(self):
        if self._selected != None:
            self._selected.lock = not self._selected.lock
            self._update_tracks_info()
            self.repaint()

    def selectDelta(self, x, y):
        #Check if the timeline pointer was selected
        if y<=20:
            if self._pointer.collide(x, y): return self._pointer
            else: return None
        #Check if the timeline periods were selected
        for col in self._data:
            if col.collide(x, y): return col
        return None

    def __drawTrackLines(self, painter, start, end):
        #Draw only from pixel start to end
        painter.setPen(QtCore.Qt.DashLine)
        painter.setOpacity(0.3)
        #Draw horizontal lines
        for track in range(0,self.numberoftracks+1): y = (track*34)+18; painter.drawLine( start, y, end, y )
        
        #Draw vertical lines
        for x in range(start - (start % 100), end, 100):
            painter.drawLine( x, 20, x, self.height() ); string = "%d" % ( x/self._scale );
            boundtext = painter.boundingRect( QtCore.QRectF(), string )
            painter.drawText( x-boundtext.width()/2, 15, string )
        painter.setOpacity(1.0)


    def __drawTrackLabels(self, painter):
        painter.setPen(QtCore.Qt.black)
        painter.setOpacity(0.5)

        for key, value in self._tracks_info.items():
            text    = value[0]
            x0      = self.visibleRegion().boundingRect().x()
            xmax    = self.visibleRegion().boundingRect().width()
            text_length = painter.fontMetrics().width(text)
            x       = 10
            y       = (key * 34) + 30
            painter.drawText(x, y, text)
            #self.update()
        painter.setOpacity(1.0)




    def importchart_csv(self, csvfileobject):
        chart = TimelineChart(self, csvfileobject, color=self._chartsColors[len(self._charts)])
        self._charts.append(chart)
        

    def import_csv(self, csvfileobject):
        """
        Extracts info from a file object and stores it in memory in
        order to display it on the timeline.

        Refer to the `export` method to learn about input file format
        and structure.
        """
        # Clear previously stored info
        self._tracks_info.clear()
        del self._data[:]

        # File flow controls
        get_track = True
        get_event = False
        for row in csvfileobject:
            #Import events files
            if row[0] == "":
                # sep line has been found, get ready to get a track line next
                get_track = True
                get_event = False
                continue

            # Get track info from the row
            if get_track:
                track_id = int(row[0])
                track_label = row[5]
                track_color = QtGui.QColor(row[4])
                self._tracks_info[track_id] = [track_label, track_color, []]
                get_track = False
                get_event = True
                continue
            # Get event info from the row
            if get_event:
                event = TimelineDelta(0, parent=self)
                event.properties = row + [track_id]
                self._data.append(event)  # add to `_data` for compatibility reasons
                self._tracks_info[track_id][2].append(event)


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
        Empty line
        Track info line
        Event info line
        Event info line
        ...
        Empty line
        Track info line
        Event info line
        Event info line
        ...
        Empty line
        --- CSV FILE END ---


        Track info line format:
        =======================

        | Id | Total # of events in this track |  |  | Color | Label |


        Event info line format:
        =======================

        | Lock status | Begin frame | End frame | Comment | Color |  |
        """

        # Transform the info in the dict to a nested list to be written
        outputstream = []
        for key, value in self._tracks_info.items():
            track_id            = key
            track_label         = value[0]
            track_color         = value[1].name()
            track_events        = value[2]
            track_events_total  = len(value[2])

            row_track_info = [ track_id,
                               track_events_total,
                               "",
                               "",
                               track_color,
                               track_label]

            outputstream.append(row_track_info)

            for event in track_events:
                row_event = event.properties[:5]  #TODO access individually
                outputstream.append(row_event)

            row_sep = ["" for item in range(len(row_track_info))]
            outputstream.append(row_sep)

        # Write outputstream generated above to CSV file object
        for row in outputstream:  csvfileobject.writerow(row)


    #FIXME To be replaced by the functions above
    # def exportcsv(self, csvspan):
    #     self._update_tracks_info()
    #     self._data = sorted(self._data, key = lambda x : (x._begin, x._end) )
    #     for period in self._data:
    #         csvspan.writerow(period.row)

    # def importcsv(self, csvspan):
    #     for row in csvspan:
    #         time = TimelineDelta(0, parent= self)
    #         time.row = row
    #         self._data.append(time)
    #         self._update_tracks_info()

    def cleanCharts(self):
        self._charts=[]
        self.repaint()

    def clean(self):
        self._data=[]
        self._charts=[]
        self._selected=None
        self._n_tracks=1
        self._update_tracks_info()
        self.repaint()

    def cleanLine(self):
        if self._selected!=None:
            track = self._selected.track
            list2delete = []
            for x in self._data:
                if x.track==track: list2delete.append(x)
            for x in list2delete: self._data.remove(x)
            self._selected=None
            self._update_tracks_info()
        else:
            QtGui.QMessageBox.about(self, "Error", "You must select a timebar first"); return


    def addPeriod(self, value, track=0, color=None):
        """Adds an annotated interval."""
        begin, end, title = value
        period = TimelineDelta(begin, end, title=title, parent= self)
        period.track = track
        if color != None:
            period.color = color
        else:
            period.color = self._tracks_info[track][1]
        self._data.append(period)

    def _update_tracks_info(self):
        """
        This method updates the dict `_tracks_info` which contains all
        info stored in the timeline.

        Currently, this method is called is the following situations:
        - Class initialization
        - Event added by double clicking the timeline
        - Everything is cleaned
        - A line is cleaned
        - After an event is removed/locked/unlocked
        #TODO- After editing a timeline line entry
        #TODO- After editing an event (TimelineDelta object)
        - After importing from a file
        - Before exporting to a file

        This dictionary stores info in the format shown below:
        {line_numer : [ line_label, line_color, [data] ] }
        """

        d = self._tracks_info

        # Initialize a dict entry if a new line gets filled
        for i in range(self._n_tracks):
            if i not in d.keys():
                self._defaulttracklabel = "Right click to attribute a behavior"
                d[i] = [self._defaulttracklabel, self.color, []]

        # Gets data events track number and stores them accordingly
        # in the dict.
        for event in self._data:
                tracknumber = event.track
                if event not in d[tracknumber][2]:
                    d[tracknumber][2].append(event)

        # When an event is deleted, it must disappear also from the dict.
        # We need to look for events in the dict that disappeared from
        # the data list.
        for key, value in d.items():
            value[2] = [event for event in value[2] if event in self._data]

        #self.__print_tracks_info()
        self.repaint()
        

    def __print_tracks_info(self):
        """Prints tracks info on screen."""
        d = self._tracks_info
        if d:  # returns True if dict is not empty
            print "{0:=>79}".format(" TIMELINE INFO")
            print "Number of active tracks:", self._n_tracks
            print "Total number of events created:", len(self._data)
            print "Tracks:"
            print "{0:>8} {1:^50} {2:^7} {3:>11}".format("ID",
                                                         "Label",
                                                         "Color",
                                                         "# of events")
            print "{0:-<79}".format("    ")
            for key, value in d.items():
                if self._selected_track == key:
                    sel = ">"
                else:
                    sel = ""
                print "{0:>4}{1:>4}{2:^50}{3:7}{4:^11}".format(sel,
                                                               key,
                                                               value[0],
                                                               value[1].name(),
                                                               len(value[2]))
            print
        else:
            print "Nothing here."

    ######################################################################################
    #### EVENTS ##########################################################################
    ######################################################################################

    def paintEvent(self, e):
        super(TimelineWidget, self).paintEvent(e)

        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setFont(QtGui.QFont('Decorative', 8))

        start   = self._scroll.horizontalScrollBar().sliderPosition()
        end     = start + self.parent().width() + 50

        #Draw graphs #####################################################################
        if len(self._charts)>0: 
            painter.setPen(QtCore.Qt.black)
            middle = self.height()//2
            painter.setOpacity(0.1)
            painter.drawLine(start, middle, end, middle)

        for chart in self._charts:  chart.draw(painter, start, end, 0, self.height())
        #End draw graph ##################################################################

        self.__drawTrackLines(painter, start, end)
        # Draw track labels
        self.__drawTrackLabels(painter)

        # Draw delta bars
        for time in self._data:
            painter.setBrush(time.color)
            time.draw(painter)

        # Draw the selected element
        if self._selected != None:
            painter.setBrush(QtGui.QColor(255, 0, 0))
            self._selected.draw(painter, showvalues=True)

        # Draw the time pointer
        self._pointer.draw(painter)

        
        painter.end()

    def mouseDoubleClickEvent(self, event):
        if  self._selected is not None and self._selected!=self._pointer and self._selected.collide(event.x(), event.y()):
            self._selected.showEditWindow()
        elif event.y() > 20:
            top = (event.y()-20) // 34
            y = top * 34 + 20
            x = event.x() / self._scale
            # time = TimelineDelta(x, x + 50 / self._scale, title='', top=y, parent=self)
            time = TimelineDelta(x, x+10, title='', top=y, parent=self)
            self._data.append(time)
            self._selected = time
            self._selected_track = self._selected.track
            self._update_tracks_info()
            self.repaint()

    def keyReleaseEvent(self, event):
        super(TimelineWidget, self).keyReleaseEvent(event)

        # Control video playback using the space bar to Play/Pause
        if event.key() == QtCore.Qt.Key_Space:
            self._video_playing = not self._video_playing
            self.playVideoEvent()
            self.repaint()

        # Increase video frame rate (FPS) by 5
        if event.key() == QtCore.Qt.Key_Plus:
            if self._video_fps_min <= (self.fps + self._video_fps_inc) <= self._video_fps_max:
                self.fps += self._video_fps_inc
            else:
                pass
            self.fpsChangeEvent()
            self.repaint()

        # Decrease video frame rate (FPS) by 5
        if event.key() == QtCore.Qt.Key_Minus:
            if self._video_fps_min <= (self.fps - self._video_fps_inc) <= self._video_fps_max:
                self.fps -= self._video_fps_inc
            else:
                pass
            self.fpsChangeEvent()
            self.repaint()

        # Jumps 20 seconds forward
        if event.key() == QtCore.Qt.Key_C:
            self._pointer.position += 10*self.fps
            self.__checkPositionIsVisible(self.position)
            self.repaint()

        # Jumps 20 seconds backwards
        if event.key() == QtCore.Qt.Key_Z:
            self._pointer.position -= 10*self.fps
            self.__checkPositionIsVisible(self.position)
            self.repaint()

        # Jumps 1 frame forward
        if event.key() == QtCore.Qt.Key_D:
            self._pointer.position += 1
            self.__checkPositionIsVisible(self.position)
            self.repaint()

        # Jumps 1 frame backwards
        if event.key() == QtCore.Qt.Key_A:
            self._pointer.position -= 1
            self.__checkPositionIsVisible(self.position)
            self.repaint()

        if self._selected is not None:
            modifier = int(event.modifiers())

            # Move the event (or the pointer) left
            if modifier == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Left:
                self._selected.move(-1, 0); self.repaint()

            # Move the event (or the pointer) right
            if modifier == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Right:
                self._selected.move(1, 0); self.repaint()

            if self._selected != self._pointer:
                # Delete the selected event
                if event.key() == QtCore.Qt.Key_Delete:
                    self.removeSelected()

                # Lock or unlock an event
                if event.key() == QtCore.Qt.Key_L:
                    self.lockSelected()

                # Move the event up
                if modifier == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Up:
                    self._selected.move(0, self._selected._top - 34); self.repaint()

                # Move the event down
                if modifier == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Down:
                    self._selected.move(0, self._selected._top + 34); self.repaint()

                # Move the event end left
                if modifier == int(QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier) and event.key() == QtCore.Qt.Key_Left:
                    self._selected.moveEnd(-1); self.repaint()

                # Move the event end right
                if modifier == int(QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier) and event.key() == QtCore.Qt.Key_Right:
                    self._selected.moveEnd(1); self.repaint()

                # Move the event begin left
                if modifier == QtCore.Qt.ShiftModifier and event.key() == QtCore.Qt.Key_Left:
                    self._selected.moveBegin(-1); self.repaint()

                # Move the event begin right
                if modifier == QtCore.Qt.ShiftModifier and event.key() == QtCore.Qt.Key_Right:
                    self._selected.moveBegin(1); self.repaint()

        else:
            # Keybinds to create an event at current frame
            if event.key() == QtCore.Qt.Key_S and not self._creating_event:
                # Start
                self._creating_event_start = self._pointer.frame
                self._creating_event = True

                #TODO Add some indicator that an event is being recorded, like using the track selector circle to become red

                return

            if event.key() == QtCore.Qt.Key_S and self._creating_event:
                # End, must be followed right after Start key and have no effect otherwise
                self._creating_event_end = self._pointer.frame

                start = self._creating_event_start
                end = self._creating_event_end
                comment = ""

                if end > start:
                    self.addPeriod((start, end, comment), self._selected_track)
                    self._update_tracks_info()
                    self.repaint()
                    self._creating_event = False
                else:
                    print "Event auto creation aborted."
                    self._creating_event = False

    def mousePressEvent(self, event):
        # Select the track
        track_clicked = (event.y() - 20) // 34
        if track_clicked in self._tracks_info.keys():
            self._selected_track = track_clicked
        else:
            pass

        # Select the period bar
        self._selected = self.selectDelta(event.x(), event.y())
        self._moving = False
        self._resizingBegin = False
        self._resizingEnd = False

        if self._selected is not None:
            #Select the action
            if event.buttons()==QtCore.Qt.LeftButton:
                if self._selected.canSlideEnd(event.x(), event.y()):
                    self._resizingEnd = True
                elif self._selected.canSlideBegin(event.x(), event.y()):
                    self._resizingBegin = True
                elif self._selected.collide(event.x(), event.y()):
                    self._moving = True
        if event.y() <= 20 and not self._moving:
            self._pointer.position = event.x()

        self._update_tracks_info()
        self.repaint()


    def mouseMoveEvent(self, event):
        super(TimelineWidget, self).mouseMoveEvent(event)

        # Do nothing if no event bar is selected
        if self._selected is None:
            return

        #Set cursors
        if self._selected.canSlideBegin(event.x(), event.y()) or self._selected.canSlideEnd(event.x(), event.y()):
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        elif self._selected.collide(event.x(), event.y()):
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
        else:
            self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

        if self._selected is None:
            return

        if event.buttons() == QtCore.Qt.LeftButton:
            if self._lastMouseY is not None:
                diff = event.x() - self._lastMouseY
                if diff!=0:
                    if self._moving:
                        self._selected.move(diff, event.y())
                    elif self._resizingBegin:
                        self._selected.moveBegin(diff)
                    elif self._resizingEnd:
                        self._selected.moveEnd(diff)
                    self.repaint()
            self._lastMouseY = event.x()

    def mouseReleaseEvent(self, event):
        self._lastMouseY = None

    def trackInPosition(self, x, y):
        return (y-30) // 34

    def playVideoEvent(self):
        pass

    def fpsChangeEvent(self):
        pass

    ######################################################################################
    #### PROPERTIES ######################################################################
    ######################################################################################

    def __checkPositionIsVisible(self, value):
        playerPos   = self.frame2x(value)
        scrollLimit = self._scroll.horizontalScrollBar().sliderPosition()+self.parent().width()-50
        if playerPos>scrollLimit:
            newPos = playerPos - self.parent().width() + 50
            self._scroll.horizontalScrollBar().setSliderPosition(newPos)
        if playerPos<self._scroll.horizontalScrollBar().sliderPosition():
            self._scroll.horizontalScrollBar().setSliderPosition(playerPos)


    @property
    def scroll(self): return self._scroll.horizontalScrollBar()

    @property
    def position(self): return self._pointer._position
    @position.setter
    def position(self, value): 
        self._pointer._position = value;
        #################################################################################
        #Check if the player position is inside the scroll
        #if is not in, update the scroll position
        self.__checkPositionIsVisible(value)
        #################################################################################
        self.repaint()

        

    @property
    def scale(self): return self._scale
    @scale.setter
    def scale(self, value): self._scale = value; self.repaint()

    @property
    def color(self): return self._defautcolor
    @color.setter
    def color(self, value): self._defautcolor = value

    @property
    def numberoftracks(self): return self._n_tracks
    @numberoftracks.setter
    def numberoftracks(self, value):
        self._n_tracks = value
        y = value * 34 + 20
        if y + 40 > self.height():
            self.setMinimumHeight(y + 40)


    # Video playback properties
    @property
    def isPlaying(self): return self._video_playing

    @property
    def fps(self): return self._video_fps
    @fps.setter
    def fps(self, value): self._video_fps = value