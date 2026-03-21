import json
from pathlib import Path

import pytest

from pytest_demo.self_healing import locator_store


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


@pytest.mark.unit
def test_load_and_get_locator_from_split_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    signin = tmp_path / "signinpage.json"
    signup = tmp_path / "signuppage.json"

    _write_json(signin, {"tangerine.login": {"primary": {"by": "id", "value": "login"}}})
    _write_json(signup, {"tangerine.signup": {"primary": {"by": "id", "value": "menu_signup"}}})

    monkeypatch.setattr(locator_store, "SIGNINPAGE_LOCATOR_FILE", signin)
    monkeypatch.setattr(locator_store, "SIGNUPPAGE_LOCATOR_FILE", signup)
    monkeypatch.setattr(locator_store, "LEGACY_LOCATOR_FILE", tmp_path / "locators.json")
    monkeypatch.setattr(
        locator_store,
        "KEY_TO_FILE",
        {
            "tangerine.login": signin,
            "tangerine.signup": signup,
        },
    )

    assert locator_store.get_locator("tangerine.login")["primary"]["value"] == "login"
    assert locator_store.get_locator("tangerine.signup")["primary"]["value"] == "menu_signup"


@pytest.mark.unit
def test_update_primary_locator_updates_only_target_split_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    signin = tmp_path / "signinpage.json"
    signup = tmp_path / "signuppage.json"

    _write_json(
        signin,
        {
            "tangerine.login": {
                "primary": {"by": "id", "value": "login"},
                "fallbacks": [],
                "expected": {"text": "Log in"},
            }
        },
    )
    _write_json(
        signup,
        {
            "tangerine.signup": {
                "primary": {"by": "id", "value": "menu_signup"},
                "fallbacks": [],
                "expected": {"text": "Sign me up"},
            }
        },
    )

    monkeypatch.setattr(locator_store, "SIGNINPAGE_LOCATOR_FILE", signin)
    monkeypatch.setattr(locator_store, "SIGNUPPAGE_LOCATOR_FILE", signup)
    monkeypatch.setattr(locator_store, "LEGACY_LOCATOR_FILE", tmp_path / "locators.json")
    monkeypatch.setattr(
        locator_store,
        "KEY_TO_FILE",
        {
            "tangerine.login": signin,
            "tangerine.signup": signup,
        },
    )

    locator_store.update_primary_locator("tangerine.login", {"by": "css", "value": "#login"})

    signin_data = json.loads(signin.read_text(encoding="utf-8"))
    signup_data = json.loads(signup.read_text(encoding="utf-8"))

    assert signin_data["tangerine.login"]["primary"] == {"by": "css", "value": "#login"}
    assert signup_data["tangerine.signup"]["primary"] == {"by": "id", "value": "menu_signup"}

