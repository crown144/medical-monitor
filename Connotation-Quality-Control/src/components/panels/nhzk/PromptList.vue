<template>
    <div class="container">
        <div style="flex-grow:1;display: flex;flex-direction: column;justify-content: center;">
            <!-- 选择与按钮 -->
            <div style="height: 50px;display: flex;align-items: center;margin-top: 20px;flex-shrink: 0;">
                <div style="width: 10%;"></div>
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
                <el-button plain style="margin-left: 2%;" @click="currentState = {
                    disease_value: this.disease_value,
                    index_value: this.index_value,
                }; get_card();">确定</el-button>


                <div style="flex-grow: 1;"></div>
                <el-button plain type="primary" @click="flag_add = true" style="margin-right: 10%;">新增卡片</el-button>
            </div>
            <div style="width: 100%;border-top:solid 1px;margin-top: 20px;margin-bottom: 20px;"></div>
            <!-- 卡片 -->
            <div style="width: 100%;display: flex;align-items: center;flex-direction: column;margin-top: 20px;">
                <el-card style="width: 80%;" shadow="hover">
                    <template #header>
                        <div style="display: flex;justify-content: space-between;">
                            <span style="font-size: 18px;display: flex;align-items: center;">Card name</span>
                            <div>
                                <el-button type="success" plain @click="changeActiveName()">测试</el-button>
                                <el-button type="danger" plain @click="flag_delete = true">删除</el-button>
                            </div>
                        </div>
                    </template>
                    <div style="display: flex;justify-content: flex-start">
                        <div>
                            <span style="font-size: 18px;">版本号：</span>
                        </div>
                        <!-- 版本显示和按钮 -->
                        <div style="width: 20%;display: flex;height: min-content;">
                            <!-- <el-input :class="no-border" type="textarea" readonly autosize resize="none" style="font-size: 16px;" v-model="rule"></el-input> -->
                            <div v-if="flag_version" style="max-width: 100%;display: flex;">
                                <span style="font-size: 15px;line-height: 1.5;">{{ version }}</span>
                            </div>
                            <el-input v-else ref="versionTextarea" type="textarea" autosize resize="none" width="auto"
                                style="font-size: 16px;" v-model="version_temp">
                            </el-input>
                            <div style="display: flex;height: auto;align-items: center;">
                                <div v-if="flag_version"
                                    style="width: 110px;display: flex;align-items: center;margin-left: 15px;">
                                    <el-button link type="primary" size="small" @click="edit_version">
                                        编辑
                                    </el-button>
                                </div>
                                <div v-else style="width: 110px;display: flex;align-items: center;margin-left: 15px">
                                    <el-button link type="primary" size="small"
                                        @click="this.flag_version = true; this.version = this.version_temp; edit_card()">
                                        确认
                                    </el-button>
                                    <el-button link type="primary" size="small" @click="cancel_version">
                                        取消
                                    </el-button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div style="display: flex;justify-content: flex-start;margin-top: 20px;">
                        <div>
                            <span style="font-size: 18px;"> 描述：</span>
                        </div>
                        <!-- 描述显示和按钮 -->
                        <div style="width: 90%;display: flex;height: min-content;">
                            <div v-if="flag_description" style="max-width: 100%;display: flex;">
                                <span style="font-size: 15px;line-height: 1.5;">{{ description }}</span>
                            </div>
                            <el-input v-else ref="descriptionTextarea" type="textarea" autosize resize="none"
                                width="auto" style="font-size: 16px;" v-model="description_temp">
                            </el-input>
                            <div style="display: flex;height: auto;align-items: center;">
                                <div v-if="flag_description"
                                    style="width: 110px;display: flex;align-items: center;margin-left: 15px;">
                                    <el-button link type="primary" size="small" @click="edit_description">
                                        编辑
                                    </el-button>
                                </div>
                                <div v-else style="width: 110px;display: flex;align-items: center;margin-left: 15px">
                                    <el-button link type="primary" size="small"
                                        @click="this.flag_description = true; this.description = this.description_temp; edit_card()">
                                        确认
                                    </el-button>
                                    <el-button link type="primary" size="small" @click="cancel_description">
                                        取消
                                    </el-button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div style="display: flex;width: 100%;margin-top: 20px;">
                        <div style="flex-shrink: 0">
                            <span style="font-size: 18px;">规则：</span>
                        </div>
                        <!-- 规则显示和按钮 -->
                        <div style="width: 80%;display: flex;height: min-content;">
                            <!-- <el-input :class="no-border" type="textarea" readonly autosize resize="none" style="font-size: 16px;" v-model="rule"></el-input> -->
                            <div v-if="flag1" style="max-width: 100%;display: flex;">
                                <span style="font-size: 15px;line-height: 1.5;">{{ rule }}</span>
                            </div>
                            <el-input v-else ref="ruleTextarea" type="textarea" autosize resize="none" width="auto"
                                style="font-size: 16px;" v-model="rule_temp"></el-input>

                            <div style="display: flex;height: auto;align-items: center;">
                                <div v-if="flag1"
                                    style="width: 110px;display: flex;align-items: center;margin-left: 15px;">
                                    <el-button link type="primary" size="small" @click="edit_rule">
                                        编辑
                                    </el-button>
                                </div>
                                <div v-else style="width: 110px;display: flex;align-items: center;margin-left: 15px">
                                    <el-button link type="primary" size="small"
                                        @click="this.flag1 = true; this.rule = this.rule_temp; edit_card()">
                                        确认
                                    </el-button>
                                    <el-button link type="primary" size="small" @click="cancel_rule">
                                        取消
                                    </el-button>
                                </div>
                            </div>
                        </div>
                        <div style="width: 20%;">
                            <span>是否是当前的prompt：</span>
                            <el-switch v-model="enable_or_not" @click="change_enable" inline-prompt active-text="是"
                                inactive-text="否" />
                        </div>
                    </div>
                    <!-- 边界线 -->
                    <div style="width: 100%;border-top:solid 1px;margin-top: 20px;margin-bottom: 20px; ">
                    </div>
                    <!-- prompt -->
                    <div>
                        <div style="display: flex;justify-content: space-between">
                            <span style="font-size: 18px;">prompt：</span>
                            <!-- <div v-if="flag2">
                                <el-button type="primary" plain @click="edit_confirm">保存</el-button>
                                <el-button type="default" plain @click="reset_table()">重置</el-button>
                            </div> -->
                        </div>
                        <!-- 表格 -->
                        <div style="margin-top: 20px;">
                            <el-table border :data="tableData">
                                <el-table-column label="编号" min-width="70" width="110" align="center">
                                    <template #default="scope">
                                        <span v-if="scope.row.flag1 == 1" style="font-size: 16px;">{{ scope.row.order
                                            }}</span>
                                        <el-input v-else class="blue-border" type="textarea" autosize resize="none"
                                            style="font-size: 16px;" v-model="scope.row.order"></el-input>
                                    </template>
                                </el-table-column>
                                <el-table-column label="prompt内容" min-width="520" align="center">
                                    <template #default="scope">
                                        <el-input v-if="scope.row.flag1 == 1" class="no-border" type="textarea" readonly
                                            autosize resize="none" style="font-size: 16px;"
                                            v-model="scope.row.prompt"></el-input>
                                        <el-input v-else ref="myTextarea" class="blue-border" type="textarea" autosize
                                            resize="none" style="font-size: 16px;"
                                            v-model="scope.row.prompt"></el-input>
                                    </template>
                                </el-table-column>
                                <el-table-column label="Operations" min-width="110" width="110" align="center">
                                    <template #default="scope">
                                        <div v-if="scope.row.flag1 == 1">
                                            <el-button link type="primary" size="small"
                                                @click="edit_line(scope.$index, 0)">
                                                编辑
                                            </el-button>
                                            <el-button link type="primary" size="small"
                                                @click="delete_line(scope.$index, 0)">
                                                删除
                                            </el-button>
                                        </div>
                                        <div v-else-if="scope.row.flag1 == 2">
                                            <el-button link type="primary" size="small"
                                                @click="confirm_linedata(scope.$index, 0)">
                                                确认
                                            </el-button>
                                            <el-button link type="primary" size="small"
                                                @click="cancel_line(scope.$index, 0)">
                                                取消
                                            </el-button>
                                        </div>
                                        <div v-else-if="scope.row.flag1 == 3">
                                            <el-button link type="primary" size="small"
                                                @click="confirm_add_prompt(scope.$index, 0)">
                                                确认
                                            </el-button>
                                            <el-button link type="primary" size="small"
                                                @click="cancel_add_prompt(scope.$index, 0)">
                                                取消
                                            </el-button>
                                        </div>
                                    </template>
                                </el-table-column>
                            </el-table>
                            <div style="width:100%;display: flex;justify-content: center;">
                                <el-button type="primary" size="small" plain @click="add_prompt(0)">添加</el-button>
                            </div>
                        </div>
                    </div>
                </el-card>
                <div style="display: flex; justify-content: flex-end;width: 80%;height: 75px;">
                    <el-pagination :page-size="pageSize" :pager-count="5" layout="prev, pager, next" :total="total_data"
                        v-model:current-page="currentPage" />
                </div>
            </div>
        </div>
    </div>

    <el-dialog v-model="flag_add" title="添加prompt" style="width: 80%;" :destroy-on-close=true
        :before-close="close_dialog_add">
        <el-card style="width: 100%;" shadow="hover">
            <template #header>
                <div style="display: flex;justify-content: space-between;">
                    <span style="font-size: 18px;display: flex;align-items: center;">Card name</span>
                </div>
            </template>
            <div style="display: flex;justify-content: space-between">
                <div style="display: flex;width: 100%;">
                    <div>
                        <span style="font-size: 18px;">版本号：</span>
                    </div>
                    <!-- 版本显示和按钮 -->
                    <div style="width: 20%;display: flex;height: min-content;">
                        <el-input ref="versionTextarea" type="textarea" autosize resize="none" width="auto"
                            style="font-size: 16px;" v-model="form.version">
                        </el-input>
                    </div>
                </div>
                <div style="width: 20%;">
                    <span>是否是当前的prompt：</span>
                    <el-switch v-model="form.enable_or_not" inline-prompt active-text="是" inactive-text="否" />
                </div>
            </div>
            <div style="display: flex;justify-content: flex-start;margin-top: 20px;">
                <div>
                    <span style="font-size: 18px;"> 描述：</span>
                </div>
                <!-- 描述显示和按钮 -->
                <div style="width: 90%;display: flex;height: min-content;">
                    <el-input ref="descriptionTextarea" type="textarea" autosize resize="none" width="auto"
                        style="font-size: 16px;" v-model="form.description">
                    </el-input>
                </div>
            </div>
            <div style="display: flex;width: 100%;margin-top: 20px;">
                <div style="flex-shrink: 0">
                    <span style="font-size: 18px;">规则：</span>
                </div>
                <!-- 规则显示和按钮 -->
                <div style="width: 90%;display: flex;height: min-content;">
                    <el-input ref="ruleTextarea" type="textarea" autosize resize="none" width="auto"
                        style="font-size: 16px;" v-model="form.rule"></el-input>
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
                    <el-table border :data="form.tableData">
                        <el-table-column label="编号" min-width="70" width="110" align="center">
                            <template #default="scope">
                                <span v-if="scope.row.flag1 == 1" style="font-size: 16px;">{{ scope.row.index
                                    }}</span>
                                <el-input v-else class="blue-border" type="textarea" autosize resize="none"
                                    style="font-size: 16px;" v-model="scope.row.index"></el-input>
                            </template>
                        </el-table-column>
                        <el-table-column label="prompt内容" min-width="520" align="center">
                            <template #default="scope">
                                <el-input v-if="scope.row.flag1 == 1" class="no-border" type="textarea" readonly
                                    autosize resize="none" style="font-size: 16px;"
                                    v-model="scope.row.prompt"></el-input>
                                <el-input v-else ref="myTextarea" class="blue-border" type="textarea" autosize
                                    resize="none" style="font-size: 16px;" v-model="scope.row.prompt"></el-input>
                            </template>
                        </el-table-column>
                        <el-table-column label="Operations" min-width="110" width="110" align="center">
                            <template #default="scope">
                                <div v-if="scope.row.flag1 == 1">
                                    <el-button link type="primary" size="small" @click="edit_line(scope.$index, 1)">
                                        编辑
                                    </el-button>
                                    <el-button link type="primary" size="small" @click="delete_line(scope.$index, 1)">
                                        删除
                                    </el-button>
                                </div>
                                <div v-else-if="scope.row.flag1 == 2">
                                    <el-button link type="primary" size="small"
                                        @click="confirm_linedata(scope.$index, 1)">
                                        确认
                                    </el-button>
                                    <el-button link type="primary" size="small" @click="cancel_line(scope.$index, 1)">
                                        取消
                                    </el-button>
                                </div>
                                <div v-else-if="scope.row.flag1 == 3">
                                    <el-button link type="primary" size="small"
                                        @click="confirm_linedata(scope.$index, 1)">
                                        确认
                                    </el-button>
                                    <el-button link type="primary" size="small"
                                        @click="cancel_add_prompt(scope.$index, 1)">
                                        取消
                                    </el-button>
                                </div>
                            </template>
                        </el-table-column>
                    </el-table>
                    <div style="width:100%;display: flex;justify-content: center;">
                        <el-button type="primary" size="small" plain @click="add_prompt(1)">添加</el-button>
                    </div>
                </div>
            </div>
        </el-card>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="add_card">确认</el-button>
                <el-button type="primary"
                    @click="flag_add = false; form = { tableData: [] }; f_change_tableData = []">取消</el-button>
            </div>
        </template>
    </el-dialog>
    <el-dialog v-model="flag_delete" title="是否删除prompt" width="300" :destroy-on-close=true>
        <template #footer>
            <div class="dialog-footer">
                <el-button type="primary" @click="delete_card">确认</el-button>
                <el-button @click="flag_delete = false">取消</el-button>
            </div>
        </template>
    </el-dialog>

</template>

<script>
import request from '@/api/request';


export default {
    props: ['active_name', 'mess'],
    emits: ['update-active-name', 'update-mess'],
    data() {
        return {
            t_f_1_0_ch: [false, true],
            a_n: this.active_name,
            local_mess: this.mess,
            options_index: [],
            card_id: 0,
            tableData: [
                {
                    index: '001',
                    prompt: '汽车行业正在与人工智能、地图绘制和智能定位领域的主要供应商合作，投入巨资用于辅助驾驶和自动驾驶的开发和部署。各种相关应用可以帮助驾驶员更安全地进行驾驶、代替驾驶员执行特定操作，或者支持驾驶员进行完全自动驾驶。',
                    flag1: 1,
                },
                {
                    index: '002',
                    prompt: '汽车行业正在与人工智能、高性能计算、地图绘制和智能定位领域的主要供应商合作，投入巨资用于辅助驾驶和自动驾驶的开发和部署。各种相关应用可以帮助驾驶员更安全地进行驾驶、代替驾驶员执行特定操作，或者支持驾驶员进行完全自动驾驶。',
                    flag1: 1,
                },
            ],
            change_tableData: [],
            copy_tableData: [],
            rule: 'prompt1 and prompt2',
            rule_temp: '5555555',
            version: 'L001',
            version_temp: '',
            description: '这是描述这是描述这是描述这是描述这是描述这是描述',
            description_temp: '',
            flag1: true,
            flag_version: true,
            flag_description: true,
            flag_add: false,
            flag_delete: false,
            enable_or_not: true,
            currentPage: 1,
            total_data: 0,
            pageSize: 1,
            form: { tableData: [] },
            f_change_tableData: [],
            disease_value: '',
            index_value: '',
            list1: [],
            list2: [],
            currentState: {},
        };
    },
    methods: {
        close_dialog_add(done) {
            this.form = { tableData: [] };
            this.f_change_tableData = [];
            done()
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
                this.get_card();
            }, 100); // 100毫秒等于0.1秒
        },
        // prompt保存
        async edit_card() {
            try {
                const params = {
                    // disease: this.currentState.disease_value,
                    // indicator_number: this.currentState.indicator_number,
                    // indicator_name: this.currentState.indicator_name,
                    // prompt: this.form.prompt,
                    // version: this.form.version,
                    // description: this.form.description,
                    // enable_or_not: 0,
                    // index_prompt_id: this.form.index_prompt_id
                    index_prompt_set_id: this.card_id,
                    version: this.version,
                    description: this.description,
                    rule: this.rule
                };
                const response = await request.post('/index_prompt_set/index_prompt_set_update', params); // 修改为实际的 API 端点和参数
                this.get_card();
            }
            catch (error) {
                console.error('Error fetching data:', error);
            }
        },
        async delete_card() {
            try {
                const params = {
                    index_prompt_set_id: this.card_id,
                };
                const response = await request.get('/index_prompt_set/index_prompt_set_delete', { params }); // 修改为实际的 API 端点和参数
                this.get_card();
                this.flag_delete = false;
            }
            catch (error) {
                console.error('Error fetching data:', error);
            }
        },
        async change_enable() {
            try {
                const params = {
                    page: this.currentPage,
                    indicator_number: this.options_index[this.currentState.index_value].indicator_number,
                    index_prompt_set_id: this.card_id,

                };
                const response = await request.get('/index_prompt_set/index_prompt_set_enable', { params }); // 修改为实际的 API 端点和参数
                this.get_card();
            }
            catch (error) {
                console.error('Error fetching data:', error);
            }
        },
        async get_disease() {
            try {
                const response = await request.get('/hospital_diseases'); // 修改为实际的 API 端点和参数
                const data = response;
                console.log(data);
                this.processDisease(data);
                // this.disease_name = response.disease_name[0];
                // this.disease_index = response.disease_index;

            }
            catch (error) {
                console.error('Error fetching data:', error);
            }
        },
        async get_card() {
            try {
                const params = {
                    page: this.currentPage,
                    size: this.pageSize,
                    disease: this.currentState.disease_value,
                    indicator_number: this.options_index[this.currentState.index_value].indicator_number,
                    indicator_name: this.options_index[this.currentState.index_value].indicator_name,
                };
                const res = await request.get('/index_prompt_set/index_prompt_set_search', { params }); // 修改为实际的 API 端点和参数
                const response = res.total_list[0];
                this.total_data = res.data_count;
                this.card_id = response.index_prompt_set_id;
                this.rule = response.rule;
                this.description = response.description;
                this.enable_or_not = this.t_f_1_0_ch[response.enable_or_not];
                this.version = response.version;
                this.tableData = response.index_prompts;
                this.change_tableData = JSON.parse(JSON.stringify(this.tableData));
                this.tableData.forEach(item => {
                    item.flag1 = 1;  // 添加 "flag" 键，值为 true
                });
                this.disease_value = this.currentState.disease_value;
                setTimeout(() => {
                    this.index_value = this.currentState.index_value;
                }, 100);
                this.index_value = this.currentState.index_value;
                // this.tableData = response.total_list;
                // this.total_data = response.data_count;
            }
            catch (error) {
                console.error('Error fetching data:', error);
            }
        },
        async add_card() {
            try {
                const params = {
                    disease: this.currentState.disease_value,
                    indicator_number: this.options_index[this.currentState.index_value].indicator_number,
                    indicator_name: this.options_index[this.currentState.index_value].indicator_name,
                    version: this.form.version,
                    description: this.form.description,
                    enable_or_not: this.form.enable_or_not ? 1 : 0,
                    rule: this.form.rule,
                };
                const response = await request.post('/index_prompt_set/index_prompt_set_creat', params); // 修改为实际的 API 端点和参数
                this.get_card();
                this.flag_add = false;
                form = { tableData: [] };
                this.f_change_tableData = [];
            }
            catch (error) {
                console.error('Error fetching data:', error);
            }
        },
        edit_line(i, type) {
            // 通过 ref 获取 el-input 组件的实例
            if (type == 0) {
                this.tableData[i].flag1 = 2;
                this.$nextTick(() => {
                    if (this.$refs.myTextarea) {
                        this.$refs.myTextarea.$el.querySelector('textarea').focus();  // 聚焦 textarea
                    }
                });
            }
            else if (type == 1) {
                this.form.tableData[i].flag1 = 2;
                this.$nextTick(() => {
                    if (this.$refs.myTextarea) {
                        this.$refs.myTextarea.$el.querySelector('textarea').focus();  // 聚焦 textarea
                    }
                });
            }
        },
        async delete_line(i, type) {
            if (type == 0) {
                try {
                    const params = {
                        index_prompt_id: this.tableData[i].index_prompt_id,
                    };
                    const res = await request.get('/index_prompt_delete', { params }); // 修改为实际的 API 端点和参数
                    this.get_card();
                }
                catch (error) {
                    console.error('Error fetching data:', error);
                }
            }
            else if (type == 1) {
                this.form.tableData.splice(i, 1);
                this.f_change_tableData.splice(i, 1);
            }
        },
        async confirm_linedata(i, type) {
            if (type == 0) {
                try {
                    const params = {
                        index_prompt_id: this.tableData[i].index_prompt_id,
                        order: this.tableData[i].order,
                        prompt: this.tableData[i].prompt

                    };
                    const response = await request.post('/index_prompt_update', params); // 修改为实际的 API 端点和参数
                    this.get_card();
                }
                catch (error) {
                    console.error('Error fetching data:', error);
                }
            }
            else if (type == 1) {
                this.form.tableData[i].flag1 = 1;
                this.f_change_tableData[i] = JSON.parse(JSON.stringify(this.form.tableData[i]));
            }
        },
        cancel_line(b, type) {
            if (type == 0) {
                this.tableData[b] = JSON.parse(JSON.stringify(this.change_tableData[b]));
                this.tableData[b].flag1 = 1;
            }
            else if (type == 1) {
                this.form.tableData[b] = JSON.parse(JSON.stringify(this.f_change_tableData[b]));
                this.form.tableData[b].flag1 = 1;
            }
        },
        async confirm_add_prompt(i) {
            try {
                const params = {
                    index_prompt_set_id: this.card_id,
                    order: this.tableData[i].order,
                    prompt: this.tableData[i].prompt
                };
                const response = await request.post('/index_prompt_creat', params); // 修改为实际的 API 端点和参数
                this.get_card();
            }
            catch (error) {
                console.error('Error fetching data:', error);
            }
        },
        edit_version() {
            this.flag_version = false;
            this.version_temp = this.version;
            this.$nextTick(() => {
                if (this.$refs.versionTextarea) {
                    this.$refs.versionTextarea.$el.querySelector('textarea').focus();  // 聚焦 textarea
                }
            });
        },
        cancel_version() {
            this.flag_version = true;
            this.version_temp = '';
        },
        edit_description() {
            this.flag_description = false;
            this.description_temp = this.description;
            this.$nextTick(() => {
                if (this.$refs.descriptionTextarea) {
                    this.$refs.descriptionTextarea.$el.querySelector('textarea').focus();  // 聚焦 textarea
                }
            });
        },
        cancel_description() {
            this.flag_description = true;
            this.description_temp = '';
        },
        edit_rule() {
            // 通过 ref 获取 el-input 组件的实例
            this.flag1 = false;
            this.rule_temp = this.rule
            this.$nextTick(() => {
                if (this.$refs.ruleTextarea) {
                    this.$refs.ruleTextarea.$el.querySelector('textarea').focus();  // 聚焦 textarea
                }
            });
        },
        cancel_rule() {
            this.flag1 = true;
            this.rule_temp = '';
        },
        add_prompt(type) {
            if (type == 0) {
                this.tableData.push({ prompt: '', flag1: 3, });
                this.change_tableData.push({});
            }
            else if (type == 1) {
                this.form.tableData.push({ prompt: '', flag1: 3, });
                this.f_change_tableData.push({});
            }
        },
        cancel_add_prompt(i, type) {
            if (type == 0) {
                this.tableData.splice(i, 1);
                this.change_tableData.splice(i, 1);
            }
            else if (type == 1) {
                this.form.tableData.splice(i, 1);
                this.f_change_tableData.splice(i, 1);
            }
        },
        reset_table() {
            this.tableData = JSON.parse(JSON.stringify(this.copy_tableData));
        },
        changeActiveName() {
            this.$emit('update-mess', {
                index_prompt_set_id: this.card_id, disease_value: this.currentState.disease_value,
                indicator_number: this.options_index[this.currentState.index_value].indicator_number, indicator_name: this.options_index[this.currentState.index_value].indicator_name,
                version:this.version,rule:this.rule,description:this.description,tableData:this.tableData,enable_or_not:this.enable_or_not
            });
            this.$emit('update-active-name', '3-61');
        }
    },
    watch: {
        currentPage(newPage) {
            console.log(newPage);
            this.get_card();
        },
        disease_value(neww) {
            this.options_index = {};
            this.index_value = ''
            const searchKey = neww;
            console.log(neww)
            const result = this.list2.find(item => Object.keys(item)[0] === searchKey);
            this.options_index = result ? result[searchKey] : 'No results found';
        },
        // tableData: {
        //     handler(neww) {
        //         const isEqual = neww.length === this.copy_tableData.length &&
        //             neww.every((item, index) => (item.prompt === this.copy_tableData[index].prompt) & (item.index === this.copy_tableData[index].index));

        //         this.flag2 = !isEqual;
        //     },
        //     deep: true
        // }

    },
    mounted() {
        this.get_disease();
        this.copy_tableData = JSON.parse(JSON.stringify(this.tableData));
        this.change_tableData = JSON.parse(JSON.stringify(this.tableData));
    },
};
</script>


<style scoped>
.container {
    display: flex;
    /* max-height: 950px; */
    flex-direction: column;
    background-color: white
}

.custom-table {
    border-radius: 15px;
    /* 增加圆角 */
}

::v-deep .no-border .el-textarea__inner {
    border: none;
    box-shadow: none;
}

::v-deep .blue-border .el-textarea__inner {
    --el-input-border-color: #409eff !important;
}
</style>