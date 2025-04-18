<template>
  <n-infinite-scroll style="height: 100%; overflow-y: auto;" :distance="10" @load="handleLoad">
    <div>
      <!-- 步骤条 -->
      <n-space vertical class="steps_container">
        <n-steps size="small" :current="Number(current)" :status="currentStatus">
          <n-step title="上传tif图像" description="请选择一张符合EPSG:32650投影坐标系的tif图像" />
          <n-step title="识别倒伏区域" description="正常区域将被标注为绿色，倒伏区域将被标注为红色" />
          <n-step title="计算倒伏面积" description="系统正在计算稻麦倒伏面积" />
          <n-step title="保存识别结果" description="点击底部保存按钮即可保存识别结果到本地" />
        </n-steps>
      </n-space>

      <!-- 上传区域 -->
      <div v-if="!imageUrl" class="upload_container">
        <n-upload
          multiple
          directory-dnd
          :max="1"
          accept=".tif"
          :default-upload="false"
          @change="handleChange"
          @preview="handlePreview"
          ref="uploadRef"
        >
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

      <!-- 图片预览 -->
      <div v-else class="image-preview">
        <div class="image-container">
          <n-image :src="imageUrl" alt="Uploaded Image" class="preview-image" />
        </div>
      </div>

      <!-- 结果展示卡片 -->
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

        <n-empty v-if="!imageUrl" description="请先选择图片" size="large" />

        <template #footer>
          <div style="display: flex; justify-content: flex-end; width: 100%;">
            <n-statistic label="倒伏数据" style="margin-right: 40px;">
              {{ lodging_area }}
            </n-statistic>
          </div>
        </template>

        <template #action>
          <div style="display: flex; justify-content: flex-end; width: 100%;">
            <n-button @click="uploadFile" type="primary">开始识别</n-button>
            <div style="width: 20px;" />
            <n-button type="primary" @click="resetSelection">重新选择</n-button>
            <div style="width: 20px;" />
            <n-button type="primary" @click="saveImage" :disabled="current !== 4">保存结果</n-button>
          </div>
        </template>
      </n-card>
    </div>
  </n-infinite-scroll>
</template>

<script setup>
import { ref } from "vue";
import * as tiff from "tiff";
import axios from "axios";
import { ArchiveOutline as ArchiveIcon } from "@vicons/ionicons5";
import { useDialog, useMessage } from "naive-ui";

const message = useMessage();
const dialog = useDialog();

const current = ref(1);
const currentStatus = ref("process");
const uploadRef = ref(null);
const fileToUpload = ref(null);
const imageUrl = ref(null);
const pngBlob = ref(null);
const lodging_area = ref("待检测");

const handleChange = async (data) => {
  if (data.fileList.length > 0) {
    fileToUpload.value = data.fileList[0].file;
    const arrayBuffer = await fileToUpload.value.arrayBuffer();

    const ifds = tiff.decode(arrayBuffer);
    const image = ifds[0];

    const canvas = document.createElement("canvas");
    canvas.width = image.width;
    canvas.height = image.height;
    const ctx = canvas.getContext("2d");
    const imgData = ctx.createImageData(image.width, image.height);

    const pixels = image.data;
    for (let i = 0; i < image.width * image.height; i++) {
      const offset = i * 4;
      imgData.data[offset] = pixels[offset];
      imgData.data[offset + 1] = pixels[offset + 1];
      imgData.data[offset + 2] = pixels[offset + 2];
      imgData.data[offset + 3] = 255;
    }
    ctx.putImageData(imgData, 0, 0);

    canvas.toBlob((blob) => {
      const pngFile = new File([blob], fileToUpload.value.name.replace(/\.[^/.]+$/, ".png"), {
        type: "image/png",
      });
      pngBlob.value = pngFile;
      imageUrl.value = URL.createObjectURL(pngFile);
    }, "image/png");
  } else {
    resetSelection();
  }
};

const resetSelection = () => {
  fileToUpload.value = null;
  pngBlob.value = null;
  imageUrl.value = null;
  uploadRef.value?.clear?.();
};

const handlePreview = (file) => {
  console.log("预览文件:", file);
};

const uploadFile = async () => {
  if (!pngBlob.value) {
    dialog.error({ title: "错误", content: "请先上传并转换.tif图像", positiveText: "确认" });
    return;
  }

  const formData = new FormData();
  formData.append("file", pngBlob.value);
  formData.append("originalName", fileToUpload.value.name);

  try {
    const res = await axios.post("http://127.0.0.1:5000/upload", formData);
    if (res.data.message) {
      message.success("识别成功");
      current.value = 4;
    }
  } catch (err) {
    console.error("上传失败:", err);
    dialog.error({ title: "上传失败", content: err.message, positiveText: "确认" });
  }
};

const saveImage = () => {
  if (!imageUrl.value) return;
  const a = document.createElement("a");
  a.href = imageUrl.value;
  a.download = pngBlob.value?.name || "result.png";
  a.click();
};
</script>

<style scoped lang="scss">
.upload_container {
  position: relative;
}

.steps_container {
  margin-bottom: 20px;
  margin-top: 10px;
}

.color_block_red,
.color_block_green {
  display: flex;
  height: 16px;
  width: 16px;
  margin-right: 4px;
}

.color_block_red {
  background-color: red;
}

.color_block_green {
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