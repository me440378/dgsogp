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
                    "amount": 150,
                    "feature": 5,
                    "hashsum": "7a1c6dc40b600415d7113cf9e0b1aab5",
                    "hadoopsource_id": 1,
                    "format": "data",
                    "state": 2
                },
                {
                    "id": 2,
                    "source": "/ops/hadoop-server-test/python/123456",
                    "amount": null,
                    "feature": null,
                    "hashsum": "f447b20a7fcbf53a5d5be013ea0b15af",
                    "hadoopsource_id": 2,
                    "format": "unknown",
                    "state": 2
                },
                {
                    "id": 3,
                    "source": "/ops/hadoop-server-test/python/hdfstest.py",
                    "amount": null,
                    "feature": null,
                    "hashsum": "c0d0e3c997878eb198dc836493bb0f07",
                    "hadoopsource_id": 2,
                    "format": "py",
                    "state": 2
                },
                {
                    "id": 4,
                    "source": "/ops/hadoop-server-test/python/httprequest.py",
                    "amount": null,
                    "feature": null,
                    "hashsum": "95f6330c759792b2d485b8116c81f056",
                    "hadoopsource_id": 2,
                    "format": "py",
                    "state": 2
                },
                {
                    "id": 5,
                    "source": "/ops/hadoop-server-test/python/iris.data",
                    "amount": null,
                    "feature": null,
                    "hashsum": "7a1c6dc40b600415d7113cf9e0b1aab5",
                    "hadoopsource_id": 2,
                    "format": "data",
                    "state": 2
                },
                {
                    "id": 6,
                    "source": "/ops/hadoop-server-test/python/paramikotest.py",
                    "amount": null,
                    "feature": null,
                    "hashsum": "54a4995fcdea5eb8e66fb65d6f853a5a",
                    "hadoopsource_id": 2,
                    "format": "py",
                    "state": 2
                },
                {
                    "id": 7,
                    "source": "/ops/hadoop-server-test/python/testfile.txt",
                    "amount": null,
                    "feature": null,
                    "hashsum": "d80d668df262e4a88c6f7d1f0dfd2bdc",
                    "hadoopsource_id": 2,
                    "format": "txt",
                    "state": 2
                },
                {
                    "id": 8,
                    "source": "/ops/hadoop-server-test/python/tmp/iris.data",
                    "amount": null,
                    "feature": null,
                    "hashsum": "7a1c6dc40b600415d7113cf9e0b1aab5",
                    "hadoopsource_id": 2,
                    "format": "data",
                    "state": 2
                },
                {
                    "id": 9,
                    "source": "/ops/hadoop-server-test/python/tmp/iris.data1",
                    "amount": null,
                    "feature": null,
                    "hashsum": "7a1c6dc40b600415d7113cf9e0b1aab5",
                    "hadoopsource_id": 2,
                    "format": "data1",
                    "state": 2
                },
                {
                    "id": 10,
                    "source": "/test/hadoop-server-test/mongo/iris.data",
                    "amount": null,
                    "feature": null,
                    "hashsum": "7a1c6dc40b600415d7113cf9e0b1aab5",
                    "hadoopsource_id": 3,
                    "format": "data",
                    "state": 2
                }
            ],
            delList: [],
            editVisible: false,
            pageTotal: 10,
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