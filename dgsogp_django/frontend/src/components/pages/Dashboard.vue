<template>
    <div>
        <el-row :gutter="10">
            <el-col :span="8">
                <el-card shadow="hover" class="mgtb5" style="height:236px;">
                    <div class="user-info">
                        <!-- <img src="../../assets/img/img.jpg" class="user-avator" alt /> -->
                        <div class="grid-content">
                            <i class="el-icon-lx-people grid-con-icon" style="color:#606266"></i>
                        </div>
                        <div class="user-info-cont">
                            <div class="user-info-name">{{user.nickname}}</div>
                            <div>{{role}}</div>
                        </div>
                    </div>
                    <div class="user-info-list">
                        上次登录时间：
                        <span>2020-01-01</span>
                    </div>
                    <div class="user-info-list">
                        上次登录地点：
                        <span>广州</span>
                    </div>
                </el-card>
            </el-col>
            <el-col :span="16">
                <el-row :gutter="20" class="mgtb5" style="height:120px;">
                    <el-col :span="8">
                        <el-card shadow="hover" :body-style="{padding: '0px'}">
                            <div class="grid-content grid-con-1">
                                <i class="el-icon-lx-location grid-con-icon"></i>
                                <div class="grid-cont-right">
                                    <div class="grid-num">{{datasourcesCount}}</div>
                                    <div>数据源</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="8">
                        <el-card shadow="hover" :body-style="{padding: '0px'}">
                            <div class="grid-content grid-con-2">
                                <i class="el-icon-lx-locationfill grid-con-icon"></i>
                                <div class="grid-cont-right">
                                    <div class="grid-num">{{hadoopsourcesCount}}</div>
                                    <div>Hadoop源</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="8">
                        <el-card shadow="hover" :body-style="{padding: '0px'}">
                            <div class="grid-content grid-con-3">
                                <i class="el-icon-lx-tag grid-con-icon"></i>
                                <div class="grid-cont-right">
                                    <div class="grid-num">{{metadataCount}}</div>
                                    <div>元数据</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                </el-row>
                <el-row :gutter="20" class="mgtb5" style="height:120px;">
                    <el-col :span="8">
                        <el-card shadow="hover" :body-style="{padding: '0px'}">
                            <div class="grid-content grid-con-5">
                                <i class="el-icon-lx-shop grid-con-icon"></i>
                                <div class="grid-cont-right">
                                    <div class="grid-num">{{datainterfacesCount}}</div>
                                    <div>数据接口</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="8">
                        <el-card shadow="hover" :body-style="{padding: '0px'}">
                            <div class="grid-content grid-con-6">
                                <i class="el-icon-lx-shopfill grid-con-icon"></i>
                                <div class="grid-cont-right">
                                    <div class="grid-num">{{databaseinterfacesCount}}</div>
                                    <div>数据库接口</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="8">
                        <el-card shadow="hover" :body-style="{padding: '0px'}">
                            <div class="grid-content grid-con-5">
                                <i class="el-icon-lx-peoplefill grid-con-icon"></i>
                                <div class="grid-cont-right">
                                    <div class="grid-num">{{usersCount}}</div>
                                    <div>用户</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                </el-row>
            </el-col>
        </el-row>
        <el-row :gutter="10">
            <el-col :span="24">
                <el-card shadow="hover" style="height:280px;">
                    <div slot="header" class="clearfix">
                        <span>系统通知</span>
                        <!-- <el-button style="float: right; padding: 3px 0" type="text">添加</el-button> -->
                    </div>
                    <el-table :show-header="false" :data="NoticeList" style="width:100%;">
                        <!-- <el-table-column width="40">
                            <template slot-scope="scope">
                                <el-checkbox v-model="scope.row.status"></el-checkbox>
                            </template>
                        </el-table-column> -->
                        <el-table-column>
                            <template slot-scope="scope">
                                <div
                                    class="todo-item"
                                    :class="{'todo-item-del': scope.row.status}"
                                >{{scope.row.title}}</div>
                            </template>
                        </el-table-column>
                        <!-- <el-table-column width="60">
                            <template>
                                <i class="el-icon-edit"></i>
                                <i class="el-icon-delete"></i>
                            </template>
                        </el-table-column> -->
                    </el-table>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
export default {
    name: 'dashboard',
    data() {
        return {
            userid: localStorage.getItem('userid'),
            user:{},
            datasourcesCount:0,
            hadoopsourcesCount:0,
            metadataCount:0,
            datainterfacesCount:0,
            databaseinterfacesCount:0,
            usersCount:0,
            NoticeList: [
                {
                    title: '上次登录时间和上次登录地点记录功能无法使用，前端页面显示只是示例',
                    status: false
                },
                {
                    title: '今天要修复100个bug',
                    status: false
                },
            ],
        };
    },
    computed: {
        role() {
            return this.userid === '1' ? '超级管理员' : '普通用户';
        }
    },
    mounted(){
        this.getData()
    },
    created() {
    },
    methods: {
        getData(){
            let userid = localStorage.getItem('userid');
            let me = this;
            this.$post("/frontend/dashboard",{
                "userid": userid,
            }).then(res=>{
                me.user = res.data.user
                me.datasourcesCount = res.data.datasourcesCount
                me.hadoopsourcesCount = res.data.hadoopsourcesCount
                me.metadataCount = res.data.metadataCount
                me.datainterfacesCount = res.data.datainterfacesCount
                me.databaseinterfacesCount = res.data.databaseinterfacesCount
                me.usersCount = res.data.usersCount
            }).catch(function(err){
                console.log(err)
            })
        }
    }
};
</script>


<style scoped>
.el-row {
    margin-bottom: 20px;
}

.grid-content {
    display: flex;
    align-items: center;
    height: 100px;
}

.grid-cont-right {
    flex: 1;
    text-align: center;
    font-size: 14px;
    color: #999;
}

.grid-num {
    font-size: 30px;
    font-weight: bold;
}

.grid-con-icon {
    font-size: 50px;
    width: 100px;
    height: 100px;
    text-align: center;
    line-height: 100px;
    color: #fff;
}

.grid-con-1 .grid-con-icon {
    background: rgb(45, 140, 240);
}

.grid-con-1 .grid-num {
    color: rgb(45, 140, 240);
}

.grid-con-2 .grid-con-icon {
    background: rgb(100, 213, 114);
}

.grid-con-2 .grid-num {
    color: rgb(100, 213, 114);
}

.grid-con-3 .grid-con-icon {
    background: rgb(242, 94, 67);
}

.grid-con-3 .grid-num {
    color: rgb(242, 94, 67);
}

.grid-con-4 .grid-con-icon {
    background: rgb(153, 204, 51);
}

.grid-con-4 .grid-num {
    color: rgb(153, 204, 51);
}

.grid-con-5 .grid-con-icon {
    background: rgb(255, 153, 0);
}

.grid-con-5 .grid-num {
    color: rgb(255, 153, 0);
}

.grid-con-6 .grid-con-icon {
    background: rgb(255, 204, 0);
}

.grid-con-6 .grid-num {
    color: rgb(255, 204, 0);
}

.user-info {
    display: flex;
    align-items: center;
    padding-bottom: 20px;
    border-bottom: 2px solid #ccc;
    margin-bottom: 20px;
}

.user-avator {
    width: 120px;
    height: 120px;
    border-radius: 50%;
}

.user-info-cont {
    padding-left: 50px;
    flex: 1;
    font-size: 14px;
    color: #999;
}

.user-info-cont div:first-child {
    font-size: 30px;
    color: #222;
}

.user-info-list {
    font-size: 14px;
    color: #999;
    line-height: 25px;
}

.user-info-list span {
    margin-left: 70px;
}

.mgtb5 {
    margin-top: 5px;
    margin-bottom: 5px;
}

.todo-item {
    font-size: 14px;
}

.todo-item-del {
    text-decoration: line-through;
    color: #999;
}

.schart {
    width: 100%;
    height: 300px;
}
</style>
