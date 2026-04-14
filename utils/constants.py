from pathlib import Path
from typing import Final

BASE_DIR: Final[Path] = Path(__file__).resolve().parents[1]
ALLURE_IMG_DIR: Final[Path] = BASE_DIR / "temps" / "allure-report" / "images"


def print_configured_constants() -> None:
    """Print constants for quick local verification."""
    constant_names = [
        "BASE_DIR",
        "ALLURE_IMG_DIR",
    ]
    for name in constant_names:
        print(f"{name}={globals()[name]}")


if __name__ == "__main__":
    print_configured_constants()
