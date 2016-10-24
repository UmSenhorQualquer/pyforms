# !/usr/bin/python
# -*- coding: utf-8 -*-

""" Control Base

"""

from PyQt4 import uic, QtGui, QtCore


__author__ = "Ricardo Ribeiro"
__copyright__ = ""
__credits__ = "Ricardo Ribeiro"
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = ["Ricardo Ribeiro", "Carlos Mão de Ferro"]
__email__ = ["ricardojvr at gmail.com", "cajomferro at gmail.com"]
__status__ = "Development"


class ControlBase(object):
	"""
	This class represents the most basic control that can exist
	A Control is a Widget or a group of widgets that can be reused from application to application

	@undocumented: __repr__
	"""

	def __init__(self, label='', defaultValue='', helptext=''):
		self._help = helptext
		self._value = defaultValue
		self._form = None  # Qt widget
		self._parent = None  # Parent window
		self._label = label  # Label
		self._popupMenu = None
		self.initForm()

	def initForm(self):
		"""
		Load Control and initiate the events
		"""
		pass

	def __repr__(self): return str(self._value)

	##########################################################################
	############ Funcions ####################################################
	##########################################################################

	def load(self, data):
		"""
		Load a value from the dict variable
		@param data: dictionary with the value of the Control
		"""
		if 'value' in data: self.value = data['value']

	def save(self, data):
		"""
		Save a value to dict variable
		@param data: dictionary with to where the value of the Control will be added
		"""
		if self.value: data['value'] = self.value
		return data

	def show(self):
		"""
		Show the control
		"""
		if self.form is None: return
		self.form.show()

	def hide(self):
		"""
		Hide the control
		"""
		if self.form is None: return
		self.form.hide()

	@property 
	def visible(self): return self.form.isVisible()
	@visible.setter
	def visible(self, value):
		if value:
			self.show()
		else:
			self.hide()
			
	def addPopupMenuOption(self, label, functionAction=None, key=None, icon=None):
		"""
		Add an option to the Control popup menu
		@param label:           label of the option.
		@param functionAction:  function called when the option is selected.
		@param key:             shortcut key
		"""
		if not self._popupMenu:
			self.form.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
			self.form.customContextMenuRequested.connect(self._openPopupMenu)
			self._popupMenu = QtGui.QMenu()
			self._popupMenu.aboutToShow.connect( self.aboutToShowContextMenuEvent )
		if label == "-":
			return self._popupMenu.addSeparator()
		else:
			action = QtGui.QAction(label, self.form)
			if icon is not None:
				action.setIconVisibleInMenu(True)
				action.setIcon( QtGui.QIcon(icon) )
			if key != None:
				action.setShortcut(QtGui.QKeySequence(key))
			if functionAction:
				action.triggered.connect(functionAction)
				self._popupMenu.addAction(action)
			return action

	def addPopupSubMenuOption(self, label, options, keys={}):
		"""
		Add submenu options to the Control popup menu
		@param label:   submenu label of the option.
		@param options: dictionary representing the submenu. ex: { 'Example': event function, ... }. 
		@param keys:    shortcut keys. ex: { 'Example': shortcut key, ... }. 
		"""
		if not self._popupMenu:
			self.form.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
			self.form.customContextMenuRequested.connect(self._openPopupMenu)
			self._popupMenu = QtGui.QMenu()
			self._popupMenu.aboutToShow.connect(
				self.aboutToShowContextMenuEvent)

		submenu = QtGui.QMenu(label, self._popupMenu)
		for text, func in options.items():
			if text == "-":
				submenu.addSeparator()
			else:
				action = QtGui.QAction(text, self.form)
				if text in keys:
					action.setShortcut(QtGui.QKeySequence(keys[text]))

				if func:
					action.triggered.connect(func)
					submenu.addAction(action)
		self._popupMenu.addMenu(submenu)

	##########################################################################
	############ Events ######################################################
	##########################################################################

	def changed(self):
		"""
		Function called when ever the Control value is changed
		"""
		return True

	def aboutToShowContextMenuEvent(self):
		"""
		Function called before open the Control popup menu
		"""
		pass

	def _openPopupMenu(self, position):
		if self._popupMenu:
			self._popupMenu.exec_(self.form.mapToGlobal(position))

	##########################################################################
	############ Properties ##################################################
	##########################################################################

	##########################################################################
	# Set the Control enabled or disabled

	@property
	def enabled(self):
		return self.form.isEnabled()

	@enabled.setter
	def enabled(self, value):
		"""@type  value: boolean"""
		self.form.setEnabled(value)

	##########################################################################
	# Return or update the value of the Control

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, value):
		"""
		This property return and set what the control should manage or store.
		@type  value: string
		"""
		oldvalue = self._value
		self._value = value
		if oldvalue != value:
			self.changed()

	@property
	def name(self):
		return self.form.objectName()

	@name.setter
	def name(self, value):
		"""
		This property return and set the name of the control
		@type  value: string
		"""
		self.form.setObjectName(value)

	##########################################################################
	# Return or update the label of the Control

	@property
	def label(self):
		return self._label

	@label.setter
	def label(self, value):
		"""
		Label of the control, if applies
		@type  value: string
		"""
		self._label = value

	##########################################################################
	# Return the QT widget

	@property
	def form(self):
		"""
		Returns the Widget of the control. 
		This property will be deprecated in a future version.
		"""
		return self._form

	##########################################################################
	# Parent window

	@property
	def parent(self): return self._parent

	@parent.setter
	def parent(self, value):
		"""
		Returns or set the parent basewidget where the Control is
		@type  value: BaseWidget
		"""
		self._parent = value


	@property
	def help(self): return self._help if self._help else ''