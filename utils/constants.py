import os
from pathlib import Path
from typing import Final


def _env_int(name: str, default: int) -> int:
    """Read an integer from environment variables with a safe default."""
    value = os.getenv(name)
    if value is None:
        return default
    return int(value)


BASE_DIR: Final[Path] = Path(__file__).resolve().parents[1]
ALLURE_IMG_DIR: Final[Path] = BASE_DIR / "temps" / "allure-report" / "images"

SELENIUM_IMPLICIT_WAIT: Final[int] = _env_int("SELENIUM_IMPLICIT_WAIT", 10)
SELENIUM_EXPLICIT_WAIT: Final[int] = _env_int("SELENIUM_EXPLICIT_WAIT", 10)
SLEEP_TIME: Final[int] = _env_int("SLEEP_TIME", 1)

# Backward-compatible aliases (to be removed after call sites are migrated).
SELENIUM_IMPLICITLY_WAIT: Final[int] = SELENIUM_IMPLICIT_WAIT
SELENIUM_EXPLICITLY_WAIT: Final[int] = SELENIUM_EXPLICIT_WAIT

TANGERINE_URL: Final[str] = os.getenv(
    "TANGERINE_URL", "https://www.tangerine.ca/en/personal"
)
DEEP_SEEK_URL: Final[str] = os.getenv("DEEP_SEEK_URL", "https://api.deepseek.com")
OPENAI_URL: Final[str] = os.getenv("OPENAI_URL", "https://api.openai.com")
CINEPLEX_URL: Final[str] = os.getenv("CINEPLEX_URL", "https://connect.cineplex.com")


def print_configured_constants() -> None:
    """Print constants for quick local verification."""
    constant_names = [
        "BASE_DIR",
        "ALLURE_IMG_DIR",
        "SELENIUM_IMPLICIT_WAIT",
        "SELENIUM_EXPLICIT_WAIT",
        "SLEEP_TIME",
        "SELENIUM_IMPLICITLY_WAIT",
        "SELENIUM_EXPLICITLY_WAIT",
        "TANGERINE_URL",
        "DEEP_SEEK_URL",
        "OPENAI_URL",
        "CINEPLEX_URL",
    ]
    for name in constant_names:
        print(f"{name}={globals()[name]}")


if __name__ == "__main__":
    print_configured_constants()

