#!/usr/bin/python
# -*- coding: utf-8 -*-

import json, AnyQt

from pyforms.utils.settings_manager import conf

from AnyQt.QtWidgets import QFrame
from AnyQt.QtWidgets import QVBoxLayout
from AnyQt.QtWidgets import QTabWidget
from AnyQt.QtWidgets import QSplitter
from AnyQt.QtWidgets import QHBoxLayout
from AnyQt.QtWidgets import QSpacerItem
from AnyQt.QtWidgets import QSizePolicy
from AnyQt.QtWidgets import QLabel
from AnyQt.QtGui     import QFont
from AnyQt.QtWidgets import QFileDialog
from AnyQt.QtWidgets import QApplication
from AnyQt           import QtCore, _api

from pyforms.gui.controls.ControlBase import ControlBase

from AnyQt.QtWidgets import QMessageBox


class BaseWidget(QFrame):
    """
    The class implements the most basic widget or window.
    """

    def __init__(self, *args, **kwargs):
        title = kwargs.get('title', args[0] if len(args)>0 else '')

        parent_win = kwargs.get('parent_win', kwargs.get('parent_widget', None))
        win_flag   = kwargs.get('win_flag', None)

        self._parent_widget = parent_win

        if parent_win is not None and win_flag is None: win_flag = QtCore.Qt.Dialog

        QFrame.__init__(self) if parent_win is None else QFrame.__init__(self, parent_win, win_flag)

        layout = QVBoxLayout()
        self.setLayout(layout)
        
        if _api.USED_API == _api.QT_API_PYQT5:
            layout.setContentsMargins(0,0,0,0)
        elif _api.USED_API == _api.QT_API_PYQT4:
            layout.setMargin(0)

        self.title = title

        self.title = title
        self.has_progress = False

        self._mainmenu = []
        self._splitters = []
        self._tabs = []
        self._formset = None
        self._formLoaded = False
        self.uid = id(self)

        self.setAccessibleName('BaseWidget')

    ##########################################################################
    ############ FUNCTIONS  ##################################################
    ##########################################################################

    def init_form(self):
        """
        Generate the module Form
        """
        if not self._formLoaded:

            
            if self._formset is not None:
                control = self.generate_panel(self._formset)
                self.layout().addWidget(control)
            else:
                allparams = self.controls
                for key, param in allparams.items():
                    param.parent = self
                    param.name = key
                    self.layout().addWidget(param.form)
            self._formLoaded = True

    def set_margin(self, margin):
        if _api.USED_API == _api.QT_API_PYQT5:
            self.layout().setContentsMargins(margin,margin,margin,margin)
        elif _api.USED_API == _api.QT_API_PYQT4:
            self.layout().setMargin(margin)


    def generate_tabs(self, formsetdict):
        """
        Generate QTabWidget for the module form
        @param formset: Tab form configuration
        @type formset: dict
        """
        tabs = QTabWidget(self)
        for key, item in sorted(formsetdict.items()):
            ctrl = self.generate_panel(item)
            tabs.addTab(ctrl, key[key.find(':') + 1:])
        return tabs

    def generate_panel(self, formset):
        """
        Generate a panel for the module form with all the controls
        formset format example: [('_video', '_arenas', '_run'), {"Player":['_threshold', "_player", "=", "_results", "_query"], "Background image":[(' ', '_selectBackground', '_paintBackground'), '_image']}, "_progress"]
        tuple: will display the controls in the same horizontal line
        list: will display the controls in the same vertical line
        dict: will display the controls in a tab widget
        '||': will plit the controls in a horizontal line
        '=': will plit the controls in a vertical line
        @param formset: Form configuration
        @type formset: list
        """
        control = None
        if '=' in formset:
            control = QSplitter(QtCore.Qt.Vertical)
            tmp = list(formset)
            index = tmp.index('=')
            firstPanel = self.generate_panel(formset[0:index])
            secondPanel = self.generate_panel(formset[index + 1:])
            control.addWidget(firstPanel)
            control.addWidget(secondPanel)
            self._splitters.append(control)
            return control
        elif '||' in formset:
            control = QSplitter(QtCore.Qt.Horizontal)
            tmp = list(formset)
            rindex = lindex = index = tmp.index('||')
            rindex -= 1
            rindex += 2
            if isinstance(formset[lindex - 1], int):
                lindex = lindex - 1
            if len(formset) > rindex and isinstance(formset[index + 1], int):
                rindex += 1
            firstPanel = self.generate_panel(formset[0:lindex])
            secondPanel = self.generate_panel(formset[rindex:])
            if isinstance(formset[index - 1], int):
                firstPanel.setMaximumWidth(formset[index - 1])
            if isinstance(formset[index + 1], int):
                secondPanel.setMaximumWidth(formset[index + 1])
            control.addWidget(firstPanel)
            control.addWidget(secondPanel)
            self._splitters.append(control)
            return control
        control = QFrame(self)
        layout = None
        if type(formset) is tuple:
            layout = QHBoxLayout()
            for row in formset:
                if isinstance(row, (list, tuple)):
                    panel = self.generate_panel(row)
                    layout.addWidget(panel)
                elif row == " ":
                    spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
                    layout.addItem(spacer)
                elif type(row) is dict:
                    c = self.generate_tabs(row)
                    layout.addWidget(c)
                    self._tabs.append(c)
                else:
                    param = self.controls.get(row, None)
                    if param is None:
                        label = QLabel()
                        label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
                        # layout.addWidget( label )

                        if row.startswith('info:'):
                            label.setText(row[5:])
                            font = QFont()
                            font.setPointSize(10)
                            label.setFont(font)
                            label.setAccessibleName('info')
                        elif row.startswith('h1:'):
                            label.setText(row[3:])
                            font = QFont()
                            font.setPointSize(17)
                            font.setBold(True)
                            label.setFont(font)
                            label.setAccessibleName('h1')
                        elif row.startswith('h2:'):
                            label.setText(row[3:])
                            font = QFont()
                            font.setPointSize(16)
                            font.setBold(True)
                            label.setFont(font)
                            label.setAccessibleName('h2')
                        elif row.startswith('h3:'):
                            label.setText(row[3:])
                            font = QFont()
                            font.setPointSize(15)
                            font.setBold(True)
                            label.setFont(font)
                            label.setAccessibleName('h3')
                        elif row.startswith('h4:'):
                            label.setText(row[3:])
                            font = QFont()
                            font.setPointSize(14)
                            font.setBold(True)
                            label.setFont(font)
                            label.setAccessibleName('h4')
                        elif row.startswith('h5:'):
                            label.setText(row[3:])
                            font = QFont()
                            font.setPointSize(12)
                            font.setBold(True)
                            label.setFont(font)
                            label.setAccessibleName('h5')
                        else:
                            label.setText(row)
                            font = QFont()
                            font.setPointSize(10)
                            label.setFont(font)
                            label.setAccessibleName('msg')
                        label.setToolTip(label.text())
                        layout.addWidget(label)
                    else:
                        param.parent = self
                        param.name = row
                        layout.addWidget(param.form)
        elif type(formset) is list:
            layout = QVBoxLayout()
            for row in formset:
                if isinstance(row, (list, tuple)):
                    panel = self.generate_panel(row)
                    layout.addWidget(panel)
                elif row == " ":
                    spacer = QSpacerItem(
                        20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
                    layout.addItem(spacer)
                elif type(row) is dict:
                    c = self.generate_tabs(row)
                    layout.addWidget(c)
                    self._tabs.append(c)
                else:
                    param = self.controls.get(row, None)
                    if param is None:
                        label = QLabel()
                        label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
                        label.resize(30, 30)
                        # layout.addWidget( label )

                        if row.startswith('info:'):
                            label.setText(row[5:])
                            font = QFont()
                            font.setPointSize(10)
                            label.setFont(font)
                            label.setAccessibleName('info')
                        elif row.startswith('h1:'):
                            label.setText(row[3:])
                            font = QFont()
                            font.setPointSize(17)
                            font.setBold(True)
                            label.setFont(font)
                            label.setAccessibleName('h1')
                        elif row.startswith('h2:'):
                            label.setText(row[3:])
                            font = QFont()
                            font.setPointSize(16)
                            font.setBold(True)
                            label.setFont(font)
                            label.setAccessibleName('h2')
                        elif row.startswith('h3:'):
                            label.setText(row[3:])
                            font = QFont()
                            font.setPointSize(15)
                            font.setBold(True)
                            label.setFont(font)
                            label.setAccessibleName('h3')
                        elif row.startswith('h4:'):
                            label.setText(row[3:])
                            font = QFont()
                            font.setPointSize(14)
                            font.setBold(True)
                            label.setFont(font)
                            label.setAccessibleName('h4')
                        elif row.startswith('h5:'):
                            label.setText(row[3:])
                            font = QFont()
                            font.setPointSize(12)
                            font.setBold(True)
                            label.setFont(font)
                            label.setAccessibleName('h5')
                        else:
                            label.setText(row)
                            font = QFont()
                            font.setPointSize(10)
                            label.setFont(font)
                            label.setAccessibleName('msg')

                        label.setToolTip(label.text())

                        layout.addWidget(label)
                    else:
                        param.parent = self
                        param.name = row
                        layout.addWidget(param.form)
        
        if _api.USED_API == _api.QT_API_PYQT5:
            layout.setContentsMargins(0,0,0,0)
        elif _api.USED_API == _api.QT_API_PYQT4:
            layout.setMargin(0)
            
        control.setLayout(layout)
        return control

    def show(self):
        self.init_form()
        super(BaseWidget, self).show()

    def save_form(self, data={}, path=None):
        allparams = self.controls

        if hasattr(self, 'load_order'):
            for name in self.load_order:
                param = allparams[name]
                data[name] = {}
                param.save_form(data[name])
        else:
            for name, param in allparams.items():
                data[name] = {}
                param.save_form(data[name])
        return data

    def load_form(self, data, path=None):
        allparams = self.controls

        if hasattr(self, 'load_order'):
            for name in self.load_order:
                param = allparams[name]
                if name in data:
                    param.load_form(data[name])
        else:
            for name, param in allparams.items():
                if name in data:
                    param.load_form(data[name])
                # self.init_form()

    def save_window(self):
        allparams = self.controls
        data = {}
        self.save_form(data)

        filename, _ = QFileDialog.getSaveFileName(self, 'Select file')
        with open(filename, 'w') as output_file: json.dump(data, output_file)

    def load_form_filename(self, filename):
        with open(filename, 'r') as pkl_file:
            project_data = json.load(pkl_file)
        data = dict(project_data)
        self.load_form(data)

    def load_window(self):
        filename, _ = QFileDialog.getOpenFileNames(self, 'Select file')
        self.load_form_filename(str(filename[0]))

    def close(self):
        super(BaseWidget, self).close()


    def question(self, msg, title=None, ):
        reply = QMessageBox.question(self, title, msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes or reply == QMessageBox.No:
            return reply == QMessageBox.Yes
        else:
            return None

    def message(self, msg, title=None, msg_type=None):
        if msg_type=='success':
            QMessageBox.about(self, title, msg)
        elif msg_type=='info':
            QMessageBox.information(self, title, msg)
        elif msg_type=='warning':
            QMessageBox.warning(self, title, msg)
        elif msg_type=='error':
            QMessageBox.critical(self, title, msg)
        elif msg_type=='about':
            QMessageBox.about(self, title, msg)
        elif msg_type=='aboutQt':
            QMessageBox.aboutQt(self, msg)
        else:
            QMessageBox.about(self, title, msg)


    def success(self,   msg, title=None):   self.message(msg, title, msg_type='success')
    def info(self,      msg, title=None):   self.message(msg, title, msg_type='info')
    def warning(self,   msg, title=None):   self.message(msg, title, msg_type='warning');
    def alert(self,     msg, title=None):   self.message(msg, title, msg_type='error')
    def critical(self,  msg, title=None):   self.message(msg, title, msg_type='error')
    def about(self,     msg, title=None):   self.message(msg, title, msg_type='about')
    def aboutQt(self,   msg, title=None):   self.message(msg, title, msg_type='aboutQt')

    def message_popup(self, msg, title='', buttons=None, handler=None, msg_type='success'):
        pass
    def success_popup(self, msg, title='', buttons=None, handler=None):
        return self.message_popup(msg, title, buttons, handler, msg_type='success')
    def info_popup(self, msg, title='', buttons=None, handler=None):
        return self.message_popup(msg, title, buttons, handler, msg_type='info')
    def warning_popup(self, msg, title='', buttons=None, handler=None):
        return self.message_popup(msg, title, buttons, handler, msg_type='warning')
    def alert_popup(self, msg, title='', buttons=None, handler=None):
        return self.message_popup(msg, title, buttons, handler, msg_type='alert')


    ##########################################################################
    ############ GUI functions ###############################################
    ##########################################################################

    def set_margin(self, margin):
        if AnyQt.USED_API=='pyqt5':
            self.layout().setContentsMargins(margin,margin,margin,margin)
        else:
            self.layout().setMargin(margin)

    ##########################################################################
    ############ EVENTS ######################################################
    ##########################################################################

    def before_close_event(self):
        """ 
        Do something before closing widget 
        Note that the window will be closed anyway    
        """
        pass

    ##########################################################################
    ############ Properties ##################################################
    ##########################################################################

    @property
    def controls(self):
        """
        Return all the form controls from the the module
        """
        result = {}
        for name, var in vars(self).items():
            try:
                if isinstance(var, ControlBase):
                    result[name] = var
            except:
                pass
        return result

    ############################################################################
    ############ GUI Properties ################################################
    ############################################################################


    @property
    def form_has_loaded(self):
        return self._formLoaded

    
    @property 
    def form(self): 
        return self 
    
    @property
    def visible(self):
        return self.isVisible()

    @property
    def mainmenu(self):
        return self._mainmenu
    @mainmenu.setter
    def mainmenu(self, value):
        self._mainmenu = value


    @property
    def controls(self):
        """
        Return all the form controls from the the module
        """
        result = {}
        for name, var in vars(self).items():
            try:
                if isinstance(var, ControlBase):
                    result[name] = var
            except:
                pass
        return result

    ############################################################################
    ############ GUI Properties ################################################
    ############################################################################


    @property
    def form_has_loaded(self):
        return self._formLoaded

    @property
    def parent_widget(self):
        return self._parent_widget

    @property
    def form(self):
        return self

    @property
    def title(self):
        return self.windowTitle()

    @title.setter
    def title(self, value):
        self.setWindowTitle(value)

    
    @property
    def formset(self):
        return self._formset

    @formset.setter
    def formset(self, value):
        self._formset = value

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        self._uid = value

    
    @property
    def visible(self):
        return self.isVisible()

    

    ##########################################################################
    ############ PRIVATE FUNCTIONS ###########################################
    ##########################################################################
    
    def closeEvent(self, event):
        self.before_close_event()
        super(BaseWidget, self).closeEvent(event)
