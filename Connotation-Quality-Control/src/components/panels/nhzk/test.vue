<template>
<div style="width: 100%;position: absolute;background-color: white;display: flex;align-items: center;overflow-y: scroll;min-height: 950px;flex-direction: column">
    <el-card style="width: 80%;" shadow="hover">
        <template #header>
            <div  style="display: flex;justify-content: space-between;">
                <span style="font-size: 18px;display: flex;align-items: center;">Card name</span>
                <div>
                    <el-button type="success"  plain @click="">测试</el-button>
                    <el-button type="danger"  plain @click="">删除</el-button>
                </div>
            </div>
        </template>
        <div style="display: flex;justify-content: space-between">
            <span style="font-size: 18px;">版本号：{{ flag2 }}</span>
        </div>
        <div style="display: flex;width: 100%;margin-top: 20px;">
            <div style="flex-shrink: 0">
                <span style="font-size: 18px;">规则：</span>
            </div>
            <div style="width: 80%;display: flex;height: min-content;">
                <!-- <el-input :class="no-border" type="textarea" readonly autosize resize="none" style="font-size: 16px;" v-model="rule"></el-input> -->
                <div v-if="flag1" style="max-width: 100%;display: flex;">
                    <span  style="font-size: 15px;line-height: 1.5;">{{ rule }}</span>
                </div>
                <el-input v-else ref="ruleTextarea" type="textarea"  autosize resize="none" width="auto" style="font-size: 16px;" v-model="rule_temp"></el-input>
            
                <div style="display: flex;height: auto;align-items: center;">
                    <div v-if="flag1" style="width: 110px;display: flex;align-items: center;margin-left: 15px;">
                        <el-button link type="primary" size="small" @click="edit">
                            编辑
                        </el-button>
                    </div>
                    <div v-else style="width: 110px;display: flex;align-items: center;margin-left: 15px">
                        <el-button link type="primary" size="small" @click="">
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
                <el-switch v-model="value3" inline-prompt active-text="是" inactive-text="否"/>
            </div>
        </div>
        <!-- 边界线 -->
        <div style="width: 100%;border-top:solid 1px;margin-top: 20px;margin-bottom: 20px; ">
        </div>
        <!-- prompt -->
        <div>
            <div style="display: flex;justify-content: space-between">
                <span style="font-size: 18px;">prompt：</span>
                <div v-if="flag2">
                    <el-button type="primary"  plain @click="">保存</el-button>
                    <el-button type="default"  plain @click="reset_table()">重置</el-button>
                </div>
            </div>
            <!-- 表格 -->
            <div style="margin-top: 20px;">
                <el-table border :data="tableData" >
                    <el-table-column  label="编号" min-width="70" width="110" align="center">
                        <template #default="scope">
                            <span v-if="scope.row.flag1==1" style="font-size: 16px;">{{ scope.row.index }}</span>
                            <el-input v-else class="blue-border" type="textarea"  autosize resize="none" style="font-size: 16px;" v-model="scope.row.index"></el-input>
                        </template>
                    </el-table-column>
                    <el-table-column  label="prompt内容" min-width="520" align="center">
                        <template #default="scope">
                            <el-input v-if="scope.row.flag1==1" class="no-border" type="textarea" readonly autosize resize="none" style="font-size: 16px;" v-model="scope.row.prompt"></el-input>
                            <el-input v-else ref="myTextarea" class="blue-border" type="textarea"  autosize resize="none" style="font-size: 16px;" v-model="scope.row.prompt"></el-input>
                        </template>
                    </el-table-column>
                    <el-table-column  label="Operations" min-width="110" width="110" align="center">
                            <template #default="scope">
                                <div v-if="scope.row.flag1==1">
                                    <el-button link type="primary" size="small" @click="edit_line(scope.$index)">
                                        编辑
                                    </el-button>
                                    <el-button link type="primary" size="small" @click="delete_line(scope.$index)">
                                        删除
                                    </el-button>
                                </div>
                                <div v-else-if="scope.row.flag1==2">
                                    <el-button link type="primary" size="small" @click="confirm_linedata(scope.$index)">
                                        确认
                                    </el-button>
                                    <el-button link type="primary" size="small" @click="cancel_line(scope.$index)">
                                        取消
                                    </el-button>
                                </div>
                                <div v-else-if="scope.row.flag1==3">
                                    <el-button link type="primary" size="small" @click="confirm_linedata(scope.$index)">
                                        确认
                                    </el-button>
                                    <el-button link type="primary" size="small" @click="cancel_add_prompt(scope.$index)">
                                        取消
                                    </el-button>
                                </div>
                            </template>
                    </el-table-column>
                </el-table>
                <div style="width:100%;display: flex;justify-content: center;">
                    <el-button type="primary" size="small" plain @click="add_prompt">添加</el-button>
                </div>
            </div>
        </div>


    

    </el-card>
    <div style="flex-grow: 1;"></div>
</div>
</template>

<script>
import request from '@/api/request';
export default {
    data() {
        return {
            tableData:[
                {
                index:'001',
                prompt:'汽车行业正在与人工智能、地图绘制和智能定位领域的主要供应商合作，投入巨资用于辅助驾驶和自动驾驶的开发和部署。各种相关应用可以帮助驾驶员更安全地进行驾驶、代替驾驶员执行特定操作，或者支持驾驶员进行完全自动驾驶。',
                flag1:1,
                },
                {
                index:'002',
                prompt:'汽车行业正在与人工智能、高性能计算、地图绘制和智能定位领域的主要供应商合作，投入巨资用于辅助驾驶和自动驾驶的开发和部署。各种相关应用可以帮助驾驶员更安全地进行驾驶、代替驾驶员执行特定操作，或者支持驾驶员进行完全自动驾驶。',
                flag1:1,
                },

            ],
            change_tableData:[],
            copy_tableData:[],
            rule:'prompt1 and prompt2',
            flag1:true,
            flag2:false,
            rule_temp:'5555555',
            value3: true,
        }
    },
    methods: {
    edit_line(i) {
      // 通过 ref 获取 el-input 组件的实例
      this.tableData[i].flag1=2;
      this.$nextTick(() => {
        if (this.$refs.myTextarea) {
          this.$refs.myTextarea.$el.querySelector('textarea').focus();  // 聚焦 textarea
        }
      });
    },
    delete_line(i){
        this.tableData.splice(i,1);
        this.change_tableData.splice(i,1);
    },
    confirm_linedata(i){
        this.tableData[i].flag1=1;
        this.change_tableData[i]=JSON.parse(JSON.stringify(this.tableData[i]));
    },
    cancel_line(b){
        this.tableData[b].prompt=this.change_tableData[b].prompt;
        this.tableData[b].flag1=1;
    },
    edit() {
      // 通过 ref 获取 el-input 组件的实例
      this.flag1=false;
      this.rule_temp = this.rule
      this.$nextTick(() => {
        if (this.$refs.ruleTextarea) {
          this.$refs.ruleTextarea.$el.querySelector('textarea').focus();  // 聚焦 textarea
        }
      });
    },
    cancel_rule(){
        this.flag1 = true;
        this.rule_temp='';
    },
    add_prompt(){
        this.tableData.push({prompt:'',flag1:3,});
        this.change_tableData.push({});
    },
    cancel_add_prompt(i){
        this.tableData.splice(i,1);
        this.change_tableData.splice(i,1);
    },
    reset_table(){
        this.tableData = JSON.parse(JSON.stringify(this.copy_tableData));
    },
    },
    mounted(){
        this.copy_tableData = JSON.parse(JSON.stringify(this.tableData));
        this.change_tableData = JSON.parse(JSON.stringify(this.tableData));
    },
    watch: {
        tableData: {
            handler(neww) {
                const isEqual = neww.length === this.copy_tableData.length && 
                    neww.every((item, index) => (item.prompt === this.copy_tableData[index].prompt) &  (item.index === this.copy_tableData[index].index));

                this.flag2 = !isEqual;
                },
            deep: true
        }
    }       
}
</script>


<style scoped>
::v-deep .no-border .el-textarea__inner {
  border: none;
  box-shadow: none;
}
::v-deep .blue-border .el-textarea__inner {
    --el-input-border-color:#409eff !important;
}
</style>