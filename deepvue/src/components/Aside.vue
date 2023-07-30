<!--侧边栏组件-->
<template>
    <div id="bd">
        <el-menu
                style="width: 200px; min-height: calc(100vh - 50px);background: rgba(217,238,255,0.18); "
                :unique-opened="true"
                :default-active="path"
                router
                class="el-menu-vertical-demo"
               >

            <el-submenu index="1"  v-if="user.role === 1">
                <template #title >后台管理</template>
<!--                <el-submenu index="1-1" >-->
<!--                    <template #title>系统管理</template>-->
                    <el-menu-item index="/news">公告管理</el-menu-item>
<!--                    <el-menu-item index="/yolo">行为识别</el-menu-item>-->
<!--                    <el-menu-item index="/knowledge">知识点出题率分析</el-menu-item>-->
                    <el-menu-item index="/user" >用户管理</el-menu-item>
<!--                </el-submenu>-->
<!--                <el-submenu index="1-2" >-->
<!--                    <template #title>数据管理</template>-->
<!--                    <el-menu-item index="/bookClassification2">书籍管理</el-menu-item>-->
<!--                    <el-menu-item index="/sojob">招聘信息</el-menu-item>-->
<!--                    <el-menu-item index="/companyRank">企业排行</el-menu-item>-->
<!--                    <el-menu-item index="/citySalary2">城市工资</el-menu-item>-->
<!--                    <el-menu-item index="/practiceMost">专项练习</el-menu-item>-->
<!--                    <el-menu-item index="/itemBank">试题热度</el-menu-item>-->
<!--                    <el-menu-item index="/questionCenter">试题广场</el-menu-item>-->
<!--                </el-submenu>-->
            </el-submenu>

            <el-submenu index="2" v-if="user.role!==1">
                <template #title>资源展示</template>
<!--                <el-menu-item index="/user" >用户管理</el-menu-item>-->
                <el-menu-item index="/news">新闻公告</el-menu-item>
<!--                <el-menu-item index="/BookClassification2">书籍展示</el-menu-item>-->
<!--                <el-menu-item index="/sojob">招聘信息</el-menu-item>-->
<!--                <el-menu-item index="/companyRank">企业排行</el-menu-item>-->
<!--                <el-menu-item index="/citySalary2">城市工资</el-menu-item>-->
<!--                <el-menu-item index="/practiceMost">专项练习</el-menu-item>-->
<!--                <el-menu-item index="/itemBank">试题热度</el-menu-item>-->
<!--                <el-menu-item index="/questionCenter">试题广场</el-menu-item>-->
            </el-submenu>

            <el-submenu index="3" >
                <template #title>实用功能</template>
                <el-menu-item index="/yolo">行为识别</el-menu-item>
            </el-submenu>

<!--            <el-submenu index="4" >-->
<!--                <template #title>就业分析</template>-->
<!--                <el-menu-item index="/scatter">薪资散点图</el-menu-item>-->
<!--                <el-menu-item index="/stackedBar">公司面经统计</el-menu-item>-->
<!--                <el-menu-item index="/scatterClustering">企业梯队分布</el-menu-item>-->
<!--                <el-menu-item index="/citySalary">城市工资对比图</el-menu-item>-->
<!--                <el-menu-item index="/jobCity">城市校招岗位数</el-menu-item>-->
<!--                <el-menu-item index="/chinaMap">百强企业分布图</el-menu-item>-->
<!--                <el-menu-item index="/roseType">招聘常用标签统计</el-menu-item>-->
<!--                <el-menu-item index="/lineRace">编程语言使用率变化</el-menu-item>-->
<!--            </el-submenu>-->

<!--            <el-submenu index="5" >-->
<!--                <template #title>学习指引</template>-->
<!--                <el-menu-item index="/bookClassification">书籍分类旭日图</el-menu-item>-->
<!--                <el-menu-item index="/simpleGraph">计算机专业学习路线图</el-menu-item>-->
<!--                <el-menu-item index="/languageRate">编程语言占比率对比图</el-menu-item>-->
<!--                <el-menu-item index="/game">游戏代码资源语言饼图</el-menu-item>-->
<!--            </el-submenu>-->

<!--            <el-submenu index="6" >-->
<!--                <template #title>实用工具</template>-->
<!--                <el-menu-item index="/previewMarkdown">校招面试合集</el-menu-item>-->
<!--                <el-menu-item index="/mavonDisplay">Markdown编辑器</el-menu-item>-->
<!--                <el-menu-item index="/markDown">我的Markdown</el-menu-item>-->
<!--            </el-submenu>-->

<!--            <el-menu-item index="data" :route="{path: '/'}">数据管理</el-menu-item>-->
        </el-menu>
    </div>
</template>

<script>
    import request from "@/utils/request";

    export default {
        name: "Aside",
        data() {
            return {
                user: {},
                path: this.$route.path  //设置默认高亮的菜单
            }
        },
        created() {
            let userStr = sessionStorage.getItem("user") || "{}"
            this.user = JSON.parse(userStr)

            // 请求服务端，确认当前登录用户的 合法信息
            // request.get("/api/user/" + this.user.id).then(res => {
            //     if (res.code === '0') {
            //         this.user = res.data
            //     }
            // })
        }
    }
</script>



<style scoped>
    #bd{
        /*background: #409EFF;*/
        background-image: url("../assets/wood_pattern_@2X.png");
        /*background-image: url("../assets/xv.png");*/
        background-repeat: no-repeat;
        background-position: left top;
        background-size: auto 100%;
    }
</style>