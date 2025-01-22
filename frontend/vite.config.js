import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host:"0.0.0.0",
    cors:true,
    headers:'Access-Control-Allow-Headers',
    port:"5174"
  }
})
