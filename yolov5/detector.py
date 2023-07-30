import argparse
import torch.backends.cudnn as cudnn
from utils import google_utils
from utils.datasets import *
from utils.utils import *
from flask import Flask, request, jsonify
import numpy as np
import os
import time
import json
import sys

# print(sys.path)
basepath = os.path.dirname(__file__)


class YOLOv5(object):
    def __init__(
            self,
            save_img=False,
            img_name='000001.jpg',
            ip_port='http://mnjpb6.natappfree.cc/',
            o_weights=r"F:\02software\yolov5\weights\yolov5s_pig.pt",
            o_source="static/images/upload",
            o_output="static/images/results",
            o_img_size=640,
            o_conf_thres=0.25,
            o_iou_thres=0.45,
            o_fourcc="mp4v",
            o_device='',
            o_view_img=False,
            o_save_txt=False,
            o_classes=None,
            o_agnostic_nms=False,
            o_augment=False):

        # net definition
        self.save_img = save_img,
        self.img_name = img_name,
        self.ip_port = ip_port,
        self.ip_port = self.ip_port[0]
        # print("parameter_ip=>", ip_port)
        print("[test...]init_ip=>", self.ip_port)
        self.o_weights = o_weights,
        self.o_source = o_source,
        self.o_output = o_output,
        self.o_img_size = o_img_size,
        self.o_conf_thres = o_conf_thres,
        self.o_iou_thres = o_iou_thres,
        self.o_fourcc = o_fourcc,
        self.o_device = o_device,
        self.o_device = self.o_device[0]
        # print('[test...] self.o_device=>',self.o_device)
        self.o_view_img = o_view_img,
        self.o_save_txt = o_save_txt,
        self.o_classes = o_classes,
        self.o_agnostic_nms = o_agnostic_nms,
        self.o_augment = o_augment

        # 初始化
        device = torch_utils.select_device(self.o_device)
        self.model = None
        if self.model == None:
            google_utils.attempt_download(o_weights)
            self.model = torch.load(o_weights, map_location=device)['model'].float()  # load to FP32
            # self.model = model

    def __call__(self, ori_img):
        pass

    def test(self):
        print(self.model)

    def detect(
            self,
            save_img=False,
            o_weights=basepath + r"/weights/yolov5s_pig.pt",
            o_source="static/images/upload",
            o_output="static/images/results",
            o_img_size=640,
            o_conf_thres=0.25,
            o_iou_thres=0.45,
            o_fourcc="mp4v",
            o_device='',
            o_view_img=False,
            o_save_txt=False,
            o_classes=None,
            o_agnostic_nms=False,
            o_augment=False):
        print("[notice...]start detect...")
        p = ''
        c1 = (0, 0)
        c2 = (0, 0)
        label_no_value = ''
        detection_result_list = []
        out, source, weights, view_img, save_txt, imgsz = \
            o_output, o_source, o_weights, o_view_img, o_save_txt, o_img_size
        webcam = source == '0' or source.startswith('rtsp') or source.startswith('http') or source.endswith('.txt')

        # 初始化
        device = torch_utils.select_device(o_device)
        # if os.path.exists(out):
        #     shutil.rmtree(out)  # delete output folder
        # os.makedirs(out)  # make new output folder
        if not os.path.exists(out):
            os.makedirs(out)  # make new output folder
        half = device.type != 'cpu'  # half precision only supported on CUDA

        model = self.model
        # 读取模型
        if model == None:
            google_utils.attempt_download(weights)
            model = torch.load(weights, map_location=device)['model'].float()  # load to FP32
            self.model = model
        # torch.save(torch.load(weights, map_location=device), weights)  # update model if SourceChangeWarning
        # model.fuse()
        model.to(device).eval()
        imgsz = check_img_size(imgsz, s=model.model[-1].stride.max())  # check img_size
        if half:
            model.half()  # to FP16

        # 两步分类器
        classify = False
        if classify:
            modelc = torch_utils.load_classifier(name='resnet101', n=2)  # initialize
            modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model'])  # load weights
            modelc.to(device).eval()
        # print("Opssssssssssssssssssss")
        # 设定数据读取器
        vid_path, vid_writer = None, None
        # 如果是摄像头的视频流
        if webcam:
            view_img = True
            cudnn.benchmark = True  # set True to speed up constant image size inference
            dataset = LoadStreams(source, img_size=imgsz)
        # 普通来源
        else:
            save_img = True
            dataset = LoadImages(source, img_size=imgsz)
            # print("source ->", source)
        # 获取类名和颜色
        names = model.module.names if hasattr(model, 'module') else model.names
        colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]

        # 运行推断
        t0 = time.time()
        img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # 初始化图像，[1,3,x,x]的张量流
        _ = model(img.half() if half else img) if device.type != 'cpu' else None  # 运行一次
        for path, img, im0s, vid_cap in dataset:
            img = torch.from_numpy(img).to(device)
            img = img.half() if half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # 推断
            t1 = torch_utils.time_synchronized()
            pred = model(img, augment=o_augment)[0]

            # 请求NMS
            # print("-----------====================",opt.augment)
            pred = non_max_suppression(pred, o_conf_thres, o_iou_thres, classes=o_classes, agnostic=o_agnostic_nms)
            t2 = torch_utils.time_synchronized()

            # 请求分类
            if classify:
                pred = apply_classifier(pred, modelc, img, im0s)

            # 处理推断结果
            for i, det in enumerate(pred):  # 每张图片的推断结果
                if webcam:  # batch_size >= 1
                    p, s, im0 = path[i], '%g: ' % i, im0s[i].copy()
                else:
                    p, s, im0 = path, '', im0s
                    # p ---------------------------------------------------------------------------------------------------------> 单张图片路径
                    # print("p111-> ", p)
                # cv2.imshow("show", im0)
                # c = cv2.waitKey(0)
                # 图像存储路径
                # save_path = str(Path(out) / Path(p).name)
                # 文本结果存储路径
                # txt_path = str(Path(out) / Path(p).stem) + ('_%g' % dataset.frame if dataset.mode == 'video' else '')
                # 输出字符串
                # s += '%gx%g ' % img.shape[2:]  # 打印 图像尺寸
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # 归一化 获得 whwh
                # 如果存在检测结果
                lab = []
                loc = []
                data = {}
                info = []
                data["identifier"] = "identifier"

                try:
                    data["counts"] = len(det)
                except:
                    print("\n[test...] don't find pig!")
                    data["counts"] = 0

                data["code"] = 200
                if det is not None and len(det):
                    # 重新缩放框从img_size到im0的尺寸
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
                    # 打印结果
                    # for c in det[:, -1].unique():
                    #     n = (det[:, -1] == c).sum()  # 推断每一类
                    # s += '%g %ss, ' % (n, names[int(c)])  # 加到输出串里面个数 标签
                    # s  = 'sssssaaaaassssaaaa %s' % ("asdffdsfsdfsfsf")
                    print("\n[show results]...\n")
                    # 写出结果
                    for *xyxy, conf, cls in det:
                        label = '%s: %.2f' % (names[int(cls)], conf)
                        label_no_value = '%s' % (names[int(cls)])
                        confidences_value = '%.2f' % (conf)
                        c1, c2 = plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=3)
                        print(c1, c2,
                              label_no_value)  # --------------------------------------------------------------------------------------->坐标 标签
                        # detection_result_list.append(p,c1,c2,label_no_value)
                        text = label
                        text_inf = text + ' ' + '(' + str(c1[0]) + ',' + str(c1[1]) + ')' + ' ' + '宽:' + str(
                            c2[0] - c1[0]) + '高:' + str(c2[1] - c1[1])
                        info.append({"label": names[int(cls)], "confidences": confidences_value})
                        loc.append([c1[0], c1[1], c2[0] - c1[0], c2[1] - c1[1]])
                        lab.append(text_inf)
                    # for *xyxy, conf, cls in det:
                    #     if save_txt:  # 写到文件
                    #         xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # 归一化 xywh
                    #         with open(txt_path + '.txt', 'a') as f:
                    #             f.write(('%g ' * 5 + '\n') % (cls, *xywh))  # 格式化标签
                    #     if save_img or view_img:  # 把框画到图像上
                    #         label = '%s %.2f' % (names[int(cls)], conf)
                    #         plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=3)
                # im0为检测图片
                # cv2.imshow("show", im0)
                # c = cv2.waitKey(0)

                # 检测结果写到的目录
                # cv2.imwrite(os.path.join(basepath, set_result_path, filename_ + '_res.jpg'), img)
                print()
                print("[test..] self.img_name=>", self.img_name)
                if '.' not in self.img_name:
                    self.img_name = self.img_name + '.jpg'
                # 为了效率，进行简单的图片压缩
                cv2.imwrite(os.path.join(basepath + r'/static/images/results', self.img_name), im0,
                            [cv2.IMWRITE_JPEG_QUALITY, 50])

                data['data'] = info
                # print("self.img_name=>",self.img_name)
                # print("self.ip_port=>", self.ip_port)
                data['resName'] = self.ip_port + 'results/' + self.img_name
                print("[test...]data=>", data)
                # data['det_img'] = im0
                # print(type(im0))
                res = jsonify(data)
                # print(res)
                # 打印时间 (推断时间 + NMS)
                # print('%sDone. (%.3fs)' % (s, t2 - t1))

                # # 视频流的结果
                # if view_img:
                #     #返回实时检测结果
                #     cv2.imshow(p, im0)
                #     if cv2.waitKey(1) == ord('q'):  # q to quit
                #         raise StopIteration

                # # 保存结果 (推断后的图像)
                # if save_img:
                #     if dataset.mode == 'images':
                #         cv2.imwrite(save_path, im0)
                #     else:
                #         if vid_path != save_path:  # 新的视频
                #             vid_path = save_path
                #             if isinstance(vid_writer, cv2.VideoWriter):
                #                 vid_writer.release()  # 释放上一个视频编写器句柄

                #             fps = vid_cap.get(cv2.CAP_PROP_FPS)
                #             w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                #             h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                #             vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*opt.fourcc), fps, (w, h))
                #         vid_writer.write(im0)
        # print(detection_result_list)
        return lab, im0, loc, res

    # if save_txt or save_img:
    #     print('Results saved to %s' % os.getcwd() + os.sep + out)
    #     if platform == 'darwin':  # MacOS
    #         os.system('open ' + save_path)
    # print('Done. (%.3fs)' % (time.time() - t0))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', type=str, default='weights/yolov5s.pt', help='model.pt path')
    parser.add_argument('--source', type=str, default='static/images/upload',
                        help='source')  # file/folder, 0 for webcam
    parser.add_argument('--output', type=str, default='static/images/results', help='output folder')  # output folder
    parser.add_argument('--img-size', type=int, default=640, help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float, default=0.4, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.5, help='IOU threshold for NMS')
    parser.add_argument('--fourcc', type=str, default='mp4v', help='output video codec (verify ffmpeg support)')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='display results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    opt = parser.parse_args()
    YOLOv5().test()
# Update all models
# for opt.weights in ['yolov5s.pt', 'yolov5m.pt', 'yolov5l.pt', 'yolov5x.pt', 'yolov3-spp.pt']:
#     detect()
#     create_pretrained(opt.weights, opt.weights)
