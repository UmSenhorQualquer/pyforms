from pyforms.Controls import ControlFile, ControlSlider, ControlText, ControlCombo, ControlCheckBox, ControlBase, ControlDir
from datetime import datetime, timedelta
import argparse, uuid, os, shutil, time, sys, subprocess

try:
	import requests
except:
	print("No requests lib")


class BaseWidget(object):

	
	
	def __init__(self, title):
		self._parser = argparse.ArgumentParser()
		f = open('pid.txt', 'w')
		f.write(str(os.getpid()))
		f.close()
		
		self._controlsPrefix 	= ''
		self._title 			= title
		self.stop 				= False

	############################################################################
	############ Module functions  #############################################
	############################################################################

	def init_form(self, parse=True):
		result = {}
		for fieldname, var in self.formControls.items():
			name = var._name
			if isinstance(var, (ControlFile,ControlSlider,ControlText, ControlCombo,ControlCheckBox, ControlDir) ):
				self._parser.add_argument("--%s" % name, help=var.label)

		if parse:
			
			self._parser.add_argument(
				"--exec{0}".format(self._controlsPrefix), 
				default='', 
				help='Function from the application that should be executed. Use | to separate a list of functions.')
			self._args = self._parser.parse_args()

			self.parseTerminalParameters()
			self.executeEvents()


	def parseTerminalParameters(self):
		for fieldname, var in self.formControls.items():
			name = var._name
			if self._args.__dict__.get(name, None):

				if isinstance(var, ControlFile):
					value = self._args.__dict__[name]
					if value!=None and (value.startswith('http://') or value.startswith('https://')):
						local_filename = value.split('/')[-1]
						outputFileName = os.path.join('input', local_filename)
						self.__downloadFile(value, outputFileName)
						var.value = outputFileName
					else:
						var.value = value

				if isinstance(var, ControlDir):
					value = self._args.__dict__[name]
					var.value = value

				elif isinstance(var,  (ControlText, ControlCombo)):
					var.value = self._args.__dict__[name]
				elif isinstance(var, ControlCheckBox):
					var.value = self._args.__dict__[name]=='True'
				elif isinstance(var, ControlSlider):
					var.value = int(self._args.__dict__[name])

			
			
	def executeEvents(self):
		for function in self._args.__dict__.get("exec{0}".format(self._controlsPrefix), []).split('|'):
			if len(function)>0: getattr(self, function)()

		res = {}
		for controlName, control in self.formControls.items(): res[controlName] = {'value': control.value }
		outfile = open('out-parameters.txt', 'wb')
		outfile.write( str(res) )
		outfile.close()


	def __downloadFile(self, url, outFilepath):
		chunksize = 512*1024
		r = requests.get(url, stream=True)
		with open(outFilepath, 'wb') as f:
			for chunk in r.iter_content(chunk_size=chunksize): 
				if chunk: f.write(chunk); f.flush(); 
		


	def execute(self): pass


	def start_progress(self, total = 100):
		self._total_processing_count = total
		self._processing_initial_time = time.time()
		self._processing_count  = 1

	def update_progress(self):
		div = int(self._total_processing_count/400)
		if div==0: div = 1
		if (self._processing_count % div )==0:
			self._processing_last_time = time.time()  
			total_passed_time = self._processing_last_time - self._processing_initial_time
			remaining_time = ( (self._total_processing_count * total_passed_time) / self._processing_count ) - total_passed_time
			if remaining_time<0: remaining_time = 0
			time_remaining = datetime(1,1,1) + timedelta(seconds=remaining_time )
			time_elapsed = datetime(1,1,1) + timedelta(seconds=(total_passed_time) )

			values = ( 
						time_elapsed.day-1,  time_elapsed.hour, time_elapsed.minute, time_elapsed.second, 
						time_remaining.day-1, time_remaining.hour, time_remaining.minute, time_remaining.second, 
						(float(self._processing_count)/float(self._total_processing_count))*100.0, self._processing_count, self._total_processing_count, 
					)

			print("Elapsed: %d:%d:%d:%d; Remaining: %d:%d:%d:%d; Processed %0.2f %%  (%d/%d); |   \r" % values) 
			sys.stdout.flush()

		self._processing_count  += 1

	def end_progress(self):
		self._processing_count = self._total_processing_count
		self.update_progress()



	def __savePID(self, pid):
		try:
			with open('pending_PID.txt', 'w') as f:
				f.write(str(pid))
				f.write('\n')
		except (IOError) as e:
			raise e

	def __savePID(self, pid):
		try:
			with open('pending_PID.txt', 'w') as f:
				f.write(str(pid))
				f.write('\n')
		except (IOError) as e:
			raise e


	def executeCommand(self, cmd, cwd=None, env=None):
		if cwd!=None: 
			currentdirectory = os.getcwd()
			os.chdir(cwd)
		
		print(" ".join(cmd))
		proc = subprocess.Popen(cmd)

		if cwd!=None: os.chdir(currentdirectory)
		self.__savePID(proc.pid)
		proc.wait()
		#(output, error) = proc.communicate()
		#if error: print 'error: ', error
		#print 'output: ', output
		return ''#output

	def exec_terminal_cmd(self, args, **kwargs):
		print('TERMINAL <<',' '.join(args) )
		sys.stdout.flush()
		proc = subprocess.Popen(args, **kwargs)
		self.__savePID(proc.pid)
		proc.wait()
		sys.stdout.flush()
		

	@property
	def formControls(self):
		"""
		Return all the form controls from the the module
		"""
		result = {}
		for name, var in vars(self).items():
			if isinstance(var, ControlBase):
				var._name = self._controlsPrefix+"-"+name if len(self._controlsPrefix)>0 else name
				result[name] = var
		return result