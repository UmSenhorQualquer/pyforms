# !/usr/bin/python
# -*- coding: utf-8 -*-

from pysettings      import conf

from AnyQt           import QtCore, uic
from AnyQt.QtWidgets import QMenu, QAction
from AnyQt.QtGui     import QIcon, QKeySequence

class ControlBase(object):
    """
    This class represents the most basic control that can exist
    A Control is a Widget or a group of widgets that can be reused from application to application

    @undocumented: __repr__
    """

    def __init__(self, *args, **kwargs):
        self._form      = None  # Qt widget
        self._parent    = None  # Parent window
        self._popup_menu = None
        
        self._help          = kwargs.get('helptext', None)
        self._value         = kwargs.get('default',  None)
        self._label         = kwargs.get('label', args[0] if len(args)>0 else '')
        """
        self._visible       = kwargs.get('visible', True)
        self._error         = kwargs.get('error', False)
        self._css           = kwargs.get('css', None)
        self._enabled       = kwargs.get('enabled', True)
        self._readonly      = kwargs.get('readonly', False)
        self._label_visible = kwargs.get('label_visible', True)
        """
        
        self.init_form()


    def __repr__(self): return str(self._value)

    ##########################################################################
    ############ Funcions ####################################################
    ##########################################################################

    def init_form(self):
        """
        Load Control and initiate the events
        """     
        if self.help: self.form.setToolTip(self.help)
   


    def load_form(self, data, path=None):
        """
        Load a value from the dict variable
        @param data: dictionary with the value of the Control
        """
        if 'value' in data:
            self.value = data['value']

    def save_form(self, data, path=None):
        """
        Save a value to dict variable
        @param data: dictionary with to where the value of the Control will be added
        """
        if self.value:
            data['value'] = self.value
        return data

    def show(self):
        """
        Show the control
        """
        if self.form is None:
            return
        self.form.show()

    def hide(self):
        """
        Hide the control
        """
        if self.form is None:
            return
        self.form.hide()


    def __create_popup_menu(self):
        if not self._popup_menu:
            self.form.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.form.customContextMenuRequested.connect(self._open_popup_menu)
            self._popup_menu = QMenu(self.parent)
            self._popup_menu.aboutToShow.connect( self.about_to_show_contextmenu_event)

    def add_popup_submenu(self, label, submenu=None):
        self.__create_popup_menu()
        menu = submenu if submenu else self._popup_menu
        submenu = QMenu(label, menu)
        menu.addMenu(submenu)
        return submenu

    def add_popup_menu_option(self, label, function_action=None, key=None, icon=None, submenu=None):
        """
        Add an option to the Control popup menu
        @param label:           label of the option.
        @param function_action:  function called when the option is selected.
        @param key:             shortcut key
        @param icon:            icon
        """
        self.__create_popup_menu()

        menu = submenu if submenu else self._popup_menu

        if label == "-":
            return menu.addSeparator()
        else:
            action = QAction(label, self.form)
            if icon is not None:
                action.setIconVisibleInMenu(True)
                action.setIcon(icon if isinstance(icon, QIcon) else QIcon(icon) )
            if key != None:
                action.setShortcut(QKeySequence(key))
            if function_action:
                action.triggered.connect(function_action)
                menu.addAction(action)
            return action


    ##########################################################################
    ############ Events ######################################################
    ##########################################################################

    def changed_event(self):
        """
        Function called when ever the Control value is changed
        """
        return True

    def about_to_show_contextmenu_event(self):
        """
        Function called before open the Control popup menu
        """
        pass

    def _open_popup_menu(self, position):
        if self._popup_menu:
            self._popup_menu.exec_(self.form.mapToGlobal(position))

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
            self.changed_event()

    
    @property
    def name(self): return self.form.objectName()

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
    def visible(self): return self.form.isVisible()

    @property
    def help(self): return self._help if self._help else ''

    @property
    def error(self): return None

    @error.setter
    def error(self, value):
        pass

    @property
    def label_visible(self): return None

    @label_visible.setter
    def label_visible(self, value):
        pass

    @property
    def readonly(self): return None

    @readonly.setter
    def readonly(self, value):
        pass

    @property
    def css(self): return None

    @css.setter
    def css(self, value):
        pass


    ##########################################################################
    ############ Properties just for the GUI version #########################
    ##########################################################################

    ##########################################################################
    # Return the QT widget

    @property
    def form(self):
        """
        Returns the Widget of the control. 
        This property will be deprecated in a future version.
        """
        return self._form
