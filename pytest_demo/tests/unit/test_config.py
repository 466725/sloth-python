import importlib

import pytest

import utils.config as config_module


CONFIG_ENV_VARS = [
    "TANGERINE_URL",
    "DEEP_SEEK_URL",
    "OPENAI_URL",
    "CINEPLEX_URL",
    "UI_LOCALE",
    "SLEEP_TIME",
    "COOKIE_BANNER_TIMEOUT_SECONDS",
    "PW_HEADLESS",
    "SELENIUM_HEADLESS",
    "SELENIUM_REMOTE_URL",
    "SELENIUM_IMPLICIT_WAIT",
    "SELENIUM_EXPLICIT_WAIT",
]


def _reload_config(monkeypatch: pytest.MonkeyPatch):
    for name in CONFIG_ENV_VARS:
        monkeypatch.delenv(name, raising=False)
    return importlib.reload(config_module)


@pytest.mark.unit
def test_settings_defaults_are_loaded_from_expected_fallbacks(monkeypatch: pytest.MonkeyPatch):
    module = _reload_config(monkeypatch)

    assert module.settings.urls.tangerine == "https://www.tangerine.ca/en/personal"
    assert module.settings.ui.base_url == module.settings.urls.tangerine
    assert module.settings.ui.locale == "en-US"
    assert module.settings.ui.sleep_time == 1
    assert module.settings.ui.cookie_banner_timeout_seconds == 5
    assert module.settings.playwright.headless is True
    assert module.settings.selenium.headless is True
    assert module.settings.selenium.remote_url is None
    assert module.settings.selenium.implicit_wait == 10
    assert module.settings.selenium.explicit_wait == 10
    assert "--incognito" in module.settings.selenium.common_arguments
    assert "--window-size=1920,1080" in module.settings.selenium.stability_arguments


@pytest.mark.unit
def test_settings_support_environment_overrides(monkeypatch: pytest.MonkeyPatch):
    module = _reload_config(monkeypatch)
    monkeypatch.setenv("TANGERINE_URL", "https://example.test")
    monkeypatch.setenv("UI_LOCALE", "fr-CA")
    monkeypatch.setenv("SLEEP_TIME", "2")
    monkeypatch.setenv("COOKIE_BANNER_TIMEOUT_SECONDS", "7")
    monkeypatch.setenv("PW_HEADLESS", "false")
    monkeypatch.setenv("SELENIUM_HEADLESS", "0")
    monkeypatch.setenv("SELENIUM_REMOTE_URL", "http://grid:4444/wd/hub")
    monkeypatch.setenv("SELENIUM_IMPLICIT_WAIT", "12")
    monkeypatch.setenv("SELENIUM_EXPLICIT_WAIT", "15")

    module = importlib.reload(module)

    assert module.settings.urls.tangerine == "https://example.test"
    assert module.settings.ui.base_url == "https://example.test"
    assert module.settings.ui.locale == "fr-CA"
    assert module.settings.ui.sleep_time == 2
    assert module.settings.ui.cookie_banner_timeout_seconds == 7
    assert module.settings.playwright.headless is False
    assert module.settings.selenium.headless is False
    assert module.settings.selenium.remote_url == "http://grid:4444/wd/hub"
    assert module.settings.selenium.implicit_wait == 12
    assert module.settings.selenium.explicit_wait == 15
    assert "--lang=fr-CA" in module.settings.selenium.common_arguments


@pytest.mark.unit
def test_invalid_boolean_environment_value_raises_value_error(monkeypatch: pytest.MonkeyPatch):
    _reload_config(monkeypatch)
    monkeypatch.setenv("PW_HEADLESS", "maybe")

    with pytest.raises(ValueError, match="PW_HEADLESS"):
        importlib.reload(config_module)

