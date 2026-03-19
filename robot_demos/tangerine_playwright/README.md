# Tangerine Playwright Robot Tests

This suite mirrors the Tangerine UI checks from `pytest_demo/tests/ui/tangerine_playwright`.

## Includes

- Homepage title test
- Sign-in navigation title test
- Sign-up navigation title test
- Shared `Test Setup` that always opens the homepage and accepts cookies when banner is present

## Self-healing scope

- Enabled only for these locator keys in Robot Playwright keywords:
  - `tangerine.login`
  - `tangerine.signup`
- Locator definitions are shared from `pytest_demo/locators/locators.json`
- Robot mode currently runs with read-only healing (`auto_update=False`)

## Run

```powershell
robot -d temps/robot_tangerine_playwright robot_demos/tangerine_playwright
```

## Optional dry run (syntax only)

```powershell
robot --dryrun -d temps/robot_tangerine_playwright_dryrun robot_demos/tangerine_playwright
```

## Outputs

Robot output files are generated under `temps/robot_tangerine_playwright/`:

- `output.xml`
- `log.html`
- `report.html`

