import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath, URL } from 'node:url';

export default defineConfig({
  plugins: [react()],
  base: '/visual-editor/',
  root: fileURLToPath(new URL('.', import.meta.url)),
  build: {
    outDir: '../public/visual-editor',
    emptyOutDir: true,
    sourcemap: false
  }
});
