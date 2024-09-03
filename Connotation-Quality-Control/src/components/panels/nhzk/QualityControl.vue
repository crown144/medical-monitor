<template>
  <div class="container3">
    <el-card style="height: 100%;width: 100%;">
      <h2>指标总表</h2>
      <div class="top-bar">
        <el-select style="width: 200px;margin-left: 20px;" v-model="hospital" placeholder="选择医院"
          @change="hospitalChange">
          <el-option v-for="item in hospitalList" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
        <el-select style="width: 200px;margin-left: 20px;" v-model="type" placeholder="选择类型">
          <el-option label="单病种" value="单病种" />
          <el-option label="专科" value="专科" />
        </el-select>
        <el-select style="width: 200px;margin-left: 20px;" v-model="disease" placeholder="选择病种">
          <el-option v-for="item in diseaseList" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
        <el-button type="primary" style="margin-left: 70%;" @click="getTableList" class="myButton">确定</el-button>
        <el-button type="primary" style="margin-left: 10px;" @click="tableReset" class="myButton">重置</el-button>
        <!-- <el-button type="primary" style="margin-left: 10px;" @click="exportExcel('IndicatorTable.xlsx', '#tableId')">结果导出</el-button> -->
      </div>
      <el-table id="tableId" height="80%" v-loading="loading" :data="tableData" :summary-method="sumMethod"
        style="margin-top: 20px; border: 0;" class="custom-table" :header-cell-style="tableHeaderColor">
        <el-table-column prop="disease" label="病历编号" width="120" align="center">
          <template #default="scope">
            <span style="font-size: 16px;">{{ scope.row.disease }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="indicator_name" label="收费明细" width="540" align="center">
          <template #default="scope">
            <span style="font-size: 16px;">{{ scope.row.indicator_name }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="emr_id" label="违规类型" width="120" align="center">
          <template #default="scope">
            <span style="font-size: 16px;">{{ scope.row.emr_id }}</span>
          </template>
        </el-table-column>
        <el-table-column label="收费明细原文" width="120" align="center">
          <template #default="scope">
            <el-button link type="primary" @click="handleText(scope.row)">查看</el-button>
          </template>
        </el-table-column>
        <el-table-column prop="predict" label="结果" align="center">
          <template #default="scope">
            <el-input type="textarea" style="font-size: 16px;" v-model="scope.row.predict"></el-input>
          </template>
        </el-table-column>
        <el-table-column prop="yes_or_no" width="100" label="是/否" align="center">
          <template #default="scope">
            <span style="font-size: 16px;" v-if="scope.row.yes_or_no === 1">是</span>
            <span style="font-size: 16px;" v-else>否</span>
          </template>
        </el-table-column>
        <!-- <el-table-column fixed="right" label="审核" width="120" align="center">
            <template #default="scope">
          <el-button link type="primary" @click="handleClick(scope.row)">{{ scope.row.audit ? '已审核' : '审核' }}</el-button>
          </template>
          </el-table-column> -->
      </el-table>
      <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize" :page-sizes="[10, 20, 30, 40]"
        layout="sizes, prev, pager, next" :total="totalPage" @size-change="handleSizeChange"
        @current-change="handleCurrentChange" />
      <el-dialog :visible.sync="dialogImport" v-model="dialogImport" title="导入" v-if="dialogImport" width="40%"
        append-to-body>
        <div style="text-align:center">
          <!-- 此处action需为有效的任意接口——当前为官网范例接口 -->
          <el-upload drag :limit="1" action="http://124.225.82.2:43210/" ref="upload" accept=".json"
            :file-list="fileList" :on-success="onSuccess" :on-remove="onRemove" :on-exceed="handleExceed"
            :on-preview="handlePreview">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
            <div class="el-upload__tip" slot="tip">
              上传json文件，且只能上传 1 个文件
            </div>
          </el-upload>
        </div>
        <span slot="footer" style="margin-top: 10px;">
          <el-button @click="dialogImport = false" size="mini">取 消</el-button>
          <el-button @click="importConfirm" size="mini" type="primary">确 定</el-button>
        </span>
      </el-dialog>
      <el-dialog :visible.sync="dialogPreviewJSON" v-model="dialogPreviewJSON" title="JSON文件预览" v-if="dialogPreviewJSON"
        width="40%" append-to-body>
        <sJson :json="jsonData"></sJson>
      </el-dialog>
      <el-dialog :visible.sync="dialogEdit" v-model="dialogEdit" title="审核" v-if="dialogEdit" width="40%">
        <el-form :model="editFormData" ref="editForm" label-width="80px">
          <el-form-item label="是/否">
            <el-radio-group v-model="editFormData.yes_or_no">
              <el-radio :value="true">是</el-radio>
              <el-radio :value="false">否</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="结果">
            <el-input type="textarea" rows="3" v-model="editFormData.predict"></el-input>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer" style="display: flex; justify-content: center;">
          <el-button @click="dialogEdit = false">取 消</el-button>
          <el-button type="primary" @click="saveEdit">确 定</el-button>
        </span>
      </el-dialog>
      <el-dialog :visible.sync="dialogText" v-if="dialogText" v-model="dialogText" title="收费明细原文">
        <el-input v-model="textValue" type="textarea" rows="3" placeholder="请输入内容"></el-input>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="handleConfirm">确 定</el-button>
        </span>
      </el-dialog>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import sJson from '../sJson.vue';
import request from '@/api/request';

const rate = ref(null);
const modifyResult = ref(true)
const dialogImport = ref(false)
const dialogText = ref(false)
const jsonData = ref('')
const dialogPreviewJSON = ref(false)
const dialogEdit = ref(false)

const type = ref('')
const hospitalList = ref([])
const hospital = ref('')
const diseaseList = ref([])
const disease = ref('')
const hospitalDiseases = ref({})

const tableHeaderColor = {
  background: ' #f5f5f5 !important',
  color: '#333333',
  fontSize: '14px',
  textAlign: 'center',
}
const editFormData = ref({})

//分页
const currentPage = ref(1);
const pageSize = ref(10);
const totalPage = ref(0)

const textValue = ref('')
const fileList = ref([]);
const uploadData = ref([]);
const selectedValue = ref('');
// 修改这个值
const tableData = ref([])
const selectIndex = ref([]);
const stockData = ref({})
const uploadJson = ref([])
const loading = ref(false);

onMounted(() => {
  tableData.value = [
    {
      "disease":110700001 ,
      "indicator_name":"医院为之前做过冠状动脉造影术的心肌梗塞患者行定向冠脉内膜旋切术，手术步骤为靶血管造影、送入旋切导管、充盈球囊旋切病变、撤出器械。医院同时收取“定向冠脉内膜旋切术”“冠状动脉造影术”费用。",
      "emr_id":"重复收费",
      "predict":"根据规定，靶血管造影是定向冠脉内膜旋切术的一个组成部分，而不是额外的操作。因此，“冠状动脉造影术”为重复收费。",
      "yes_or_no":1
      
    }
    ,
    {
      "disease":120100013  ,
      "indicator_name":"医院为患者开展“骨密度测定”，分别测定腰椎、髋部、前臂3个部位，收取3次费用。",
      "emr_id":"超标准收费",
      "predict":"根据标准，骨密度测定计价单位为“次”，不同部位测定均算在一次内。因此，只应收取1次“骨密度测定”收费。",
      "yes_or_no":1
    },
    
    {
      "disease":210102003   ,
      "indicator_name":"医院经鼻饲管为重症患者滴入胃肠营养液，按照“肠内高营养治疗”（单价：22元/次）收取费用。",
      "emr_id":"串换项目",
      "predict":"根据鼻饲管置管项目内涵：含胃肠营养滴入；肠内高营养治疗项目内涵：指经腹部造瘘置管的胃肠营养治疗，含肠营养配置。因此，医院应收取“鼻饲管置管”（单价：12元/次）费用，而非“肠内高营养治疗”。",
      "yes_or_no":1
    },
    {
      "disease":210103035   ,
      "indicator_name":"医院为重症患者开展经纤支镜下肺泡灌洗诊疗术，医院同时收取“经纤支镜下肺泡灌洗诊疗术”和“氯化钠注射液（供冲洗用）”费用",
      "emr_id":"重复收费",
      "predict":"由于经纤支镜下肺泡灌洗诊疗术项目包含生理盐水。因此，“氯化钠注射液（供冲洗用）”为重复收费。",
      "yes_or_no":1
    },
    {
      "disease":230300004   ,
      "indicator_name":"医院对慢性肾功能衰竭患者进行血液透析加滤过治疗，收取“血液透析”费用340元和“血液滤过”费用380元",
      "emr_id":"分解收费",
      "predict":"根据血液净化标准操作规程，血液透析滤过是将病人血液引出体外，并利用血液滤过器进行血液透析加滤过治疗。因此，医院应收取“血液透析滤过”费用480元，而非两项费用。",
      "yes_or_no":1
    
    },
    {
      "disease":230410502   ,
      "indicator_name":"医院眼科将胸部CT作为眼科疾病必查项目。",
      "emr_id":"过度检查",
      "predict":"胸部CT是针对特定科室、特定适应证的检查项目，打包在常规检查里向大多数患者普遍开展并收费，属于过度检查。",
      "yes_or_no":1
    
    },
    
  ]
  getOptionList()
  getTableList()
});

// 上传文件超出文件数量限制/文件格式不符合要求时
const handleExceed = (files, fileList) => {
  ElMessage.warning(`每次只能导入一个json文件！`);
};

// 文件上传成功
const onSuccess = (res, file, fileList) => {
  let reader = new FileReader();
  reader.readAsText(file.raw);
  reader.onload = (e) => {
    let jsonData = JSON.parse(e.target.result);

    // 打印JSON数据
    console.log(jsonData);
    uploadData.value = [];
    uploadData.value = JSON.parse(e.target.result);

    const data = uploadData.value
    const dataArray = Object.keys(data).map(key => ({
      id: key,
      text: data[key]['手术记录']['手术经过'],
      reason: data[key]['reason']
    }));
    uploadJson.value = dataArray
    console.log(uploadJson._rawValue);
  };
};

// 移除文件
const onRemove = (file) => {
  fileList.value = [];
};

// 导入确认
const importConfirm = () => {
  ElMessageBox.confirm("导入后原数据会被覆盖，确定导入吗?", "温馨提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  }).then(() => {
    // 使用目标数据变量接收上传后的文件数据
    stockData.value = JSON.stringify(uploadData.value);

    const data = stockData._rawValue
    console.log(data)
    dialogImport.value = false;

    ElMessage({
      type: "success",
      message: "导入成功!",
    });
  });
};

const handlePreview = (file) => {
  console.log(file)
  let reader = new FileReader();
  reader.readAsText(file.raw);
  reader.onload = (e) => {
    jsonData.value = JSON.parse(e.target.result);
    dialogPreviewJSON.value = true;
  };
};
const resetResult = () => {
  modifyResult.value = true;
};
const updateResult = (val) => {
  console.log(val)
};
const sumMethod = (val) => {
  const { columns, row } = val;
  const sums = [];
  columns.forEach((item, index) => {
    if (index === 0) {
      sums[index] = '达标率';
      return;
    }
    else if (index === 2) {
      sums[index] = "6/7"
      return;
    }
  });
  return sums
}

const getOptionList = () => {
  request.get('/hospital_diseases/').then(res => {
    console.log(res)
    hospitalDiseases.value = res
    Object.keys(res).forEach(key => {
      hospitalList.value.push({
        'label': key,
        'value': key
      })
    }
    )
  })
}

const hospitalChange = () => {
  diseaseList.value = []
  const list = hospitalDiseases.value[hospital.value]
  console.log(Object.keys(list))
  Object.keys(list).forEach(item => {
    diseaseList.value.push({
      'label': item,
      'value': item
    })
  })
  console.log(diseaseList.value)
}

const handleOk = () => {
  console.log(selectedValue.value)
  console.log(selectIndex._rawValue[0])
}

const handleClick = (row) => {
  console.log(row)
  const rowData = JSON.parse(JSON.stringify(row));
  dialogEdit.value = true
  editFormData.value.predict = rowData.predict
  editFormData.value.emr_id = rowData.emr_id
  editFormData.value.yes_or_no = rowData.yes_or_no === '是' ? true : false
  editFormData.value.emr_result_id = rowData.emr_result_id
  editFormData.value.hospital_name = rowData.hospital_name
  editFormData.value.disease = rowData.disease
  editFormData.value.disease_type = rowData.disease_type
  editFormData.value.indicator_name = rowData.indicator_name
  editFormData.value.indicator_number = rowData.indicator_number
  editFormData.value.predict = rowData.predict
  editFormData.value.content = rowData.content
  editFormData.value.audit = rowData.audit

  console.log(editFormData.value)
  console.log('点击编辑按钮，当前行数据：', rowData);
}

const handleText = (row) => {
  console.log(row)
  dialogText.value = true
  const rowData = JSON.parse(JSON.stringify(row));
  textValue.value = rowData.content
  console.log('点击编辑按钮，当前行数据：', rowData);
}

const saveEdit = () => {
  const rowData = JSON.parse(JSON.stringify(editFormData.value));
  console.log(rowData)
  dialogEdit.value = false
  const req = {
    emr_result_id: rowData.emr_result_id,
    disease: rowData.disease,
    disease_type: rowData.disease_type,
    hospital_name: rowData.hospital_name,
    indicator_name: rowData.indicator_name,
    indicator_number: rowData.indicator_number,
    emr_id: rowData.emr_id,
    content: rowData.content,
    predict: editFormData.value.predict,
    yes_or_no: editFormData.value.yes_or_no == false ? 0 : 1,
    audit: 1
  }
  request.put('/update_emr_result', req).then(res => {
    console.log(res)
    getTableList()
  })
}

const tableReset = () => {
  hospital.value = ''
  disease.value = ''
  type.value = ''
  getTableList()
}

const getTableList = () => {
  const req = {
    'page': currentPage.value,
    'size': pageSize.value,
    'disease': disease.value,
    'hospital_name': hospital.value,
    'disease_type': type.value
  };

  console.log(req);
  const queryString = Object.keys(req).map(key => `${encodeURIComponent(key)}=${encodeURIComponent(req[key])}`).join('&');
  const url = '/latest_records?' + queryString;
  request.get(url).then(res => {
    console.log(res);
    totalPage.value = res.data_count;
    tableData.value = res.total_list;
    console.log(tableData.value);
  }).catch(error => {
    console.error('Error fetching data:', error);
  });
}

const handleSizeChange = (val) => {
  console.log(`每页 ${val} 条`);
  pageSize.value = val;
  currentPage.value = 1
  getTableList()
};

const handleCurrentChange = (val) => {
  console.log(`当前页: ${val}`);
  currentPage.value = val;
  getTableList()
};

</script>
<style scoped>
.container3 {
  flex-direction: column;
  width: 100%;
  height: 90%;
  font-family: 'PingFang';
  display: flex;
  justify-content: center;
}

.top-bar {
  display: flex;
  align-items: center;
}

.example-pagination-block {
  margin: 20px;
  float: right
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
  max-width: 20%
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
</style>
