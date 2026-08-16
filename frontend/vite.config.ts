import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: true,
    allowedHosts: ['luka-mosala-web.onrender.com', 'client-luka-mosala.onrender.com', '.onrender.com', 'all'],
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
  preview: {
    host: true,
    allowedHosts: ['luka-mosala-web.onrender.com', 'client-luka-mosala.onrender.com', '.onrender.com', 'all'],
  },
});
