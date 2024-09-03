<template>
  <div>
    <!-- 内容区域 -->

    <div
      id="content"
    >
      <h2 style="text-align: center;">电子病历标准性检测</h2>
      <!-- 步骤指示器 -->
      <div class="ui segment" style="height: 900px;">
        <el-steps style="max-width: 1800px" :active="stepIndex" align-center finish-status="success" >
        <el-step title="确定检测文档"  style=""/>
        <el-step title="查看检测结果"  />
        <el-step title="重新上传文档"  @click="reback"/>
        </el-steps>

        <div class="show1" v-if="!showCardList" style="width: 600px;;margin:40px auto">
          <!-- 步骤内容 -->
          <h3 class="ui header">STEP 1 : 选择需要检测的文档</h3>
          <div style="font-size: 14px; color: red; padding-bottom: 10px">
            <br />
          </div>

          <div style="overflow: auto;width: 500px;margin-top: -20px;" v-show="tableData.length > 0">
            <el-table :data="tableData" border class="custom-table">
              <el-table-column prop="bzname" label="规则类型" weight="100"></el-table-column>
              <el-table-column prop="tid" label="病人ID" weight="100"></el-table-column>
            </el-table>
            <el-pagination
              style="margin-top: 15px"
              small
              background
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
              :current-page="currentPage"
              :page-sizes="[10, 20, 30, 40]"
              :page-size="pageSize"
              :total="total"
            >
            </el-pagination>
          </div>
          <br />

          <!-- 文件上传表单 -->
          <el-form  :inline="true" v-show="showTid" :model="formInline" class="demo-form-inline">
            <el-form-item label="请输入要检测的病人ID*">
              <el-input
                v-model="formInline.id"
                placeholder="请输入病人ID"
                clearable
              />
            </el-form-item>
          </el-form>

          <form id="uploadForm" @submit.prevent="submitForm">
            <button
              @click.prevent="downloadTemplatesFile"
              style="border-radius: 17px; margin-right: 20px;background-color: rgb(34,128,254);"
              class="ui primary button"
              v-show="!tableData.length > 0"
            >
              下载模版文件
            </button>
            <div class="ui action input">
              <input
                id="fileInput"
                type="file"
                ref="fileInput"
                @change="getExcelData"
                accept=".xlsx"
                required

              />
              <button
                @click="uploadFile"
                type="submit"
                class="ui primary button"
                style="background-color: rgb(34,128,254);"
              >
                提交检测
              </button>
            </div>
          </form>
        </div>

        <div  v-else >
          <div style="text-align: center;width: 100%;height: 50px;line-height:50px;margin: 10px 0 18px 0;color:rgb(40,131,254);font-size: 25px;background-color: rgb(241,242,247);">您检测的病人ID为:{{ formInline.id }}</div>
          <div class="res-box" >
            <div class="res-box-left" v-show="showCardList">
            <el-table height="600" style="width: 950px;" :data="tableData3" border class="custom-table">
              <el-table-column prop="wdmxlbsm" label="文书名称" width="150"></el-table-column>
              <el-table-column prop="wddmc" label="字段名称" width="150"></el-table-column>
              <el-table-column prop="wddnr" label="内容" width="600"></el-table-column>
            </el-table>
            <el-pagination
              style="margin-top: 15px"
              small
              background
              @size-change="handleSizeChange3"
              @current-change="handleCurrentChange3"
              :current-page="currentPage3"
              :page-sizes="[10, 20, 30, 40]"
              :page-size="pageSize3"
              :total="total3"
            >
            </el-pagination>
          </div>
          <div class="card-box">
            <div
            v-show="showTitle>0"
              class="top"
              style="
                height: 80px;
                width: 100%;
                text-align: center;
                
              "
            >
            <div style="width:100%;text-align:center;font-size:25px;line-height: 40px;;background-color: rgb(241,242,247);">
              {{tmsg}}
            </div>
            </div>
            <div class="card-list" >
              <el-card
                style="width: 900px;margin: 0  0 30px 0;background-color: rgb(241,242,247);"
                v-for="(item, index) in cardList"
                :key="index"
               
              >
                <div class="text item" >
                  <li
                    style="text-align: left;margin: 10px;line-height: 30px;"
                    v-for="key in Object.keys(item)"
                    :key="key"
                    :class="{
                          redc: key === '审查结论' &&( item[key] === '存在问题'|| item[key] === '格式上存在问题'|| item[key] === '内容上存在问题'),
                          bluec: key === '审查理由'
                        }"
                  >
                    <span style="font-weight: 800" class="title"
                      >{{ key }}:</span
                    >
                    <span class="cxt">{{ item[key] }}</span>
                  </li>
                </div>
              </el-card>
            
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
import { ref, onMounted,reactive } from "vue";
import * as XLSX from "xlsx";
import axios from "axios";
// 引入 JavaScript 文件
import { ElLoading } from 'element-plus'

import { ElMessage } from 'element-plus'
// 引入 JavaScript 文件
import '../../../../public/js/jquery-3.6.4.min.js';
import '../../../../public/js/jsQR.js';
import '../../../../public/js/semantic.min.js';
import '../../../../public/js/jszip.min.js';
import '../../../../public/js/docx-preview.js';

// 引入 CSS 文件
import '../../../../public/css/semantic.min.css';

import { useRouter } from 'vue-router';

const router = useRouter();

const showCardList = ref(false);
const cardList = ref([]);

const index = ref(0);
const stepIndex=ref(0);

const showTid = ref(false)
const tid = ref("");
const bzname = ref("");
const jsonData1 = ref([])
// 表单数据
const formInline = reactive({
  id: '',
  name: '',
})



function uniqueByProperty(arr, prop) {
    const map = new Map();
    arr.forEach(item => {
        map.set(item[prop], item);
    });
    return [...map.values()];
}

const excelData2 = ref([]);
// 获取excel数据
const getExcelData = (event) => {
  const file = event.target.files[0];

  if (file && file.name.endsWith(".xlsx")) {
    // 读取 .xlsx 文件内容
    const reader = new FileReader();

    reader.onload = function (event) {
      const data = new Uint8Array(event.target.result);
      const workbook = XLSX.read(data, { type: "array" });
      const sheetName = workbook.SheetNames[0];
      const worksheet = workbook.Sheets[sheetName];
      const jsonData = XLSX.utils.sheet_to_json(worksheet);
      jsonData1.value = uniqueByProperty(jsonData, 'tid');
      
      const headers = [];
      for (let key in worksheet) {
        if (key[0] === "!") continue;
        if (key[1] === "1") {
          headers.push(worksheet[key].v);
        } else {
          break;
        }
      }
      excelData2.value = []
      for (let key in jsonData1.value) {
        const obj = {};
        Object.keys(jsonData1.value[key]).forEach((item, index) => {
          obj[headers[index]] = jsonData1.value[key][item];
        });
        excelData2.value.push(obj);

      }
      excelData2.value = uniqueByProperty(excelData2.value, 'tid');
      // console.log(excelData2.value);
      // console.log(excelData2.value);
      getData();
      showTid.value = true
      stepIndex.value=1
      //   displayExcelData(parsedData);
    };
    reader.readAsArrayBuffer(file); // 替换成你的Excel文件
  } else {
    // 提示选择有效的 .xlsx 文件
    ElMessage.warning("Please select a valid .xlsx file.");
  }
};



// 路由跳转到列表页面
const gotoList = ()=>{
  router.push({path:'/one'})
}

const reback = () => {
  console.log("aaaa");
  stepIndex.value=0;
  index.value = 0;
  showCardList.value = false;
  tableData.value = [];
  formInline.id = ''
  formInline.name = ''
  showTid.value = false
};

const fileInput = ref(null);


const onSubmit = () => {
  console.log('submit!')
}

const tmsg = ref('')
const excelData3 = ref([])

const showTitle = ref(false)
// 上传文件以及后续数据处理
const uploadFile = async () => {
  const file = fileInput.value.files[0];
  const formData = new FormData();
  formData.append("file", file);
  formData.append("id", formInline.id);
  formData.append("name", formInline.name);
  if(formInline.id===''){
    ElMessage.warning("请输入要检测的病人ID！");
    return 
  }

const isStringInArray = excelData2.value.some(item => item.tid === formInline.id);


if (!isStringInArray) {
  ElMessage.warning("请输入正确的病人ID！");
  return false; // 结束函数
}
  const loading = ElLoading.service({
    lock: true,
    text: "正在检测，请稍后。",
    background: "rgba(0, 0, 0, 0.7)",
  });

  const response = await axios.post(
    "http://127.0.0.1:5000/upload_doc",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  console.log(response,'===============')
  if (response.status === 200) {
    index.value = 1;
    stepIndex.value=2;
    loading.close();
    showCardList.value = true;
    jsonData1.value = []
    excelData3.value = response.data[0].table_data;
    
    //console.log(response.data[0].data_Classify)
    let myJsonClassify=response.data[0].data_Classify
    console.log(myJsonClassify)
    tid.value = formInline.id;
    getData3() 
    if(response.data[0].data.length===0){
      ElMessage.warning("检测文档没有错误！");
      tmsg.value = response.data[0].message
      showTitle.value = true
      cardList.value = [];
    }else{
      ElMessage.success("检测成功");
      showTitle.value = false
      cardList.value = response.data[0].data;
      fileInput.value.value = "";
      bzname.value = formInline.name;
      tmsg.value = '';
    }

      // 排序检测结果
    sortDetectionResults();
    // 处理上传成功后的逻辑
  } else {
    loading.close();
    ElMessage.error("检测失败: " + response.data.error);

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
  for (let i = start; i <end; i++) {
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
        responseType: "blob",
      }
    );
    console.log(response); // 打印响应详细信息
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "模板文件.xlsx");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link); // 下载后移除链接
    window.URL.revokeObjectURL(url); // 释放内存
  } catch (error) {
    console.error(error); // 打印错误详细信息
    ElMessage.error("下载模版文件失败！");
  }
};

// 文件检测成功后的后端数据返回以及逻辑处理
const tableData3 = ref([]);
const currentPage3 = ref(1);
const pageSize3 = ref(10);
const total3 = ref(0);

const getData3 = async () => {
  const totalValue = excelData3.value.length;
  total3.value = totalValue;;
  const start = (currentPage3.value - 1) * pageSize3.value;
  const end = Math.min(currentPage3.value * pageSize3.value, totalValue);
  const data = [];
  for (let i = start; i <end; i++) {
    data.push(excelData3.value[i]);
  }
  tableData3.value = data;
  
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
  showTitle.value = false
});
</script>
  
  



  <style scoped>
body {
  margin: 0;
  padding: 0;
  font-family: "Arial", sans-serif;
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
  background-color: rgba(50, 50, 50, 0.8); /* 半透明白色背景 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* 确保加载界面在最上层 */
}

/* Excel 样式 */

.res-box{
  margin-top: 15px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  
}
.res-box-left{
  width: 900px;
  height: 600px;
  /* margin-left: 40px; */
  /* overflow: auto; */
}
.card-list {
  display: flex;
  flex-wrap: wrap;
  /* min-width: 600px; */
  width: 900px;
  list-style: none;
  justify-content: space-between;
  align-content:flex-start;
}
.card-box {
  width: 900px;
  height: 600px;
  
  /* margin-right: 40px; */
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
:deep(.el-table__header th) {
  background-color: #f5f5f5 !important;
  color: black;
}
.custom-table{
    border-radius: 8px; /* 增加圆角 */
  }
  ::v-deep(.el-table .el-table__row:nth-child(odd)) {
  background-color: #ffffff !important; /* 白色 */
}
::v-deep(.el-table .el-table__row:nth-child(even)) {
  background-color: #f5f5f5 !important; /* 淡灰色 */
}
:deep(.el-step .el-step__line) {
  
  border-top: 3px dashed #CCD1DE;
  height: 0;
  background-color: transparent;
  
  
}
:deep(.el-step__title){
  font-size: 18px;
}
:deep(.el-step__icon.is-text){
  width: 40px;
  height: 40px;
  font-size: 18px;
  border: 5px solid;
}
:dep(.el-step__icon-inner){
  font-size: 18px;
  font-weight: 700 !important;
}
:deep(.el-step .el-step__line-inner) {
  display: none;
}
.bluec{
  color:blue;
  
}
.redc {
  color: red;
}

</style>
  