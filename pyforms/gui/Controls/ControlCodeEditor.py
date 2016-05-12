#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@author: Ricardo Ribeiro
@credits: Ricardo Ribeiro
@license: MIT
@version: 0.0
@maintainer: Ricardo Ribeiro
@email: ricardojvr@gmail.com
@status: Development
@lastEditedBy: Carlos Mão de Ferro (carlos.maodeferro@neuro.fchampalimaud.org)
'''

import logging
from pyforms.gui.Controls.ControlBase import ControlBase
import pyforms.Utils.tools as tools
from PyQt4 import uic, QtGui
from PyQt4.Qsci import QsciScintilla, QsciLexerPython  # pylint: disable=no-name-in-module
from PyQt4.QtGui import QFontMetrics
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QColor
from PyQt4.QtCore import Qt

from pyforms import conf


class ControlCodeEditor(ControlBase):
    """
    Control that offers a code editor with pretty-print and line numbers and a save button
    """

    ARROW_MARKER_NUM = 8

    def initForm(self):
        self.logger = logging.getLogger(__name__)

        control_path = tools.getFileInSameDirectory(__file__, "code_editor.ui")
        self._form = uic.loadUi(control_path)

        self._code_editor = self._form.code_editor

        self._save_button = self._form.save_button
        self._save_button.clicked[bool].connect(self.on_save_changes)

        self.form.font_size.addItem('9')
        self.form.font_size.addItem('10')
        self.form.font_size.addItem('11')
        self.form.font_size.addItem('12')
        self.form.font_size.addItem('14')
        self.form.font_size.addItem('18')
        self.form.font_size.addItem('24')

        # Set the default font size
        index = self.form.font_size.findText(conf.CONTROL_CODE_EDITOR_DEFAULT_FONT_SIZE)
        self.form.font_size.setCurrentIndex(index)

        self.form.font_size.currentIndexChanged.connect(self.__font_size_index_changed)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.qApp.style().standardPixmap(QtGui.QStyle.SP_DialogSaveButton), mode=QtGui.QIcon.Normal, state=QtGui.QIcon.On)
        icon.addPixmap(QtGui.qApp.style().standardPixmap(QtGui.QStyle.SP_DialogSaveButton), mode=QtGui.QIcon.Normal, state=QtGui.QIcon.Off)
        self.form.save_button.setIcon(icon)

        self.lexer = QsciLexerPython

        self._code_editor.keyPressEvent = self._key_pressed

        super(ControlCodeEditor, self).initForm()

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

        # not too small
        #self._code_editor.setMinimumSize(600, 450)

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
        self._save_button.setEnabled(True)

    def on_save_changes(self):
        """
        On button save clicked, save changes made on the code editor to file
        """
        if self.value is None:
            self._value = QtGui.QFileDialog.getSaveFileName(self.form, "Save file")
        with open(self.value, "w") as file:
            file.write(self._code_editor.text())

        self._code_editor.setModified(False)
        self._save_button.setEnabled(False)

    def _key_pressed(self, event):
        """
        Handle KeyPressed event
        We only care about CTRL-S in order to save changes
        :param event: key event
        """
        QsciScintilla.keyPressEvent(self._code_editor, event)
        if event.key() in [Qt.Key_S, Qt.Key_Save]:
            modifiers = QtGui.QApplication.keyboardModifiers()
            if modifiers == Qt.ControlModifier:
                self.logger.debug("Saving...")
                self.on_save_changes()

        self.key_pressed(event)

    def key_pressed(self, event):
        """
        Override KeyPressed event as you like
        :param event: key event
        """
        pass

    ###################################################################
    ############ Properties ###########################################
    ###################################################################

    @property
    def lexer(self): return self._lexer

    @lexer.setter
    def lexer(self, value):
        self._lexer = value
        self._load_code_editor_settings()

    @property
    def value(self):
        if len(self._value) == 0:
            return None
        return self._value

    @value.setter
    def value(self, value):
        ControlBase.value.fset(self, value)
        if len(value) > 0:
            with open(value, "r") as file:
                self._code_editor.setText(str(file.read()))
            self._code_editor.setModified(False)
            self._save_button.setEnabled(False)
