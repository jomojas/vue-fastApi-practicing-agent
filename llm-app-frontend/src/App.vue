<script setup>
// 1. 导入你的聊天组件
import Chat from './components/Chat.vue'
</script>

<template>
  <div class="app-container">
    <header>
      <h1>我的 AI 助手</h1>
      <p>基于 FastAPI + Vue 3 + DeepSeek</p>
    </header>

    <main>
      <!-- 2. 直接像 HTML 标签一样使用它 -->
      <Chat />
    </main>

    <footer>
      <p>&copy; 2024 Jomo's LLM Project</p>
    </footer>
  </div>
</template>

<style>
/* 一些基础的全屏样式 */
body {
  margin: 0;
  font-family: Arial, sans-serif;
  background-color: #f4f7f6;
}

.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh; /* 撑满屏幕高度 */
}

header {
  background-color: #2c3e50;
  color: white;
  padding: 1rem;
  text-align: center;
}

header h1 {
  margin: 0;
  font-size: 1.5rem;
}

main {
  flex: 1; /* 占据剩余空间 */
  padding: 20px;
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: flex-start; /* 从顶部开始排列 */
}

footer {
  text-align: center;
  padding: 10px;
  color: #666;
  font-size: 0.8rem;
}
</style>
