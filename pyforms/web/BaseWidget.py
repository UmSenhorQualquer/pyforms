
from pyforms.web.Controls.ControlBase import ControlBase
from pyforms.web.Controls.ControlFile import ControlFile
from pyforms.web.Controls.ControlSlider import ControlSlider
from pyforms.web.Controls.ControlText import ControlText
from pyforms.web.Controls.ControlCheckBox import ControlCheckBox
from pyforms.web.Controls.ControlPlayer import ControlPlayer
from pyforms.web.Controls.ControlButton import ControlButton
import uuid, os, shutil

class BaseWidget(object):

    _formset   = None
    _splitters = None

    def __init__(self, title):
        self._splitters     = []
        self._title         = title
        self._formLoaded    = False
        self._controls      = []
        self._controlsPrefix = ''
        self._html          = ''
        self._js            = ''

    ############################################################################
    ############ Module functions  #############################################
    ############################################################################

    def initForm(self):
        """
        Generate the module Form
        """
        self._html = ''
        self._js = ''
        if self._formset != None: 
            self._html += self.generatePanel(self._formset)
            self._js = "\n".join( self._controls )
        self._formLoaded = True
        return { 'code': self._html, 'controls_js': self._js, 'title': self._title }

        

    def generateTabs(self, formsetDict):
        """
        Generate QTabWidget for the module form
        @param formset: Tab form configuration
        @type formset: dict
        """
        tabs_head = ""
        tabs_body = ""
        tab_id = uuid.uuid4()

        for index, (key, item) in enumerate( sorted(formsetDict.items()) ):
            tabs_body += "<div id='%s-tab%d' >%s</div>\n" % (tab_id, index, self.generatePanel(item))
            tabs_head += "<li><a href='#%s-tab%d' >%s</a></li>\n" % (tab_id, index, key[key.find(':')+1:])
        return """<div id='%s' class='application-tabs' ><ul>%s</ul> %s</div>""" % (tab_id, tabs_head, tabs_body)



    def generatePanel(self, formset):
        """
        Generate a panel for the module form with all the controls
        formset format example: [('_video', '_arenas', '_run'), {"Player":['_threshold', "_player", "=", "_results", "_query"], "Background image":[(' ', '_selectBackground', '_paintBackground'), '_image']}, "_progress"]
        tuple: will display the controls in the same horizontal line
        list: will display the controls in the same vertical line
        dict: will display the controls in a tab widget
        '||': will plit the controls in a horizontal line
        '=': will plit the controls in a vertical line
        @param formset: Form configuration
        @type formset: list
        """
        control = ""
        if '=' in formset:
            tmp = list( formset )
            index = tmp.index('=')
            firstPanel = self.generatePanel(formset[0:index])
            secondPanel = self.generatePanel(formset[index+1:])
            splitter_id =uuid.uuid4()
            self._splitters.append( splitter_id )
            control = ("<div id='%s' class='horizontalSplitter' ><div>" + firstPanel + "</div><div>" + secondPanel + "</div></div>") % ( splitter_id, )
            return control
        elif '||' in formset:
            tmp = list( formset )
            index = tmp.index('||')
            firstPanel = self.generatePanel(formset[0:index])
            secondPanel = self.generatePanel(formset[index+1:])
            splitter_id = uuid.uuid4()
            self._splitters.append( splitter_id )
            control = ("<div id='%s' class='verticalSplitter' ><div>" + firstPanel + "</div><div>" + secondPanel + "</div></div>") % ( splitter_id, )
            return control
        
        layout = ""
        if type(formset) is tuple:
            for row in formset:
                if isinstance(row, (list, tuple)):
                    panel = self.generatePanel( row )
                    layout += "<div class='rows' >%s</div>" % panel
                elif row == " ":
                    layout += "<div class='space' ></div>"
                elif type(row) is dict:
                    tabs = self.generateTabs(row)
                    layout += tabs
                else:
                    control = self.formControls.get(row, None)
                    if control==None:
                        if row.startswith('info:'): layout += "<pre class='info' >%s</pre>" % row[5:]
                        elif row.startswith('h1:'): layout += "<h1>%s</h1>" % row[3:]
                        elif row.startswith('h2:'): layout += "<h2>%s</h2>" % row[3:]
                        elif row.startswith('h3:'): layout += "<h3>%s</h3>" % row[3:]
                        elif row.startswith('h4:'): layout += "<h4>%s</h4>" % row[3:]
                        elif row.startswith('h5:'): layout += "<h5>%s</h5>" % row[3:]
                        else: layout += "<span class='info' >%s</span>" % row
                    else:
                        self._controls.append( control.initControl() )
                        layout += "<div class='control' >%s</div>" % control
        elif type(formset) is list:
            for row in formset:
                if isinstance(row, (list, tuple)):
                    panel = self.generatePanel( row )
                    layout += "<div class='columns' >%s</div>" % panel
                elif row == " ":
                    layout += "<div class='space' ></div>"
                elif type(row) is dict:
                    tabs = self.generateTabs(row)
                    layout += tabs
                else:
                    control = self.formControls.get(row, None)
                    if control==None:
                        if row.startswith('info:'): layout += "<pre class='info' >%s</pre>" % row[5:]
                        elif row.startswith('h1:'): layout += "<h1>%s</h1>" % row[3:]
                        elif row.startswith('h2:'): layout += "<h2>%s</h2>" % row[3:]
                        elif row.startswith('h3:'): layout += "<h3>%s</h3>" % row[3:]
                        elif row.startswith('h4:'): layout += "<h4>%s</h4>" % row[3:]
                        elif row.startswith('h5:'): layout += "<h5>%s</h5>" % row[3:]
                        else: layout += "<span class='info' >%s</span>" % row
                    else:
                        self._controls.append( control.initControl() )
                        layout += "<div class='control' >%s</div>" % control
        
        return layout

    def findParameterByLabel(self, label):
        for a in self.formControls.values():
            if a._label == label: return a._name 
        return None


    def loadSerializedForm(self, params):
        for key, value in params.items():
            control = self.formControls.get(key, None)
            if control!=None:control.value = value

        if 'event' in params.keys():
            for key, item in self.formControls.items():
                if key==params['event']['control']:
                    func = getattr(item, params['event']['event'])
                    func()
                    

    def serializeForm(self):
        res = {}
        for key, item in self.formControls.items():
            if isinstance(item, ControlPlayer ): 
                res[item._name] = item.value
                if item._value!=None and item._value!='': item._value.release() #release any open video
            elif isinstance(item, ControlButton ): 
                pass
            else:
                res[item._name] = item.value

        return res

    ############################################################################
    ############ Parent class functions reemplementation #######################
    ############################################################################

    def show(self): pass

    ############################################################################
    ############ Properties ####################################################
    ############################################################################
    
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

    def start_progress(self, total = 100): pass

    def update_progress(self): pass

    def end_progress(self): pass


    #### Variable connected to the Storage manager of the corrent user
    @property
    def storage(self): return self._storage

    @storage.setter
    def storage(self, value): 
        self._storage = value
        for control in self.formControls.values(): control.storage = value
    #######################################################

    #### This variable has the current http request #######
    @property
    def httpRequest(self): return self._httpRequest

    @httpRequest.setter
    def httpRequest(self, value): 
        from opencsp import AVAILABLE_STORAGES
        self.storage = AVAILABLE_STORAGES.get(value.user)
        self._httpRequest = value
        for control in self.formControls.values(): control.httpRequest = value
    #######################################################

    
    @property
    def form(self): return self._html

    @property
    def js(self): return self._js
    

    @property
    def title(self): return self._title

    @title.setter
    def title(self, value): self._title = value
