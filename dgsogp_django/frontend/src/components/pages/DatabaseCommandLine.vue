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
                            <el-input v-model="form.wserver" spellcheck="false"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="1">
                        &nbsp;
                    </el-col>
                    <el-col :span="10">
                        <el-form-item label="工作端口">
                            <el-input type="number" v-model="form.wport" spellcheck="false"></el-input>
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
                            <el-input v-model="form.name" spellcheck="false"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="6">
                        <el-form-item label="用户名">
                            <el-input v-model="form.username" spellcheck="false"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="6">
                        <el-form-item label="密码">
                            <el-input type="password" v-model="form.password" spellcheck="false"></el-input>
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
            <el-input class="dbicmd" id="dbitextarea" type="textarea" rows="20" v-model="cmd.content" spellcheck="false" :readonly="true"></el-input>
            <el-input class="dbicmd" rows="1" v-model="cmd.line" spellcheck="false" @keyup.enter.native="onSend" ref="dbiinput"><template slot="prepend">></template></el-input>
        </div>

        <!-- 编辑弹出框 -->
        <el-dialog title="请使用adminMongo" :visible.sync="mongoVisible" width="45%">
            <el-form ref="form" :model="form.data" label-width="168px">
                <el-form-item label="adminMongo链接">
                    <el-row>
                        <el-col :span="20">
                            <span>{{form.data.adminMongoUrl}}</span>
                        </el-col>
                        <el-col :span="4">
                            <el-button type="primary" @click="handleOpen">打开</el-button>
                        </el-col>
                    </el-row>
                </el-form-item>
                <el-form-item label="MongoDB标准链接URI">
                    <el-row>
                        <el-col :span="20">
                            <span>{{form.data.mongodbUrl}}</span>
                        </el-col>
                        <el-col :span="4">
                            <el-button type="primary" v-clipboard:copy="form.data.mongodbUrl" v-clipboard:success="onCopySuccess" v-clipboard:error="onCopyError">复制</el-button>
                        </el-col>
                    </el-row>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="mongoVisible = false">关 闭</el-button>
            </span>
        </el-dialog>

    </div>
</template>

<script>
    export default {
        name: 'editor',
        data: function(){
            return {
                websock: null,
                form: {
                    wserver: 'hadoop-server-test',
                    wport:'27017',
                    type: '1',
                    name:'xxx_db',
                    username:'root',
                    password:'123456',
                    data:{
                        adminMongoUrl:'',
                        mongodbUrl:'',
                    },
                },
                cmd:{
                    content:'',
                    histoty:'',
                    line:'',
                },
                mongoVisible: false,
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
                if(key.type=='0'){
                    // MySQL
                    // console.log(key)
                    this.initWebSocket(key)
                    // 聚焦到输入行
                    this.$nextTick(()=>{
                        this.$refs.dbiinput.focus()
                    })
                } else {
                    //MongoDB
                    this.form.data.adminMongoUrl=this.adminMongoUrl
                    this.form.data.mongodbUrl='mongodb://'+key.username+':'+key.password+'@'+key.wserver+':'+key.wport+'/'+key.name
                    //Connection string: mongodb://<user>:<password>@<host>:<port>/<db>
                    this.mongoVisible=true
                }
                
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
                //连接成功
                this.websock.onopen = function(event){
                    me.websock.send(JSON.stringify(key))
                }
                //连接错误
                this.websock.onerror = function(event){
                    console.log("WebSocket连接发生错误")
                    if(me.websock!=null){
                        me.websock.close()
                    }
                }
                //接收信息
                this.websock.onmessage = function(event){
                    if(event.data=="bye"){
                        me.websock.close()
                    }
                    me.cmd.content+=event.data
                    me.textareaScroll()
                }
                //连接关闭
                this.websock.onclose = function(event){
                    console.log("WebSocket连接已关闭")
                    me.websock=null
                    me.cmd.content+="\n数据库连接已关闭\n"
                    me.textareaScroll()
                }
            },
            onSend(){
                if(this.websock==null){
                    this.cmd.content+="还未连接到数据库\n"
                    this.textareaScroll()
                    return
                }
                let key = this.cmd.line
                this.websock.send(key)
                this.cmd.line=''
                this.cmd.content+=key+'\n'
                this.textareaScroll()
            },
            textareaScroll(){
                var textarea = document.getElementById('dbitextarea');
                textarea.scrollTop = textarea.scrollHeight;
            },
            handleOpen() {
                let url = this.form.data.adminMongoUrl
                window.open(url)
            },
            onCopySuccess(event) {
                this.$message.success('复制成功')
            },
            onCopyError(event) {
                this.$message.error('复制失败')
                console.log(event)
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
.dbicmd > input{
    font-size: 18px;
    color: #AAAAAA;
    background-color: #080808;
}
.dbicmd > div{
    font-size: 18px;
    color: #AAAAAA;
    background-color: #080808;
}
</style>