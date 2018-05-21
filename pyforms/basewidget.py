from confapp import conf


if conf.PYFORMS_MODE in ['GUI']:

    from pyforms_gui.basewidget import BaseWidget
    from pyforms_gui.organizers import vsplitter, hsplitter, segment, no_columns

elif conf.PYFORMS_MODE in ['TERMINAL']:

    from pyforms_terminal.basewidget import BaseWidget
    no_columns = tuple
    segment = list
    
elif conf.PYFORMS_MODE in ['WEB']:

    from pyforms_web.basewidget import BaseWidget
    from pyforms_web.organizers import no_columns, segment
    
    from pyforms_web.modeladmin import ModelAdmin
    from pyforms_web.modeladmin import ViewFormAdmin
    from pyforms_web.modeladmin import EditFormAdmin
