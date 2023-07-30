# -*- coding: utf-8 -*-

"""
Module implementing balanceUIController.
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from Ui_balanceUI2 import Ui_MainWindow
from PIL import ImageFilter
from PIL import Image
from PIL import ImageQt
from PIL import ImageEnhance
from PIL import ImageOps
import sys
import cv2
import numpy as np
import os


class balanceUIController(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(balanceUIController, self).__init__(parent)
        self.setupUi(self)
        self.original_image = None
        self.draw_image = None
        self.general_image = None
        self.slider_move = False
        self.final_image = None
        self.original_image = None
        self.filter_select = False
        # self.filter_select1 = False
        # self.filter_select2 = False
        # self.filter_select3 = False
        self.invertColor_have_press = 0
        self.deColor_have_press = False
        self.filter_list = [self.filter_blue,self.filter_contour,
                           self.filter_detail,self.filter_max,
                           self.filter_min,self.filter_median,
                           self.filter_rank,self.filter_emboss,
                           self.filter_smooth,self.filter_sharpen,
                           self.filter_mode,self.filter_reset]
        # self.signal = QtCore.pyqtSignal(str)
        # self.init_ui()
        # self.start_ui()

    def init_ui(self):
        self.imgBalanceWin.setScaledContents(True)
        self.origin_mode()

    def start_ui(self):
        self.show_image(self.original_image)
        self.draw_image = self.original_image
        self.radio_button_event()
        self.slider_event()
        # self.show()

    def origin_mode(self):
        self.origin_Btn.setStyleSheet("background-color: rgb(193, 255, 230);")
        self.draw_Btn.setStyleSheet("background-color: rgb(225, 225, 225);")

    def draw_mode(self):
        self.origin_Btn.setStyleSheet("background-color: rgb(225, 225, 225);")
        self.draw_Btn.setStyleSheet("background-color: rgb(193, 255, 230);")

    def set_control_lock(self):
        pass

    def set_control_unlock(self):
        pass

    def slider_event(self):
        self.GaussBlurSlider.valueChanged.connect(self.img_GaussBlur_event)
        self.brightSlider.valueChanged.connect(self.img_bright_event)
        self.saturatSlider.valueChanged.connect(self.img_saturat_event)
        self.contrastSlider.valueChanged.connect(self.img_contrast_event)

    def img_GaussBlur_event(self):
        self.slider_move = True
        value = float(self.GaussBlurSlider.value())
        self.GaussBlur_label.setText(str(value))
        self.what_filter_is_check()
        filters = ImageFilter.GaussianBlur(radius=value)
        self.draw_image = self.general_image.filter(filters)
        self.retain_other_three('Gaussian')
        self.show_image(self.draw_image)

    def img_bright_event(self):
        self.slider_move = True
        value = float(self.brightSlider.value() / 50)
        self.bright_label.setText(str(value))
        self.what_filter_is_check()
        bright_enhance = ImageEnhance.Brightness(self.general_image)
        self.draw_image = bright_enhance.enhance(value)
        self.retain_other_three('bright')
        self.show_image(self.draw_image)

    def img_saturat_event(self):
        self.slider_move = True
        value = float(self.saturatSlider.value() / 50)
        self.saturat_label.setText(str(value))
        self.what_filter_is_check()
        saturat_enhance = ImageEnhance.Color(self.general_image)
        self.draw_image = saturat_enhance.enhance(value)
        self.retain_other_three('saturat')
        self.show_image(self.draw_image)

    def img_contrast_event(self):
        self.slider_move = True
        value = float(self.contrastSlider.value() / 50)
        self.contrast_label.setText(str(value))
        self.what_filter_is_check()
        contrast_enhance = ImageEnhance.Contrast(self.general_image)
        self.draw_image = contrast_enhance.enhance(value)
        self.retain_other_three(mode='constrast')
        self.show_image(self.draw_image)

    def retain_other_three(self, mode=''):
        value0 = float(self.brightSlider.value() / 50)
        value1 = float(self.saturatSlider.value() / 50)
        value2 = float(self.contrastSlider.value() / 50)
        value3 = float(self.GaussBlurSlider.value())
        if mode == 'general':
            self.draw_image = self.original_image
        if self.invertColor_have_press % 2 == 1:
            self.invertColor_have_press += 2
            self.draw_image = ImageOps.invert(self.draw_image)
        if self.deColor_have_press:
            self.draw_image = ImageEnhance.Color(self.draw_image).enhance(0)
        if mode == 'bright':
            saturat_enhance = ImageEnhance.Color(self.draw_image)
            self.draw_image = saturat_enhance.enhance(value1)
            contrast_enhance = ImageEnhance.Contrast(self.draw_image)
            self.draw_image = contrast_enhance.enhance(value2)
            filters = ImageFilter.GaussianBlur(radius=value3)
            self.draw_image = self.draw_image.filter(filters)
        elif mode == 'saturat':
            bright_enhance = ImageEnhance.Brightness(self.draw_image)
            self.draw_image = bright_enhance.enhance(value0)
            contrast_enhance = ImageEnhance.Contrast(self.draw_image)
            self.draw_image = contrast_enhance.enhance(value2)
            filters = ImageFilter.GaussianBlur(radius=value3)
            self.draw_image = self.draw_image.filter(filters)
        elif mode == 'constrast':
            bright_enhance = ImageEnhance.Brightness(self.draw_image)
            self.draw_image = bright_enhance.enhance(value0)
            saturat_enhance = ImageEnhance.Color(self.draw_image)
            self.draw_image = saturat_enhance.enhance(value1)
            filters = ImageFilter.GaussianBlur(radius=value3)
            self.draw_image = self.draw_image.filter(filters)
        elif mode == 'Gaussian':
            bright_enhance = ImageEnhance.Brightness(self.draw_image)
            self.draw_image = bright_enhance.enhance(value0)
            saturat_enhance = ImageEnhance.Color(self.draw_image)
            self.draw_image = saturat_enhance.enhance(value1)
            contrast_enhance = ImageEnhance.Contrast(self.draw_image)
            self.draw_image = contrast_enhance.enhance(value2)
        elif mode == 'general':
            bright_enhance = ImageEnhance.Brightness(self.draw_image)
            self.general_image = bright_enhance.enhance(value0)
            saturat_enhance = ImageEnhance.Color(self.general_image)
            self.general_image = saturat_enhance.enhance(value1)
            contrast_enhance = ImageEnhance.Contrast(self.general_image)
            self.general_image = contrast_enhance.enhance(value2)
            filters = ImageFilter.GaussianBlur(radius=value3)
            self.general_image = self.general_image.filter(filters)

    def radio_button_event(self):
        self.filter_reset.toggled.connect(self.radio_reset_event)
        self.filter_blue.toggled.connect(self.radio_blue_event)
        self.filter_contour.toggled.connect(self.radio_contour_event)
        self.filter_detail.toggled.connect(self.radio_detail_event)
        # self.filter_edge_enhance.toggled.connect(self.radio_edge_enhance_event)
        self.filter_emboss.toggled.connect(self.radio_emboss_event)
        self.filter_max.toggled.connect(self.radio_max_event)
        self.filter_median.toggled.connect(self.radio_median_event)
        self.filter_min.toggled.connect(self.radio_min_event)
        self.filter_mode.toggled.connect(self.radio_mode_event)
        self.filter_rank.toggled.connect(self.radio_rank_event)
        self.filter_sharpen.toggled.connect(self.radio_sharpen_event)
        self.filter_smooth.toggled.connect(self.radio_smooth_event)

    def radio_reset_event(self):
        print("[radio] reset")
        # for item in self.filter_list:
        #     item.setChecked(False)
        # self.filter_min.setChecked(False)
        # self.filter_min.setCheckanle(False)
        self.filter_select = False
        # self.filter_select1 = self.filter_select2 = self.filter_select3 = False
        self.retain_other_three('general')
        self.draw_image = self.general_image
        self.show_image(self.draw_image)

    def what_filter_is_check(self):
        if self.filter_blue.isChecked():
            self.general_image = self.original_image.filter(ImageFilter.BLUR)
        elif self.filter_contour.isChecked():
            self.general_image = self.original_image.filter(ImageFilter.CONTOUR)
        elif self.filter_detail.isChecked():
            self.general_image = self.original_image.filter(ImageFilter.CONTOUR)
        elif self.filter_max.isChecked():
            self.general_image = self.original_image.filter(ImageFilter.MaxFilter)
        elif self.filter_min.isChecked():
            self.general_image = self.original_image.filter(ImageFilter.MinFilter)
        elif self.filter_median.isChecked():
            self.general_image = self.original_image.filter(ImageFilter.MedianFilter)
        elif self.filter_rank.isChecked():
            self.general_image = self.original_image.filter(ImageFilter.RankFilter(5, 0))
        # elif self.filter_edge_enhance.isChecked():
        #     self.general_image = self.original_image.filter(ImageFilter.EDGE_ENHANCE)
        elif self.filter_emboss.isChecked():
            self.general_image = self.original_image.filter(ImageFilter.EMBOSS)
        elif self.filter_smooth.isChecked():
            self.general_image = self.original_image.filter(ImageFilter.SMOOTH)
        elif self.filter_sharpen.isChecked():
            self.general_image = self.original_image.filter(ImageFilter.SHARPEN)
        elif self.filter_mode.isChecked():
            self.general_image = self.original_image.filter(ImageFilter.ModeFilter)
        else:
            self.general_image = self.original_image

    def radio_blue_event(self):
        print("[radio] filter_blue")
        self.retain_other_three('general')
        self.draw_image = self.general_image.filter(ImageFilter.BLUR)
        self.filter_select = True
        self.show_image(self.draw_image)

    def radio_contour_event(self):
        print("[radio] filter_contour")
        self.retain_other_three('general')
        self.draw_image = self.general_image.filter(ImageFilter.CONTOUR)
        self.filter_select = True
        self.show_image(self.draw_image)

    def radio_detail_event(self):
        print("[radio] filter_detail")
        self.retain_other_three('general')
        self.draw_image = self.general_image.filter(ImageFilter.DETAIL)
        self.filter_select = True
        self.show_image(self.draw_image)

    def radio_edge_enhance_event(self):
        print("[radio] filter_edge_enhance")
        self.retain_other_three('general')
        self.draw_image = self.general_image.filter(ImageFilter.EDGE_ENHANCE)
        self.filter_select = True
        self.show_image(self.draw_image)

    def radio_emboss_event(self):
        print("[radio] filter_emboss")
        self.retain_other_three('general')
        self.draw_image = self.general_image.filter(ImageFilter.EMBOSS)
        self.filter_select = True
        self.show_image(self.draw_image)

    def radio_max_event(self):
        print("[radio] filter_max")
        self.retain_other_three('general')
        self.draw_image = self.general_image.filter(ImageFilter.MaxFilter)
        self.filter_select = True
        self.show_image(self.draw_image)

    def radio_median_event(self):
        print("[radio] filter_median")
        self.retain_other_three('general')
        self.draw_image = self.general_image.filter(ImageFilter.MedianFilter)
        self.filter_select = True
        self.show_image(self.draw_image)

    def radio_min_event(self):
        print("[radio] filter_min")
        self.retain_other_three('general')
        self.draw_image = self.general_image.filter(ImageFilter.MinFilter)
        self.filter_select = True
        self.show_image(self.draw_image)

    def radio_mode_event(self):
        print("[radio] mode")
        self.retain_other_three('general')
        self.draw_image = self.general_image.filter(ImageFilter.ModeFilter)
        self.filter_select = True
        self.show_image(self.draw_image)

    def radio_rank_event(self):
        print("[radio] filter_rank")
        self.retain_other_three('general')
        self.draw_image = self.general_image.filter(ImageFilter.RankFilter(5, 0))
        self.filter_select = True
        self.show_image(self.draw_image)

    def radio_sharpen_event(self):
        print("[radio] filter_sharpen")
        self.retain_other_three('general')
        self.draw_image = self.general_image.filter(ImageFilter.SHARPEN)
        self.filter_select = True
        self.show_image(self.draw_image)

    def radio_smooth_event(self):
        #  self.btn1.setChecked(True)
        print("[radio] filter_smooth")
        self.retain_other_three('general')
        self.draw_image = self.general_image.filter(ImageFilter.SMOOTH)
        self.filter_select = True
        self.show_image(self.draw_image)

    @staticmethod
    def PIL_to_QPixmap(image):
        pixmap = ImageQt.toqpixmap(image)
        return pixmap

    def pil_to_qt(self, image): # 已更正
        image = self.PIL_to_cv2(image) # cv2格式
        # h, w, ch = image.shape
        # bytesPerLine = ch * w
        # disp_frame = QtGui.QImage(image.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
        # return QPixmap.fromImage(disp_frame)
        try:
            # BGR => RGB 文件格式
            shrink = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # cv 图片转换成 qt图片
            qt_img = QtGui.QImage(shrink.data,  # 数据源
                                  shrink.shape[1],  # 宽度
                                  shrink.shape[0],  # 高度
                                  shrink.shape[1] * 3,  # 行字节数
                                  QtGui.QImage.Format_RGB888)
            # disp_frame = QtGui.QImage(image.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
            return QPixmap.fromImage(qt_img)
        except Exception as ex:
            print(ex)

    # PIL转cv2
    @staticmethod
    def PIL_to_cv2(image):
        try:
            # return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        except():
            return cv2.cvtColor(np.array(image), cv2.COLOR_BGRA2RGBA)

    # cv2转PIL
    @staticmethod
    def cv2_to_PIL(image):
        try:
            # return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        except():
            return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA))

    def show_image(self, image):
        # print("[test...] type(image)=>",type(image))
        if image == self.original_image or (self.slider_move is False and self.filter_select is False):
            self.origin_mode()
        else:
            self.draw_mode()
        self.imgBalanceWin.setPixmap(self.pil_to_qt(image))

    @pyqtSlot()
    def on_deColor_Btn_clicked(self):
        if self.draw_image is not None:
            Enhance = ImageEnhance.Color(self.draw_image)
        else:
            Enhance = ImageEnhance.Color(self.original_image)
        self.draw_image = Enhance.enhance(0)
        self.deColor_have_press = True
        self.show_image(self.draw_image)

    @pyqtSlot()
    def on_invertColor_Btn_clicked(self):
        try:
            if self.draw_image is not None:
                self.draw_image = ImageOps.invert(self.draw_image)
            else:
                self.draw_image = ImageOps.invert(self.original_image)
            self.invertColor_have_press += 1
            self.show_image(self.draw_image)
        except():
            print("on_invertColor_Btn_clicked: 反色异常")

    @pyqtSlot()
    def on_origin_Btn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.show_image(self.original_image)

    @pyqtSlot()
    def on_draw_Btn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if self.draw_image is not None:
            self.show_image(self.draw_image)

    def reset_slider(self):
        self.slider_move = False
        self.GaussBlurSlider.setSliderPosition(0)
        self.brightSlider.setSliderPosition(50)
        self.saturatSlider.setSliderPosition(50)
        self.contrastSlider.setSliderPosition(50)
        self.GaussBlur_label.setText('0')
        self.bright_label.setText('50')
        self.saturat_label.setText('50')
        self.contrast_label.setText('50')

    @pyqtSlot()
    def on_reset_Btn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        try:
            self.filter_reset.setChecked(True)
            self.reset_slider()
            self.invertColor_have_press = 0
            self.deColor_have_press = False
            self.draw_image = self.original_image
            self.general_image = None
            self.show_image(self.original_image)
        except():
            print('on_reset_Btn_clicked: 重置按钮错误')

    @pyqtSlot()
    def on_ok_Btn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        reply = QMessageBox.question(self, 'warning', '该图片将会覆盖原图片，您确定要覆盖吗？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.draw_image is not None:
                self.final_image = self.draw_image
            else:
                self.final_image = self.original_image

            basepath = os.path.dirname(__file__)
            tmp_image_dir = basepath+'/.tmp_pic'  # 临时保存数据增广后的结果
            print("[create...] tmp_image_dir=>",tmp_image_dir)
            if not os.path.exists(tmp_image_dir):
                os.makedirs(tmp_image_dir)
            self.final_image.save(tmp_image_dir+'/tmp.jpg')

            self.signal.emit("OK")
            self.close()
        else:
            return

    def closeEvent(self, event):
        # if self.draw_image != None:
        #     reply = QMessageBox.question(self, 'warning', '您调整了图片，确定要退出吗？',
        #                                  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        #     if reply == QMessageBox.Yes:
        #         event.accept()
        #     else:
        #         event.ignore()
        pass


def run_balance_Win(image=None):
    app = QtWidgets.QApplication(sys.argv)
    balanceUI = balanceUIController()
    balanceUI.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    img = Image.open('./Images/2.jpeg')
    run_balance_Win(image=img)
