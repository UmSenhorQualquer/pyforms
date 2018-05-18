from confapp import conf

if conf.PYFORMS_MODE=='GUI':
	from pyforms.gui.dialogs.csv_parser import CsvParserDialog


elif conf.PYFORMS_MODE in ['TERMINAL']:
	class CsvParserDialog(object): pass