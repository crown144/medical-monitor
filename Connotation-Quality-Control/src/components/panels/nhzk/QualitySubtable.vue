<template>
    <div class="container">
      <div class="top-bar">
        <el-cascader
          v-model="selectedOptions"
          placeholder="请选择指标"
          :options="options"
          :props="props"
          collapse-tags
          clearable
          style="width: 200px;"
        />
        <el-select v-model="selectedValue" placeholder="请选择模型" style="margin-left: 20px; width: 120px;">
          <el-option label="chatglm" value="1" />
          <el-option label="pulse" value="2" />
          <el-option label="qwen" value="3" />
        </el-select>
        <el-button size="primary" type="primary" style="margin-left: 10px;" @click="importData">导入数据</el-button>
        <el-button type="primary" style="margin-left: 10px;" @click="handleReset">确定</el-button>
        <el-button type="primary" style="margin-left: 10px;" @click="exportExcel('interestTable.xlsx', '#tableId')">结果导出</el-button>
      </div>
      <el-descriptions style="width: 200px;margin-top: 20px;" title="" :column="1" border>
        <el-descriptions-item label="达标率(达标数/总数)">6/7</el-descriptions-item>
      </el-descriptions>
      <el-table id="tableId" stripe :data="tableData" :summary-method="sumMethod" style="margin-top: 20px;">
        <el-table-column prop="record" label="电子病历">
          <template v-slot="{ row }">
            <el-link type="primary" :underline="false" @click="openDetail">
              {{ row.record }}
            </el-link>
          </template>
        </el-table-column>
        <el-table-column prop="index" label="指标"></el-table-column>
        <el-table-column prop="num" width="100" label="是/否"></el-table-column>
        <el-table-column prop="output" width="400" label="结果" align="center">
         <template #default="scope">
            <el-input type="textarea" v-model="scope.row.output"></el-input>
            <!-- <span v-if="scope.row.result?.length <= 20">
              {{ scope.row.result }}
            </span>
            <span v-else-if="!scope.row.result?.length"> --- </span>
            <span v-else>
              <el-popover effect="dark" placement="top-start" :width="400" trigger="hover" :content="scope.row.result">
                <template #reference> {{ scope.row.result?.slice(0, 20) }}... </template>
              </el-popover>
            </span> -->
          </template>
        </el-table-column>
        <el-table-column prop="result" label="结果"></el-table-column>
        <el-table-column prop="correct" label="修正">
          <template #default="{ row }">
            <!-- <span> {{row.result}}</span> -->
            <el-input v-show="!modifyResult" v-model="row.result" style="width:80px;margin-right: 10px;"></el-input>
            <el-button v-if="modifyResult" type="primary" v-model="row.result" @click="modifyResult = false">
              <el-icon><Edit/></el-icon>
            </el-button>
            <el-button v-else-if="!modifyResult" type="primary" @click="updateResult(row)">
              <el-icon><Check/></el-icon>
            </el-button>
            <el-button v-if="!modifyResult" type="primary" @click="resetResult">
              <el-icon><Close/></el-icon>
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="example-pagination-block">
        <el-pagination layout="prev, pager, next"
        :total="1000" />
      </div>

      <el-dialog
        :visible.sync="dialogImport"
        v-model="dialogImport"
        title="导入"
        v-if="dialogImport"
        width="40%"
        append-to-body
      >
        <div style="text-align:center">
          <!-- 此处action需为有效的任意接口——当前为官网范例接口 -->
          <el-upload
            drag
            :limit="1"
            action="http://127.0.0.1:8000/"
            ref="upload"
            accept=".json"
            :file-list="fileList"
            :on-success="onSuccess"
            :on-remove="onRemove"
            :on-exceed="handleExceed"
            :on-preview="handlePreview"
          >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
            <div class="el-upload__tip" slot="tip">
              上传json文件，且只能上传 1 个文件
            </div>
          </el-upload>
        </div>
        <span slot="footer" style="margin-top: 10px;">
          <el-button @click="dialogImport = false" size="mini">取 消</el-button>
          <el-button @click="importConfirm" size="mini" type="primary"
            >确 定</el-button
          >
        </span>
      </el-dialog>

      <el-dialog
        :visible.sync="dialogPreviewJSON"
        v-model="dialogPreviewJSON"
        title="JSON文件预览"
        v-if="dialogPreviewJSON"
        width="40%"
        append-to-body
      >
        <sJson :json="jsonData"></sJson>
      </el-dialog>

    </div>
    <showPdf v-model="openPdf" :uuid="uuid"></showPdf>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { ElMessage, ElMessageBox } from 'element-plus';
  import {Edit,Check,Close} from "@element-plus/icons";
  import { onMounted, reactive } from 'vue'
  import showPdf from "./showPdf.vue"
  import sJson from './sJson.vue'
  import { exportExcel } from '../../../utils/excelutil.js';

  const uuid = ref(null);
  const openPdf = ref(false);
  const modifyResult = ref(true)
  const dialogImport = ref(false)
  const jsonData = ref('')
  const dialogPreviewJSON = ref(false)

  const openDetail=()=> {
  openPdf.value = true;
  };
  const isViewPdf20 = ref(false);
  const props = ref({ multiple: true });
  const options = ref([
    {
      value: 'pjs',
      label: '帕金森病',
      children: [
        { value: '4', label: 'PD2022_SH_PD_004' },
        { value: '8', label: 'PD2022_SH_PD_008' }
      ]
    },
    {
      value: 'jdm',
      label: '颈动脉支架',
      children: [
        { value: '6', label: '2022_SH_CAS_006' },
        { value: '8', label: '2022_SH_CAS_008' }
      ]
    }
  ]);
  const selectedOptions = ref([]);
  const fileList = ref([]);
  const uploadData = ref([]);
  const selectedValue = ref('');
  const tableData = ref([
    { record: '23092405a', index: '手术全切除及近全切除程度比例', num: '是', result:'全切除', 
    output:'手术名称：脑脊液鼻漏修补术（探查术）\n\n手术经过：...见6点钟方向有一个0.4mm 大小蛛网膜缺口，以人工脑膜及胶水修补缺口内、部分留在鞍内，生物胶水妥善固定...\n\n判断依据：手术记录中提到的是对蛛网膜的一个小缺口进行修补，并没有提及对肿瘤的切除情况。因此，这不属于全切除、近全切除、部分切除或次全切除的肿瘤手术类型。手术的主要目的是修复脑脊液鼻漏，而非切除肿瘤。' },
    { record: '21568091a', index: '手术全切除及近全切除程度比例', num: '是', result:'全切除', output:'手术名称：脑脊液鼻漏修补术（探查术）\n\n手术经过：...见6点钟方向有一个0.4mm 大小蛛网膜缺口，以人工脑膜及胶水修补缺口内、部分留在鞍内，生物胶水妥善固定...\n\n判断依据：手术记录中提到的是对蛛网膜的一个小缺口进行修补，并没有提及对肿瘤的切除情况。因此，这不属于全切除、近全切除、部分切除或次全切除的肿瘤手术类型。手术的主要目的是修复脑脊液鼻漏，而非切除肿瘤。' },
    { record: '22892176a', index: '手术全切除及近全切除程度比例', num: '是', result:'全切除', output:'手术名称：脑脊液鼻漏修补术（探查术）\n\n手术经过：...见6点钟方向有一个0.4mm 大小蛛网膜缺口，以人工脑膜及胶水修补缺口内、部分留在鞍内，生物胶水妥善固定...\n\n判断依据：手术记录中提到的是对蛛网膜的一个小缺口进行修补，并没有提及对肿瘤的切除情况。因此，这不属于全切除、近全切除、部分切除或次全切除的肿瘤手术类型。手术的主要目的是修复脑脊液鼻漏，而非切除肿瘤。' },
    { record: '21494936a', index: '手术全切除及近全切除程度比例', num: '是', result:'全切除', output:'手术名称：脑脊液鼻漏修补术（探查术）\n\n手术经过：...见6点钟方向有一个0.4mm 大小蛛网膜缺口，以人工脑膜及胶水修补缺口内、部分留在鞍内，生物胶水妥善固定...\n\n判断依据：手术记录中提到的是对蛛网膜的一个小缺口进行修补，并没有提及对肿瘤的切除情况。因此，这不属于全切除、近全切除、部分切除或次全切除的肿瘤手术类型。手术的主要目的是修复脑脊液鼻漏，而非切除肿瘤。' },
    { record: '21472986a', index: '手术全切除及近全切除程度比例', num: '是', result:'全切除', output:'手术名称：脑脊液鼻漏修补术（探查术）\n\n手术经过：...见6点钟方向有一个0.4mm 大小蛛网膜缺口，以人工脑膜及胶水修补缺口内、部分留在鞍内，生物胶水妥善固定...\n\n判断依据：手术记录中提到的是对蛛网膜的一个小缺口进行修补，并没有提及对肿瘤的切除情况。因此，这不属于全切除、近全切除、部分切除或次全切除的肿瘤手术类型。手术的主要目的是修复脑脊液鼻漏，而非切除肿瘤。' },
    { record: '21379345a', index: '手术全切除及近全切除程度比例', num: '是', result:'全切除', output:'手术名称：脑脊液鼻漏修补术（探查术）\n\n手术经过：...见6点钟方向有一个0.4mm 大小蛛网膜缺口，以人工脑膜及胶水修补缺口内、部分留在鞍内，生物胶水妥善固定...\n\n判断依据：手术记录中提到的是对蛛网膜的一个小缺口进行修补，并没有提及对肿瘤的切除情况。因此，这不属于全切除、近全切除、部分切除或次全切除的肿瘤手术类型。手术的主要目的是修复脑脊液鼻漏，而非切除肿瘤。' },
    { record: '24034629a', index: '手术全切除及近全切除程度比例', num: '是', result:'近全切除', output:'手术名称：脑脊液鼻漏修补术（探查术）\n\n手术经过：...见6点钟方向有一个0.4mm 大小蛛网膜缺口，以人工脑膜及胶水修补缺口内、部分留在鞍内，生物胶水妥善固定...\n\n判断依据：手术记录中提到的是对蛛网膜的一个小缺口进行修补，并没有提及对肿瘤的切除情况。因此，这不属于全切除、近全切除、部分切除或次全切除的肿瘤手术类型。手术的主要目的是修复脑脊液鼻漏，而非切除肿瘤。' },
  ]);

  const importData = () => {
    dialogImport.value = true;
  };

    // 上传文件超出文件数量限制/文件格式不符合要求时
  const handleExceed = (files, fileList) => {
    ElMessage.warning(`每次只能导入一个json文件！`);
  };

    // 文件上传成功
  const  onSuccess = (res, file, fileList) => {
      let reader = new FileReader();
      reader.readAsText(file.raw);
      reader.onload = (e) => {
        uploadData.value = [];
        uploadData.value = JSON.parse(e.target.result);
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
        stockData.value = uploadData.value;

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
        else if(index===2){
          sums[index] = "6/7"
          return;
        }
      });
      return sums
  };

  </script>
  <style scoped>
  
  .container {
    padding: 20px;
  }
  
  .top-bar {
    display: flex;
    align-items: center;
  }

  .example-pagination-block {
    margin: 20px;
    float: right
  }

  .record:hover{
    cursor: pointer;
    background-color: aqua;
  }

  ::v-deep .el-table {
    display: flex;
    flex-direction: column;
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

  .el-tooltip__popper{
  max-width:20%
}
#tableId .el-table__cell {
  text-align: center;
}
  </style>
  