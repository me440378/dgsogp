<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-locationfill"></i> Hadoop源管理
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="handle-box">
                <el-input v-model="query.name" placeholder="" class="handle-input mr10"></el-input>
                <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
            </div>
            <el-table
                :data="tableData"
                border
                class="table"
                ref="multipleTable"
                header-cell-class-name="table-header"
                @selection-change="handleSelectionChange"
            >
                <el-table-column prop="id" label="ID" width="55" align="center"></el-table-column>
                <el-table-column prop="source" label="HDFS路径"></el-table-column>
                <el-table-column prop="datasource_id" label="数据源ID"></el-table-column>
                <el-table-column prop="state" label="处理状态">
                    <template slot-scope="scope">
                        {{
                            scope.row.state == '0' ? "未标记" :
                            scope.row.state == '1' ? "持续标记中" :
                            scope.row.state == '2' ? "已完成" : ""
                        }}
                    </template>
                </el-table-column>
                <el-table-column prop="excepted" label="异常状态">
                    <template slot-scope="scope">
                        {{
                            scope.row.excepted == '0' ? "正常" :
                            scope.row.excepted == '1' ? "异常" : ""
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
import { fetchData } from '../../api/index';
export default {
    name: 'HadoopsourcesManage',
    data() {
        return {
            query: {
                name: '',
                nickname: '',
                pageIndex: 1,
                pageSize: 10
            },
            tableData: [
                {
                    "id": 1,
                    "source": "/dev/hadoop-server-test/iris.data",
                    "state": 2,
                    "datasource_id": 1
                },
                {
                    "id": 2,
                    "source": "/ops/hadoop-server-test/python",
                    "state": 2,
                    "datasource_id": 2
                },
                {
                    "id": 3,
                    "source": "/test/hadoop-server-test/mongo/iris.data",
                    "state": 2,
                    "datasource_id": 3
                }
            ],
            delList: [],
            editVisible: false,
            passwordVisible: false,
            forcepasswordVisible: false,
            pageTotal: 4,
            form: {},
            idx: -1,
            id: -1
        };
    },
    created() {
        // this.getData();
    },
    methods: {
        // 获取 easy-mock 的模拟数据
        // getData() {
        //     fetchData(this.query).then(res => {
        //         console.log(res);
        //         this.tableData = res.list;
        //         this.pageTotal = res.pageTotal || 50;
        //     });
        // },
        // 触发搜索按钮
        handleSearch() {
            this.$set(this.query, 'pageIndex', 1);
            this.getData();
        },
        // 删除操作
        handleDelete(index, row) {
            // 二次确认删除
            this.$confirm('确定要删除吗？', '提示', {
                type: 'warning'
            })
                .then(() => {
                    this.$message.success('删除成功');
                    this.tableData.splice(index, 1);
                })
                .catch(() => {});
        },
        // 编辑操作
        handleEdit(index, row) {
            this.idx = index;
            this.form = row;
            this.editVisible = true;
        },
        // 保存编辑
        saveEdit() {
            this.editVisible = false;
            this.$message.success(`修改 ${this.form.name} 信息成功`);
            this.$set(this.tableData, this.idx, this.form);
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
