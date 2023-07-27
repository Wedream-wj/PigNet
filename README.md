# PigNet
Research on Behavior Recognition of Group-housed Pigs by Weijun Yuan.

群养猪的运动信息和行为信息与其健康状况息息相关，但人工巡视费时费力，本项目提出采用**行为识别**算法于群养猪的养殖管理中，识别群养猪**drink（饮水）**、**stand（站立）**和**lie（躺卧）**行为，为自动化养殖提供基础。本项目最终以**三种不同的形式**进行部署，分别为：

- PyQt应用程序
- 网站平台
- 微信小程序

## 项目流程

下图是基于改进YOLOv5s的群养猪行为识别模型建立流程，可概括为以下几个阶段：数据集的准备工作，YOLOv5模型的搭建，模型结构的调优和模型的部署。

<img src="http://1.12.231.219:8083/results/readme01.png#pic_center" width="100%" alt="" align="center" />

## 数据集的准备工作

关于群养猪的行为相关的数据集十分难获取，尤其是饮水行为的数据集。进行数据集的准备工作时，首先通过在生猪养殖场抓拍特定行为的图片和编写脚本爬取网络图片来采集数据集，然后使用labelImg软件进行数据集的标注，并将群养猪的行为定义为drink（饮水）、stand（站立）和lie（躺卧），标注完成后编写代码将标注数据转化为txt格式，原始图片和txt格式的标注文件共同构成群养猪行为识别数据集。

## YOLOv5模型的搭建

在YOLOv5s模型的搭建阶段，将输入端、骨干网络、颈部网络和头部网络按照一定组织结构连接起来，同时可在`yolov5/models/yolov5s.yaml`文件中按需修改骨干网络和头部网络的结构，修改后可通过运行`yolov5/models/yolo.py`文件查看网络结构。

注意：YOLOv5模型的搭建对应的工作目录是`yolov5`。

## 模型结构的调优

在模型结构的调优阶段，在深度学习平台中开始对模型进行训练，直到模型收敛，然后对模型进行测试，比较并调整模型结构，周而复始，直到得到适用于群养环境下密集拥挤的生猪检测场景的模型。

在YOLOv5s基础上，提出两种改进群养猪行为识别方法。第一点改进为：将**坐标注意力模块**（Coordinate Attention，CA）融合在YOLOv5s的骨干网络之后，记为YOLOv5s_CA。CA能够突出特征图的重要行为特征，抑制一般特征，对比于基于YOLOv5s群养猪行为识别算法，该模型的召回率、F1得分和mAP@0.5均有提升，分别为90.6%，0.897和93.0%。第二点改进为：在YOLOv5s_CA的基础上，用**DIoU-NMS**后处理算法替换NMS，记为改进YOLOv5s_CA。该改进方法在行为识别预测阶段，能够有效保留图像中密集遮挡的目标生猪检测框，降低生猪的漏检率。

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

首先将自己训练得到的群养猪行为识别模型，转换为机器学习通用中间格式**ONNX**，为后续**ONNX Runtime**部署奠定基础。导出ONNX需要声明输入图像的大小，我指定为$640\times640$，其核心代码如下：

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

使用轻量级的Flask框架编写调用YOLOv5s模型进行推理的接口，各个接口的功能如下：

| 接口                                                         | 功能                         |
| ------------------------------------------------------------ | ---------------------------- |
| [http://1.12.231.219:8083/demo](http://1.12.231.219:8083/demo) | 上传图片并进行推理识别的demo |
| [http://1.12.231.219:8083/upload_image](http://1.12.231.219:8083/upload_image) | 上传图片                     |
| [http://1.12.231.219:8083/upload_image/results/<imageId>](http://1.12.231.219:8083/upload_image/results/<imageId>) | 查看图片                     |
| [http://1.12.231.219:8083/yolo](http://1.12.231.219:8083/yolo) | 调用ONNX模型进行推理         |

注意：使用Flask部署后端服务的工作目录为`yolov5_deploy`。





### 环境

- Vue3.0（脚手架搭建）+ ElementPlus（UI组件） + v-md-editor（支持markdown语法） + echarts（大数据展示）

### 运行前端项目
```
npm run serve
```

### 打包前端项目
```
npm run build
```

### Tips

- **vue/public/static/config.js**：配置文件上传的ip地址，filesUploadUrl进行本地开发时为localhost，发布时为服务器的ip地址，如“120.79.9.66”
- **vue/public/index.html**：记得在此文件中引入config.js，代码为`<script src="static/config.js"></script>`
- **vue/src/utils/request.js**: 获取后端接口的工具类文件
- **vue/vue.config.js**：主要解决前端的跨域问题
- 打包vue的命令：进入vue目录后，运行`npm run build`即可生成dist目录。
- 前端开发步骤：在views中编写对应的vue-> 在router中中配置路由-> 在Aside.vue里面添加相应的模块
- **注意**：部署时一定要修改对应的配置文件文件上传ip地址（config.js）



## 后端

### 环境

Springboot2.5 + Mybatisplus（不用写SQL语句了）+ swagger （项目API文档）

### Tips

- **files**文件夹存放的是用户上传的图片
- **springboot/src/main/java/com/example/demo/common/CorsConfig.java**：后端跨域的配置
- **springboot/src/main/resources/application.properties**：进行本地开发时的配置文件，其中参数file.ip是上传文件的ip地址。file.ip开发时可为“localhost”，发布时为服务器的ip地址，如“120.79.9.66”
- **springboot/src/main/resources/application-prod.properties**：发布时的配置文件，参数file.ip一般为服务器ip地址，如“120.79.9.66”。激活该配置文件的命令为：--spring.profiles.active=prod
- 运行后端项目命令为：`nohup java -jar demo-0.0.1-SNAPSHOT.jar --spring.profiles.active=prod &`
- 后端开发步骤：在entity中添加相应的实体类-> 在mapper中继承相应的类-> 在controller中添加对应的接口类
- 启动后端后，访问 http://localhost:9090/swagger-ui.html 能够查看项目API文档
- **注意**：部署时一定要启用对应的配置文件（application-prod.properties）



## 数据库

### 云数据库

url：rm-bp1n4269q5xqhgna0125010bm.mysql.rds.aliyuncs.com

username：ywj

password：Ywj123456