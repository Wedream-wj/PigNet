<!--书籍管理-->
<template>
    <div style="padding: 10px;">
        <!--    功能区域-->
        <div style="margin: 10px 0;">
            <el-button v-if="user.role===1" type="primary" @click="add">新增</el-button>
            <el-button type="primary" @click="dealIn">导入</el-button>
            <a href="http://120.79.9.66:9090/book/downloadExcel" style="margin-left: 10px">
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
            <el-table-column
                    prop="id"
                    label="ID"
                    sortable>
            </el-table-column>
            <el-table-column
                    prop="name"
                    label="名称">
            </el-table-column>
            <el-table-column
                    prop="price"
                    label="单价">
            </el-table-column>
            <el-table-column
                    prop="author"
                    label="作者">
            </el-table-column>
            <el-table-column
                    prop="createTime"
                    label="出版时间">
            </el-table-column>
            <el-table-column
                    label="封面">
                <template #default="scope">
                    <el-image
                    style="width: 100px;height: 100px"
                    :src="scope.row.cover"
                    :preview-src-list="[scope.row.cover]">
                    </el-image>
                </template>
            </el-table-column>
            <el-table-column
                    fixed="right"
                    label="操作">
                <template #default="scope" v-if="user.role===1">  <!--            user.role===1才有权限编辑-->
                    <el-button  size="mini" @click="handleEdit(scope.row)" >编辑</el-button>
                    <el-popconfirm @confirm="handleDelete(scope.row.id)"
                                   title="确认删除吗？"
                    >
                        <template #reference>
                            <el-button  size="mini" type="danger" >删除</el-button>
                        </template>
                    </el-popconfirm>
                </template>
                <template #default="scope" v-if="user.role!==1">
                    <el-button  size="mini" >无</el-button>
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

            <el-dialog title="提示" v-model="dialogVisible" width="30%">
                <el-form :model="form" label-width="120px">
                    <el-form-item label="名称">
                        <el-input v-model="form.name" style="width: 80%;"></el-input>
                    </el-form-item>
                    <el-form-item label="价格">
                        <el-input v-model="form.price" style="width: 80%;"></el-input>
                    </el-form-item>
                    <el-form-item label="作者">
                        <el-input v-model="form.author" style="width: 80%;"></el-input>
                    </el-form-item>
                    <el-form-item label="出版时间">
                       <el-date-picker v-model="form.createTime" value-format="YYYY-MM-DD" type="date" style="width: 80%" clearable></el-date-picker>
                    </el-form-item>
                    <el-form-item label="封面">
                        <el-upload ref="upload" :action="filesUploadUrl" :on-success="filesUploadSuccess">
                            <el-button type="primary">点击上传</el-button>
                        </el-upload>
                    </el-form-item>
                </el-form>
                <template #footer>
                <span class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="save">确 定</el-button>
                 </span>
                </template>
            </el-dialog>

        </div>

    </div>
</template>

<script>
    // @ is an alias to /src

    import request from "../utils/request";

    export default {
            name: 'Book',

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
                filesUploadUrl: "http://" + window.server.filesUploadUrl + ":9090/files/upload"
                // filesUploadUrl: "http://" + "localhost" + ":9090/files/upload"
            }
        },

        created() {
            this.load()
            let userStr = sessionStorage.getItem("user") || "{}"
            this.user = JSON.parse(userStr)
        },

        methods: {
            filesUploadSuccess(res) {
                console.log(res)
                this.form.cover = res.data
            },
            load() {
                    request.get("/book",{
                    params: {
                        pageNum: this.currentPage,
                        pageSize: this.pageSize,
                        search: this.search
                    }
                }).then(res=>{
                    console.log(res)
                    this.tableData=res.data.records
                    this.total=res.data.total
                })
            },
            add() {
                this.dialogVisible=true;
                this.form = {}
                if(this.$refs['upload']) {
                    this.$refs['upload'].clearFiles()  //清除历史上传
                }
            },

            save() {
                if(this.form.id) {
                    request.put("/book",this.form).then(res=>{
                        console.log(res)
                        if (res.code==='0') {
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
                        this.load()
                        this.dialogVisible=false
                    })
                } else {
                    request.post("/book",this.form).then(res=>{
                        console.log(res)
                        if (res.code==='0') {
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
                        this.load()
                        this.dialogVisible=false
                    })
                }
            },
            handleEdit(row) {
                this.form = JSON.parse(JSON.stringify(row));
                this.dialogVisible=true;
                this.$nextTick(()=>{
                    if(this.$refs['upload']) {
                        this.$refs['upload'].clearFiles()  //清除历史上传
                    }
                })
            },

            handleDelete(id) {
                console.log(id)
                request.delete("/book/"+id).then(res=> {
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
