<template>
  <div>
      <!-- 内容区域 -->

      <div id="content">
          <h2 style="text-align: center; margin-top: revert;">电子病历标准性检测</h2>
          <!-- 步骤指示器 -->
          <div class="ui segment" style="height: 900px;">
              <el-steps style="width: 70%; margin: 10px auto" :active="stepIndex" align-center
                  finish-status="success">
                  <el-step title="确定检测文档" style="" />
                  <el-step title="选择检测内容" />
                  <el-step title="查看检测结果" />
                  <el-button v-if="stepIndex === 3" @click="reback" type="primary">返回</el-button>
              </el-steps>


              <div class="show1" v-if="!showCardList" style="width: 70%; margin: 40px auto">
                  <div class="d-flex align-center justify-center" style="margin: 20px 0" @submit.prevent="submitForm">
                      <el-button class="download" @click.prevent="downloadTemplatesFile" type="primary"
                          v-show="!tableData.length > 0">下载模版文件</el-button>
                      <div class="border-container">
                          <div class="search-wrap d-flex align-center">
                              <el-form :model="formInline">
                                  <el-form-item label="医院名称">
                                      <el-select v-model="formInline.hospitalName" placeholder="请选择医院">
                                          <el-option label="新华医院" value="shanghai"></el-option>
                                          <el-option label="复旦医院" value="beijing"></el-option>
                                      </el-select>
                                  </el-form-item>
                                  <el-form-item label="文件上传时间">
                                      <el-date-picker v-model="formInline.uploadTime" type="date"
                                          placeholder="请选择时间" />
                                  </el-form-item>
                                  <el-form-item label="文件名">
                                      <el-select v-model="formInline.fileName" placeholder="请选择文件名">
                                          <el-option label="外科" value="shanghai"></el-option>
                                          <el-option label="内科" value="beijing"></el-option>
                                      </el-select>
                                  </el-form-item>
                              </el-form>
                          </div>
                          <div class="ui action input flex-shrink-0">
                              <input id="fileInput" type="file" ref="fileInput" @change="getExcelData" accept=".xlsx"
                                  required />
                          </div>
                          <el-button @click="uploadFile" type="primary">提交</el-button>
                      </div>
                  </div>
                  <!-- 步骤内容 -->
                  <div v-show="tableData.length > 0">
                      <el-table :data="tableData" border class="custom-table">
                          <el-table-column prop="bzname" label="规则类型" weight="100"></el-table-column>
                          <el-table-column prop="tid" label="病人ID" weight="100"></el-table-column>
                          <el-table-column label="操作" width="200">
                              <template #default="scope">
                                  <el-button type="primary" size="small"
                                      @click.prevent="selected(scope.row)">选中该病人</el-button>
                              </template>
                          </el-table-column>
                      </el-table>
                      <el-pagination style="margin-top: 15px" small background @size-change="handleSizeChange"
                          @current-change="handleCurrentChange" :current-page="currentPage"
                          :page-sizes="[10, 20, 30, 40]" :page-size="pageSize" :total="total"></el-pagination>
                  </div>
                  <br />
              </div>
              <div class="border" v-else>
                  <div>
                      <div class="title-wrap border">
                          <div style="width: 50%">
                              <div class="border-container select-step2">
                                  <div class="ui action input flex-shrink-0" style="width: 100px">选中审查病人ID</div>
                                  <div class="search-wrap d-flex align-center flex-1">
                                      <el-form :model="formInline">
                                          <el-form-item label="病种名" style="width: 300px">
                                              <el-select v-model="formInline.name" filterable clearable
                                                  placeholder="请选择病种名">
                                                  <el-option v-for="item in tableData" :key="item.tid"
                                                      :label="item.bzname" :value="item.bzname">{{ item.bzname
                                                      }}</el-option>
                                              </el-select>
                                          </el-form-item>
                                          <el-form-item label="病人ID" style="width: 300px">
                                              <el-select v-model="formInline.id" filterable clearable
                                                  placeholder="请选择病人ID">
                                                  <el-option v-for="item in tableData" :key="item.tid"
                                                      :label="item.tid" :value="item.tid">
                                                      {{
                  item.tid }}
                                                  </el-option>
                                              </el-select>
                                          </el-form-item>
                                      </el-form>
                                  </div>
                                  <el-button @click="filterParentById" type="primary">提交</el-button>

                              </div>
                          </div>
                          <div v-if="cardList?.length" class="success-rate border">
                              检测正确率：{{ accuracy }}
                          </div>
                      </div>
                      <div class="res-box">
                          <div class="res-box-left" style=" left: 190px; top: 165px">
                              <el-row class="tac" style="
                                  width: 160px;
                                  position: absolute;
                                  left: 20px;
                                  height: 600px;
                                  overflow-y: auto;
                                  min-height: 600px;
                                  ">
                                  <el-col style="width: 100%">
                                      <el-menu active-text-color="skyblue" background-color="#F1F2F7"
                                          default-active="1" class="el-menu-vertical-demo" @open="handleOpen"
                                          @close="handleClose">
                                          <el-sub-menu :index="x + 1" v-for="(Fvalue, x) in Object.keys(menuData)"
                                              :key="x" style="overflow: hidden">
                                              <template #title>
                                                  <span>{{ Fvalue }}</span>
                                              </template>
                                              <el-menu-item @click="showExcelData(Fvalue, c)"
                                                  :index="String(x + 1) + '-' + String(key + 1)" style="width: 100%"
                                                  v-for="(c, key) in Object.keys(menuData[Fvalue])" :key="key">
                                                  {{ c
                                                  }}
                                              </el-menu-item>
                                          </el-sub-menu>
                                      </el-menu>
                                  </el-col>
                              </el-row>
                              <el-table height="600" style="width: 750px;margin-left: 162px;" :data="tableData3"
                                  border class="custom-table">
                                  <el-table-column prop="wddmc" label="字段名称" width="150" />
                                  <el-table-column prop="wddnr" label="内容" width="600"></el-table-column>
                              </el-table>
                              <el-pagination style="margin-top: 15px" small background
                                  @size-change="handleSizeChange3" @current-change="handleCurrentChange3"
                                  :current-page="currentPage3" :page-sizes="[10, 20, 30, 40]" :page-size="pageSize3"
                                  :total="total3"></el-pagination>
                          </div>
                          <div class="card-box">
                              <div class="border-container select-step2" style="margin-bottom: 20px; width: 900px;">
                                  <div class="ui action input flex-shrink-0" style="width: 200px">请选择要审查的文书</div>
                                  <div class="search-wrap d-flex align-center flex-1">
                                      <el-select v-model="formInline.wdmxlbsm" placeholder="所有文书">
                                          <el-option label="所有文书" value="所有文书"></el-option>
                                          <el-option v-for="(Fvalue, x) in Object.keys(menuData)" :key="x"
                                              :label="Fvalue" :value="Fvalue"></el-option>
                                      </el-select>
                                  </div>
                                  <el-button @click="searchBook" type="primary">提交</el-button>
                              </div>
                              <div class="card-list">
                                  <el-card style="
                                  flex: 1;
                                  margin: 0 0 30px 0;
                                  background-color: rgb(241, 242, 247);
                                  " v-for="(item, index) in cardList" :key="index">
                                      <div class="text item">
                                          <li style="text-align: left; margin: 10px; line-height: 30px"
                                              v-for="key in Object.keys(item)" :key="key" :class="{
                  redc:
                      key === '审查结论' &&
                      (item[key] === '存在问题' ||
                          item[key] === '格式上存在问题' ||
                          item[key] === '内容上存在问题'),
                  bluec: key === '审查理由',
              }">
                                              <span style="font-weight: 800" class="title">{{ key }}:</span>
                                              <span class="cxt">{{ item[key] }}</span>
                                          </li>
                                      </div>
                                  </el-card>
                              </div>
                          </div>
                      </div>
                  </div>
              </div>
          </div>

          <!-- 其他模态框等内容 -->
      </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, nextTick } from 'vue';
import * as XLSX from 'xlsx';
import axios from 'axios';
// 引入 JavaScript 文件
import { ElLoading } from 'element-plus';
//引入数据
import Axios from 'axios';

import { ElMessage } from 'element-plus';
// 引入 JavaScript 文件
import '../../../../public/js/jquery-3.6.4.min.js';
import '../../../../public/js/jsQR.js';
import '../../../../public/js/semantic.min.js';
import '../../../../public/js/jszip.min.js';
import '../../../../public/js/docx-preview.js';

// 引入 CSS 文件
import '../../../../public/css/semantic.min.css';

const showCardList = ref(false);
const cardList = ref([]);
const index = ref(0);
const sideCardList = ref([]);

const showTid = ref(false);
const tid = ref('');
const bzname = ref('');
const jsonData1 = ref([]);
const accuracy = ref(0);
const searchBook = async () => {
  const loading = ElLoading.service({
      lock: true,
      text: '正在检测，请稍后。',
      background: 'rgba(0, 0, 0, 0.7)',
  });
  const doc_name = formInline.wdmxlbsm;
  // 请求文书的数据
  const response = await axios.get(
      `http://127.0.0.1:5000/check_doc/${doc_name}`
  );
  loading.close();
  cardList.value = response.data[0].data;
  accuracy.value = response.data[0].accuracy;
};
const stepIndex = ref(1);
// 表单数据
const formInline = reactive({
  id: '',
  name: '',
  hospitalName: '',
  uploadTime: '',
  fileName: '',
  wdmxlbsm: '',
});

const selected = (row) => {
  formInline.id = row.tid;
  formInline.name = row.bzname;
  uploadFile();
};

function uniqueByProperty(arr, prop) {
  const map = new Map();
  arr.forEach((item) => {
      map.set(item[prop], item);
  });
  return [...map.values()];
}

const excelData2 = ref([]);
// 获取excel数据
const getExcelData = (event) => {
  const file = event.target.files[0];

  if (file && file.name.endsWith('.xlsx')) {
      // 读取 .xlsx 文件内容
      const reader = new FileReader();

      reader.onload = function (event) {
          const data = new Uint8Array(event.target.result);
          const workbook = XLSX.read(data, { type: 'array' });
          const sheetName = workbook.SheetNames[0];
          const worksheet = workbook.Sheets[sheetName];
          const jsonData = XLSX.utils.sheet_to_json(worksheet);
          jsonData1.value = uniqueByProperty(jsonData, 'tid');

          const headers = [];
          for (let key in worksheet) {
              if (key[0] === '!') continue;
              if (key[1] === '1') {
                  headers.push(worksheet[key].v);
              } else {
                  break;
              }
          }
          excelData2.value = [];
          for (let key in jsonData1.value) {
              const obj = {};
              Object.keys(jsonData1.value[key]).forEach((item, index) => {
                  obj[headers[index]] = jsonData1.value[key][item];
              });
              excelData2.value.push(obj);
          }
          excelData2.value = uniqueByProperty(excelData2.value, 'tid');
          getData();
          showTid.value = true;
          stepIndex.value = 2;
      };
      reader.readAsArrayBuffer(file); // 替换成你的Excel文件
  } else {
      // 提示选择有效的 .xlsx 文件
      ElMessage.warning('Please select a valid .xlsx file.');
  }
};
const fileInput = ref(null);
const reback = () => {
  stepIndex.value = 0;
  index.value = 0;
  showCardList.value = false;
  tableData.value = [];
  formInline.id = "";
  formInline.name = "";
  showTid.value = false;
};

const showTitle = ref(false);

// 上传文件以及后续数据处理
const filterParentById = async () => {
  const pid = formInline.id;
  const response = await axios.get(
      `http://127.0.0.1:5000/change_patient/${pid}`
  );
  if (response.status === 200) {
      stepIndex.value = 3;
      showCardList.value = true;
      jsonData1.value = [];
      let myJsonClassify = response.data[0].data_Classify;
      getJsonData1(myJsonClassify);

      getData3();
  } else {
      loading.close();
      ElMessage.error('检测失败: ' + response.data.error);

      // 处理上传失败后的逻辑
  }
  console.log(response, '===============');
};

// 上传文件以及后续数据处理
const uploadFile = async () => {
  cardList.value = [];
  const file = fileInput?.value?.files[0];
  const formData = new FormData();
  formData.append('file', file || '');
  formData.append('id', formInline.id);
  formData.append('name', formInline.name);
  if (formInline.id === '') {
      ElMessage.warning('请输入要检测的病人ID！');
      return;
  }

  const isStringInArray = excelData2.value.some(
      (item) => item.tid === formInline.id
  );

  if (!isStringInArray) {
      ElMessage.warning('请输入正确的病人ID！');
      return false; // 结束函数
  }
  const loading = ElLoading.service({
      lock: true,
      text: '正在检测，请稍后。',
      background: 'rgba(0, 0, 0, 0.7)',
  });

  setTimeout(() => {
      loading.close();
      showCardList.value = true;
      stepIndex.value = 2;
      sideCardList.value = [
          {
              "审查模块": "该病历是否包含入院记录",
              "审查内容": "检查上传病历是否包含入院记录",
              "审查结论": "该病历包含入院记录"
          },
          {
              "审查模块": "该病历是否包含主诉",
              "审查内容": "检查上传病历是否包含主诉",
              "审查结论": "格式上完整，书写正确",
              "审查理由": "该病历包含主诉",
              "修正意见": "无"
          },
          {
              "审查模块": "入院记录---主诉",
              "审查内容": "'主诉'应包含'病症'和'持续时间'内容信息",
              "审查原文": "泡沫尿4年。",
              "审查结论": "格式上完整，书写正确",
              "审查理由": "模块结构完整，无遗漏",
              "修正意见": "无"
          }];
  }, 1000);

  const response = await axios.post(
      'http://127.0.0.1:5000/upload_doc_new',
      formData,
      {
          headers: {
              'Content-Type': 'multipart/form-data',
          },
      }
  );

  if (response.status === 200) {
      index.value = 1;
      stepIndex.value = 3;
      loading.close();
      showCardList.value = true;
      jsonData1.value = [];
      let myJsonClassify = response.data[0].data_Classify;
      getJsonData1(myJsonClassify);

      tid.value = formInline.id;
      getData3();
      if (response.data[0].data.length === 0) {
          ElMessage.warning('检测文档没有错误！');
          showTitle.value = true;
          sideCardList.value = [];
      } else {
          ElMessage.success('检测成功');
          showTitle.value = false;
          sideCardList.value = response.data[0].data;
          fileInput.value.value = '';
          bzname.value = formInline.name;
      }
  } else {
      loading.close();
      ElMessage.error('检测失败: ' + response.data.error);

      // 处理上传失败后的逻辑
  }
};

const tableData = ref([]);
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);

const getData = async () => {
  const totalValue = excelData2.value.length;
  total.value = totalValue;
  console.log(currentPage.value);
  const start = (currentPage.value - 1) * pageSize.value;
  const end = Math.min(currentPage.value * pageSize.value, totalValue);
  const data = [];
  for (let i = start; i < end; i++) {
      data.push(excelData2.value[i]);
  }
  tableData.value = data;
};

const handleSizeChange = (page) => {
  console.log(page);
  pageSize.value = page;
  getData();
};

const handleCurrentChange = (current) => {
  currentPage.value = current;
  getData();
};

// 下载模版文件
const downloadTemplatesFile = async () => {
  try {
      const response = await axios.get(
          `http://127.0.0.1:5000/download_templates/`,
          {
              responseType: 'blob',
          }
      );
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', '模板文件.xlsx');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link); // 下载后移除链接
      window.URL.revokeObjectURL(url); // 释放内存
  } catch (error) {
      console.error(error); // 打印错误详细信息
      ElMessage.error('下载模版文件失败！');
  }
};

// 文件检测成功后的后端数据返回以及逻辑处理
const tableData3 = ref([]);
const currentPage3 = ref(1);
const pageSize3 = ref(10);
const total3 = ref(0);

const getData3 = async () => {
  const totalValue = tableShowData.value.length;
  total3.value = totalValue;
  const start = (currentPage3.value - 1) * pageSize3.value;
  const end = Math.min(currentPage3.value * pageSize3.value, totalValue);
  const data = [];
  for (let i = start; i < end; i++) {
      data.push(tableShowData.value[i]);
  }

  const processedData = data.flatMap((item) => {
      if (Array.isArray(item.wddnr)) {
          return item.wddnr.map((wddnrItem) => ({
              ...item,
              wddnr: wddnrItem,
          }));
      } else {
          return [item];
      }
  });

  // console.log("process data:",processedData)
  // 将处理后的数据赋值给 tableData3
  tableData3.value = processedData;
  nextTick(() => {
      console.log("tableData3:", tableData3.value);
  });
};

const handleSizeChange3 = (page) => {
  pageSize3.value = page;
  getData3();
};

const handleCurrentChange3 = (current) => {
  currentPage3.value = current;
  getData3();
};

onMounted(() => {
  index.value = 0;
  showTid.value = false;
  showTitle.value = false;
});

const menuData = ref([]);
/*若是menuData.value[key1][key2][key3]是一个列表，则需要将其拆分，wddcm仍旧为key3，wddnr为列表中的值*/
const getJsonData1 = (JsaonData) => {
  menuData.value = JsaonData;
  for (let key1 in menuData.value) {
      for (let key2 in menuData.value[key1]) {
          for (let key3 in menuData.value[key1][key2]) {
              tableShowData.value.push({
                  wddmc: key3,
                  wddnr: menuData.value[key1][key2][key3],
              });
          }
      }
  }
  getData3();
};
const getJsonData = async () => {
  const res = await Axios.get(
      'http://localhost:5173/src/assets/output_file.json'
  );
  if (res.status === 200) {
      console.log('主诉：');
      //console.log(res)
      menuData.value = res.data;
      //console.log(menuData.value);
      for (let key1 in menuData.value) {
          for (let key2 in menuData.value[key1]) {
              for (let key3 in menuData.value[key1][key2]) {
                  tableShowData.value.push({
                      wddmc: key3,
                      wddnr: menuData.value[key1][key2][key3],
                  });
              }
          }
      }
      getData3();
  } else {
      alert('暂无数据');
  }
};

const tableShowData = ref([]);

const showFisrtExcelData = () => { };

const showExcelData = (f, value) => {
  const fieldValue = menuData.value[f][value];
  tableShowData.value = [];
  // 输出结果
  if (fieldValue) {
      for (let key in fieldValue) {
          tableShowData.value.push({
              wdmxlbsm: value,
              wddmc: key,
              wddnr: fieldValue[key],
          });
      }
      getData3();
  } else {
      console.log(`未找到 ${value} 字段的值。`);
  }
};
onMounted(() => {
  getJsonData();
  showFisrtExcelData();
});
</script>





<style scoped>
body {
  margin: 0;
  padding: 0;
  font-family: 'Arial', sans-serif;
  list-style: none;
}

#content {
  flex-direction: column;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  background-color: #ffffff;
}

#header {
  /*background-color: #2185d0;*/
  color: #fff;
  text-align: left;
  display: flex;
  justify-content: left;
  align-content: left;
  /*padding: 20px;
            height: 15%;*/
}

.ui.menu .item {
  padding: 15px 20px;
  font-size: 16px;
}

.ui.segment {
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.ui.steps {
  margin-bottom: 20px;
  margin-left: 600px;
}

.menu-side-1 {
  color: white;
}

#loading {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(50, 50, 50, 0.8);
  /* 半透明白色背景 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  /* 确保加载界面在最上层 */
}

/* Excel 样式 */

.res-box {
  margin-top: 15px;
  width: 100%;
  display: flex;
}

.res-box-left {
  flex: 1;
  height: 600px;
  /* margin-left: 40px; */
  /* overflow: auto; */
}

.card-list {
  flex-wrap: wrap;
  /* min-width: 600px; */
  width: 900px;
  list-style: none;
  justify-content: space-between;
  align-content: flex-start;
}

.card-box {
  flex: 1;
  height: 600px;

  /*margin-right: 10px; */
  overflow-y: scroll;
  overflow-x: hidden;
}

.card-box .top div {
  height: 40px;
  width: 200px;
  font-size: 20px;
  font-family: 800;
  color: red;
}

:deep(.el-pagination__rightwrapper) {
  justify-content: flex-start !important;
}

:deep(.el-table__header th) {
  background-color: #f5f5f5 !important;
  color: black;
}

.custom-table {
  border-radius: 8px;
  /* 增加圆角 */
}

::v-deep(.el-table .el-table__row:nth-child(odd)) {
  background-color: #ffffff !important;
  /* 白色 */
}

::v-deep(.el-table .el-table__row:nth-child(even)) {
  background-color: #f5f5f5 !important;
  /* 淡灰色 */
}

:deep(.el-step .el-step__line) {
  border-top: 3px dashed #ccd1de;
  height: 0;
  background-color: transparent;
}

:deep(.el-step__title) {
  font-size: 18px;
}

:deep(.el-step__icon.is-text) {
  width: 40px;
  height: 40px;
  font-size: 18px;
  border: 5px solid;
}

:dep(.el-step__icon-inner) {
  font-size: 18px;
  font-weight: 700 !important;
}

:deep(.el-step .el-step__line-inner) {
  display: none;
}

.bluec {
  color: blue;
}

.redc {
  color: red;
}

.search-wrap {
  display: inline-block;
}

.title-wrap {
  display: flex;
  align-items: center;
}

.success-rate {
  line-height: 1;
  flex: 1;
  font-size: 36px;
  font-weight: 600;
}

.download {
  margin: 0 10px;
}

.d-flex {
  display: flex;
}

.align-center {
  align-items: center;
}

.justify-center {
  justify-content: center;
}

.flex-shrink-0 {
  flex-shrink: 0;
}

::v-deep .el-form {
  display: flex;

  .el-form-item {
      margin: 0 10px;
      flex-shrink: 0;
  }

  .el-input,
  .el-select {
      width: 100px;
  }
}

.border-container {
  display: flex;
  align-items: center;
  padding: 10px;
  border-radius: 12px;
  border: 1px solid #dcdfe6;

  input[type='file'] {
      border: none;
  }
}

.border {
  padding: 10px;
  border-radius: 12px;
  border: 1px solid #dcdfe6;
}

.show1 {
  height: 50vh;
  display: flex;
  align-content: center;
  justify-content: center;
  flex-direction: column;
}

.select-step2 {
  width: 910px;

  .el-select {
      width: 100%;
  }
}

.flex-1 {
  flex: 1;
}
</style>