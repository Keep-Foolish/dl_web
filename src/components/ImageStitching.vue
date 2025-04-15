<template>
  <n-card title="待拼接图片">
    <template #header-extra>
      <n-statistic label="已选择图片" :value="filesToUpload.length">
        <template #prefix>
          <n-icon>
            <SaveOutline />
          </n-icon>
        </template>
        <template #suffix>
          / 100
        </template>
      </n-statistic>
    </template>
    <n-upload action="https://www.mocky.io/v2/5e4bafc63100007100d8b70f" :default-file-list="previewFileList" multiple
      list-type="image-card" @preview="handlePreview" @change="handleFileChange" :max="100" />
    <n-modal v-model:show="showModal" preset="card" style="width: 600px">
      <img :src="previewImageUrl" style="width: 100%">
    </n-modal>
    <template #footer>
      请选择待拼接的无人机近地遥感图像（按住ctrl可一次选择多张图片）
    </template>
    <template #action>
      <div style="display: flex; justify-content: flex-end; width: 100%;">
        <n-button @click="uploadFile" type="primary">
          开始拼接
        </n-button>
      </div>
    </template>
  </n-card>
  <n-card title="倒伏检测结果" style="margin-top: 30px;">
    <n-empty description="暂未拼接" size="large">
    </n-empty>
    <template #action>
      <div style="display: flex; justify-content: flex-end; width: 100%;">
        <n-button type="primary" @click="saveImage">
          保存结果
        </n-button>
      </div>
    </template>
  </n-card>
</template>

<script setup>
import { ref } from 'vue'
import { SaveOutline } from '@vicons/ionicons5' // 新增导入


const showModal = ref(false)
const previewImageUrl = ref('')

const handlePreview = (file) => {
  const { url } = file
  previewImageUrl.value = url
  showModal.value = true
}

const filesToUpload = ref([]);
const handleFileChange = (data) => {
  // 更新待上传的文件列表（支持多选）
  filesToUpload.value = data.fileList.map(item => item.file);
  console.log("已选择文件列表:", filesToUpload.value);
}
</script>

<style lang="scss" scoped></style>
