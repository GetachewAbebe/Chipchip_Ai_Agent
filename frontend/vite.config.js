import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    // Specific build configurations if needed
    rollupOptions: {
      // Custom Rollup options
    }
  }
})
