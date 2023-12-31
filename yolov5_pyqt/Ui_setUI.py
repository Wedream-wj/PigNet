# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\python\qt\setUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QRadioButton, QButtonGroup


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(250, 310)
        MainWindow.setWindowTitle("设置")
        MainWindow.setWindowIcon(QIcon('./Icons/setting3.png'))
        MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.music_Box = QtWidgets.QCheckBox(self.centralWidget)
        self.music_Box.setGeometry(QtCore.QRect(10, 20, 61, 19))
        self.music_Box.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.music_Box.setObjectName("music_Box")
        self.music_change_label = QtWidgets.QLabel(self.centralWidget)
        self.music_change_label.setGeometry(QtCore.QRect(130, 20, 61, 21))
        self.music_change_label.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.music_change_label.setAlignment(QtCore.Qt.AlignCenter)
        self.music_change_label.setObjectName("music_change_label")
        self.last_music = QtWidgets.QPushButton(self.centralWidget)
        self.last_music.setGeometry(QtCore.QRect(110, 80, 93, 28))
        self.last_music.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.last_music.setObjectName("last_music")
        self.next_music = QtWidgets.QPushButton(self.centralWidget)
        self.next_music.setGeometry(QtCore.QRect(110, 120, 93, 28))
        self.next_music.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.next_music.setObjectName("next_music")
        self.statc_pic_Box = QtWidgets.QCheckBox(self.centralWidget)
        self.statc_pic_Box.setGeometry(QtCore.QRect(100, 160, 111, 21))
        self.statc_pic_Box.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.statc_pic_Box.setObjectName("statc_pic_Box")
        self.musicSlider = QtWidgets.QSlider(self.centralWidget)
        self.musicSlider.setGeometry(QtCore.QRect(10, 50, 22, 171))
        self.musicSlider.setSliderPosition(50)
        self.musicSlider.setOrientation(QtCore.Qt.Vertical)
        self.musicSlider.setObjectName("musicSlider")
        self.pic_mask_Box = QtWidgets.QCheckBox(self.centralWidget)
        self.pic_mask_Box.setGeometry(QtCore.QRect(100, 200, 121, 21))
        self.pic_mask_Box.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.pic_mask_Box.setObjectName("pic_mask_Box")

        self.imgLab_adaption = QtWidgets.QCheckBox(self.centralWidget)
        self.imgLab_adaption.setGeometry(QtCore.QRect(15, 275, 121, 21))
        self.imgLab_adaption.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.imgLab_adaption.setObjectName("imgLab_adaption")

        self.win_adaption = QtWidgets.QCheckBox(self.centralWidget)
        self.win_adaption.setGeometry(QtCore.QRect(135, 275, 121, 21))
        self.win_adaption.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.win_adaption.setObjectName("win_adaption")

        self.musicName = QtWidgets.QLabel(self.centralWidget)
        self.musicName.setGeometry(QtCore.QRect(80, 45, 151, 21))
        self.musicName.setStyleSheet("font: 10pt \"微软雅黑\";\n"
                                     "background-color: rgb(255, 240, 229);")
        self.musicName.setText("")
        self.musicName.setAlignment(QtCore.Qt.AlignCenter)
        self.musicName.setObjectName("musicName")

        self.detectRadio = QRadioButton(MainWindow)
        self.detectRadio.move(40, 235)
        self.detectRadio.setChecked(True)
        self.detectRadio.setStyleSheet("font: 10pt \"微软雅黑\";\n")
        self.trackRadio = QRadioButton(MainWindow)
        self.trackRadio.move(140, 235)
        self.trackRadio.setStyleSheet("font: 10pt \"微软雅黑\";\n")
        self.group = QButtonGroup()
        self.group.addButton(self.detectRadio, 1)
        self.group.addButton(self.trackRadio, 2)

        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.music_Box.setText(_translate("MainWindow", "音乐"))
        self.music_change_label.setText(_translate("MainWindow", "换曲"))
        self.last_music.setText(_translate("MainWindow", "上一首"))
        self.next_music.setText(_translate("MainWindow", "下一首"))
        self.statc_pic_Box.setText(_translate("MainWindow", "静态背景图"))
        self.pic_mask_Box.setText(_translate("MainWindow", "轮播图遮罩"))
        self.detectRadio.setText(_translate("MainWindow", "检测"))
        self.trackRadio.setText(_translate("MainWindow", "跟踪"))
        self.imgLab_adaption.setText(_translate("MainWindow", "图显自适应"))
        self.win_adaption.setText(_translate("MainWindow", "窗口自适应"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
