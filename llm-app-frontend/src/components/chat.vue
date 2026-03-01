<template>
  <div class="chat-container">
    <!-- 1. 消息展示区 -->
    <div class="message-list" ref="messageListRef">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="['message', msg.role]"
      >
        <div class="avatar">{{ msg.role === 'user' ? '我' : 'AI' }}</div>
        <div class="content">{{ msg.content }}</div>
      </div>
    </div>

    <!-- 2. 输入区 -->
    <div class="input-area">
      <textarea
        v-model="userInput"
        @keyup.enter.exact="sendMessage"
        placeholder="输入问题，Enter 发送..."
      ></textarea>
      <button :disabled="isStreaming" @click="sendMessage">
        {{ isStreaming ? '回答中...' : '发送' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'

const userInput = ref('')
const messages = ref([])
const isStreaming = ref(false)
const messageListRef = ref(null)

// 自动滚动到底部
const scrollToBottom = async () => {
  await nextTick()
  if (messageListRef.value) {
    messageListRef.value.scrollTop = messageListRef.value.scrollHeight
  }
}

const sendMessage = async () => {
  if (!userInput.value.trim() || isStreaming.value) return

  const userContent = userInput.value
  userInput.value = ''

  // 添加用户消息到列表
  messages.value.push({ role: 'user', content: userContent })

  // 添加一个空的 AI 消息占位
  messages.value.push({ role: 'assistant', content: '' })
  const aiMsgIndex = messages.value.length - 1

  isStreaming.value = true
  await scrollToBottom()

  try {
    // 使用原生 fetch 调用后端的 /api/chat/stream
    const response = await fetch('/api/chat/stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userContent })
    })

    if (!response.ok) throw new Error('网络请求失败')

    // 核心：处理流式数据
    const reader = response.body.getReader()
    const decoder = new TextDecoder()

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      // 解码二进制数据为文本
      const chunk = decoder.decode(value)

      // 实时追加内容到刚才那个 AI 消息对象中
      messages.value[aiMsgIndex].content += chunk

      // 随着文字变多，自动往上滚
      scrollToBottom()
    }
  } catch (error) {
    messages.value[aiMsgIndex].content = '出错了：' + error.message
  } finally {
    isStreaming.value = false
  }
}
</script>

<style scoped>
/* 简单的样式让它像个聊天框 */
.chat-container {
  display: flex;
  flex-direction: column;
  height: 80vh;
  max-width: 800px;
  margin: 0 auto;
  border: 1px solid #ddd;
}
.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f9f9f9;
}
.message {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}
.message.user {
  flex-direction: row-reverse;
}
.content {
  padding: 10px;
  border-radius: 8px;
  max-width: 70%;
  white-space: pre-wrap;
}
.user .content {
  background: #007bff;
  color: white;
}
.assistant .content {
  background: white;
  border: 1px solid #eee;
}
.input-area {
  padding: 20px;
  border-top: 1px solid #ddd;
  display: flex;
  gap: 10px;
}
textarea {
  flex: 1;
  height: 60px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>
