#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.controls.ControlList

"""
import logging
import os

from pyforms.utils.settings_manager import conf

from AnyQt           import QtCore, uic
from AnyQt.QtWidgets import QTableWidgetItem, QWidget, QAbstractItemView
from AnyQt.QtGui     import QIcon

from pyforms.gui.basewidget import BaseWidget
from pyforms.gui.controls.ControlBase import ControlBase

logger = logging.getLogger(__name__)


class ControlList(ControlBase, QWidget):
    """ This class represents a wrapper to the table widget
        It allows to implement a list view
    """

    CELL_VALUE_BEFORE_CHANGE = None  # store value when cell is double clicked

    def __init__(self, *args, **kwargs):
        QWidget.__init__(self)

        self._plusFunction  = kwargs.get('add_function', None)
        self._minusFunction = kwargs.get('remove_function', None)
        ControlBase.__init__(self, *args, **kwargs)

        self.autoscroll         = kwargs.get('autoscroll',          True)
        self.resizecolumns      = kwargs.get('resizecolumns',       True)
        self.select_entire_row  = kwargs.get('select_entire_row',   False)
        self.horizontal_headers = kwargs.get('horizontal_headers',  None)

    ##########################################################################
    ############ FUNCTIONS ###################################################
    ##########################################################################

    def init_form(self):
        plusFunction  = self._plusFunction
        minusFunction = self._minusFunction

        # Get the current path of the file
        rootPath = os.path.dirname(__file__)
        # Load the UI for the self instance
        uic.loadUi(os.path.join(rootPath, "list.ui"), self)

        self.label = self._label

        self.tableWidget.currentCellChanged.connect(self.tableWidgetCellChanged)
        self.tableWidget.currentItemChanged.connect(self.tableWidgetItemChanged)
        self.tableWidget.itemSelectionChanged.connect(self.tableWidgetItemSelectionChanged)
        self.tableWidget.cellDoubleClicked.connect(self.tableWidgetCellDoubleClicked)
        self.tableWidget.model().dataChanged.connect(self._dataChangedEvent)


        self.tableWidget.horizontalHeader().setVisible(False)

        if plusFunction is None and minusFunction is None:
            self.plusButton.hide()
            self.minusButton.hide()
        elif plusFunction is None:
            self.plusButton.hide()
            self.minusButton.pressed.connect(minusFunction)
        elif minusFunction is None:
            self.minusButton.hide()
            self.plusButton.pressed.connect(plusFunction)
        else:
            self.plusButton.pressed.connect(plusFunction)
            self.minusButton.pressed.connect(minusFunction)

        

    def __repr__(self):
        return "ControlList " + str(self._value)

    def clear(self, headers=False):

        for row in range(self.rows_count):
            columns = []
            for column in range(self.columns_count):
                v = self.get_value(column, row)
                if isinstance(v, BaseWidget):
                    v.destroy()

        if headers:
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(3)
            self.tableWidget.setRowCount(0)
        else:
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(0)

    def save_form(self, data, path=None):
        if self.value:
            rows = []
            for row in range(self.rows_count):
                columns = []
                for column in range(self.columns_count):
                    v = self.get_value(column, row)
                    if isinstance(v, BaseWidget):
                        columns.append(v.save_form({}, path))
                    else:
                        columns.append(str(v))
                rows.append(columns)
            data['value'] = rows
        return data

    def load_form(self, data, path=None):
        if self.value:
            rows = data['value']
            for row in range(len(rows)):
                for column in range(len(rows[row])):
                    v = self.get_value(column, row)
                    if isinstance(v, BaseWidget):
                        v.load_form(rows[row][column], path)
                    else:
                        self.set_value(column, row, rows[row][column])
        elif 'value' in data.keys():
            self.value = data['value']

    def __add__(self, other):
        row_index = self.tableWidget.rowCount()

        self.tableWidget.insertRow(row_index)

        #increase the number of columns if necessary ####
        if self.tableWidget.currentColumn() < len(other):
            self.tableWidget.setColumnCount(len(other))
        #################################################

        for column, e in enumerate(other): self.set_value(column, row_index, e)

        #Auto resize the columns if the flag is activated ################
        if self.resizecolumns:
            self.tableWidget.resizeColumnsToContents()
        ##################################################################

        # auto scroll the list to the new inserted item ##################
        if self.autoscroll:
            self.tableWidget.scrollToItem( self.get_cell(0,row_index) )
        ##################################################################
        return self

    def __sub__(self, other):

        if isinstance(other, int):
            if other < 0:
                indexToRemove = self.tableWidget.currentRow()
            else:
                indexToRemove = other

            self.tableWidget.removeRow(indexToRemove)
        return self

    def set_value(self, column, row, value):
        if isinstance(value, QWidget):
            self.tableWidget.setCellWidget(row, column, value)
            value.show()
            self.tableWidget.setRowHeight(row, value.height())
        elif isinstance(value, ControlBase):
            self.tableWidget.setCellWidget(row, column, value.form)
            value.show()
            self.tableWidget.setRowHeight(row, value.form.height())
        else:
            args = [value] if not hasattr(value, 'icon') else [QIcon(value.icon), value]
            item = QTableWidgetItem()
            item.setData(QtCore.Qt.EditRole, *args)
            self.tableWidget.setItem(row, column, item)

    def get_value(self, column, row):
        try:
            return str(self.tableWidget.item(row, column).text())
        except AttributeError as err:
            return self.tableWidget.cellWidget(row, column)
        except AttributeError as err:
            return ''

    def resize_rows_contents(self):
        self.tableWidget.resizeRowsToContents()

    def get_currentrow_value(self):
        currentRow = self.tableWidget.currentRow()
        if not currentRow < 0:
            return self.value[currentRow]
        else:
            return []

    def get_cell(self, column, row):
        return self.tableWidget.item(row, column)

    def set_sorting_enabled(self, value):
        """
        Enable or disable columns sorting
        
        :param bool value: True to enable sorting, False otherwise 
        """
        self.tableWidget.setSortingEnabled(value)

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
        if horizontal_headers is None:
            self._horizontalHeaders = horizontal_headers
            self.tableWidget.horizontalHeader().setVisible(False)
            return


        self._horizontalHeaders = horizontal_headers

        self.tableWidget.setColumnCount(len(horizontal_headers))
        self.tableWidget.horizontalHeader().setVisible(True)

        for idx, header in enumerate(horizontal_headers):
            item = QTableWidgetItem()
            item.setText(header)
            self.tableWidget.setHorizontalHeaderItem(idx, item)

    @property
    def word_wrap(self):
        return self.tableWidget.wordWrap()

    @word_wrap.setter
    def word_wrap(self, value):
        self.tableWidget.setWordWrap(value)

    @property
    def readonly(self):
        return self.tableWidget.editTriggers()

    @readonly.setter
    def readonly(self, value):
        if value:
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            self.tableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)

    @property
    def select_entire_row(self):
        return self.tableWidget.selectionBehavior()

    @select_entire_row.setter
    def select_entire_row(self, value):
        if value:
            self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        else:
            self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectItems)

    @property
    def rows_count(self):
        return self.tableWidget.rowCount()

    @property
    def columns_count(self):
        return self.tableWidget.columnCount()

    def __len__(self):
        return self.rows_count

    @property
    def value(self):
        if hasattr(self, 'tableWidget'):
            results = []
            for row in range(self.tableWidget.rowCount()):
                r = []
                for col in range(self.tableWidget.columnCount()):
                    try:
                        r.append(self.get_value(col, row))
                    except Exception as err:
                        logger.debug(str(err))
                        r.append("")
                results.append(r)
            return results
        return self._value

    @value.setter
    def value(self, value):
        self.clear()
        for row in value: self += row

    # TODO: implement += on self.value? I want to add a list of tuples to
    # self.value

    @property
    def selected_rows_indexes(self):
        result = []
        for index in self.tableWidget.selectedIndexes():
            result.append(index.row())
        return list(set(result))

    @property
    def selected_row_index(self):
        indexes = self.selected_rows_indexes
        if len(indexes) > 0:
            return indexes[0]
        else:
            return None

    @property
    def label(self):
        return self.labelWidget.getText()

    @label.setter
    def label(self, value):
        if value != '':
            self.labelWidget.setText(value)
        else:
            self.labelWidget.hide()

    @property
    def form(self):
        return self

    @property
    def icon_size(self):
        return self.tableWidget.iconSize()

    @icon_size.setter
    def icon_size(self, value):
        if isinstance(value, (tuple, list)):
            self.tableWidget.setIconSize(QtCore.QSize(*value))
        else:
            self.tableWidget.setIconSize(QtCore.QSize(value, value))

    @property
    def autoscroll(self): return self._autoscroll
    @autoscroll.setter
    def autoscroll(self, value): self._autoscroll = value

    @property
    def resizecolumns(self): return self._resizecolumns
    @resizecolumns.setter
    def resizecolumns(self, value): self._resizecolumns = value


    ##########################################################################
    ############ PRIVATE FUNCTIONS ###########################################
    ##########################################################################

    def _dataChangedEvent(self, item):
        self.data_changed_event(item.row(), item.column(), self.tableWidget.model().data(item))
        self.changed_event()

    def tableWidgetCellChanged(self, nextRow, nextCol, previousRow,
                               previousCol):
        self.current_cell_changed_event(nextRow, nextCol, previousRow, previousCol)
        self.changed_event()

    def tableWidgetItemChanged(self, current, previous):
        self.current_item_changed_event(current, previous)
        self.changed_event()

    def tableWidgetItemSelectionChanged(self):
        self.item_selection_changed_event()

    def tableWidgetCellDoubleClicked(self, row, column):
        """
        (From PyQt) This signal is emitted whenever a cell in the table is double clicked.
        The row and column specified is the cell that was double clicked.

        Besides firing this signal, we save the current value, in case the user needs to know the old value.
        :param row:
        :param column:
        :return:
        """
        self.CELL_VALUE_BEFORE_CHANGE = self.get_value(column, row)
        logger.debug("Cell double clicked. Stored value: %s", self.CELL_VALUE_BEFORE_CHANGE)
        self.cell_double_clicked_event(row, column)

    def empty_signal(self, *args, **kwargs):
        """
        Use this function if you want to disconnect a signal temporarily
        """
        pass
