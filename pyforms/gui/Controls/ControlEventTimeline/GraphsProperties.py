import csv, time, datetime, decimal, logging, sys
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

	def __init__(self, timelineWidget=None, parentWindow=None):
		super(GraphsProperties, self).__init__('Graphs properties', parentWindow=parentWindow)
		self.setContentsMargins(10, 10, 10, 10)
		self._timeline = timelineWidget

		# Definition of the forms fields
		self._graphs_list = ControlList('Datasets')
		self._name        = ControlText('Name')
		self._min_value   = ControlNumber('Min', 0, -sys.float_info.max, sys.float_info.max)
		self._max_value   = ControlNumber('Max', 0, -sys.float_info.max, sys.float_info.max)
		self._values_zoom = ControlSlider('Amplitude', 100, 60, 400)
		self._values_top  = ControlNumber('Bottom', 0, -1000, 1000)
		self._remove_graph_btn = ControlButton('Remove graph')
		self._value 	  = ControlLabel()

		self._formset = [
			(
				['_graphs_list','_remove_graph_btn'],
				'||', 
				[
					' ',
					'_name',
					('_min_value', '_max_value'),
					('_values_top',' '),
					'_values_zoom',
					'info:Choose one dataset and move the mouse over the graph line to visualize the coordenates.',
					'_value'
				]),
			]

		self._graphs_list.itemSelectionChanged = self.__graphs_list_selection_changed

		self._loaded = False

		self._name.changed          = self.__save_graphs_changes
		self._min_value.changed     = self.__save_graphs_changes
		self._max_value.changed     = self.__save_graphs_changes
		self._values_zoom.changed   = self.__save_graphs_changes
		self._values_top.changed    = self.__save_graphs_changes

		self._name.enabled          = False
		self._min_value.enabled     = False
		self._max_value.enabled     = False
		self._values_zoom.enabled   = False
		self._values_top.enabled    = False
		self._remove_graph_btn.enabled = False

		self._remove_graph_btn.value = self.__remove_chart

	@property
	def selected_chart(self):
		index = self._graphs_list.mouseSelectedRowIndex
		return self._timeline._charts[0] if (index is not None) else None
	
	@property
	def coordenate_text(self): return self._value
	@coordenate_text.setter
	def coordenate_text(self, value): self._value.value = str(value) if value else ''
	


	def show(self):
		super(GraphsProperties, self).show()
		self._loaded = False

		self._graphs_list.clear()            
		for graph in self._timeline._charts:
			self._graphs_list += [graph.name]

	def __remove_chart(self):
		index = self._graphs_list.mouseSelectedRowIndex
		if index is not None:
			self._graphs_list -= -1
			self._timeline._charts.pop(index)
			self._timeline.repaint()


	def __graphs_list_selection_changed(self):        
		index = self._graphs_list.mouseSelectedRowIndex
		if index is not None:
			graph = self._timeline._charts[index]

			exponent_min = abs(decimal.Decimal(graph._graphMin).as_tuple().exponent)
			exponent_max = abs(decimal.Decimal(graph._graphMax).as_tuple().exponent)
			exponent_min = 4 if exponent_min>4 else exponent_min
			exponent_max = 4 if exponent_min>4 else exponent_min

			self._name.value            = graph.name
			self._min_value.decimals    = exponent_min
			self._min_value.value       = graph._graphMin
			self._max_value.decimals    = exponent_max
			
			self._max_value.value   = graph._graphMax
			self._values_zoom.value = graph._zoom * 100.0
			self._values_top.value  = graph._top

			self._loaded = True

			self._name.enabled          = True
			self._min_value.enabled     = True
			self._max_value.enabled     = True
			self._values_zoom.enabled   = True
			self._values_top.enabled    = True
			self._remove_graph_btn.enabled = True
		else:
			self._name.enabled          = False
			self._min_value.enabled     = False
			self._max_value.enabled     = False
			self._values_zoom.enabled   = False
			self._values_top.enabled    = False
			self._remove_graph_btn.enabled = False


	def __save_graphs_changes(self):
		index = self._graphs_list.mouseSelectedRowIndex
			
		if self._loaded and index is not None:
			graph = self._timeline._charts[index]

			logger.debug('Before: Min: {0} | Max: {1} Zoom: {2}'.format(graph.graph_min, graph.graph_max,graph.zoom ) )


			graph.name = self._name.value; 
			data = self._graphs_list.value
			data[index]= [self._name.value]
			self._graphs_list.value = data
			graph.graph_min = self._min_value.value
			graph.graph_max = self._max_value.value

			graph.zoom     	= self._values_zoom.value / 100.0
			graph.top      	= self._values_top.value  

			logger.debug('Min: {0} | Max: {1} Zoom: {2}'.format(graph.graph_min, graph.graph_max,graph.zoom ) )

			self._timeline.repaint()

	@property
	def charts(self):
		return self._timeline._charts


##################################################################################################################
##################################################################################################################
##################################################################################################################

# Execute the application
if __name__ == "__main__":
	import pyforms
	pyforms.startApp(GraphsProperties, geometry=(0, 0, 600, 400))
