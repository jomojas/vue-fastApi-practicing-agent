import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      // 只要请求路径以 /api 开头，就转发到后端，注意：不是'/api'替换'http://127.0.0.1:8080'
      '/api': {
        target: 'http://127.0.0.1:8080',
        changeOrigin: true
        // 如果后端接口没有 /api 前缀，可以开启下面的重写
        // rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
