"""UserProfileManager class skeleton for Python string-method practice.

This module intentionally contains stubs only. Implementations should rely on
built-in string methods such as title(), lower(), strip(), split(), count(),
startswith(), endswith(), zfill(), and f-strings.
"""

from __future__ import annotations


class UserProfileManager:
    """Manages formatting, validation, and display of user profile data."""

    def format_name(self, name: str) -> str:
        """Format a full name into title case.

        Expected behavior:
        - Strip leading/trailing whitespace.
        - Convert each word to title case, e.g. "jOHN dOE" -> "John Doe".
        - Use str.title() (or equivalent string methods) for casing.
        """
        raise NotImplementedError

    def normalize_email(self, email: str) -> str:
        """Normalize an email address to a canonical lowercase form.

        Expected behavior:
        - Strip leading/trailing whitespace.
        - Convert the entire address to lowercase, e.g. "John.Doe@Example.COM"
          -> "john.doe@example.com".
        - Use str.lower() for case folding.
        """
        raise NotImplementedError

    def validate_email(self, email: str) -> bool:
        """Validate email format using string methods only (no regex).

        Expected behavior:
        - Return True only when the address has exactly one "@".
        - Both local part and domain must be non-empty after split("@").
        - Domain must contain at least one "." and must not start or end
          with "." or "@".
        - Combine str.count(), str.split(), str.startswith(), str.endswith(),
          and the `in` operator for the checks.
        """
        raise NotImplementedError

    def get_display_string(self, name: str, email: str, user_id: int) -> str:
        """Build a display string like "John Doe | john@example.com | ID: 001".

        Expected behavior:
        - Use format_name() and normalize_email() for the name and email parts.
        - Zero-pad the ID to 3 digits, e.g. 7 -> "007" (str.zfill() or the
          f-string format specifier :03d).
        - Join the parts with " | " using an f-string.
        - Raise ValueError if validate_email() returns False.
        """
        raise NotImplementedError
