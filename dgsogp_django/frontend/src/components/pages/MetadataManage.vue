<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-tag"></i> 元数据管理
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-row class="handle-box">
                <el-col :span="8">
                    <el-input v-model="query.key" placeholder="" class="input-with-select">
                        <el-select v-model="query.select" slot="prepend" placeholder="请选择" style="width: 130px;">
                          <el-option label="ID" value="id"></el-option>
                          <el-option label="HDFS文件路径" value="source"></el-option>
                          <el-option label="数据量" value="amount"></el-option>
                          <el-option label="数据特征数" value="feature"></el-option>
                          <el-option label="文件检验和" value="hashsum"></el-option>
                          <el-option label="文件格式" value="format"></el-option>
                          <el-option label="Hadoop源ID" value="hadoopsource_id"></el-option>
                          <el-option label="入库状态" value="state"></el-option>
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
                <el-table-column prop="source" label="HDFS文件路径"></el-table-column>
                <el-table-column prop="amount" label="数据量"></el-table-column>
                <el-table-column prop="feature" label="数据特征数"></el-table-column>
                <el-table-column prop="hashsum" label="文件校验和"></el-table-column>
                <el-table-column prop="format" label="文件格式"></el-table-column>
                <el-table-column prop="hadoopsource_id" label="Hadoop源ID"></el-table-column>
                <el-table-column prop="state" label="入库状态">
                    <template slot-scope="scope">
                        {{
                            scope.row.state == '0' ? "未入库" :
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
    name: 'HadoopsourcesManage',
    data() {
        return {
            query: {
                select:'',
                key: '',
                pageIndex: 1,
                pageSize: 10,
            },
            tableData: [],
            pageTotal: 0,
        };
    },
    mounted() {
        this.getData();
    },
    methods: {
        getData() {
            let key = this.query
            if (key.select&&key.key) {
                if(key.select=='state'){
                    key.key=(key.key=='未入库')?'0':
                            (key.key=='持续标记中')?'1':
                            (key.key=='已完成或无需入库')?'2':key.key
                }
            } else {
                key.select=''
                key.key=''
            }
            var me = this
            this.$get(`/metadata?pageIndex=${key.pageIndex}&pageSize=${key.pageSize}&select=${key.select}&key=${key.key}`).then(res=>{
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