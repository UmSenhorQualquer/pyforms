import csv, time, datetime, decimal
from pyforms import BaseWidget
from pyforms.Controls import ControlProgress
from pyforms.Controls import ControlButton
from pyforms.Controls import ControlList
from pyforms.Controls import ControlNumber
from pyforms.Controls import ControlSlider
from pyforms.Controls import ControlText

class GraphsProperties(BaseWidget):

	def __init__(self, timelineWidget=None, parentWindow=None):
		super(GraphsProperties, self).__init__('Graphs properties', parentWindow=parentWindow)
		self.setContentsMargins(10, 10, 10, 10)
		self._timeline = timelineWidget

		# Definition of the forms fields
		self._graphs_list = ControlList('Graphs list')
		self._name        = ControlText('Name')
		self._min_value   = ControlNumber('Min')
		self._max_value   = ControlNumber('Max')
		self._values_zoom = ControlSlider('Amplitude', 100, 60, 400)
		self._values_top  = ControlNumber('Top position', 0, -1000, 1000)
		self._remove_graph_btn = ControlButton('Remove graph')

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
					' '
				]),
			]

		self._graphs_list.itemSelectionChanged = self.__graphs_list_selection_changed

		self._loaded = False

		self._name.changed          = self.__save_graphs_changes
		self._min_value.changed     = self.__save_graphs_changes
		self._max_value.changed     = self.__save_graphs_changes
		self._values_zoom.changed   = self.__save_graphs_changes
		self._values_top.changed    = self.__save_graphs_changes

	def show(self):
		super(GraphsProperties, self).show()
		self._loaded = False

		self._graphs_list.clear()            
		for graph in self._timeline._charts:
			self._graphs_list += [graph.name]

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

	def __save_graphs_changes(self):
		index = self._graphs_list.mouseSelectedRowIndex
			
		if self._loaded and index is not None:
			graph = self._timeline._charts[index]

			graph.name      = self._name.value; self._graphs_list.setValue(0, index, self._name.value)
			graph._graphMin = self._min_value.value   
			graph._graphMax = self._max_value.value   
			graph._zoom     = self._values_zoom.value / 100.0
			graph._top      = self._values_top.value  

			self._timeline.repaint()


##################################################################################################################
##################################################################################################################
##################################################################################################################

# Execute the application
if __name__ == "__main__":
	import pyforms
	pyforms.startApp(GraphsProperties, geometry=(0, 0, 600, 400))
