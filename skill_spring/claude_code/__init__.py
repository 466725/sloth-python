"""Claude Code learning material package.

Exposes the digit-prefixed subpackage "047_cognizant_sdet_ai_builder_program"
under an importable alias since module names cannot start with a digit.
"""

from __future__ import annotations

import importlib

_047_cognizant_sdet_ai_builder_program = importlib.import_module(
    "claude_code.047_cognizant_sdet_ai_builder_program"
)
