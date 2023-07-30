# -*- coding: utf-8 -*-

"""
Module implementing videoUIController.
"""
import sys
import threading

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from UI_videoUI import Ui_MainWindow
import cv2


class videoUIController(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    signal_musicSlider = QtCore.pyqtSignal(str)

    def __init__(self, result, imgLab_adapt=False):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(videoUIController, self).__init__()
        self.img_list = result['frame_list']
        self.frame = result['frame']
        self.frame_info = result['frame_info']
        self.n = len(self.img_list)
        self.index = 0

        self.current_frame = self.frame

        self.setupUi(self)

        self.imgLab_adapt = imgLab_adapt
        self.original_x = self.imgWin.x()
        self.original_y = self.imgWin.y()
        self.original_w = self.imgWin.width()
        self.original_h = self.imgWin.height()
        self.image_radio = 1

        self.imgWin.setScaledContents(True)
        self.infoLabel.setWordWrap(True)

        self.is_play = False
        self.slider_event()
        self.speed_event()
        self.print_info()

    def start_ui(self):
        self.show()
        img = self.img_list[0]
        self.image_radio = img.shape[1] / img.shape[0]
        print(img.shape)
        self.set_label_geometry()
        self.show_image(self.get_frame(0))

    # ------------------播放状态-------------------
    def play_mode(self):
        self.playButton.setText("暂停")

    def pause_mode(self):
        self.playButton.setText("播放")

    # 显示信息
    def print_info(self):
        info = "视频信息：\n"
        info = info + f"帧率：{self.frame}\n"
        info = info + f"总帧数：{self.n}\n"
        info = info + f"时长：{self.n / self.frame}\n\n"
        info = info + f"当前帧：{self.index}\n"
        info = info + f"当前帧率：{self.current_frame}\n"
        info = info + f"帧信息：{self.frame_info[self.index] if self.index < len(self.frame_info) else '无'}\n\n"
        info = info + f"播放转态：{'播放' if self.is_play else '暂停'}\n"

        self.infoLabel.setText(info)

    # 取帧
    def get_frame(self, index):
        if index >= self.n:
            return
        img = cv2.cvtColor(self.img_list[index], cv2.COLOR_RGB2BGR)
        return QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)

    # 显示帧
    def show_image(self, img):
        if img is None:
            return
        self.imgWin.setPixmap(QPixmap.fromImage(img))

    # 倍速控制
    def speed_event(self):
        self.speedButton.addItems(
            [str(self.frame // 4), str(self.frame // 2), str(self.frame), str(self.frame * 2), str(self.frame * 4),
             '25'])
        self.speedButton.setCurrentText(str(self.current_frame))
        self.speedButton.currentIndexChanged[str].connect(self.speed_change_event)

    # 倍速事件
    def speed_change_event(self, i):
        self.current_frame = int(i)

    # 进度条事件
    def slider_event(self):
        self.progressSlider.setRange(0, self.n)
        self.progressSlider.sliderMoved.connect(self.progressSlider_move_event)
        self.progressSlider.sliderPressed.connect(self.progressSlider_press_event)
        self.progressSlider.sliderReleased.connect(self.progressSlider_release_event)

    # 按下滑块
    def progressSlider_press_event(self):
        pass

    # 释放滑块
    def progressSlider_release_event(self):
        value = int(self.progressSlider.value())
        self.frameLabel.setText(str(value))

    # 移动滑块
    def progressSlider_move_event(self):
        self.is_play = False
        self.print_info()
        self.pause_mode()
        value = int(self.progressSlider.value())
        self.frameLabel.setText(str(value))
        self.index = value
        self.show_image(self.get_frame(value))

    # 播放
    @pyqtSlot()
    def on_playButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if not self.is_play:
            self.is_play = True
            self.play_mode()
            thread = threading.Thread(target=self.play)
            thread.start()
        else:
            self.pause_mode()
            self.is_play = False
            self.print_info()

    def play(self):
        while self.is_play and self.index < self.n:
            # print(f"第{self.index}帧")
            self.set_label_geometry()
            img = self.get_frame(self.index)
            self.show_image(img)
            self.progressSlider.setValue(self.index)
            self.frameLabel.setText(str(self.index))
            self.print_info()
            self.index += 1
            cv2.waitKey(int(1000 / self.current_frame))

    # 重播
    @pyqtSlot()
    def on_replayButton_clicked(self):
        self.index = 0
        self.is_play = False
        self.on_playButton_clicked()

    # 保存视频结果
    @pyqtSlot()
    def on_saveButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        save_video_name = QFileDialog.getSaveFileName(self, "save video", "./output/", "videos(*.mp4)")[0]
        if save_video_name == '':
            return
        shape = self.img_list[0].shape
        out = cv2.VideoWriter(save_video_name, cv2.VideoWriter_fourcc(*'mp4v'), self.current_frame,
                              (shape[1], shape[0]))
        print(self.current_frame)
        for i, img in enumerate(self.img_list):
            # print(f"写入第{i}帧")
            out.write(img)
        out.release()

    def set_label_geometry(self):
        try:
            if not self.imgLab_adapt:
                x = self.original_x
                y = self.original_y
                w = self.original_w
                h = self.original_h
                self.imgWin.setGeometry(QtCore.QRect(x, y, w, h))
            else:
                lefts = self.original_x
                tops = self.original_y
                rights = self.original_x + self.original_w
                bottoms = self.original_y + self.original_h

                imgLab_cx = (lefts + rights) / 2
                imgLab_cy = (tops + bottoms) / 2

                if self.image_radio >= 1:
                    imgLab_h = bottoms - tops
                    imgLab_w = imgLab_h * self.image_radio
                    if imgLab_w > (rights - lefts):
                        imgLab_w = rights - lefts
                        imgLab_h = imgLab_w / self.image_radio
                else:
                    imgLab_w = rights - lefts
                    imgLab_h = imgLab_w * self.image_radio
                    if imgLab_h > (bottoms - tops):
                        imgLab_h = bottoms - tops
                        imgLab_w = imgLab_h / self.image_radio

                x, y, w, h = int(imgLab_cx - imgLab_w / 2), int(imgLab_cy - imgLab_h / 2), int(imgLab_w), int(
                    imgLab_h)

                # print(f"x:{x}, y:{y}, w:{w}, h:{h}")

                self.imgWin.setGeometry(QtCore.QRect(x, y, w, h))
        except Exception as ex:
            print(ex)


if __name__ == "__main__":
    capture = cv2.VideoCapture(r'E:\python\Yolov5_DeepSort_Pytorch\qt\02.mp4')
    frame_list = []
    while True:
        _, frame = capture.read()
        if not _:
            break
        frame_list.append(frame)
    video = {'frame_list': frame_list, "frame": 25, 'frame_info': []}
    app = QtWidgets.QApplication(sys.argv)
    mainUI = videoUIController(video, imgLab_adapt=False)
    mainUI.start_ui()
    sys.exit(app.exec_())
