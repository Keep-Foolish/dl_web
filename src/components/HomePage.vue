<template>
  <div v-html="readmeContent" class="readme-container"></div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { marked } from 'marked';

export default {
  name: 'Readme',
  setup() {
    const readmeContent = ref('');

    // 在组件挂载时加载 README.md 文件
    onMounted(() => {
      fetch('/README.md')
        .then(response => response.text())
        .then((markdown) => {
          // 将 Markdown 转换为 HTML
          readmeContent.value = marked(markdown);
        })
        .catch((error) => {
          console.error('加载 README.md 时出错:', error);
        });
    });

    return {
      readmeContent,
    };
  },
};
</script>

<style scoped>
.readme-container {
  font-family: Arial, sans-serif;
  line-height: 1.6;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
}
</style>
