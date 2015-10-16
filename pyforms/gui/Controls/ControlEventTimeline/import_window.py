import csv
from pyforms import BaseWidget
from pyforms.Controls import ControlProgress
from pyforms.Controls import ControlCombo
from pyforms.Controls import ControlButton
from pyforms.Controls import ControlEmptyWidget
from pyforms.Controls import ControlFile
from pyforms.dialogs import CsvParserDialog


class ImportWindow(BaseWidget):
    
    def __init__(self, timeline=None):
        super(ImportWindow,self).__init__('Import file')

        self._timeline = timeline
        
        #Definition of the forms fields
        self._filetype      = ControlCombo('Type of file')
        self._importButton  = ControlButton('Import')
        self._panel         = ControlEmptyWidget('Panel')
        self._file          = ControlFile('File to import')

        self._panel.value = self._file
        self._filetype.addItem('Event file')
        self._filetype.addItem('Graph file')

        self._formset = [
            ('_filetype', ' '), 
            '_panel',
            (' ','_importButton')]


        self._filetype.changed   = self.__fileTypeChanged
        self._importButton.value = self.__importData

        self._graphCsvParserDlg = CsvParserDialog()
        self._graphCsvParserDlg.xField.label = "Value column"
        self._graphCsvParserDlg.yField.hide()
        self._graphCsvParserDlg.zField.hide()




    def __fileTypeChanged(self):
        if self._filetype.value == 'Event file':
            self._panel.value = self._file

        elif self._filetype.value == 'Graph file':
            self._panel.value = self._graphCsvParserDlg


    def __importData(self):
        if self._filetype.value == 'Event file':
            separator = ','
            with open(self._file.value, 'rU') as csvfile:
                line = csvfile.readline()
                if ";" in line: separator = ';'
            with open(self._file.value, 'rU') as csvfile:
                csvfile = csv.reader(csvfile, delimiter=separator)
                self._timeline._time.import_csv(csvfile)

        elif self._filetype.value == 'Graph file':
            self._timeline._time.importchart_csv( self._graphCsvParserDlg )

        self.close()
        




##################################################################################################################
##################################################################################################################
##################################################################################################################

#Execute the application
if __name__ == "__main__":   
    import pyforms
    pyforms.startApp( ImportWindow, geometry=(0,0,600,400) )