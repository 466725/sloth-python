import {expect, test} from '@playwright/test';
import path from 'node:path';
import {BACKEND_PORT, resolveBackendCommand} from '../backend-command';

const repoRoot = path.resolve('repo with spaces');

test.describe('backend startup command', () => {
    test('preserves an explicit command override', () => {
        expect(resolveBackendCommand(repoRoot, {
            env: {DSA_WEB_SMOKE_BACKEND_CMD: 'custom-backend'},
        })).toBe('custom-backend');
    });

    for (const platform of ['win32', 'darwin', 'linux'] as const) {
        const pythonParts = platform === 'win32' ? ['Scripts', 'python.exe'] : ['bin', 'python'];

        test(`${platform}: prefers the activated environment and quotes its path`, () => {
            const activeEnv = path.resolve('active environment');
            const python = path.join(activeEnv, ...pythonParts);
            const command = resolveBackendCommand(repoRoot, {
                env: {VIRTUAL_ENV: activeEnv},
                platform,
                existsSync: () => true,
            });
            expect(command).toBe(`"${python}" main.py --webui-only --host 127.0.0.1 --port ${BACKEND_PORT}`);
        });

        for (const name of ['.venv', '.venv314']) {
            test(`${platform}: discovers ${name} without an activated environment`, () => {
                const python = path.join(repoRoot, name, ...pythonParts);
                const command = resolveBackendCommand(repoRoot, {
                    env: {},
                    platform,
                    existsSync: (candidate) => candidate === python,
                });
                expect(command).toBe(`"${python}" main.py --webui-only --host 127.0.0.1 --port ${BACKEND_PORT}`);
            });
        }
    }

    test('uses PATH when no virtual environment exists', () => {
        expect(resolveBackendCommand(repoRoot, {
            env: {},
            existsSync: () => false,
        })).toBe(`python main.py --webui-only --host 127.0.0.1 --port ${BACKEND_PORT}`);
    });
});
