<template>
  <div>
    <!-- 内容区域 -->
    <div
      id="content"
      style="margin: 0px 100px 0 0; width: 100%; height: 900px"

    >
      <!-- 步骤指示器 -->
      <h2>术语定义标准</h2>
      <div class="ui segment">
        <el-steps style="max-width: 1600px" :active="stepIndex" align-center finish-status="success" >
        <el-step title="输入文本"  />
        <el-step title="查看结果"  />
        <el-step title="重新输入"  @click="reback"/>
        </el-steps>
        

        <div class="show1" v-show="!showCardList" style="margin-left: 440px; margin-top:60px">
             <!-- 步骤内容 -->
        <h3 style="text-align: left; padding-left: 48px " class="ui header">
          STEP 1 : 输入需要检测的文本文字
        </h3>
        <h3 style="text-align: left; padding-left: 48px; color: red; font-size: medium" class="ui header" >
        提示：可输入应为一段文本，包含电子病历的中文名和相应的初始定义，可以一次性输出多条数据，并按照空行隔开。也可输入电子病历查询其定义。
        </h3>

        <div style="font-size: 14px; color: red; padding-bottom: 20px">
          <br />
        </div>

        <!-- 文件上传表单 -->

        <div
          style="
            padding-left: 48px;
            display: flex;
            flex-direction: column;
            align-items: flex-start;
          "
        >
          <textarea
          placeholder="请输入要检测的文本..."
            style="width: 690px; height: 200px; margin-bottom: 25px"
            id="fileInput"
            v-model="tInput"
            ref="fileInput"
            required
            @input="handleInput"
          ></textarea>
          <button @click="uploadFile" type="submit" class="ui primary button">
            提交检测
          </button>
        </div>
        </div>
        <div v-show="showCardList">
          
        <div class="card-list"  >
          
          <div class="left">
            <h4 style="margin-left: 300px;">输入文本</h4>
            <textarea   placeholder="请输入要检测的文本..." v-model="tInput" class="content1" style="resize: none;border: none;overflow: auto;outline: none;">
              
            </textarea>
          </div>
          <div class="right">
            <h4>输出文本</h4>
            <div v-html="typedText"  class="content2" style="overflow: auto;">

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
import { ref, onMounted } from "vue";
import * as XLSX from "xlsx";
import axios from "axios";

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
const index = ref(3);
const stepIndex=ref(0)


// const mytext = ref("");

// 路由跳转到列表页面
const gotoList = ()=>{
  router.push({path:'/three'})
}

const reback = () => {
  stepIndex.value=0;
  index.value = 0;
  showCardList.value = false;
  tInput.value = ''
};

const tInput = ref("");
const showCardList = ref(false);
const handleInput = () => {
  
  if(tInput.value==""){
    stepIndex.value=0;
  }else{
    stepIndex.value=1;
  }
  
}
const uploadFile = async () => {

const loading = ElLoading.service({
    lock: true,
    text: "正在检测，请稍后。",
    background: "rgba(0, 0, 0, 0.7)",
  });
  const response = await axios.post(
    "http://127.0.0.1:5000/submittext/",
    { text: tInput.value },
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }
  );

 
  if (response.status === 200) {
    loading.close();
    index.value = 1;
    stepIndex.value=2;
    showCardList.value = true;
    ElMessage.success("检测成功");
    typedText.value = ''; // Clear previous typed text
    // console.log(response.data.data[0].res2)
    await typeWriter(response.data.data[0].res2);
    // 处理上传成功后的逻辑
  }
  else if(response.status === 500){
    loading.close();
    ElMessage.error("检测失败: " + response.data.error);
  }
  else {
    loading.close();
    ElMessage.error("检测失败: " + response.data.error);
    // 处理上传失败后的逻辑
  }
}

const speed = 100;
const typedText = ref('');
// const typeWriter = () => {
  
//   return new Promise(resolve => {
//     let i = 0;
//     const type = () => {
//       if (i < mytext.value?.length) {
//         typedText.value += mytext.value.charAt(i);
//         console.log('bbbb');
//         i++;
//         setTimeout(type, speed); // 修改这里
//       } else {
//         resolve(); // 表示 Promise 完成
//       }
//     }
//     type(); // 初始调用
//   });
// }

async function typeWriter(text) {
  let i = 0;
  const maxLength = text.length;

  while (i < maxLength) {
    const char = text.charAt(i);
    typedText.value += char;
    i++;
    await sleep(speed);
  }
}




// const highlightedText = ref('');

// async function compareAndHighlight() {
//   const maxLength = Math.max(tInput.value.length, mytext.value.length);
//   let result = '';

//   for (let i = 0; i < maxLength; i++) {
//     const char1 = tInput.value[i] || '';
//     const char2 = mytext.value[i] || '';

//     if (char1 !== char2) {
//       result += `<span style="color: red">${char2}</span>`;
//     } else {
//       result += char2;
//     }
//   }

//   mytext.value = result;
//   await typeWriter();
// }
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

onMounted(() => {index.value = 0;});
// onMounted(()=>typeWriter())
</script>
    
    
  
  
  
<style scoped>
body {
  margin: 0;
  padding: 0;
  font-family: "Arial", sans-serif;
}

#content {
  margin-left: 300px;
  padding: 20px;
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
.excel-table {
  border: 1px solid #000 !important;
  border-collapse: collapse;
  width: 100%;
  font-family: Arial, sans-serif;
  max-height: 600px;
}
.excel-table th,
.excel-table td {
  border: 1px solid #ddd;
  padding: 8px;
}
.excel-table th {
  background-color: #f2f2f2;
  font-weight: bold;
  text-align: left;
}
.excel-table tr:nth-child(even) {
  background-color: #f9f9f9;
}
.excel-table tr:hover {
  background-color: #f2f2f2;
}

.card-list{
  margin-top: 10px;
  display: flex;
  justify-content: space-between;
  max-height: 1200px;
  max-height: 600px;
}
.content1,.content2{
  padding: 20px;
  width: 450px;
  height: 400px;
  /* border: 1px solid red; */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s ease-in-out; /* 添加过渡效果 */
}
.content1{
  margin-left: 300px;
}
.content2{
  margin-right: 300px;
}
:deep(.el-step .el-step__line) {
  
  border-top: 3px dashed #CCD1DE;
  height: 0;
  background-color: transparent;
  
  
}
:deep(.el-step .el-step__line-inner) {
  display: none;
}

</style>
    