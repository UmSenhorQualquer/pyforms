from confapp import conf


if conf.PYFORMS_MODE=='GUI':
	from pyforms_gui.dialogs.csv_parser import CsvParserDialog


elif conf.PYFORMS_MODE=='TERMINAL':
	class CsvParserDialog(object): pass