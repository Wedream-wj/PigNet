<!--找回密码-->
<template>
    <div id="bg">
        <Canvas></Canvas>
        <div id="registerBox">
            <div style="color: #ffffff; font-size: 30px; text-align: center; padding: 30px 0">
                重置密码
            </div>
            <el-form ref="form" :model="form" size="normal" :rules="rules">
                <el-form-item prop="username">
                    <el-input class="inps" prefix-icon="el-icon-user-solid" v-model="form.username" placeholder='请输入用户名'></el-input>
                </el-form-item>
                <el-form-item prop="email">
                    <el-input class="inps" prefix-icon="el-icon-s-platform" v-model="form.email" placeholder='请输入注册时的邮箱'></el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input class="inps" prefix-icon="el-icon-lock" v-model="form.password" show-password placeholder='请输入新密码'></el-input>
                </el-form-item>
                <el-form-item prop="confirm">
                    <el-input class="inps" prefix-icon="el-icon-lock" v-model="form.confirm" show-password placeholder='请再次输入新密码'></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button class="submitBtn" style="width: 100%" type="primary" @click="reset">重置密码</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>

</template>

<script>
    import request from "../utils/request";
    import Canvas from "../components/Canvas";

    export default {
        name: "RetrievePassword",
        components: {Canvas},
        data() {
            return {
                form: {},
                rules: {
                    username: [
                        {required: true, message: '请输入用户名', trigger: 'blur'},
                    ],
                    password: [
                        {required: true, message: '请输入新密码', trigger: 'blur'},
                    ],
                    confirm: [
                        {required: true, message: '请确认新密码', trigger: 'blur'},
                    ],
                    email: [
                        {required: true, message: '请输入邮箱', trigger: 'blur'},
                    ]
                },
            }
        },
        methods: {
            reset() {
                if(this.form.password !== this.form.confirm) {
                    this.$message({
                        type: "error",
                        message: "2次输入密码不一致"
                    })
                    return
                }

                // 邮箱格式验证
                var email=this.form.email;
                console.log(email);
                var reg= /^[a-zA-Z\d]+([-_.][A-Za-z\d]+)*@[a-zA-Z0-9]{1,6}.([c,o,m]{3})|([c,n]{2})$/; //正则表达式
                if(reg.test(email)===false) {
                    this.$message({
                        type: "error",
                        message: "邮箱格式不正确"
                    })
                    return
                }

                this.$refs['form'].validate((valid)=>{
                    if(valid) {
                        request.put("/api/user/retrievePassword",this.form).then(res=> {
                            if (res.code === '0') {
                                this.$message({
                                    type: "success",
                                    message: "重置成功"
                                })
                                this.$router.push("/login")  // 登录成功之后跳转主页
                            } else {
                                this.$message({
                                    type: "error",
                                    message: res.msg
                                })
                                this.$router.push("/retrievePassword")  // 重置失败之后跳回原来网页
                            }
                        })
                    }
                })

            }
        }
    }
</script>

<style >
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
        background-image: url("../assets/pig3.jpg");
        position: relative;}
    #registerBox {
        width: 400px;
        height: 450px;
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
                rgb(245 235 208) 100%
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