# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
from AnyQt.QtGui import QIcon, QPixmap
from AnyQt.QtWidgets import QStyle, qApp


def path(filename):
	"""	
	:param filename: 
	:return: 
	"""
	return os.path.join(os.path.dirname(__file__), filename)


PYFORMS_ICON_VIDEOPLAYER_PAUSE_PLAY = QIcon()
PYFORMS_ICON_VIDEOPLAYER_PAUSE_PLAY.addPixmap(qApp.style().standardPixmap(QStyle.SP_MediaPlay), mode=QIcon.Normal,
                                              state=QIcon.Off)
PYFORMS_ICON_VIDEOPLAYER_PAUSE_PLAY.addPixmap(qApp.style().standardPixmap(QStyle.SP_MediaPause), mode=QIcon.Normal,
                                              state=QIcon.On)

PYFORMS_ICON_CODEEDITOR_SAVE = QIcon(qApp.style().standardPixmap(QStyle.SP_DialogSaveButton))
PYFORMS_ICON_CODEEDITOR_DISCART = QIcon(qApp.style().standardPixmap(QStyle.SP_DialogDiscardButton))

PYFORMS_PIXMAP_EVENTTIMELINE_ZOOM_IN = QPixmap(path(os.path.join("Controls", "uipics", "zoom_in.png")))
PYFORMS_PIXMAP_EVENTTIMELINE_ZOOM_OUT = QPixmap(path(os.path.join("Controls", "uipics", "zoom_in.png")))

PYFORMS_ICON_EVENTTIMELINE_IMPORT = QIcon(path(os.path.join("Controls", "uipics", "page_white_get.png")))
PYFORMS_ICON_EVENTTIMELINE_EXPORT = QIcon(path(os.path.join("Controls", "uipics", "page_white_put.png")))
PYFORMS_ICON_EVENTTIMELINE_GRAPH = QIcon(path(os.path.join("Controls", "uipics", "graph.png")))
PYFORMS_ICON_EVENTTIMELINE_TIMELINE = QIcon(path(os.path.join("Controls", "uipics", "timeline.png")))
PYFORMS_ICON_EVENTTIMELINE_REFRESH = QIcon(path(os.path.join("Controls", "uipics", "refresh.png")))
PYFORMS_ICON_EVENTTIMELINE_ADD = QIcon(path(os.path.join("Controls", "uipics", "add.png")))
PYFORMS_ICON_EVENTTIMELINE_REMOVE = QIcon(path(os.path.join("Controls", "uipics", "remove.png")))

PYFORMS_ICON_FILE_OPEN = QIcon()

PYFORMS_MAINWINDOW_MARGIN = 7
