"""Unit tests for UserProfileManager string-method behavior."""

import pytest

from claude_code import _047_cognizant_sdet_ai_builder_program as upm

UserProfileManager = upm.UserProfileManager


@pytest.fixture
def manager() -> UserProfileManager:
    return UserProfileManager(name="john doe", email="John@Example.COM", user_id="001")


class TestFormatName:
    def test_normal_input_title_cases_each_word(self, manager):
        assert manager.format_name("john doe") == "John Doe"

    def test_mixed_case_input_is_normalized(self, manager):
        assert manager.format_name("jOHN dOE") == "John Doe"

    def test_extra_spaces_are_stripped(self, manager):
        assert manager.format_name("   jane smith  ") == "Jane Smith"

    def test_empty_name_returns_empty_string(self, manager):
        assert manager.format_name("") == ""


class TestNormalizeEmail:
    def test_uppercase_email_is_lowered(self, manager):
        assert manager.normalize_email("John@Example.COM") == "john@example.com"

    def test_extra_spaces_are_stripped(self, manager):
        assert manager.normalize_email("  user@site.com  ") == "user@site.com"


class TestValidateEmail:
    def test_valid_email_passes(self, manager):
        assert manager.validate_email("john@example.com") is True

    def test_missing_at_sign_fails(self, manager):
        assert manager.validate_email("johnexample.com") is False

    def test_double_at_sign_fails(self, manager):
        assert manager.validate_email("a@@b.com") is False

    def test_empty_local_part_fails(self, manager):
        assert manager.validate_email("@example.com") is False

    def test_domain_without_dot_fails(self, manager):
        assert manager.validate_email("john@examplecom") is False

    def test_domain_starting_with_dot_fails(self, manager):
        assert manager.validate_email("john@.com") is False

    def test_domain_ending_with_dot_fails(self, manager):
        assert manager.validate_email("john@example.") is False

    def test_extra_spaces_around_valid_email_still_pass(self, manager):
        assert manager.validate_email("  john@example.com  ") is True


class TestGetDisplayString:
    def test_format_is_exact_for_normal_inputs(self, manager):
        result = manager.get_display_string("john doe", "John@Example.COM", "001")
        assert result == "John Doe | john@example.com | ID: 001"

    def test_integer_id_is_zero_padded(self, manager):
        result = manager.get_display_string("john doe", "john@example.com", 7)
        assert result == "John Doe | john@example.com | ID: 007"

    def test_invalid_email_raises_value_error(self, manager):
        with pytest.raises(ValueError, match="Invalid email address"):
            manager.get_display_string("john doe", "johnexample.com", "001")

    def test_empty_name_keeps_exact_separator_format(self, manager):
        result = manager.get_display_string("", "john@example.com", "001")
        assert result == " | john@example.com | ID: 001"
