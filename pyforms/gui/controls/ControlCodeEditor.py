# !/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from AnyQt import _api
from pyforms.utils.settings_manager import conf

from pyforms.gui.controls.ControlBase import ControlBase
import pyforms.utils.tools as tools

from AnyQt 			 import QtCore, uic
from AnyQt.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSpinBox
from AnyQt.QtGui 	 import QFontMetrics, QColor, QIcon, QFont

if _api.USED_API == _api.QT_API_PYQT5:
    from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs
elif _api.USED_API == _api.QT_API_PYQT4:
    from PyQt4.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs


logger = logging.getLogger(__name__)


class ControlCodeEditor(ControlBase):
	"""
	Control that offers a code editor with pretty-print and line numbers and a save button
	"""

	ARROW_MARKER_NUM = 8

	def __init__(self, *args, **kwargs):
		"""
		
		:param label: 
		:param default: 
		:param helptext: 
		"""
		self._read_only = kwargs.get('readonly', False)
		self._changed_func = None
		super(ControlCodeEditor, self).__init__(*args, **kwargs)

		self.discart_event = kwargs.get('discart_event', self.discart_event)
		

	def init_form(self):
		"""
		
		"""

		control_path = tools.getFileInSameDirectory(__file__, "code_editor.ui")
		self._form = uic.loadUi(control_path)


		self._code_editor = self._form.code_editor
		self._save_button = self._form.save_button
		self._discart_button = self._form.discart_button

		self._save_button.clicked[bool].connect(self.on_save_changes)
		self._discart_button.clicked[bool].connect(self.on_discart_changes)


		if self._read_only:
			self._code_editor.setReadOnly(True)
			self._save_button.setVisible(False)
			self._discart_button.setVisible(False)

		self.form.font_size.addItem('9')
		self.form.font_size.addItem('10')
		self.form.font_size.addItem('11')
		self.form.font_size.addItem('12')
		self.form.font_size.addItem('14')
		self.form.font_size.addItem('18')
		self.form.font_size.addItem('24')

		# Set the default font size
		index = self.form.font_size.findText(conf.PYFORMS_CONTROL_CODE_EDITOR_DEFAULT_FONT_SIZE)
		self.form.font_size.setCurrentIndex(index)

		self.form.font_size.currentIndexChanged.connect(self.__font_size_index_changed)

		self.form.save_button.setIcon(QIcon(conf.PYFORMS_ICON_CODEEDITOR_SAVE))
		self.form.discart_button.setIcon(QIcon(conf.PYFORMS_ICON_CODEEDITOR_DISCART))

		self.lexer = QsciLexerPython

		self._code_editor.keyPressEvent = self._key_pressed
		self._changed_func = None

		self.value = self._value
		super(ControlCodeEditor, self).init_form()

	def __font_size_index_changed(self, index):
		item = self.form.font_size.currentText()
		if len(item) >= 1:
			self._load_code_editor_settings()

	def _load_code_editor_settings(self):
		"""
		Load settings on the code editor like, font style, margins, scroll, etc.
		Based on the example from http://eli.thegreenplace.net/2011/04/01/sample-using-qscintilla-with-pyqt/
		"""

		item = self.form.font_size.currentText()
		size = int(item)

		# Set the default font
		font = QFont()
		font.setFamily('Courier')
		font.setFixedPitch(True)
		font.setPointSize(size)
		self._code_editor.setFont(font)
		self._code_editor.setMarginsFont(font)

		# Margin 0 is used for line numbers
		fontmetrics = QFontMetrics(font)
		self._code_editor.setMarginsFont(font)
		self._code_editor.setMarginWidth(0, fontmetrics.width("00000") + 6)
		self._code_editor.setMarginLineNumbers(0, True)
		self._code_editor.setMarginsBackgroundColor(QColor("#cccccc"))

		# Clickable margin 1 for showing markers
		self._code_editor.setMarginSensitivity(1, True)
		self._code_editor.marginClicked.connect(self.on_margin_clicked)
		self._code_editor.markerDefine(QsciScintilla.RightArrow, self.ARROW_MARKER_NUM)
		self._code_editor.setMarkerBackgroundColor(QColor("#ee1111"), self.ARROW_MARKER_NUM)

		# Detect changes to text
		self._code_editor.modificationChanged.connect(self.on_modification_changed)

		# Brace matching: enable for a brace immediately before or after the current position
		self._code_editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)

		# Current line visible with special background color
		self._code_editor.setCaretLineVisible(True)
		self._code_editor.setCaretLineBackgroundColor(QColor("#ffe4e4"))

		# Set Python lexer
		# Set style for Python comments (style number 1) to a fixed-width Courier.
		lexer = self.lexer()
		lexer.setDefaultFont(font)
		self._code_editor.setLexer(lexer)
		self._code_editor.setIndentationWidth(4)
		# self._code_editor.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, 'Courier')
		self._code_editor.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1)

		# Don't want to see the horizontal scrollbar at all
		# Use raw message to Scintilla here (all messages are documented here: http://www.scintilla.org/ScintillaDoc.html)
		self._code_editor.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)
		
		self._lexer_obj = lexer
		self.qsci_api = QsciAPIs(self._lexer_obj)
		## Add autocompletion strings
		self.qsci_api.add("aLongString")
		self.qsci_api.add("aLongerString")
		self.qsci_api.add("aDifferentString")
		self.qsci_api.add("sOmethingElse")
		## Compile the api for use in the lexer
		self.qsci_api.prepare()
		self._code_editor.setAutoCompletionThreshold(1)
		self._code_editor.setAutoCompletionSource(QsciScintilla.AcsAll)

	# not too small
	# self._code_editor.setMinimumSize(600, 450)

	###################################################################
	############ Events ###############################################
	###################################################################

	def on_margin_clicked(self, nmargin, nline, modifiers):  # pylint: disable=unused-argument
		"""
		On margin clicked, toggle marker for the line the margin was clicked on
		:param nmargin:
		:type nmargin:
		:param nline:
		:type nline:
		:param modifiers:
		:type modifiers:
		"""
		if self._code_editor.markersAtLine(nline) != 0:
			self._code_editor.markerDelete(nline, self.ARROW_MARKER_NUM)
		else:
			self._code_editor.markerAdd(nline, self.ARROW_MARKER_NUM)

	def on_modification_changed(self):
		"""
		On modification change, re-enable save button
		"""
		if self._changed_func: 
			self._save_button.setEnabled(True)
			self._discart_button.setEnabled(True)

	def on_save_changes(self):
		"""
		On button save clicked, save changes made on the code editor to file
		"""
		if self.changed_event():
			self._code_editor.setModified(False)
			self._save_button.setEnabled(False)
			self._discart_button.setEnabled(False)

	def on_discart_changes(self):

		if self.discart_event():
			self._code_editor.setModified(False)
			self._save_button.setEnabled(False)
			self._discart_button.setEnabled(False)

	def discart_event(self):

		return True


	def _key_pressed(self, event):
		"""
		Handle KeyPressed event
		We only care about CTRL-S in order to save changes
		:param event: key event
		"""
		QsciScintilla.keyPressEvent(self._code_editor, event)
		if event.key() in [QtCore.Qt.Key_S, QtCore.Qt.Key_Save]:
			modifiers = QApplication.keyboardModifiers()
			if modifiers == QtCore.Qt.ControlModifier and self.is_modified:
				logger.debug("Saving...")
				self.on_save_changes()

		self.key_pressed_event(event)

	def key_pressed_event(self, event):
		"""
		Override KeyPressed event as you like
		:param event: key event
		"""
		pass

	@property
	def is_modified(self):
		return self._code_editor.isModified()

	###################################################################
	############ Properties ###########################################
	###################################################################

	@property
	def lexer(self):
		return self._lexer

	@lexer.setter
	def lexer(self, value):
		self._lexer = value
		self._load_code_editor_settings()

	@property
	def value(self):
		return self._code_editor.text()

	@value.setter
	def value(self, value):
		if value is not None:
			self._code_editor.setText(str(value))
			self._code_editor.setModified(False)
			self._save_button.setEnabled(False)
			self._discart_button.setEnabled(False)

	@property
	def changed_event(self):
		return self._changed_func if self._changed_func else (lambda: 0)

	@changed_event.setter
	def changed_event(self, value):
		self._changed_func = value
