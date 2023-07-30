import shutil
import os
import cv2
import re

mode = 'test' # test


def main():
    #  images-dir
    path_image = './data/images/'+mode
    #  labels-dir
    path_labels = './data/labels/'+mode
    type_object = '.txt'

    # 画框效果图的输出目录
    output_images = './hands/images/'+mode
    # output_labels = './hands/labels'

    history_name = []

    if not os.path.exists(output_images):
        os.makedirs(output_images)

    for ii in os.walk(path_image):
        for j in ii[2]:
            type = j.split(".")[1]
            # if type != 'jpg':
            #     continue
            path_img = os.path.join(path_image, j)
            label_name = j[:-4] + type_object
            path_label = os.path.join(path_labels, label_name)
            if os.path.exists(path_label) != True:
                continue
            f = open(path_label, 'r+', encoding='utf-8')
            # print(path_img)
            img = cv2.imread(path_img)
            w = img.shape[1]
            h = img.shape[0]
            img_tmp = img.copy()
            new_lines = []
            hands_lines = []
            save_path = os.path.join(output_images, path_img.split('\\')[-1])
            lines = f.readlines()
            for line in lines:
                if line:
                    # img_tmp = img.copy()
                    msg = line.split(" ")
                    # print(x_center,",",y_center,",",width,",",height)
                    x1 = int((float(msg[1]) - float(msg[3]) / 2) * w)  # x_center - width/2
                    y1 = int((float(msg[2]) - float(msg[4]) / 2) * h)  # y_center - height/2
                    x2 = int((float(msg[1]) + float(msg[3]) / 2) * w)  # x_center + width/2
                    y2 = int((float(msg[2]) + float(msg[4]) / 2) * h)  # y_center + height/2
                    # print(x1, ",", y1, ",", x2, ",", y2)
                    cv2.rectangle(img_tmp, (x1, y1), (x2, y2), (0, 0, 255), 5)
            # cv2.imshow("show", img_tmp)
            # c = cv2.waitKey(0)
            cv2.imwrite(save_path, img_tmp);
            print(save_path)

if __name__ == '__main__':
    main()

