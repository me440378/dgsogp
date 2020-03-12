<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-shop"></i> 数据接口管理
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
                <el-table-column prop="source" label="HDFS文件路径"></el-table-column>
                <el-table-column prop="amount" label="数据量"></el-table-column>
                <el-table-column prop="feature" label="数据特征数"></el-table-column>
                <el-table-column prop="hashsum" label="文件校验和"></el-table-column>
                <el-table-column prop="format" label="文件格式"></el-table-column>
                <el-table-column prop="hadoopsource_id" label="Hadoop源ID"></el-table-column>
                <el-table-column prop="state" label="入库状态">
                    <template slot-scope="scope">
                        {{
                            scope.row.state == '0' ? "未标记" :
                            scope.row.state == '1' ? "持续标记中" :
                            scope.row.state == '2' ? "已完成或无需入库" : ""
                        }}
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
    name: 'DatainterfacesManage',
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
                    "source": "/dev/hadoop-server-test/iris.data",
                    "amount": 150,
                    "feature": 5,
                    "hashsum": "7a1c6dc40b600415d7113cf9e0b1aab5",
                    "hadoopsource_id": 1,
                    "format": "data",
                    "state": 2
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
            this.$get("/metadata").then(res=>{
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