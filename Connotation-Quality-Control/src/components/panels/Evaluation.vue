<template>
    <div class="container">
      <div class="top-bar">
        <el-select
          v-model="selectedOptions"
          multiple
          collapse-tags
          collapse-tags-tooltip
          :max-collapse-tags="3"
          placeholder="请选择数据集"
          style="width: 200px"
        >
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
        <el-select v-model="selectedValue" placeholder="请选择模型" style="margin-left: 20px; width: 120px;">
          <el-option label="chatglm" value="1" />
          <el-option label="chatgpt" value="2" />
          <el-option label="qwen" value="3" />
        </el-select>
        <el-upload
            class="upload-demo"
            action="https://jsonplaceholder.typicode.com/posts/"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :before-remove="beforeRemove"
            :before-upload="beforeUpload"
            multiple
            :limit="1"
            :on-exceed="handleExceed">
            <el-button size="primary" type="primary" style="margin-left: 10px;">导入数据</el-button>
            <!-- <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div> -->
        </el-upload>
        <el-button type="primary" style="margin-left: 10px;" @click="handleReset">确定</el-button>
        <el-button type="primary" style="margin-left: 10px;" @click="handleDelete">结果导出</el-button>
      </div>
      <el-table :data="tableData" style="margin-top: 20px;">
        <el-table-column prop="data" label=""></el-table-column>
        <el-table-column prop="dataset1" label="数据集（ACC）"></el-table-column>
        <el-table-column prop="dataset2" label="数据集（F1）"></el-table-column>
      </el-table>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { ElMessage } from 'element-plus';
  const props = { multiple: true }
  // 级联选择器的选项数据
  const options = ref([
    {
      value: 'cblue',
      label: 'cblue',
    },
    {
      value: 'belle',
      label: 'belle',
    }
  ]);
  
  // 级联选择器的选中值
  const selectedOptions = ref([]);
  
  // 下拉菜单选中的值
  const selectedValue = ref('');
  
  // 表格数据
  const tableData = ref([
    { data: 'chatglm3', dataset1: '', dataset2: ''},
  ]);
  
  // 处理搜索按钮点击事件
  const handleSearch = () => {
    // 这里可以根据选中的级联选择器和下拉菜单的值进行搜索操作
    console.log('搜索按钮点击');
  };
  
  // 处理重置按钮点击事件
  const handleReset = () => {
    selectedOptions.value = [];
    selectedValue.value = '';
  };
  
  // 处理删除按钮点击事件
  const handleDelete = () => {
    // 这里可以根据选中的数据进行删除操作
    console.log('删除按钮点击');
  };
  
  // 处理上传成功
  const handleUploadSuccess = (response, file, fileList) => {
    console.log('上传成功', response, file, fileList);
  };
  
  // 处理上传失败
  const handleUploadError = (err, file, fileList) => {
    console.error('上传失败', err, file, fileList);
  };
  
  // 上传前处理
  const beforeUpload = (file) => {
    const isJSON = /\.json$/.test(file.name);
    console.log(isJSON)
    if (!isJSON) {
      ElMessage({
        message: '只能上传json文件',
        type: 'warning',
      })
    }
    return isJSON;
  };
  </script>
  
  <style>
  .container {
  }
  
  .top-bar {
    display: flex;
    align-items: center;
    margin: 5px 0;
  }
  </style>
  