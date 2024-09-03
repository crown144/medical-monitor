<template>
  <div class="box" style="margin-top: 0px;width: 100%; height: auto;position: relative;">
    <el-card>
    <div class="chat-container" ref="chatContainer">
    <el-table :data="tableData"  style="width: 100%" class="custom-table">
      <el-table-column prop="created" label="检测时间" width="280" />
      <el-table-column show-overflow-tooltip prop="txt_ori" label="原始文本"  />

      <el-table-column label="操作" width="180">
        <template #default="scope">
          <div style="display: flex; justify-content: space-between">
            <el-button @click="lookfileFn(scope.row.id)">预览</el-button>
            <el-button @click="downloadFileJson(scope.row.id, scope.row.res_file)" type="primary">结果</el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>
  </div>
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
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus'
const router = useRouter();
const responseData = ref(null);

const getData = () => {
  axios
    .get("http://127.0.0.1:5000/textlist")
    .then((response) => {
      // 请求成功，处理返回的数据
      responseData.value = response.data;
      responseData.value.forEach((item)=>{
      item.created = formatDateTime(item.created)
    })
    getData2()
    })
    .catch((error) => {
      // 请求失败，处理错误
      console.error("Error fetching data:", error);
    });
};

// 点击事件


const downloadFileJson = async (id, filename) => {
  try {
    const response = await axios.get(
      `http://127.0.0.1:5000/download_text_json/${id}`,
      {
        responseType: "blob",
      }
    );
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    var fileName = filename.split("\\").pop();
    link.setAttribute("download", fileName);
    document.body.appendChild(link);
    link.click();
  } catch (error) {
    console.error("Error downloading file:", error);
  }
};

const getData2 = async () => {
// 模拟获取数据，实际应用中可以从接口获取数据
// 假设 total 为总条目数，这里使用 Math.ceil(total / pageSize) 计算总页数
const totalValue = responseData.value.length;
total.value = totalValue;
const start = (currentPage.value - 1) * pageSize.value;
const end = Math.min(currentPage.value * pageSize.value, totalValue);
const data = [];
for (let i = start; i <end; i++) {
  data.push(responseData.value[i]);
}
tableData.value = data;
console.log(data);

};

//时间处理函数
const formatDateTime = (dateTimeString)=> {
  // 创建Date对象
  var date = new Date(dateTimeString);
  
  // 获取年、月、日
  var year = date.getFullYear();
  var month = (date.getMonth() + 1).toString().padStart(2, '0'); // 月份从0开始，需要加1，并补齐为两位数
  var day = date.getDate().toString().padStart(2, '0'); // 补齐为两位数
  
  // 拼接成格式化后的日期字符串
  var formattedDate = year + '年' + month + '月' + day + '日';
  
  return formattedDate;
}

const tableData = ref([]);
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);

const handleSizeChange = (page) => {
console.log(page);
pageSize.value = page;
getData2();
};

const handleCurrentChange = (current) => {
currentPage.value = current;
getData2();
};

const lookfileFn = async (id) => {
await axios({
    url: `http://127.0.0.1:5000/download_text_json/${id}`, // 请求地址
    method: 'get',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded;charset-utf-8',
    },
    responseType: 'blob', // 表明返回服务器返回的数据类型
  })
    .then(async res => {
      if (res.status === 200) {
        try {
          const binaryData = []
          binaryData.push(res.data)
          // 判断类型
         
          const re_url = URL.createObjectURL(
            new Blob(binaryData, { type: 'text/plain;charset=utf-8' })
          )
          window.open(re_url)
          
          
        } catch (e) {
          ElMessage({
            type: 'error',
            message: '文件预览失败' + e,
            duration: 1000,
          })
        }
      }
    })
    .catch(err => {
      console.log(err);
      
    })
}
// 在组件挂载时发起请求
onMounted(() => getData());
</script>

<style scoped >


/* 给表头单元格加背景色 */
  /* 给表头单元格加背景色 */
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
  .chat-container {
      width: 100%;
      padding: 10px;
      border: 0;
      height: 600px; /* 设置 chat-container 的固定高度 */
      overflow-y: auto 
    }
    .chat-container::-webkit-scrollbar {
      width: 6px; /* 设置滚动条宽度 */
      background-color: transparent; /* 设置滚动条背景色为透明 */
    }
    .chat-container::-webkit-scrollbar-thumb {
      background-color: rgba(0, 0, 0, 0.2); /* 设置滚动条滑块颜色为半透明 */
      border-radius: 3px; /* 设置滚动条滑块圆角 */
    }
    .chat-container::-webkit-scrollbar-thumb:hover {
      background-color: rgba(0, 0, 0, 0.4); /* 设置滚动条滑块悬停时的颜色 */
    }
</style>