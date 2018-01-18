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
import traceback
import time
import datetime

from pysettings import conf

if conf.PYFORMS_USE_QT5:
    from PyQt5.QtWidgets import QMessageBox
else:
    from PyQt4.QtGui import QMessageBox



class GraphsEventsGenerator(BaseWidget):

    def __init__(self, timeline=None):
        super(GraphsEventsGenerator, self).__init__('Apply a function to the graph values', parent_win=timeline)
        self.setContentsMargins(10, 10, 10, 10)
        self._timeline = timeline


        # Definition of the forms fields
        self._graphs_list = ControlList('Graphs list (try double click)', readonly=False, select_entire_row=True)
        self._equation    = ControlTextArea('Equation')
        self._graphname   = ControlText('Graph name')
        self._genevts_btn = ControlButton('Generate graph')

        
        self._formset = [
            (
                ['_graphs_list'],
                '||', 
                [
                    '_graphname',
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

    def show(self):
        super(GraphsEventsGenerator, self).show()

        if len(self._graphname.value.strip())==0:
            self._graphname.value = "generated-graph-{0}".format( len(self._timeline.graphs)) 



    def __cell_double_clicked_evt(self, row, column):
        if len(self._equation.value.strip())==0:
            self._equation.value += '[{0}]'.format( self._graphs_list.value[row][column] )
        else:
            self._equation.value += ' and [{0}]'.format( self._graphs_list.value[row][column] )


    def __generage_events_evt(self):
        if len(self._graphname.value.strip())==0: 
            QMessageBox.warning(
                self, "Attention!", 'The graph name cannot be empty')
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
        data   = []
        try:
            for i in range(max_frame):

                try:
                    value = eval(equation)
                except:
                    value = None

                data.append( (i, value) )
            self._timeline.add_chart(self._graphname.value, data)

            self._graphname.value = "generated-graph-{0}".format( len(self._timeline.graphs)) 
        except Exception as e:
            traceback.print_exc()
            QMessageBox.warning( self, "Error!", str(e) )

    
##################################################################################################################
##################################################################################################################
##################################################################################################################

# Execute the application
if __name__ == "__main__":
    import pyforms
    pyforms.start_app(GraphsEventsGenerator, geometry=(0, 0, 600, 400))
