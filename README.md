# PigNet
Research on Behavior Recognition of Group-housed Pigs by Weijun Yuan.

<img src="assets/readme_res.png#pic_center" width="60%" alt="" align="center" />

群养猪的运动信息和行为信息与其健康状况息息相关，但人工巡视费时费力，本实验提出采用**行为识别**算法于群养猪的养殖管理中，识别群养猪**drink（饮水）**、**stand（站立）**和**lie（躺卧）**行为，为自动化养殖提供基础。本项目最终以**三种不同的形式**进行部署，分别为：

- 网站平台
- 微信小程序
- PyQt应用程序

## 实验流程

下图是基于改进YOLOv5s的群养猪行为识别模型建立流程，可概括为以下几个阶段：数据集的准备工作，YOLOv5模型的搭建，模型结构的调优和模型的部署。

<img src="assets/readme01.png#pic_center" width="100%" alt="" align="center" />

## 数据集的准备工作

关于群养猪的行为相关的数据集十分难获取，尤其是饮水行为的数据集。进行数据集的准备工作时，首先通过在生猪养殖场抓拍特定行为的图片和编写脚本爬取网络图片来采集数据集，然后使用labelImg软件进行数据集的标注，并将群养猪的行为定义为drink（饮水）、stand（站立）和lie（躺卧），标注完成后编写代码将标注数据转化为txt格式，原始图片和txt格式的标注文件共同构成群养猪行为识别数据集。

## YOLOv5模型的搭建

在YOLOv5s模型的搭建阶段，将输入端、骨干网络、颈部网络和头部网络按照一定组织结构连接起来，同时可在`yolov5/models/yolov5s.yaml`文件中按需修改骨干网络和头部网络的结构，修改后可通过运行`yolov5/models/yolo.py`文件查看网络结构。

注意：YOLOv5模型的搭建对应的工作目录是`yolov5`。

## 模型结构的调优

在模型结构的调优阶段，在深度学习平台中开始对模型进行训练，直到模型收敛，然后对模型进行测试，比较并调整模型结构，周而复始，直到得到适用于群养环境下密集拥挤的生猪检测场景的模型。

在YOLOv5s基础上，提出两种改进群养猪行为识别方法。第一点改进为：将**坐标注意力模块**（Coordinate Attention，CA）融合在YOLOv5s的骨干网络之后，记为YOLOv5s_CA。CA能够突出特征图的重要行为特征，抑制一般特征，对比于基于YOLOv5s群养猪行为识别算法，该模型的召回率、F1得分和mAP@0.5均有提升，分别为90.6%，0.897和93.0%。第二点改进为：在YOLOv5s_CA的基础上，用**DIoU-NMS**后处理算法替换NMS，记为改进YOLOv5s_CA。该改进方法在行为识别预测阶段，能够有效保留图像中密集遮挡的目标生猪检测框，降低生猪的漏检率。下图为改进YOLOv5s_CA的网络结构：

<img src="assets/readme02.png#pic_center" width="80%" alt="" align="center" />

下表为基于YOLOv5s网络的消融实验结果：

| CA   | DIoU-NMS | 精确率(%) | 召回率(%) | F1        | mAP@0.5(%) | 推理时间   |
| ---- | -------- | --------- | --------- | --------- | ---------- | ---------- |
| -    | -        | **92.4**  | 86.4      | 0.893     | 92.9       | 2.475ms/张 |
| √    | -        | 88.8      | 90.6      | 0.897     | 93.0       | 2.725ms/张 |
| -    | √        | 88.4      | **93.1**  | 0.907     | 93.6       | 6.600ms/张 |
| √    | √        | 90.9      | 91.5      | **0.912** | **94.1**   | 6.763ms/张 |

注意：YOLOv5模型结构的调优对应的工作目录是`yolov5`。

## 模型的部署

### 通用中间格式ONNX

首先将自己训练得到的群养猪行为识别模型，转换为机器学习通用中间格式**ONNX**，为后续**ONNX Runtime**部署奠定基础。导出ONNX需要声明输入图像的大小，我指定为640×640​，其核心代码如下：

```python
torch.onnx.export(model, img, f, verbose=False, opset_version=12, input_names=['images'],
                   dynamic_axes={'images': {0: 'batch', 2: 'height', 3: 'width'},  # size(1,3,640,640)
                                'output': {0: 'batch', 2: 'y', 3: 'x'}} if opt.dynamic else None)
```

注意：导出ONNX的代码为`yolov5/models/export.py`。在导出改进YOLOv5s_CA模型为ONNX格式时，坐标注意力中使用了nn.AdaptiveAvgPool2d，这个操作符在ONNX是动态的，ONNX暂时不支持导出。因此，导出的是基于YOLOv5s的群养猪行为识别模型，并在后续的部署中使用该模型。

使用**ONNX Runtime**部署即可调用ONNX格式的模型，其核心代码如下：

```python
import onnxruntime as ort
self.onnx_session = ort.InferenceSession(onnx_path)
# 推理结果
pred = self.onnx_session.run(None, input_feed)[0]  # <class 'numpy.ndarray'>(1, 25200, 9)
```

注意：使用ONNX进行推理的代码为`yolov5_deploy/onnx_inference3.py`。

### 使用Flask部署后端服务

使用轻量级的**Flask**框架编写调用YOLOv5s模型进行推理的接口，各个接口的功能如下：

| 接口                                                         | 功能                         |
| ------------------------------------------------------------ | ---------------------------- |
| [http://1.12.231.219:8083/demo](http://1.12.231.219:8083/demo) | 上传图片并进行推理识别的demo |
| [http://1.12.231.219:8083/upload_image](http://1.12.231.219:8083/upload_image) | 上传图片                     |
| [http://1.12.231.219:8083/results/<imageId>](http://1.12.231.219:8083/results/<imageId>) | 查看图片                     |
| [http://1.12.231.219:8083/yolo](http://1.12.231.219:8083/yolo) | 调用ONNX模型进行推理         |

注意：使用Flask部署后端服务的工作目录为`yolov5_deploy`。

下图为能直接展示的Flask后端接口：

<img src="assets/readme03.png#pic_center" width="100%" alt="" align="center" />

### 网站平台

网站部署网址：[http://1.12.231.219/](http://1.12.231.219/)

在网站平台的实现上，实验采用**Vue.js**作为前端框架，使用轻量级的Flask框架编写的后端接口，采用前后端分离的方式进行网站平台的开发。下图为网站平台首页：

<img src="assets/readme04.png#pic_center" width="90%" alt="" align="center" />

将网页下拉到底部，用户可以点击“选择文件”的按钮上传群养猪图片，并点击“行为识别”：

<img src="assets/readme04-1.png#pic_center" width="90%" alt="" align="center" />

注意：使用Vue部署网站平台的工作目录为`deepvue`。

### 微信小程序

在微信小程序的实现上，实验使用**微信开发者工具**进行开发，后端采用Flask框架进行编写，以前后端分离的方式完成该项目设计与开发。由于需要**域名**才能上线小程序，因此微信端的部署仅限于本地开发，之后有充足的经济支持会考虑上架小程序。

微信小程序的界面如下图所示，界面划分为“登录”、 “行为识别”和“个人中心”三个部分。

<img src="assets/readme05.png#pic_center" width="60%" alt="" align="center" />

 群养猪行为识别检测系统（微信小程序）操作展示如下：

<img src="assets/readme05-1.png#pic_center" width="50%" alt="" align="center" />

<img src="assets/readme05-2.png#pic_center" width="50%" alt="" align="center" />

注意：使用开发微信小程序的工作目录为`wx-pig`。

### PyQt应用程序

在应用软件的实现上，实验采用Python和PyQt5完成对群养猪行为识别检测系统的开发，借助界面设计辅助工具QtDesigner完成应用软件的界面设计工作。应用软件的主界面如下所示，界面划分为五个模块，分别为“图片显示模块”、“图片调整模块”、“图片信息模块”、“识别结果模块”和“功能按钮模块”。

<img src="assets/readme06.png#pic_center" width="90%" alt="" align="center" />

应用程序操作如下所示：

<img src="assets/readme06-1.png#pic_center" width="90%" alt="" align="center" />

注意：使用PyQt开发应用程序的工作目录为`yolov5_pyqt`。

