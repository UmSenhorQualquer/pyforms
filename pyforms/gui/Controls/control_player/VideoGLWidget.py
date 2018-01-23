#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.controls.ControlPlayer.VideoGLWidget

"""

from pyforms.gui.controls.ControlPlayer.AbstractGLWidget import AbstractGLWidget
from AnyQt.QtOpenGL import QGLWidget

class VideoGLWidget(AbstractGLWidget, QGLWidget): pass