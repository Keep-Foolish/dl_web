<template>
  <n-infinite-scroll style="height: 100%;overflow-y: auto;" :distance="10" @load="handleLoad">

    <div>
      <n-space vertical class="steps_container">
        <n-steps size="small" :current="Number(current)" :status="currentStatus">
          <n-step title="上传tif图像" description="请选择一张符合EPSG:4326投影坐标系的tif图像" />
          <n-step title="识别倒伏区域" description="正常区域将被标注为绿色，倒伏区域将被标注为红色" />
          <n-step title="计算倒伏面积" description="系统正在计算稻麦倒伏面积" />
          <n-step title="保存识别结果" description="点击底部保存按钮即可保存识别结果到本地" />
        </n-steps>
      </n-space>
      <div v-if="!imageUrl" class="upload_container">
        <n-upload multiple directory-dnd :max="1" accept=".jpg,.tif" :default-upload="false" @change="handleChange"
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
      </div>

      <!-- 展示选择的图片 -->
      <div v-else class="image-preview">
        <div class="image-container">
          <n-image :src="imageUrl" alt="Uploaded Image" class="preview-image" />
        </div>
      </div>

      <div>
        <n-card title="倒伏检测结果" class="result-card">
          <template #header-extra>
            <div style="display: flex;">
              <div style="display: flex; margin-right: 10px;">
                <div class="color_block_red"></div>正常区域
              </div>
              <div style="display: flex;">
                <div class="color_block_green"></div>倒伏区域
              </div>
            </div>
          </template>
          <n-empty description="请先选择图片" size="large">
          </n-empty>
          <template #footer>
            <div style="display: flex; justify-content: flex-end; width: 100%;">
              <n-statistic label="倒伏数据" style="margin-right: 40px;">
                {{ lodging_area }}
              </n-statistic>
            </div>
          </template>
          <template #action>
            <div style="display: flex; justify-content: flex-end; width: 100%;">
              <n-button @click="uploadFile" type="primary">
                开始识别
              </n-button>
              <div style="width: 20px;"> </div>
              <n-button type="primary" @click="saveImage" :disabled="current !== 4">
                重新选择
              </n-button>
              <div style="width: 20px;"> </div>
              <n-button type="primary" @click="saveImage" :disabled="current !== 4">
                保存结果
              </n-button>
            </div>
          </template>
        </n-card>
      </div>
    </div>
  </n-infinite-scroll>
</template>

<script setup>
import { ref } from "vue";
import { config } from '../config.js'; // 导入配置文件
import axios from 'axios';
import { ArchiveOutline as ArchiveIcon } from "@vicons/ionicons5";
import { MdArrowRoundBack, MdArrowRoundForward } from "@vicons/ionicons4";
import { useDialog, useMessage } from "naive-ui";

const message = useMessage();
const dialog = useDialog();

// 顶部进度栏
const current = ref(4); //记录当前在哪一步
const currentStatus = ref("process"); //记录这一步的状态

const responseData = ref(null); // 新增：存储后端返回的数据
const uploadRef = ref(null);
const fileToUpload = ref(null); //保存选择的文件

// 倒伏面积
const lodging_area = ref('待检测')
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

// 新增：生成图片预览 URL
const imageUrl = ref(null);

const handleChange = (data) => {
  if (data.fileList.length > 0) {
    fileToUpload.value = data.fileList[0].file;
    // 生成图片 URL 用于预览
    imageUrl.value = URL.createObjectURL(fileToUpload.value);
    console.log("已选择文件:", fileToUpload.value);
  } else {
    fileToUpload.value = null;
    imageUrl.value = null; // 清空图片预览
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
  console.log(fileToUpload.value)

  try {
    const response = await axios.post(`${config.apiUrl}/upload`, formData, {
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
      imageUrl.value = null; // 上传后清空图片预览

    } else {
      console.log('文件上传失败');
    }

  } catch (error) {
    console.error('上传错误:', error);
  }
};

const saveImage = () => {
  message.success("保存成功")
}
</script>

<style lang='scss' scoped>
.upload_container {
  position: relative;
}

.steps_container {
  margin-bottom: 20px;
  margin-top: 10px;
}

.color_block_red {
  display: flex;
  height: 16px;
  width: 16px;
  margin-right: 4px;
  background-color: red;
}

.color_block_green {
  display: flex;
  height: 16px;
  width: 16px;
  margin-right: 4px;
  background-color: green;
}

.image-preview {
  margin-top: 20px;
  text-align: center;
}

.result-card {
  margin-bottom: 50px;
}
</style>