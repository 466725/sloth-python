"""Learning exercises for the Cognizant SDET AI Builder Program."""

from __future__ import annotations

from importlib import import_module as _import_module

_user_profile_manager = _import_module(
    "claude_code.047_cognizant_sdet_ai_builder_program.user_profile_manager"
)

UserProfileManager = _user_profile_manager.UserProfileManager

__all__ = ["UserProfileManager"]
