import csv
from pyforms import BaseWidget
from pyforms.controls import ControlProgress
from pyforms.controls import ControlCombo
from pyforms.controls import ControlButton
from pyforms.controls import ControlEmptyWidget
from pyforms.controls import ControlFile
from pyforms.controls import ControlNumber

        
import time
import datetime
import dateutil.parser

import logging

logger=logging.getLogger(__file__)

class BonsaiImportFileDlg(BaseWidget):

    def __init__(self, timeline=None):
        super(BonsaiImportFileDlg, self).__init__('Import file')

        self._file          = ControlFile('File to import')
        self._fps           = ControlNumber('Video FPS', default=30)
        self._startframe    = ControlNumber('Initial frame', visible=False)


        self._formset = [('_startframe','_fps', '_file')]

        #self._file.value = '/home/ricardo/Desktop/rat1e2.csv'


class ImportWindow(BaseWidget):

    def __init__(self, timeline=None):
        super(ImportWindow, self).__init__('Import file', parent_win=timeline)
        self.setContentsMargins(10, 10, 10, 10)
        self._timeline = timeline

        # Definition of the forms fields
        self._filetype      = ControlCombo('Please select the type of file you would like to import:')
        self._importButton  = ControlButton('Import')
        self._panel         = ControlEmptyWidget('Panel')
        self._file          = ControlFile('File to import')
        
        self._panel.value = self._file
        self._filetype.add_item('Events file', 0)
        self._filetype.add_item('Graph file', 1)
        self._filetype.add_item('Bonsai events file', 2)
        self._filetype.add_item('Bonsai events file (old format)', 3)

        self._formset = [
            ('_filetype', ' '),
            '_panel',
            (' ', '_importButton'),
            ' '
        ]

        self._filetype.changed_event = self.__fileTypeChanged
        self._importButton.value = self.__importData

        from pyforms.gui.dialogs.csv_parser import CsvParserDialog
        self._graphCsvParserDlg = CsvParserDialog()
        self._graphCsvParserDlg.xField.label = "Value column"
        self._graphCsvParserDlg.yField.hide()
        self._graphCsvParserDlg.zField.hide()
        self._graphCsvParserDlg.loadButton.hide()

        self._bonsai_import_dlg = BonsaiImportFileDlg()

    def __fileTypeChanged(self):
        if self._filetype.value == 0:
            self._panel.value = self._file

        elif self._filetype.value == 1:
            self._panel.value = self._graphCsvParserDlg

        elif self._filetype.value == 2:
            self._panel.value = self._bonsai_import_dlg
            self._bonsai_import_dlg._startframe.hide()

        elif self._filetype.value == 3:
            self._panel.value = self._bonsai_import_dlg
            self._bonsai_import_dlg._startframe.show()













    def __importData(self):
        if self._filetype.value == 0:
            separator = ','
            with open(self._file.value, 'rU') as csvfile:
                line = csvfile.readline()
                if ";" in line:
                    separator = ';'
            with open(self._file.value, 'rU') as csvfile:
                csvfile = csv.reader(csvfile, delimiter=separator)
                self._timeline._time.import_csv(csvfile)

        elif self._filetype.value == 1:
            self._timeline._time.importchart_csv(self._graphCsvParserDlg)
            self._timeline.show_graphs_properties()

        elif self._filetype.value == 2:
            self.__import_bonsai_events()
        elif self._filetype.value == 3:
            self.__import_bonsai_events_oldformat()

        self._timeline.repaint()
        self._timeline._time.repaint()
        self.close()  # pylint: disable=no-member


    def import_chart(self, filename, frame_col=0, val_col=1):
        self._filetype.value = 1            
        self._graphCsvParserDlg.filename    = filename
        self._graphCsvParserDlg.frameColumn = frame_col
        self._graphCsvParserDlg.xColumn     = val_col
        
            

    def __import_bonsai_events(self):
        
        with open(self._bonsai_import_dlg._file.value, 'rU') as csvfile:
            values = []
            pointEventValues = []
            csvfile = csv.reader(csvfile, delimiter=' ')
            for row in csvfile:  # strip Start/End word from all events names which are not PointEven
                
                try:
                    timestr = row[1].rstrip('0')
                    cvttime = datetime.datetime.strptime(timestr, "%H:%M:%S.%f")
                except:
                    timestr = row[1]
                    try:
                        print(timestr)
                        cvttime = datetime.datetime.strptime(timestr, "%H:%M:%S")
                    except:
                        timestr = timestr.replace('T', ' ')
                        print(timestr)
                        cvttime = dateutil.parser.parse(timestr)

                seconds = (cvttime - datetime.datetime(1900, 1, 1)).total_seconds()
                frame = int(round(self._bonsai_import_dlg._fps.value * seconds))

                if row[2] == "PointEvent":
                    eventtype = row[0]
                    pointEventValues.append([eventtype, frame, row[2]])
                else:
                    if row[0].startswith('Start'):
                        eventtype = row[0][len('Start'):]  # strip Start word from the beginning
                    else:
                        eventtype = row[0][len('End'):]  # strip End word from the beginning
                    values.append([eventtype, frame, row[2]])

            values = sorted(values, key=lambda x: (x[0].capitalize(), x[1]))
            pointEventValues = sorted(pointEventValues, key=lambda x: (x[0].capitalize(), x[1]))
            ntracks = len(set([x[0] for x in values])) + 1

            # collapse
            events = []
            eventsTypes = {}  # Events names
            currentTrack = 0
            for index in range(0, len(pointEventValues)):
                pointEventValue = pointEventValues[index]
                eventsTypes[pointEventValue[0]] = currentTrack
                self._timeline.add_period([pointEventValue[1], pointEventValue[1] + 50, pointEventValue[0]], row=currentTrack)

            currentTrack = 1

            for index in range(0, len(values), 2):
                row0 = values[index]
                row1 = values[index + 1]

                if row0[0] not in eventsTypes:
                    eventsTypes[row0[0]] = currentTrack
                    track = currentTrack
                    currentTrack += 1
                else:
                    track = eventsTypes[row0[0]]

                self._timeline.add_period([row0[1], row1[1], row0[0]], row=track)




    def __import_bonsai_events_oldformat(self):
        
        try:
            with open(self._bonsai_import_dlg._file.value, 'rU') as csvfile:
                windows_events = []
                points_events  = []
                first_date     = None

                initial_frame = int(self._bonsai_import_dlg._startframe.value)

                open_windows = {}
                for row in csvfile:
                    row = row[:-1] #remove the newline character

                    if row.endswith('WindowClosing'):
                        split     = row.rfind(' ')
                        #eventtype = row[-split:]
                        eventtype = 'end'
                        timestr   = row[split-33:split]
                        eventname = row[3:split-33].strip()
                    elif row.endswith('PointEvent'):
                        split     = row.rfind(' ')
                        eventtype = row[split+1:]
                        timestr   = row[split-33:split]
                        eventname = row[:split-33]
                    else:
                        eventtype = 'start'
                        timestr   = row[-33:]
                        eventname = row[5:-33].strip()
                    
                    cvttime = dateutil.parser.parse(timestr.replace('T', ' '))
                    cvttime = cvttime.replace(tzinfo=None)
                    if first_date is None: first_date = cvttime
                    
                    seconds = (cvttime - first_date).total_seconds()
                    frame   = int(round(self._bonsai_import_dlg._fps.value * seconds)) + initial_frame

                    if eventtype=='PointEvent':
                        points_events.append([eventtype, frame, eventname])
                    else:
                        if eventtype=='start':
                            open_windows[eventname] = frame
                        elif eventtype=='end':
                            begin_frame = open_windows[eventname]
                            del open_windows[eventname]
                            windows_events.append( [eventtype, (begin_frame, frame) , eventname] )
                    

                windows_events = sorted(windows_events, key=lambda x: (x[0].capitalize(), x[2], x[1]))
                points_events  = sorted(points_events,  key=lambda x: (x[0].capitalize(), x[1]))
                ntracks        = len(set([x[0][1] for x in windows_events])) + 1

                # collapse
                events = []
                events_types = {}  # Events names
                current_track = 0
                for index in range(0, len(points_events)):
                    eventtype, frame, eventname = points_events[index]
                    events_types[eventname] = current_track
                    self._timeline.add_period([frame, frame+2, eventname], row=current_track)

                current_track = 1

                for event in windows_events:
                    eventtype, (frame_begin, frame_end), eventname = event
                    
                    if eventname not in events_types:
                        events_types[eventname] = current_track
                        track         = current_track
                        current_track += 1
                    else:
                        track = events_types[eventname]

                    self._timeline.add_period([frame_begin, frame_end, eventname], row=track)


        except Exception as e:
            self.warning("An error occurred when trying to import the file. Please check the logs.")
            logger.error(e, exc_info=True)