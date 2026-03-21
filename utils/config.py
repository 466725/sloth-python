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



@dataclass(frozen=True)
class UrlSettings:
	tangerine: str
	deep_seek: str
	openai: str


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
class AIGenerationSettings:
	model: str
	base_url: str
	max_dom_chars: int
	output_dir: str


@dataclass(frozen=True)
class Settings:
	urls: UrlSettings
	ui: UiSettings
	playwright: PlaywrightSettings
	ai_generation: AIGenerationSettings


def load_settings() -> Settings:
	urls = UrlSettings(
		tangerine=_env_str("TANGERINE_URL", "https://www.tangerine.ca/en/personal"),
		deep_seek=_env_str("DEEP_SEEK_URL", "https://api.deepseek.com"),
		openai=_env_str("OPENAI_URL", "https://api.openai.com"),
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
	ai_generation = AIGenerationSettings(
		model=_env_str("AI_GEN_MODEL", "gpt-4.1"),
		base_url=_env_str("AI_GEN_BASE_URL", urls.openai),
		max_dom_chars=_env_int("AI_GEN_MAX_DOM_CHARS", 12000),
		output_dir=_env_str("AI_GEN_OUTPUT_DIR", "pytest_demo/tests/AI/generated_playwright"),
	)

	return Settings(urls=urls, ui=ui, playwright=playwright, ai_generation=ai_generation)


settings: Final[Settings] = load_settings()


def print_configured_settings() -> None:
	"""Print shared runtime settings for quick verification."""
	print(f"urls.tangerine={settings.urls.tangerine}")
	print(f"urls.deep_seek={settings.urls.deep_seek}")
	print(f"urls.openai={settings.urls.openai}")
	print(f"ui.base_url={settings.ui.base_url}")
	print(f"ui.locale={settings.ui.locale}")
	print(f"ui.sleep_time={settings.ui.sleep_time}")
	print(
		"ui.cookie_banner_timeout_seconds="
		f"{settings.ui.cookie_banner_timeout_seconds}"
	)
	print(f"playwright.headless={settings.playwright.headless}")
	print(f"ai_generation.model={settings.ai_generation.model}")
	print(f"ai_generation.base_url={settings.ai_generation.base_url}")
	print(f"ai_generation.max_dom_chars={settings.ai_generation.max_dom_chars}")
	print(f"ai_generation.output_dir={settings.ai_generation.output_dir}")


if __name__ == "__main__":
	print_configured_settings()

