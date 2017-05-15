import csv, sys
from pyforms import BaseWidget
from pyforms.Controls import ControlProgress
from pyforms.Controls import ControlButton
from pyforms.Controls import ControlList
from pyforms.Controls import ControlNumber
from pyforms.Controls import ControlSlider
from pyforms.Controls import ControlTextArea
from pyforms.Controls import ControlText
from pyforms.Controls import ControlNumber
from pyforms.Controls import ControlLabel
		
import time
import datetime

from pysettings import conf

if conf.PYFORMS_USE_QT5:
	from PyQt5.QtWidgets import QMessageBox
else:
	from PyQt4.QtGui import QMessageBox



class Graph2Event(BaseWidget):

	def __init__(self, timeline=None):
		super(Graph2Event, self).__init__('Graph to event', parent_win=timeline)
		self.setContentsMargins(10, 10, 10, 10)
		self._timeline = timeline

		# Definition of the forms fields
		self._graphs_list = ControlList('Graphs list (try double click)')
		self._equation    = ControlTextArea('Equation')
		self._eventname   = ControlText('Event name', 'New event')
		self._rownumber   = ControlNumber('Row number')
		self._mindiff 	  = ControlNumber('Minimum of frames', 0)
		self._genevts_btn = ControlButton('Generate events')
		
		self._formset = [
			(
				['_graphs_list'],
				'||', 
				[
					('_eventname','_rownumber','_mindiff'),
					'_equation',
					'_genevts_btn',
				]
			),
		]

		self._graphs_list.cell_double_clicked_event = self.__cell_double_clicked_evt 
		self._graphs_list.readonly = True
		self._graphs_list.select_entire_row = True
		self._genevts_btn.value = self.__generage_events_evt



	def __add__(self, other):
		self._graphs_list += [other.name]
		return self

	def __sub__(self, other):
		self._graphs_list -= other
		return self

	def rename_graph(self, graph_index, newname):
		self._graphs_list.set_value(graph_index, 0, newname)

	@property
	def graphs(self):
		return self._timeline._charts


	def __cell_double_clicked_evt(self, row, column):
		if len(self._equation.value.strip())==0:
			self._equation.value += '[{0}]'.format( self._graphs_list.value[row][column] )
		else:
			self._equation.value += ' and [{0}]'.format( self._graphs_list.value[row][column] )


	def __generage_events_evt(self):
		if len(self._eventname.value.strip())==0: 
			QMessageBox.warning(
				self, "Attention!", 'The event name cannot be empty')
			return

		if len(self._equation.value.strip())==0: 
			QMessageBox.warning(
				self, "Attention!", 'The equation cannot be empty')
			return 

		max_frame = 0
		equation  = self._equation.value
		for i, values in enumerate(self._graphs_list.value):
			graphname = '[{0}]'.format(values[0])

			if graphname in equation: max_frame = max(max_frame, len(self.graphs[i]))

			equation  = equation.replace(graphname, 'graphs[{0}][i]'.format(i) )
		
		graphs = self.graphs

		last_index = None
		last_value = False

		try:		
			for i in range(max_frame):			
				value = eval(equation)
				
				if not last_value and bool(value):
					last_index = i
					last_value = True
				
				if last_value and not bool(value):
					if (i-1-last_index)>=self._mindiff.value:
						self._timeline.addPeriod([last_index, i-1, self._eventname.value], int(self._rownumber.value) ) 
					last_value = False
					last_index = None

			if last_value and (max_frame-last_index)>=self._mindiff.value:
				self._timeline.addPeriod([last_index, max_frame, self._eventname.value], int(self._rownumber.value) ) 
		except Exception as e:
			QMessageBox.warning( self, "Error!", str(e) )
			

		self._timeline.repaint()

	
##################################################################################################################
##################################################################################################################
##################################################################################################################

# Execute the application
if __name__ == "__main__":
	import pyforms
	pyforms.start_app(Graph2Event, geometry=(0, 0, 600, 400))
