#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.Controls.ControlPlayer.VideoGLWidget

"""

from pyforms.gui.Controls.ControlPlayer.AbstractGLWidget import AbstractGLWidget


from pysettings import conf

if conf.PYFORMS_USE_QT5:
    from PyQt5.QtOpenGL import QGLWidget
else:
    from PyQt4.QtOpenGL import QGLWidget

class VideoGLWidget(AbstractGLWidget, QGLWidget): pass