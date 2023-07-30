var app = getApp();
var api = require('../../utils/api.js');
Page({
  data: {
    motto: '行为识别',
    result: [],
    images: {},
    resultData: null,
    // resultData: [{'id': '1','label': 'lie', 'confidences': '0.90'}, {'id': '2','label': 'lie', 'confidences': '0.84'}, {'id': '3','label': 'lie', 'confidences': '0.74'}],
    img: '',
    modalName: '',
    modalTitle: null,
    modalContent: null,
    detail: null,
  },
  //用户点击右上角分享朋友圈
  onShareTimeline: function () {
  },
  //用户点击右上角分享朋友|朋友圈
  onShareAppMessage: function () {
    wx.showShareMenu({
      withShareTicket: true,
      menus: ['shareAppMessage', 'shareTimeline']
    })
    return {
      title: '行为识别',
      path: '/pages/detect/detect'
    }
  },
  //打开识别结果详情
  showDetail: function (e) {
    var that = this
    // var description = that.detail (特别注意！！！) 应该写成that.data.detail
    var description = that.data.detail
    // console.log(description)
    // console.log("detail=>",that.data.detail)
    var name = '详情';
    if (description == undefined) {
      wx.showToast({
        title: '暂无介绍内容1',
        icon: 'none',
        duration: 2000,
        mask: true
      })
    } else {
      if (description.length > 0) {
        wx.showModal({
          title: name,
          content: description,
          showCancel: false,
          confirmText: '关闭详情',
          confirmColor: '#02A0E7'
        })
      } else {
        wx.showToast({
          title: '暂无介绍内容2',
          icon: 'none',
          duration: 2000,
          mask: true
        })
      }
    }
  },
  clear: function (event) {
    wx.clearStorage();
  },
  //事件处理函数
  bindViewTap: function () {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
    //从聊天页面选择图片（小bug）
  chooseMessage:function(){
    var that = this;
    wx.chooseMessageFile({
      count: 1,
      sizeType: ['compressed'],
      type:'image',
      success(res){
        if (res.tempFiles[0].size > (4096 * 2048)) {
          wx.showToast({
            title: '图片文件过大哦',
            icon: 'none',
            mask: true,
            duration: 1500
          })
        } else {
          that.setData({
            img: res.tempFiles[0].path
          })
          console.log("[test...] ",res.tempFiles[0].path)
          that.doUpload(res.tempFiles[0].path); // 上传图片
        }
      }
    })
  },
  //请求方法
  uploads: function () {
    var that = this
    var takephonewidth
    var takephoneheight
    wx.chooseImage({
      count: 1, // 默认9
      sizeType: ['compressed'], // 可以指定是原图还是压缩图，默认二者都有
      sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
      success: function (res) {
        wx.getImageInfo({
          src: res.tempFilePaths[0],
          success(res) {
            takephonewidth = res.width,
              takephoneheight = res.height
          }
        })
        // 返回选定照片的本地文件路径列表，tempFilePath可以作为img标签的src属性显示图片
        if (res.tempFiles[0].size > (4096 * 2048)) {
          wx.showToast({
            title: '图片文件过大哦',
            icon: 'none',
            mask: true,
            duration: 1500
          })
        } else {
          that.doUpload(res.tempFilePaths[0]);
          console.log("[test...]",res.tempFilePaths[0])
        }

      },
    })
  },
  //图片上传
  doUpload(file){
    var that = this;
    that.setData({
      img: file
    }),
    wx.showLoading({
      title: "图片上传中...",
      mask: true
    }),
    api.yoloRequest(file,  { // 上传图片的接口
      success(result) {
        var resultJ = JSON.parse(result)
        // console.log(resultJ.data)
        wx.hideLoading();
        if (resultJ.code == 200) {
          // that.setData({
          //   resultData: resultJ.result
          // })
        } else {
          if (resultJ.code == 87014) {
            wx.hideLoading();
            wx.showModal({
              content: '存在敏感内容，请更换图片',
              showCancel: false,
              confirmText: '明白了'
            })
            that.setData({
              img: null
            })
          } else {
            wx.hideLoading();
            wx.showModal({
              content: resultJ.msg_zh,
              showCancel: false,
              confirmText: '明白了'
            })
          }
        }
      }
    })
  },
//行为识别
doDetect(){
  var that = this;
  that.setData({
    // img: file
  }),
  wx.showLoading({
    title: "行为识别中...",
    mask: true
  }),
  api.yoloRequest2(  { // 行为识别接口
    success(result) {
      wx.hideLoading();
      console.log(result)
      var resultJ = result
      var res = result
      var tmpResData = []
      var detData = [0,0,0]
      var detJson = ''

      for (var i=0;i<result.data.length;i++) // 获取行为识别列表
      {
          var tt={}
          tt['id'] = i+1
          if(result.data[i]['label'] === 'drink')
             tt['label']='饮水',detData[0] += 1
          else if(result.data[i]['label'] === 'stand')
              tt['label']='站立',detData[1] += 1
          else
              tt['label']='躺卧',detData[2] += 1
          tt['confidences']=Math.round((result.data[i]['confidences'])*100)  
          tmpResData.push(tt)
      }

      // 生成详情的字符内容
      detJson = '一共检测出 '+res.counts+' 头群养猪；'
      detJson = detJson+'其中正在饮水的有 '+detData[0]+' 头， '
          +'正在站立的有 '+detData[1]+' 头， '
          +'正在躺卧的有 '+detData[2]+' 头 '+'；\n\n'
      detJson = detJson+'详细识别结果按置信度排序如下：\n'
      for (var i=0;i<res.data.length;i++)
      {
          if(res.data[i]['label'] === 'drink')
              detJson = detJson+' '+(i+1)+'号猪'+ '进行饮水行为，置信度为 '+res.data[i]['confidences']+'；\n'
          else if(res.data[i]['label'] === 'stand')
              detJson = detJson+' '+(i+1)+'号猪'+ '进行站立行为，置信度为 '+res.data[i]['confidences']+'；\n'
          else
              detJson = detJson+' '+(i+1)+'号猪'+ '进行躺卧行为，置信度为 '+res.data[i]['confidences']+'；\n'
      }
      detJson = detJson + '\n'
      // console.log(detJson)

      if (resultJ['code'] == 200) {
        that.setData({
          img: resultJ['resName']
        })
        that.setData({
          // resultData: [{'id': '1','label': 'lie', 'confidences': '0.50'}, {'id': '2','label': 'lie', 'confidences': '0.50'}, {'id': '3','label': 'lie', 'confidences': '0.50'}]
          resultData: tmpResData,
          detail: detJson,
        })
        if (res.counts === 0)
        {
          wx.showToast({
            title: '没有检测出群养猪',
            icon: 'none',
            mask: true,
            duration: 2000
          })
        }
        console.log("detail====>"+detJson)
      } else {
        if (resultJ['code'] == 87014) {
          wx.hideLoading();
          wx.showModal({
            content: '存在敏感内容，请更换图片',
            showCancel: false,
            confirmText: '明白了'
          })
          that.setData({
            img: null
          })
        } else {
          wx.hideLoading();
          wx.showModal({
            content: resultJ.msg_zh,
            showCancel: false,
            confirmText: '明白了'
          })
        }
      }
    }
  })
},


  onLoad: function () {
  },
  /**
 * 点击查看图片，可以进行保存
 */
  preview(e) {
    var that = this;
    wx.previewImage({
      urls: [that.data.img],
      current: that.data.img
    })
  }
});
