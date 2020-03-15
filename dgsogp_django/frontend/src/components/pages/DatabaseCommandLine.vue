<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-shopfill"></i> 数据库接口命令行
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-form ref="form" :model="form" label-width="150px">
                <el-row>
                    <el-col :span="10">
                        <el-form-item label="工作服务器">
                            <el-input v-model="form.wserver"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="1">
                        &nbsp;
                    </el-col>
                    <el-col :span="10">
                        <el-form-item label="工作端口">
                            <el-input v-model="form.wport"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="10">
                        <el-form-item label="数据库类型">
                            <el-radio-group v-model="form.type">
                                <el-radio label="0">MySQL</el-radio>
                                <el-radio label="1">MongoDB</el-radio>
                            </el-radio-group>
                        </el-form-item>
                    </el-col>
                    <el-col :span="1">
                        &nbsp;
                    </el-col>
                    <el-col :span="10">
                        <el-form-item label="数据库名/集合名">
                            <el-input v-model="form.name"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="6">
                        <el-form-item label="用户名">
                            <el-input v-model="form.username"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="6">
                        <el-form-item label="密码">
                            <el-input v-model="form.password"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="2">
                        <el-form-item>
                            <el-button type="primary" @click="onStart">连接数据库</el-button>
                        </el-form-item>
                    </el-col>
                    <el-col :span="2">
                        <el-form-item>
                            <el-button type="danger" @click="onFinish">关闭连接</el-button>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
            <el-input class="dbicmd" type="textarea" rows="20" v-model="cmd.content" spellcheck="false"></el-input>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'editor',
        data: function(){
            return {
                websock: null,
                timeout: 28*1000, //30s 一次心跳
                timeoutObj: null, //心跳倒计时
                form: {
                    wserver: '',
                    wport:'',
                    type: '',
                    name:'',
                    username:'',
                    password:'',
                },
                cmd:{
                    content:'',
                },
            }
        },
        methods: {
            onStart() {
                let key = {}
                if(this.form.wserver&&this.form.wport&&this.form.type
                    &&this.form.name) {
                    key.wserver = this.form.wserver
                    key.wport = this.form.wport
                    key.type = this.form.type
                    key.name = this.form.name
                } else {
                    this.$message.error('请完整填写必要信息')
                    return
                }
                if (this.form.username&&this.form.password) {
                    key.username = this.form.username
                    key.password = this.form.password
                } else {
                    this.$message.error('请完整填写用户名与密码')
                    return  
                }
                console.log(key)
                this.initWebSocket(key)
            },
            onFinish() {
                if(this.websock!=null){
                    this.websock.close()
                }
                this.websock=null
            },
            initWebSocket(key){
                this.websock = new WebSocket("ws://localhost:8000/api/1.0/databaseinterfaces/dbcli")

                let me = this
                // //连接成功
                // this.websock.onopen = this.websocketonopen(key);
                this.websock.onopen = function(event){
                    me.websock.send(JSON.stringify(key))
                }
                // this.websock.on('open',function(event){
                //     this.websock.send(key)
                // });
                //连接错误
                this.websock.onerror = function(event){
                    console.log("WebSocket连接发生错误")
                    console.log(e)
                }
                //接收信息
                this.websock.onmessage = function(event){
                    console.log(event.data)
                }
                //连接关闭
                this.websock.onclose = this.websocketclose;
            },
        },
        destroyed(){
            if(this.websock!=null){
                    this.websock.close()
                }
            this.websock=null
        },
    }
</script>
<style>
.dbicmd > textarea{
    font-size: 18px;
    color: #AAAAAA;
    background-color: #080808;
}
</style>