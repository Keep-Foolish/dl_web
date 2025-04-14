<template>
  <div>
    <n-space vertical class="steps_container">
      <n-steps size="small" :current="Number(current)" :status="currentStatus">
        <n-step title="上传tif图像" description="请选择一张符合EPSG:32650投影坐标系的tif图像" />
        <n-step title="识别倒伏区域" description="正常区域将被标注为绿色，倒伏区域将被标注为红色" />
        <n-step title="计算倒伏面积" description="系统正在计算稻麦倒伏面积" />
        <n-step title="保存识别结果" description="点击底部保存按钮即可保存识别结果到本地" />
      </n-steps>
    </n-space>
    <div class="upload_container">
      <n-upload multiple directory-dnd :max="1" accept=".png" :default-upload="false" @change="handleChange"
        @preview="handlePreview" ref="uploadRef">
        <n-upload-dragger>
          <div style="margin-bottom: 12px">
            <n-icon size="48" :depth="3">
              <ArchiveIcon />
            </n-icon>
          </div>
          <n-text style="font-size: 16px">
            点击或者拖动文件到该区域来上传
          </n-text>
        </n-upload-dragger>
      </n-upload>
      <n-button @click="uploadFile" type="primary" style="margin-top: 12px;position: absolute;right: 0px;">
        开始识别
      </n-button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from 'axios';
import { ArchiveOutline as ArchiveIcon } from "@vicons/ionicons5";
import { MdArrowRoundBack, MdArrowRoundForward } from "@vicons/ionicons4";
import { useDialog, useMessage } from "naive-ui";

const message = useMessage();
const dialog = useDialog();


const current = ref(1);
const currentStatus = ref("process");

const responseData = ref(null); // 新增：存储后端返回的数据
const uploadRef = ref(null);
const fileToUpload = ref(null);

const next = () => {
  if (current.value === null) {
    current.value = 1;
  } else if (current.value >= 5) {
    current.value = null;
  } else {
    current.value++;
  }
};

const prev = () => {
  if (current.value === 0) {
    current.value = null;
  } else if (current.value === null) {
    current.value = 5;
  } else {
    current.value--;
  }
};

const handleChange = (data) => {
  if (data.fileList.length > 0) {
    fileToUpload.value = data.fileList[0].file;
    console.log("已选择文件:", fileToUpload.value);
  } else {
    fileToUpload.value = null;
  }
};

const handlePreview = (file) => {
  console.log("预览文件:", file);
};

const uploadFile = async () => {
  if (!fileToUpload.value) {
    dialog.error({
      title: "错误",
      content: "请先选择.tif格式的图像",
      positiveText: "确认",
    });
    return;
  }

  const formData = new FormData();
  formData.append('file', fileToUpload.value);

  try {
    const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    if (response.data.message) {
      console.log('文件上传成功', response.data.message);
      current.value = 2

      // 上传成功后清空文件选择
      uploadRef.value.clear();
      fileToUpload.value = null;
    } else {
      console.log('文件上传失败');
    }
  } catch (error) {
    console.error('上传错误:', error);
  }
};
</script>
<style lang='scss' scoped>
.upload_container {
  position: relative;
}

.steps_container {
  margin-bottom: 20px;
  margin-top: 10px;
}
</style>
