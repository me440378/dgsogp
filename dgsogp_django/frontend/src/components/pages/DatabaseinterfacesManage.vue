<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-shopfill"></i> 数据库接口管理
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-row class="handle-box">
                <el-col :span="8">
                    <el-input v-model="query.key" placeholder="" class="input-with-select">
                        <el-select v-model="query.select" slot="prepend" placeholder="请选择" style="width: 130px;">
                            <el-option label="ID" value="id"></el-option>
                            <el-option label="数据库类型" value="type"></el-option>
                            <el-option label="工作服务器" value="wserver"></el-option>
                            <el-option label="工作端口" value="wport"></el-option>
                            <el-option label="数据库名" value="name"></el-option>
                            <el-option label="数据源ID" value="datasource_id"></el-option>
                        </el-select>
                        <el-button type="primary" icon="el-icon-search" @click="handleSearch" slot="append">搜索</el-button>
                    </el-input>
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
                <el-table-column prop="type" label="数据库类型">
                    <template slot-scope="scope">
                        {{
                            scope.row.type == '0' ? "mysql" :
                            scope.row.type == '1' ? "mongodb" :
                            scope.row.type == '2' ? "redis" : ""
                        }}
                    </template>
                </el-table-column>
                <el-table-column prop="wserver" label="工作服务器"></el-table-column>
                <el-table-column prop="wport" label="工作端口"></el-table-column>
                <el-table-column prop="name" label="数据库名"></el-table-column>
                <el-table-column prop="datasource_id" label="数据源ID"></el-table-column>
                <el-table-column label="操作" width="180" align="center">
                    <template slot-scope="scope">
                        <el-button
                            type="primary"
                            icon="el-icon-edit"
                            @click="handleJump(scope.row)"
                        >进行操作</el-button>
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
    </div>
</template>

<script>
export default {
    name: 'DatabaseinterfacesManage',
    data() {
        return {
            query: {
                select: '',
                key: '',
                pageIndex: 1,
                pageSize: 10
            },
            tableData: [],
            pageTotal: 10,
            idx: -1,
            id: -1
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
                    key.key=(key.key=='mysql')?'0':
                            (key.key=='mongodb')?'1':
                            (key.key=='redis')?'2':key.key
                }
            } else {
                key.select=''
                key.key=''
            }
            var me = this
            this.$get(`/databaseinterfaces?pageIndex=${key.pageIndex}&pageSize=${key.pageSize}&select=${key.select}&key=${key.key}`).then(res=>{
                me.tableData = res.data.data
                me.pageTotal = res.data.total
            }).catch(function(err){
                console.log(err)
            })
        },
        // 触发搜索按钮
        handleSearch() {
            this.getData()
        },
        // 分页导航
        handlePageChange(val) {
            this.$set(this.query, 'pageIndex', val);
            this.getData();
        },
        handleJump(row) {
            let key = {}
            key.type = row.type
            key.wserver = row.wserver
            key.wport = row.wport
            key.name = row.name
            this.$router.push({
               path:"/databasecommandline",
               query:key,
            });
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