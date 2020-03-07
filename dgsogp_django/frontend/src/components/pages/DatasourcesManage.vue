<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-location"></i> 数据源管理
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="handle-box">
                <el-input v-model="query.name" placeholder="" class="handle-input mr10"></el-input>
                <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
                <el-button type="primary" icon="el-icon-lx-add" @click="">添加数据源</el-button>
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
                <el-table-column prop="wgroup" label="工作组"></el-table-column>
                <el-table-column prop="wserver" label="工作服务器"></el-table-column>
                <el-table-column prop="type" label="数据源类型">
                    <template slot-scope="scope">
                        {{
                            scope.row.type == '0' ? "文件" :
                            scope.row.type == '1' ? "目录" :
                            scope.row.type == '2' ? "数据库" : ""
                        }}
                    </template>
                </el-table-column>
                <el-table-column prop="source" label="路径/数据库"></el-table-column>
                <el-table-column prop="putindb" label="入库需求">
                    <template slot-scope="scope">
                        {{
                            scope.row.putindb == '0' ? "是" :
                            scope.row.putindb == '1' ? "否" : ""
                        }}
                    </template>
                </el-table-column>
                <el-table-column prop="related" label="结构存储形式">
                    <template slot-scope="scope">
                        {{
                            scope.row.related == '0' ? "关系型" :
                            scope.row.related == '1' ? "非关系型" : ""
                        }}
                    </template>
                </el-table-column>
                <el-table-column prop="pattern" label="采集模式">
                    <template slot-scope="scope">
                        {{
                            scope.row.pattern == '0' ? "只采集一次" :
                            scope.row.pattern == '1' ? "每天采集一次" : ""
                        }}
                    </template>
                </el-table-column>
                <el-table-column prop="target" label="Hadoop路径"></el-table-column>
                <el-table-column prop="state" label="处理状态">
                    <template slot-scope="scope">
                        {{
                            scope.row.state == '0' ? "未采集" :
                            scope.row.state == '1' ? "持续采集中" :
                            scope.row.state == '2' ? "已完成" : ""
                        }}
                    </template>
                </el-table-column>
                <el-table-column prop="content" label="备注"></el-table-column>
                <el-table-column prop="excepted" label="异常状态">
                    <template slot-scope="scope">
                        {{
                            scope.row.excepted == '0' ? "正常" :
                            scope.row.excepted == '1' ? "异常" : ""
                        }}
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="180" align="center">
                    <template slot-scope="scope">
                        <el-button
                            type="text"
                            icon="el-icon-edit"
                            @click="handleEdit(scope.$index, scope.row)"
                        >编辑</el-button>
                        <el-button
                            type="text"
                            icon="el-icon-delete"
                            class="red"
                            @click="handleDelete(scope.$index, scope.row)"
                        >删除</el-button>
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

        <!-- 编辑弹出框 -->
        <el-dialog title="编辑" :visible.sync="editVisible" width="30%">
            <el-form ref="form" :model="form" label-width="70px">
                <el-form-item label="用户昵称">
                    <el-input v-model="form.nickname"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>

    </div>
</template>

<script>
import { fetchData } from '../../api/index';
export default {
    name: 'DatasourcesManage',
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
                    "wgroup": "dev",
                    "wserver": "hadoop-server-test",
                    "type": 0,
                    "source": "/home/wing/Code/base/python/iris.data",
                    "putindb": 0,
                    "related": 0,
                    "pattern": 0,
                    "target": "/iris.data",
                    "state": 2,
                    "content": "花朵分类数据",
                    "excepted": 0
                },
                {
                    "id": 2,
                    "wgroup": "ops",
                    "wserver": "hadoop-server-test",
                    "type": 1,
                    "source": "/home/wing/Code/base/python",
                    "putindb": 1,
                    "related": 1,
                    "pattern": 0,
                    "target": "/python",
                    "state": 2,
                    "content": "python脚本",
                    "excepted": 0
                },
                {
                    "id": 3,
                    "wgroup": "test",
                    "wserver": "hadoop-server-test",
                    "type": 0,
                    "source": "/home/wing/Code/base/python/iris.data",
                    "putindb": 0,
                    "related": 1,
                    "pattern": 0,
                    "target": "/mongo/iris.data",
                    "state": 2,
                    "content": "花朵分类数据",
                    "excepted": 0
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
