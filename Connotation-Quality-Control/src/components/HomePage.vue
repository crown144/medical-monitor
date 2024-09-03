<template>
  <div class="container">
    <nav class="custom-navbar">    
      <ul class="custom-navbar-list">   
        <li class="custom-menu-item">   
          <div class="logo-container">
            <img src="../assets/wjw.png" alt="Logo" class="custom-menu-image" />    
            <span class="custom-menu-text">基于大模型的三医联动监管平台</span>
          </div> 
        </li> 
        <span class="custom-menu-time">海南卫健委信息中心</span>    
      </ul>    
    </nav> 
    <nav class="custom-navbar" style="margin-top: 10px;">   
      <ul class="custom-navbar-list">   
        <!-- <li class="custom-menu-item">   
          <div class="logo-container">
            <img src="../assets/wjw.png" alt="Logo" class="custom-menu-image" />    
            <span class="custom-menu-text">沪医智算</span>
          </div> 
        </li> -->
        <!-- <li   
          class="custom-navbar-item"   
          style="margin-left: 50px;"
          :class="{ 'active': activeName === '1' }"   
          @click="activeName = '1'"  
        >  
          首页  
        </li>     -->
        <li   
          class="custom-navbar-item"   
          :class="{ 'active': activeName === '3' }"   
          @click="activeName = '3'"  
        >  
        医保控费 
        </li>    
        <li   
          class="custom-navbar-item"   
          :class="{ 'active': activeName === '4' }"   
          @click="activeName = '4'"  
        >  
        医疗质控  
        </li>    
        <!-- <li   
          class="custom-navbar-item"   
          :class="{ 'active': activeName === '5' }"   
          @click="activeName = '5'"  
        >  
          术语归一化  
        </li>    
        <li   
          class="custom-navbar-item"   
          :class="{ 'active': activeName === '6' }"   
          @click="activeName = '6'"  
        >  
          数据助手  
        </li>     -->
        <li   
          class="custom-navbar-item"   
          :class="{ 'active': activeName === '7' }"   
          @click="activeName = '7'"  
        >  
        药品监管  
        </li>   
        <!-- <span class="custom-menu-time">{{  currentDateTime  }}</span>     -->
      </ul>    
    </nav> 
    <!-- <div class="block text-center">
      <div class="cover-layer">
        <p @click="showImage(0)">数据</p>
        <p @click="showImage(1)">预训练</p>
        <p @click="showImage(2)">微调</p>
        <p @click="showImage(3)">应用</p>
      </div>
      <el-carousel height="150px" class="carousel-container">
        <el-carousel-item v-for="(image, index) in imageList" :key="index">
          <img :src="image.path" alt="carousel-image" class="carousel-image">
          <div class="caption">{{ image.text }}</div>
        </el-carousel-item>
      </el-carousel>
    </div> -->

    <div class="content">
      <Evaluation v-if="activeName === '2'"/>
      <Quality v-else-if="activeName === '3-1'" />
      <IndexQualit v-else-if="activeName === '3-2'" />
      <QualityControl v-else-if="activeName === '3-3'" />
      <MainPage @childEvent="handleChildData" @activeName="receiveActive" v-else-if="activeName === '1'"/>
      <SygyhTotal v-else-if="activeName === '5'"></SygyhTotal>
      <!-- <Shujuzhushou v-else-if="activeName === '6'"></Shujuzhushou> -->
      <QualityTotal v-else-if="activeName === '3'"></QualityTotal>
      <div v-show="activeName === '4'" class="term-normalization">
        <iframe src="http://localhost:8501/" frameborder="0" class=""></iframe>
      </div>
      <div v-show="activeName === '6'" class="term-normalization">
        <iframe src="http://localhost:8099/" frameborder="0" class=""></iframe>
      </div>
      <div v-show="activeName === '7'" class="term-normalization">
        <iframe src="http://localhost:9111/" frameborder="0" class=""></iframe>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onMounted } from 'vue'
import QualityControl from './panels/nhzk/QualityControl.vue'
import Evaluation from './panels/Evaluation.vue'
import MainPage from './panels/MainPage.vue'
import Quality from './panels/nhzk/Qualit.vue'
import IndexQualit from './panels/nhzk/IndexPage.vue'
import Shujuzhushou from './panels/Shujuzhushou.vue'
import QualityTotal from './panels/nhzk/QualityTotal.vue'
import SygyhTotal from './panels/sygyh/SygyhTotal.vue'

const activeName = ref('3')
 
const receiveActive = (message) => {
  activeName.value = message;
  console.log(activeName.value)
}

const imageList = ref([
  {
    name: '数据',
    path: '/src/assets/pic/1.png',
    text: '大量医学语料，卫健委提供的权威指南'
  },
  {
    name: '预训练',
    path: '/src/assets/pic/2.png',
    text: '海量医学语料，卫健委提供的权威指南'
  },
  {
    name: '微调',
    path: '/src/assets/pic/3.png',
    text: '上百万条医疗对话，术语库转换，归一化、推理任务'
  },
  {
    name: '应用',
    path: '/src/assets/pic/4.png',
    text: '医疗问答、术语归一化、数据助手、电子病历生成'
  }
])

const handleChildData = (data: string) => {
  console.log(data)
  activeName.value = data
}

const showImage = (index: number) => {
  activeName.value = '1'; 
  setTimeout(() => {
    activeName.value = (index + 1).toString(); 
  }, 100);
}

const currentDateTime = ref('');

const getCurrentDateTime = () => {
  const date = new Date();
  const year = date.getFullYear();
  const month = date.getMonth() + 1; // 月份从0开始，需要加1
  const day = date.getDate();

  const hours = date.getHours();
  const minutes = date.getMinutes();

  const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
  const weekday = weekdays[date.getDay()];

  const formattedDateTime = `${year}/${month}/${day} ${hours}:${minutes} ${weekday}`;

  currentDateTime.value = formattedDateTime;
}

onMounted(() => {
  getCurrentDateTime();
  setInterval(getCurrentDateTime, 1000);
});

</script>
<style scoped>
.container {
  width: 100%;
  height: 100%;
}

.custom-navbar {
  display: flex;
  background-color:white ;
  height: 60px;
  border-radius: 5px;
  justify-content: space-between;
  align-items: center;
}

.carousel-image {
  width: 100%; 
  height: 200px; 
  object-fit: cover;
}

.block {
  position: relative;
}

.cover-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 80px;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.6);
  z-index: 2; 
  display: flex; 
  flex-direction: column;
  justify-content: center; 
  align-items: center;
  text-align: center;
}

.cover-layer p {
  margin: 5px 0;
  font-weight: 400;
}

.carousel-container {
  z-index: 1; 
  border-radius: 10px
}

.fixed-content {
  position: absolute;
  top: 0;
  left: 0;
  width: 100px;
  height: 200px; 
  z-index: 3; 
}

.carousel-item-wrapper {
  position: relative;
}

.caption {
  position: absolute;
  bottom: 10px;
  left: 100px;
  background-color: rgba(255, 255, 255, 0.6);
  color: black;
  padding: 5px;
  border-radius: 5px; 
}

.content {
  border-radius: 10px
}

.custom-menu-image {
  width: 60px;
  height: 60px; 
  margin-left: 10px;
}

.custom-menu-text {
  color: black;
  margin-left: 10px;
  font-weight: 600;
  font-size: 28px;
}

.custom-menu-time {
  margin-top: 5px;
  background-color: transparent; 
  padding: 5px 10px;
  border-radius: 5px;
  font-weight: 600;
  font-size: 20px;
  float: right;
  color: rgb(153, 153, 154);
  position: static;
  margin-left: auto;
  float: right;
}


iframe {
  width: 100%;
  height: 1050px;
}

.custom-navbar-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-wrap: nowrap;
  align-items: center;
  width: 100%;
  height: 100%;
}

.custom-menu-item {
  display: flex;
  align-items: center;
  height: 100%;
}

.custom-navbar-item {
  cursor: pointer;
  padding: 10px;
  margin: 0 5px; /* 调整左右边距 */
  font-size: 24px;
  width: 200px; 
  text-align: center;
  font-weight: 600;
  display: flex; /* 使用 Flexbox */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  transition: background-color 0.3s, color 0.3s; /* 添加过渡效果 */
}

.custom-navbar-item.active {
  background-color: rgb(35, 129, 254);
  color: #ffffff; 
  border-radius: 5px; 
  height: 40px; 
  text-align: center;
}

.logo-container {
  display: flex;
  align-items: center;
}


</style>

