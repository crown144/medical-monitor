<template>
  <div class="box" style="margin-top: 0px;width: 100%; position: relative;">
    <el-table :data="tableData" class="custom-table" style="width: 100%">
      <!-- <el-table-column prop="id" label="ID" width="200" /> -->
      <el-table-column prop="tid" label="病人ID" width="400" />
      <!-- <el-table-column prop="name" label="病种类型" width="350" /> -->
      <el-table-column prop="created" label="检测时间" width="400" />
      <el-table-column prop="filename" label="检测文件" />
      <!--<el-table-column prop="filepath" label="保存路径" width="220" />-->
      
      <!-- <el-table-column prop="json_error_file" label="结果文件" width="280" />
      <el-table-column prop="detectstatus" label="检测状态" /> -->
      <el-table-column label="操作" width="400" >
        <template #default="scope">
          <div style="display: flex; justify-content: space-between">
            <el-button @click="downloadFileDoc(scope.row.id, scope.row.filename)">下载检测文件</el-button>
            <el-button @click="downloadFileJson(scope.row.id, scope.row.json_error_file)">下载检测结果</el-button>
            <el-button @click="lookfileFn(scope.row.id)">查看检测结果</el-button>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="accuracy" label="正确率" width="200" />
    </el-table>
    <el-pagination style="margin-top: 15px" small background @size-change="handleSizeChange"
      @current-change="handleCurrentChange" :current-page="currentPage" :page-sizes="[10, 20, 30, 40]"
      :page-size="pageSize" :total="total">
    </el-pagination>


    <el-dialog v-model="dialogTableVisible" title="" width="1200" style="height: 800px;overflow-y: auto;border-radius: 17px;" >
      <div class="card-list" style="overflow-y: auto;">
              <el-card
                style="width: 1000px;margin: 0  0 30px 0;background-color: rgb(241,242,247);"
                v-for="(item, index) in cardList"
                :key="index"
               
              >
                <div class="text item" >
                  <li
                    style="text-align: left;margin: 10px;line-height: 30px;"
                    v-for="key in Object.keys(item)"
                    :key="key"
                    :class="{
                          redc: key === '审查结论' && item[key] === '格式上存在问题',
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
          
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus'
const router = useRouter();
const responseData = ref(null);

// const getData = () => {
//   axios
//     .get("http://127.0.0.1:5000/doclist")
//     .then((response) => {
//       // 请求成功，处理返回的数据
//       responseData.value = response.data;
//       responseData.value.forEach((item) => {
//         item.created = formatDateTime(item.created)
//       })
//       getData2()
//     })
//     .catch((error) => {
//       // 请求失败，处理错误
//       console.error("Error fetching data:", error);
//     });
// };
const getData = () => {
  axios
    .get("http://127.0.0.1:5000/doclist")
    .then((response) => {
      // 请求成功，处理返回的数据
      responseData.value = response.data;

      // 对数据按照 `created` 字段进行排序，倒序排列
      responseData.value.sort((a, b) => new Date(b.created) - new Date(a.created));

      responseData.value.forEach((item) => {
        item.created = formatDateTime(item.created);
      });

      getData2();
    })
    .catch((error) => {
      // 请求失败，处理错误
      console.error("Error fetching data:", error);
    });
};

// 点击事件
const downloadFileDoc = async (id, filename) => {
  try {
    const response = await axios.get(
      `http://127.0.0.1:5000/download_doc/${id}`,
      {
        responseType: "blob",
      }
    );
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
  } catch (error) {
    console.error("Error downloading file:", error);
  }
};

const downloadFileJson = async (id, filename) => {
  try {
    const response = await axios.get(
      `http://127.0.0.1:5000/download_json/${id}`,
      {
        responseType: "blob",
      }
    );
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", filename);
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
  for (let i = start; i < end; i++) {
    data.push(responseData.value[i]);
  }
  tableData.value = data;
};

//时间处理函数
const formatDateTime = (dateTimeString) => {
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

const cardList = ref([])
const dialogTableVisible = ref(false)
const lookfileFn = async (id) => {
  await axios({
    url: `http://127.0.0.1:5000/download_json/${id}`, // 请求地址
    method: 'get',
    headers: {
      'Content-Type': 'application/json;charset-utf-8',
    },
    responseType: 'json', // 表明返回服务器返回的数据类型
  })
    .then(async res => {
      if (res.status === 200) {
        dialogTableVisible.value  = true
        cardList.value = res.data.data
      }
    })
    .catch(err => {
      ElMessage({
        type: 'error',
        message: '文件预览失败' + err,
        duration: 1000,
      })

    })
}

// 在组件挂载时发起请求
onMounted(() => getData());
</script>

<style scoped>
.btn {
  display: inline-block;
  width: 45px;
  height: 25px;
  line-height: 25px;
  border-radius: 4px;
  box-shadow: rgba(34, 36, 38, 0.15) 0px 0px 0px 0px inset;
  font-size: 12px;
  text-align: center;
  font-family: Lato, "Helvetica Neue", Arial, Helvetica, sans-serif;
  cursor: pointer;
}

.btn1 {
  background-color: rgb(33, 133, 208);
  color: rgb(255, 255, 255);
}

.btn2 {
  background-color: rgb(116, 117, 118);
  color: rgba(0, 0, 0, 0.6);
}

/* 给表头单元格加背景色 */
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

.chat-container {
  width: 100%;
  padding: 10px;
  border: 0;
  height: 620px;
  /* 设置 chat-container 的固定高度 */
  overflow-y: auto
}

.chat-container::-webkit-scrollbar {
  width: 6px;
  /* 设置滚动条宽度 */
  background-color: transparent;
  /* 设置滚动条背景色为透明 */
}

.chat-container::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  /* 设置滚动条滑块颜色为半透明 */
  border-radius: 3px;
  /* 设置滚动条滑块圆角 */
}

.chat-container::-webkit-scrollbar-thumb:hover {
  background-color: rgba(0, 0, 0, 0.4);
  /* 设置滚动条滑块悬停时的颜色 */
}
.card-list{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.bluec{
  color:blue;
  
}
.redc {
  color: red;
}

</style>