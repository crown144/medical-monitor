<template>
    <!-- 弹出框 -->
    <el-dialog
      title="电子病历预览"
      v-model="openPdf"
      @close="onClose"
      :close-on-click-modal="false"
      width="1050px"
    >
    <!-- 预览pdf文件 -->
      <embed
        src="../../public/21379345a.pdf"
        type="application/pdf"
        width="1010px"
        height="600px"
      />
    </el-dialog>
  </template>
  
  <script setup name="showPdf">
  import { ref, reactive, computed, watch, getCurrentInstance } from "vue";
  const { proxy } = getCurrentInstance();
  // 是否打开弹窗
  const openPdf = ref(false);
  
  const props = defineProps({
    openPdf:{
      type:Boolean
    },
    uuid:{
      type:String
    },
    title:{
      type:String
    }
  })
  // 关闭弹窗
  const onClose =()=>{
    openPdf.value = false;
  }
  </script>
  
  <style lang="scss" scoped></style>
  
  