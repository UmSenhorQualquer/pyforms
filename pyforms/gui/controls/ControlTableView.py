#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.controls.ControlList

"""
import logging
import os

from confapp import conf

from AnyQt           import QtCore, uic
from AnyQt.QtWidgets import QTableView, QAbstractItemView
from AnyQt.QtGui     import QIcon

from pyforms.gui.basewidget import BaseWidget
from pyforms.gui.controls.ControlBase import ControlBase

logger = logging.getLogger(__name__)


class ControlTableView(ControlBase, QTableView):
    """ This class represents a wrapper to the table widget
        It allows to implement a list view
    """

    CELL_VALUE_BEFORE_CHANGE = None  # store value when cell is double clicked

    def __init__(self, *args, **kwargs):
        QTableView.__init__(self)
        ControlBase.__init__(self, *args, **kwargs)

        if kwargs.get('select_entire_row', False):
            self.setSelectionBehavior(QAbstractItemView.SelectRows)

    
    ##########################################################################
    ############ EVENTS ######################################################
    ##########################################################################

    
    ##########################################################################
    ############ PROPERTIES ##################################################
    ##########################################################################



    @property
    def value(self):
        return self.model()
        
    @value.setter
    def value(self, value):
        self.setModel(value)
  
    

   
    @property
    def form(self):
        return self

    
    ##########################################################################
    ############ PRIVATE FUNCTIONS ###########################################
    ##########################################################################
