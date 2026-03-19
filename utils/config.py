from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Final


def _env_bool(name: str, default: bool) -> bool:
	value = os.getenv(name)
	if value is None:
		return default

	normalized = value.strip().lower()
	if normalized in {"1", "true", "yes", "on"}:
		return True
	if normalized in {"0", "false", "no", "off"}:
		return False
	raise ValueError(f"Environment variable {name} must be a boolean-like value, got: {value!r}")


def _env_int(name: str, default: int) -> int:
	value = os.getenv(name)
	if value is None:
		return default
	return int(value)


def _env_str(name: str, default: str) -> str:
	return os.getenv(name, default).strip() or default


def _env_optional_str(name: str) -> str | None:
	value = os.getenv(name)
	if value is None:
		return None
	value = value.strip()
	return value or None


@dataclass(frozen=True)
class UrlSettings:
	tangerine: str
	deep_seek: str
	openai: str
	cineplex: str


@dataclass(frozen=True)
class UiSettings:
	base_url: str
	locale: str
	sleep_time: int
	cookie_banner_timeout_seconds: int


@dataclass(frozen=True)
class PlaywrightSettings:
	headless: bool


@dataclass(frozen=True)
class SeleniumSettings:
	headless: bool
	remote_url: str | None
	implicit_wait: int
	explicit_wait: int
	common_arguments: tuple[str, ...]
	stability_arguments: tuple[str, ...]


@dataclass(frozen=True)
class Settings:
	urls: UrlSettings
	ui: UiSettings
	playwright: PlaywrightSettings
	selenium: SeleniumSettings


def load_settings() -> Settings:
	urls = UrlSettings(
		tangerine=_env_str("TANGERINE_URL", "https://www.tangerine.ca/en/personal"),
		deep_seek=_env_str("DEEP_SEEK_URL", "https://api.deepseek.com"),
		openai=_env_str("OPENAI_URL", "https://api.openai.com"),
		cineplex=_env_str("CINEPLEX_URL", "https://connect.cineplex.com"),
	)

	ui = UiSettings(
		base_url=urls.tangerine,
		locale=_env_str("UI_LOCALE", "en-US"),
		sleep_time=_env_int("SLEEP_TIME", 1),
		cookie_banner_timeout_seconds=_env_int("COOKIE_BANNER_TIMEOUT_SECONDS", 5),
	)

	playwright = PlaywrightSettings(
		headless=_env_bool("PW_HEADLESS", True),
	)

	selenium = SeleniumSettings(
		headless=_env_bool("SELENIUM_HEADLESS", True),
		remote_url=_env_optional_str("SELENIUM_REMOTE_URL"),
		implicit_wait=_env_int("SELENIUM_IMPLICIT_WAIT", 10),
		explicit_wait=_env_int("SELENIUM_EXPLICIT_WAIT", 10),
		common_arguments=(
			"--start-maximized",
			"--incognito",
			f"--lang={ui.locale}",
		),
		stability_arguments=(
			"--no-sandbox",
			"--disable-dev-shm-usage",
			"--disable-gpu",
			"--disable-extensions",
			"--disable-web-resources",
			"--disable-sync",
			"--disable-plugins",
			"--disable-images",
			"--disable-background-networking",
			"--no-first-run",
			"--no-default-browser-check",
			"--window-size=1920,1080",
		),
	)

	return Settings(urls=urls, ui=ui, playwright=playwright, selenium=selenium)


settings: Final[Settings] = load_settings()


def print_configured_settings() -> None:
	"""Print shared runtime settings for quick verification."""
	print(f"urls.tangerine={settings.urls.tangerine}")
	print(f"urls.deep_seek={settings.urls.deep_seek}")
	print(f"urls.openai={settings.urls.openai}")
	print(f"urls.cineplex={settings.urls.cineplex}")
	print(f"ui.base_url={settings.ui.base_url}")
	print(f"ui.locale={settings.ui.locale}")
	print(f"ui.sleep_time={settings.ui.sleep_time}")
	print(
		"ui.cookie_banner_timeout_seconds="
		f"{settings.ui.cookie_banner_timeout_seconds}"
	)
	print(f"playwright.headless={settings.playwright.headless}")
	print(f"selenium.headless={settings.selenium.headless}")
	print(f"selenium.remote_url={settings.selenium.remote_url}")
	print(f"selenium.implicit_wait={settings.selenium.implicit_wait}")
	print(f"selenium.explicit_wait={settings.selenium.explicit_wait}")
	print(f"selenium.common_arguments={settings.selenium.common_arguments}")
	print(f"selenium.stability_arguments={settings.selenium.stability_arguments}")


if __name__ == "__main__":
	print_configured_settings()

