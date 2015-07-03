#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = ["Ricardo Ribeiro", "Hugo Cachitas"]
__credits__     = ["Ricardo Ribeiro", "Hugo Cachitas"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


from PyQt4 import uic
from PyQt4 import QtCore, QtGui

import pyforms.Utils.tools as tools
# from pyforms.BaseWidget import BaseWidget
# from pyforms.Controls.ControlButton import ControlButton
# from pyforms.Controls.ControlCombo import ControlCombo


class TimelinePopupWindow(QtGui.QDialog):
    """
    Opens a dialog where the user can specify the behavior annotated
    in the selected line, as well as some related options.

    The parent timeline widget must be given, as well as the track
    identifier to edit.
    """

    def __init__(self, parent, track_id):
        super(TimelinePopupWindow, self).__init__(parent=parent)
        self._parent = parent
        control_path = tools.getFileInSameDirectory(__file__, "TimelinePopupWindow.ui")
        self._ui = uic.loadUi(control_path)
        self._ui.setWindowTitle("Track {:d} properties".format(track_id + 1))

        # Dialog variables
        self.behaviors = []
        self.behavior = None
        self.color = self._parent.color
        self.current_track = track_id

        self._default_comboBox_text = "Add a new behavior"
        self.__get_existing_tracklabels()

        # Set default color display
        self.__preview_color()

        # SIGNALS
        self._ui.comboBox.currentIndexChanged.connect(self.__on_comboBox_change)
        self._ui.pushButton_add.clicked.connect(self.__add_behavior)
        self._ui.pushButton_remove.clicked.connect(self.__remove_behavior)
        self._ui.pushButton_color.clicked.connect(self.__pick_color)

    def __on_comboBox_change(self):
        """Handles comboBox index change."""
        cb = self._ui.comboBox
        self.behavior = cb.itemText(cb.currentIndex())

    def __add_behavior(self):
        """Add a behavior to the already existing ones."""
        cb = self._ui.comboBox
        text, ok = QtGui.QInputDialog.getText(self, 'Add behavior', 'Description:', text='')
        if ok:
            self.behavior = str(text)
            self.behaviors.append(self.behavior)
            self._ui.comboBox.addItem(self.behavior)
            cb.setCurrentIndex(cb.findText(self.behavior))

        # If adding the first item, we need to enable the comboBox and
        # remove the placeholder text
        if not cb.isEnabled():
            cb.removeItem(cb.findText(self._default_comboBox_text))
            cb.setEnabled(True)

    def __remove_behavior(self):
        """Remove a behavior from the already existing ones."""
        cb = self._ui.comboBox
        i = cb.currentIndex()
        self.behaviors.remove(str(cb.itemText(i)))
        cb.removeItem(i)

        # If there are no behaviors assigned, just fill the comboBox
        # with a placeholder
        if cb.count() < 1:
            cb.addItem(self._default_comboBox_text)
            cb.setEnabled(False)

    def __pick_color(self):
        """Dialog to choose a color."""
        self.color = QtGui.QColorDialog.getColor(self.color)
        self.__preview_color()

    def __preview_color(self):
        """
        Shows selected colors in two QLabel widgets.

        The first shows true color, while the second presents the color
        with an opacity as seen in the timeline and with some dummy text
        to preview readability.
        """
        pixmap = QtGui.QPixmap(50, 25)
        color = QtGui.QColor(*self.color.getRgb())

        # Preview color
        color.setAlpha(int(255 * 1.0))
        pixmap.fill(color)
        self._ui.label_color.setPixmap(pixmap)

        # Preview color with transparency and some text
        color.setAlpha(int(255 * 0.5))
        pixmap.fill(color)
        painter = QtGui.QPainter(pixmap)
        painter.setFont(QtGui.QFont('Decorative', 8))
        painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, "Text")
        painter.end()
        self._ui.label_color_alpha.setPixmap(pixmap)

    def __get_existing_tracklabels(self):
        """
        Gets existing track labels already assigned.

        Scans the timeline track labels and sets the comboBox value
        accordingly.
        """
        d = self._parent._tracks_info
        cb = self._ui.comboBox

        # Loop across timeline labels
        for key, value in d.items():
            # If there is already an assigned label, append it to the
            # behaviors list and to the comboBox (if not a duplicate)
            if value[0] != self._parent._defaulttracklabel:
                self.behavior = value[0]
                if self.behavior not in self.behaviors:
                    cb.addItem(self.behavior)
                    self.behaviors.append(self.behavior)

                # Set comboBox value to the one of the selected track
                if key == self.current_track:

                    cb.setCurrentIndex(cb.findText(self.behavior))

        # If there are no behaviors assigned yet, just fill the comboBox
        # with a placeholder
        if cb.count() < 1:
            cb.addItem(self._default_comboBox_text)
            cb.setEnabled(False)



















########################################################################
###
###     MAYBE IN THE FUTURE IMPLEMENT THIS USING THE BaseWidget

# class TimelinePopupWindow(BaseWidget):
#     """
#     Opens a dialog where the user can specify the behavior annotaded
#     in the selected line, as well as some related options.
#     """

#     def __init__(self, parent=None):
#         super(TimelinePopupWindow, self).__init__('Adjust line options')

#         if parent is not None:
#             self.parent = parent

#         self._behaviors = None
#         self._behaviorname  = None
#         self._linecolor = None

#         # Combobox
#         self._combobox = ControlCombo()

#         # Buttons
#         self._btn_add = ControlButton()
#         self._btn_remove = ControlButton()
#         self._btn_import = ControlButton()
#         self._btn_export = ControlButton()
#         self._btn_color = ControlButton()
#         self._btn_ok = ControlButton()
#         self._btn_cancel = ControlButton()

#         self._formset = ['_combobox',
#                          ('_btn_add', '_btn_remove', '_btn_import', '_btn_export'),
#                          ('_btn_ok', '_btn_cancel')]

#         def __choose_color(self):
#             pass
#             QtGui.QColorDialog.getColor()
