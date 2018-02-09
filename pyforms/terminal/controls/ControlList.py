#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.Controls.ControlList

"""
import logging
from pyforms.terminal.BaseWidget import BaseWidget
from pyforms.terminal.controls.ControlBase import ControlBase


logger = logging.getLogger(__name__)


class ControlList(ControlBase):
    """ This class represents a wrapper to the table widget
        It allows to implement a list view
    """
    def __init__(self, *args, **kwargs):
        if 'default' not in kwargs: kwargs['default'] = []
        super(ControlList, self).__init__(*args, **kwargs)


    def clear(self, headers=False):
        pass

    def save_form(self, data, path=None):
        if self.value:
            rows = []
            for row in range(self.rows_count):
                columns = []
                for column in range(self.columns_count):
                    v = self.get_value(column, row)
                    if isinstance(v, BaseWidget):
                        columns.append(v.save({}))
                    else:
                        columns.append(str(v))
                rows.append(columns)
            data['value'] = rows
        return data

    def load_form(self, data, path=None):
        rows = data.get('value')
        
        if self.value is not None and rows is not None:
            for row_index in range(len(self.value)):
                for column_index in range(len(self.value[row_index])):
                    v = self.get_value(column_index, row_index)

                    if isinstance(v, BaseWidget):
                        v.load_form(rows[row_index][column_index], path)
                    else:
                        self.value[row_index] = list(self.value[row_index])
                        self.value[row_index][column_index] = rows[row_index][column_index]
        elif rows is not None:
            self.value = rows

    def __add__(self, other):
        self._value.append(val)
        return self
        """
        row_index = self.tableWidget.rowCount()

        self.tableWidget.insertRow(row_index)

        #increase the number of columns if necessary ####
        if self.tableWidget.currentColumn() < len(other):
            self.tableWidget.setColumnCount(len(other))
        #################################################

        for column, e in enumerate(other): self.set_value(column, row_index, e)

        self.tableWidget.resizeColumnsToContents()

        # auto scroll the list to the new inserted item ##################
        if self.autoscroll:
            self.tableWidget.scrollToItem( self.get_cell(0,row_index) )
        ##################################################################
        return self
        """

    def __sub__(self, other):
        self._value.remove(other)
        return self
        """
        if isinstance(other, int):
            if other < 0:
                indexToRemove = self.tableWidget.currentRow()
            else:
                indexToRemove = other

            self.tableWidget.removeRow(indexToRemove)
        return self
        """

    def set_value(self, column, row, value):
        self.value[row][column] = value

    def get_value(self, column, row):
        return self.value[row][column]

    def resize_rows_contents(self):
        pass

    def get_currentrow_value(self):
        return None

    def get_cell(self, column, row):
        return None

    def set_sorting_enabled(self, value):
        pass

    ##########################################################################
    ############ EVENTS ######################################################
    ##########################################################################

    def data_changed_event(self, row, col, item):
        pass

    def item_selection_changed_event(self):
        pass

    def current_cell_changed_event(self, next_row, next_col, previous_row, previous_col):
        pass

    def current_item_changed_event(self, current, previous):
        pass

    def cell_double_clicked_event(self, row, column):
        pass

    ##########################################################################
    ############ PROPERTIES ##################################################
    ##########################################################################


    @property
    def horizontal_headers(self):
        return self._horizontalHeaders

    @horizontal_headers.setter
    def horizontal_headers(self, horizontal_headers):
        """Set horizontal headers in the table list."""

        self._horizontalHeaders = horizontal_headers

        
    @property
    def word_wrap(self):
        return True

    @word_wrap.setter
    def word_wrap(self, value):
        pass

    @property
    def readonly(self):
        return False

    @readonly.setter
    def readonly(self, value):
        pass

    @property
    def select_entire_row(self):
        pass

    @select_entire_row.setter
    def select_entire_row(self, value):
        pass

    @property
    def rows_count(self):
        return 0

    @property
    def columns_count(self):
        return 0

    def __len__(self):
        return 0

   
    # TODO: implement += on self.value? I want to add a list of tuples to
    # self.value

    @property
    def selected_rows_indexes(self):
        return None

    @property
    def selected_row_index(self):
        pass

    @property
    def icon_size(self):
        return 0

    @icon_size.setter
    def icon_size(self, value):
        pass

    @property
    def autoscroll(self): return False
    @autoscroll.setter
    def autoscroll(self, value): pass

