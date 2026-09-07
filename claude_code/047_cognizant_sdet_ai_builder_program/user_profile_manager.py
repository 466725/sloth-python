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
        # str.strip() removes stray whitespace so it doesn't affect casing;
        # str.title() uppercases each word's first letter and lowercases the rest.
        return name.strip().title()

    def normalize_email(self, email: str) -> str:
        """Normalize an email address to a canonical lowercase form.

        Expected behavior:
        - Strip leading/trailing whitespace.
        - Convert the entire address to lowercase, e.g. "John.Doe@Example.COM"
          -> "john.doe@example.com".
        - Use str.lower() for case folding.
        """
        # str.strip() drops surrounding whitespace from form/CSV input;
        # str.lower() gives a canonical form so comparisons are case-insensitive.
        return email.strip().lower()

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
        # str.strip() first: surrounding spaces should not fail validation.
        email = email.strip()
        # str.count("@") ensures exactly one separator (rejects "a@@b.com").
        if email.count("@") != 1:
            return False
        # str.split("@") separates local part from domain; both must be non-empty.
        local, domain = email.split("@")
        if not local or not domain:
            return False
        # `in` operator requires a dot in the domain ("example.com", not "examplecom").
        if "." not in domain:
            return False
        # str.startswith()/str.endswith() reject malformed domains like ".com" or "com.".
        if domain.startswith(".") or domain.endswith("."):
            return False
        return True

    def get_display_string(self, name: str, email: str, user_id: int | str) -> str:
        """Build a display string like "John Doe | john@example.com | ID: 001".

        Expected behavior:
        - Use format_name() and normalize_email() for the name and email parts.
        - Zero-pad the ID to 3 digits, e.g. 7 -> "007" (str.zfill() or the
          f-string format specifier :03d).
        - Join the parts with " | " using an f-string.
        - Raise ValueError if validate_email() returns False.
        """
        if not self.validate_email(email):
            raise ValueError(f"Invalid email address: {email!r}")
        # Reuse our own helpers so formatting rules stay in one place.
        formatted_name = self.format_name(name)
        normalized_email = self.normalize_email(email)
        # str(user_id).zfill(3) zero-pads to width 3: 7 -> "007", "001" -> "001".
        padded_id = str(user_id).zfill(3)
        # f-string joins the parts with the " | " separator and the "ID:" label.
        return f"{formatted_name} | {normalized_email} | ID: {padded_id}"


if __name__ == "__main__":
    manager = UserProfileManager()
    display = manager.get_display_string(name="john doe", email="John@Example.COM", user_id="001")
    print(display)
