<!--登录页面-->
<template>
    <div id="bg">
        <Canvas>

        </Canvas>
        <div id="loginBox">
            <div style="color: #ecf5ff; font-size: 30px; text-align: center; padding: 10px 0">
                群养猪行为识别系统<br/>
                欢迎登录
            </div>
            <el-form ref="form" :model="form" size="normal" :rules="rules" label-width="0px">
                <el-form-item prop="username" style="margin-top:40px;">
                    <el-input class="inps" prefix-icon="el-icon-user-solid" v-model="form.username" placeholder='请输入用户名'></el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input class="inps" prefix-icon="el-icon-lock" v-model="form.password" show-password placeholder='请输入密码'></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button class="submitBtn" style="width: 100%" type="primary" @click="login">登 录</el-button>
                </el-form-item>
                <el-form-item>
                    <router-link target="_blank" :to="{path:'/register'}">
                        <el-button class="submitBtn" style="width: 100%" type="primary" @click="login">注 册</el-button>
                    </router-link>
                </el-form-item>
                <el-form-item>
                    <router-link target="_blank" :to="{path:'/retrievePassword'}">
                        <el-button class="submitBtn" style="width: 100%" type="primary" @click="">重置密码</el-button>
                    </router-link>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script>
    import request from "../utils/request";
    import Canvas from "../components/Canvas"
    export default {
        name: "Login",
        components: {Canvas},
        data() {
            return {
                form: {},
                rules: {
                    username: [
                        {required: true, message: '请输入用户名', trigger: 'blur'},
                    ],
                    password: [
                        {required: true, message: '请输入密码', trigger: 'blur'},
                    ]
                },
            }
        },

        methods: {
            login() {
                this.$refs['form'].validate((valid)=>{
                    if(valid) {
                        request.post("/api/user/login2",this.form).then(res=> {
                            if (res.code === '0') {
                                this.$message({
                                    type: "success",
                                    message: "登录成功"
                                })
                                sessionStorage.setItem("user", JSON.stringify(res.data))  // 缓存用户信息
                                this.$router.push("/")  // 登录成功之后跳转主页
                            } else {
                                this.$message({
                                    type: "error",
                                    message: res.msg
                                })
                            }
                        })
                    }
                })
            }

        }
    }
</script>

<style scoped>
    #bg {
        width: 100vw;
        padding: 0;
        margin: 0;
        height: 100vh;
        font-size: 16px;
        background-repeat: no-repeat;
        background-position: left top;
        background-color: #242645;
        color: #fff;
        font-family: "Source Sans Pro";
        background-size: 100% 100%;
        background-image: url("../assets/pig5.jpg");
        position: relative;}
    #loginBox {
        width: 400px;
        height: 500px;
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        margin: auto;
        padding: 50px 40px 40px 40px;
        box-shadow: -15px 15px 15px rgba(169,174,186, 0.7);
        opacity: 1;
        background: linear-gradient(
                230deg,
                rgba(53, 57, 74, 0) 0%,
                rgb(125,150,182) 100%
        );}
    inps input {
        border: none;
        color: #fff;
        background-color: transparent;
        font-size: 12px;
    }
    .submitBtn {
        background-color: #4bb3dd;
        color: #f2f6fc;
        width: 200px;
    }
    .iconfont {
        color: #fff;
    }

</style>