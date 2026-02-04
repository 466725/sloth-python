import subprocess
from pathlib import Path
from shutil import which, rmtree

import pytest


def main() -> int:
    # Paths resolved relative to this file (stable regardless of CWD)
    here = Path(__file__).resolve().parent
    project_root = here.parent

    # Prefer repo-root pytest.ini; fall back to the local one if present
    ini_path = project_root / "pytest.ini"
    if not ini_path.is_file():
        ini_path = here / "pytest.ini"

    if not ini_path.is_file():
        print(
            "Could not find pytest.ini.\n"
            f"Looked in:\n  - {project_root / 'pytest.ini'}\n  - {here / 'pytest.ini'}\n"
            "Fix: place pytest.ini in one of these locations or update main_test.py to point to it."
        )
        return 2

    # Force ALL output under PROJECT ROOT (no dependence on current working directory)
    results_dir = project_root / "temps"
    report_dir = results_dir / "allure-report"
    log_dir = report_dir / "log"
    log_file = log_dir / "pytest.log"

    log_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)

    # Run tests once and preserve the real test exit code.
    # Override ini addopts that use relative paths by providing absolute ones here.
    pytest_exit_code = pytest.main(
        [
            "-c",
            str(ini_path),
            "--alluredir",
            str(results_dir),
            "--clean-alluredir",
            "-o",
            f"log_file={log_file}",
        ]
    )

    allure_cmd = which("allure")
    if not allure_cmd:
        print(
            "Allure CLI was not found on PATH, so the HTML report cannot be generated.\n"
            f"Pytest exit code: {pytest_exit_code}\n"
            f"Expected allure results directory: {results_dir}\n"
        )
        return int(pytest_exit_code)

    # Clean report output but keep the pytest log folder/file
    report_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    for child in report_dir.iterdir():
        if child.name == "log":
            continue
        if child.is_dir():
            rmtree(child, ignore_errors=True)
        else:
            try:
                child.unlink(missing_ok=True)
            except OSError:
                pass

    try:
        subprocess.run(
            [allure_cmd, "generate", "-o", str(report_dir), str(results_dir)],
            check=True,
            shell=False,
        )
        print(f"Allure report generated at: {report_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Allure report generation failed (exit code {e.returncode}).")
        return int(pytest_exit_code)

    return int(pytest_exit_code)


if __name__ == "__main__":
    raise SystemExit(main())