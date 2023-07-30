# import onnx
# import onnxruntime as ort
# import numpy as np
import random
import sys
import time

import onnx
import onnxruntime as ort
import cv2
import numpy as np
from flask import jsonify
import os

from utils import scale_coords, plot_one_box

CLASSES = ['drink', 'stand', 'lie']  # 3个行为类别
# basepath为项目的路径
basepath = os.path.dirname(__file__)


class Yolov5ONNX(object):
    # def __init__(self, img_name='000001.jpg', ip_port= 'http://mnjpb6.natappfree.cc/' ,onnx_path="weights/yolov5s_pig_origin.onnx"):
    def __init__(self, img_name='000001.jpg', ip_port='http://mnjpb6.natappfree.cc/',
                     # onnx_path=basepath+r"\weights\yolov5s_pig_origin.onnx"):
                    onnx_path=os.path.join(basepath,"weights","yolov5s_pig_origin.onnx")):
        """检查onnx模型并初始化onnx"""
        onnx_model = onnx.load(onnx_path)
        try:
            onnx.checker.check_model(onnx_model)
        except Exception:
            print("[test..] Model incorrect")
        else:
            print("[test..] Model correct")

        self.img_name = img_name,
        self.ip_port = ip_port,
        self.ip_port = self.ip_port[0]

        options = ort.SessionOptions()
        options.enable_profiling = True
        # self.onnx_session = ort.InferenceSession(onnx_path, sess_options=options,
        #                                          providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
        self.onnx_session = ort.InferenceSession(onnx_path)
        self.input_name = self.get_input_name()  # ['images']
        self.output_name = self.get_output_name()  # ['output0']

    def get_input_name(self):
        """获取输入节点名称"""
        input_name = []
        for node in self.onnx_session.get_inputs():
            input_name.append(node.name)

        return input_name

    def get_output_name(self):
        """获取输出节点名称"""
        output_name = []
        for node in self.onnx_session.get_outputs():
            output_name.append(node.name)

        return output_name

    def get_input_feed(self, image_numpy):
        """获取输入numpy"""
        input_feed = {}
        for name in self.input_name:
            input_feed[name] = image_numpy

        return input_feed

    def inference(self, img_path):
        """ 1.cv2读取图像并resize
        2.图像转BGR2RGB和HWC2CHW(因为yolov5的onnx模型输入为 RGB：1 × 3 × 640 × 640)
        3.图像归一化
        4.图像增加维度
        5.onnx_session 推理 """
        # print("inference!")

        img = cv2.imread(img_path)
        im0 = img.copy()
        im0_shape = img.shape
        # print("im0_shape:{}".format(im0_shape))
        h_origin, w_origin = img.shape[0], img.shape[1]
        # print("h_origin,w_origin: {},{}".format(h_origin, w_origin))
        or_img = cv2.resize(img, (640, 640))  # resize后的原图 (640, 640, 3)
        img = or_img[:, :, ::-1].transpose(2, 0, 1)  # BGR2RGB和HWC2CHW
        img = img.astype(dtype=np.float32)  # onnx模型的类型是type: float32[ , , , ]
        img /= 255.0  # 归一化 图像
        img = np.expand_dims(img, axis=0)  # [3, 640, 640]扩展为[1, 3, 640, 640]
        # img尺寸(1, 3, 640, 640)
        input_feed = self.get_input_feed(img)  # dict:{ input_name: input_value }

        # 获取类名和颜色
        names = CLASSES
        colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]

        # 推理结果
        pred = self.onnx_session.run(None, input_feed)[0]  # <class 'numpy.ndarray'>(1, 25200, 9)

        # 请求NMS
        # print("-----------====================",opt.augment)
        # print("pred=> {}".format(pred))
        # print("\npred_size=> {}".format(pred.shape))

        # pred = non_max_suppression(pred, conf_thres=0.25, iou_thres=0.45, classes=None, agnostic=False)
        pred = filter_box(pred, conf_thres=0.5, iou_thres=0.45)

        # print('outbox( x1 y1 x2 y2 score class):')

        lab = []
        loc = []
        data = {}
        info = []
        data["identifier"] = "identifier"

        try:
            data["counts"] = len(pred)
        except:
            print("\n[test...] don't find pig!")
            data["counts"] = 0

        data["code"] = 200

        # 处理推断结果
        for i, det in enumerate(pred):  # 每张图片的推断结果
            # 如果存在检测结果
            if det is not None and len(det):
                # 重新缩放框从img_size到im0的尺寸
                det[:4] = scale_coords(img.shape[2:], det[:4], im0_shape).round()

                print("[show results]...")
                # 写出结果
                # for *xyxy, conf, cls in det:
                # for (x1,y1,x2,y2, conf, cls) in det:
                # print("det=>{}".format(det))
                # for d in det:
                #     print("d=>{}".format(d))
                x1, y1, x2, y2, conf, cls = det[0],det[1],det[2],det[3],det[4],det[5]
                label = '%s: %.2f' % (names[int(cls)], conf)
                label_no_value = '%s' % (names[int(cls)])
                confidences_value = '%.2f' % (conf)
                c1, c2 = plot_one_box((x1,y1,x2,y2), im0, label=label, color=colors[int(cls)], line_thickness=3)
                print(c1, c2,label_no_value)  # --------------------------------------------------------------------------------------->坐标 标签
                # detection_result_list.append(p,c1,c2,label_no_value)
                text = label
                text_inf = text + ' ' + '(' + str(c1[0]) + ',' + str(c1[1]) + ')' + ' ' + '宽:' + str(
                    c2[0] - c1[0]) + '高:' + str(c2[1] - c1[1])
                info.append({"label": names[int(cls)], "confidences": confidences_value})
                loc.append([c1[0], c1[1], c2[0] - c1[0], c2[1] - c1[1]])
                lab.append(text_inf)

        # 检测结果写到的目录
        # cv2.imwrite(os.path.join(basepath, set_result_path, filename_ + '_res.jpg'), img)
        # print()
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

        # res = jsonify(data)

        return lab, im0, loc, res

    def run(self, image_name):
        print("call run()=>")
        # print(type(image_name))
        t1 = time.time()
        lab, im0, loc, data= self.inference(img_path=image_name)
        t2 = time.time()

        num = data['counts']
        cnt = [0,0,0]
        for item in data['data']:
            if item['label'] == 'drink':
                cnt[0]+=1
            elif item['label'] == 'stand':
                cnt[1]+=1
            else:
                cnt[2]+=1

        # info = '其中正在饮水的有 '+str(cnt[0])+' 头， '+\
        #        '正在站立的有 '+str(cnt[1])+' 头， '+\
        #        '正在躺卧的有 '+str(cnt[2])+' 头 '
        info = '正在饮水的有 ' + str(cnt[0]) + ' 头， \n' + \
               '\t   正在站立的有 ' + str(cnt[1]) + ' 头， \n' + \
               '\t   正在躺卧的有 ' + str(cnt[2]) + ' 头。'

        # print("[test...] type(im0)=>",type(im0))
        # path = r"F:\02software\yolov5\qt\huoyin.jpg"
        # num_img = plt.imread(path)
        return {'image': im0, 'time': t2-t1, 'info': info,'num':num}


# dets:  array [x,6] 6个值分别为x1,y1,x2,y2,score,class
# thresh: 阈值
def nms(dets, thresh):
    # dets:x1 y1 x2 y2 score class
    # x[:,n]就是取所有集合的第n个数据
    x1 = dets[:, 0]
    y1 = dets[:, 1]
    x2 = dets[:, 2]
    y2 = dets[:, 3]
    # -------------------------------------------------------
    #   计算框的面积
    #	置信度从大到小排序
    # -------------------------------------------------------
    areas = (y2 - y1 + 1) * (x2 - x1 + 1)
    scores = dets[:, 4]
    # print(scores)
    keep = []
    index = scores.argsort()[::-1]  # np.argsort()对某维度从小到大排序
    # [::-1] 从最后一个元素到第一个元素复制一遍。倒序从而从大到小排序

    while index.size > 0:
        i = index[0]
        keep.append(i)
        # -------------------------------------------------------
        #   计算相交面积
        #	1.相交
        #	2.不相交
        # -------------------------------------------------------
        x11 = np.maximum(x1[i], x1[index[1:]])
        y11 = np.maximum(y1[i], y1[index[1:]])
        x22 = np.minimum(x2[i], x2[index[1:]])
        y22 = np.minimum(y2[i], y2[index[1:]])

        w = np.maximum(0, x22 - x11 + 1)
        h = np.maximum(0, y22 - y11 + 1)

        overlaps = w * h
        # -------------------------------------------------------
        #   计算该框与其它框的IOU，去除掉重复的框，即IOU值大的框
        #	IOU小于thresh的框保留下来
        # -------------------------------------------------------
        ious = overlaps / (areas[i] + areas[index[1:]] - overlaps)
        idx = np.where(ious <= thresh)[0]
        index = index[idx + 1]
    return keep


def xywh2xyxy(x):
    # [x, y, w, h] to [x1, y1, x2, y2]
    y = np.copy(x)
    y[:, 0] = x[:, 0] - x[:, 2] / 2
    y[:, 1] = x[:, 1] - x[:, 3] / 2
    y[:, 2] = x[:, 0] + x[:, 2] / 2
    y[:, 3] = x[:, 1] + x[:, 3] / 2
    return y


def filter_box(org_box, conf_thres, iou_thres):  # 过滤掉无用的框
    # -------------------------------------------------------
    #   删除为1的维度
    #	删除置信度小于conf_thres的BOX
    # -------------------------------------------------------
    org_box = np.squeeze(org_box)  # 删除数组形状中单维度条目(shape中为1的维度)
    # (25200, 9)
    # […,4]：代表了取最里边一层的所有第4号元素，…代表了对:,:,:,等所有的的省略。此处生成：25200个第四号元素组成的数组
    conf = org_box[..., 4] > conf_thres  # 0 1 2 3 4 4是置信度，只要置信度 > conf_thres 的
    box = org_box[conf == True]  # 根据objectness score生成(n, 9)，只留下符合要求的框
    # print('box:符合要求的框')
    # print(box.shape)

    # -------------------------------------------------------
    #   通过argmax获取置信度最大的类别
    # -------------------------------------------------------
    cls_cinf = box[..., 5:]  # 左闭右开（5 6 7 8），就只剩下了每个grid cell中各类别的概率
    cls = []
    for i in range(len(cls_cinf)):
        cls.append(int(np.argmax(cls_cinf[i])))  # 剩下的objecctness score比较大的grid cell，分别对应的预测类别列表
    all_cls = list(set(cls))  # 去重，找出图中都有哪些类别
    # set() 函数创建一个无序不重复元素集，可进行关系测试，删除重复数据，还可以计算交集、差集、并集等。
    # -------------------------------------------------------
    #   分别对每个类别进行过滤
    #   1.将第6列元素替换为类别下标
    #	2.xywh2xyxy 坐标转换
    #	3.经过非极大抑制后输出的BOX下标
    #	4.利用下标取出非极大抑制后的BOX
    # -------------------------------------------------------
    output = []
    for i in range(len(all_cls)):
        curr_cls = all_cls[i]
        curr_cls_box = []
        curr_out_box = []

        for j in range(len(cls)):
            if cls[j] == curr_cls:
                box[j][5] = curr_cls
                curr_cls_box.append(box[j][:6])  # 左闭右开，0 1 2 3 4 5

        curr_cls_box = np.array(curr_cls_box)  # 0 1 2 3 4 5 分别是 x y w h score class
        # curr_cls_box_old = np.copy(curr_cls_box)
        curr_cls_box = xywh2xyxy(curr_cls_box)  # 0 1 2 3 4 5 分别是 x1 y1 x2 y2 score class
        curr_out_box = nms(curr_cls_box, iou_thres)  # 获得nms后，剩下的类别在curr_cls_box中的下标

        for k in curr_out_box:
            output.append(curr_cls_box[k])
    output = np.array(output)
    return output


def draw(image, box_data):
    # -------------------------------------------------------
    #	取整，方便画框
    # -------------------------------------------------------

    boxes = box_data[..., :4].astype(np.int32)  # x1 x2 y1 y2
    scores = box_data[..., 4]
    classes = box_data[..., 5].astype(np.int32)
    for box, score, cl in zip(boxes, scores, classes):
        top, left, right, bottom = box
        # print('class: {}, score: {}'.format(CLASSES[cl], score))
        # print('box coordinate left,top,right,down: [{}, {}, {}, {}]'.format(top, left, right, bottom))

        cv2.rectangle(image, (top, left), (right, bottom), (255, 0, 0), 2)
        cv2.putText(image, '{0} {1:.2f}'.format(CLASSES[cl], score),
                    (top, left),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (0, 0, 255), 2)
    return image


if __name__ == "__main__":
    # onnx_path = 'weights/sim_best20221027.onnx'
    onnx_path = 'weights/yolov5s_pig_origin.onnx'
    model = Yolov5ONNX(onnx_path)
    # output, or_img = model.inference('data/images/img.png')
    output, or_img, h, w = model.inference('qt/data/J_000076.png')
    print('pred: 位置[0, 10000, :]的数组')
    print(output.shape)
    print(output[0, 10000, :])
    outbox = filter_box(output, 0.5, 0.5)  # 最终剩下的Anchors：0 1 2 3 4 5 分别是 x1 y1 x2 y2 score class
    print('outbox( x1 y1 x2 y2 score class):')
    print(outbox)
    if len(outbox) == 0:
        print('没有发现物体')
        sys.exit(0)
    or_img = draw(or_img, outbox)
    # add by wedream. resize back
    # 使用cv2.resize时，参数输入是 宽×高×通道 ，与以往操作不同
    or_img = cv2.resize(or_img, (w, h))
    # end
    # cv2.imwrite('./runs/images/res.jpg', or_img)
