<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-location"></i> 数据源管理
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-row class="handle-box">
                <el-col :span="8">
                    <el-input v-model="query.key" placeholder="" class="input-with-select">
                        <el-select v-model="query.select" slot="prepend" placeholder="请选择" style="width: 130px;">
                          <el-option label="ID" value="id"></el-option>
                          <el-option label="工作组" value="wgroup"></el-option>
                          <el-option label="工作服务器" value="wserver"></el-option>
                          <el-option label="数据源类型" value="type"></el-option>
                          <el-option label="路径/数据库" value="source"></el-option>
                          <el-option label="是否入库" value="putindb"></el-option>
                          <el-option label="结构存储形式" value="related"></el-option>
                          <el-option label="采集模式" value="pattern"></el-option>
                          <el-option label="hadoop路径" value="target"></el-option>
                          <el-option label="处理状态" value="state"></el-option>
                          <el-option label="备注" value="content"></el-option>
                          <el-option label="异常状态" value="excepted"></el-option>
                        </el-select>
                        <el-button type="primary" icon="el-icon-search" @click="handleSearch" slot="append">搜索</el-button>
                    </el-input>
                </el-col>
                <el-col :span="1">
                    &nbsp;
                </el-col>
                <el-col :span="2">
                    <el-button type="primary" icon="el-icon-lx-add" @click="handleCreate">添加数据源</el-button>
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
                <el-table-column prop="wgroup" label="工作组"></el-table-column>
                <el-table-column prop="wserver" label="工作服务器"></el-table-column>
                <el-table-column prop="type" label="数据源类型">
                    <template slot-scope="scope">
                        {{
                            scope.row.type == '0' ? "文件" :
                            scope.row.type == '1' ? "目录" :
                            scope.row.type == '2' ? "数据库" : "无"
                        }}
                    </template>
                </el-table-column>
                <el-table-column prop="source" label="路径/数据库"></el-table-column>
                <el-table-column prop="putindb" label="入库需求">
                    <template slot-scope="scope">
                        {{
                            scope.row.putindb == '0' ? "是" :
                            scope.row.putindb == '1' ? "否" : "无"
                        }}
                    </template>
                </el-table-column>
                <el-table-column prop="related" label="结构存储形式">
                    <template slot-scope="scope">
                        {{
                            scope.row.related == '0' ? "关系型" :
                            scope.row.related == '1' ? "非关系型" : "无"
                        }}
                    </template>
                </el-table-column>
                <el-table-column prop="pattern" label="采集模式">
                    <template slot-scope="scope">
                        {{
                            scope.row.pattern == '0' ? "只采集一次" :
                            scope.row.pattern == '1' ? "每天采集一次" : "无"
                        }}
                    </template>
                </el-table-column>
                <el-table-column prop="target" label="Hadoop路径"></el-table-column>
                <el-table-column prop="state" label="处理状态">
                    <template slot-scope="scope">
                        {{
                            scope.row.state == '0' ? "未采集" :
                            scope.row.state == '1' ? "持续采集中" :
                            scope.row.state == '2' ? "已完成" : "无"
                        }}
                    </template>
                </el-table-column>
                <el-table-column prop="content" label="备注"></el-table-column>
                <el-table-column prop="excepted" label="异常状态">
                    <template slot-scope="scope">
                        {{
                            scope.row.excepted == '0' ? "正常" :
                            scope.row.excepted == '1' ? "异常" : "无"
                        }}
                    </template>
                </el-table-column>
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
        <el-dialog title="编辑" :visible.sync="editVisible" width="40%">
            <el-form ref="form" :model="form.data" label-width="100px">
                <el-form-item label="工作组">
                    <span>{{form.data.wgroup}}</span>
                </el-form-item>
                <el-form-item label="工作服务器">
                    <span>{{form.data.wserver}}</span>
                </el-form-item>
                <el-form-item label="数据源类型">
                    <span>
                        {{
                            form.data.type == '0' ? "文件" :
                            form.data.type == '1' ? "目录" :
                            form.data.type == '2' ? "数据库" : "无"
                        }}
                    </span>
                </el-form-item>
                <el-form-item label="路径/数据库">
                    <span>{{form.data.source}}</span>
                </el-form-item>
                <el-form-item label="入库需求">
                    <span>
                        {{
                            form.data.putindb == '0' ? "是" :
                            form.data.putindb == '1' ? "否" : "无"
                        }}
                    </span>
                </el-form-item>
                <el-form-item label="存储结构形式">
                    <span>
                        {{
                            form.data.related == '0' ? "关系型" :
                            form.data.related == '1' ? "非关系型" : "无"
                        }}
                    </span>
                </el-form-item>
                <el-form-item label="采集模式">
                    <span>
                        {{
                            form.data.pattern == '0' ? "只采集一次" :
                            form.data.pattern == '1' ? "一天采集一次" : "无"
                        }}
                    </span>
                </el-form-item>
                <el-form-item label="Hadoop路径">
                    <span>{{form.data.target}}</span>
                </el-form-item>
                <el-form-item label="处理状态">
                    <el-select v-model="form.data.finish" placeholder="请选择" v-if="form.data.state==1">
                        <el-option key="0" label="持续采集中" value="false"></el-option>
                        <el-option key="1" label="已完成" value="true"></el-option>
                    </el-select>
                    <span v-else>
                        {{
                            form.data.state == '0' ? "未采集" :
                            form.data.state == '2' ? "已完成" : "无"
                        }}
                    </span>
                </el-form-item>
                <el-form-item label="备注">
                    <el-input v-model="form.data.content"></el-input>
                </el-form-item>
                <el-form-item label="异常状态">
                    <span>
                        {{
                            form.data.excepted == '0' ? "正常" :
                            form.data.excepted == '1' ? "异常" : "无"
                        }}
                    </span>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit(form.data.id)">确 定</el-button>
            </span>
        </el-dialog>

        <!-- 添加弹出框 -->
        <el-dialog title="添加数据源" :visible.sync="createVisible" width="40%">
            <el-form ref="form" :model="form.data" label-width="100px">
                <el-form-item label="工作组">
                    <el-input v-model="form.data.wgroup"></el-input>
                </el-form-item>
                <el-form-item label="工作服务器">
                    <el-input v-model="form.data.wserver"></el-input>
                </el-form-item>
                <el-form-item label="数据源类型">
                    <el-select v-model="form.data.type" placeholder="请选择">
                        <el-option key="0" label="文件" value="0"></el-option>
                        <el-option key="1" label="目录" value="1"></el-option>
                        <el-option key="2" label="数据库" value="2"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="路径/数据库">
                    <el-input v-model="form.data.source"></el-input>
                </el-form-item>
                <el-form-item label="入库需求" v-if="form.data.type!=2">
                    <el-select v-model="form.data.putindb" placeholder="请选择">
                        <el-option key="0" label="入库" value="0"></el-option>
                        <el-option key="1" label="无需入库" value="1"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="存储结构形式">
                    <el-select v-model="form.data.related" placeholder="请选择">
                        <el-option key="0" label="关系型" value="0"></el-option>
                        <el-option key="1" label="非关系型" value="1"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="采集模式" v-if="form.data.type!=2">
                    <el-select v-model="form.data.pattern" placeholder="请选择">
                        <el-option key="0" label="只采集一次" value="0"></el-option>
                        <el-option key="1" label="一天采集一次" value="1"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="Hadoop路径" v-if="form.data.type!=2">
                    <el-input v-model="form.data.target"></el-input>
                </el-form-item>
                <el-form-item label="备注">
                    <el-input v-model="form.data.content"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="createVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveCreate">确 定</el-button>
            </span>
        </el-dialog>

    </div>
</template>

<script>
export default {
    name: 'DatasourcesManage',
    data() {
        return {
            query: {
                select:'',
                key:'',
                pageIndex: 1,
                pageSize: 10,
            },
            tableData: [],
            editVisible: false,
            createVisible: false,
            pageTotal: 0,
            form: {
                data:{
                    id:'',
                    wgroup:'',
                    wserver:'',
                    type:'',
                    source:'',
                    putindb:'',
                    related:'',
                    target:'',
                    state:'',
                    content:'',
                    excepted:'',
                    finish: 'false',
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
                if(key.select=='type'){
                    key.key=(key.key=='文件')?'0':
                            (key.key=='目录')?'1':
                            (key.key=='数据库')?'2':key.key
                }
                if(key.select=='putindb'){
                    key.key=(key.key=='是')?'0':
                            (key.key=='否')?'1':key.key
                }
                if(key.select=='related'){
                    key.key=(key.key=='关系型')?'0':
                            (key.key=='非关系型')?'1':key.key
                }
                if(key.select=='pattern'){
                    key.key=(key.key=='只采集一次')?'0':
                            (key.key=='每天采集一次')?'1':key.key
                }
                if(key.select=='state'){
                    key.key=(key.key=='未采集')?'0':
                            (key.key=='持续采集中')?'1':
                            (key.key=='已完成')?'2':key.key
                }
                if(key.select=='excepted'){
                    key.key=(key.key=='正常')?'0':
                            (key.key=='异常')?'1':key.key
                } 
            } else {
                key.select=''
                key.key=''
            }
            var me = this
            this.$get(`/datasources?pageIndex=${key.pageIndex}&pageSize=${key.pageSize}&select=${key.select}&key=${key.key}`).then(res=>{
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
                this.$delete(`/datasources/${id}`).then(res=>{
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
            this.form.data.id = row.id
            this.form.data.wgroup = row.wgroup
            this.form.data.wserver = row.wserver
            this.form.data.type = row.type
            this.form.data.source = row.source
            this.form.data.putindb = row.putindb
            this.form.data.related = row.related
            this.form.data.target = row.target
            this.form.data.state = row.state
            this.form.data.content = row.content
            this.form.data.excepted = row.excepted
            this.form.data.finish = 'false'
            this.editVisible = true;
        },
        // 保存编辑
        saveEdit(id) {
            let key = {}
            key.content=this.form.data.content
            this.editVisible = false;
            if(this.form.data.finish){
                let me = this
                this.$post(`/frontend/dstate/${id}`).then(res=>{
                    if(res.data.error == 0){
                        me.$message.success('修改状态成功')
                        me.getData();
                    } else {
                        me.$message.error('修改状态失败，' + res.data.detail)
                        console.log(res.data.detail)
                        return
                    }
                }).catch(function(err){
                    console.log(err)
                })
            }

            let me = this
                this.$put(`/datasources/${id}`, key).then(res=>{
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
        //添加数据源
        handleCreate() {
            this.form.data.wgroup = ''
            this.form.data.wserver = ''
            this.form.data.type = ''
            this.form.data.source = ''
            this.form.data.putindb = ''
            this.form.data.related = ''
            this.form.data.pattern = ''
            this.form.data.target = ''
            this.form.data.content = ''
            this.createVisible = true;
        },
        saveCreate(){
            let key = {}
            if(this.form.data.wgroup&&this.form.data.wserver&&this.form.data.type
                &&this.form.data.source&&this.form.data.related){
                key.wgroup = this.form.data.wgroup
                key.wserver = this.form.data.wserver
                key.type = this.form.data.type
                key.source = this.form.data.source
                key.related = this.form.data.related

                key.content = this.form.data.content
            } else {
                this.$message.error('请完整填写信息')
                return
            }
            //不是数据库就需要验证其他数据存在
            if(this.form.data.type!="2"){
                if(this.form.data.putindb&&this.form.data.pattern&&this.form.data.target){
                    key.putindb = this.form.data.putindb
                    key.pattern = this.form.data.pattern
                    key.target = this.form.data.target
                } else {
                this.$message.error('请完整填写信息')
                return
                }
            }
            this.createVisible = false

            let me = this
            this.$post("/datasources", key).then(res=>{
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
