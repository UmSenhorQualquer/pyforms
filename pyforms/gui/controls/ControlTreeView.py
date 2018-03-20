# !/usr/bin/python
# -*- coding: utf-8 -*-
from pyforms.gui.controls.ControlBase import ControlBase

from AnyQt.QtWidgets import QTreeView, QAbstractItemView
from AnyQt.QtGui     import QStandardItem, QStandardItemModel


class ControlTreeView(ControlBase, QTreeView):

    default_width = None
    
    def __init__(self, *args, **kwargs):
        QTreeView.__init__(self)
        ControlBase.__init__(self, *args, **kwargs)

        self.item_selection_changed_event = kwargs.get('item_selection_changed_event', self.item_selection_changed_event)
        self.item_double_clicked_event    = kwargs.get('item_double_clicked_event',    self.item_double_clicked_event)

    def init_form(self):
        #self.header().hide()
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setUniformRowHeights(True)
        #self.setDragDropMode(QAbstractItemView.InternalMove)
        #self.setDragEnabled(True)
        #self.setAcceptDrops(True)

        self.value = QStandardItemModel() if self._value is None else self._value
        self.selectionChanged = self.selectionChanged

        self.mouseDoubleClickEvent = self.__itemDoubleClicked

    def item_selection_changed_event(self, selected, deselected):
        pass

    def item_double_clicked_event(self, evt):
        pass

    ###################################################
    ## OTHER FUNCTIONS ################################
    ###################################################

    def __itemDoubleClicked(self, evt):
        self.item_double_clicked_event(evt)

    def selectionChanged(self, selected, deselected):
        super(QTreeView, self.form).selectionChanged(selected, deselected)
        self.item_selection_changed_event(selected, deselected)

    ###################################################
    ## PROPERTIES #####################################
    ###################################################

    @property
    def selected_row_index(self):
        for index in self.selectedIndexes():
            return index.row()
        return None

    @property
    def selected_item(self):
        for index in self.selectedIndexes():
            res = []
            while index.isValid():
                res.append( index.data() )
                index = index.parent()
            return list(reversed(res))
        return None

    @property
    def value(self):
        return self.model()
        
    @value.setter
    def value(self, value): self.setModel(value)
    
    
    @property
    def form(self): return self
