<!--知识点易出-->
<template>
<!--    切换最容易考的知识点和不经常考的知识点-->
    <div id="main" style="width:1000px;height:700px;margin: 10px auto;"></div>
</template>
<script>
    import request from "../utils/request";

    const echarts = require('echarts');

    export default{
        data () {
            return {
                search: '',
                currentPage: 1,
                pageSize: 700,
                total: 0,
                title: '校招知识点出题率统计（热门）',
                tableData: [],
                isMax: true,
                data0: [],
                data1: [],
                data2: [],
                dataMap: {},
                dataKey: [],
            };
        },
        created() {

        },
        methods: {
            initCharts () {
                var chartDom = document.getElementById('main');
                var myChart = echarts.init(chartDom);
                var option;


                request.get("/contest",{ // 请求/wordCloud接口
                    params: {
                        pageNum: this.currentPage,
                        pageSize: this.pageSize,
                        search: this.search
                    }
                }).then(res=>{
                    // console.log(res);

                    this.data0=[]
                    this.data1=[]
                    this.data2=[]
                    this.dataMap={}
                    this.dataKey=[]

                    for (var i=0;i<res.data.records.length;i++)
                    {
                        var time=res.data.records[i]['contestTime'];
                        time=time.substr(0,10)
                        // time='2020-'+time
                        if(this.dataMap[time]) {
                            this.dataMap[time]=this.dataMap[time]+1
                        } else {
                            this.dataMap[time]=1
                            this.dataKey.push(time)
                        }
                    }

                    // var max=0;
                    for (var i=0;i<this.dataKey.length;i++)
                    {
                        // if(this.dataMap[this.dataKey[i]]>max) {
                        //     max=this.dataMap[this.dataKey[i]];
                        // }
                        if(this.dataKey[i][3]==='9')
                            this.data0.push([this.dataKey[i],this.dataMap[this.dataKey[i]]])
                        else if(this.dataKey[i][3]==='0')
                            this.data1.push([this.dataKey[i],this.dataMap[this.dataKey[i]]])
                        else if(this.dataKey[i][3]==='1')
                            this.data2.push([this.dataKey[i],this.dataMap[this.dataKey[i]]])
                    }
                    // console.log(max)

                    // console.log(this.data0)

                    // console.log(getVirtulData(2016))

                    function getVirtulData(year) {
                        year = year || '2017';
                        var date = +echarts.number.parseDate(year + '-01-01');
                        var end = +echarts.number.parseDate((+year + 1) + '-01-01');
                        var dayTime = 3600 * 24 * 1000;
                        var data = [];
                        for (var time = date; time < end; time += dayTime) {
                            data.push([
                                echarts.format.formatTime('yyyy-MM-dd', time),
                                Math.floor(Math.random() * 1000)
                            ]);
                        }
                        return data;
                    }


                    option = {
                        title: {
                            top: 10,
                            left: 'center',
                            text: '牛客网举办比赛的热力图',
                            subtext: '数据来自牛客网',
                        },
                        tooltip: {
                            position: 'top',
                            formatter: function (p) {
                                var format = echarts.format.formatTime('yyyy-MM-dd', p.data[0]);
                                return format + ': ' + p.data[1]+'次比赛';
                            }
                        },
                        toolbox: {  // 显示保存图片的按钮
                            show: true,
                            orient: 'horizontal',
                            bottom: 30,
                            left: 20,
                            feature: {
                                // dataView: {readOnly: true},
                                // restore: {},
                                saveAsImage: {}
                            }
                        },
                        visualMap: {
                            min: 0,
                            max: 6,
                            calculable: true,
                            orient: 'vertical',
                            left: '0',
                            top: '300'
                        },

                        calendar: [{
                            top: 100,
                            left: 120,
                            cellSize: [ 'auto',20],
                            orient: 'horizontal',
                            range: '2019'
                        },
                            {
                                top: 300,
                                left: 120,
                                cellSize: [ 'auto',20],
                                orient: 'horizontal',
                                range: '2020'
                            },
                            {
                                top: 500,
                                left: 120,
                                cellSize: [ 'auto',20],
                                // bottom: 10,
                                // orient: 'vertical',
                                range: '2021',
                                dayLabel: {
                                    margin: 5
                                }
                            }],

                        series: [{
                            type: 'heatmap',
                            coordinateSystem: 'calendar',
                            calendarIndex: 0,
                            data: this.data0,
                        }, {
                            type: 'heatmap',
                            coordinateSystem: 'calendar',
                            calendarIndex: 1,
                            data: this.data1,
                        }, {
                            type: 'heatmap',
                            coordinateSystem: 'calendar',
                            calendarIndex: 2,
                            data: this.data2,
                        }]
                    };

                    option && myChart.setOption(option);

                })

            },

            handleCommand(command) {
                if(command==='high') {
                    this.isMax=true;
                    this.title='校招知识点出题率统计（热门）';

                } else {
                    this.isMax=false;
                    this.title='校招知识点出题率统计（偏冷）';
                }
                this.initCharts();
                // console.log(this.type)
            }

        },
        mounted () {
            this.initCharts();
            // console.log("mounted")
        }
    }
</script>

<style scoped>

</style>