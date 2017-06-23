import csv, time, datetime, decimal, logging, sys, numpy as np
from pyforms import BaseWidget
from pyforms.Controls import ControlProgress
from pyforms.Controls import ControlButton
from pyforms.Controls import ControlList
from pyforms.Controls import ControlNumber
from pyforms.Controls import ControlSlider
from pyforms.Controls import ControlText
from pyforms.Controls import ControlLabel

logger = logging.getLogger(__name__)

class GraphsProperties(BaseWidget):

	def __init__(self, timelineWidget=None, parent_win=None):
		super(GraphsProperties, self).__init__('Graphs properties', parent_win=parent_win)
		self.setContentsMargins(10, 10, 10, 10)
		self._mainwindow = parent_win
		self._timeline = timelineWidget

		#self.setMaximumWidth(300)


		# Definition of the forms fields
		self._graphs_list = ControlList('Graphs list')
		self._name        = ControlText('Name')
		self._min_value   = ControlNumber('Min', 0, -sys.float_info.max, sys.float_info.max)
		self._max_value   = ControlNumber('Max', 0, -sys.float_info.max, sys.float_info.max)
		self._values_zoom = ControlSlider('Amplitude', 100, 60, 400)
		self._values_top  = ControlNumber('Bottom', 0, -1000, 1000)
		self._remove_graph_btn = ControlButton('Remove graph')
		self._value 	  = ControlLabel()

		self._graphs_list.readonly = True

		self._formset = [
			(
				['_graphs_list','_remove_graph_btn'],
				'||', 
				[
					' ',
					'_name',
					('_min_value', '_max_value', ' '),
					('_values_top', ' '),
					'_values_zoom',
					'info:Choose one graph and move the mouse over \nthe timeline to visualize the coordenates.',
					'_value'
				]),
			]

		self._graphs_list.select_entire_row = True
		self._graphs_list.item_selection_changed_event = self.__graphs_list_selection_changed

		self._loaded = False
		self._current_selected_graph = None

		self._name.changed_event          = self.__save_graphs_changes
		self._min_value.changed_event     = self.__save_graphs_changes
		self._max_value.changed_event     = self.__save_graphs_changes
		self._values_zoom.changed_event   = self.__save_graphs_changes
		self._values_top.changed_event    = self.__save_graphs_changes

		self._name.enabled          = False
		self._min_value.enabled     = False
		self._max_value.enabled     = False
		self._values_zoom.enabled   = False
		self._values_top.enabled    = False
		self._remove_graph_btn.enabled = False

		self._remove_graph_btn.value = self.__remove_chart


	def __add__(self, other):
		self._graphs_list += [other.name]
		return self

	def __sub__(self, other):
		self._graphs_list -= other
		return self

	def rename_graph(self, graph_index, newname):
		self._graphs_list.set_value(graph_index, 0, newname)

	@property
	def selected_graph(self):
		index = self._graphs_list.selected_row_index
		return self._timeline._charts[index] if (index is not None) else None
	
	@property
	def coordenate_text(self): return self._value
	@coordenate_text.setter
	def coordenate_text(self, value): self._value.value = str(value) if value else ''
	


	def show(self):
		super(GraphsProperties, self).show()
		self._loaded = False


	def __remove_chart(self):
		index = self._graphs_list.selected_row_index
		if index is not None:
			self._current_selected_graph = None
			self._timeline._charts.pop(index)
			self._loaded 					= False
			self._name.enabled          	= False
			self._min_value.enabled     	= False
			self._max_value.enabled     	= False
			self._values_zoom.enabled   	= False
			self._values_top.enabled    	= False
			self._remove_graph_btn.enabled 	= False
			self._timeline.repaint()
			self._mainwindow -= index


	def __graphs_list_selection_changed(self):        
		graph = self.selected_graph
		self._updating_properties = True

		if graph is not None:
			graphmin = np.asscalar(graph.graph_min) if isinstance(graph.graph_min, np.generic) else graph.graph_min
			graphmax = np.asscalar(graph.graph_max) if isinstance(graph.graph_max, np.generic) else graph.graph_max
			
			exponent_min = abs(decimal.Decimal(graphmin).as_tuple().exponent)
			exponent_max = abs(decimal.Decimal(graphmax).as_tuple().exponent)
			exponent_min = 4 if exponent_min>4 else exponent_min
			exponent_max = 4 if exponent_min>4 else exponent_min

			self._name.value            = graph.name
			self._min_value.decimals    = exponent_min
			self._min_value.value       = graph.graph_min
			self._max_value.decimals    = exponent_max
			
			self._max_value.value   = graph.graph_max
			self._values_zoom.value = graph._zoom * 100.0
			self._values_top.value  = graph._top

			self._loaded 					= True
			self._name.enabled          	= True
			self._min_value.enabled     	= True
			self._max_value.enabled     	= True
			self._values_zoom.enabled   	= True
			self._values_top.enabled    	= True
			self._remove_graph_btn.enabled 	= True
			self._current_selected_graph 	= graph

		del self._updating_properties
		


	def __save_graphs_changes(self):
		if hasattr(self, '_updating_properties'):  return

		if self._loaded and self._current_selected_graph is not None:
			graph = self._current_selected_graph

			#logger.debug('Before: Min: {0} | Max: {1} Zoom: {2}'.format(graph.graph_min, graph.graph_max,graph.zoom ) )

			graph.name = self._name.value; 
			graph.graph_min = self._min_value.value
			graph.graph_max = self._max_value.value

			graph.zoom     	= self._values_zoom.value / 100.0
			graph.top      	= self._values_top.value  

			logger.debug('Min: {0} | Max: {1} Zoom: {2}'.format(graph.graph_min, graph.graph_max,graph.zoom ) )

			self._timeline.repaint()

	@property
	def graphs(self):
		return self._timeline.graphs


	def mouse_moveover_timeline_event(self, event):
		graph = self.selected_graph
		if graph is not None: graph.mouse_move_evt(event, 0, self.height())
		
##################################################################################################################
##################################################################################################################
##################################################################################################################

# Execute the application
if __name__ == "__main__":
	import pyforms
	pyforms.start_app(GraphsProperties, geometry=(0, 0, 600, 400))
