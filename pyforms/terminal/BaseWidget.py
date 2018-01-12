from pyforms.terminal.Controls.ControlFile import ControlFile
from pyforms.terminal.Controls.ControlSlider import ControlSlider
from pyforms.terminal.Controls.ControlText import ControlText
from pyforms.terminal.Controls.ControlCombo import ControlCombo
from pyforms.terminal.Controls.ControlCheckBox import ControlCheckBox
from pyforms.terminal.Controls.ControlBase import ControlBase
from pyforms.terminal.Controls.ControlDir import ControlDir
from pyforms.terminal.Controls.ControlNumber import ControlNumber
from datetime import datetime, timedelta
import argparse, uuid, os, shutil, time, sys, subprocess
import simplejson as json

try:
    import requests
except:
    print("No requests lib")


class BaseWidget(object):

    def __init__(self, *args, **kwargs):
        self._parser = argparse.ArgumentParser()
        self._controlsPrefix    = ''
        self._title             = kwargs.get('title', args[0] if len(args)>0 else '')
        self.stop               = False

        self._conf = kwargs.get('load', None)

    ############################################################################
    ############ Module functions  #############################################
    ############################################################################

    def init_form(self, parse=True):
        result = {}
        for fieldname, var in self.controls.items():
            name = var._name
            if isinstance(var, (
                    ControlFile, ControlSlider,   ControlText, 
                    ControlCombo,ControlCheckBox, ControlDir, ControlNumber
                ) 
            ):
                self._parser.add_argument("--%s" % name, help=var.label)

        if parse:
            self._parser.add_argument('terminal_mode', type=str, default='terminal_mode', help='Flag to run pyforms in terminal mode')
            self._parser.add_argument(
                "--exec{0}".format(self._controlsPrefix), 
                default='', 
                help='Function from the application that should be executed. Use | to separate a list of functions.')
            self._parser.add_argument(
                "--load{0}".format(self._controlsPrefix), 
                default=None, 
                help='Load a json file containing the pyforms form configuration.')
            self._args = self._parser.parse_args()

            self.__parse_terminal_parameters()
            self.__execute_events()

    def load_form(self, data, path=None):
        allparams = self.controls

        if hasattr(self, 'load_order'):
            for name in self.load_order:
                param = allparams[name]
                if name in data:
                    param.load_form(data[name])
        else:
            for name, param in allparams.items():
                if name in data:
                    param.load_form(data[name])


    def __parse_terminal_parameters(self):
        for fieldname, var in self.controls.items():
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
                elif isinstance(var, (ControlSlider, ControlNumber) ):
                    var.value = int(self._args.__dict__[name])

        if self._args.load:
            print('\n--------- LOADING CONFIG ------------------')
            with open(self._args.load) as infile:
                data = json.load(infile)
                self.load_form(data, os.path.dirname(self._args.load))
            print('--------- END LOADING CONFIG --------------\n')
        elif self._conf is not None:
            print('\n--------- LOADING DEFAULT CONFIG ------------------')
            self.load_form(self._conf, '.')
            print('--------- END LOADING DEFAULT CONFIG --------------\n')

            
            
    def __execute_events(self):
        for function in self._args.__dict__.get("exec{0}".format(self._controlsPrefix), []).split('|'):
            if len(function)>0: 
                getattr(self, function)()

        res = {}
        for controlName, control in self.controls.items(): 
            res[controlName] = {'value': control.value }
        with open('out-parameters.txt', 'w') as outfile:
            outfile.write( str(res) )


    def __downloadFile(self, url, outFilepath):
        chunksize = 512*1024
        r = requests.get(url, stream=True)
        with open(outFilepath, 'w') as f:
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
    def controls(self):
        """
        Return all the form controls from the the module
        """
        result = {}
        for name, var in vars(self).items():
            if isinstance(var, ControlBase):
                var._name = self._controlsPrefix+"-"+name if len(self._controlsPrefix)>0 else name
                result[name] = var
        return result