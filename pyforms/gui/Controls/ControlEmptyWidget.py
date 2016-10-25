#!/usr/bifn/python
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
import sip
			
from PyQt4 import QtGui
from pyforms.gui.Controls.ControlBase import ControlBase
from pyforms.gui.BaseWidget import BaseWidget


class ControlEmptyWidget(ControlBase, QtGui.QWidget):


	def __init__(self, label=''):
		ControlBase.__init__(self, label)
		QtGui.QWidget.__init__(self)

		layout = QtGui.QVBoxLayout(); layout.setMargin(0)
		self.form.setLayout( layout )



	def initForm(self):
		pass

	############################################################################
	############ Properties ####################################################
	############################################################################

	@property
	def value(self): return ControlBase.value.fget(self)

	@value.setter
	def value(self, value):
		ControlBase.value.fset(self, value)		
		self.__clearLayout()			

		if value is None or value=='':  return 
		
		if isinstance( self._value, list ):
			for w in self._value:
				if w!=None and w!="": self.form.layout().removeWidget( w.form )
		
		if isinstance( value, list ):
			for w in value:
				self.form.layout().addWidget( w.form )
		else:
			self.form.layout().addWidget( value.form )

		#The initForm should be called only for the BaseWidget

		if isinstance(value, BaseWidget) and not value._formLoaded: 
			print "passou aqui", value.title
			value.initForm()
		
		
	@property
	def form(self): return self

	def save(self, data={}): 
		if self.value is not None and self.value!='':
			data['value'] = {}
			self.value.save(data['value'])
		return data

	def load(self, data):
		if 'value' in data and self.value is not None and self.value!='': 
			self.value.load(data['value'])

	def __clearLayout(self):
		if self.form.layout() is not None:
			old_layout = self.form.layout()
			for i in reversed(range(old_layout.count())):
				old_layout.itemAt(i).widget().setParent(None)
			

	def show(self):
		"""
		Show the control
		"""
		QtGui.QWidget.show(self)

	def hide(self):
		"""
		Hide the control
		"""
		QtGui.QWidget.hide(self)