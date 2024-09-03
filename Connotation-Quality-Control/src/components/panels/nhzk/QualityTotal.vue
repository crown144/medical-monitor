<template>
  <div class="nav-bar">
    <el-dropdown>
      <span 
        class="el-dropdown-link" 
        :class="{ active: activeName === '3-6' }" 
        @click="activeName = '3-6'"
      >
        首页
      </span>
    </el-dropdown>
    <div class="separator"></div>
    <!-- <el-dropdown>
      <span 
        class="el-dropdown-link"
        :class="{ active: activeName === '3-0' }" 
        @click="activeName = '3-0'"
      >
        上传文件管理
      </span>
    </el-dropdown> -->
    <!-- <div class="separator"></div> -->
    <el-dropdown>
      <span class="el-dropdown-link" :class="{ active: activeName.includes('3-1') || activeName.includes('3-2') || activeName.includes('3-3') }">
        异常监测
        <el-icon class="el-icon--right">
          <arrow-down />
        </el-icon>
      </span>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item @click="activeName = '3-1'">指标计算</el-dropdown-item>
          <el-dropdown-item @click="activeName = '3-3'">指标总表</el-dropdown-item>
          <!-- <el-dropdown-item @click="activeName = '3-2'">指标计算历史记录</el-dropdown-item> -->
          <!-- <el-dropdown-item @click="activeName = '3-10'">指标描述</el-dropdown-item> -->
        </el-dropdown-menu>
      </template>
    </el-dropdown>
    <div class="separator"></div>

    <el-dropdown>
      <span 
        class="el-dropdown-link" 
        :class="{ active: activeName === '3-60'||activeName === '3.62' }" 
      >
      规则编辑
      </span>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item @click="activeName = '3-60'">Prompt列表</el-dropdown-item>
          <el-dropdown-item @click="activeName = '3-62'">指标总览</el-dropdown-item>
          <el-dropdown-item @click="activeName = '3-63'">字段总览</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
    <div class="separator"></div>
    <el-dropdown>
      <span 
        class="el-dropdown-link"
        :class="{ active: activeName === '3-8' }"
        @click="activeName = '3-8'"
      >
        数据助手
      </span>
    </el-dropdown>
    <div class="separator"></div>
    <el-dropdown>
      <span class="el-dropdown-link" :class="{ active: activeName.includes('3-4') || activeName.includes('3-5') || activeName.includes('3-9') }">
        医院管理
        <el-icon class="el-icon--right">
          <arrow-down />
        </el-icon>
      </span>
      <template #dropdown>
        <el-dropdown-menu>
          <!--<el-dropdown-item @click="activeName = '3-4'">测试</el-dropdown-item>-->
          <el-dropdown-item @click="activeName = '3-9'">电子病历标准性检测</el-dropdown-item>
          <el-dropdown-item @click="activeName = '3-5'">电子病历检测任务列表</el-dropdown-item>
          <el-dropdown-item @click="activeName = '3-66'">电子病历审查规则</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
    <div class="separator"></div>
    <el-dropdown>
      <span 
        class="el-dropdown-link" 
        :class="{ active: activeName === '3-7' }" 
        @click="activeName = '3-7'"
      >
      后台管理
      </span>
    </el-dropdown>
  </div>

  <div v-if="activeName === '3-6'">
    <MainPage @activeName="receiveActive" />
  </div>
  <div v-else-if="activeName === '3-1'">
    <Qualit />
  </div>
  <div v-else-if="activeName === '3-3'">
    <QualityControl />
  </div>
  <div v-else-if="activeName === '3-2'">
    <DataHistory />
  </div>
  <div v-else-if="activeName === '3-4'">
    <UpLoadData />
  </div>
  <div v-else-if="activeName === '3-9'">
    <UpLoadData1 />
  </div>
  <div v-else-if="activeName === '3-5'">
    <DataHistory />
  </div>
  <div v-else-if="activeName === '3-7'">
    <iframe src="http://localhost:3170/realtime" frameborder="0" class="iframe"></iframe>
  </div>
  <div v-else-if="activeName === '3-8'">
    <iframe src="http://localhost:8100/" frameborder="0" class="iframe"></iframe>
  </div>
  <div v-else-if="activeName === '3-10'">
    <RecordData />
  </div>
  <!-- <div v-else-if="activeName === '3-11'">
    <iframe src="http://localhost:8100/" frameborder="0" class="iframe"></iframe>
  </div> -->
  <div v-else-if="activeName === '3-60'">
    <!-- <PromptList /> -->
    <PromptList :active_name="activeName" @update-active-name="updateActiveName" :mess="mess" @update-mess="updateMess"/>
  </div>
  <div v-else-if="activeName === '3-61'">
    <PromptTest :mess="mess"/>
  </div>
  <div v-else-if="activeName === '3-62'">
    <indicatorList/>
  </div>
  <div v-else-if="activeName === '3-63'"> 
    <fieldList/>
  </div>
  <div v-else-if="activeName === '3-66'">
    <ruleList />
  </div>
</template>


<script>
import Qualit from './Qualit.vue';
import IndexPage from './IndexPage.vue';
import QualityControl from './QualityControl.vue';
import UpLoadData from './UpLoadData.vue';
import UpLoadData1 from './UploadData1.vue';
import DataHistory from './DataHistory.vue';
import MainPage from '../MainPage.vue';
import SygyhTotal from '../sygyh/SygyhTotal.vue';
import RecordData from './RecordData.vue';
import PromptList from './PromptList.vue';
import PromptTest from './PromptTest.vue';
import ruleList from './ruleList.vue';
import test from './test.vue'
import indicatorList from './indicatorList.vue'
import fieldList from './fieldList.vue';

export default {
  data() {
    return {
      activeName: '3-6',
      mess:{},
    };
  },
  methods: {
    receiveActive(message){
      this.activeName = message;
      console.log(message)
    },
    updateActiveName(newActiveName) {
      this.activeName = newActiveName;
    },
    updateMess(neww) {
      this.mess = neww;
    },
  },
  components: {
    Qualit,
    IndexPage,
    QualityControl,
    UpLoadData,
    UpLoadData1,
    DataHistory,
    MainPage,
    SygyhTotal,
    RecordData,
    PromptList,
    PromptTest,
    ruleList,
    test,
    indicatorList,
    fieldList,
  }
};
</script>

<style scoped>
.nav-bar {
  display: flex;
  align-items: center;
  background-color: #fff;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 10px;
}

.el-dropdown-link {
  margin-right: 20px;
  cursor: pointer;
  padding: 10px 15px;
  border-radius: 4px;
  transition: background-color 0.3s, color 0.3s;
  display: flex;
  align-items: center;
  font-size: 16px;
  outline: none;
}

/* .el-dropdown-link:hover {
  background-color: #409EFF;
  color: #fff;
} */

.active {
  background-color: #409EFF;
  color: #fff;
}

.iframe {
  width: 100%;
  height: 950px;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.el-dropdown-menu {
  border: 1px solid #ccc;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.el-dropdown-item {
  transition: background-color 0.3s, color 0.3s;
  outline: none;
}

.el-dropdown-item:hover {
  background-color: #f0f0f0;
}

.separator {
  border-right: 1px solid #ccc;
  height: 20px;
  margin-right: 20px;
}
</style>

