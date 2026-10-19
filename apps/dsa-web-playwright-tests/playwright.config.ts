import {defineConfig, devices} from '@playwright/test';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {BACKEND_URL, resolveBackendCommand} from './backend-command';

const currentDir = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(currentDir, '../..');
const dsaWebDir = path.resolve(currentDir, '../dsa-web');

export default defineConfig({
    testDir: './e2e',
    outputDir: path.join(repoRoot, 'temps', 'dsa-web-ts-playwright'),
    fullyParallel: false,
    workers: 1,
    retries: process.env.CI ? 2 : 0,
    reporter: [
        ['list'],
        ['html', {
            outputFolder: path.join(repoRoot, 'temps', 'dsa-web-ts-playwright', 'html-report'),
            open: 'never',
        }],
    ],
    use: {
        baseURL: 'http://127.0.0.1:4173',
        locale: 'zh-CN',
        trace: 'on-first-retry',
        screenshot: 'only-on-failure',
        video: 'retain-on-failure',
    },
    webServer: [
        {
            command: resolveBackendCommand(repoRoot),
            cwd: repoRoot,
            env: {PYTHONIOENCODING: 'utf-8', PYTHONUNBUFFERED: '1'},
            url: `${BACKEND_URL}/api/v1/health`,
            reuseExistingServer: !process.env.CI && process.env.DSA_WEB_REUSE_BACKEND === '1',
            timeout: 120_000,
            stdout: 'pipe',
        },
        {
            command: 'npm run dev -- --host 127.0.0.1 --port 4173 --strictPort',
            cwd: dsaWebDir,
            url: 'http://127.0.0.1:4173',
            env: {DSA_WEB_API_PROXY_TARGET: BACKEND_URL},
            reuseExistingServer: false,
            timeout: 120_000,
            stdout: 'pipe',
        },
    ],
    projects: [
        {
            name: 'chromium',
            use: {...devices['Desktop Chrome']},
        },
    ],
});
