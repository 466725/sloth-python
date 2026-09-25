from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
from typing import Final

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


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


def _normalize_openai_base_url(url: str) -> str:
	"""Ensure OpenAI-compatible URL has the /v1 prefix expected by the SDK path layout."""
	normalized = url.rstrip("/")
	parsed = urlparse(normalized)
	if parsed.netloc == "api.openai.com" and not parsed.path.endswith("/v1"):
		return f"{normalized}/v1"
	return normalized



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
	slow_mo: int


@dataclass(frozen=True)
class LoggerSettings:
	level: str
	log_file: str | None
	log_format: str
	log_directory: str = "temps/logs"
	max_bytes: int = 500 * 1024 * 1024


@dataclass(frozen=True)
class AIGenerationSettings:
	model: str
	base_url: str
	max_dom_chars: int
	output_dir: str
	temperature: float = 0.7


@dataclass(frozen=True)
class DatabaseSettings:
	host: str
	port: int
	database: str
	user: str
	password: str

	@classmethod
	def from_env(cls, prefix: str = "SLOTH_MYSQL") -> "DatabaseSettings":
		return cls(
			host=_env_str(f"{prefix}_HOST", "localhost"),
			port=_env_int(f"{prefix}_PORT", 3306),
			database=_env_str(f"{prefix}_DB", "slothdb"),
			user=_env_str(f"{prefix}_USER", "slothuser"),
			password=os.getenv(f"{prefix}_PASSWORD", ""),
		)

	def as_mysql_kwargs(self) -> dict[str, object]:
		return {
			"host": self.host,
			"port": self.port,
			"user": self.user,
			"password": self.password,
			"database": self.database,
		}


@dataclass(frozen=True)
class Settings:
	urls: UrlSettings
	ui: UiSettings
	playwright: PlaywrightSettings
	logger: LoggerSettings
	ai_generation: AIGenerationSettings
	database: DatabaseSettings


def load_settings() -> Settings:
	urls = UrlSettings(
		tangerine=_env_str("TANGERINE_URL", "https://www.tangerine.ca/en/personal"),
		deep_seek=_env_str("DEEP_SEEK_URL", "https://api.deepseek.com"),
		openai=_normalize_openai_base_url(_env_str("OPENAI_URL", "https://api.openai.com/v1")),
	)

	ui = UiSettings(
		base_url=urls.tangerine,
		locale=_env_str("UI_LOCALE", "en-US"),
		sleep_time=_env_int("SLEEP_TIME", 1),
		cookie_banner_timeout_seconds=_env_int("COOKIE_BANNER_TIMEOUT_SECONDS", 5),
	)

	playwright = PlaywrightSettings(
		headless=_env_bool("PW_HEADLESS", False),
		slow_mo=_env_int("PW_SLOW_MO", 0),
	)

	logger = LoggerSettings(
		level=_env_str("LOG_LEVEL", "INFO").upper(),
		log_file=os.getenv("LOG_FILE") or None,
		log_format=_env_str("LOG_FORMAT", "%(asctime)s %(levelname)s %(name)s: %(message)s"),
		log_directory=_env_str("LOG_DIRECTORY", "temps/logs"),
		max_bytes=_env_int("LOG_MAX_BYTES", 500 * 1024 * 1024),
	)
	
	ai_generation = AIGenerationSettings(
		model=_env_str("AI_GEN_MODEL", "gpt-4.1"),
		base_url=_normalize_openai_base_url(_env_str("AI_GEN_BASE_URL", urls.openai)),
		max_dom_chars=_env_int("AI_GEN_MAX_DOM_CHARS", 12000),
		output_dir=_env_str("AI_GEN_OUTPUT_DIR", "temps/ai/ai_gen_tests"),
	)
	database = DatabaseSettings.from_env()

	return Settings(
		urls=urls,
		ui=ui,
		playwright=playwright,
		logger=logger,
		ai_generation=ai_generation,
		database=database,
	)


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
	print(f"logger.level={settings.logger.level}")
	print(f"logger.log_file={settings.logger.log_file}")
	print(f"logger.log_format={settings.logger.log_format}")
	print(f"logger.log_directory={settings.logger.log_directory}")
	print(f"logger.max_bytes={settings.logger.max_bytes}")
	print(f"ai_generation.model={settings.ai_generation.model}")
	print(f"ai_generation.base_url={settings.ai_generation.base_url}")
	print(f"ai_generation.max_dom_chars={settings.ai_generation.max_dom_chars}")
	print(f"ai_generation.output_dir={settings.ai_generation.output_dir}")
	print(f"ai_generation.temperature={settings.ai_generation.temperature}")
	print(f"database.host={settings.database.host}")
	print(f"database.port={settings.database.port}")
	print(f"database.database={settings.database.database}")
	print(f"database.user={settings.database.user}")


if __name__ == "__main__":
	print_configured_settings()

