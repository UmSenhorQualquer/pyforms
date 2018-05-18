#!/usr/bin/python
# -*- coding: utf-8 -*-

from confapp import conf

from AnyQt 			 import _api
from AnyQt.QtWidgets import QToolBox
from AnyQt.QtWidgets import QFrame
from AnyQt.QtWidgets import QVBoxLayout
from AnyQt.QtWidgets import QHBoxLayout

from pyforms.gui.controls.ControlBase import ControlBase


class ControlToolBox(ControlBase):
	def init_form(self):
		self._form = QToolBox()

	# self.form.layout().setMargin(0)

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, value):
		ControlBase.label.fset(self, value);

		for item in range(self.form.count(), -1, -1): self.form.removeItem(item)

		for item in value:
			if isinstance(item, tuple):
				widget = QFrame(self.form);
				layout = QVBoxLayout();
				
				if _api.USED_API == _api.QT_API_PYQT5:
					layout.setContentsMargins(0,0,0,0)
				elif _api.USED_API == _api.QT_API_PYQT4:
					layout.setMargin(0)

				widget.setLayout(layout)

				for e in item[1]:
					if isinstance(e, tuple):
						hwidget = QFrame(self.form);
						hlayout = QHBoxLayout();
						
						if _api.USED_API == _api.QT_API_PYQT5:
							hlayout.setContentsMargins(0,0,0,0)
						elif _api.USED_API == _api.QT_API_PYQT4:
							hlayout.setMargin(0)
							
						hwidget.setLayout(hlayout)
						for ee in e:
							hlayout.addWidget(ee.form)
						widget.layout().addWidget(hwidget)
					else:
						widget.layout().addWidget(e.form)
				self.form.addItem(widget, item[0])
			else:
				self.form.addItem(item.form, item.label)


	def set_item_enabled(self, index, enabled): 
		"""
		Enable or disable an item
		"""
		self.form.setItemEnabled(index, enabled)

	def is_item_enabled(self, index): 
		"""
		Check if an item is enabled or disabled
		"""
		return self.form.isItemEnabled(index)