# Environment Variable Examples

This folder contains example environment files for the `sloth-python` project.
They use placeholder values only. Keep real secrets in your own local files, such as
`.env/local.env`, which remain ignored by git.

## Available Examples

- `local.env.example` - common local development settings.
- `test.env.example` - values useful when running pytest, Robot Framework, or Playwright demos.
- `ai-generation.env.example` - values for AI-assisted Playwright test generation.
- `load_env_example.py` - a small `python-dotenv` loading example.

## PowerShell Usage

Copy an example to a local file:

```powershell
Copy-Item .env\local.env.example .env\local.env
```

Load the values into the current PowerShell session:

```powershell
Get-Content .env\local.env | ForEach-Object {
    if ($_ -match '^\s*#' -or $_ -notmatch '=') { return }
    $name, $value = $_ -split '=', 2
    [Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim(), 'Process')
}
```

Verify the project settings:

```powershell
python utils\config.py
```

## Python Usage

The project already depends on `python-dotenv`, so scripts can load a file before
importing `utils.config`:

```python
from dotenv import load_dotenv

load_dotenv(".env/local.env")

from utils.config import settings

print(settings.ui.base_url)
```

`utils.config.settings` is created when the module is imported, so call
`load_dotenv(...)` before importing settings.
