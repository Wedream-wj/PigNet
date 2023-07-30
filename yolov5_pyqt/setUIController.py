# -*- coding: utf-8 -*-

"""
Module implementing setUIController.
"""
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from Ui_setUI import Ui_MainWindow


class setUIController(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    signal_music_Box = QtCore.pyqtSignal(str)
    signal_musicSlider = QtCore.pyqtSignal(str)
    signal_last_music = QtCore.pyqtSignal(str)
    signal_next_music = QtCore.pyqtSignal(str)
    signal_static_pic_Box = QtCore.pyqtSignal(str)
    signal_pic_mask_Box = QtCore.pyqtSignal(str)
    signal_video_type = QtCore.pyqtSignal(str)
    signal_imgLab_adapt = QtCore.pyqtSignal(str)
    signal_win_adapt = QtCore.pyqtSignal(str)

    def __init__(self, meta, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(setUIController, self).__init__(parent)
        self.isMusicPlay = meta['play']
        self.sound = meta['sound']
        self.setupUi(self)
        self.is_music_play()
        self.slider_event()
        self.checkBox_event()
        self.radio_event()

    def start_ui(self):
        self.show()

    def is_music_play(self):
        if self.isMusicPlay:
            self.musicSlider.setValue(self.sound)
            self.music_Box.setChecked(True)
        else:
            self.music_Box.setChecked(False)

    def slider_event(self):
        self.musicSlider.valueChanged.connect(self.music_slider_event)

    def music_slider_event(self):
        value = self.musicSlider.value()
        self.signal_musicSlider.emit(str(value))

    def checkBox_event(self):
        self.music_Box.stateChanged.connect(self.music_event)
        self.statc_pic_Box.stateChanged.connect(self.state_pic_event)
        self.pic_mask_Box.stateChanged.connect(self.pic_mask_event)
        self.imgLab_adaption.stateChanged.connect(self.imgLab_adapt_event)
        self.win_adaption.stateChanged.connect(self.win_adapt_event)

    def music_event(self):
        self.signal_music_Box.emit('')

    def state_pic_event(self):
        if self.statc_pic_Box.isChecked():
            self.signal_static_pic_Box.emit('yes')
        else:
            self.signal_static_pic_Box.emit('no')

    def pic_mask_event(self):
        if self.pic_mask_Box.isChecked():
            self.signal_pic_mask_Box.emit('yes')
        else:
            self.signal_pic_mask_Box.emit('no')

    def imgLab_adapt_event(self):
        if self.imgLab_adaption.isChecked():
            self.signal_imgLab_adapt.emit("yes")
        else:
            self.signal_imgLab_adapt.emit("no")

    def win_adapt_event(self):
        if self.win_adaption.isChecked():
            self.signal_win_adapt.emit("yes")
        else:
            self.signal_win_adapt.emit("no")

    def radio_event(self):
        self.detectRadio.toggled.connect(self.radio_detect_event)
        self.trackRadio.toggled.connect(self.radio_track_event)

    def radio_detect_event(self):
        if self.detectRadio.isChecked():
            self.signal_video_type.emit('detect')

    def radio_track_event(self):
        if self.trackRadio.isChecked():
            self.signal_video_type.emit('track')

    @pyqtSlot()
    def on_last_music_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.signal_last_music.emit('')
        self.music_Box.setChecked(True)

    @pyqtSlot()
    def on_next_music_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.signal_next_music.emit('')
        self.music_Box.setChecked(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainUI = setUIController({"play": True, "sound": 50})
    mainUI.show()

    sys.exit(app.exec_())
