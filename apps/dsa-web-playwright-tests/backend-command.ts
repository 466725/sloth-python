import fs from 'node:fs';
import path from 'node:path';

export const BACKEND_PORT = 18000;
export const BACKEND_URL = `http://127.0.0.1:${BACKEND_PORT}`;

export function resolveBackendCommand(
  repoRoot: string,
  {
    env = process.env,
    platform = process.platform,
    existsSync = fs.existsSync,
  }: {
    env?: NodeJS.ProcessEnv;
    platform?: NodeJS.Platform;
    existsSync?: typeof fs.existsSync;
  } = {},
): string {
  if (env.DSA_WEB_SMOKE_BACKEND_CMD) {
    return env.DSA_WEB_SMOKE_BACKEND_CMD;
  }

  const pythonParts = platform === 'win32' ? ['Scripts', 'python.exe'] : ['bin', 'python'];
  const environments = [env.VIRTUAL_ENV, path.join(repoRoot, '.venv'), path.join(repoRoot, '.venv311')];
  for (const environment of environments) {
    if (!environment) {
      continue;
    }
    const python = path.join(environment, ...pythonParts);
    if (existsSync(python)) {
      return `"${python}" main.py --webui-only --host 127.0.0.1 --port ${BACKEND_PORT}`;
    }
  }

  return `python main.py --webui-only --host 127.0.0.1 --port ${BACKEND_PORT}`;
}
