const app = getApp();
import Toast from '@vant/weapp/toast/toast';
Page({

	/**
	 * 页面的初始数据
	 */
	data: {
		userInfo: {
			nickName: '',
			sex: 0,
			address: '',
			avatarUrl: 'https://img-blog.csdnimg.cn/2c5d951ad8e24a7fa2b9460c6628861a.jpg',
		},
		// isAccept: false,
		phoneNumber: '',
		msgCode: '',
		smsText: '发送验证码',
		//是否可以点击
		disabled: false,
		token: null,
		//用户点击tabbar
		active: 0,
		//食物类型列表
		foodList: [],
	},

	/**
	 * 微信用户确认授权
	 */
	getAgree() {
		wx.getUserProfile({
			desc: '用于完善会员资料',
			lang: 'zh_CN',
			success: (res) => {
				//拿到用户信息
				let user = res.userInfo;
				console.log(user);
				//昵称
				let nickName = user.nickName;
				//性别
				let sex = user.gender;
				//地址
				let address = user.country + user.province + user.city;
				//头像
				let avatarUrl = user.avatarUrl;
				//用户信息
				this.data.userInfo = {
					nickName: nickName,
					sex: sex,
					address: address,
					avatarUrl: avatarUrl
				};
				console.log(this.data.userInfo)
				console.log('avURL=>'+this.data.userInfo.avatarUrl)
				this.data.avatarUrl=avatarUrl;
				//获取到用户信息后登录
				wx.login({
					success: (res) => {
						if (res.code) {
							//使用请求码发送请求
							console.log('[test...]登录成功 --> ');
							wx.setStorageSync('userInfo', this.data.userInfo);
							this.onLoad();
							return Toast.success('授权登录成功');
						} else {
							console.log('[test...]登录失败 --> ' + res.errMsg);
						}
					}
				});

			}
		});
	},

		/**
	 * 生命周期函数--监听页面加载
	 */
	onLoad: function (options) {
		let userInfo = wx.getStorageSync('userInfo');
		// console.log('111'+userInfo)
		if(userInfo) {
			this.setData({
				userInfo: userInfo
			});
		} else {
			this.setData({
				userInfo: {
					nickName: '',
					sex: 0,
					address: '',
					avatarUrl: 'https://img-blog.csdnimg.cn/2c5d951ad8e24a7fa2b9460c6628861a.jpg',
				}
			});
		}
	},

	/**
	 * 生命周期函数--监听页面初次渲染完成
	 */
	onReady: function () {
		// this.getAgree()
	},

	/**
	 * 生命周期函数--监听页面显示
	 */
	onShow: function () {
		let token = wx.getStorageSync('token');
		this.setData({
			token: token
		});
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
})