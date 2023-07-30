import Toast from '@vant/weapp/toast/toast';
Component({
    data: {
        active: 0,
        show: true,
        list: [
            {
                pagePath: "/pages/index/index",
                text: "登录",
                icon: 'smile',
            },
            /*{
                pagePath: "/pages/goods/goods",
                text: "商品",
                icon: 'shopping-cart'
            },*/
            {
                pagePath: "/pages/detect/detect",
                text: "行为识别",
                icon: 'fire'
            },
            /*{
                pagePath: "/pages/fire/fire",
                text: "我的运动",
                icon: 'fire'
            },*/
            {
                pagePath: "/pages/user/user",
                text: "个人中心",
                icon: 'gem'
            },
        ]
    },
    methods: {
        /**
         * 用户点击导航栏触发
         * @param {*} event 
         */
        onChange(event) {
            // event.detail 的值为当前选中项的索引
            let userInfo = wx.getStorageSync('userInfo');
            if(!userInfo) {
                console.log("请先授权登录")
                return Toast.fail('请先授权登录');
            } else {
                this.setData({
                    active: event.detail 
                });
                //页面切换
                wx.switchTab({
                    url: this.data.list[event.detail].pagePath,
                });
            }
        },

        init() {
            /*let token = wx.getStorageSync('token');
            if (!token) {
                this.setData({
                    show: false
                });
            } else {
                this.setData({
                    show: true
                });
            }*/
            // 注释显示底部侧边栏
            const page = getCurrentPages().pop();
            this.setData({
        　      active: this.data.list.findIndex(item => item.pagePath === `/${page.route}`)
            });
        }
    }
});