# Settings

Pyforms is using the pysettings library to manage it settings.
Here it is described some of the settings of the library.


#### PYFORMS_MODE = os.environ.get('PYFORMS_MODE', 'GUI')

It defines the mode that the pyforms should run. Currently pyforms can run as **GUI** or **TERMINAL** mode.

#### PYFORMS_LOG_HANDLER_FILE_LEVEL = logging.DEBUG

Logging level.

#### PYFORMS_LOG_HANDLER_CONSOLE_LEVEL = logging.INFO

Logging level.

## GUI layout

#### PYFORMS_STYLESHEET = None

Path to the stylesheet file of the application.

#### PYFORMS_STYLESHEET_DARWIN = None
#### PYFORMS_STYLESHEET_LINUX = None
#### PYFORMS_STYLESHEET_WINDOWS = None

Frequently it is necessary to adapt the layout of an application for each operating system. These variables allow you to do just that.  
For each operating system you can define a stylesheet that will complement the default stylesheet for a specific OS.



## Controls

#### PYFORMS_CONTROL_CODE_EDITOR_DEFAULT_FONT_SIZE = '12'
#### PYFORMS_CONTROL_EVENTS_GRAPH_DEFAULT_SCALE = 1
#### PYFORMS_CONTROLPLAYER_FONT = 9


