# -*- coding: utf-8 -*-

"""
Module implementing MainUIController.
"""
import shutil
import sys
import threading

from PyQt5 import QtCore

# sys.path.append("../qt")
# sys.path.append("../../yolov5")
# sys.path.append("../yolov5")
# sys.path.append("../yolov5")
# sys.path.append("../")
# print(sys.path)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtWidgets
from Ui_MainUI2 import Ui_MainWindow
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageQt
from balanceUIController2 import balanceUIController
from helpUIController import helpUIController
from setUIController import setUIController
import cv2
import numpy as np
# import pygame
import time
import os
import math
import random
import yaml
import matplotlib.pyplot as plt

basepath = os.path.dirname(__file__)

# import qtDetector
# det = qtDetector.YOLOv5(model = basepath + r"/weights/yolov5s_pig.pt",)
import onnx_inference3
det = onnx_inference3.Yolov5ONNX(onnx_path=basepath+r"/weights/yolov5s_pig_origin.onnx",)

# import global_var as glo
import warnings
warnings.filterwarnings("ignore")

IMG_FORMATS = ['bmp', 'jpg', 'jpeg', 'png', 'tif', 'tiff', 'dng', 'webp', 'mpo']  # 支持的图像格式
VID_FORMATS = ['mov', 'avi', 'mp4', 'mpg', 'mpeg', 'm4v', 'wmv', 'mkv']  # 支持的视频格式
AUD_FORMATS = ['mp3', 'flac', 'ape', 'wav']


# 杀死线程
def stop_thread(thread):
    tid, exctype = thread.ident, SystemExit

    """Raises an exception in the threads with id tid"""
    import inspect
    import ctypes
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


class MainUIController(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainUIController, self).__init__(parent)
        # pygame.init()
        self.setupUi(self)

        # 配置文件
        self.conf = None
        self.parse_conf_file()

        # 背景图片文件夹
        self.imgDir = './Images'
        # 诗句文件
        self.poetryPath = './Images/poetry.txt'

        self.img_list = []
        self.poetry_list = []
        self.music_list = []
        self.musicIndex = -3

        # 轮播前后图
        self.imgIndex = 0
        self.nextIndex = 1

        # 最大最近文件数
        self.max_recent_files = 15

        # 随机切换背景图
        self.img_play_random = True
        self.static_pic = True
        # 轮播图遮罩
        # self.use_img_mask = True
        self.use_img_mask = False
        self.musicPath = r'./music/5Flower Dance.mp3'
        # self.musicPackage = r'./music'
        self.musicPackage = r'D:\本地音乐'
        # 播放音乐
        self.isMusicPlay = False
        # 自动切换
        self.autoMusicPlay = True
        # 轮播间隔
        self.carousel_time = 5000
        # 音量
        self.musicSound = 50
        # 音量缩放比例
        self.musicRadio = 200
        # 最多加载音乐的数量
        self.max_music_num = 50

        # 文件位置
        self.chooseImgPath = '' # 选择的待检测图片的位置
        self.imgFilePath = ''
        self.vidFilePath = ''
        # 当前数据格式
        self.file_format = ''

        # 鼠标指针位置
        self.pos = None

        # 检测器
        # self.detector = None
        self.detector = det
        # 跟踪器(用于处理视频)
        self.tracker = None
        # 选择模型
        # self.select_model = '改进后处理算法的'+'\n\t '+'YOLOv5_CA模型'
        self.select_model = 'YOLOv5s模型'
        # 原始图像
        self.original_Image = None
        # 静态图像信息
        self.original_info = ""
        # 新图像
        self.new_Image = None
        # 检测图像
        self.detect_Image = None
        # 动态调整信息
        self.new_info = ""
        # 是否已加载图像
        self.haveImage = False
        # 是否检测过图像
        self.have_det = False
        # 图像调整层对象
        self.banlanceUI = None
        # 结果
        self.result = {'time': 0, 'num': 0, "info": ''}

        # 视频为检测/跟踪
        self.video_type = 'detect'
        # 原始视频
        self.original_video = None
        # 是否开启视频检测
        self.use_video = True
        # 视频第一帧
        self.first_frame = None
        # 帧集
        self.frame_list = []
        # 帧结果信息
        self.frame_info = []
        # 帧率
        self.fps = 25
        # 是否在opencv窗口显示
        self.show_in_cvWin = False

        # 解析文件支持列表
        self.file_support = self.parse_format_support()

        # ----------------------------------------------------
        # 设置界面
        self.setUI = setUIController({'play': self.isMusicPlay, 'sound': self.musicSound})
        # 帮助界面
        self.helpUI = None
        # 视频结果显示界面
        self.videoUI = None
        # 未加载图像不可以按钮
        self.control_Enable = [self.resetBtn, self.saveBtn, self.effectBtn, self.originBtn, self.detectBtn,
                               self.balanceBtn]
        # 鼠标跟踪，不放在此处可能出现其他情况
        self.setMouseTracking(True)

        # 原图和效果图按钮切换样式
        self.btn_no_select_style = "QPushButton{\n" + "    height:40px;\n" + "    border:1px solid #4e6096;\n" + "    background-color: rgb(155, 255, 189);\n" + "    color:#2a2a2a;\n" + "    font-family:\"微软雅黑\";\n" + "    font-size:17px;\n" + "    font-weight:bold;\n" + "    -moz-border-radius:10px;\n" + "}\n" + "QPushButton:hover{\n" + "    background-color:#2e9eff;\n" + "    border:1px solid #1569bd;\n" + "    color:#ecff3d;\n" + "}"
        self.btn_select_style = "QPushButton{height:40px;\n" + "    border:1px solid #4e6096;\n" + "    background-color: rgb(255, 255, 126);\n" + "    color:#2a2a2a;\n" + "    font-family:\"微软雅黑\";\n" + "    font-size:17px;\n" + "    font-weight:bold;\n" + "    -moz-border-radius:10px;\n" + "}\n" + "QPushButton:hover{\n" + "    background-color:#2e9eff;\n" + "    border:1px solid #1569bd;\n" + "    color:#ecff3d;\n" + "}"

        # 根据计时器更新窗体透明度
        self.counter = 1
        # 控制透明度的增减性
        self.degree = -0.01

        # 自适应布局参数
        # self.leftMargin = 300
        self.leftMargin = 20
        # self.topMargin = 70
        self.topMargin = 50
        self.bottomMargin = 170
        self.rightMargin = 460
        self.imgLab_width = self.imgDisplayLaebl.width()
        self.imgLab_height = self.imgDisplayLaebl.height()
        self.width = self.width()
        self.current_width = self.width
        self.height = self.height()
        self.current_height = self.height
        self.image_radio = 1

        # 窗口自适应
        self.win_adapt = True
        # 图显自适应
        self.imgLab_adapt = True

        # 时间定时器
        self.Timer = None
        # 轮播图定时器
        self.timer_ = None
        # 轮播淡入淡出定时器
        self.timer2 = None
        # 音乐播放定时器
        self.timer_music = None
        # 缓存清除定时器
        self.timer_clear = None
        self.init_UI()
        self.start_UI()

    # 初始化程序
    def init_UI(self):
        if self.win_adapt:
            self.setUI.win_adaption.setChecked(True)

        if self.imgLab_adapt:
            self.setUI.imgLab_adaption.setChecked(True)
        self.actionSave.setEnabled(False)
        if self.use_img_mask:
            # 图片模糊的遮罩
            # self.pic_mask.setStyleSheet("background-color: rgba(0, 0, 0, 125);")
            self.pic_mask.setStyleSheet("background-color: rgba(65,105,225, 50);")
            self.setUI.pic_mask_Box.setChecked(True)

        if self.static_pic:
            self.setUI.statc_pic_Box.setChecked(True)

        # 槽信号注解失效？？？
        self.actionOpen.triggered.connect(self.on_actionOpen_triggered)
        self.actionSave.triggered.connect(self.on_actionSave_triggered)
        self.actionQuit.triggered.connect(self.on_actionQuit_triggered)
        self.actionHelp.triggered.connect(self.on_actionHelp_triggered)
        self.actionYolov5s.setChecked(True)
        self.actionYolov5s.triggered.connect(self.on_yolov5s_triggered)
        self.actionYolov5l.triggered.connect(self.on_yolov5l_triggered)
        self.actionYolov5m.triggered.connect(self.on_yolov5m_triggered)
        self.actionYolov5x.triggered.connect(self.on_yolov5x_triggered)

    # 启动界面程序
    def start_UI(self):
        # 获取背景图片
        self.get_background_img_path(self.imgDir)
        # 获取诗句
        # self.get_poetry(poetry_txt=self.poetryPath)
        # 加载音乐
        # self.load_music()
        try:
            # pygame.mixer.music.load(self.musicPath)
            pass
        except Exception as ex:
            print(ex)
        # 是否播放音乐
        self.is_music_play()
        # 自动切换
        self.auto_music_play()
        # 轮播图
        self.carousel_img()
        # 滑动条事件绑定
        self.sliderEvent()

        # 创建样式
        self.create_style()

        # 图片自适应
        self.imgDisplayLaebl.setScaledContents(True)

        # 当前时间
        self.show_currentTime()
        # 控件加锁
        self.set_control_lock()

        self.show()

    # 解析配置文件
    def parse_conf_file(self):
        try:
            with open('./conf/conf.yaml') as f:
                self.conf = yaml.safe_load(f)
        except Exception as ex:
            print(ex)
        self.parse_recent_files()

    # 解析近期使用的文件
    def parse_recent_files(self):
        try:
            files = self.conf['recent_files']
            self.recentMenu.clear()
            for i in range(len(files)):
                file = files[len(files) - i - 1]
                action = QtWidgets.QAction(f"&{file}", self.recentMenu)
                self.recentMenu.addAction(action)
                action.triggered.connect(lambda: self.chooseFile(filename=file))
        except Exception as ex:
            print(ex)

    # 添加最近文件
    def add_recent_files(self, file):
        try:
            action = QtWidgets.QAction(f"&{file}", self.recentMenu)
            self.recentMenu.addAction(action)
            action.triggered.connect(lambda: self.chooseFile(filename=file))
        except Exception as ex:
            print(ex)

    def set_variable_value(self):
        try:
            self.imgDir = self.conf['imgDir']
            self.poetryPath = self.conf['poetryPath']
            self.img_play_random = self.conf['img_play_random']
            self.max_recent_files = self.conf['max_recent_files']
            self.use_img_mask = self.conf['use_img_mask']
            self.musicPath = self.conf['musicPath']
            self.musicPackage = self.conf['musicPackage']
            self.isMusicPlay = self.conf['isMusicPlay']
            self.autoMusicPlay = self.conf['autoMusicPlay']

            self.video_type = self.conf['video_type']
        except Exception as ex:
            print(ex)

    # 初始化清除定时器
    def init_clear_timer(self):
        try:
            self.timer_clear.stop()
        except Exception as ex:
            print(ex)
        self.timer_clear = QTimer()
        self.timer_clear.timeout.connect(self.clear_cache)
        self.timer_clear.start(30000)

    # 定时清空缓存
    def clear_cache(self):
        try:
            for ui in [self.banlanceUI, self.setUI, self.videoUI]:
                if ui is not None and ui.isVisible():
                    return
            self.detector = None
            self.tracker = None
            self.frame_list = []
            self.frame_info = []
            print("清除缓存成功")
        except Exception as ex:
            print(ex)
            print("清除缓存失败")

    # 单次定时任务
    @staticmethod
    def setTimer(func, t):
        try:
            timer = QTimer()
            timer.timeout.connect(func)
            timer.setSingleShot(True)
            timer.start(t)
        except Exception as ex:
            print(ex)

    # 解析脚本支持的文件格式
    def parse_format_support(self):
        s = "Images("
        for img in IMG_FORMATS:
            ss = "*." + img + ";"
            s += ss
        if self.use_video:
            s += ");; Videos("
            for vid in VID_FORMATS:
                ss = "*." + vid + ";"
                s += ss
            s += ")"
        return s

    # 加载音乐
    def load_music(self):
        try:
            max_num, i = self.max_music_num, 0
            if os.path.exists(self.musicPackage):
                file_list = os.listdir(path=self.musicPackage)
                for file in file_list:
                    if self.musicFile_is_available(file):
                        if file.split(".")[-1] in AUD_FORMATS and i < max_num:
                            path = os.path.join(self.musicPackage, file)
                            if os.path.isfile(path):
                                self.music_list.append(path)
                            i += 1
            self.check_music_available()
            random.shuffle(self.music_list)
        except Exception as ex:
            print(ex)

    # 自动切换音乐
    def auto_music_play(self):
        self.timer_music = QTimer()
        self.timer_music.timeout.connect(self.music_end)
        self.timer_music.start(1000)

    # 音乐结束
    def music_end(self):
        # if not pygame.mixer.music.get_busy() and self.isMusicPlay:
        #     self.next_music_event(context='')
        pass

    # 判断文件是否可用
    @staticmethod
    def musicFile_is_available(file):
        if file == '' or file is None:
            return False
        if file.find(' ') != -1:
            return False
        if file.find('\n') != -1:
            return False
        return True

    # 检查音乐是否可用
    def check_music_available(self):
        for music in self.music_list:
            try:
                # pygame.mixer.music.load(music)
                # pygame.mixer.music.play()
                pass
            except RuntimeError:
                self.music_list.remove(music)

    def is_music_play(self):
        try:
            # pygame.mixer.music.play()
            # pygame.mixer.music.set_volume(self.musicSound / self.musicRadio)
            pass
            if not self.isMusicPlay:
                # pygame.mixer.music.pause()
                icon__ = QtGui.QIcon()
                icon__.addPixmap(QtGui.QPixmap("./Icons/music_no.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.musicBtn.setIcon(icon__)
        except Exception as ex:
            print(ex)

    def create_style(self):
        pass

    # 原图按钮模式
    def origin_mode(self):
        self.originBtn.setStyleSheet(self.btn_select_style)
        self.effectBtn.setStyleSheet(self.btn_no_select_style)

    # 效果图按钮模式
    def new_mode(self):
        self.effectBtn.setStyleSheet(self.btn_select_style)
        self.originBtn.setStyleSheet(self.btn_no_select_style)

    # 设置调整层界面的确认槽函数，捕获调整后的图像
    def get_final_image(self, content):
        # print(content)
        if content == "OK":
            self.original_Image = self.banlanceUI.final_image
            final_image_path = basepath + '/.tmp_pic/tmp.jpg'  # 临时保存数据增广后的结果
            self.chooseImgPath = final_image_path
            self.on_resetBtn_clicked()

    # 控件加锁
    def set_control_lock(self):
        if self.original_Image is None and self.file_format in IMG_FORMATS or self.file_format == '':
            self.brightSlider.setEnabled(False)
            self.contrastSlider.setEnabled(False)
            self.saturatSlider.setEnabled(False)
            self.balanceBtn.setEnabled(False)
            self.detectBtn.setEnabled(False)
            self.originBtn.setEnabled(False)
            self.effectBtn.setEnabled(False)
            self.saveBtn.setEnabled(False)
            self.resetBtn.setEnabled(False)
        if self.vidFilePath is not None and self.file_format in VID_FORMATS:
            self.original_Image = None
            self.new_Image = None
            self.detect_Image = None
            self.brightSlider.setEnabled(False)
            self.contrastSlider.setEnabled(False)
            self.saturatSlider.setEnabled(False)
            for btn in self.control_Enable:
                btn.setEnabled(False)
                btn.setStyleSheet("QPushButton{\n"
                                  "    height:40px;\n"
                                  "    border:1px solid #4e6096;\n"
                                  "    background-color: rgb(255, 255, 255, 125);\n"
                                  # "    background-color: rgb(155, 255, 189);\n"
                                  "    color:#2a2a2a;\n"
                                  # "    background-color:#61ddff;\n"
                                  "    font-family:\"微软雅黑\";\n"
                                  "    font-size:17px;\n"
                                  "    font-weight:bold;\n"
                                  "    -moz-border-radius:10px;\n"
                                  "}\n")
            self.detectBtn.setEnabled(True)
            self.detectBtn.setText("行为识别")
            self.detectBtn.setStyleSheet("QPushButton{\n"
                                         "    height:40px;\n"
                                         "    border:1px solid #4e6096;\n"
                                         "    background-color: rgb(155, 255, 189);\n"
                                         "    color:#2a2a2a;\n"
                                         # "    background-color:#61ddff;\n"
                                         "    font-family:\"微软雅黑\";\n"
                                         "    font-size:17px;\n"
                                         "    font-weight:bold;\n"
                                         "    -moz-border-radius:10px;\n"
                                         "}\n"
                                         "QPushButton:hover{\n"
                                         "    background-color:#2e9eff;\n"
                                         "    border:1px solid #1569bd;\n"
                                         "    color:#ecff3d;\n"
                                         "}")
            self.fps = self.original_video.get(cv2.CAP_PROP_FPS)
            frame_all = int(self.original_video.get(cv2.CAP_PROP_FRAME_COUNT))
            self.original_info = "视频信息：\n" + \
                                 "大小：" + str(self.first_frame.shape) + "\n" + \
                                 "总帧数：" + str(frame_all) + "\n" + \
                                 "时长：" + str(frame_all / self.fps) + "s\n" + \
                                 "路径：" + self.vidFilePath + '\n'
            self.add_trim_info()
            self.imgInfoLabel.setStyleSheet(
                # "QLabel{"
                # "font: 10pt \"微软雅黑\";"
                # "color: rgba(255, 255, 255, 0);"
                # "}"
                "QLabel{\n"
                "    color: rgb(255, 255, 0);\n"
                # "    color: rgb(220,20,60);\n"
                # "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, "
                "    background-color: rgb(0, 0, 0, 75);\n"
                # "stop:0.447761 rgba(0, 0, 0, 180), stop:0.99005 rgba(255, 0, 0, 0));"
                "font: 10pt \"微软雅黑\";"
                # "color: rgba(255, 255, 255);"
                # "    background-color: rgb(0, 0, 0, 125);\n"
                "}")
            self.imgInfoLabel2.setStyleSheet(
                # "QLabel{"
                # "font: 10pt \"微软雅黑\";"
                # "color: rgba(255, 255, 255, 0);"
                # "}"
                "QLabel{\n"
                # "    color: rgb(255, 255, 255);\n"
                # "    color: rgb(220,20,60);\n"
                "    color: rgb(255,255,0);\n"
                # "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, "
                "    background-color: rgb(0, 0, 0, 75);\n"
                # "stop:0.447761 rgba(0, 0, 0, 180), stop:0.99005 rgba(255, 0, 0, 0));"
                "font: 10pt \"微软雅黑\";"
                # "color: rgba(255, 255, 255);"
                # "    background-color: rgb(0, 0, 0, 125);\n"
                "}")

    # 控件解锁
    def set_control_unlock(self):
        if self.original_Image is not None and self.file_format in IMG_FORMATS:
            self.brightSlider.setEnabled(True)
            self.contrastSlider.setEnabled(True)
            self.saturatSlider.setEnabled(True)
            self.resetBtn.setEnabled(True)
            self.OcclusionBox.setText('图片调整')
            self.imgDisplayLaebl.setToolTip('双击可查看图像')
            self.original_info = "图像信息：\n" + \
                                 "图像大小：" + str(self.original_Image.size) + "\n" + \
                                 "图像格式：" + self.original_Image.format + "\n" + \
                                 "图像路径：" + self.imgFilePath + '\n'
            self.original_info = "图像大小：" + str(self.original_Image.size) + "\n" + \
                                 "图像格式：" + self.original_Image.format + "\n"

            self.add_trim_info()
            self.detectBtn.setText("行为识别")
            for btn in self.control_Enable:
                btn.setEnabled(True)
                btn.setStyleSheet("QPushButton{\n"
                                  "    height:40px;\n"
                                  "    border:1px solid #4e6096;\n"
                                  "    background-color: rgb(155, 255, 189);\n"
                                  "    color:#2a2a2a;\n"
                                  # "    background-color:#61ddff;\n"
                                  "    font-family:\"微软雅黑\";\n"
                                  "    font-size:17px;\n"
                                  "    font-weight:bold;\n"
                                  "    -moz-border-radius:10px;\n"
                                  "}\n"
                                  "QPushButton:hover{\n"
                                  "    background-color:#2e9eff;\n"
                                  "    border:1px solid #1569bd;\n"
                                  "    color:#ecff3d;\n"
                                  "}")
            self.imgInfoLabel.setStyleSheet(
                # "QLabel{"
                # "font: 10pt \"微软雅黑\";"
                # "color: rgba(255, 255, 255, 0);"
                # "}"
                                "QLabel{\n"
                "    color: rgb(255, 255, 0);\n"
                # "    color: rgb(220,20,60);\n"
                # "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, "
                "    background-color: rgb(0, 0, 0, 75);\n"
                # "stop:0.447761 rgba(0, 0, 0, 180), stop:0.99005 rgba(255, 0, 0, 0));"
                "font: 10pt \"微软雅黑\";"
                # "color: rgba(255, 255, 255);"
                # "    background-color: rgb(0, 0, 0, 125);\n"
                "}")
            self.imgInfoLabel2.setStyleSheet(
                # "QLabel{"
                # "font: 10pt \"微软雅黑\";"
                # "color: rgba(255, 255, 255, 0);"
                # "}"
                "QLabel{\n"
                # "    color: rgb(255, 255, 255);\n"
                # "    color: rgb(220,20,60);\n"
                "    color: rgb(255,255,0);\n"
                # "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, "
                "    background-color: rgb(0, 0, 0, 75);\n"
                # "stop:0.447761 rgba(0, 0, 0, 180), stop:0.99005 rgba(255, 0, 0, 0));"
                "font: 10pt \"微软雅黑\";"
                # "color: rgba(255, 255, 255);"
                # "    background-color: rgb(0, 0, 0, 125);\n"
                "}")

    # 图片调整信息
    def add_trim_info(self):
        try:
            info = "\n"
            info_det = ""
            if self.file_format in IMG_FORMATS:
                num1 = round((self.brightSlider.value() - 50) * 2, 1)
                num2 = round((self.saturatSlider.value() - 50) * 2, 1)
                num3 = round((self.contrastSlider.value() - 50) * 2, 1)
                add_or_sub_1 = '' if num1 == 0 else ('+' if num1 > 0 else '-')
                add_or_sub_2 = '' if num2 == 0 else ('+' if num2 > 0 else '-')
                add_or_sub_3 = '' if num3 == 0 else ('+' if num3 > 0 else '-')
                # info = "\n图像调整信息：" + "\n亮度调整： " + add_or_sub_1 + str(math.fabs(num1)) + "%" + "\n饱和度调整： " + \
                #        add_or_sub_2 + str(
                #     math.fabs(num2)) + "%""\n对比度调整： " + add_or_sub_3 + str(math.fabs(num3)) + "%"
                info = "\n亮度变化： " + add_or_sub_1 + str(math.fabs(num1)) + "%" + "\n饱和度变化： " + \
                       add_or_sub_2 + str(
                    math.fabs(num2)) + "%""\n对比度变化： " + add_or_sub_3 + str(math.fabs(num3)) + "%"
                if self.have_det:
                    info_det = info_det + f"检测时间：{self.result['time']:.3f}s"
                    info_det = info_det + "\n" + "检测数目：" + str(self.result['num'])
                    info_det = info_det + "\n" + "检测信息：" + str(self.result['info'])
            elif self.file_format in VID_FORMATS:
                if self.result:
                    info_det = info_det + f"检测时间：{self.result['time']:.3f}s"
                    info_det = info_det + "\n" + "检测数目：" + str(self.result['num'])
                    info_det = info_det + "\n" + "检测信息：" + str(self.result['info'])

            info_det = info_det + f"\n\n当前模型: {self.select_model}"
            self.imgInfoLabel.setText(self.original_info + info)
            self.imgInfoLabel2.setText(info_det)
        except Exception as ex:
            print(ex)

    # 滑动条设置事件
    def sliderEvent(self):
        self.brightSlider.valueChanged.connect(self.img_bright_event)
        self.saturatSlider.valueChanged.connect(self.img_saturat_event)
        self.contrastSlider.valueChanged.connect(self.img_contrast_event)

    # 滑动条重置
    def reset_slider(self):
        self.brightSlider.setSliderPosition(50)
        self.saturatSlider.setSliderPosition(50)
        self.contrastSlider.setSliderPosition(50)

    # 亮度事件
    def img_bright_event(self):
        try:
            value = (float)(self.brightSlider.value() / 50)
            if not self.have_det:
                bright_enhance = ImageEnhance.Brightness(self.original_Image)
            else:
                bright_enhance = ImageEnhance.Brightness(self.detect_Image)
            self.new_Image = bright_enhance.enhance(value)
            self.retain_other_two('bright')
            self.show_image(self.new_Image)
            self.add_trim_info()
        except Exception as ex:
            print(ex)

    # 饱和度事件
    def img_saturat_event(self):
        try:
            value = float(self.saturatSlider.value() / 50)
            if not self.have_det:
                bright_enhance = ImageEnhance.Color(self.original_Image)
            else:
                bright_enhance = ImageEnhance.Color(self.detect_Image)
            self.new_Image = bright_enhance.enhance(value)
            self.retain_other_two('saturat')
            self.show_image(self.new_Image)
            self.add_trim_info()
        except Exception as ex:
            print(ex)

    # 对比度事件
    def img_contrast_event(self):
        try:
            value = float(self.contrastSlider.value() / 50)
            if not self.have_det:
                bright_enhance = ImageEnhance.Contrast(self.original_Image)
            else:
                bright_enhance = ImageEnhance.Contrast(self.detect_Image)
            self.new_Image = bright_enhance.enhance(value)
            self.retain_other_two('constrast')
            self.show_image(self.new_Image)
            self.add_trim_info()
        except Exception as ex:
            print(ex)

    # 保留另外两种属性
    def retain_other_two(self, mode=''):
        try:
            value0 = float(self.brightSlider.value() / 50)
            value1 = float(self.saturatSlider.value() / 50)
            value2 = float(self.contrastSlider.value() / 50)
            if mode == 'bright':
                saturat_enhance = ImageEnhance.Color(self.new_Image)
                self.new_Image = saturat_enhance.enhance(value1)
                contrast_enhance = ImageEnhance.Contrast(self.new_Image)
                self.new_Image = contrast_enhance.enhance(value2)
            elif mode == 'saturat':
                bright_enhance = ImageEnhance.Brightness(self.new_Image)
                self.new_Image = bright_enhance.enhance(value0)
                contrast_enhance = ImageEnhance.Contrast(self.new_Image)
                self.new_Image = contrast_enhance.enhance(value2)
            elif mode == 'constrast':
                bright_enhance = ImageEnhance.Brightness(self.new_Image)
                self.new_Image = bright_enhance.enhance(value0)
                saturat_enhance = ImageEnhance.Color(self.new_Image)
                self.new_Image = saturat_enhance.enhance(value1)
            else:
                print("模式不正确")
        except Exception as ex:
            print(ex)
            print("retain_other_two： 保留另外两种属性错误")

    # Image转为QPixmap
    @staticmethod
    def PIL_to_QPixmap(image):
        try:
            pixmap = ImageQt.toqpixmap(image)
        except Exception as ex:
            print(ex)
            print("PIL_to_QPixmap:  图片格式转换错误（Image to QPixmap）")
        return pixmap

    # python3.7后PIL转qt使用该方式
    def pil_to_qt(self, image):
        image = self.PIL_to_cv2(image)
        # cv2.imshow("PIL_to_cv2", image)
        # cv2.waitKey(0)
        return self.cv2_to_qt(image)

    # 错误的cv2转qt的方法(原)
    @staticmethod
    def cv2_to_qt2(image):
        try:
            h, w, ch = image.shape
            bytesPerLine = ch * w
            disp_frame = QtGui.QImage(image.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
            return QPixmap.fromImage(disp_frame)
        except Exception as ex:
            print(ex)

    # 正确的cv2转qt的方法
    @staticmethod
    def cv2_to_qt(image):
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


    # 图片显示
    def show_image(self, image):
        try:
            if self.file_format in IMG_FORMATS:
                if image == self.original_Image:
                    self.origin_mode()
                else:
                    self.new_mode()
                # self.imgDisplayLaebl.setPixmap(self.PIL_to_QPixmap(image=image))
                self.imgDisplayLaebl.setPixmap(self.pil_to_qt(image=image))
            elif self.file_format in VID_FORMATS:
                self.imgDisplayLaebl.setPixmap(self.cv2_to_qt(image))
        except Exception as ex:
            print(ex)

    # 获取诗句
    def get_poetry(self, poetry_txt="./Images/poetry.txt"):
        try:
            with open(poetry_txt, 'r', encoding='utf-8') as fp:
                self.poetry_list = fp.readlines()
        except Exception as ex:
            print(ex)

    # 获取背景图
    def get_background_img_path(self, img_dir='./Images'):
        try:
            if os.path.exists(img_dir):
                file_list = os.listdir(path=img_dir)
                for i in file_list:
                    fm = i.split(".")[-1]
                    path = img_dir + '/' + i
                    if os.path.isfile(path) and fm in IMG_FORMATS:
                        self.img_list.append(path)
        except Exception as ex:
            print(ex)

    # 展示当前时间
    def show_currentTime(self):
        self.Timer = QTimer()
        self.Timer.timeout.connect(self.timer_time_timeout)
        self.Timer.start()

    # 时间事件
    def timer_time_timeout(self):
        datetime = QDateTime.currentDateTime()
        text = datetime.toString('yyyy-MM-dd hh:mm:ss dddd')
        self.timeLabel.setText(text)

    # 轮播图
    def carousel_img(self):
        self.timer_ = QTimer(self)
        self.timer_.timeout.connect(self.timer_img_timeout)
        if self.static_pic:
            return
        self.timer_.start(self.carousel_time)

    # 轮播图事件
    def timer_img_timeout(self):
        try:
            path = self.img_list[self.imgIndex]
            self.backgroundImg.setPixmap(QPixmap(path))

            self.timer2 = QTimer()
            t = (self.carousel_time / 2) / (1 / math.fabs(self.degree))
            self.timer2.start(int(t))
            self.timer2.timeout.connect(self.gradual_change_timeout)
            cv2.waitKey(100)

            path2 = self.img_list[self.nextIndex]
            self.backgroundImg2.setPixmap(QPixmap(path2))

            self.poetryText.setText(self.poetry_list[self.nextIndex])
            self.imgIndex = self.nextIndex
            if self.img_play_random:
                idx = random.randint(0, len(self.img_list) - 1)
                while idx is self.nextIndex:
                    idx = random.randint(0, len(self.img_list) - 1)
                self.nextIndex = idx
            else:
                self.nextIndex = (self.nextIndex + 1) % len(self.img_list)
        except Exception as ex:
            print(ex)

    # 轮播图淡入淡出效果
    def gradual_change_timeout(self):
        try:
            if self.counter <= 1:
                self.counter += self.degree
                op = QtWidgets.QGraphicsOpacityEffect()
                op.setOpacity(abs(self.counter))
                self.backgroundImg.setGraphicsEffect(op)
            if self.counter < 0:
                self.counter = 1
                self.timer2.stop()
        except Exception as ex:
            print(ex)

    # 图片宽高比例过大不采用自适应
    # def img_adaption(self):
    #     radio = self.original_Image.width / self.original_Image.height
    #     print(radio)
    #     if radio > 0.6 and radio < 1.8:
    #         self.imgDisplayLaebl.setScaledContents(True)
    #     else:
    #         self.imgDisplayLaebl.setScaledContents(False)

    # 选择文件
    def chooseFile(self, filename=""):
        try:
            if filename == "":
                file = QFileDialog.getOpenFileName(self, "请选择一张图片", "./image",
                                                   self.file_support)
                if file[0] == '':
                    return
                filename = file[0]
            filename = '/'.join(filename.split('\\'))
            self.chooseImgPath = filename
            det.img_name = filename
            print("[test...] filename=> ",filename)

            files = self.conf['recent_files']
            if filename in files:
                files.remove(filename)
            if len(files) >= self.max_recent_files:
                self.conf['recent_files'].pop(0)
            files.append(filename)
            # self.add_recent_files(filename)
            self.parse_recent_files()

            self.file_format = filename.split('.')[-1]
            self.have_det = False

            if self.file_format in IMG_FORMATS:
                self.video_type = 'detect'
                # 将图片新状态设为未调整
                if self.haveImage:
                    self.new_Image = None
                # 重置滑动条
                self.reset_slider()
                self.imgFilePath = filename
                self.original_Image = Image.open(self.imgFilePath)
                w, h = self.original_Image.size[0], self.original_Image.size[1]
                self.image_radio = w / h

                self.haveImage = True

                self.set_control_unlock()
                self.show_image(self.original_Image)

            elif self.file_format in VID_FORMATS:
                self.vidFilePath = filename
                self.original_video = cv2.VideoCapture(self.vidFilePath)
                _, self.first_frame = self.original_video.read()
                self.image_radio = self.first_frame.shape[1] / self.first_frame.shape[0]
                self.set_control_lock()
                self.show_image(self.first_frame)
            self.set_label_geometry()
        except Exception as ex:
            print(ex)

    # 进入图片调整层界面
    def run_balance(self):
        # 创建界面对象必须放在此函数中，否则界面中的值无法刷新
        try:
            self.banlanceUI = balanceUIController()
            if self.have_det:
                self.banlanceUI.original_image = self.original_Image
            else:
                if self.new_Image is not None:
                    self.banlanceUI.original_image = self.new_Image
                else:
                    self.banlanceUI.original_image = self.original_Image
            self.banlanceUI.init_ui()
            self.banlanceUI.start_ui()
            self.banlanceUI.signal.connect(self.get_final_image)
            self.banlanceUI.show()
        except Exception as ex:
            print(ex)

    def music_change_event(self, context):
        value = float(context) / self.musicRadio
        # pygame.mixer.music.set_volume(value)

    def music_open_close_event(self, context):
        if context == '':
            self.on_musicBtn_clicked()

    def last_music_event(self, context):
        if context == '':
            try:
                self.musicIndex -= 1
                if math.fabs(self.musicIndex) == len(self.music_list):
                    self.musicIndex = 0
                name = self.music_list[self.musicIndex]
                name = name.split(os.sep)[-1]
                name = name[0:name.rfind('.')]
                self.setUI.musicName.setText(name)
                path = self.music_list[self.musicIndex]
                # pygame.mixer.music.stop()
                # pygame.mixer.music.load(path)
                # pygame.mixer.music.play()
            except Exception as ex:
                print(ex)
                print("切换下首歌失败")

    def next_music_event(self, context):
        if context == '':
            try:
                self.musicIndex += 1
                if self.musicIndex == len(self.music_list):
                    self.musicIndex %= len(self.music_list)
                name = self.music_list[self.musicIndex]
                name = name.split(os.sep)[-1]
                name = name[0:name.rfind('.')]
                self.setUI.musicName.setText(name)
                path = self.music_list[self.musicIndex]
                # pygame.mixer.music.stop()
                # pygame.mixer.music.load(path)
                # pygame.mixer.music.play()
            except Exception as ex:
                print(ex)
                print("切换上首歌失败")

    def static_pic_event(self, context):
        if context == 'yes':
            self.timer_.stop()
        elif context == 'no':
            self.timer_.start(5000)

    def pic_mask_event(self, context):
        if context == 'yes':
            self.pic_mask.setStyleSheet("background-color: rgba(0, 0, 0, 125);")
        elif context == 'no':
            self.pic_mask.setStyleSheet("background-color: rgba(0, 0, 0, 0);")

    def video_type_event(self, context):
        self.video_type = context

    def imgLab_adapt_event(self, context):
        if context == "yes":
            self.imgLab_adapt = True
        elif context == "no":
            self.imgLab_adapt = False
        self.set_label_geometry()
        if self.videoUI is not None:
            self.videoUI.imgLab_adapt = self.imgLab_adapt
            self.videoUI.set_label_geometry()

    def win_adapt_event(self, context):
        if context == "yes":
            self.win_adapt = True
        elif context == "no":
            self.win_adapt = False

    @pyqtSlot()
    def on_setBtn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        try:
            try:
                name = self.music_list[self.musicIndex]
                name = name[9:name.rfind('.')]
                self.setUI.musicName.setText(name)
            except Exception as ex:
                print(ex)
            self.setUI.start_ui()
            self.setUI.signal_musicSlider.connect(self.music_change_event)
            self.setUI.signal_music_Box.connect(self.music_open_close_event)
            self.setUI.signal_last_music.connect(self.last_music_event)
            self.setUI.signal_next_music.connect(self.next_music_event)
            self.setUI.signal_static_pic_Box.connect(self.static_pic_event)
            self.setUI.signal_pic_mask_Box.connect(self.pic_mask_event)
            self.setUI.signal_video_type.connect(self.video_type_event)
            self.setUI.signal_imgLab_adapt.connect(self.imgLab_adapt_event)
            self.setUI.signal_win_adapt.connect(self.win_adapt_event)
        except Exception as ex:
            print(ex)

    @pyqtSlot()
    def on_helpBtn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.helpUI = helpUIController()

    # 重置
    @pyqtSlot()
    def on_resetBtn_clicked(self):
        """
                Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.reset_slider()
        if not self.have_det:
            self.new_Image = None
            self.show_image(self.original_Image)
        else:
            self.show_image(self.detect_Image)

    # 音乐
    @pyqtSlot()
    def on_musicBtn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        try:
            if self.isMusicPlay:
                # pygame.mixer.music.pause()
                self.isMusicPlay = False
                icon_ = QtGui.QIcon()
                icon_.addPixmap(QtGui.QPixmap("./Icons/music_no2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.musicBtn.setIcon(icon_)
            else:
                # pygame.mixer.music.unpause()
                self.isMusicPlay = True
                icon__ = QtGui.QIcon()
                icon__.addPixmap(QtGui.QPixmap("./Icons/music.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.musicBtn.setIcon(icon__)
        except Exception as ex:
            print(ex)

    # 调整
    @pyqtSlot()
    def on_balanceBtn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.run_balance()

    # 选择文件
    @pyqtSlot()
    def on_selectBtn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.chooseFile()

    # 保存图像
    @pyqtSlot()
    def on_saveBtn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        save_image_name = QFileDialog.getSaveFileName(self, "save image", "./output/", "image files(*.jpg)")[0]
        if save_image_name == '':
            return
        if self.new_Image is not None:
            save_img = self.new_Image
        else:
            save_img = self.original_Image
        save_img.save(save_image_name)

    # 效果图
    @pyqtSlot()
    def on_effectBtn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if self.new_Image is not None:
            # print("[test...] type(new_Image)=>",self.new_Image)
            self.show_image(self.new_Image)

    # 原图
    @pyqtSlot()
    def on_originBtn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # print("[test...] type(original_Image)=>", self.original_Image)
        self.show_image(self.original_Image)

    # 加载模型
    # 可不用此方法
    def load_model(self):
        try:
            if self.video_type == 'track':
                import qtTrack
                self.tracker = qtTrack.get_detector(model=self.select_model)
            else:
                self.detector = get_detector(model=self.select_model)
        except Exception as ex:
            print(ex)

    # 检测
    @pyqtSlot()
    def on_detectBtn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        try:
            print(self.select_model)
            if (self.detector is None and self.video_type == 'detect') or (
                    self.tracker is None and self.video_type == 'track'):
                self.imgDisplayLaebl2.setVisible(True)
                cv2.waitKey(100)
                # 开启线程加载模型，防止程序卡顿
                thread = threading.Thread(target=self.load_model)
                thread.start()
                num = 1
                string = "模型正在加载，请等待"
                while True:
                    if self.detector is not None and self.video_type == 'detect':
                        break
                    if self.tracker is not None and self.video_type == 'track':
                        break
                    self.imgDisplayLaebl2.setText(string[0:num % len(string) + 1])
                    cv2.waitKey(250)
                    num += 1
                    if num >= 60:
                        self.imgDisplayLaebl2.setText("模型加载失败！")
                        cv2.waitKey(500)
                        self.imgDisplayLaebl2.setText("可以尝试切换模型")
                        cv2.waitKey(1000)
                        self.imgDisplayLaebl2.setText("")
                        self.imgDisplayLaebl2.setVisible(False)
                        # self.close()
                        # stop_thread(thread)
                        return
                if num < 60:
                    print("模型加载完成")
                    self.imgDisplayLaebl2.setText("模型加载完成")

                cv2.waitKey(200)
                self.imgDisplayLaebl2.setVisible(False)

            if self.file_format in IMG_FORMATS:
                if self.new_Image is None:
                    image = self.original_Image
                else:
                    if not self.have_det:
                        image = self.new_Image
                    else:
                        image = self.original_Image
                if self.new_Image is not None and self.have_det is False:
                    self.original_Image = self.new_Image
                # print("[test...] ",image )
                # here
                # result = self.detector.run(image=self.PIL_to_cv2(image))
                result = self.detector.run(image_name=self.chooseImgPath)
                self.result = result
                self.have_det = True
                det_img = result['image']
                self.result['time'] = round(result['time'], 3)
                self.add_trim_info()

                # cv2显示检测结果看看 (此时det确实是cv2的格式)
                # cv2.imshow("det_img", det_img)
                # cv2.waitKey(0)

                self.detect_Image = self.cv2_to_PIL(det_img)
                # PIL显示检测结果看看 (此时detect_Image确实是PIL的格式)
                # self.detect_Image.show()

                self.reset_slider()
                self.new_Image = self.detect_Image
                self.show_image(self.new_Image)
                self.actionSave.setEnabled(True)
            elif self.use_video and not self.have_det and self.vidFilePath != "" and self.file_format in VID_FORMATS:
                self.detectBtn.setEnabled(False)
                self.selectBtn.setEnabled(False)
                self.actionSave.setEnabled(False)
                self.have_det = True
                self.frame_list.clear()
                self.frame_info.clear()
                cap = self.original_video
                if self.show_in_cvWin:
                    cv2.namedWindow('video', cv2.WINDOW_KEEPRATIO)
                    shape = self.first_frame.shape
                    cv2.resizeWindow('video', 1200, 675)
                    if shape[0] > shape[1]:
                        cv2.resizeWindow('video', 630, 1120)
                while True:
                    _, img = cap.read()
                    if not _:
                        break
                    if self.video_type == 'track':
                        self.result = self.tracker.run(image=img)
                    elif self.video_type == 'detect':
                        self.result = self.detector.run(image=img)
                    self.frame_list.append(self.result['image'])
                    self.save_frame_info()
                    self.add_trim_info()
                    if self.show_in_cvWin:
                        cv2.imshow('video', self.result['image'])
                        if cv2.waitKey(1) == ord('q'):  # q to quit
                            raise StopIteration
                    else:
                        self.show_image(self.result['image'])
                        cv2.waitKey(int(1000 / self.fps / 5))
                self.detectBtn.setText("视频结果")
                self.detectBtn.setEnabled(True)
                self.selectBtn.setEnabled(True)
            else:
                from qt.videoUIController import videoUIController
                result2 = {'frame_list': self.frame_list, 'frame': int(self.fps), 'frame_info': self.frame_info}
                self.videoUI = videoUIController(result2, imgLab_adapt=self.imgLab_adapt)
                self.videoUI.start_ui()
        except Exception as ex:
            print(ex)

    @pyqtSlot()
    def on_actionOpen_triggered(self):
        self.chooseFile()

    @pyqtSlot()
    def on_actionSave_triggered(self):
        self.on_saveBtn_clicked()

    @pyqtSlot()
    def on_actionQuit_triggered(self):
        self.close()

    @pyqtSlot()
    def on_actionHelp_triggered(self):
        self.on_helpBtn_clicked()

    def set_action_True(self, action):
        for model in self.model_list:
            if model == action:
                action.setChecked(True)
            else:
                model.setChecked(False)
        self.add_trim_info()

    @pyqtSlot()
    def on_yolov5s_triggered(self):
        if self.select_model == "yolov5s":
            return
        else:
            self.select_model = "yolov5s"
            self.clear_cache()
        self.set_action_True(self.actionYolov5s)

    @pyqtSlot()
    def on_yolov5l_triggered(self):
        if self.select_model == "yolov5l":
            return
        else:
            self.select_model = "yolov5l"
            self.clear_cache()
        self.set_action_True(self.actionYolov5l)

    @pyqtSlot()
    def on_yolov5m_triggered(self):
        if self.select_model == "yolov5m":
            return
        else:
            self.select_model = "yolov5m"
            self.clear_cache()
        self.set_action_True(self.actionYolov5m)

    @pyqtSlot()
    def on_yolov5x_triggered(self):
        if self.select_model == "yolov5x":
            return
        else:
            self.select_model = "yolov5x"
            self.clear_cache()
        self.set_action_True(self.actionYolov5x)

    # 保存帧信息
    def save_frame_info(self):
        try:
            info = "\n" + f"检测时间：{self.result['time']:.3f}s"
            info = info + "\n" + "检测数目：" + str(self.result['num'])
            info = info + "\n" + "检测信息：" + str(self.result['info'])
            self.frame_info.append(info)
        except Exception as ex:
            print(ex)

    # PIL转cv2
    @staticmethod
    def PIL_to_cv2(image):
        try:
            return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        except Exception as ex:
            print(ex)
            return cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2BGRA)

    # cv2转PIL
    @staticmethod
    def cv2_to_PIL(image):
        try:
            return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        except Exception as ex:
            print(ex)
            return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA))

    # 保留相关配置信息
    def save_conf(self):
        try:
            self.conf['imgDir'] = self.imgDir
            self.conf['poetryPath'] = self.poetryPath
            self.conf['img_play_random'] = self.img_play_random
            self.conf['max_recent_files'] = self.max_recent_files
            self.conf['use_img_mask'] = self.use_img_mask
            self.conf['musicPath'] = self.musicPath
            self.conf['musicPackage'] = self.musicPackage
            self.conf['isMusicPlay'] = self.isMusicPlay
            self.conf['autoMusicPlay'] = self.autoMusicPlay

            self.conf['video_type'] = self.video_type
        except Exception as ex:
            print(ex)

    # 鼠标单击事件
    def mousePressEvent(self, event):
        self.pos = event.pos()
        self.mouse_press_handle()

    # 鼠标双击事件
    def mouseDoubleClickEvent(self, event):
        self.pos = event.pos()
        self.mouse_double_handle()

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        self.pos = event.pos()
        self.mouse_move_handle()

    # 移动事件处理
    def mouse_move_handle(self):
        try:
            if self.pos is None:
                return
            x = self.pos.x()
            y = self.pos.y()
            control_x = self.OcclusionBox.x()
            control_y = self.OcclusionBox.y()
            control_width = self.OcclusionBox.width()
            control_height = self.OcclusionBox.height()
            if control_x < x < control_x + control_width and \
                    control_y < y < control_y + control_height:
                self.OcclusionBox.setStyleSheet("background-color: rgb(0, 0, 0, 125);color: rgb(255, 255, 255, 255);")
            else:
                self.OcclusionBox.setStyleSheet("background-color: rgb(0, 0, 0, 0);color: rgb(255, 255, 255, 0);")
        except Exception as ex:
            print(ex)

    # 单击事件处理
    def mouse_press_handle(self):
        try:
            if self.pos is None:
                return
            x = self.pos.x()
            y = self.pos.y()
            control_x = self.imgDisplayLaebl.x()
            control_y = self.imgDisplayLaebl.y()
            control_width = self.imgDisplayLaebl.width()
            control_height = self.imgDisplayLaebl.height()

            if control_x < x < control_x + control_width and \
                    control_y < y < control_y + control_height:
                if self.original_Image is None:
                    self.chooseFile()
        except Exception as ex:
            print(ex)

    # 双击事件处理
    def mouse_double_handle(self):
        try:
            x = self.pos.x()
            y = self.pos.y()
            control_x = self.imgDisplayLaebl.x()
            control_y = self.imgDisplayLaebl.y()
            control_width = self.imgDisplayLaebl.width()
            control_height = self.imgDisplayLaebl.height()
            if control_x < x < control_x + control_width and \
                    control_y < y < control_y + control_height:
                if self.haveImage:
                    if self.new_Image is not None:
                        self.new_Image.show()
                    else:
                        self.original_Image.show()
        except Exception as ex:
            print(ex)

    # 图显窗口自适应图像
    def set_label_geometry(self):
        try:
            if self.file_format == '' or not self.imgLab_adapt:
                x = self.leftMargin
                y = self.topMargin
                w = self.current_width - self.rightMargin - x
                h = self.current_height - self.bottomMargin - y
                self.imgDisplayLaebl.setGeometry(QtCore.QRect(x, y, w, h))
                self.imgDisplayLaebl2.setVisible(True)
                # self.imgDisplayLaebl2.setGeometry(QtCore.QRect(x, y, w, h))
            elif self.imgLab_adapt:
                lefts = self.leftMargin
                tops = self.topMargin
                rights = self.current_width - self.rightMargin
                bottoms = self.current_height - self.bottomMargin

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

                self.imgDisplayLaebl.setGeometry(QtCore.QRect(x, y, w, h))
                self.imgDisplayLaebl2.setVisible(True)
                # self.imgDisplayLaebl2.setGeometry(QtCore.QRect(x, y, w, h))
        except Exception as ex:
            print(ex)

    def resizeEvent(self, event):
        # print("w = {0}; h = {1}".format(event.size().width(), event.size().height()))
        try:
            if not self.win_adapt:
                self.resize(self.current_width, self.current_height)
                return
            self.current_width = event.size().width()
            self.current_height = event.size().height()
            self.backgroundImg.setGeometry(QtCore.QRect(0, 0, int(self.current_width), int(self.current_height)))
            self.backgroundImg2.setGeometry(QtCore.QRect(0, 0, int(self.current_width), int(self.current_height)))
            self.pic_mask.setGeometry(QtCore.QRect(0, 0, int(self.current_width), int(self.current_height)))

            width_change = self.current_width - self.width
            height_change = self.current_height - self.height

            # 底层按钮位置调整
            bottomBtn_list = [self.selectBtn, self.balanceBtn, self.detectBtn, self.originBtn, self.effectBtn,
                              self.saveBtn]

            bottomMargin = 61
            btnInterval = 20

            cx = self.leftMargin + (self.current_width - self.rightMargin - self.leftMargin) / 2
            length = len(bottomBtn_list) * self.saveBtn.width() + (len(bottomBtn_list) - 1) * btnInterval
            begin = cx - length / 2
            width, height = self.saveBtn.width(), self.saveBtn.height()

            for idx, btn in enumerate(bottomBtn_list):
                x = int(begin + idx * (width + btnInterval))
                y = int(self.current_height - bottomMargin - height)
                w, h = width, height
                btn.setGeometry(QtCore.QRect(x, y, w, h))

            # 时间框位置调整
            x = self.current_width - 42 - self.timeLabel.width()
            y = self.current_height - 35 - self.timeLabel.height()
            self.timeLabel.move(x, y)

            # 顶部按钮位置调整
            topBtn_list = [self.setBtn, self.musicBtn, self.helpBtn]

            for idx, btn in enumerate(topBtn_list):
                x = width_change + 830 + idx * 50
                y = 20
                btn.setGeometry(QtCore.QRect(x, y, btn.width(), btn.height()))

            # 顶部语句标签
            self.poetryText.setGeometry(QtCore.QRect(30, 30, 700, 21))

            # 底部滑动条区调整
            self.brightLabel.setGeometry(QtCore.QRect(40, height_change + 600, 50, 16))
            self.saturatLabel.setGeometry(QtCore.QRect(40, height_change + 650, 50, 15))
            self.contrastLabel.setGeometry(QtCore.QRect(40, height_change + 700, 50, 15))
            self.brightSlider.setGeometry(QtCore.QRect(110, height_change + 600, 160, 22))
            self.saturatSlider.setGeometry(QtCore.QRect(110, height_change + 650, 160, 22))
            self.contrastSlider.setGeometry(QtCore.QRect(110, height_change + 700, 160, 22))
            self.resetBtn.setGeometry(QtCore.QRect(120, height_change + 730, 61, 28))
            self.OcclusionBox.setGeometry(QtCore.QRect(30, height_change + 570, 251, 161))
            self.logo.setGeometry(QtCore.QRect(10, height_change + 720, 60, 45))

            self.set_label_geometry()
            QtWidgets.QWidget.resizeEvent(self, event)
        except Exception as ex:
            print(ex)

    # 关闭窗口
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'warning', '您确定要退出吗？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # self.save_conf()   # 保存配置
            try:
                with open('./conf/conf.yaml', 'w') as fw:
                    yaml.dump(self.conf, fw, default_flow_style=False, encoding='utf-8', allow_unicode=True)
            except Exception as ex:
                print(ex)
            tmp_image_dir = basepath + '/.tmp_pic'  # 临时保存数据增广后的结果
            print("[delete...] tmp_image_dir=>", tmp_image_dir)
            if os.path.exists(tmp_image_dir):
                shutil.rmtree(tmp_image_dir)
            self.clear_cache()
            # pygame.mixer.music.stop()
            self.timer_music.stop()
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainUI = MainUIController()
    sys.exit(app.exec_())
