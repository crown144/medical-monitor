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
                <!-- <el-button plain type="primary" @click="" style="margin-right: 10%;">重置</el-button> -->
            </div>
        </div>
        <!-- 分界线 -->
        <div style="width: 100%;border-top:solid 1px;margin-top: 20px;margin-bottom: 20px; ">
        </div>
        <div style="margin-bottom: 20px;width: 80%;display: flex;justify-content: space-between;align-items: center;">
            <span style="font-size: 20px;">查询表格{{ add_act }}</span>
            <el-button plain style="margin-left: 2%;" @click="flag_add = true;">新增字段来源</el-button>
        </div>
        <!-- 表格 -->
        <div style="height: 600px;width: 80%;">
            <el-table border :data="tableData" :header-cell-style="tableHeaderColor">
                <el-table-column label="字段1" style="width: 33%;" align="center">
                    <template #default="scope">
                        <span style="font-size: 16px;">{{ scope.row.field1 }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="字段2" style="width: 33%;" align="center">
                    <template #default="scope">
                        <span style="font-size: 16px;">{{ scope.row.field2 }}</span>
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
                    </template>
                </el-table-column>
            </el-table>
        </div>
    </div>
    <el-dialog v-model="flag_add" title="添加" width="700" style="min-height: 200px;" :destroy-on-close=true
        :before-close="close_dialog_add">
        <div style="width: 100%;display: flex;flex-direction: column;align-items: center;">
            <div style="display: flex;width: 70%;margin-top: 30px;align-items: center">
                <div>
                    <span style="font-size: 16px;">病种名： xxxxxxxx</span>
                </div>
            </div>
            <div style="display: flex;width: 70%;margin-top: 30px;align-items: center">
                <div>
                    <span style="font-size: 16px;">指标名： xxxxxxxx</span>
                </div>
            </div>
            <div style="display: flex;justify-content: center;width: 70%;margin-top: 30px;align-items: center">
                <div style="flex-shrink: 0;">
                    <span style="font-size: 16px;">新增字段1：</span>
                </div>
                <el-input type="textarea" autosize resize="none" style="font-size: 15px;"
                    v-model="add_field1">
                </el-input>
            </div>
            <div style="display: flex;justify-content: center;width: 70%;margin-top: 30px;align-items: center">
                <div style="flex-shrink: 0;">
                    <span style="font-size: 16px;">新增字段2：</span>
                </div>
                <el-input type="textarea" autosize resize="none" style="font-size: 15px;"
                    v-model="add_field2">
                </el-input>
            </div>
        </div>
        <div style="width: 100%;display: flex;flex-direction: row-reverse;margin-bottom: 10px;margin-top: 30px;">
            <el-button plain style="" @click="flag_add=false;">取消</el-button>
            <el-button plain style="margin-right: 10px;" @click="add_act = 1;">确认</el-button>
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
            tableHeaderColor: {
                background: ' #f5f5f5 !important',
                color: '#333333',
                fontSize: '14px',
                textAlign: 'center',
            },
            tableData: [{ field1: '001', field2: '002' }, { field1: '001', field2: '002' }],
            flag_add: false,
            add_field1: '',
            add_field2: '',
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
            this.disease_value = this.list1[0];
            setTimeout(() => {
                this.index_value = 0;
                this.currentState = {
                    disease_value: this.disease_value,
                    index_value: this.index_value,
                };
            }, 100); // 100毫秒等于0.1秒
        },
        close_dialog_add(done) {
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