//域名地址
// var prefix2 = 'http://127.0.0.1:8081'; //后端接口的ip
// var prefix2 = 'http://127.0.0.1:8083'; //后端接口的ip
var prefix2 = 'http://1.12.231.219:8083'; //后端接口的ip
// var prefix = '';
//小程序账号编码(自己定义，后端项目中对应weixin_account表中的account_code)

//目标检测接口
const yolo_url = prefix2+'/upload_image';
const yolo_url2 = prefix2+'/yolo';


/**
 * 用户首次访问累计天数
 * @param userId 用户ID
 * @param openid 微信用户openid
 */
let userDaysRequest = (userId,openid,callback) => {
  //发送接口请求
  wx.request({
    url: userdays_url,
    method: 'GET',
    data: {
      'userId': userId,
      'openid': openid
    },
    success: function (res) {
      callback.success(res.data)
    },
    fail: function (res) {
      if (callback.fail)
        callback.fail()
    }
  })
}

/**
 * 目标检测上传图片
 * @param file 图片
 */
let yoloRequest = (file,callback) => {
    //发送接口请求
    wx.uploadFile({
      url: yolo_url,
      filePath: file,
      header: {
        'content-type': 'multipart/form-data'
      },
      name: 'file',
      formData: {
        'version':'2',
        'userId': 'userId',
        'account_code': 'account_code',
        'cityId': 'cityId'
      },
      method: 'POST',
      success: function (res) {
        callback.success(res.data)
      },
      fail: function (res) {
        if (callback.fail)
          callback.fail()
      }
    })
  }

  /**
 * 目标检测
 */
let yoloRequest2 = (callback) => {
  //发送接口请求
  wx.request({
    url: yolo_url2,
    method: 'GET',
    data: {
      'userId': 'userId',
      'openid': 'openid'
    },
    success: function (res) {
      callback.success(res.data)
    },
    fail: function (res) {
      if (callback.fail)
        callback.fail()
    }
  })
}


/** 暴露出去 */
module.exports={
  /** 暴露出去url */
  yolo_url: yolo_url,
  yolo_url2: yolo_url2,

  /** 暴露出去方法 */
  yoloRequest:yoloRequest,
  yoloRequest2:yoloRequest2,
}
