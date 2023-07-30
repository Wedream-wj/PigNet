import Dialog from '@vant/weapp/dialog/dialog';
Page({

	/**
	 * 页面的初始数据
	 */
	data: {
		userInfo: {},
	},

	/**
	 * 生命周期函数--监听页面加载
	 */
	onLoad: function (options) {
		let userInfo = wx.getStorageSync('userInfo');
		this.setData({
			userInfo: userInfo
		});
	},

	/**
	 * 退出
	 */
	logout() {
		Dialog.confirm({
			message: '是否退出登录？'
		}).then(() => {
			//点击确定
			wx.clearStorageSync();
			this.getTabBar().init();
			wx.switchTab({
				url: '/pages/index/index',
				success: function(e) { //刷新登录页面头像

					var page = getCurrentPages().pop();
					
					if (page == undefined || page == null) return
					
					page.onLoad();
					
					}
			});
		}).catch(() => {
			// on cancel
		});
	},

	  //复制作者博客地址
	  CopyLink(e) {
		wx.setClipboardData({
		  data: e.currentTarget.dataset.link,
		  success: res => {
			wx.showToast({
			  title: '博客链接已复制',
			  duration: 1000,
			})
		  }
		})
	  },

	/**
	 * 生命周期函数--监听页面初次渲染完成
	 */
	onReady: function () {

	},

	/**
	 * 生命周期函数--监听页面显示
	 */
	onShow: function () {
		this.getTabBar().init();
	},

	/**
	 * 生命周期函数--监听页面隐藏
	 */
	onHide: function () {

	},

	/**
	 * 生命周期函数--监听页面卸载
	 */
	onUnload: function () {

	},

	/**
	 * 页面相关事件处理函数--监听用户下拉动作
	 */
	onPullDownRefresh: function () {

	},

	/**
	 * 页面上拉触底事件的处理函数
	 */
	onReachBottom: function () {

	},

	/**
	 * 用户点击右上角分享
	 */
	onShareAppMessage: function () {

	}


});