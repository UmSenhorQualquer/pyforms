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
from PyQt4.Qsci import QsciScintilla, QsciLexerPython
from PyQt4.QtGui import QFontMetrics
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QColor


class ControlCodeEditor(ControlBase):

    def initForm(self):
        control_path = tools.getFileInSameDirectory(__file__, "code_editor.ui")
        self._form = uic.loadUi(control_path)
        # self.form.label.setText(self._label)
        # self.form.lineEdit.setText(self._value)
        # self.form.setToolTip(self.help)

        # Set the default font
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self._form.code_area.setFont(font)
        self._form.code_area.setMarginsFont(font)

        # Margin 0 is used for line numbers
        fontmetrics = QFontMetrics(font)
        self._form.code_area.setMarginsFont(font)
        self._form.code_area.setMarginWidth(0, fontmetrics.width("00000") + 6)
        self._form.code_area.setMarginLineNumbers(0, True)
        self._form.code_area.setMarginsBackgroundColor(QColor("#cccccc"))

        super(ControlCodeEditor, self).initForm()
        # self.form.lineEdit.editingFinished.connect(self.finishEditing)

#	def finishEditing(self):
#		"""Function called when the lineEdit widget is edited"""
#		self.changed()
#		self.form.lineEdit.focusNextChild()

    ###################################################################
    ############ Properties ###########################################
    ###################################################################

#     @property
#     def value(self):
#         return self._form.code_area.toPlainText()
#
#     @value.setter
#     def value(self, value):
#         self._form.code_area.setPlainText(str(value))
