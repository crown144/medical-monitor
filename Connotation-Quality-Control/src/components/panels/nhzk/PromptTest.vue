<template>
    <div class="container">
        <div style="flex-grow:1;display: flex;flex-direction: column;height:950px;">
            <!-- 选择与按钮 -->
            <div
                style="min-height: 50px;width: 100%;display: flex;align-items: center;margin-top: 20px;border-bottom:1px solid;">
                <div style="width: 10%;"></div>
                <div style="height: 100%;display: flex;align-items: center;">
                    <span style="font-size: large;">规则类型: </span>
                    <span style="font-size: large;color: red;">{{ mess.disease_value }}</span>
                </div>
                <div style="margin-left: 40px;height: 100%;display: flex;align-items: center;">
                    <span style="font-size: large;">规则名称: </span>
                    <span style="font-size: large;color: red;">{{ mess.indicator_name }}</span>
                </div>
                <div style="flex-grow: 1;display: flex;align-items: center"></div>
                <div style="margin-left: 40px;height: 100%;display: flex;align-items: center;">
                    <span style="font-size: large;">测试文件</span>
                    <el-select v-model="file_name" placeholder="Select" style="margin-left: 20px;width: 150px;">
                        <el-option v-for="(file, index) in test_file" :key="index" :label="file" :value="file" />
                    </el-select>
                </div>

                <el-button style="margin-left: 2%;" @click="run_test">测试</el-button>
                <div style="width: 10%;"></div>
            </div>
            <!-- prompt展示 -->
            <div style="width: 100%;display: flex;justify-content: center;margin-top: 15px;">
                <div style="width: 80%;display: flex;">
                    <!-- <span style="font-size: 20px;margin-right: 10px;">prompt:</span> -->
                    <div style="width: 80%;display: flex;flex-direction: column;align-items: center;">
                        <el-card :class="{ expanded: isExpanded, collapsed: !isExpanded }" style="width: 100%;" shadow="hover">
                            <template #header>
                                <div style="display: flex;justify-content: space-between;">
                                    <span style="font-size: 18px;display: flex;align-items: center;">Card name</span>
                                </div>
                            </template>
                            <div style="display: flex;justify-content: space-between">
                                <div style="display: flex;width: 100%;align-items: center;">
                                    <div>
                                        <span style="font-size: 18px;">版本号：</span>
                                    </div>
                                    <!-- 版本显示和按钮 -->
                                    <div style="width: 20%;display: flex;height: min-content;">
                                        <!-- <el-input ref="versionTextarea" type="textarea" autosize resize="none"
                                            width="auto" readonly style="font-size: 16px;" v-model="mess.version">
                                        </el-input> -->
                                        <span style="font-size: 15px;line-height: 1.5;">{{ mess.version }}</span>
                                    </div>
                                </div>
                                <div style="width: 20%;min-width: 200px;">
                                    <span>是否是当前的prompt：</span>
                                    <el-switch v-model="mess.enable_or_not" disabled inline-prompt active-text="是" inactive-text="否" />
                                </div>
                            </div>
                            <div style="display: flex;justify-content: flex-start;margin-top: 20px;">
                                <div>
                                    <span style="font-size: 18px;"> 描述：</span>
                                </div>
                                <!-- 描述显示和按钮 -->
                                <div style="width: 90%;display: flex;height: min-content;">
                                    <span style="font-size: 15px;line-height: 1.5;">{{ mess.description }}</span>
                                </div>
                            </div>
                            <div style="display: flex;width: 100%;margin-top: 20px;">
                                <div style="flex-shrink: 0">
                                    <span style="font-size: 18px;">规则：</span>
                                </div>
                                <!-- 规则显示和按钮 -->
                                <div style="width: 90%;display: flex;height: min-content;">
                                    <span style="font-size: 15px;line-height: 1.5;">{{ mess.rule }}</span>
                                </div>
                            </div>
                            <!-- 边界线 -->
                            <div style="width: 100%;border-top:solid 1px;margin-top: 20px;margin-bottom: 20px; ">
                            </div>
                            <!-- prompt -->
                            <div>
                                <div style="display: flex;justify-content: space-between">
                                    <span style="font-size: 18px;">prompt：</span>
                                </div>
                                <!-- 表格 -->
                                <div style="margin-top: 20px;">
                                    <div style="width:100%;display: flex;justify-content: center;">
                                        <el-table border :data="mess.tableData" style="width: 80%;">
                                            <el-table-column label="编号" min-width="70" width="110" align="center">
                                                <template #default="scope">
                                                    <span v-if="scope.row.flag1 == 1" style="font-size: 16px;">{{
                                                        scope.row.index
                                                        }}</span>
                                                    <el-input v-else class="blue-border" type="textarea" autosize
                                                        resize="none" style="font-size: 16px;"
                                                        v-model="scope.row.index"></el-input>
                                                </template>
                                            </el-table-column>
                                            <el-table-column label="prompt内容" min-width="520" align="center">
                                                <template #default="scope">
                                                    <el-input v-if="scope.row.flag1 == 1" class="no-border"
                                                        type="textarea" readonly autosize resize="none"
                                                        style="font-size: 16px;" v-model="scope.row.prompt"></el-input>
                                                    <el-input v-else ref="myTextarea" class="blue-border"
                                                        type="textarea" autosize resize="none" style="font-size: 16px;"
                                                        v-model="scope.row.prompt"></el-input>
                                                </template>
                                            </el-table-column>
                                        </el-table>
                                    </div>
                                </div>
                            </div>
                        </el-card>
                        <el-button size="small" @click="toggleExpand">{{ isExpanded ? '收起' : '展开' }}</el-button>
                    </div>
                    <div style="width: 20%;display: flex;align-items: center;justify-content:center ">
                        <span v-if="running" style="font-size: large;">准确率：{{ accuracy }}%</span>
                        <!-- 转圈圈 -->
                        <div v-else style="width: 100%;height: 100%;position: relative">
                            <div class="run b1"></div>
                            <div class="run b2"></div>
                            <div
                                style="position: absolute;top: 50%;left: 50%;transform: translate(-50%, -50%);z-index: 4;">
                                测试中</div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- <el-button @click="toggleExpand">{{ isExpanded ? '收起' : '展开' }}</el-button> -->
            <!-- 测试结果 -->
            <div style="width: 100%;height: 850px;display: flex;align-items: center;flex-direction: column;">
                <el-table id="tableId" border :data="tableData"
                    style="width: 80%;margin-top: 30px; border: 0;max-height: 90%;overflow-y: auto" class="custom-table"
                    :header-cell-style="tableHeaderColor">
                    <el-table-column label="病例编号" width="100" align="center">
                        <template #default="scope">
                            <span style="font-size: 16px;">{{ scope.row.emr_id }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column width="340" label="电子病例原文" align="center">
                        <template #default="scope">
                            <!-- <span style="font-size: 16px;">{{ scope.row.prompt }}</span> -->
                            <el-input type="textarea" readonly :rows="4" style="font-size: 16px;"
                                v-model="scope.row.content"></el-input>
                        </template>
                    </el-table-column>
                    <el-table-column width="340" label="模型分析" align="center">
                        <template #default="scope">
                            <el-input type="textarea" readonly :rows="4" style="font-size: 16px;"
                                v-model="scope.row.predict"></el-input>
                        </template>
                    </el-table-column>
                    <el-table-column width="340" label="标注分析" align="center">
                        <template #default="scope">
                            <!-- <span style="font-size: 16px;">{{ scope.row.prompt }}</span> -->
                            <el-input type="textarea" readonly :rows="4" style="font-size: 16px;"
                                v-model="scope.row.label"></el-input>
                        </template>
                    </el-table-column>
                    <el-table-column label="模型答案" width="115" align="center">
                        <template #default="scope">
                            <span style="font-size: 16px;">{{ change[scope.row.yes_or_no] }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="标注答案" align="center">
                        <template #default="scope">
                            <span style="font-size: 16px;">{{ change[scope.row.label_yes_or_no] }}</span>
                        </template>
                    </el-table-column>
                </el-table>
                <div style="display: flex; justify-content: flex-end;width: 80%;margin-top: 10px;">
                    <el-pagination :page-size="5" :pager-count="5" layout="prev, pager, next" :total="total_data"
                        v-model:current-page="currentPage" />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import request from '@/api/request';
export default {
    props: ['mess'],
    data() {
        return {
            disease_value: '001001001001',
            indicator_name: '100100100100',
            prompt_content: '',
            tableHeaderColor: {
                background: ' #f5f5f5 !important',
                color: '#333333',
                fontSize: '14px',
                textAlign: 'center',
            },
            currentPage: 1,
            test_file: ['file1'],
            file_name: '111',
            accuracy: 70,
            tableData: [],
            total_data: 0,
            running: true,
            change: { 1: '是', 0: '否' },
            isExpanded:false,
        }
    },
    methods: {
        async get_file() {
            try {
                // const params = {
                //     index_prompt_id: row.index_prompt_id,
                //     indicator_number: this.currentState.indicator_number,
                // };
                const response = await request.get('/prompt_test/file_list'); // 修改为实际的 API 端点和参数
                this.test_file = response.files;
                this.file_name = this.test_file[0];
            }
            catch (error) {
                console.error('Error fetching data:', error);
            }
        },
        async get_result() {
            try {
                const params = {
                    index_prompt_set_id:this.mess.index_prompt_set_id,
                    file_name: this.file_name,
                    size: 5,
                };
                const response = await request.get('/prompt_test/search', { params }); // 修改为实际的 API 端点和参数
                this.tableData = response.data;
                this.total_data = response.data_count;
                this.accuracy = response.accuracy * 100;
            }
            catch (error) {
                console.error('Error fetching data:', error);
            }
        },
        async run_test() {
            try {
                this.running = false;
                const params = {
                    index_prompt_set_id: this.mess.index_prompt_set_id,
                    indicator_number: this.mess.indicator_number,
                    disease: this.mess.disease_value,
                    indicator_name: this.mess.indicator_name,
                    file_name: this.file_name,
                };
                this.tableData = [];
                const response = await request.get('/prompt_test/one_test', { params }); // 修改为实际的 API 端点和参数
                if (response.hasOwnProperty('message')) {
                    window.alert(response.message);
                }
                this.currentPage = 1;
                this.get_result();
                this.running = true;
            }
            catch (error) {
                console.error('Error fetching data:', error);
            }
        },
        toggleExpand() {
            this.isExpanded = !this.isExpanded;
        }
    },
    watch: {
        file_name() {
            this.get_result();
        },
        currentPage() {
            this.get_result();
        },
    },
    mounted() {
        this.get_file();
    }
};
</script>

<style scoped>
.container {
    display: flex;
    max-height: 950px;
    flex-direction: column;
    background-color: white
}

.custom-table {
    border-radius: 15px;
    /* 增加圆角 */
}

@keyframes go {
    0% {
        transform: rotate(0deg);
    }

    90% {
        transform: rotate(360deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

@keyframes un_go {
    0% {
        transform: rotate(0deg);
    }

    99% {
        transform: rotate(-360deg);
    }

    100% {
        transform: rotate(-360deg);
    }
}

.run {
    width: 70px;
    height: 70px;
    background-color: aqua;
    position: absolute;
    border-radius: 50%;
    left: calc(50% - 35px);
    top: calc(50% - 35px);
    animation: 3s go infinite;
}

.run::after {
    content: "";
    height: 50%;
    width: 100%;
    background-color: white;
    left: 0;
    top: 50%;
    position: absolute;
    border-radius: 50%;

}

.run::before {
    content: "";
    height: calc(100% - 14px);
    width: calc(100% - 14px);
    position: absolute;
    left: 7px;
    top: 7px;
    background-color: white;
    border-radius: 50%;
}

.b1 {
    z-index: 3;
    animation: 2.5s un_go infinite;
}

.b2 {
    width: 100px;
    height: 100px;
    background-color: rgb(64, 64, 230);
    z-index: 2;
    left: calc(50% - 50px);
    top: calc(50% - 50px);
}
::v-deep .no-border .el-textarea__inner {
    border: none;
    box-shadow: none;
}

::v-deep .blue-border .el-textarea__inner {
    --el-input-border-color: #409eff !important;
}
.collapsed {
  max-height: 200px;
  overflow: auto;
  transition: max-height 0.3s ease-out;
}

.expanded {
    max-height: none;
    transition: max-height 0.3s ease-out;
}
</style>