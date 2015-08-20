import sys, glob, os
from PyQt4 import uic
from PyQt4 import QtGui, QtCore
import pyforms.Utils.tools as tools, time
import settings


from pyforms.web.BaseWidget import BaseWidget
from pyforms.web.Controls.ControlPlayer import ControlPlayer
from pyforms.web.Controls.ControlButton import ControlButton

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
			if hasattr(state, 'init'): 
				state.init()
			if hasattr(state, 'app') and state.app:
				state.app._controlsPrefix = stateName

		self._html = ''
		self._js = ''

		self._currentIteration = 0


	def initForm(self):
		image = os.path.join( settings.MEDIA_ROOT, 'statesmachines', '{0}.png'.format( self.__class__.__name__) )
		self.exportGraph(image)
				
		self._controls = []
		self._html = '<h3>Application workflow states</h3><br/>'
		
		# Load the applications
		for fromStateName, state in reversed( self.states.items() ):
			if hasattr(state, 'app') and state.app:
				# Add the instance of the application to the State machine node
				formset = state.app.formControls.keys() if state.app._formset==None else state.app._formset
				
				self._html += '<h4 class="statemachine-toggleButton" state="{0}" >{0} <small>({1})</small></h4>'.format(fromStateName, state.app.title)
				self._html += '<div id="statemachine-{0}-form" style="display:none;" >'.format( fromStateName )
				self._html += state.app.generatePanel(formset)
				self._html += '</div><hr/>'
				self._controls += state.app._controls
		
		self._html += '<br/><br/><h3>Application workflow diagram</h3>'
		self._html += '<img src="/load/{0}/statemachine/diagram/" >'.format(self.__class__.__name__)
		self._formLoaded = True
		
		self._js = "\n".join( self._controls )
		return {  'title': self._title }

	#def submit(self)
		

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

		self._currentIteration += 1



	def execute(self): 
		# Initiate the parameters set by the user
		self._currentState = self.returnCurrentStatesValues()

		# Iterate the states execution
		while not self.ended:  self.iterateStates()

	
	def loadSerializedForm(self, params):

		self._currentIteration = params.get('currentIteration', 0)

		for key, value in params.items():
			tmp = key.split('-')
			if len(tmp)>1: 
				stateName, controlName = tmp
				self.states[stateName].app.formControls[controlName].value = value
			elif key in self.formControls:
				control = self.formControls[key]
				control.value = value

		if 'event' in params.keys():
			tmp = params['event']['control'].split('-')
			if len(tmp)>1:
				stateName, controlName = tmp
				control = self.states[stateName].app.formControls[controlName]
				func = getattr(control, params['event']['event'])
				func()
			else:
				for key, item in self.formControls.items():
					if key==params['event']['control']:
						func = getattr(item, params['event']['event'])
						func()
		
	
	def serializeForm(self):
		res = {}
		for stateName, state in reversed( self.states.items() ):
			if hasattr(state, 'app') and state.app!=None:
				res.update( state.app.serializeForm() )

		for key, item in self.formControls.items():
			if isinstance(item, ControlPlayer ): 
				res[item._name] = item.value
				if item._value!=None and item._value!='': item._value.release() #release any open video
			elif isinstance(item, ControlButton ): 
				pass
			else:
				res[item._name] = item.value

		res['currentIteration'] = self._currentIteration
		return res

	def returnCurrentStatesValues(self):
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

	@property
	def currentIteration(self): return self._currentIteration








	


def startApp(states):
	app = QtGui.QApplication(sys.argv)
	container = Container(states)
	app.exec_()
