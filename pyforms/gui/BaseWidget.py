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

from pyforms.gui.Controls.ControlBase       import ControlBase
from pyforms.gui.Controls.ControlProgress   import ControlProgress
import os, json, subprocess, time
from datetime import datetime, timedelta
from PyQt4 import QtGui, QtCore
from pyforms import conf


class BaseWidget(QtGui.QWidget):
    """
    The class implements the most basic widget or window.
    """

    def __init__(self, title):
        QtGui.QWidget.__init__(self)
        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)
        self.layout().setMargin(0)

        self.title = title

        self._mainmenu = []
        self._splitters = []
        self._tabs = []
        self._formset = None
        self._formLoaded = False

        

    ##########################################################################
    ############ Module functions  ###########################################
    ##########################################################################

    

    def initForm(self):
        """
        Generate the module Form
        """
        if not self._formLoaded:

            if conf.PYFORMS_MODE in ['GUI-OPENCSP']:
                self._progress = ControlProgress("Progress", 0, 100)
                if self._formset != None: self._formset += ['_progress']

            if self._formset is not None:
                control = self.generatePanel(self._formset)
                self.layout().addWidget(control)
            else:
                allparams = self.formControls
                for key, param in allparams.items():
                    param.parent = self
                    param.name = key
                    self.layout().addWidget(param.form)
            self._formLoaded = True

    def generateTabs(self, formsetDict):
        """
        Generate QTabWidget for the module form
        @param formset: Tab form configuration
        @type formset: dict
        """
        tabs = QtGui.QTabWidget(self)
        for key, item in sorted(formsetDict.items()):
            ctrl = self.generatePanel(item)
            tabs.addTab(ctrl, key[key.find(':') + 1:])
        return tabs

    def generatePanel(self, formset):
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
            control = QtGui.QSplitter(QtCore.Qt.Vertical)
            tmp = list(formset)
            index = tmp.index('=')
            firstPanel = self.generatePanel(formset[0:index])
            secondPanel = self.generatePanel(formset[index + 1:])
            control.addWidget(firstPanel)
            control.addWidget(secondPanel)
            self._splitters.append(control)
            return control
        elif '||' in formset:
            control = QtGui.QSplitter(QtCore.Qt.Horizontal)
            tmp = list(formset)
            rindex = lindex = index = tmp.index('||')
            rindex -= 1
            rindex += 2
            if isinstance(formset[lindex - 1], int):
                lindex = lindex - 1
            if len(formset) > rindex and isinstance(formset[index + 1], int):
                rindex += 1
            firstPanel = self.generatePanel(formset[0:lindex])
            secondPanel = self.generatePanel(formset[rindex:])
            if isinstance(formset[index - 1], int):
                firstPanel.setMaximumWidth(formset[index - 1])
            if isinstance(formset[index + 1], int):
                secondPanel.setMaximumWidth(formset[index + 1])
            control.addWidget(firstPanel)
            control.addWidget(secondPanel)
            self._splitters.append(control)
            return control
        control = QtGui.QWidget()
        layout = None
        if type(formset) is tuple:
            layout = QtGui.QHBoxLayout()
            for row in formset:
                if isinstance(row, (list, tuple)):
                    panel = self.generatePanel(row)
                    layout.addWidget(panel)
                elif row == " ":
                    spacer = QtGui.QSpacerItem(
                        40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
                    layout.addItem(spacer)
                elif type(row) is dict:
                    c = self.generateTabs(row)
                    layout.addWidget(c)
                    self._tabs.append(c)
                else:
                    param = self.formControls.get(row, None)
                    if param is None:
                        label = QtGui.QLabel()
                        label.setSizePolicy(
                            QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
                        #layout.addWidget( label )

                        if row.startswith('info:'):
                            label.setText(row[5:])
                            font = QtGui.QFont()
                            font.setPointSize(10)
                            label.setFont(font)
                        elif row.startswith('h1:'):
                            label.setText(row[3:])
                            font = QtGui.QFont()
                            font.setPointSize(17)
                            font.setBold(True)
                            label.setFont(font)
                        elif row.startswith('h2:'):
                            label.setText(row[3:])
                            font = QtGui.QFont()
                            font.setPointSize(16)
                            font.setBold(True)
                            label.setFont(font)
                        elif row.startswith('h3:'):
                            label.setText(row[3:])
                            font = QtGui.QFont()
                            font.setPointSize(15)
                            font.setBold(True)
                            label.setFont(font)
                        elif row.startswith('h4:'):
                            label.setText(row[3:])
                            font = QtGui.QFont()
                            font.setPointSize(14)
                            font.setBold(True)
                            label.setFont(font)
                        elif row.startswith('h5:'):
                            label.setText(row[3:])
                            font = QtGui.QFont()
                            font.setPointSize(12)
                            font.setBold(True)
                            label.setFont(font)
                        else:
                            label.setText(row)
                            font = QtGui.QFont()
                            font.setPointSize(10)
                            label.setFont(font)

                        layout.addWidget(label)
                    else:
                        param.parent = self
                        param.name = row
                        layout.addWidget(param.form)
        elif type(formset) is list:
            layout = QtGui.QVBoxLayout()
            for row in formset:
                if isinstance(row, (list, tuple)):
                    panel = self.generatePanel(row)
                    layout.addWidget(panel)
                elif row == " ":
                    spacer = QtGui.QSpacerItem(
                        20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
                    layout.addItem(spacer)
                elif type(row) is dict:
                    c = self.generateTabs(row)
                    layout.addWidget(c)
                    self._tabs.append(c)
                else:
                    param = self.formControls.get(row, None)
                    if param is None:
                        label = QtGui.QLabel()
                        label.setSizePolicy(
                            QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
                        label.resize(30, 30)
                        #layout.addWidget( label )

                        if row.startswith('info:'):
                            label.setText(row[5:])
                            font = QtGui.QFont()
                            font.setPointSize(10)
                            label.setFont(font)
                        elif row.startswith('h1:'):
                            label.setText(row[3:])
                            font = QtGui.QFont()
                            font.setPointSize(17)
                            font.setBold(True)
                            label.setFont(font)
                        elif row.startswith('h2:'):
                            label.setText(row[3:])
                            font = QtGui.QFont()
                            font.setPointSize(16)
                            font.setBold(True)
                            label.setFont(font)
                        elif row.startswith('h3:'):
                            label.setText(row[3:])
                            font = QtGui.QFont()
                            font.setPointSize(15)
                            font.setBold(True)
                            label.setFont(font)
                        elif row.startswith('h4:'):
                            label.setText(row[3:])
                            font = QtGui.QFont()
                            font.setPointSize(14)
                            font.setBold(True)
                            label.setFont(font)
                        elif row.startswith('h5:'):
                            label.setText(row[3:])
                            font = QtGui.QFont()
                            font.setPointSize(12)
                            font.setBold(True)
                            label.setFont(font)
                        else:
                            label.setText(row)
                            font = QtGui.QFont()
                            font.setPointSize(10)
                            label.setFont(font)

                        layout.addWidget(label)
                    else:
                        param.parent = self
                        param.name = row
                        layout.addWidget(param.form)
        layout.setMargin(0)
        control.setLayout(layout)
        return control

    ##########################################################################
    ############ Parent class functions reemplementation #####################
    ##########################################################################

    def show(self):
        """
        OTModuleProjectItem.show reimplementation
        """
        self.initForm()
        super(BaseWidget, self).show()

    ##########################################################################
    ############ Properties ##################################################
    ##########################################################################

    @property
    def formControls(self):
        """
        Return all the form controls from the the module
        """
        result = {}
        for name, var in vars(self).items():
            if isinstance(var, ControlBase):
                result[name] = var
        return result

    def start_progress(self, total=100):
        self._progress.max = total
        self._progress.min = 0
        self._progress.value = 0
        self._processing_count = 0
        self._processing_initial_time = time.time()

    def update_progress(self, progress=1):
        self._progress.value = self._processing_count
        self._processing_count += progress

        div = int(self._progress.max / 400)
        if div == 0:
            div = 1
        if (self._processing_count % div) == 0:
            self._processing_last_time = time.time()
            total_passed_time = self._processing_last_time - \
                self._processing_initial_time
            remaining_time = (
                (self._progress.max * total_passed_time) / self._processing_count) - total_passed_time
            time_remaining = datetime(
                1, 1, 1) + timedelta(seconds=remaining_time)
            time_elapsed = datetime(
                1, 1, 1) + timedelta(seconds=(total_passed_time))

            values = (time_elapsed.day - 1, time_elapsed.hour, time_elapsed.minute, time_elapsed.second,
                      time_remaining.day -
                      1, time_remaining.hour, time_remaining.minute, time_remaining.second,
                      (float(self._processing_count) / float(self._progress.max)
                       ) * 100.0, self._processing_count, self._progress.max,
                      self._processing_count / total_passed_time)
            self._progress.label = "Elapsed: %d:%d:%d:%d; Remaining: %d:%d:%d:%d; Processed %0.2f %%  (%d/%d); Cicles per second: %0.3f" % values

        QtGui.QApplication.processEvents()

    def end_progress(self):
        # self.update_progress()
        self._progress.value = self._progress.max

    def executeCommand(self, cmd, cwd=None):
        if cwd is not None:
            currentdirectory = os.getcwd()
            os.chdir(cwd)
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (output, error) = proc.communicate()
        if cwd is not None:
            os.chdir(currentdirectory)
        if error:
            print('Error: ' + error)
        return output

    @property
    def form(self): return self

    @property
    def title(self): return self.windowTitle()

    @title.setter
    def title(self, value): self.setWindowTitle(value)

    @property
    def mainmenu(self): return self._mainmenu

    @mainmenu.setter
    def mainmenu(self, value): self._mainmenu = value


    def save(self, data):
        allparams = self.formControls
        for name, param in allparams.items():
            data[name] = {}
            param.save(data[name])

    def saveWindow(self):
        allparams = self.formControls
        data = {}
        self.save(data)

        filename = QtGui.QFileDialog.getSaveFileName(self, 'Select file')

        with open(filename, 'w') as output_file:
            json.dump(data, output_file)

    def loadWindowData(self, filename):
        with open(filename, 'r') as pkl_file:
            project_data = json.load(pkl_file)
        data = dict(project_data)
        self.load(data)

    def load(self, data):
        allparams = self.formControls
        for name, param in allparams.items():
            if name in data:
                param.load(data[name])
        self.initForm()

    def loadWindow(self):
        filename = QtGui.QFileDialog.getOpenFileNames(self, 'Select file')
        self.loadWindowData(str(filename[0]))
