# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\python\qt\balanceUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(957, 751)
        MainWindow.setWindowTitle("图像增广界面")
        MainWindow.setWindowIcon(QIcon('./Icons/pig_nose.png'))
        MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.imgBalanceWin = QtWidgets.QLabel(self.centralWidget)
        self.imgBalanceWin.setGeometry(QtCore.QRect(130, 30, 721, 451))
        self.imgBalanceWin.setText("")
        self.imgBalanceWin.setObjectName("imgBalanceWin")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(660, 550, 141, 121))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(10, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralWidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(360, 550, 400, 121))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_3.setContentsMargins(10, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.filter_mode = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.filter_mode.setObjectName("filter_mode")
        # self.gridLayout.addWidget(self.filter_mode, 3, 0, 1, 1)
        self.gridLayout_3.addWidget(self.filter_mode, 3, 2, 1, 1)
        self.filter_sharpen = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.filter_sharpen.setObjectName("filter_sharpen")
        # self.gridLayout.addWidget(self.filter_sharpen, 2, 0, 1, 1)
        self.gridLayout_3.addWidget(self.filter_sharpen, 2, 2, 1, 1)
        self.filter_smooth = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.filter_smooth.setObjectName("filter_smooth")
        # self.gridLayout.addWidget(self.filter_smooth, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.filter_smooth, 1, 2, 1, 1)
        self.filter_emboss = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.filter_emboss.setObjectName("filter_emboss")
        # self.gridLayout.addWidget(self.filter_emboss, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.filter_emboss, 0, 2, 1, 1)

        self.filter_max = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        self.filter_max.setObjectName("filter_max")
        self.gridLayout_3.addWidget(self.filter_max, 3, 0, 1, 1)
        self.filter_reset = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        self.filter_reset.setObjectName("filter_reset")
        self.gridLayout_3.addWidget(self.filter_reset, 0, 0, 1, 1)
        self.filter_contour = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        self.filter_contour.setObjectName("filter_contour")
        self.gridLayout_3.addWidget(self.filter_contour, 2, 0, 1, 1)
        self.filter_blue = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        self.filter_blue.setObjectName("filter_blue")
        self.gridLayout_3.addWidget(self.filter_blue, 1, 0, 1, 1)
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.centralWidget)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(510, 550, 136, 121))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_4.setContentsMargins(10, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.filter_detail = QtWidgets.QRadioButton(self.gridLayoutWidget_3)
        self.filter_detail.setObjectName("filter_detail")
        # self.gridLayout_4.addWidget(self.filter_detail, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.filter_detail, 1, 1, 1, 1)
        self.filter_median = QtWidgets.QRadioButton(self.gridLayoutWidget_3)
        self.filter_median.setObjectName("filter_median")
        # self.gridLayout_4.addWidget(self.filter_median, 2, 0, 1, 1)
        self.gridLayout_3.addWidget(self.filter_median, 2, 1, 1, 1)
        self.filter_rank = QtWidgets.QRadioButton(self.gridLayoutWidget_3)
        self.filter_rank.setObjectName("filter_rank")
        # self.gridLayout_4.addWidget(self.filter_rank, 3, 0, 1, 1)
        self.gridLayout_3.addWidget(self.filter_rank, 3, 1, 1, 1)
        self.filter_min = QtWidgets.QRadioButton(self.gridLayoutWidget_3)
        self.filter_min.setObjectName("filter_min")
        # self.gridLayout_4.addWidget(self.filter_min, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.filter_min, 0, 1, 1, 1)

        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(50, 30, 211, 21))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.saturatSlider = QtWidgets.QSlider(self.centralWidget)
        self.saturatSlider.setGeometry(QtCore.QRect(90, 630, 160, 22))
        self.saturatSlider.setSliderPosition(50)
        self.saturatSlider.setOrientation(QtCore.Qt.Horizontal)
        self.saturatSlider.setObjectName("saturatSlider")
        self.brightLabel = QtWidgets.QLabel(self.centralWidget)
        self.brightLabel.setGeometry(QtCore.QRect(20, 580, 50, 16))
        self.brightLabel.setStyleSheet("color: rgb(35, 35, 35);")
        self.brightLabel.setObjectName("brightLabel")
        self.saturatLabel = QtWidgets.QLabel(self.centralWidget)
        self.saturatLabel.setGeometry(QtCore.QRect(20, 630, 50, 15))
        self.saturatLabel.setStyleSheet("color: rgb(35, 35, 35);")
        self.saturatLabel.setObjectName("saturatLabel")
        self.contrastLabel = QtWidgets.QLabel(self.centralWidget)
        self.contrastLabel.setGeometry(QtCore.QRect(20, 680, 50, 15))
        self.contrastLabel.setStyleSheet("color: rgb(35, 35, 35);")
        self.contrastLabel.setObjectName("contrastLabel")
        self.brightSlider = QtWidgets.QSlider(self.centralWidget)
        self.brightSlider.setEnabled(True)
        self.brightSlider.setGeometry(QtCore.QRect(90, 580, 160, 22))
        self.brightSlider.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.brightSlider.setMouseTracking(False)
        self.brightSlider.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.brightSlider.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.brightSlider.setAutoFillBackground(False)
        self.brightSlider.setSliderPosition(50)
        self.brightSlider.setOrientation(QtCore.Qt.Horizontal)
        self.brightSlider.setObjectName("brightSlider")
        self.contrastSlider = QtWidgets.QSlider(self.centralWidget)
        self.contrastSlider.setGeometry(QtCore.QRect(90, 680, 160, 22))
        self.contrastSlider.setSliderPosition(50)
        self.contrastSlider.setOrientation(QtCore.Qt.Horizontal)
        self.contrastSlider.setObjectName("contrastSlider")
        self.GaussBlurLabel = QtWidgets.QLabel(self.centralWidget)
        self.GaussBlurLabel.setGeometry(QtCore.QRect(20, 540, 61, 16))
        self.GaussBlurLabel.setStyleSheet("color: rgb(35, 35, 35);")
        self.GaussBlurLabel.setObjectName("GaussBlurLabel")
        self.GaussBlurSlider = QtWidgets.QSlider(self.centralWidget)
        self.GaussBlurSlider.setEnabled(True)
        self.GaussBlurSlider.setGeometry(QtCore.QRect(90, 540, 160, 22))
        self.GaussBlurSlider.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.GaussBlurSlider.setMouseTracking(False)
        self.GaussBlurSlider.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.GaussBlurSlider.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.GaussBlurSlider.setAutoFillBackground(False)
        self.GaussBlurSlider.setMaximum(10)
        self.GaussBlurSlider.setSliderPosition(0)
        self.GaussBlurSlider.setOrientation(QtCore.Qt.Horizontal)
        self.GaussBlurSlider.setObjectName("GaussBlurSlider")
        self.origin_Btn = QtWidgets.QPushButton(self.centralWidget)
        self.origin_Btn.setGeometry(QtCore.QRect(520, 700, 93, 28))
        self.origin_Btn.setStyleSheet("")
        self.origin_Btn.setObjectName("origin_Btn")
        self.draw_Btn = QtWidgets.QPushButton(self.centralWidget)
        self.draw_Btn.setGeometry(QtCore.QRect(660, 700, 93, 28))
        self.draw_Btn.setObjectName("draw_Btn")
        self.reset_Btn = QtWidgets.QPushButton(self.centralWidget)
        self.reset_Btn.setGeometry(QtCore.QRect(380, 700, 93, 28))
        self.reset_Btn.setObjectName("reset_Btn")
        self.ok_Btn = QtWidgets.QPushButton(self.centralWidget)
        self.ok_Btn.setGeometry(QtCore.QRect(800, 700, 93, 28))
        self.ok_Btn.setObjectName("ok_Btn")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 1001, 751))
        # 界面背景颜色
        # self.label_2.setStyleSheet("background-color: rgb(255, 250, 212);\n"
        #                            "")
        self.label_2.setStyleSheet("background-color: rgb(229, 251, 245);\n"
                                   "")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.GaussBlur_label = QtWidgets.QLabel(self.centralWidget)
        self.GaussBlur_label.setGeometry(QtCore.QRect(270, 540, 31, 21))
        self.GaussBlur_label.setAlignment(QtCore.Qt.AlignCenter)
        self.GaussBlur_label.setObjectName("GaussBlur_label")
        self.saturat_label = QtWidgets.QLabel(self.centralWidget)
        self.saturat_label.setGeometry(QtCore.QRect(270, 630, 31, 21))
        self.saturat_label.setAlignment(QtCore.Qt.AlignCenter)
        self.saturat_label.setObjectName("saturat_label")
        self.bright_label = QtWidgets.QLabel(self.centralWidget)
        self.bright_label.setGeometry(QtCore.QRect(270, 580, 31, 21))
        self.bright_label.setAlignment(QtCore.Qt.AlignCenter)
        self.bright_label.setObjectName("bright_label")
        self.contrast_label = QtWidgets.QLabel(self.centralWidget)
        self.contrast_label.setGeometry(QtCore.QRect(270, 680, 31, 21))
        self.contrast_label.setAlignment(QtCore.Qt.AlignCenter)
        self.contrast_label.setObjectName("contrast_label")
        self.deColor_Btn = QtWidgets.QPushButton(self.centralWidget)
        self.deColor_Btn.setGeometry(QtCore.QRect(810, 580, 71, 22))
        self.deColor_Btn.setObjectName("deColor_Btn")
        self.invertColor_Btn = QtWidgets.QPushButton(self.centralWidget)
        self.invertColor_Btn.setGeometry(QtCore.QRect(810, 620, 71, 22))
        self.invertColor_Btn.setObjectName("invertColor_Btn")
        self.label_2.raise_()
        self.imgBalanceWin.raise_()
        # self.gridLayoutWidget.raise_()
        self.gridLayoutWidget_2.raise_()
        # self.gridLayoutWidget_3.raise_()
        # self.label.raise_()
        self.saturatSlider.raise_()
        self.brightLabel.raise_()
        self.saturatLabel.raise_()
        self.contrastLabel.raise_()
        self.brightSlider.raise_()
        self.contrastSlider.raise_()
        self.GaussBlurLabel.raise_()
        self.GaussBlurSlider.raise_()
        self.origin_Btn.raise_()
        self.draw_Btn.raise_()
        self.reset_Btn.raise_()
        self.ok_Btn.raise_()
        self.GaussBlur_label.raise_()
        self.saturat_label.raise_()
        self.bright_label.raise_()
        self.contrast_label.raise_()
        self.deColor_Btn.raise_()
        self.invertColor_Btn.raise_()
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.filter_mode.setText(_translate("MainWindow", "波形滤镜 "))
        self.filter_sharpen.setText(_translate("MainWindow", "锐化滤镜 "))
        self.filter_smooth.setText(_translate("MainWindow", "平滑滤镜 "))
        self.filter_emboss.setText(_translate("MainWindow", "浮雕滤镜"))
        self.brightLabel.setText(_translate("MainWindow", "亮度"))
        self.brightLabel.setStyleSheet("color: rgb(220,20,60);")
        self.saturatLabel.setText(_translate("MainWindow", "饱和度"))
        self.saturatLabel.setStyleSheet("color: rgb(220,20,60);")
        self.contrastLabel.setText(_translate("MainWindow", "对比度"))
        self.contrastLabel.setStyleSheet("color: rgb(220,20,60);")
        self.GaussBlurLabel.setText(_translate("MainWindow", "高斯模糊"))
        self.GaussBlurLabel.setStyleSheet("color: rgb(220,20,60);")
        self.deColor_Btn.setText(_translate("MainWindow", "去色"))
        self.invertColor_Btn.setText(_translate("MainWindow", "反色"))
        self.origin_Btn.setText(_translate("MainWindow", "原图"))
        self.draw_Btn.setText(_translate("MainWindow", "效果图"))
        self.reset_Btn.setText(_translate("MainWindow", "复原"))
        self.ok_Btn.setText(_translate("MainWindow", "确定"))
        self.GaussBlur_label.setText(_translate("MainWindow", "0"))
        self.saturat_label.setText(_translate("MainWindow", "50"))
        self.bright_label.setText(_translate("MainWindow", "50"))
        self.contrast_label.setText(_translate("MainWindow", "50"))
        self.filter_max.setText(_translate("MainWindow", "最大值滤波"))
        self.filter_reset.setText(_translate("MainWindow", "复原"))
        self.filter_contour.setText(_translate("MainWindow", "轮廓滤镜"))
        self.filter_blue.setText(_translate("MainWindow", "模糊滤镜"))
        self.filter_detail.setText(_translate("MainWindow", "细节滤镜"))
        # self.filter_edge_enhance.setText(_translate("MainWindow", "边界增强滤镜"))
        self.filter_median.setText(_translate("MainWindow", "中值滤波滤镜 "))
        self.filter_rank.setText(_translate("MainWindow", "等级滤波 "))
        self.filter_min.setText(_translate("MainWindow", "最小值滤波  "))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())