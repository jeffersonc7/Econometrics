import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 30000,
  fullyParallel: false,
  workers: 1,
  reporter: 'list',
  use: {
    baseURL: 'http://127.0.0.1:4173',
    headless: true,
    launchOptions: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ? {executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH} : {},
    trace: 'retain-on-failure',
  },
  webServer: {
    command: 'python3 ../backend/server.py --port 4173',
    url: 'http://127.0.0.1:4173/health',
    reuseExistingServer: false,
  },
});
