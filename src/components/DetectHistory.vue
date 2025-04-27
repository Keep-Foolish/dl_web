<template>
  <n-card title="历史记录">
    <div v-if="allData.length === 0">
      <n-empty description="暂无历史记录">
        <template #icon>
          <n-icon>
            <IosAirplane />
          </n-icon>
        </template>
      </n-empty>
    </div>
    <div v-else>
      <div v-for="item in pagedData" :key="item.id" style="margin-bottom: 20px;">
        <n-card :title="item.title">
          <template #header-extra>
            ID: {{ item.id }}
          </template>
          {{ item.content }}
          <template #footer>
            底部信息
          </template>
          <template #action>
            <div style="display: flex; justify-content: flex-end; width: 100%; margin-top: -10px; margin-bottom: -10px;">
              <n-button type="success">
                下载
              </n-button>
            </div>
          </template>
        </n-card>
      </div>

      <div style="display: flex; justify-content: center; margin-top: 20px; margin-bottom: 40px;">
        <n-pagination
          v-model:page="page"
          :page-count="Math.ceil(allData.length / pageSize)"
          :page-size="pageSize"
        />
      </div>
    </div>
  </n-card>
</template>

<script setup>
import { ref, computed } from 'vue'
import { IosAirplane } from '@vicons/ionicons4'

const page = ref(1)
const pageSize = 3

const allData = ref(
  Array.from({ length: 200 }, (_, i) => ({
    id: i + 1,
    title: `卡片标题 #${i + 1}`,
    content: `这是第 ${i + 1} 条数据的内容。`
  }))
)

const pagedData = computed(() => {
  const start = (page.value - 1) * pageSize
  return allData.value.slice(start, start + pageSize)
})
</script>

<style lang="scss" scoped></style>
