<template>
    <div class="">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-copy"></i>通知管理</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-button type="primary" @click="handleCreate">添加通知</el-button>
            <el-tabs v-model="message">
                <el-tab-pane :label="`未读信息(${unread.length})`" name="first">
                    <el-table :data="unread" :show-header="false" style="width: 100%">
                        <el-table-column>
                            <template slot-scope="scope">
                                <span class="message-name">{{scope.row.name}}</span>
                            </template>
                        </el-table-column>
                        <el-table-column prop="created_at" width="180"></el-table-column>
                        <el-table-column width="240">
                            <template slot-scope="scope">
                                <el-button size="small" type="primary" @click="handleContent(scope.row)">详细内容</el-button>
                                <el-button size="small" @click="handleRead(scope.$index, scope.row)">标为已读</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                    <!-- <div class="handle-row">
                        <el-button type="primary">全部标为已读</el-button>
                    </div> -->
                </el-tab-pane>
                <el-tab-pane :label="`已读信息(${read.length})`" name="second">
                    <template v-if="message === 'second'">
                        <el-table :data="read" :show-header="false" style="width: 100%">
                            <el-table-column>
                                <template slot-scope="scope">
                                    <span class="message-name">{{scope.row.name}}</span>
                                </template>
                            </el-table-column>
                            <el-table-column prop="created_at" width="150"></el-table-column>
                            <el-table-column width="120">
                                <template slot-scope="scope">
                                    <el-button type="danger" @click="handleDel(scope.$index, scope.row)">删除</el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                    <!--     <div class="handle-row">
                            <el-button type="danger">删除全部</el-button>
                        </div> -->
                    </template>
                </el-tab-pane>
                <el-tab-pane :label="`回收站(${recycle.length})`" name="third">
                    <template v-if="message === 'third'">
                        <el-table :data="recycle" :show-header="false" style="width: 100%">
                            <el-table-column>
                                <template slot-scope="scope">
                                    <span class="message-name">{{scope.row.name}}</span>
                                </template>
                            </el-table-column>
                            <el-table-column prop="created_at" width="150"></el-table-column>
                            <el-table-column width="120">
                                <template slot-scope="scope">
                                    <el-button @click="handleRestore(scope.$index, scope.row)">还原</el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                      <!--   <div class="handle-row">
                            <el-button type="danger">清空回收站</el-button>
                        </div> -->
                    </template>
                </el-tab-pane>
            </el-tabs>
        </div>

        <!-- 添加弹出框 -->
        <el-dialog title="添加通知" :visible.sync="createVisible" width="40%">
            <el-form ref="form" :model="form.data" label-width="100px">
                <el-form-item label="通知标题">
                    <el-input v-model="form.data.name"></el-input>
                </el-form-item>
                <el-form-item label="通知内容">
                    <el-input type=textarea rows="6" v-model="form.data.content"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="createVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveCreate">确 定</el-button>
            </span>
        </el-dialog>

        <el-dialog title="通知内容" :visible.sync="contentVisible" width="40%">
            <el-form ref="form" :model="form.data" label-width="100px">
                <el-form-item label="通知标题">
                    <span>{{form.data.name}}</span>
                </el-form-item>
                <el-form-item label="通知内容">
                    <span>{{form.data.content}}</span>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button type="primary" @click="contentVisible = false">关 闭</el-button>
            </span>
        </el-dialog>

    </div>
</template>

<script>
    export default {
        name: 'MessagesManage',
        data() {
            return {
                message: 'first',
                showHeader: false,
                unread: [{
                    id:1,
                    created_at: '2018-04-19 20:00:00',
                    name: 'Hadoop服务器集群的监控功能还无法使用，前端页面显示只是示例',
                    content: 'Hadoop服务器集群的监控功能还无法使用，前端页面显示只是示例'
                },{
                    id:2,
                    created_at: '2018-04-19 21:00:00',
                    name: '上次登录时间和上次登录地点记录功能无法使用，前端页面显示只是示例',
                    content: '上次登录时间和上次登录地点记录功能无法使用，前端页面显示只是示例'
                }],
                read: [],
                recycle: [{
                    id:3,
                    created_at: '2018-04-19 20:00:00',
                    name: '今天要修复100个bug',
                    content: '上次登录时间和上次登录地点记录功能无法使用，前端页面显示只是示例'
                }],
                createVisible: false,
                contentVisible: false,
                form: {
                    data:{
                        name:'',
                        content:'',
                    },
                },
            }
        },
        mounted() {
            this.getData();
        },
        methods: {
            getData() {
                let select = 'status'
                var me = this

                this.$get(`/messages?pageIndex=1&pageSize=1000&select=status&key=0`).then(res=>{
                    me.unread = res.data.data
                }).catch(function(err){
                    console.log(err)
                })
                this.$get(`/messages?pageIndex=1&pageSize=1000&select=status&key=1`).then(res=>{
                    me.read = res.data.data
                }).catch(function(err){
                    console.log(err)
                })
                this.$get(`/messages?pageIndex=1&pageSize=1000&select=status&key=2`).then(res=>{
                    me.recycle = res.data.data
                }).catch(function(err){
                    console.log(err)
                })
            },
            handleRead(index, row) {
                let id = row.id
                let me = this
                this.$put(`/messages/${id}`, {"status":1}).then(res=>{
                    if(res.data.error == 0){
                        me.getData();
                        me.$message.success('操作成功')
                    } else {
                        me.$message.error('操作失败，' + res.data.detail)
                        console.log(res.data.detail)
                        return
                    }
                }).catch(function(err){
                    console.log(err)
                })

                const item = this.unread.splice(index, 1);
                console.log(item);
                this.read = item.concat(this.read);
            },
            handleDel(index, row) {
                let id = row.id
                let me = this
                this.$put(`/messages/${id}`, {"status":2}).then(res=>{
                    if(res.data.error == 0){
                        me.getData();
                        me.$message.success('操作成功')
                    } else {
                        me.$message.error('操作失败，' + res.data.detail)
                        console.log(res.data.detail)
                        return
                    }
                }).catch(function(err){
                    console.log(err)
                })

                const item = this.read.splice(index, 1);
                this.recycle = item.concat(this.recycle);
            },
            handleRestore(index, row) {
                let id = row.id
                let me = this
                this.$put(`/messages/${id}`, {"status":1}).then(res=>{
                    if(res.data.error == 0){
                        me.getData();
                        me.$message.success('操作成功')
                    } else {
                        me.$message.error('操作失败，' + res.data.detail)
                        console.log(res.data.detail)
                        return
                    }
                }).catch(function(err){
                    console.log(err)
                })

                const item = this.recycle.splice(index, 1);
                this.read = item.concat(this.read);
            },
            handleContent(row){
                this.form.data.name = row.name
                this.form.data.content = row.content
                this.contentVisible = true;
            },
            handleCreate(){
                this.form.data.name = ''
                this.form.data.content = ''
                this.createVisible = true;
            },
            saveCreate(){
                let key = {}
                if(this.form.data.name&&this.form.data.content){
                    key.name = this.form.data.name
                    key.content = this.form.data.content
                } else {
                    this.$message.error('请完整填写信息')
                    return
                }

                this.createVisible = false

                let me = this
                this.$post("/messages", key).then(res=>{
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
        },
        computed: {
            unreadNum(){
                return this.unread.length;
            }
        }
    }

</script>

<style>
.message-name{
    cursor: pointer;
}
.handle-row{
    margin-top: 30px;
}
</style>

