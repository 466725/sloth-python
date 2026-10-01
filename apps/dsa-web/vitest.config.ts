import { configDefaults, defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/setupTests.ts',
    exclude: [...configDefaults.exclude, 'e2e/**', 'playwright.config.ts'],
    // Default 5s is too tight under CPU contention from parallel test workers / other dev processes.
    testTimeout: 15000,
    hookTimeout: 15000,
  },
});
