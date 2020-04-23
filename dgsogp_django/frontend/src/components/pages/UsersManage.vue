<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-people"></i> 用户管理
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-row class="handle-box">
                <el-col :span="8">
                    <el-input v-model="query.key" placeholder="" class="input-with-select">
                        <el-select v-model="query.select" slot="prepend" placeholder="请选择" style="width: 130px;">
                          <el-option label="ID" value="id"></el-option>
                          <el-option label="用户名" value="username"></el-option>
                          <el-option label="用户昵称" value="nickname"></el-option>
                        </el-select>
                        <el-button type="primary" icon="el-icon-search" @click="handleSearch" slot="append">搜索</el-button>
                    </el-input>
                </el-col>
                <el-col :span="1">
                    &nbsp;
                </el-col>
                <el-col :span="2">
                    <el-button type="primary" icon="el-icon-add" @click="handleRegister" >添加用户</el-button>
                </el-col>
            </el-row>
            <el-table
                :data="tableData"
                border
                class="table"
                ref="multipleTable"
                header-cell-class-name="table-header"
            >
                <el-table-column prop="id" label="ID" width="55" align="center"></el-table-column>
                <el-table-column prop="username" label="用户名"></el-table-column>
                <el-table-column prop="nickname" label="用户昵称"></el-table-column>
                <el-table-column label="密码操作" width="180" align="center">
                    <template slot-scope="scope">
                        <el-button
                                type="text"
                                icon="el-icon-edit"
                                @click="handlePassword(scope.row)"
                            >修改</el-button>
                        <el-button
                                type="text"
                                icon="el-icon-edit"
                                class="red"
                                @click="handleForcePassword(scope.row)"
                            >强制修改</el-button>
                    </template>
                </el-table-column>
                <el-table-column prop="created_at" label="注册时间"></el-table-column>
                <el-table-column label="操作" width="180" align="center">
                    <template slot-scope="scope">
                        <el-button
                            type="text"
                            icon="el-icon-edit"
                            @click="handleEdit(scope.row)"
                        >编辑</el-button>
                        <el-button
                            type="text"
                            icon="el-icon-delete"
                            class="red"
                            @click="handleDelete(scope.row)"
                        >删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <div class="pagination">
                <el-pagination
                    background
                    layout="total, prev, pager, next"
                    :current-page="query.pageIndex"
                    :page-size="query.pageSize"
                    :total="pageTotal"
                    @current-change="handlePageChange"
                ></el-pagination>
            </div>
        </div>

        <!-- 编辑弹出框 -->
        <el-dialog title="编辑" :visible.sync="editVisible" width="30%">
            <el-form ref="form" :model="form.data" label-width="70px">
                <el-form-item label="用户昵称">
                    <el-input v-model="form.data.nickname"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit(form.data.id)">确 定</el-button>
            </span>
        </el-dialog>

        <!-- 修改密码弹出框 -->
        <el-dialog title="修改密码" :visible.sync="passwordVisible" width="30%">
            <el-form ref="form" :model="form.data" label-width="70px">
                <el-form-item label="旧密码">
                    <el-input v-model="form.data.oldpassword"></el-input>
                </el-form-item>
                <el-form-item label="新密码">
                    <el-input v-model="form.data.newpassword"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="passwordVisible = false">取 消</el-button>
                <el-button type="primary" @click="savePassword(form.data.id)">确 定</el-button>
            </span>
        </el-dialog>

        <!-- 强制修改密码弹出框 -->
        <el-dialog title="强制修改密码" :visible.sync="forcepasswordVisible" width="30%">
            <el-form ref="form" :model="form.data" label-width="70px">
                <el-form-item label="新密码">
                    <el-input v-model="form.data.newpassword"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="forcepasswordVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveForcePassword(form.data.id)">确 定</el-button>
            </span>
        </el-dialog>

        <!-- 添加用户弹出框 -->
        <el-dialog title="添加用户" :visible.sync="registerVisible" width="30%">
            <el-form ref="form" :model="form.data" label-width="70px">
                <el-form-item label="用户名">
                    <el-input v-model="form.data.username"></el-input>
                </el-form-item>
                <el-form-item label="用户昵称">
                    <el-input v-model="form.data.nickname"></el-input>
                </el-form-item>
                <el-form-item label="用户密码">
                    <el-input v-model="form.data.password"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="registerVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveRegister">确 定</el-button>
            </span>
        </el-dialog>

    </div>
</template>

<script>
export default {
    name: 'UsersManage',
    data() {
        return {
            query: {
                select:'',
                key:'',
                pageIndex: 1,
                pageSize: 10
            },
            tableData: [],
            editVisible: false,
            passwordVisible: false,
            forcepasswordVisible: false,
            registerVisible: false,
            pageTotal: 0,
            form: {
                data:{
                    id:'',
                    username:'',
                    nickname:'',
                    password:'',
                    oldpassword:'',
                    newpassword:'',
                },
            },
        };
    },
    mounted() {
        this.getData();
    },
    methods: {
        getData() {
            let key = this.query
            if (key.select&&key.key) {
                
            } else {
                key.select=''
                key.key=''
            }
            var me = this
            this.$get(`/users?pageIndex=${key.pageIndex}&pageSize=${key.pageSize}&select=${key.select}&key=${key.key}`).then(res=>{
                me.tableData = res.data.data
                me.pageTotal = res.data.total
            }).catch(function(err){
                console.log(err)
            })
        },
        // 触发搜索按钮
        handleSearch() {
            this.getData();
        },
        // 删除操作
        handleDelete(row) {
            // 二次确认删除
            let id = row.id
            this.$confirm('确定要删除吗？', '提示', {
                type: 'warning'
            }).then(() => {
                let me = this
                this.$delete(`/users/${id}`).then(res=>{
                    if(res.data.error == 0){
                        me.$message.success('删除成功');
                        me.getData()
                    } else {
                        me.$message.error('删除失败，' + res.data.detail)
                        console.log(res.data.detail)
                        return
                    }
                }).catch(function(err){
                    console.log(err)
                })
            }).catch(function(err){
                console.log(err)
            })
        },
        // 编辑操作
        handleEdit(row) {
            this.form.data.id = row.id;
            this.form.data.nickname = row.nickname;
            this.editVisible = true;
        },
        // 保存编辑
        saveEdit(id) {
            let key = {}
            if(this.form.data.nickname){
                key.nickname=this.form.data.nickname
            } else {
                this.$message.error('请完整填写信息')
                return
            }
            this.editVisible = false;
            let me = this
            this.$put(`/users/${id}`, key).then(res=>{
                if(res.data.error == 0){
                    me.$message.success('修改成功')
                    me.getData();
                } else {
                    me.$message.error('修改失败，' + res.data.detail)
                    console.log(res.data.detail)
                    return
                }
            }).catch(function(err){
                console.log(err)
            })
        },
        //修改密码
        handlePassword(row) {
            this.form.data.id = row.id;
            this.passwordVisible = true;
        },
        //保存密码
        savePassword(id) {
            let key = {}
            if(this.form.data.oldpassword&&this.form.data.newpassword){
                key.oldpassword=this.form.data.oldpassword
                key.newpassword=this.form.data.newpassword
            } else {
                this.$message.error('请完整填写信息')
                return
            }
            this.passwordVisible = false;
            this.form.data.oldpassword=''
            this.form.data.newpassword=''
            let me = this
            this.$put(`/users/password/${id}`, key).then(res=>{
                if(res.data.error == 0){
                    me.$message.success('修改成功')
                } else {
                    me.$message.error('修改失败，' + res.data.detail)
                    console.log(res.data.detail)
                    return
                }
            }).catch(function(err){
                console.log(err)
            })
        },
        //强制修改密码
        handleForcePassword(row) {
            this.form.data.id = row.id;
            this.forcepasswordVisible = true;
        },
        saveForcePassword(id) {
            let key = {}
            if(this.form.data.newpassword){
                key.newpassword=this.form.data.newpassword
            } else {
                this.$message.error('请完整填写信息')
                return
            }
            this.forcepasswordVisible = false;
            this.form.data.newpassword=''
            let me = this
            this.$put(`/users/forcepassword/${id}`, key).then(res=>{
                if(res.data.error == 0){
                    me.$message.success('修改成功')
                } else {
                    me.$message.error('修改失败，' + res.data.detail)
                    console.log(res.data.detail)
                    return
                }
            }).catch(function(err){
                console.log(err)
            })
        },
        //添加用户
        handleRegister() {
            this.registerVisible = true;
        },
        //保存添加用户
        saveRegister() {
            let key = {}
            if(this.form.data.username&&this.form.data.nickname&&this.form.data.password){
                key.username=this.form.data.username
                key.nickname=this.form.data.nickname
                key.password=this.form.data.password
            } else {
                this.$message.error('请完整填写信息')
                return
            }
            this.registerVisible = false
            this.form.data.username=''
            this.form.data.nickname=''
            this.form.data.password=''
            let me = this
            this.$post("/users", key).then(res=>{
                if(res.data.error == 0){
                    me.$message.success('添加成功')
                    me.getData();
                } else {
                    me.$message.error('添加失败，' + res.data.detail)
                    console.log(res.data.detail)
                    return
                }
            }).catch(function(err){
                console.log(err)
            })
        },
        // 分页导航
        handlePageChange(val) {
            this.$set(this.query, 'pageIndex', val);
            this.getData();
        }
    }
};
</script>

<style scoped>
.handle-box {
    margin-bottom: 20px;
}

.handle-select {
    width: 120px;
}

.handle-input {
    width: 300px;
    display: inline-block;
}
.table {
    width: 100%;
    font-size: 14px;
}
.red {
    color: #ff0000;
}
.mr10 {
    margin-right: 10px;
}
.table-td-thumb {
    display: block;
    margin: auto;
    width: 40px;
    height: 40px;
}
</style>
