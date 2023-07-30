<!--折线图堆叠-->
<template>
    <div id="main" style="margin: 10px auto;width: 800px;height: 800px;"></div>
</template>
<script>
    import request from "../utils/request";
    //
    const echarts = require('echarts');
    //
    export default {
        name: "Test",
        data () {
            return {
                name:[],
                value:[]
                // interviewNum:[],
                // commentNum:[],
                // questionNum:[],
                // array3:[],
                // array4:[],
                // array5:[]
            }
        },
        mounted(){
            this.initChart();
        },
        methods: {
            initChart(){
                var chartDom = document.getElementById('main');
                var myChart = echarts.init(chartDom);
                var option;
                var dataAxis = ['点', '击', '柱', '子', '或', '者', '两', '指', '在', '触', '屏', '上', '滑', '动', '能', '够', '自', '动', '缩', '放'];
                var data = [220, 182, 191, 234, 290, 330, 310, 123, 442, 321, 90, 149, 210, 122, 133, 334, 198, 123, 125, 220];
                var yMax = 500;
                var dataShadow = [];
                for (var i = 0; i < data.length; i++) {
                    dataShadow.push(yMax);
                }
                // var hours = ['0', '1', '2', '3', '4', '5', '6',
                //     '7', '8', '9','10','11',
                //     '12', '13', '14', '15', '16', '17',
                //     '18', '19', '20', '21', '22', '23'];
                // var days = ['0', '1', '2', '3', '4', '5', '6',
                //     '7', '8', '9','10','11',
                //     '12', '13', '14', '15', '16', '17',
                //     '18', '19', '20', '21', '22', '23'];
                //
                // var data;


                request.get("/sojob/city",{
                    params: {
                        pageNum: this.currentPage,
                        pageSize: this.pageSize,
                        search: this.search
                    }
                }).then(res=> {
                    // this.data2 = [];
                    for (let i = 0; i < 21; i++) {
                        this.name[i]=res.data.records[i].name;
                        this.value[i]=Number(res.data.records[i].value);

                        // console.log(str1[i]);
                        // this.interviewNum[i]=Number(res.data.records[i].interviewNum);
                        // this.commentNum[i]=Number(res.data.records[i].commentNum);
                        // this.questionNum[i]=Number(res.data.records[i].questionNum);


                        // console.log(this.company[i])

                    }
                    option = {
                        xAxis: {
                            type: 'category',
                            data: this.name,
                            axisLabel: {interval: 0, rotate: 50},
                        },
                        yAxis: {
                            type: 'value'
                        },
                        series: [{
                            data: this.value,
                            type: 'bar',
                            showBackground: true,
                            backgroundStyle: {
                                color: 'rgba(180, 180, 180, 0.2)'
                            }
                        }]
                    };

                    option && myChart.setOption(option);
                })

            },
        }
    }
</script>

<style scoped>

</style>