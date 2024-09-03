
<template>
    <div class="container2">
      <el-card style="height: 100%;width: 100%">
        <h2>指标计算</h2>
      <div class="top-bar">
        <!-- <el-button type="primary" style="margin-right: 20px;" @click="loadFile(1)" class="myButton">测试样例1</el-button>
        <el-button type="primary" style="margin-right: 20px;" @click="loadFile(2)" class="myButton">测试样例2</el-button>
        <el-button type="primary" style="margin-right: 20px;" @click="loadFile(3)" class="myButton">测试样例3</el-button> -->
        <el-select
          style="width: 250px"
          v-model="hospital"
          placeholder="选择医院"
          @change="hospitalChange"
        >
          <el-option
          v-for="item in hospitalList"
          :key="item.value"
          :label="item.label"
          :value="item.value"
          />
        </el-select>
        <!-- <el-select
          style="width: 200px;margin-left: 20px;"
          v-model="type"
          placeholder="选择类型"
        >
          <el-option label="单病种" value="单病种" />
          <el-option label="专科" value="专科" />
        </el-select> -->
        <!-- <el-select
          style="width: 200px;margin-left: 20px;"
          v-model="disease"
          placeholder="选择病种"
          @change="diseaseChange"
        >
          <el-option
            v-for="item in diseaseList"
            :key="item.value"
            :label="item.label"
            :value="item.value"
            />
        </el-select> -->
        <!-- <el-select
          style="width: 200px;margin-left: 20px;"
          v-model="index"
          placeholder="选择指标"
        >
          <el-option
            v-for="item in indexList"
            :key="item.indicator_number"
            :label="item.indicator_number"
            :value="item.indicator_number"
            />
        </el-select> -->
        <!-- <el-button type="primary" style="margin-left: 800px;" @click="importData" class="myButton">导入数据</el-button> -->
          <input
            id="fileInput"
            type="file"
            ref="fileInputRef"
            style="width: 250px;margin-left: 20px"
            @change="getExcelData"
            accept=".xlsx"
            required/>
        <el-button type="primary" style="margin-left: 70%;" @click="uploadFile"
        class="myButton">确定</el-button>
        <el-button type="primary" style="margin-left: 10px;" @click="tableReset"
        class="myButton">重置</el-button> 
        <!-- <el-button type="primary" style="" @click="uploadFile"
        class="myButton">刷新</el-button> -->
        <!-- <el-button type="primary" style="margin-left: 10px;" @click="exportExcel('IndicatorTable.xlsx', '#tableId')">结果导出</el-button> -->
      </div>
      <div style="display: flex;">
        <el-divider style="flex: 3;"content-position="left">指标信息</el-divider>
        <el-divider style="flex: 1;margin-left: 20px" content-position="left">达标率</el-divider>
      </div>
      <div style="display: flex;">  
        <el-table id="tableId" height="750px" stripe v-loading="loading" :data="tableData" :summary-method="sumMethod" style="margin-top: 20px;flex: 3;"  
          :header-cell-style="tableHeaderColor" class="custom-table">
          <el-table-column type="selection" width="55">
          </el-table-column>
          <el-table-column prop="disease" label="病种" width="200" align="center">
            <template #default="scope">
              <span style="font-size: 16px;">{{ scope.row.disease }}</span>
            </template>
          </el-table-column>
          <!-- <el-table-column prop="indicator_number" label="指标编号" width="200" align="center">
            <template #default="scope">
              <span style="font-size: 16px;">{{ scope.row.indicator_number }}</span>
            </template>
          </el-table-column> -->
          <el-table-column prop="indicator_name" label="规则名称1" width="200" align="center">
            <template #default="scope">
              <span style="font-size: 16px;">{{ scope.row.indicator_name }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="emr_id" label="病历编号" width="120" align="center">
            <template #default="scope">
              <span style="font-size: 16px;">{{ scope.row.emr_id }}</span>
            </template>
          </el-table-column>
          <el-table-column label="收费明细原文文" width="120" align="center">
            <template #default="scope">
              <el-button link type="primary" size="small" @click="handleText(scope.row)">查看</el-button>
            </template>
          </el-table-column>
          <el-table-column prop="predict" label="结果" align="center">
          <template #default="scope">
              <el-input type="textarea" rows="4" v-model="scope.row.predict"></el-input>
            </template>
          </el-table-column>
          <el-table-column  prop="yes_or_no"  width="100"  label="是/否"  align="center"  >  
            <template #default="scope">  
              <span v-if="scope.row.yes_or_no === 1">是</span>  
              <span v-else>否</span>  
            </template>  
          </el-table-column>
          <!-- <el-table-column fixed="right" label="审核" width="120" align="center">
            <template #default="scope">
          <el-button link type="primary" size="small" @click="handleClick(scope.row)">{{ scope.row.audit ? '已审核' : '审核' }}</el-button>
          </template>
          </el-table-column> -->
        </el-table>     
        <el-table  v-loading="loading" :data="rateList" style="margin-top: 20px;margin-left: 20px; flex: 1;height: 750px;"  
          :header-cell-style="tableHeaderColor" class="custom-table">
          <el-table-column type="selection" width="55">
          </el-table-column>
          <el-table-column prop="disease" label="病种" align="center"></el-table-column>
          <el-table-column prop="indicator_name" label="规则名称" align="center"></el-table-column>
          <el-table-column prop="rate" label="达标率" align="center" min-width="68">
                <template #default="scope">
                    <span style="color: red">{{ scope.row.rate }}</span>
                </template>
            </el-table-column>
          <!-- <el-table-column prop="rate" label="达标率" align="center"></el-table-column> -->
        </el-table>    
      </div>
      <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 30, 40]"
          layout="sizes, prev, pager, next"
          :total="totalPage"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
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
            action="http://124.225.82.2:43210/"
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

      <el-dialog
        :visible.sync="dialogEdit"
        v-model="dialogEdit"
        title="审核"
        v-if="dialogEdit"
        width="40%"
      >
        <el-form :model="editFormData" ref="editForm" label-width="80px">
          <!-- 这里是你的表单项 -->
          <el-form-item label="是/否">
            <el-radio-group v-model="editFormData.yes_or_no">
              <el-radio :label="true" :checked="editFormData.yes_or_no != 0">是</el-radio>
              <el-radio :label="false" :checked="editFormData.yes_or_no == 0">否</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="结果">
            <el-input type="textarea" rows="4" v-model="editFormData.predict"></el-input>
          </el-form-item>
          </el-form>
          <span slot="footer" class="dialog-footer" style="display: flex; justify-content: center;">
            <el-button @click="dialogEdit = false">取 消</el-button>
            <el-button type="primary" @click="saveEdit">确 定</el-button>
        </span>
      </el-dialog>

      <el-dialog :visible.sync="dialogText" v-if="dialogText" v-model="dialogText" title="收费明细原文">
      <el-input v-model="textValue" type="textarea" rows="3" placeholder="请输入内容"></el-input>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleConfirm">确 定</el-button>
      </span>
    </el-dialog>
    </el-card>
    </div>
</template>
  
  <script setup>
  import { ref,onMounted } from 'vue';
  import { ElMessage, ElMessageBox } from 'element-plus';
  import sJson from '../sJson.vue';
  import axios from "axios";

  import request from '@/api/request';
  const fileInputRef = ref(null);
  const downloadUrl = ref('../../../../public/template.xlsx')

  const rateList = ref([])
  const dialogImport = ref(false)
  const dialogText = ref(false)
  const jsonData = ref('')
  const dialogPreviewJSON = ref(false)
  const dialogEdit = ref(false)
  const textValue = ref('')
  const tableHeaderColor = {
    background: ' #f5f5f5 !important',
    color: '#333333',
    fontSize: '14px',
    textAlign: 'center',
  }
  const hospitalDiseases = ref({})
  const type = ref('')
  const hospitalList = ref([])
  const hospital = ref('')
  const diseaseList = ref([])
  const disease = ref('')
  const indexList = ref([])
  const index = ref('')

  const fileList = ref([]);
  const uploadData = ref([]);
  const tableData = ref([]);
  const stockData = ref({})
  const uploadJson = ref([])
  const editFormData = ref({
    pass:true,
    result:'',
    id:''
  })
  const loading = ref(false);

//分页
const currentPage = ref(1);  
const pageSize = ref(10);  
const totalPage = ref(0)

  onMounted(() => {
      getOptionList()
  });

  const importData = () => {
    dialogImport.value = true;
  };

  const downloadTemplate = () => {  
      const link = document.createElement('a');  
      link.href = downloadUrl.value;  
      link.setAttribute('download', 'template.xlsx'); 
      document.body.appendChild(link);  
      link.click();  
      document.body.removeChild(link);  
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
        let jsonData = JSON.parse(e.target.result);
        
        // 打印JSON数据
        console.log(jsonData);
        uploadData.value = [];
        uploadData.value = JSON.parse(e.target.result);

        const data = uploadData.value
        const dataArray = Object.keys(data).map(key => ({
            emr_id: key,
            content: data[key]['content'],
            // reason: data[key]['reason']
        }));
        uploadJson.value = dataArray
        console.log(uploadJson._rawValue);
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
        stockData.value = JSON.stringify(uploadData.value);

        const data = stockData._rawValue
        console.log(data)
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

  const handleSizeChange = (val) => {  
    console.log(`每页 ${val} 条`);  
    pageSize.value = val;  
    currentPage.value = 1
    getNewList()
  };  

  const handleCurrentChange = (val) => {  
    console.log(`当前页: ${val}`);  
    currentPage.value = val; 
    getNewList() 
  };

  const loadFile = (num) => {
    loading.value = true
    request.get('/excel_count', {  
              params: {  
                hospital_name: '1院' ,
                file_num: num
              }  
            }).then(response => {  
              console.log(response);  
              if (response.success) {  
                getNewList()
                loading.value = false
              }  
            }).catch(error => {  
              console.error(error);  
              ElMessage({  
                type: "error",  
                message: "error",  
              });  
            });
  };

  const uploadFile = () => {
      // loading.value = true
      const file = fileInputRef.value.files[0]; // 使用fileInputRef.value访问$refs.fileInput的引用
      const formData = new FormData(); // 创建表单数据对象
      formData.append('file', file); // 将文件添加到表单数据对象中
      let intervalId;

      const apiUrl = 'http://localhost:43210/upload-excel/';
      axios.post(apiUrl, formData).then(response => {
          console.log(response.data)
          if(response.data.success) {
            ElMessage({
              type: "success",
              // message: response.data.message,
              message: "文件上传成功！"
            });
            response.data.bznameList.forEach(item => {
              diseaseList.value.push({
                label: item,
                value: item
              })
            });
            intervalId = setInterval(getNewList, 1000);
            request.get('/excel_count', {  
              params: {  
                hospital_name: hospital.value 
              }  
            }).then(response => {  
              console.log(response);  
              if (response.success) {  
                getNewList() 
                clearInterval(intervalId);
                // loading.value = false
              }  
            }).catch(error => {  
              console.error(error);  
              ElMessage({  
                type: "error",  
                message: "error",  
              });  
            });
          } else {
            ElMessage({
              type: "error",
              message: response.data.message,
            });
            loading.value = false
          }
        })
        .catch(error => {
          console.log(error)
        });
  };

  const getTarget = () => {
    loading.value = true
    const req = {
        'model': '申医-20b-vllm-banben',
        'disease_type': type.value,
        'disease': disease.value,
        'indicator_number': index.value,
        'hospital_name': hospital.value,
        'record': uploadJson._rawValue
    }
    console.log(req)
    request.post('/target_indicator_number', req).then(res => {
      console.log(res)
      // tableData.value = res.result.record
      getTableList()
      // res.result.rate.forEach(item => {
      //   rateList.value.push({
      //     disease: item.disease,
      //     indicator_name: item.indicator_name,
      //     rate: Number(item.rate*100).toFixed(0) + '%'
      //   })
      // })
      rateList.value = res.result.rate
      console.log(tableData.value)
      loading.value = false
    })
  }

  const getTableList = () => {
    const req = {  
    'page': currentPage.value,  
    'size': pageSize.value,  
    'disease': disease.value,  
    'hospital_name': hospital.value,  
    'disease_type': type.value,
    'indicator_number': index.value
    };  

    console.log(req);  
    const queryString = Object.keys(req).map(key => `${encodeURIComponent(key)}=${encodeURIComponent(req[key])}`).join('&');  
    const url = '/latest_records?' + queryString;   
    request.get(url).then(res => {  
    console.log(res);  
    totalPage.value = res.data_count;  
    tableData.value = res.total_list;  
    console.log(tableData.value);  
    }).catch(error => {  
      console.error('Error fetching data:', error);  
    });
  }

  const getNewList = () => {
    const req = {  
    'page': currentPage.value,  
    'size': pageSize.value,  
    // 'disease': disease.value,  
    'hospital_name': hospital.value,  
    // 'disease_type': type.value,
    // 'indicator_number': index.value
    };  

    console.log(req);  
    const queryString = Object.keys(req).map(key => `${encodeURIComponent(key)}=${encodeURIComponent(req[key])}`).join('&');  
    const url = '/latest_records_new?' + queryString;   
    request.get(url).then(res => {  
      console.log(res);  
      totalPage.value = res.data_count;  
      tableData.value = res.total_list;  
      console.log(tableData.value);  
    }).catch(error => {  
      console.error('Error fetching data:', error);  
    });
    request.get('/latest_rate_new?hospital_name=' + hospital.value).then(res => {  
      console.log(res)
      rateList.value = res.rates
      rateList.value.forEach(item => {
        item.rate = Number(item.rate*100).toFixed(0) + '%'
      })
      console.log(rateList.value)
    })
  }

  const handleClick = (row) => {
    console.log(row)
    const rowData = JSON.parse(JSON.stringify(row));
    dialogEdit.value = true
    editFormData.value.predict = rowData.predict
    editFormData.value.emr_id  = rowData.emr_id
    editFormData.value.yes_or_no = rowData.yes_or_no === '是' ? true : false
    editFormData.value.emr_result_id = rowData.emr_result_id
    editFormData.value.hospital_name = rowData.hospital_name
    editFormData.value.disease = rowData.disease
    editFormData.value.disease_type = rowData.disease_type
    editFormData.value.indicator_name = rowData.indicator_name
    editFormData.value.indicator_number = rowData.indicator_number
    editFormData.value.predict = rowData.predict
    editFormData.value.content = rowData.content
    editFormData.value.audit = rowData.audit

    console.log(editFormData.value)
    console.log('点击编辑按钮，当前行数据：', rowData);
}

  const handleText = (row) => {
    console.log(row)
    dialogText.value = true
    const rowData = JSON.parse(JSON.stringify(row));
    textValue.value = rowData.content
    console.log('点击编辑按钮，当前行数据：', rowData);
}

  const saveEdit = () => {
    const rowData = JSON.parse(JSON.stringify(editFormData.value));
    console.log(rowData)
    dialogEdit.value = false
    const req = {
      emr_result_id: rowData.emr_result_id,
      disease: rowData.disease,
      disease_type: rowData.disease_type,
      hospital_name: rowData.hospital_name,
      indicator_name: rowData.indicator_name,
      indicator_number: rowData.indicator_number,
      emr_id: rowData.emr_id,
      content: rowData.content,
      predict: editFormData.value.predict,
      yes_or_no: editFormData.value.yes_or_no == false ? 0 : 1,
      audit: 1
    }
    request.put('/update_emr_result', req).then(res => {
      console.log(res)
      getTableList()
    })
  }

  const tableReset = () => {
    hospital.value = ''
    disease.value = ''
    type.value = ''
    index.value = ''
  } 

  const getOptionList = () => {
    request.get('/hospital_diseases/').then(res => {
      console.log(res)
      hospitalDiseases.value = res
      Object.keys(res).forEach(key => {
        hospitalList.value.push({
          'label': key,
          'value': key
        })
      }
      )
    })
  }

  const hospitalChange = () => {
    diseaseList.value = []
    const list = hospitalDiseases.value[hospital.value]
    console.log(Object.keys(list))
    Object.keys(list).forEach(item => {
      diseaseList.value.push({
      'label': item,
      'value': item
      })
    })
    console.log(diseaseList.value)
  }

  const diseaseChange = () => {
    indexList.value = []
    indexList.value = hospitalDiseases.value[hospital.value][disease.value]
  }

</script>
<style scoped>
  
.container2 {
  width: 100%;
  height: 100%;
  font-family: 'PingFang';
  display: flex;  
  justify-content: center; 
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
  margin-left: 20px
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
#tableId .el-table__cell {
  text-align: center;
}
.el-tooltip__popper{
  max-width:20%
}
#tableId .el-table__cell {
  text-align: center;
}
.el-pagination {
  margin: 20px;
  margin-left: 60%;
  float: left;
}
.myButton{
  border-radius: 20px;
  width: 120px;
  
}
.custom-table{
    border-radius: 15px; /* 增加圆角 */
  }
  :deep(.el-table__row:nth-child(odd)) {
  background-color: #ffffff !important; /* 白色 */
}
:deep(.el-table__row:nth-child(even)) {
  background-color: #f5f5f5 !important; /* 淡灰色 */
}

</style>
  