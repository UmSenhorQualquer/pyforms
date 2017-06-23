import csv
from pyforms import BaseWidget
from pyforms.Controls import ControlProgress
from pyforms.Controls import ControlCombo
from pyforms.Controls import ControlButton
from pyforms.Controls import ControlEmptyWidget
from pyforms.Controls import ControlFile
from pyforms.Controls import ControlNumber

		
import time
import datetime


class BonsaiImportFileDlg(BaseWidget):

	def __init__(self, timeline=None):
		super(BonsaiImportFileDlg, self).__init__('Import file')

		self._file = ControlFile('File to import')
		self._fps = ControlNumber('Video FPS', 30)

		self._formset = [('_fps', '_file')]

		#self._file.value = '/home/ricardo/Desktop/rat1e2.csv'


class ImportWindow(BaseWidget):

	def __init__(self, timeline=None):
		super(ImportWindow, self).__init__('Import file', parent_win=timeline)
		self.setContentsMargins(10, 10, 10, 10)
		self._timeline = timeline

		# Definition of the forms fields
		self._filetype = ControlCombo('Please select the type of file you would like to import:')
		self._importButton = ControlButton('Import')
		self._panel = ControlEmptyWidget('Panel')
		self._file = ControlFile('File to import')

		self._panel.value = self._file
		self._filetype.add_item('Events file', 0)
		self._filetype.add_item('Graph file', 1)
		self._filetype.add_item('Bonsai events file', 2)

		self._formset = [
			('_filetype', ' '),
			'_panel',
			(' ', '_importButton'), ' ']

		self._filetype.changed_event = self.__fileTypeChanged
		self._importButton.value = self.__importData

		from pyforms.gui.dialogs.csv_parser import CsvParserDialog
		self._graphCsvParserDlg = CsvParserDialog()
		self._graphCsvParserDlg.xField.label = "Value column"
		self._graphCsvParserDlg.yField.hide()
		self._graphCsvParserDlg.zField.hide()
		self._graphCsvParserDlg.loadButton.hide()

		self._bonsaiImportDlg = BonsaiImportFileDlg()

	def __fileTypeChanged(self):
		if self._filetype.value == 0:
			self._panel.value = self._file

		elif self._filetype.value == 1:
			self._panel.value = self._graphCsvParserDlg

		elif self._filetype.value == 2:
			self._panel.value = self._bonsaiImportDlg

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
			with open(self._bonsaiImportDlg._file.value, 'rU') as csvfile:
				values = []
				pointEventValues = []
				csvfile = csv.reader(csvfile, delimiter=' ')
				for row in csvfile:  # strip Start/End word from all events names which are not PointEven
					try:
						timestr = row[1].rstrip('0')
						cvttime = datetime.datetime.strptime(timestr, "%H:%M:%S.%f")
					except:
						timestr = row[1]
						cvttime = datetime.datetime.strptime(timestr, "%H:%M:%S")

					seconds = (cvttime - datetime.datetime(1900, 1, 1)).total_seconds()
					frame = int(round(self._bonsaiImportDlg._fps.value * seconds))

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
					self._timeline.addPeriod([pointEventValue[1], pointEventValue[1] + 50, pointEventValue[0]], track=currentTrack)

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

					self._timeline.addPeriod([row0[1], row1[1], row0[0]], track=track)

		self._timeline.repaint()
		self._timeline._time.repaint()
		self.close()  # pylint: disable=no-member


	def import_chart(self, filename, frame_col=0, val_col=1):
		self._filetype.value = 1            
		self._graphCsvParserDlg.filename    = filename
		self._graphCsvParserDlg.frameColumn = frame_col
		self._graphCsvParserDlg.xColumn     = val_col
		
			
			

##################################################################################################################
##################################################################################################################
##################################################################################################################

# Execute the application
if __name__ == "__main__":
	import pyforms
	pyforms.start_app(ImportWindow, geometry=(0, 0, 600, 400))
