# -*- coding: utf-8 -*-

"""
Module implementing helpUIController.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from Ui_helpUI import Ui_MainWindow
import sys


class helpUIController(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(helpUIController, self).__init__(parent)
        self.setupUi(self)
        text = "关于软件：\n" + \
               "软件用于模型支持下的任意物体检测。\n\n" + \
               "---------------------帮助--------------------\n" + \
               "导入图像：\n" \
               "未导入图像之前图像的调整控件被锁定，您可通过文件选择按钮或文件选择框选取图片" \
               ""
        self.label.setText(text)
        self.show()

    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.close()

    def closeEvent(self, event):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainUI = helpUIController()
    sys.exit(app.exec_())
