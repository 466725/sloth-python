from __future__ import annotations

from pathlib import Path
import sys

try:
    from dotenv import load_dotenv
except ImportError as exc:
    raise SystemExit(
        "python-dotenv is required for this example. "
        "Install project dependencies with: pip install -r requirements.txt"
    ) from exc


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = PROJECT_ROOT / ".env" / "local.env"
sys.path.insert(0, str(PROJECT_ROOT))


def main() -> None:
    load_dotenv(ENV_FILE)

    from utils.config import print_configured_settings

    print_configured_settings()


if __name__ == "__main__":
    main()
