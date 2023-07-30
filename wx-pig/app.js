// app.js
App({
  onLaunch() {
    // 展示本地存储能力

    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
      }
    })
  },
  globalData: {
    userInfo: null,
    // url: 'http://116.62.54.239:9000',
    url: 'http://localhost:9000',
    token: null,
    runData: []
  }
})
