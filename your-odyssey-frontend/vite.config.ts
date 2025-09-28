import { reactRouter } from "@react-router/dev/vite";
import { defineConfig } from "vite";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
  plugins: [
    reactRouter(), 
    tsconfigPaths()
  ],
  resolve: {
    alias: {
      '~': '/app'
    }
  },
  css: {
    devSourcemap: false // Disable CSS source maps in development
  }
});
