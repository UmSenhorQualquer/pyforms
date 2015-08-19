import sys, glob, os
from PyQt4 import uic
from PyQt4 import QtGui, QtCore
import pyforms.Utils.tools as tools, time
import settings


from pyforms.web.BaseWidget import BaseWidget
from pyforms.web.Controls.ControlPlayer import ControlPlayer
from pyforms.web.Controls.ControlButton import ControlButton

from pyStateMachine.States.State import State
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

	def run(self, inVar):
		if hasattr(self,'_application'): self._application.execute()
		return super(PyFormsState, self).run(inVar)

		

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

				
		

	def iterateStates(self):
		"""
		Iterate states - each call go to another level
		"""
		if len(self._waitingStates)>0:
			statesOutputs = []

			for fromStateName, toStateName, inputParam in self._waitingStates:
				state = self._states[toStateName]
				if hasattr(state,'APP_CLASS'):
					state._application = state.APP_CLASS(); state._application.initForm()

					# Initiante the application with the default values set by the user
					for controlName, controlValue in self._initalParms[toStateName].items():
						getattr(state._application, controlName).value = controlValue

					if toStateName in self._paramsFlow:
						for inParm, outParam in self._paramsFlow[toStateName][fromStateName].items():
							state._application.formControls[inParm].value = self._appsOutParams[outParam]
					else:
						print "no params found for", toStateName


			#First run all the pending states
			for fromStateName, toStateName, inputParam in self._waitingStates:
				state = self._states[toStateName]
				statesOutputs.append( (toStateName ,state, state.run(inputParam) ) )



			#Check the events of each exectuted state:
			for stateName, state, output in statesOutputs:

				if hasattr(state,'_application'):
					for controlName, control in state._application.formControls.items():
						self._appsOutParams['{0}.{1}'.format(stateName, controlName)] = control.value

				#Remove the exectued state from the waiting queue
				self._waitingStates.pop(0) 

				#Check each event
				for e in state.events:
					#Select the next state to go
					go2State = e.go2StateTrue if e(state, output) else e.go2StateFalse

					
					#In case the state is None, it stops the state execution
					if go2State!=None: 
						self._waitingStates.append( [stateName, go2State, output] )
					else:
						self._waitingStates.append( [stateName, 'EndState', output] )

		else:
			print "State machine ended"



	def execute(self): 

		apps 	 	   		= {}
		inParams 	   		= {}


		# Load the applications
		for fromStateName, state in reversed( self.states.items() ):
			if hasattr(state,'APP_CLASS'):
				
				for e in state.events:
					for paramIn, paramOut in e.trueParms.items():
						#For each event define the flow of parameters

						if e.go2StateTrue not in self._paramsFlow:  
							self._paramsFlow[e.go2StateTrue] = {}
						if paramIn 		  not in self._paramsFlow[e.go2StateTrue]:  
							self._paramsFlow[e.go2StateTrue][fromStateName] = {}

						paramState, stateParam = paramIn.split('.')
						self._paramsFlow[e.go2StateTrue][fromStateName][stateParam] = paramOut
						

		self._appsOutParams = {}

		
		# Save the parameters set by the user
		for stateName, state in reversed( self.states.items() ):
			if hasattr(state, '_application'):
				self._initalParms[stateName] = {}
				for controlName, control in state._application.formControls.items():
					self._initalParms[stateName][controlName] = control.value
			

		while not self.ended:  self.iterateStates()

	
	def loadSerializedForm(self, params):
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

		return res


	def eventExtraComment(self, e, result):
		if result:
			if len(e.trueParms)>0: 
				res = ""
				for inparam, outparam in e.trueParms.items():
					inStateName, inParamName = inparam.split('.')
					outStateName, outParamName = outparam.split('.')

					inParamName = self.states[inStateName]._application.formControls[inParamName].label
					outParamName = self.states[outStateName]._application.formControls[outParamName].label
					res += '{0}::{1}={2}::{3}\n'.format(inStateName, inParamName, outStateName, outParamName)
				return res
			else:
				return None
		else:
			if len(e.falseParms)>0:
				for inparam, outparm in e.falseParms.items():
					inParamName = self.states[inStateName]._application.formControls[inParamName].label
					outParamName = self.states[outStateName]._application.formControls[outParamName].label
					res += '{0}::{1}={2}::{3}\n'.format(inStateName, inParamName, outStateName, outParamName)
				return res
			else:
				return None








	


def startApp(states):
	app = QtGui.QApplication(sys.argv)
	container = Container(states)
	app.exec_()
