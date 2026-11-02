import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  // Load all env vars (including those without VITE_ prefix from Render hosting)
  const env = loadEnv(mode, process.cwd(), "");
  const backendUrl =
    env.VITE_API_URL ||
    env.HOPE_BACKEND_URL ||
    env.BACKEND_URL ||
    env.API_URL ||
    "https://hope-9dq5.onrender.com";

  return {
    plugins: [react()],
    define: {
      "__BACKEND_URL__": JSON.stringify(backendUrl),
    },
    server: {
      port: 5173,
      proxy: {
        "/api": {
          target: "http://127.0.0.1:8000",
          changeOrigin: true,
        },
      },
    },
  };
});
