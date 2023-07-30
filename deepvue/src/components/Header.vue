<!--头部组件-->
<template>
    <div id="hd" style="height: 80px; line-height: 100px; border-bottom: 1px solid #ccc; display: flex">
        <div id="logo" style="width: 270px; padding-left: 30px; font-weight: bold; color: #ffffff; font-family:STKaiti"></div>
        <div style="flex: 1;padding-left: 10px; font-weight: bold; color: #ffffff; font-family:STKaiti;font-size: 20px">群养猪行为识别系统</div>
        <div style="width: 100px;float: right">
            <el-dropdown>
                <span class="el-dropdown-link fontstyle">
                    {{ user.nickName }}<i class="el-icon-arrow-down el-icon--right"></i>
                </span>
                <template #dropdown>
                    <el-dropdown-menu>
                        <el-dropdown-item @click="$router.push('/person')">个人信息</el-dropdown-item>
                        <el-dropdown-item @click="$router.push('/login')">退出系统</el-dropdown-item>
                    </el-dropdown-menu>
                </template>
            </el-dropdown>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Header",
        data() {
            return {
                user: {}
            }
        },
        created() {
            let str = sessionStorage.getItem("user") || "{}"
            this.user = JSON.parse(str)
        }
    }
</script>

<style scoped>
    .fontstyle {
        /*line-height: 5em;*/
        /*font-family: Verdana, Geneva, sans-serif;*/
        /*font-size: 15px;*/
        color: #ffffff;
    }
    #hd{
        /*background: #409EFF;*/
        background-image: url("../assets/cork-board.png");
        /*background-image: url("../assets/trees.png");*/
        background-repeat: no-repeat;
        background-position: left top;
        background-size:  100%  100%;
    }
    #logo{
        /*background-image: url("../assets/head_bg.png");*/
        background-image: url("../assets/logo2.svg");
        background-repeat: no-repeat;
        background-position: left top;
        /*background-size:  100% ;*/
        background-size: 80% 100%;
        overflow: hidden;
        margin-top: 17.5px;
    }
</style>