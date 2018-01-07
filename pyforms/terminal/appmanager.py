from pyforms import BaseWidget

def start_app(AppClass, **kwargs):	
	app = AppClass(**kwargs)
	app.init_form()
