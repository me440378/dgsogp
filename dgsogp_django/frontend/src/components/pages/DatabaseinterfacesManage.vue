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
            <div class="handle-box">
                <el-input v-model="query.key" placeholder="" class="handle-input mr10"></el-input>
                <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
            </div>
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
                key: '',
                pageIndex: 1,
                pageSize: 10
            },
            tableData: [
                {
                    "id": 1,
                    "type": 0,
                    "wserver": "hadoop-server-test",
                    "wport": "3306",
                    "name": "xxx_db",
                    "datasource_id": 3
                },
            ],
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
            var me = this
            this.$get("/databaseinterfaces").then(res=>{
                me.tableData = res.data
            }).catch(function(err){
                console.log(err)
            })
        },
        // 触发搜索按钮
        handleSearch() {
            this.getData();
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