import csv
from pyforms import BaseWidget
from pyforms.controls import ControlText
from pyforms.controls import ControlButton
from pyforms.controls import ControlFile
from pyforms.controls import ControlList
from pyforms.controls import ControlNumber


class CsvParserDialog(BaseWidget):

    def __init__(self, parent=None):
        super(CsvParserDialog, self).__init__('CSV Choose the columns', parent_win = parent)
        self._filename = None

        # Definition of the forms fields
        self._filename = ControlFile('CSV File')
        self._separator = ControlText('Separator', ';')
        self._startingrow = ControlNumber('Starting row', 0)
        self._frameCol = ControlNumber('Frame column', 0, 0, 100)
        self._xCol = ControlNumber('X column', 1, 0, 100)
        self._yCol = ControlNumber('Y column', 2, 0, 100)
        self._zCol = ControlNumber('Z column', 3, 0, 100)
        self._filePreview = ControlList('Preview')
        self._loadButton = ControlButton('Load')

        self._formset = [('_filename','_startingrow'), ('_separator', '_frameCol', '_xCol', '_yCol', '_zCol', '_loadButton'), '_filePreview']
        self._separator.changed_event = self.__refreshPreview
        self._filename.changed_event  = self.__refreshPreview
        self._startingrow.changed_event = self.__refreshPreview

        #self._filename.value = '/home/ricardo/Downloads/2012.12.01_13.48_3D_POSITIONS_version_03.06.2015.csv'

    @property
    def filename(self): return self._filename.value

    @filename.setter
    def filename(self, value):
        self._filename.value = value
        self.__refreshPreview()

    @property
    def loadFileEvent(self): return self._loadButton.value

    @loadFileEvent.setter
    def loadFileEvent(self, value): self._loadButton.value = value

    @property
    def separator(self): return self._separator.value

    @property
    def starting_row(self): return self._startingrow.value
    @starting_row.setter
    def starting_row(self, value): self._startingrow.value = value

    @property
    def frameColumn(self): return self._frameCol.value
    @frameColumn.setter
    def frameColumn(self, value): self._frameCol.value = value

    @property
    def xColumn(self): return self._xCol.value
    @xColumn.setter
    def xColumn(self, value): self._xCol.value = value

    @property
    def yColumn(self): return self._yCol.value
    @yColumn.setter
    def yColumn(self, value): self._yCol.value = value

    @property
    def zColumn(self): return self._zCol.value
    @zColumn.setter
    def zColumn(self, value): self._zCol.value = value

    @property
    def loadButton(self): return self._loadButton

    @property
    def xField(self): return self._xCol

    @property
    def yField(self): return self._yCol

    @property
    def zField(self): return self._zCol

    def __iter__(self):
        if self._filename.value != None and self._filename.value != '':

            csvfile = open(self._filename.value, 'U')
            self._spamreader = csv.reader(csvfile, delimiter=self._separator.value)
            for i in range(int(self._startingrow.value)): next(self._spamreader, None)  # skip the headers
            self._cols = [self.frameColumn]
            if self.xField.visible:
                self._cols.append(self.xColumn)
            if self.yField.visible:
                self._cols.append(self.yColumn)
            if self.zField.visible:
                self._cols.append(self.zColumn)
        else:
            self._spamreader = None
        return self

    # For compatibility with python 3
    def __next__(self): return self.next()

    def next(self):
        if self._spamreader != None:
            row = self._spamreader.next()
            return [row[int(col)] for col in self._cols]
        else:
            raise StopIteration()

    def __refreshPreview(self):
        if self._filename.value != None and self._filename.value != '':
            with open(self._filename.value, 'U') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=self._separator.value)
                for i in range(int(self._startingrow.value)): next(spamreader, None)  # skip the headers
                self._filePreview.value = []
                self._filePreview.horizontalHeaders = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", ]
                for i, row in enumerate(spamreader):
                    self._filePreview += row
                    if i >= 10:
                        break

    def load(self): 
        self.__refreshPreview()
        self._loadButton.value()

##################################################################################################################
##################################################################################################################
##################################################################################################################

# Execute the application
if __name__ == "__main__":
    import pyforms
    pyforms.start_app(CsvParserDialog, geometry=(0, 0, 600, 400))
