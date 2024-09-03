<template>
    <div class="container">
        <div style="min-height: 100px;width: 80%;display: flex;align-items: center;">
            <div style="height: 50px;display: flex;align-items: center;margin-top: 20px;flex-shrink: 0;width: 100%;">
                <div>
                    <span style="height: 80%;">规则类型：</span>
                </div>
                <el-select v-model="disease_value" placeholder="Select" style="width: 250px;">
                    <el-option v-for="item in list1" :key="item" :label="item" :value="item" />
                </el-select>
                <div style="width: 20px;"></div>
                <div>
                    <span style="height: 80%;">规则名称：</span>
                </div>
                <el-select v-model="index_value" placeholder="选择指标" style="width: 250px;">
                    <el-option v-for="(item, index) in options_index" :key="item.indicator_number"
                        :label="item.indicator_name" :value="index" />
                </el-select>
                <div style="flex-grow: 1;"></div>
                <el-button plain style="margin-left: 2%;" @click="">确定</el-button>
                <el-button plain type="primary" @click="reset()" style="margin-right: 10%;">重置</el-button>
            </div>
        </div>
        <!-- 分割线 -->
        <div style="width: 100%;border-top:solid 1px;margin-top: 20px;margin-bottom: 20px; ">
        </div>
        <div style="margin-bottom: 20px;width: 80%;display: flex;justify-content: space-between;align-items: center;">
            <span style="font-size: 20px;">查询表格{{ add_act }}</span>
            <el-button plain style="margin-left: 2%;" @click="flag_add = true;">新增指标</el-button>
        </div>
        <div style="height: 600px;width: 80%;">
            <el-table border :data="tableData" :header-cell-style="tableHeaderColor">
                <el-table-column label="病种名" style="width: 33%;" align="center">
                    <template #default="scope">
                        <span style="font-size: 16px;">{{ scope.row.disease_value }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="指标名" style="width: 33%;" align="center">
                    <template #default="scope">
                        <span style="font-size: 16px;">{{ scope.row.indicator_name }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="操作" style="width: 33%;" align="center">
                    <template #default="scope">
                        <el-button link type="primary" size="small" @click="">
                            编辑
                        </el-button>
                        <el-button link type="primary" size="small" @click="">
                            删除
                        </el-button>
                        <el-button link type="primary" size="small" @click="">
                            字段溯源
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
    </div>

    <el-dialog v-model="flag_add" title="添加" width="700" style="min-height: 200px;" :destroy-on-close=true :before-close="close_dialog_add">
        <div style="width: 100%;height: 120px;display: flex;justify-content: center;align-items: center;">
            <el-steps style="width: 60%;" :active="add_act">
                <el-step title="选择疾病名" />
                <el-step title="输入指标名" />
                <!-- <el-step  title="Some description" /> -->
            </el-steps>
        </div>
        <!-- 第一步 -->
        <div v-show="add_act == 1" style="width: 100%;display: flex;flex-direction: column;">
            <div v-show="flag_add_disease" style="width: 100%;display: flex;flex-direction: column;">
                <div style="display: flex;justify-content: center;width: 100%;margin-top: 30px;align-items: center">
                    <div>
                        <span style="font-size: 20px;">规则类型：</span>
                    </div>
                    <el-select v-model="add_index.disease_value" placeholder="Select" style="width: 250px;">
                        <el-option v-for="item in list1" :key="item" :label="item" :value="item" />
                    </el-select>
                    <span style="font-size: 15px;margin-left: 10px;margin-right: 10px;">或</span>
                    <el-button plain style="" @click="flag_add_disease = false;">新增病种</el-button>
                </div>
                <!-- <div
                    style="width: 100%;justify-content: center;display: flex;height: 30px;margin-top: 30px;margin-bottom: 30px;align-items: center;">
                    <span style="font-size: 25px;">或者</span>
                </div> -->
                <!-- <div style="width: 100%;justify-content: center;display: flex;">
                    <el-button plain style="" @click="flag_add_disease = false;">新增病种</el-button>
                </div> -->
            </div>
            <!-- 新增疾病 -->
            <div v-show="!flag_add_disease" style="width: 100%;display: flex;flex-direction: column;">
                <div style="display: flex;justify-content: center;width: 100%;margin-top: 30px;align-items: center">
                    <div>
                        <span style="font-size: 15px;">新增规则类型：</span>
                    </div>
                    <el-input type="textarea" autosize resize="none" style="font-size: 15px;width: 50%;"
                        v-model="add_index.new_disease">
                    </el-input>
                    <el-button plain style="margin-left: 20px" @click="flag_add_disease = true;">取消新增</el-button>
                </div>
            </div>
            <!-- 分割线 -->
            <div style="width: 100%;border-top:solid 1px;margin-top: 30px;margin-bottom: 30px; ">
            </div>
            <div style="width: 100%;display: flex;flex-direction: row-reverse;margin-bottom: 20px;">
                <el-button plain style="" @click="add_act = 2;">下一步</el-button>
            </div>
        </div>

        <!-- 第二步 -->
        <div v-show="add_act == 2" style="width: 100%;display: flex;flex-direction: column;">
            <div style="display: flex;justify-content: center;width: 100%;margin-top: 30px;align-items: center">
                <div>
                    <span style="font-size: 20px;">新增规则名称：</span>
                </div>
                <el-input type="textarea" autosize resize="none" style="font-size: 15px;width: 50%;"
                    v-model="add_index.new_index">
                </el-input>
            </div>


            <!-- 分割线 -->
            <div style="width: 100%;border-top:solid 1px;margin-top: 30px;margin-bottom: 30px; ">
            </div>
            <div style="width: 100%;display: flex;flex-direction: row-reverse;margin-bottom: 20px;">
                <el-button plain style="" @click="">下一步</el-button>
                <el-button plain style="margin-right: 10px;" @click="add_act = 1;">上一步</el-button>
            </div>
        </div>

    </el-dialog>
</template>


<script>
import request from '@/api/request';
export default {
    data() {
        return {
            disease_value: '',
            index_value: null,
            list1: [],
            list2: [],
            options_index: [],
            currentState: {},
            tableData: [{ disease_value: '111', index_value: '222' },
            { disease_value: '111', index_value: '222' }
            ],
            tableHeaderColor: {
                background: ' #f5f5f5 !important',
                color: '#333333',
                fontSize: '14px',
                textAlign: 'center',
            },
            flag_add: false,
            add_act: 1,
            add_index: {},
            flag_add_disease: true,
            new_disease: '',
        }
    },
    methods: {
        async get_disease() {
            try {
                const response = await request.get('/hospital_diseases'); // 修改为实际的 API 端点和参数
                const data = response;
                this.processDisease(data);
            }
            catch (error) {
                console.error('Error fetching data:', error);
            }
        },
        processDisease(data) {
            const a = data['1院'];
            const b = data['2院'];
            const keysSet = new Set([...Object.keys(a), ...Object.keys(b)]);
            this.list1 = Array.from(keysSet);
            this.list2 = this.list1.map(key => {
                const combinedArray = [
                    ...(a[key] || []),
                    ...(b[key] || [])
                ];
                // 使用 Set 去重
                const uniqueItems = Array.from(new Map(combinedArray.map(item => [item.indicator_number, item])).values());
                return { [key]: uniqueItems };
            });
            console.log(this.list2)
            this.tableData = [];
            this.list2.forEach(item => {
                // 遍历每个对象的键值对
                Object.keys(item).forEach(key => {
                    // 遍历键对应的数组中的每个对象
                    item[key].forEach(value => {
                        value.disease_value = key;
                        this.tableData.push(value);
                    });
                });
            });
            console.log(this.tableData)
        },
        reset() {
            this.disease_value = '';
            this.index_value = numm;
        },
        close_dialog_add(done) {
            this.add_index={};
            this.add_act=1;
            this.flag_add_disease=true;
            done()
        },
    },
    mounted() {
        this.get_disease();
    },
    watch: {
        disease_value(neww) {
            this.options_index = {};
            this.index_value = ''
            const searchKey = neww;
            const result = this.list2.find(item => Object.keys(item)[0] === searchKey);
            this.options_index = result ? result[searchKey] : 'No results found';
        },
    }
}
</script>

<style scoped>
.container {
    display: flex;
    /* max-height: 950px; */
    min-height: 80vh;
    flex-direction: column;
    background-color: white;
    align-items: center;
}
</style>