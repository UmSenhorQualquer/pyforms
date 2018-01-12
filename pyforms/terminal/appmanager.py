from pyforms import BaseWidget

def start_app(AppClass, **kwargs):
    app = AppClass(**kwargs.get('app_args', {}))
    app.init_form()
