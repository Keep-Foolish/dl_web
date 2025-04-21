<template>
  <n-infinite-scroll style="height: 100%;overflow-y: auto;" :distance="10" @load="handleLoad">

    <div>
      <n-space vertical class="steps_container">
        <n-steps size="small" :current="Number(current)" :status="currentStatus">
          <n-step title="上传tif图像" description="请选择一张符合EPSG:4326投影坐标系的tif图像" />
          <n-step title="识别倒伏区域" description="正常区域将被标注为绿色，倒伏区域将被标注为红色" />
          <n-step title="保存识别结果" description="点击底部保存按钮即可保存识别结果到本地" />
        </n-steps>
      </n-space>
      <div class="upload_container">
        <n-upload multiple directory-dnd :max="1" accept=".jpg,.tif" :default-upload="true" @change="handleChange"
          @preview="handlePreview" ref="uploadRef" :action="config.apiUrl + '/upload'"
          :custom-request="customUploadRequest">
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
          <n-empty v-if="imageUrl == null" description="请先选择图片" size="large" />
          <div v-else class="result_image_container">
            <n-image :src="rgb_image_url" :height="400" />
            <n-image :src="imageUrl" :height="400" />
          </div>
          <template #footer>
            <div style="display: flex; justify-content: flex-end; width: 100%;">
              <n-statistic label="倒伏数据" style="margin-right: 40px;white-space: pre;">
                {{ lodging_area }}
              </n-statistic>
            </div>
          </template>
          <template #action>
            <div style="display: flex; justify-content: flex-end; width: 100%;">
              <n-button @click="startPredict(tifUploadInfo)" type="info" :disabled="startPredictButton && current == 1">
                开始识别
              </n-button>
              <div style="width: 20px;"> </div>
              <div style="width: 20px;"> </div>
              <n-button type="primary"
                @click="saveFilesAsZip(rgb_image_url, imageUrl, predictiveData, tifUploadInfo.png_filename)"
                :disabled="current !== 3">
                保存结果
              </n-button>
              <div style="width: 20px;"> </div>
              <div style="width: 20px;"> </div>
              <n-button type="warning" @click="refreshPage" :disabled="current !== 3">重新选择</n-button>
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
import { useLoadingBar } from 'naive-ui'
import { ArchiveOutline as ArchiveIcon } from "@vicons/ionicons5";
import { useDialog, useMessage } from "naive-ui";
import { load } from '../untils/loading.js';
import { saveFilesAsZip } from '../untils/download.js'

const message = useMessage();
const dialog = useDialog();
const loadingBar = useLoadingBar()
const disabled = ref(true)
const predictiveData = ref(null)

//开始识别按钮
const startPredictButton = ref(true)

const handleStart = () => {
  loadingBar.start()
  disabled.value = false
}

const handleFinish = () => {
  loadingBar.finish()
  disabled.value = true
}

const handleError = () => {
  disabled.value = true
  loadingBar.error()
}
// 顶部进度栏
const current = ref(1); //记录当前在哪一步
const currentStatus = ref("process"); //记录这一步的状态

const responseData = ref(null); //存储后端返回的数据
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

// 自动上传
let tifUploadInfo = null;
const customUploadRequest = async ({ file, onProgress, onFinish, onError }) => {
  handleStart();
  console.log("正在自动上传tif文件:", file);

  const formData = new FormData();
  formData.append('file', fileToUpload.value);

  try {
    const response = await axios.post(`${config.apiUrl}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    // 后端返回数据的状态检查
    if (response.data && response.data.message) {
      const responseMessage = response.data.message;

      // 检查是否是图像坐标参考系统（CRS）不符合要求的错误
      if (responseMessage.includes("坐标参考系统（CRS）不符合要求") || responseMessage.includes("上传的图像坐标参考系统（CRS）不符合要求")) {
        handleError(); // 进度条错误处理
        onError(); // 上传失败回调
        message.error(responseMessage || "上传的图像不符合要求");
        return;
      }

      // 其他错误信息
      handleError(); // 进度条错误处理
      onError(); // 上传失败回调
      message.error(responseMessage || "上传过程中发生错误");
      return;
    }

    // 如果没有错误信息，说明上传成功
    tifUploadInfo = response.data.params;
    current.value = 2;
    console.log("上传成功，服务器响应:", response.data.params);
    startPredictButton.value = false;

    handleFinish(); // 上方进度条
    message.success("tif图像上传成功");
    onFinish(); // 上传成功回调

  } catch (error) {
    console.error("上传错误:", error);
    handleError(); // 进度条错误处理
    onError(); // 上传失败回调
    message.error("上传过程中发生错误");
  }
};


// 开始识别
const rgb_image_url = ref(null) //原图url
const imageUrl = ref(null)
const startPredict = async (tifUploadInfo) => {
  if (!startPredictButton.value) {
    dialog.warning("识别结果已返回，请自行保存。")
  } else {
    console.log("开始识别", tifUploadInfo);
    try {
      // 1. 发送预测请求获取元数据和图片URL
      load.show("识别中，请稍候...");
      const predictResponse = await axios.post(
        `${config.apiUrl}/predict`,
        tifUploadInfo,
        {
          headers: { 'Content-Type': 'application/json' },
          responseType: 'json'
        }
      );

      current.value = 3

      console.log('元数据:', predictResponse.data.json);

      // 2. 存储元数据
      predictiveData.value = predictResponse.data.json;
      const lodgingRatio =
        predictiveData.value.area_analysis.lodged_area_m2 /
        (predictiveData.value.area_analysis.lodged_area_m2 +
          predictiveData.value.area_analysis.healthy_area_m2);
      const lodgingRatioPercent = (lodgingRatio * 100).toFixed(2) + '%';

      // 渲染数据
      lodging_area.value =
        `倒伏区域：${predictiveData.value.area_analysis.lodged_area_m2}㎡    正常区域：${predictiveData.value.area_analysis.healthy_area_m2}㎡    倒伏比例：${lodgingRatioPercent}`;

      // 请求图片
      let imagePath = predictResponse.data.seg_image_url
      rgb_image_url.value = `${config.apiUrl}/download_image?image_path=${encodeURIComponent(predictResponse.data.rgb_image_url)}`;
      imageUrl.value = `${config.apiUrl}/download_image?image_path=${encodeURIComponent(imagePath)}`;
      console.log("imageUrl.value", imageUrl.value)
      load.hide()

    } catch (error) {
      console.error('请求失败:', error);
      // 可以添加用户提示
      alert(`识别失败: ${error.response?.data?.message || error.message}`);
    }
  }
};

const refreshPage = () => {
  window.location.reload(); // 刷新页面
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


.result-card {
  margin-bottom: 50px;
}

.result_image_container {
  display: flex;
  justify-content: space-around;
}
</style>