<!--用户管理-->
<template>
  <div style="padding: 10px;">
<!--    功能区域-->
    <div style="margin: 10px 0;">
        <el-button type="primary" @click="add">新增</el-button>
        <el-button type="primary" @click="dealIn">导入</el-button>
        <a href="http://120.79.9.66:9090/user/downloadExcel" style="margin-left: 10px">
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
              prop="username"
              label="用户名">
      </el-table-column>
      <el-table-column
              prop="nickName"
              label="昵称">
      </el-table-column>
        <el-table-column
                prop="age"
                label="年龄">
        </el-table-column>
        <el-table-column
                prop="sex"
                label="性别">
        </el-table-column>
        <el-table-column
                prop="email"
                label="邮箱">
        </el-table-column>
        <el-table-column
                label="角色">
            <template #default="scope">
                <span v-if="scope.row.role === 1">管理员</span>
                <span v-if="scope.row.role === 2">普通用户</span>
            </template>
        </el-table-column>
      <el-table-column
              fixed="right"
              label="操作">
        <template #default="scope">
          <el-button v-if="user.role===1" size="mini" @click="handleEdit(scope.row)" >编辑</el-button>
<!--            user.role===1才有权限编辑-->
          <el-popconfirm @confirm="handleDelete(scope.row.id)"
                  title="确认删除吗？"
          >
            <template #reference>
              <el-button v-if="user.role===1" size="mini" type="danger" >删除</el-button>
                <!--            user.role===1才有权限删除-->
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
              :page-sizes="[5, 8,10, 20]"
              :page-size="pageSize"
              layout="total, sizes, prev, pager, next, jumper"
              :total="total">
      </el-pagination>

        <el-dialog title="提示" v-model="dialogVisible" width="30%">
            <el-form :model="form" label-width="120px">
                <el-form-item label="用户名">
                    <el-input v-model="form.username" style="width: 80%;"></el-input>
                </el-form-item>
                <el-form-item label="昵称">
                    <el-input v-model="form.nickName" style="width: 80%;"></el-input>
                </el-form-item>
                <el-form-item label="年龄">
                    <el-input v-model="form.age" style="width: 80%;"></el-input>
                </el-form-item>
                <el-form-item label="性别">
                    <el-radio v-model="form.sex" label="男">男</el-radio>
                    <el-radio v-model="form.sex" label="女">女</el-radio>
                    <el-radio v-model="form.sex" label="未知">未知</el-radio>
                </el-form-item>
                <el-form-item label="邮箱">
                    <el-input v-model="form.email" style="width: 80%;"></el-input>
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
  name: 'Home',

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
      tableData: []
    }
  },

    created() {
      this.load()
      let userStr = sessionStorage.getItem("user") || "{}"
      this.user = JSON.parse(userStr)
    },

    methods: {
    load() {
        request.get("/api/user",{
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
    },

    save() {
        if(this.form.id) {
            request.put("/api/user",this.form).then(res=>{
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
            request.post("/api/user",this.form).then(res=>{
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
    },

    handleDelete(id) {
        console.log(id)
        request.delete("/api/user/"+id).then(res=> {
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
