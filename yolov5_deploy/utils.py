import random

import cv2
import numpy as np

# Set printoptions
np.set_printoptions(linewidth=320, formatter={'float_kind': '{:11.5g}'.format})  # format short g, %precision=5
# matplotlib.rc('font', **{'size': 11})

# Prevent OpenCV from multithreading (to use PyTorch DataLoader)
cv2.setNumThreads(0)

def scale_coords(img1_shape, coords, img0_shape, ratio_pad=None):
    # Rescale coords (xyxy) from img1_shape to img0_shape
    if ratio_pad is None:  # calculate from img0_shape
        gain = max(img1_shape) / max(img0_shape)  # gain  = old / new
        pad = (img1_shape[1] - img0_shape[1] * gain) / 2, (img1_shape[0] - img0_shape[0] * gain) / 2  # wh padding
    else:
        gain = ratio_pad[0][0]
        pad = ratio_pad[1]

    # coords[:, [0, 2]] -= pad[0]  # x padding
    # coords[:, [1, 3]] -= pad[1]  # y padding
    # coords[:, :4] /= gain

    coords[[0, 2]] -= pad[0]  # x padding
    coords[[1, 3]] -= pad[1]  # y padding
    coords[:4] /= gain

    clip_coords(coords, img0_shape)
    return coords


def clip_coords(boxes, img_shape):
    # Clip bounding xyxy bounding boxes to image shape (height, width)
    # boxes[:, 0].clamp_(0, img_shape[1])  # x1
    # boxes[:, 1].clamp_(0, img_shape[0])  # y1
    # boxes[:, 2].clamp_(0, img_shape[1])  # x2
    # boxes[:, 3].clamp_(0, img_shape[0])  # y2
    # boxes[0].clamp_(0, img_shape[1])  # x1
    # boxes[1].clamp_(0, img_shape[0])  # y1
    # boxes[2].clamp_(0, img_shape[1])  # x2
    # boxes[3].clamp_(0, img_shape[0])  # y2
    np.clip(boxes[0], 0, img_shape[1])
    np.clip(boxes[1], 0, img_shape[0])
    np.clip(boxes[2], 0, img_shape[1])
    np.clip(boxes[3], 0, img_shape[0])


# 画框
def plot_one_box(x, img, color=None, label=None, line_thickness=None):
    # Plots one bounding box on image img
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    # print("c1,c2=>",c1,c2)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
    # cv2.imshow("show", img)
    # c = cv2.waitKey(0)
    return c1,c2
