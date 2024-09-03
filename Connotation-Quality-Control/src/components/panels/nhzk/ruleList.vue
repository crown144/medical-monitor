<template>
    <div class="container">
        <el-card>
            <h2 class="text-center">电子病历规则总表</h2>
            <div class="top-bar border">
                <el-form :inline="true" :model="formInline">
                    <el-form-item label="审查内容">
                        <el-select style="width: 200px;margin-left: 20px;" v-model="formInline.hospital"
                            placeholder="选择审查内容">
                            <el-option label="单病种" value="单病种" />
                            <el-option label="专科" value="专科" />
                        </el-select>
                    </el-form-item>
                    <el-form-item label="审查内容详情">
                        <el-input v-model="formInline.disease" placeholder="请输入审查内容详情"></el-input>
                    </el-form-item>
                    <el-form-item label="审查内容来源">
                        <el-select style="width: 200px;margin-left: 20px;" v-model="formInline.type"
                            placeholder="选择审查内容来源">
                            <el-option label="单病种" value="单病种" />
                            <el-option label="专科" value="专科" />
                        </el-select>
                    </el-form-item>
                    
                    <el-form-item>
                        <div class="form-actions">
                            <el-button type="primary" size="mini" @click="getTableList" class="myButton">确定</el-button>
                            <el-button type="primary" size="mini" @click="tableReset" class="myButton">重置</el-button>
                        </div>
                    </el-form-item>
                </el-form>
            </div>
            <div class="submit-container">
                <el-button type="primary" size="mini" class="myButton" @click="handleOpneAddDialog">新增</el-button>
            </div>
            <el-table id="tableId" height="80%" v-loading="loading" :data="tableData"
                style="margin-top: 20px; border: 0;" class="custom-table" :header-cell-style="tableHeaderColor">
                <el-table-column type="index" :index="indexMethod" label="编号" width="80" />
                <el-table-column prop="aa" label="审查名称" align="center"></el-table-column>
                <el-table-column prop="bb" label="审查内容详情" align="center"></el-table-column>
                <el-table-column prop="cc" label="审查内容来源" align="center"></el-table-column>
                <el-table-column label="审查方案" align="center">
                    <template #default="scope">
                        <el-button link type="primary" @click="handleDetail(scope.row)">查看详情</el-button>
                        <el-button link type="primary" @click="handleModify(scope.row)">修改</el-button>
                        <el-button link type="primary" @click="handleDelete(scope.$index)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize"
                :page-sizes="[10, 20, 30, 40]" layout="sizes, prev, pager, next" :total="totalPage"
                @size-change="handleSizeChange" @current-change="handleCurrentChange" />

            <el-dialog :visible.sync="dialog" v-model="dialog" center title="审查规则详情" width="40%" append-to-body>
                <el-form :model="formContent" label-width="auto" style="max-width: 600px">
                    <el-form-item label="审查模块">
                        <el-input v-model="formContent.aa" />
                    </el-form-item>
                    <el-form-item label="相关字段">
                        <el-input v-model="formContent.bb" />
                    </el-form-item>
                    <el-form-item label="任务描述">
                        <el-input v-model="formContent.cc" />
                    </el-form-item>
                    <el-form-item label="关键字列表">
                        <el-input v-model="formContent.dd" />
                    </el-form-item>
                    <el-form-item label="执行步骤">
                        <el-input v-model="formContent.ee" />
                    </el-form-item>
                    <el-form-item label="指令/规则">
                        <el-input type="textarea" v-model="formContent.ff" />
                    </el-form-item>
                </el-form>
                <span slot="footer" style="margin-top: 10px;">
                    <el-button @click="dialog = false" size="mini">取 消</el-button>
                    <el-button @click="confirm" size="mini" type="primary">确 定</el-button>
                </span>
            </el-dialog>
        </el-card>

        <!-- 审查规则详情弹窗 -->
<el-dialog
    v-model="dialogVisible"
    :title="dialogTitle"
    width="30%"
    center
    @close="handleClose"
  >
  <el-form :model="form" label-width="auto" style="max-width: 600px">
    <el-form-item label="审查模块">
      <el-input v-model="form.censor" />
    </el-form-item>
    <el-form-item label="相关字段">
      <el-input v-model="form.field" />
    </el-form-item>
    <el-form-item label="任务描述">
      <el-input v-model="form.description" />
    </el-form-item>
    <el-form-item label="关键字列表">
      <el-input v-model="form.keyLisy" />
    </el-form-item>
    <el-form-item label="执行步骤">
      <el-input v-model="form.step" />
    </el-form-item>
    <el-form-item label="指令/规则">
        <el-upload
        v-model:file-list="fileList"
        class="upload-demo"
        action="#"
        :limit="3"
        accept=".xlsx,.xls"
        @on-change="hanldeUploadChange"
    >
    <el-button type="primary">文件上传</el-button>
    <template #tip>
      <div class="el-upload__tip" style="color: red;">
        <!-- 请上传jpg/png文件且文件大小不超过5KB! -->
         请上传文件！
      </div>
    </template>
  </el-upload>
    </el-form-item>
  </el-form>
    <template #footer center>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="dialogVisible = false">
          提交
        </el-button>
        <el-button type="primary" @click="dialogVisible = false">
          测试
        </el-button>
      </div>
    </template>
  </el-dialog>
    </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import request from '@/api/request';
const dialog = ref(false);
const hospitalList = ref([]);
const hospitalDiseases = ref({});
const jsonData =
    [
        {
            "aa": "判断病人是否需要进行手术",
            "bb": "判断病人是否需要进行手术",
            "cc": "条件性审查-任务前置条件"
        },
        {
            "aa": "判断病人是否需要进行有创操作",
            "bb": "判断病人是否需要进行有创操作",
            "cc": "条件性审查-任务前置条件"
        },
        {
            "aa": "判断病人是否需要申请会诊",
            "bb": "判断病人是否需要申请会诊",
            "cc": "条件性审查-任务前置条件"
        },
        {
            "aa": "判断病人是否需要输血",
            "bb": "判断病人是否需要输血",
            "cc": "条件性审查-任务前置条件"
        },
        {
            "aa": "判断病人是否为疑难病例\n",
            "bb": "判断病人是否为疑难病例\n",
            "cc": "条件性审查-任务前置条件"
        },
        {
            "aa": "判断病人是否需要专科检查",
            "bb": "判断病人是否需要专科检查",
            "cc": "条件性审查-任务前置条件"
        },
        {
            "aa": "判断病人是否为危重病例",
            "bb": "判断病人是否为危重病例",
            "cc": "条件性审查-任务前置条件"
        },
        {
            "aa": "判断病人是否死亡",
            "bb": "判断病人是否死亡",
            "cc": "条件性审查-任务前置条件"
        },
        {
            "aa": "判断病人住院时长是否超过一个月",
            "bb": "判断病人住院时长是否超过一个月",
            "cc": "条件性审查-任务前置条件"
        },
        {
            "aa": "有无入院记录",
            "bb": "电子病历结构中是否存在入院记录",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "入院记录未在24小时内完成",
            "bb": "入院记录书写时间和患者入院时间相差不超过24小时",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "无主诉  ",
            "bb": "电子病历结构中是否存在主诉",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "主诉描述是否规范",
            "bb": "主诉是否清晰明了，能够反映患者的病症及其持续时间",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "现病史与主诉不符  ",
            "bb": "现病史内容应与主诉内容相关",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "现病史是否有缺项",
            "bb": "现病史内容是否记录发病情况；主要症状特点及其发展变化情况；伴随症状；发病后诊疗经过及结果；睡眠和饮食等一般情况的变化",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "有无既往史",
            "bb": "电子病历结构中是否存在既往史",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "既往史是否有缺项",
            "bb": "既往史内容是否记录'一般健康情况'、'传染病史'、'预防接种史'、'手术史'、'外伤史'、'输血史'、'食物或药物过敏史'以及'疾病史'",
            "cc": "《病历书写要求》"
        },
        {
            "aa": "有无家族史",
            "bb": "电子病历结构中是否存在家族史",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "家族史是否有缺项",
            "bb": "家族史内容是否记录'家人健康情况','遗传病史'和'传染病史'",
            "cc": "《病历书写要求》"
        },
        {
            "aa": "有无个人史",
            "bb": "电子病历结构中是否存在个人史",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "个人史是否有缺项",
            "bb": "个人史内容是否记录'出生地','长期居留地','生活习惯',,'冶游史','药物史','吸烟史'和'饮酒史'",
            "cc": "《病历书写要求》"
        },
        {
            "aa": "有无婚育史",
            "bb": "电子病历结构中是否存在婚育史",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "婚育史是否有缺项",
            "bb": "婚育史内容是否记录'婚姻情况'、'家人健康状况'和'生育情况'",
            "cc": "《病历书写要求》"
        },
        {
            "aa": "有无体格检查                                 ",
            "bb": "电子病历结构中是否存在体格检查",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "体格检查是否存在缺项",
            "bb": "体格检查内容是否记录体温,脉搏,呼吸,血压，一般情况，皮肤粘膜，头，颈，胸，腹，直肠肛门，外生殖器，脊柱和四肢，神经系统等内容",
            "cc": "《病历书写要求》"
        },
        {
            "aa": "体格检查遗漏标志性的阳性体征和阴性体征                 ",
            "bb": "？",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "需要专科检查的病历缺专科情况",
            "bb": "需要专科检查的病人的电子病历结构中是否存在专科情况",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "无辅助检查记录",
            "bb": "电子病历结构中是否记录辅助检查",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "辅助检查记录不完整",
            "bb": "辅助检查应分类按检查时间顺序记录检查结果，如系在其他医疗机构所作检查，应当写明该机构名称及检查号",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "缺初步诊断                                 ",
            "bb": "电子病历结构中是否存在初步诊断",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "初步诊断不规范、不全面（主次分明，规范，全面）",
            "bb": "？",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "主诉与初步诊断第一诊断是否匹配",
            "bb": "主诉是否能够导出初步诊断的第一诊断",
            "cc": "专家提出"
        },
        {
            "aa": "现病史与初步诊断第一诊断是否匹配",
            "bb": "现病史是否能够导出初步诊断的第一诊断",
            "cc": "专家提出"
        },
        {
            "aa": "首次病程未在患者入院后8小时内完成                                                                 ",
            "bb": "首次病程录的记录时间和入院时间的差值小于8小时",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "首次病程记录中无病例特点、初步诊断、诊断依据、鉴别诊断和诊疗计划之一者     ",
            "bb": "首次病程录的结构中是否存在病例特点、初步诊断、诊断依据、鉴别诊断和诊疗计划",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "病情变化或检查结果异常时无记录及分析、判断、处理及结果  ",
            "bb": "对患者病情变化和检查结果的异常情况，医师应该针对性地进行分析，判断，给出处理",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "对病情稳定的患者病程录未按规定时间记录",
            "bb": "对病情稳定的患者，至少三天进行一次查房",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "病程录中未反映上级医生查房意见，主任（副）一周一次，主治一周二次",
            "bb": "主治医师查房记录至少一周两次；主任（副）医师查房至少一周一次",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "患者入院48小时内无主治医师、一周内无主任（副）首次查房记录",
            "bb": "患者首次主治医师的查房记录时间与入院时间相差小于48小时；患者首次主任医师的查房记录时间与入院时间相差小于一周",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "首次主治及主任（副）查房记录未记录上级医师补充的病史和体征",
            "bb": "首次主治及主任（副）查房记录中应该体现上级医师补充的病史和体征",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "首次主治查房无诊断依据与鉴别诊断",
            "bb": "首次主治查房记录的结构中是否存在诊断依据和鉴别诊断",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "首次主任（副）查房记录无分析讨论",
            "bb": "首次主任医师查房记录的结构中是否存在分析讨论",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "首次病程录、首次主治及主任（副）查房记录内容雷同",
            "bb": "首次病程录、首次主治及主任（副）查房记录内容是否雷同",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "有无疑难病例讨论",
            "bb": "该病人为疑难病例时，电子病历结构中是否存在疑难病例讨论记录",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "疑难病例讨论有缺项",
            "bb": "疑难病例讨论记录内容包括讨论日期、主持人、参加人员姓名及专业技术职务、讨论目的、具体讨论意见及主持人小结意见等。",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "疑难病例主任查房讨论意见无“两点”",
            "bb": "疑难病例主任查房讨论意见是否记录1.症状、体征、实验室检查结果在鉴别诊断或治疗中的意义2.明确诊断或治疗的途径、措施和方法",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "有无阶段小结( 每月一次，最长不超过31天)",
            "bb": "病人住院超过一个月后，电子病历结构中是否记录阶段小结内容",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "阶段小结有缺项",
            "bb": "阶段小结的内容包括入院日期、小结日期，患者姓名、性别、年龄、主诉、入院情况、入院诊断、诊疗经过、目前情况、目前诊断、诊疗计划等。",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "抢救次数、抢救医嘱、抢救记录未一致",
            "bb": "/",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "抢救记录不完整",
            "bb": "抢救记录内容包括病情变化情况、抢救时间及措施、参加抢救的医务人员姓名及专业技术职称等。记录抢救时间应当具体到分钟。",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "放弃抢救未写病程记录",
            "bb": "抢救记录中若患者家属放弃相关抢救需要在病程录/出院记录中体现",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "死亡病历缺死亡前抢救记录或未在6小时内补记抢救记录",
            "bb": "死亡病人应在电子病历结构中存在抢救记录，且抢救记录书写时间与病人死亡时间差距小于6小时",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "缺有创性操作记录（如胸腔穿刺、腹腔穿刺、骨髓穿刺、腰椎穿刺、内镜检查治疗、心导管检查、起搏器安装、各种造影检查等）",
            "bb": "做过有创操作的病人的电子病历结构中应该存在有创性操作记录",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "有创诊疗操作记录有缺项",
            "bb": "有创诊疗操作记录内容包括操作名称、操作时间、操作步骤、结果及患者一般情况，记录过程是否顺利、有无不良反应，术后注意事项及是否向患者说明。",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "无会诊单（会诊请求记录）",
            "bb": "患者在住院期间需要其他科室或者其他医疗机构协助诊疗时，电子病历结构中需要有会诊请求记录",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "会诊单（会诊请求记录）有部分项目未填写",
            "bb": "申请会诊记录应当简要载明患者病情及诊疗情况、申请会诊的理由和目的",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "急会诊未精确记录会诊时间到分钟",
            "bb": "会诊类型为急会诊时，会诊时间应该精确到分钟",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "有无会诊记录",
            "bb": "患者在住院期间需要其他科室或者其他医疗机构协助诊疗时，电子病历结构中需要有会诊记录",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "病程记录未反映会诊意见及执行情况",
            "bb": "会诊记录中的会诊意见需要在病程中体现针对性的执行情况",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "无术前小结（所有手术均需术前小结）",
            "bb": "做过手术的病人的电子病历结构中应该存在术前小结",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "术前小结有缺项",
            "bb": "术前小结内容包括简要病情、术前诊断、手术指征、拟施手术名称和方式、拟施麻醉方式、注意事项，并记录手术者术前查看患者相关情况等。",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "术前诊断和手术方案是否匹配",
            "bb": "术前诊断和手术方案是否匹配",
            "cc": "专家提出"
        },
        {
            "aa": "中等（III级）以上择期手术无术前讨论记录",
            "bb": "术前讨论记录是指因患者病情较重或手术难度较大，手术前在上级医师主持下，对拟实施手术方式和术中可能出现的问题及应对措施所作的讨论。",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "术前讨论记录有缺项",
            "bb": "术前讨论内容包括术前准备情况、手术指征、手术方案、可能出现的意外及防范措施、参加讨论者的姓名及专业技术职务、具体讨论意见及主持人小结意见、讨论日期等。",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "无手术记录或未在术后24小时内完成",
            "bb": "做过手术的病人的电子病历结构中应该存在手术记录，且手术记录时间与手术时间间隔小于24小时",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "手术记录无书写时间或其他缺项",
            "bb": "手术记录内容包括一般项目(患者姓名、性别、科别、病房、床位号、住院病历号或病案号)、手术日期、术前诊断、术中诊断、手术名称、手术者及助手姓名、麻醉方法、手术经过、术中出现的情况及处理等",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "手术经过和手术名称是否匹配",
            "bb": "手术经过和手术名称是否匹配",
            "cc": "专家提出"
        },
        {
            "aa": "无术后首次病程录",
            "bb": "做过手术的病人的电子病历结构中应该存在术后首次病程记录",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "术后三天无连续病程记录",
            "bb": "术后三天不包括手术日",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "术后三天至少有一天病程录可体现上级医师或术者查房内容",
            "bb": "术后三天至少有一天病程录可体现上级医师或术者查房内容",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "危重病例无副主任以上职称医师查房记录",
            "bb": "危重病例的电子病例结构中应具有危重病例主任（副）医师查房记录",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "危重病例主任（副）查房记录未反应“两点”",
            "bb": "第1天主任（副）查房要求反映出当前主要矛盾；解决主要矛盾的途径、措施、方法。如以后病情无特殊变化，后二次主任（副）查房可无需反映以上“两点”",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "病程录中未体现抗生素合理使用的相关内容",
            "bb": "病程录中未体现抗生素合理使用的相关内容",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "输血患者未记录输血指征、输血品种、输血量及输血过程有无反应",
            "bb": "输血患者须记录输血指征、输血品种（如全血、红细胞悬液、白细胞、血小板、冷沉淀等）、输血量及输血过程有无反应",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "缺死亡讨论记录或未在一周内完成",
            "bb": "死亡病人应在电子病历结构中存在死亡记录，且死亡讨论记录书写时间与病人死亡时间差距小于一周",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "死亡讨论记录有缺项",
            "bb": "死亡病例讨论记录内容包括讨论日期、主持人及参加人员姓名、专业技术职务、具体讨论意见及主持人小结意见",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "缺出院（死亡）记录或未按时完成出院（死亡）记录",
            "bb": "电子病历结构中是否存在出院记录或死亡记录",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        },
        {
            "aa": "出院（死亡）记录缺项",
            "bb": "出院记录内容主要包括入院日期、出院日期、入院情况、入院诊断、诊疗经过、出院诊断、出院情况、出院医嘱、医师签名等。（应当在患者出院后24小时内完成。）死亡记录内容包括入院日期、死亡时间、入院情况、入院诊断、诊疗经过（重点记录病情演变、抢救经过）、死亡原因、死亡诊断等。记录死亡时间应当具体到分钟。",
            "cc": "《上海地区病历质量考核评价标准考核表》"
        }
    ]
// 新增弹框开关
const dialogVisible = ref(false)
// 表单参数
const form = reactive({
    censor:'',
    field:'',
    description:'',
    keyLisy:'',
    step:''
})
// 弹框标题
const dialogTitle = ref('新增审查规则');
const tableHeaderColor = {
    background: ' #f5f5f5 !important',
    color: '#333333',
    fontSize: '14px',
    textAlign: 'center',
};
//分页
const currentPage = ref(1);
const pageSize = ref(10);
const totalPage = ref(0);

const tableData = ref([]);
const loading = ref(false);

const formInline = reactive({
    hospital: '',
    disease: '',
    type: '',
});

onMounted(() => {
    getOptionList();
    getTableList();
});
// 关闭弹框
const handleClose = () => {
    dialogVisible.value = false;
}
// 点击新增按钮触发
const handleOpneAddDialog = () => {
    dialogVisible.value = true;
}
// 文件上传
const hanldeUploadChange = (file,fileList) => {

    
}

const getOptionList = () => {
    request.get('/hospital_diseases/').then((res) => {
        console.log(res);
        hospitalDiseases.value = res;
        Object.keys(res).forEach((key) => {
            hospitalList.value.push({
                label: key,
                value: key,
            });
        });
    });
};

const indexMethod = (index) => {
    return index + 1
}



const handleAdd = (row) => {
    console.log('新增按钮被点击了', row);
    formContent.value = {};
    formContent.aa = row.aa;
    formContent.bb = row.bb;
    formContent.cc = row.cc;
    formContent.dd = row.dd;
    formContent.ee = row.ee;
    formContent.ff = row.ff;
    dialog.value = true;
};

const handleDetail = (row) => {
    formContent.value = {};
    formContent.aa = row.aa;
    formContent.bb = row.bb;
    formContent.cc = row.cc;
    formContent.dd = row.dd;
    formContent.ee = row.ee;
    formContent.ff = row.ff;
    dialog.value = true;
};

const handleModify = (row) => {
    formContent.value = {};
    formContent.aa = row.aa;
    formContent.bb = row.bb;
    formContent.cc = row.cc;
    formContent.dd = row.dd;
    formContent.ee = row.ee;
    formContent.ff = row.ff;
    dialog.value = true;
};

const handleDelete = (index) => {
    ElMessageBox.confirm('此操作将永久删除该审查规则, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
    })
        .then(() => {
            request
                .delete('', { ...tableData.value[index] })
                .then((res) => {
                    ElMessage({
                        type: 'success',
                        message: '删除成功!',
                    });
                    getTableList();
                })
                .catch(() => {
                    ElMessage({
                        type: 'error',
                        message: '删除失败!',
                    });
                });
        })
        .catch(() => {
            ElMessage({
                type: 'info',
                message: '已取消删除',
            });
        });
};

const tableReset = () => {
    formInline.hospital = '';
    formInline.disease = '';
    formInline.type = '';
    getTableList();
};

const getTableList = () => {
    const req = {
        page: currentPage.value,
        size: pageSize.value,
        disease: formInline.disease.value,
        hospital_name: formInline.hospital.value,
        disease_type: formInline.type.value,
    };

    const queryString = Object.keys(req)
        .map(
            (key) =>
                `${encodeURIComponent(key)}=${encodeURIComponent(req[key])}`
        )
        .join('&');
    const url = '/latest_records?' + queryString;
    request
        .get(url)
        .then((res) => {
            console.log(res);
            totalPage.value = res.data_count;
            tableData.value = res.total_list;
            console.log(tableData.value);
        })
        .catch((error) => {
            console.error('Error fetching data:', error);
        })
        .finally(() => {
            tableData.value = jsonData;
            totalPage.value = 100;
            loading.value = false;
        });
};

const generateRandomChinese = (length) => {
    let result = '';
    for (let i = 0; i < length; i++) {
        const unicodeNum = Math.floor(Math.random() * 20902) + 19968;
        result += String.fromCharCode(unicodeNum);
    }
    return result;
}

const formContent = reactive({
    aa: '',
    bb: '',
    cc: '',
    dd: '',
    ee: '',
    ff: '',
});

const confirm = () => {
    request
        .post('', { ...formContent.value })
        .then((res) => { })
        .finally(() => {
            dialog.value = false;
        });
};

const handleSizeChange = (val) => {
    console.log(`每页 ${val} 条`);
    pageSize.value = val;
    currentPage.value = 1;
    getTableList();
};

const handleCurrentChange = (val) => {
    console.log(`当前页: ${val}`);
    currentPage.value = val;
    getTableList();
};
</script>
<style scoped>
.container {
    flex-direction: column;
    width: 100%;
    height: 90%;
    font-family: 'PingFang';
    display: flex;
    justify-content: center;
}

.text-center {
    text-align: center;
}

.top-bar {
    display: flex;
    align-items: center;
}

.example-pagination-block {
    margin: 20px;
    float: right;
}

.record:hover {
    cursor: pointer;
    background-color: aqua;
}

::v-deep .el-table {
    display: flex;
    flex-direction: column;
    margin-left: 20px;
}

::v-deep .el-table__body-wrapper {
    order: 1;
}

.el-table__fixed-body-wrapper {
    top: 96px !important;
}

.el-table__fixed-footer-wrapper {
    z-index: 0;
    top: 48px;
}

#tableId .el-table__cell {
    text-align: center;
}

.el-tooltip__popper {
    max-width: 20%;
}

#tableId .el-table__cell {
    text-align: center;
}

.el-pagination {
    margin-top: 40px;
    float: right;
}

.myButton {
    border-radius: 20px;
    width: 120px;
}

.top-bar {
    display: flex;
    justify-content: space-between; /* 确保表单和按钮在一行中 */
}

.form-actions {
    display: flex;
    align-items: center;
}

.submit-container {
    margin-left: auto; /* 自动将按钮推到右边 */
}

.custom-table {
    border-radius: 15px;
    /* 增加圆角 */
}

:deep(#tableId .el-table .el-table__row:nth-child(odd)) {
    background-color: #ffffff !important;
    /* 白色 */
}

:deep(#tableId.el-table .el-table__row:nth-child(even)) {
    background-color: #f5f5f5 !important;
    /* 淡灰色 */
}

.border {
    width: 70%;
    margin: auto;
    display: flex;
    justify-content: center;
    padding: 20px 20px 0;
    border-radius: 12px;
    border: 1px solid #dcdfe6;
}

:deep(.el-table__cell .cell) {
    font-size: 16px;
}
</style>