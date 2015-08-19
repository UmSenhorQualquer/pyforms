import sys, glob, os
import pyforms.Utils.tools as tools, time
import argparse
from pyforms.terminal.BaseWidget import BaseWidget

from pyStateMachine.States.State import State,EndState
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

	def run(self, inVar, currentState={}):
		res = super(PyFormsState, self).run(inVar)
		if self.app: self.app.execute()
		return res

	@property
	def app(self): return self._app if hasattr(self, '_app') else None
	
	@app.setter
	def app(self, value): self._app = value

	def parseTerminalParameters(self):
		if hasattr(self, 'app') and self.app: self.app.parseTerminalParameters(); 

	def initForm(self):
		if hasattr(self, 'app') and self.app: self.app.initForm(parse=False); 

	@property
	def form(self): return self.app.form if self.app else None


class PyFormsStateMachine(StatesController, BaseWidget):

	_parser = argparse.ArgumentParser()
	

	def __init__(self, title):
		BaseWidget.__init__(self, title)
		StatesController.__init__(self, self.STATES)		
		
		for stateName, state in self.states.items():
			if hasattr(state, 'init'): state.init()
			

	def initForm(self):

		# Load the applications
		for fromStateName, state in reversed( self.states.items() ):
			if hasattr(state, 'app') and state.app:
				state.app._parser 			= self._parser
				state.app._controlsPrefix 	= fromStateName
				#Override the original application formset if the state has a new one
				state.initForm() 

 	
		self._parser.add_argument(
			"--exec", default='', 
			help='Function from the application that should be executed. Use | to separate a list of functions.')
		
		self._parser.add_argument(
			"--exportDiagramTo", default='', 
			help='File to where the diagram should export to.')
		
		self._args = self._parser.parse_args()

		if self._args.exportDiagramTo!='':  self.exportGraph(self._args.exportDiagramTo)
		
		
		for fromStateName, state in reversed( self.states.items() ):
			if hasattr(state, 'app') and state.app:
				state.app._args 	= self._args
				state.parseTerminalParameters()	

		for function in self._args.__dict__.get("exec", []).split('|'):
			if len(function)>0: getattr(self, function)()

 		
	def iterateStates(self):
		"""
		Iterate states - each call go to another level
		"""
		if len(self._waitingStates)>0:
			statesOutputs = []

			#First run all the pending states
			for fromStateName, toStateName, inputParam in self._waitingStates:
				state 				= self._states[toStateName]
				copyOfCurrentState 	= dict(self._currentState)

				if isinstance(state, EndState): executionDetails = (toStateName, state, state.run(inputParam ) )
				else: 							executionDetails = (toStateName, state, state.run(inputParam, copyOfCurrentState ) )
				
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