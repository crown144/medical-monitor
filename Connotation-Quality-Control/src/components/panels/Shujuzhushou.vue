<template>
    <div class="chat-top" style="height: 10vh; margin-top: 20px; width: 100%; display: flex; align-items: center; justify-content: space-between;">
      <!-- <div style="float: left;height: 100px;width: 100px;background-color: gray;">logo</div> -->
      <div style="display: flex; justify-content: center; align-items: center;">
        <el-select
          style="width: 200px;margin-right: 800px;"
          v-model="value"
          placeholder="选择数据库"
          size="large"
        >
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </div>  
    </div>
    <div class="chat-container">
      <div class="chat-list">
        <div class="chat-add" @click="chatAdd">
          <svg class="icon" aria-hidden="true">
            <use xlink:href="#icon-duihua"></use>
          </svg>
          <span class="icon-name">历史记录1</span>
        </div>
        <div class="chat-zsk">
          <svg class="icon" aria-hidden="true">
            <use xlink:href="#icon-duihua"></use>
          </svg>
          <span class="icon-name">历史记录2</span>
        </div>
        <div class="chat-zsk">
          <svg class="icon" aria-hidden="true">
            <use xlink:href="#icon-duihua"></use>
          </svg>
          <span class="icon-name">历史记录2</span>
        </div>
        <el-divider style="margin-top: 300px;" border-style="double" />
        <!-- <div class="chat-add" @click="chatAdd">
          <svg class="icon" aria-hidden="true">
            <use xlink:href=""></use>
          </svg>
          <span class="icon-name">模型管理</span>
        </div>
        <div class="chat-add" @click="chatAdd">
          <svg class="icon" aria-hidden="true">
            <use xlink:href=""></use>
          </svg>
          <span class="icon-name">数据库管理</span>
        </div> -->
      </div>
      <div class="chat-main">
        <div class="chat-messages">
          <div class="message">
            <div class="user-info">
              <svg class="icon assistant-icon" aria-hidden="true">
                <use xlink:href="#icon-chat-gpt"></use>
              </svg>
              <span class="username bold"></span>
            </div>
            <el-tabs v-model="activeName" class="message-content" @tab-click="handleClick">
              <el-tab-pane label="图表" name="first">
                <div class="message-content">
              <div ref="echartsContainer" style="height: 300px; width: 500px;"></div>
            </div>
              </el-tab-pane>
              <el-tab-pane label="查询语句" name="second">
                <pre>  
                  <code>  
          SELECT
            地区名称，
            SUM(死亡人数)As total deaths,
            SUM(死亡人数)/SUM(死亡人数)OVER(
              PARTITION BY
                地区编码
            )as death percentage
          FROM
            goutibing
          GROUP BY
            地区编码，
            地区名称  
                  </code>  
              </pre>  
              </el-tab-pane>
              <el-tab-pane label="数据" name="third">
                <el-table :data="tableData" border style="width: 500px"
                :header-cell-style="tableHeaderColor">
                  <el-table-column prop="name" align="center" label="地区名称" width="180" />
                  <el-table-column prop="total_deaths" align="center" label="total deaths" width="120" />
                  <el-table-column prop="death_percentage" align="center" label="death percentage" />
                </el-table>
              </el-tab-pane>
            </el-tabs>
          </div>
        </div>
        <div class="chat-input">
          <el-input v-model="newMessage" @keyup.enter.native="sendMessage" placeholder="Message AI..." />
          <el-button type="primary" style="margin-left: 10px;height: 50px;">发送</el-button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import * as echarts from 'echarts';
  
  export default {
    data() {
      return {
        messages: [],
        newMessage: '',
        hasMessages: false,
        showPopup: false,
        chatList: [
          {
            id: 1,
            request: "请问我该做什么检查？",
            response: "心电图"
          }
        ],
        value: '',
        options: [
          { label: '数据库1', value: 'db1' },
          { label: '数据库2', value: 'db2' },
          // 添加更多选项...
        ],
        tableHeaderColor : {
            background: ' white !important',
            color: '#333333',
            fontSize: '14px',
            textAlign: 'center',
        },
        tableData: [
          {
            name:'全国',
            total_deaths:707,
            death_percentage:7
          },
          {
            name:'北京市',
            total_deaths:25,
            death_percentage:8
          },
          {
            name:'天津市',
            total_deaths:10,
            death_percentage:5
          },
          {
            name:'河北省',
            total_deaths:10,
            death_percentage:2
          },
          {
            name:'山西省',
            total_deaths:12,
            death_percentage:2
          },
        ]
      };
    },
    mounted() {
      this.initEcharts();
    },
    methods: {
      initEcharts() {
        const chartInstance = echarts.init(this.$refs.echartsContainer);
  
        const option = {
          xAxis: {
            type: 'category',
            data: ['', '', '', '']
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              data: [ 80, 70, 110, 130],
              type: 'bar'
            }
          ]
        };
  
        chartInstance.setOption(option);
      },
      sendMessage() {
        this.hasMessages = true;
        const userMessage = { text: this.newMessage, user: 'YOU', isUser: true };
        this.messages.push(userMessage);
        this.newMessage = '';
  
        setTimeout(() => {
          const assistantMessage = {
            text: '病人入院后，按照临床指南和专家知识，立即做了影像学检查，做了影像学检查，做了影像学检查，在病原体检查结果未知情况，依据儿科专家经验，按照XX情况诊疗，依据前期数据以及机器学习结果，XX的感染概率是xx.病人危重的概率是X决策结果:高度怀疑MP感染，建议MP感染治疗',
            user: 'AI助手',
            isUser: false,
          };
          this.messages.push(assistantMessage);
          this.hasMessages = true;
        }, 500);
      },
      chatAdd() {
        this.hasMessages = false;
        this.messages = [];
      }
    }
  };
  </script>
  
  <style scoped>
  .chat-container {
    background-color: white;
    display: flex;
    height: 80vh; /* 设置容器高度为 500px */
    border: 1px solid #ccc;
    padding: 10px;
    font-size: 20px;
  }
  
  .chat-list {
    flex: 20%; /* chat-list 占据 20% 的宽度 */
    overflow-y: auto; /* 添加滚动条 */
    border: 1px solid #ccc;
    border-radius: 10px;
    margin-right: 10px;
    height: 80%;
  }
  
  .chat-main {
    flex: 80%;
    display: flex;
    flex-direction: column;
  }
  
  .chat-messages {
    flex: 1; /* chat-messages 占据 chat-main 的全部高度 */
    overflow-y: auto; /* 添加滚动条 */
  }
  
  .chat-add {
    border: 1px solid #409EFF;
    border-radius: 10px;
    margin: 10px;
    width: 90%;
    height: 50px;
    transition: border-color 0.3s;
    background-color: white;
  }
  .chat-zsk {
    border: 1px solid #409EFF;
    border-radius: 10px;
    margin: 10px;
    width: 90%;
    height: 50px;
    transition: border-color 0.3s;
    background-color: white;
  }
  
  .chat-add:hover {
    background: #175dfd;
    cursor: pointer;
    .icon-name {
      color: white;
    }
  }
  
  .chat-zsk:hover {
    background: #175dfd;
    cursor: pointer;
    .icon-name {
      color: white;
    }
  }
  
  .center-message {
    position: absolute;
    top: 50%;
    left: 60%;
    transform: translate(-50%, -50%);
    text-align: center;
  }
  
  .message {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    margin-bottom: 8px;
  }
  
  .user-info {
    display: flex;
    align-items: center;
    margin-bottom: 4px;
  }
  
  .username {
    margin-left: 4px;
  }
  
  .bold {
    font-weight: bold;
  }
  
  .user-icon,
  .assistant-icon {
    width: 24px; /* 设置图标宽度 */
    height: 24px; /* 设置图标高度 */
    margin-right: 8px;
  }
  
  .message-content {
    align-items: center;
    text-align: left;
    /* font-size: 20px; */
    background-color: #DCDCDC; /* 设置用户发送消息的背景色 */
    border-radius: 10px; /* 添加椭圆形边框 */
    padding: 8px; /* 添加内边距 */
    margin-left: 50px;
  }
  
  .chat-input {
    display: flex;
    margin-top: 10px;
    height: 50px;
  }
  
  .el-input {
    font-size: 20px;
  }
  
  input {
    flex: 1;
    padding: 8px;
    box-sizing: border-box;
  }
  
  .username.bold {
    font-size: 20px; /* 缩小字体 */
  }
  
  .user-info .assistant-icon {
    font-size: 20px; /* 缩小字体 */
  }
  
  .user-message {
    background-color: #DCDCDC; /* 设置用户发送消息的背景色 */
    border-radius: 10px; /* 添加椭圆形边框 */
    padding: 8px; /* 添加内边距 */
  }
  
  .icon {
    float: left;
    width: 40px; 
    height: 40px;
    margin: 5px;
  }
  
  .icon-name {
    float: left;
    margin: 10px;
  }
  
  .el-select {
    height: 100%;
    width: 90%;
    margin: 10px;
  }
  
  .title {
    font-size: 14px;
    margin: 10px;
  }
  </style>
  