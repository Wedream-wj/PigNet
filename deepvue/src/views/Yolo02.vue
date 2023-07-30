<!--Yolo目标检测-->
<template>
    <div style="padding: 10px;">
        <!--    功能区域-->
        <div id="main" style="width:800px;height:320px;margin: 10px auto;"></div>

<!--        <div style="margin: 10px 0; ">-->

<!--        </div>-->

        <div class="leftullidiv">
<!--            <input type="file" class="updata" accept="image/*" @change="change($event)" ref="updata">-->
            <el-button type="primary"  class="updata" @click="handleOpen1">查看图片</el-button>
            <img :src="imageUrl ? imageUrl : baseImg" alt="" class="rightulliimg">

            <div class="open1">

                <input type="file" class="" accept="image/*" @change="change($event)" ref="updata">

                <div style="margin-top: 10px;">
<!--                <el-button type="primary" @click="uploadImg">点击上传</el-button>-->
                <el-button type="primary" style="margin-right: 10px" @click="detect">行为识别</el-button>
<!--                变成行级元素-->
                <div style="display: inline;">
                    <!--            <button @click="handleOpen">打开查看器</button>-->
                    <el-button type="primary" @click="handleOpen1">查看图片</el-button>
                    <duo-image-viewer
                            :src="imageUrl ? imageUrl : baseImg"
                            @close="handleClose1"
                            :showViewer="showViewer1"
                    />
                </div>
                </div>

            </div>


        </div>


        <div class="rightullidiv">
            <el-button type="primary" class="updata" @click="handleOpen2">查看图片</el-button>
            <img :src="imageUrl2 ? imageUrl2 : baseImg2" alt="" class="rightulliimg">

            <div class="open2" style="">
                <!--            <button @click="handleOpen">打开查看器</button>-->
                <el-button type="primary" @click="handleOpen2">查看图片</el-button>
                <el-button :type= buttonType @click="details">详细结果</el-button>
                <duo-image-viewer
                        :src="imageUrl2 ? imageUrl2 : baseImg2"
                        @close="handleClose2"
                        :showViewer="showViewer2"
                />
            </div>
        </div>

        <el-dialog title="详细结果" v-model="vis" width="50%">
            <el-card>
                <div v-html="detJson" style="min-height: 100px;"></div>
            </el-card>
        </el-dialog>

    </div>


</template>

<script>
    // @ is an alias to /src

    import request from "../utils/request";
    const echarts = require('echarts');

    export default {
        name: 'Yolo',

        components: {

        },

        data() {
            return {
                user: {},
                search: '',
                form: {},
                dialogVisible: false,
                currentPage: 1,
                pageSize: 8,
                total: 0,
                tableData: [],
                // 上传的图片
                imageUrl: '',
                // 默认的图片
                baseImg: '',
                // 检测的图片
                imageUrl2: '',
                // 检测的图片
                baseImg2: '',
                vis: false,
                fd: {},
                showViewer1: false,
                showViewer2: false,
                detData: [0,0,0],
                counts: 10,
                detJson: '<p>请先选择图片进行行为识别</p>',
                buttonType: 'primary',
            }
        },

        created() {
            this.load()
            let userStr = sessionStorage.getItem("user") || "{}"
            this.user = JSON.parse(userStr)
        },

        methods: {
            details() {
                this.vis=true
            },
            filesUploadSuccess(res) {
                console.log(res)
                this.form.cover = res.data
            },
            load() {
                // 获取默认显示的图片
                // this.baseImg = 'https://img-blog.csdnimg.cn/a9523af1d2ac41df8e0c32507e80528f.png'
                this.baseImg =  'http://1.12.231.219:8083/results/01.png'
                this.baseImg2 = 'http://1.12.231.219:8083/results/02.png'
            },
            detect() {
                this.$message({
                    type: "success",
                    message: '正在检测中，请耐心等待...'
                })
                // request.get("/deep/yolo",{
                request.get("http://1.12.231.219:8083/yolo",{

                }).then(res=>{
                    console.log(res)
                    this.counts = res.counts
                    this.detData = [0,0,0]

                    for (var i=0;i<res.data.length;i++)
                    {
                        if(res.data[i]['label'] === 'drink')
                            this.detData[0] += 1
                        else if(res.data[i]['label'] === 'stand')
                            this.detData[1] += 1
                        else
                            this.detData[2] += 1
                    }

                    // 字符串拼接详细结果
                    var strDet = JSON.stringify(res.data)
                    // html中<br/>即为换行
                    this.detJson = '一共检测出 <b>'+res.counts+'</b> 头群养猪；<br/>'
                    this.detJson = this.detJson+'其中正在饮水的有 <b>'+this.detData[0]+'</b> 头， '
                        +'正在站立的有 <b>'+this.detData[1]+'</b> 头， '
                        +'正在躺卧的有 <b>'+this.detData[2]+'</b> 头 '+'；<br/><br/>'
                    this.detJson = this.detJson+'详细识别结果按<b>置信度</b>排序如下：<br/>'
                    for (var i=0;i<res.data.length;i++)
                    {
                        if(res.data[i]['label'] === 'drink')
                            this.detJson = this.detJson+'第 <b>'+(i+1)+'</b>头群养猪：'+ 'drink（发生饮水行为），置信度为 <b>'+res.data[i]['confidences']+'</b> ；<br/>'
                        else if(res.data[i]['label'] === 'stand')
                            this.detJson = this.detJson+'第 <b>'+(i+1)+'</b>头群养猪：'+ 'stand（发生站立行为），置信度为 <b>'+res.data[i]['confidences']+'</b> ；<br/>'
                        else
                            this.detJson = this.detJson+'第 <b>'+(i+1)+'</b>头群养猪：'+ 'lie（发生躺卧行为），置信度为 <b>'+res.data[i]['confidences']+'</b> ；<br/>'
                    }
                    this.detJson = this.detJson + '<br/>'
                    // console.log(this.detData)
                    // console.log(this.detJson)



                    this.initCharts();

                    this.imageUrl2=res.resName
                    this.$message({
                        type: "success",
                        message: '检测成功'
                    })

                    this.buttonType = 'success'

                    if(res.counts === 0)
                    {
                        this.$message({
                            type: "error",
                            message: '并未检测到群养猪'
                        })
                    }
                })
            },
            uploadActionUrl() {

            },
            change(e) {
                console.log(e.target.files[0].name);
                // 判断是不是规定格式
                // let name  =  e.target.files[0].name

                // 获取到第一张图片
                let file = e.target.files[0]

                // 创建文件读取对象
                var reader = new FileReader()
                var that = this

                //  将文件读取为DataURL
                reader.readAsDataURL(file)

                // 读取成功调用方法
                reader.onload = e => {
                    console.log('读取成功');

                    // e.target.result 获取 读取成功后的  文件DataURL
                    that.imageUrl = e.target.result

                    // 如果要将图片上传服务器，就在这里调用后台方法
                    // console.log( that.imageUrl)
                    this.form.file=that.imageUrl


                    // request.post("/deep/upload_image",this.form).then(res=>{
                    //     console.log(res)
                    // })
                }

                var fd = new FormData();
                fd.append("file",  e.target.files[0]);
                this.fd=fd
                console.log(fd)

                /* 上传图片 */
                // request.post("/deep/upload_image",this.fd).then(res=>{
                request.post("http://1.12.231.219:8083/upload_image",this.fd).then(res=>{
                    console.log(res)
                    this.$message({
                        type: "success",
                        message: '上传成功'
                    })
                })

            },

            uploadImg() {
                console.log(this.imageUrl)
                if(this.imageUrl==='') {
                    this.$message({
                        type: "error",
                        message: '请先选择图片'
                    })
                    return;
                }

                // request.post("/deep/upload_image",this.fd).then(res=>{
                request.post("http://1.12.231.219:8083/upload_image",this.fd).then(res=>{
                    console.log(res)
                    this.$message({
                        type: "success",
                        message: '上传成功'
                    })
                })
            },


            handleOpen1() {
                if(this.imageUrl==='') {
                    this.$message({
                        type: "error",
                        message: '请先选择图片'
                    })
                    return;
                }
                this.showViewer1 = !this.showViewer1
            },
            handleClose1() {
                this.showViewer1 = false
            },

            handleOpen2() {
                if(this.imageUrl2==='') {
                    this.$message({
                        type: "error",
                        message: '请先进行目标检测'
                    })
                    return;
                }
                this.showViewer2 = !this.showViewer2
            },
            handleClose2() {
                this.showViewer2 = false
            },

            initCharts () {
                var chartDom = document.getElementById('main');
                var myChart = echarts.init(chartDom);
                var option;

                const spirit =
                    'image://data:image/png;base64,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';
                var maxData = this.counts;
                option = {
                    title: { text: '群养猪行为识别结果统计' ,
                        // subtext: '识别结果仅供参考',
                    },
                    tooltip: {},
                    toolbox: {  // 显示保存图片的按钮
                        show: true,
                        orient: 'horizontal',
                        bottom: 40,
                        right: 20,
                        feature: {
                            saveAsImage: {}
                        }
                    },
                    xAxis: {
                        max: maxData,
                        // sum: maxData,
                        splitLine: { show: false },
                        offset: 10,
                        axisLine: {
                            lineStyle: {
                                color: '#999'
                            }
                        },
                        axisLabel: {
                            margin: 10
                        }
                    },
                    yAxis: {
                        data: ['drink(饮水)', 'stand(站立)', 'lie(躺卧)'],
                        inverse: true,
                        axisTick: { show: false },
                        axisLine: { show: false },
                        axisLabel: {
                            margin: 10,
                            color: '#4f58d7',
                            fontSize: 16
                        }
                    },
                    grid: {
                        top: 55,
                        height: 200,
                        left: 100,
                        right: 100
                    },
                    series: [
                        {
                            // current data
                            type: 'pictorialBar',
                            symbol: spirit,
                            symbolRepeat: 'fixed',
                            symbolMargin: '5%',
                            symbolClip: true,
                            symbolSize: 30,
                            symbolBoundingData: maxData,
                            // data: [891, 1220, 660],
                            data: this.detData,
                            markLine: {
                                symbol: 'none',
                                label: {
                                    formatter: 'maxCounts（发生最多行为的数量）: {c}',
                                    position: 'start',
                                    fontSize: 15,
                                    color: '#ff0000',
                                },
                                lineStyle: {
                                    color: 'green',
                                    type: 'dotted',
                                    opacity: 0.2,
                                    width: 2
                                },
                                data: [
                                    {
                                        type: 'max'
                                    }
                                ]
                            },
                            z: 10
                        },
                        {
                            // full data
                            type: 'pictorialBar',
                            itemStyle: {
                                opacity: 0.2
                            },
                            label: {
                                show: true,
                                formatter: function (params) {
                                    return ((params.value / maxData) * 100).toFixed(1) + ' %';
                                },
                                position: 'right',
                                offset: [10, 0],
                                color: 'green',
                                fontSize: 18
                            },
                            animationDuration: 0,
                            symbolRepeat: 'fixed',
                            symbolMargin: '5%',
                            symbol: spirit,
                            symbolSize: 30,
                            symbolBoundingData: maxData,
                            // data: [891, 1220, 660],
                            data: this.detData,
                            z: 5
                        }
                    ]
                };

                option && myChart.setOption(option,true);


            },

        },

        mounted () {
            this.initCharts();
            // console.log("mounted")
        }

    }
</script>

<style scoped>
    .file {
        position: relative;
        left: 50px;
        width: 500px;
        height: 500px;
        background-color: #ccc;
    }
    .vis_pic {
        position: relative;
        top:-580px;
        left: 600px;
        width: 500px;
        height: 500px;
        background-color: #ccc;
    }
    .open1 {
        position: absolute;
        bottom:-70px;
        left: 0;
        /*width: 500px;*/
        /*height: 550px;*/
        /*background-color: #ccc;*/
    }
    .open2 {
        position: absolute;
        bottom:-70px;
        left: 0;
        /*width: 500px;*/
        /*height: 550px;*/
        /*background-color: #ccc;*/
    }
    .updata {
        display: block;
        height: 100%;
        width: 100%;
        opacity: 0;
        position: absolute;
        top: 0;
        left: 0;
        z-index: 10;
    }

    .leftullidiv {
        /*width: 100%;*/
        /*height: 200px;*/
        width: 500px;
        height: 300px;
        background: #f2f2f2;
        position: relative;
        /*display: flex;*/
        margin-left: 80px;
        margin-bottom: 80px;
        float:left;
        display:flex;
        justify-content: center;
        align-items: center;
    }
    .rightullidiv {
        /*width: 100%;*/
        /*height: 200px;*/
        width: 500px;
        height: 300px;
        background: #f2f2f2;
        position: relative;
        /*display: flex;*/
        margin-right: 80px;
        margin-bottom: 80px;
        float:right;
        display:flex;
        justify-content: center;
        align-items: center;
    }
    .rightulliimg {
        /*max-width: 100%;*/
        /*max-height: 200px;*/
        max-width: 500px;
        max-height: 300px;
    }

</style>