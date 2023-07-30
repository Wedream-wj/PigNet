<!--支持markdown语法-->
<!--markdown编辑器-->
<template>
    <div style="margin: 10px 20px;">
        标题：<el-input v-model="title" placeholder="请输入文章标题" style="width: 20%;" clearable></el-input>
    </div>
    <v-md-editor v-model="text" height="600px" @save="save"></v-md-editor>
</template>

<script>
    import request from "../utils/request";

    export default {
        name: 'MavonDisplay',
        data() {
            return {
                user: {},
                text: '',
                form: {},
                title: '',
            };
        },
        created() {
            this.load()
            let userStr = sessionStorage.getItem("user") || "{}"
            this.user = JSON.parse(userStr)
        },
        methods: {
            load() {
                this.form.id = this.$route.params.markdownId
                console.log(this.form.id)
                if(this.form.id) {
                    request.get("/markdown/"+this.form.id,{

                    }).then(res=>{
                        console.log(res)
                        this.text=res.content
                        this.form=res
                        this.title=res.title
                    })
                }
            },

            save(text, html) { // 保存text
                // console.log("saving hhh")
                // console.log(text)
                // console.log(html)

                let userStr = sessionStorage.getItem("user") || "{}"
                let user = JSON.parse(userStr)
                this.form.author = user.username
                this.form.content = text
                this.form.html = html
                this.form.title = this.title

                if(this.form.id) { //修改
                    request.put("/markdown", this.form).then(res => {
                        console.log(res)
                        if (res.code === '0') {
                            this.$message({
                                type: "success",
                                message: "保存成功，前往【我的Markdown】查看"
                            })
                        } else {
                            this.$message({
                                type: "error",
                                message: res.msg
                            })
                        }
                    })
                } else { //增加
                    request.post("/markdown", this.form).then(res => {
                        console.log(res)
                        if (res.code === '0') {
                            this.$message({
                                type: "success",
                                message: "保存成功，前往【我的Markdown】查看"
                            })
                        } else {
                            this.$message({
                                type: "error",
                                message: res.msg
                            })
                        }
                    })
                }
            },
        }
    };
</script>

<style scoped>

</style>