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
            <el-row class="handle-box">
                <el-col :span="8">
                    <el-input v-model="query.key" placeholder="" class="input-with-select">
                        <el-select v-model="query.select" slot="prepend" placeholder="请选择" style="width: 130px;">
                            <el-option label="ID" value="id"></el-option>
                            <el-option label="数据库类型" value="type"></el-option>
                            <el-option label="表名/集合名" value="name"></el-option>
                            <el-option label="元数据ID" value="metadata_id"></el-option>
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
                <el-table-column prop="name" label="表名/集合名"></el-table-column>
                <el-table-column prop="metadata_id" label="元数据ID"></el-table-column>
                <el-table-column label="数据接口http地址(GET方法)">
                    <template slot-scope="scope">
                        {{dataInterfacesBaseUrl}}/{{scope.row.id}}
                    </template>
                </el-table-column>
                <el-table-column label="操作">
                    <template slot-scope="scope">
                            <el-button
                                type="text"
                                icon="el-icon-link"
                                @click="handleOpen(scope.row)"
                            >预览</el-button>
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
                select:'',
                key: '',
                pageIndex: 1,
                pageSize: 10,
            },
            tableData: [],
            dataInterfacesBaseUrl:'',
            pageTotal: 0,
        };
    },
    mounted() {
        this.getData();
        this.dataInterfacesBaseUrl = this.DataInterfacesBaseUrl
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
            this.$get(`/datainterfaces?pageIndex=${key.pageIndex}&pageSize=${key.pageSize}&select=${key.select}&key=${key.key}`).then(res=>{
                me.tableData = res.data.data
                me.pageTotal = res.data.total
            }).catch(function(err){
                console.log(err)
            })
        },
        handleOpen(row) {
            let id = row.id
            let url = this.dataInterfacesBaseUrl+'/'+id
            window.open(url)
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
    },
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