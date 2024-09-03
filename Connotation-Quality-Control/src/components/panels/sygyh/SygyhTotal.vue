<template>
    <el-tabs v-model="activeName" class="custom-tabs" @tab-click="handleClick">
      <el-tab-pane label="术语标准化" name="3-1">
        <iframe src="http://localhost:3170/realtime" frameborder="0" class=""></iframe>
      </el-tab-pane>
      <!-- <el-tab-pane label="术语定义" name="3-2">
        <SyDefine/>
      </el-tab-pane>
      <el-tab-pane label="术语定义展示" name="3-3">
        <DefineShow/>
      </el-tab-pane> -->
    </el-tabs>
  </template>
  
  <script>
import SyDefine from './SyDefine.vue'
import DefineShow from './DefineShow.vue';

  
  export default {
    data() {
      return {
        activeName: '3-1' // 设置默认显示的标签页
      };
    },
    methods: {
      handleClick(tab) {
        console.log('Tab clicked: ', tab.name);
      }
    },
    components: {
      SyDefine,
      DefineShow
      
      
    }
  };
  </script>
  
<style scoped>
iframe {
    width: 100%;
    height: 950px;
    background-color: white;
}

.custom-tabs {
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 10px;
  background-color: white
}

.custom-tabs .el-tabs__header {
  background-color: #ebebeb;
}

.custom-tabs .el-tabs__header .el-tabs__item {
  padding: 10px 20px;
  color: #333;
}

.custom-tabs .el-tabs__header .el-tabs__item.is-active {
  background-color: #fff;
  border-bottom-color: transparent;
}

.custom-tabs .el-tabs__content {
  padding: 20px;
  background-color: #fff;
  border: 1px solid #ccc;
  border-top: none;
  border-radius: 4px;
}
</style>