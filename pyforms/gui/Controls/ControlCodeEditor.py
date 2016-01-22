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

from pyforms.gui.Controls.ControlBase import ControlBase
import pyforms.Utils.tools as tools
from PyQt4 import uic
from PyQt4.Qsci import QsciScintilla, QsciLexerPython  # pylint: disable=no-name-in-module
from PyQt4.QtGui import QFontMetrics
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QColor


class ControlCodeEditor(ControlBase):
    """
    Control that offers a code editor with pretty-print and line numbers and a save button
    """

    ARROW_MARKER_NUM = 8

    def initForm(self):
        control_path = tools.getFileInSameDirectory(__file__, "code_editor.ui")
        self._form = uic.loadUi(control_path)

        self._code_file_path = ""

        self._code_editor = self._form.code_editor

        self._save_button = self._form.save_button
        self._save_button.clicked[bool].connect(self.on_save_changes)

        self._load_code_editor_settings()

        super(ControlCodeEditor, self).initForm()

    def _load_code_editor_settings(self):
        """
        Load settings on the code editor like, font style, margins, scroll, etc.
        Based on the example from http://eli.thegreenplace.net/2011/04/01/sample-using-qscintilla-with-pyqt/
        """

        # Set the default font
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(14)
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
        lexer = QsciLexerPython()
        lexer.setDefaultFont(font)
        self._code_editor.setLexer(lexer)
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
        with open(self.value, "w") as file:
            file.write(self._code_editor.text())

        self._code_editor.setModified(False)
        self._save_button.setEnabled(False)

    ###################################################################
    ############ Properties ###########################################
    ###################################################################

    @property
    def value(self):
        return self._code_file_path

    @value.setter
    def value(self, value):
        with open(value, "r") as file:
            self._code_editor.setText(str(file.read()))
        self._code_file_path = value
        self._code_editor.setModified(False)
        self._save_button.setEnabled(False)
