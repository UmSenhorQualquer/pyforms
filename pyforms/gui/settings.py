import os
from PyQt4 import QtGui

def path(filename): return os.path.join(os.path.dirname(__file__),filename)

PYFORMS_ICON_VIDEOPLAYER_PAUSE_PLAY = QtGui.QIcon()
PYFORMS_ICON_VIDEOPLAYER_PAUSE_PLAY.addPixmap(QtGui.qApp.style().standardPixmap(QtGui.QStyle.SP_MediaPlay), mode=QtGui.QIcon.Normal, state=QtGui.QIcon.Off)
PYFORMS_ICON_VIDEOPLAYER_PAUSE_PLAY.addPixmap(QtGui.qApp.style().standardPixmap(QtGui.QStyle.SP_MediaPause),mode=QtGui.QIcon.Normal, state=QtGui.QIcon.On)

PYFORMS_ICON_CODEEDITOR_SAVE = QtGui.QIcon(QtGui.qApp.style().standardPixmap(QtGui.QStyle.SP_DialogSaveButton))

PYFORMS_PIXMAP_EVENTTIMELINE_ZOOM_IN  = QtGui.QPixmap(path(os.path.join("Controls", "uipics", "zoom_in.png")))
PYFORMS_PIXMAP_EVENTTIMELINE_ZOOM_OUT = QtGui.QPixmap(path(os.path.join("Controls", "uipics", "zoom_in.png")))

PYFORMS_ICON_EVENTTIMELINE_IMPORT = QtGui.QIcon(path(os.path.join("Controls", "uipics", "page_white_get.png")))
PYFORMS_ICON_EVENTTIMELINE_EXPORT = QtGui.QIcon(path(os.path.join("Controls", "uipics", "page_white_put.png")))


PYFORMS_ICON_FILE_OPEN = QtGui.QIcon()

PYFORMS_MAINWINDOW_MARGIN = 7