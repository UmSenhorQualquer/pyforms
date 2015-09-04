import sys, glob, os
from PyQt4 import uic
from PyQt4 import QtGui, QtCore
import pyforms.Utils.tools as tools, time
from pyforms.gui.BaseWidget import BaseWidget

from pyStateMachine.States.State import State, EndState
from pyStateMachine.StateMachineControllers.StatesController import StatesController


def gotoAppState(true=None, false=None, trueParms={}, falseParms={}):
	def go2decorator(func):
		def func_wrapper(self, inVar): return func(self, inVar)

		func_wrapper.trueParms 		= trueParms
		func_wrapper.falseParms 	= falseParms
		func_wrapper.go2StateTrue  	= true
		func_wrapper.go2StateFalse 	= false
		func_wrapper.label = func.__name__ if func.__doc__==None else '\n'.join([x for x in func.__doc__.replace('\t','').split('\n') if len(x)>0])
		return func_wrapper
	return go2decorator


class PyFormsState(State):

	def init(self): pass

	def enter(self, inVar, currentState={}): return inVar

	def leave(self, inVar, currentState={}): return inVar

	def execute(self): 
		if self.app!=None and hasattr(self.app, 'execute'): self.app.execute()

	@property
	def app(self): return self._app if hasattr(self, '_app') else None
	
	@app.setter
	def app(self, value): self._app = value


	def initForm(self):
		if hasattr(self, 'app') and self.app: self.app.initForm(); 

	@property
	def form(self): return self.app.form if self.app else None
	


class PyFormsStateMachine(StatesController, BaseWidget):

	def __init__(self, title):
		BaseWidget.__init__(self, title)
		StatesController.__init__(self, self.STATES)		
		for stateName, state in self.states.items():
			if hasattr(state, 'init'): state.init()
	
	


	def initForm(self):
		tabs = QtGui.QTabWidget(self)
		self.layout().addWidget(tabs)
		self.layout().setMargin(0)
		self.layout().setSpacing(0)
		
		# Generates and load the State machine graph
		self.exportGraph()
		self._image = QtGui.QLabel()
		self._image.setPixmap(QtGui.QPixmap('stateMachine.png'))	
		scrollArea = QtGui.QScrollArea();
 		scrollArea.setWidget(self._image);
 		tabs.addTab(scrollArea, 'State Machine Diagram')

		# Load the applications
		for fromStateName, state in reversed( self.states.items() ):
			if hasattr(state, 'app') and state.app:
				#Override the original application formset if the state has a new one
				state.initForm(); 
				# Add the application form to a new Tab
				tabs.addTab(state.form, fromStateName)
				
						

 		

	def iterateStates(self):
		"""
		Iterate states - each call go to another level
		"""
		if len(self._waitingStates)>0:
			statesOutputs = []
			print self._waitingStates

			#First run all the pending states
			for fromStateName, toStateName, inputParam in self._waitingStates:
				state 				= self._states[toStateName]
				copyOfCurrentState 	= dict(self._currentState)

				if isinstance(state, EndState): executionDetails = (toStateName, state, inputParam )
				else:
					p = state.enter(inputParam, copyOfCurrentState)
					state.execute()
					outParam = state.leave(p, copyOfCurrentState)
					executionDetails = (toStateName, state, outParam )
				
				statesOutputs.append( executionDetails )

			#Check the events of each exectuted state:
			for stateName, state, output in statesOutputs:
				#Remove the exectued state from the waiting queue
				self._waitingStates.pop(0) 
				#Check each event
				for e in state.events:
					#Select the next state to go
					go2State = e.go2StateTrue if e(state, output) else e.go2StateFalse
					#In case the state is None, it stops the state execution
					if go2State!=None:  self._waitingStates.append( [stateName, go2State, output] )
					else: 				self._waitingStates.append( [stateName, 'EndState', output] )

			"Save the currentState of the iteration"
			self._currentState = self.__returnCurrentStatesValues()
		else:
			print("State machine ended")



	def execute(self):
		# Initiate the parameters set by the user
		self._currentState = self.__returnCurrentStatesValues()

		# Iterate the states execution
		while not self.ended:  self.iterateStates()


	def __returnCurrentStatesValues(self):
		"""
		Iterate all the states and save the values of their controls
		"""
		currentState = {}
		for stateName, state in reversed( self.states.items() ):
			appState = {}
			#The state has an application associated to it
			if hasattr(state, 'app') and state.app:
				for controlName, control in state.app.formControls.items():
					appState[controlName] = control.value
			currentState[stateName] = appState
		return currentState








def startApp(states):
	app = QtGui.QApplication(sys.argv)
	container = Container(states)
	app.exec_()