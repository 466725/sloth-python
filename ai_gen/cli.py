"""Keep ``python -m ai_gen.cli`` working after the move into utils."""

from utils.ai_gen.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
