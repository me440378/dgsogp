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
                                <el-radio label="MySQL" value='0'></el-radio>
                                <el-radio label="MongoDB" value='1'></el-radio>
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
                    <el-col :span="4">
                        <el-form-item label="启用用户名与密码">
                            <el-switch v-model="form.usenp"></el-switch>
                        </el-form-item>
                    </el-col>
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
                    <el-col :span="4">
                        <el-form-item>
                            <el-button type="primary" @click="onSubmit">连接数据库</el-button>
                        </el-form-item>
                    </el-col>
                </el-row>
                
<!--                 <el-form-item label="文本框">
                    <el-input type="textarea" rows="5" v-model="form.desc"></el-input>
                </el-form-item> -->
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
                form: {
                    wserver: '',
                    wport:'',
                    type: '',
                    name:'',
                    usenp: true,
                    username:'',
                    password:'',
                },
                cmd:{
                    content:'',
                },
            }
        },
        methods: {
            onEditorChange({ editor, html, text }) {
                this.content = html;
            },
            onSubmit() {
                let key = {}
                if(this.form.wserver&&this.form.wport&&this.form.type
                    &&this.form.name) {
                    key.wserver = this.form.wserver
                    key.wport = this.form.wport
                    key.type = this.form.type
                    key.name = this.form.name
                } else {
                    this.$message.error('请完整填写信息')
                    return
                }
                if(this.form.usenp){
                    if (this.form.username&&this.form.password) {
                        key.username = this.form.username
                        key.password = this.form.password
                    } else {
                        this.$message.error('请完整填写信息')
                        return  
                    }
                }
                console.log(key)
            }
        }
    }
</script>
<style>
.dbicmd > textarea{
    font-size: 18px;
    color: #AAAAAA;
    background-color: #080808;
}
</style>