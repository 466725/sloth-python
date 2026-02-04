import subprocess
import sys
from pathlib import Path
from shutil import which

import pytest


def main() -> int:
    # Run tests first and preserve the real test exit code
    pytest_exit_code = pytest.main()

    # Paths resolved relative to this file (stable regardless of CWD)
    here = Path(__file__).resolve().parent
    results_dir = here / "temps"
    report_dir = results_dir / "allure-report"
    results_dir.mkdir(parents=True, exist_ok=True)

    allure_cmd = which("allure")
    if not allure_cmd:
        print(
            "Allure CLI was not found on PATH, so the HTML report cannot be generated.\n"
            f"Pytest exit code: {pytest_exit_code}\n"
            f"Expected allure results directory: {results_dir}\n"
            "If you want report generation, ensure the 'allure' command is available in your terminal."
        )
        return int(pytest_exit_code)

    try:
        subprocess.run(
            [allure_cmd, "generate", str(results_dir), "-o", str(report_dir), "--clean"],
            check=True,
            shell=False,
        )
        print(f"Allure report generated at: {report_dir}")
    except subprocess.CalledProcessError as e:
        # Allure exists but failed; keep pytest's exit code as the primary signal
        print(f"Allure report generation failed (exit code {e.returncode}).")
        return int(pytest_exit_code)

    return int(pytest_exit_code)


if __name__ == "__main__":
    raise SystemExit(main())