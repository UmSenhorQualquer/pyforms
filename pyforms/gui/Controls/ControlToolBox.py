#!/usr/bin/python
# -*- coding: utf-8 -*-

from pysettings import conf

if conf.PYFORMS_USE_QT5:
	from PyQt5.QtWidgets import QToolBox
	from PyQt5.QtWidgets import QFrame
	from PyQt5.QtWidgets import QVBoxLayout
	from PyQt5.QtWidgets import QHBoxLayout

else:
	from PyQt4.QtGui import QToolBox
	from PyQt4.QtGui import QFrame
	from PyQt4.QtGui import QVBoxLayout
	from PyQt4.QtGui import QHBoxLayout

from pyforms.gui.Controls.ControlBase import ControlBase


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
				# layout.setMargin(0);
				widget.setLayout(layout)

				for e in item[1]:
					if isinstance(e, tuple):
						hwidget = QFrame(self.form);
						hlayout = QHBoxLayout();
						# hlayout.setMargin(0);
						hwidget.setLayout(hlayout)
						for ee in e:
							hlayout.addWidget(ee.form)
						widget.layout().addWidget(hwidget)
					else:
						widget.layout().addWidget(e.form)
				self.form.addItem(widget, item[0])
			else:
				self.form.addItem(item.form, item.label)
