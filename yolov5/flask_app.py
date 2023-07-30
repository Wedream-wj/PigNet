# -*- coding: utf-8 -*-#
import os
import uuid
# import global_var as glo
import warnings
from datetime import timedelta

from flask import Flask, request, Response
from flask import render_template, jsonify
from werkzeug.utils import secure_filename

import detector
from utils.utils import *

warnings.filterwarnings("ignore")
set_upload_path = 'static/images/upload'
set_result_path = 'static/images/results'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
# basepath为项目的路径
basepath = os.path.dirname(__file__)
# print("basepath=>",basepath)

# glo._init()
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
app = Flask(__name__)
file_name_g=''
app.send_file_max_age_default = timedelta(seconds=1)

def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    # try:
    #     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #     s.connect(('8.8.8.8', 80))
    #     ip = s.getsockname()[0]
    # finally:
    #     s.close()
    with open(basepath + '/ip.config', 'r') as f:
        ip = f.readline()
        if ip[-1]=='\n':
            ip=ip[:len(ip)-1]
        # print("get_ip=>",ip)
    return ip

# 处理中文编码
app.config['JSON_AS_ASCII'] = False
# ip+端口
# ip = 'http://'+get_host_ip()
# port = ':8081/'
# ip_port = ip+port
# print('ip=>',ip_port)

# ip = "http://6n994w.natappfree.cc/"
ip_port = get_host_ip()+'/'
print('[test...]ip=>',ip_port)
det = detector.YOLOv5(ip_port=ip_port)

# 跨域支持
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


app.after_request(after_request)
# 设置上传图片保存的文件夹
app.config['UPLOAD_FOLDER'] = basepath+r'/static/images/upload'
# 设置检测结果保存的文件夹
app.config['RESULT_FOLDER'] = basepath+r'/static/images/results'

# 设置允许上传的文件格式
ALLOW_EXTENSIONS = ['png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JEPG',]


# 判断文件后缀是否在列表中
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1] in ALLOW_EXTENSIONS

# 上传图片
@app.route("/upload_image", methods=['POST', "GET"])
def uploads():
    # global file_name_g
    if request.method == 'POST':
        # 获取post过来的文件名称，从name=file参数中获取
        # print(request.files)
        # print(type(request.files))
        file = request.files['file']
        # print(type(file))
        # 检测文件格式
        if file and allowed_file(file.filename):
            # secure_filename方法会去掉文件名中的中文
            # file_name = secure_filename(file.filename)
            uuid_str = uuid.uuid4().hex[:10]
            file_name = '%s.jpg' % uuid_str # 生成随机图片名字
            det.img_name=file_name
            print("[test...]filename=>",file_name)
            # 保存图片
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
            return {"code": '200', "data": "", "message": "上传成功"}
        else:
            return "格式错误，仅支持jpg、png、jpeg格式文件"
    return {"code": '503', "data": "", "message": "仅支持post方法"}


# 查看图片
@app.route("/results/<imageId>")
def get_frame(imageId):
    # 图片上传保存的路径
    # with open(r'./static/images/{}'.format(imageId), 'rb') as f:
    with open(basepath+r'/static/images/results/{}'.format(imageId), 'rb') as f:
    # with open(r'./static/images/results/{}'.format(imageId), 'rb') as f:
        image = f.read()
        result = Response(image, mimetype="image/jpg")
        return result

# 调用YOLOv5
@app.route("/yolo")
def get_yolo():
    # 调用YOLOv5中的detect方法
    # global file_name_g
    print(det.img_name)
    all_file_name_g=os.path.join(app.config['UPLOAD_FOLDER'], det.img_name)
    # print("all_file_name_g=>",all_file_name_g)

    with torch.no_grad():
        # lab, img, loc, res = yolo5.detect(o_source = upload_path)
        lab, img, loc, res = det.detect(o_source=all_file_name_g)
    basepath = os.path.dirname(__file__)
    # 检测结果写到的目录
    # cv2.imwrite(os.path.join(basepath, set_result_path, filename_ + '_res.jpg'), img)
    # cv2.imwrite(os.path.join(app.config['RESULT_FOLDER'], det.img_name), img)
    print("[test...]res=>", res)
    return res


    resName= ip_port+'results/'+det.img_name
    print(det.img_name)
    return {"code": '200', "data": "hello", "message": "检测成功","resName":resName}

# 调用YOLOv3
@app.route("/")
def get_index():
    # 首页
    return {"code": '200', "data": "hello", "message": "访问成功"}

#URL地址
@app.route('/demo', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        #data = request.get_data()
        #json_data = json.loads(data)
        f = request.files['file']
        sss = request.form["identifier"]
        # print(sss)
        # glo.set_value("identifier",sss)
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "File type exception !"})
        t = f.filename
        filename_ = t.split('.')[0]
        det.img_name = filename_
        user_input = request.form.get("name")
        basepath = os.path.dirname(__file__)
        # 文件上传目录地址
        upload_path = os.path.join(basepath, set_upload_path, secure_filename(f.filename))
        # result_path = os.path.join(basepath, set_result_path,  filename_+'_res.jpg')
        f.save(upload_path)
        # lab, img, loc, res = yolo.yolo_detect(pathIn=upload_path)
        with torch.no_grad():
            # lab, img, loc, res = yolo5.detect(o_source = upload_path)
            lab, img, loc, res = det.detect(o_source=upload_path)
        #检测结果写到的目录
        cv2.imwrite(os.path.join(basepath, set_result_path, filename_+'.jpg'), img)
        print("[test...]res=>",res)
        return res
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
