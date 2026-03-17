# Tangerine Selenium Robot Tests

This suite mirrors the Tangerine UI checks from `pytest_demo/tests/ui/tangerine_selenium`.

## Includes

- Homepage title test
- Sign-in navigation title test
- Sign-up navigation title test
- Shared `Test Setup` that always opens the homepage and accepts cookies when banner is present

## Run

```powershell
robot -d temps/robot_tangerine_selenium robot_demos/tangerine_selenium
```

## Optional dry run (syntax only)

```powershell
robot --dryrun -d temps/robot_tangerine_selenium_dryrun robot_demos/tangerine_selenium
```

## Outputs

Robot output files are generated under `temps/robot_tangerine_selenium/`:

- `output.xml`
- `log.html`
- `report.html`

