from pathlib import Path
from typing import Final

from utils.config import settings

BASE_DIR: Final[Path] = Path(__file__).resolve().parents[1]
ALLURE_IMG_DIR: Final[Path] = BASE_DIR / "temps" / "allure-report" / "images"

SLEEP_TIME: Final[int] = settings.ui.sleep_time

TANGERINE_URL: Final[str] = settings.urls.tangerine
DEEP_SEEK_URL: Final[str] = settings.urls.deep_seek
OPENAI_URL: Final[str] = settings.urls.openai


def print_configured_constants() -> None:
    """Print constants for quick local verification."""
    constant_names = [
        "BASE_DIR",
        "ALLURE_IMG_DIR",
        "SLEEP_TIME",
        "TANGERINE_URL",
        "DEEP_SEEK_URL",
        "OPENAI_URL",
    ]
    for name in constant_names:
        print(f"{name}={globals()[name]}")


if __name__ == "__main__":
    print_configured_constants()
