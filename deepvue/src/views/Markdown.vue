<!--我的Markdown-->
<template>
    <div style="padding: 10px;">
        <!--    功能区域-->
        <div style="margin: 10px 0;">
            <el-button v-if="user.role===1" type="primary" @click="add">新增</el-button>
            <el-button type="primary" @click="dealIn">导入</el-button>
            <a :href=excelDownloadUrl style="margin-left: 10px">
                <el-button type="primary" @click="dealOut">导出</el-button>
            </a>
        </div>
        <!--    搜索区域-->
        <div style="margin: 10px 0;">
            <el-input v-model="search" placeholder="请输入关键字" style="width: 20%;" clearable></el-input>
            <el-button type="primary" @click="load" style="margin-left: 5px;"> 查询</el-button>
        </div>
        <el-table
                :data="tableData"
                border
                stripe
                style="width: 100%">
<!--            <el-table-column-->
<!--                    prop="id"-->
<!--                    label="ID"-->
<!--                    sortable>-->
<!--            </el-table-column>-->
            <el-table-column
                    prop="title"
                    label="标题">
            </el-table-column>
            <el-table-column
                    prop="author"
                    label="作者">
            </el-table-column>
            <el-table-column
                    prop="time"
                    label="时间">
            </el-table-column>
            <el-table-column
                    fixed="right"
                    label="操作">
                <template #default="scope" >
                    <el-button size="mini" @click="details(scope.row)" >详情</el-button>
                    <el-button size="mini" @click="handleEdit(scope.row)" >编辑</el-button>
                    <el-popconfirm @confirm="handleDelete(scope.row.id)"
                                   title="确认删除吗？"
                    >
                        <template #reference>
                            <el-button size="mini" type="danger" >删除</el-button>
                        </template>
                    </el-popconfirm>
                </template>

            </el-table-column>
        </el-table>

        <div style="margin: 10px 0;">
            <el-pagination
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="currentPage"
                    :page-sizes="[5, 10, 20]"
                    :page-size="pageSize"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="total">
            </el-pagination>

            <el-dialog title="提示" v-model="dialogVisible" width="50%">
                <el-form :model="form" label-width="120px">
                    <el-form-item label="标题">
                        <el-input v-model="form.title" style="width: 50%;"></el-input>
                    </el-form-item>
                    <div id="div1">

                    </div>
                    <!--                    <el-form-item label="价格">-->
                    <!--                        <el-input v-model="form.price" style="width: 80%;"></el-input>-->
                    <!--                    </el-form-item>-->
                </el-form>
                <template #footer>
                <span class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="save">确 定</el-button>
                 </span>
                </template>
            </el-dialog>

        </div>

        <el-dialog title="详情" v-model="vis" width="50%">
            <el-card>
<!--                <div v-html="detail.html" style="min-height: 100px;"></div>-->
                <v-md-preview :text="detail.content"></v-md-preview>
            </el-card>
        </el-dialog>

    </div>
</template>

<script>
    // @ is an alias to /src
    import request from "../utils/request";

    let editor;

    export default {
        name: 'Markdown',

        components: {

        },

        data() {
            return {
                user: {},
                search: '',
                form: {},
                dialogVisible: false,
                currentPage: 1,
                pageSize: 10,
                total: 0,
                tableData: [],
                // user: {},
                detail: {},
                vis: false,
                excelDownloadUrl: "http://" + window.server.filesUploadUrl + ":9090/markdown/downloadExcel",
            }
        },

        created() {
            let userStr = sessionStorage.getItem("user") || "{}"
            this.user = JSON.parse(userStr)
            this.load()
        },

        // mounted() {
        //
        // },

        methods: {
            details(row) {
                this.detail=row
                this.vis=true
            },
            load() {
                request.get("/markdown",{
                    params: {
                        pageNum: this.currentPage,
                        pageSize: this.pageSize,
                        search: this.user.username
                    }
                }).then(res=>{
                    console.log(res)
                    this.tableData=res.data.records
                    this.total=res.data.total
                })
            },
            add() {
                this.$router.push("/mavonDisplay")  // 跳转到编辑页面
            },

            save() {  // 这里不用save方法
                this.form.content = editor.txt.html()  // 获取 编辑器里面的值，然后赋予到实体当中

                if (this.form.id) {  // 更新
                    request.put("/markdown", this.form).then(res => {
                        console.log(res)
                        if (res.code === '0') {
                            this.$message({
                                type: "success",
                                message: "更新成功"
                            })
                        } else {
                            this.$message({
                                type: "error",
                                message: res.msg
                            })
                        }
                        this.load() // 刷新表格的数据
                        this.dialogVisible = false  // 关闭弹窗
                    })
                }  else {  // 新增
                    let userStr = sessionStorage.getItem("user") || "{}"
                    let user = JSON.parse(userStr)
                    this.form.author = user.username
                    this.form.content = text
                    this.form.html = html
                    this.form.title = this.title

                    request.post("/markdown", this.form).then(res => {
                        console.log(res)
                        if (res.code === '0') {
                            this.$message({
                                type: "success",
                                message: "新增成功"
                            })
                        } else {
                            this.$message({
                                type: "error",
                                message: res.msg
                            })
                        }

                        this.load() // 刷新表格的数据
                        this.dialogVisible = false  // 关闭弹窗
                    })
                }

            },

            handleEdit(row) {
                this.form = JSON.parse(JSON.stringify(row))
                // this.$router.push("/mavonDisplay")
                this.$router.push({name: 'MavonDisplay', params: {markdownId: this.form.id}})  // 'name属性router/index.js'
            },

            handleDelete(id) {
                console.log(id)
                request.delete("/markdown/"+id).then(res=> {
                    if (res.code==='0') {
                        this.$message({
                            type: "success",
                            message: "删除成功"
                        })
                    } else {
                        this.$message({
                            type: "error",
                            message: res.msg
                        })
                    }
                    this.load()
                })
            },

            handleSizeChange(pageSize) { // 改变当前每页的个数触发
                this.pageSize=pageSize
                this.load()
            },

            handleCurrentChange(pageNum) { // 改变当前页码触发
                this.currentPage=pageNum
                this.load()
            },
            dealOut() {
                this.$message({
                    type: "success",
                    message: "导出成功"
                })
            },
            dealIn() {
                this.$message({
                    type: "error",
                    message: "导入功能敬请期待"
                })
            },

        }

    }
</script>
