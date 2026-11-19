# -*- coding: utf-8 -*-
"""Tests for env-based LLM channel parsing."""

import os
import tempfile
import unittest
from unittest.mock import Mock, patch

from tests.unit.llm.litellm_stub import ensure_litellm_stub

ensure_litellm_stub()

from ai_stock.config import (
    ANSPIRE_LLM_BASE_URL_DEFAULT,
    ANSPIRE_LLM_MODEL_DEFAULT,
    Config,
    get_effective_agent_models_to_try,
    get_effective_agent_primary_model,
    normalize_litellm_temperature,
)
from ai_stock.llm.generation_params import (
    apply_litellm_generation_params,
    resolve_litellm_temperature_directive,
)
from ai_stock.services.system_config_service import SystemConfigService


class LLMChannelConfigTestCase(unittest.TestCase):
    @patch("ai_stock.config.setup_env")
    @patch.object(Config, "_parse_litellm_yaml", return_value=[])
    def test_anspire_key_enables_openai_compatible_legacy_model(self, _mock_parse_yaml, _mock_setup_env) -> None:
        env = {
            "ANSPIRE_API_KEYS": "sk-anspire-test-value",
        }

        with patch.dict(os.environ, env, clear=True):
            config = Config._load_from_env()

        self.assertEqual(config.anspire_api_keys, ["sk-anspire-test-value"])
        self.assertEqual(config.openai_api_keys, ["sk-anspire-test-value"])
        self.assertEqual(config.openai_base_url, ANSPIRE_LLM_BASE_URL_DEFAULT)
        self.assertEqual(config.litellm_model, f"openai/{ANSPIRE_LLM_MODEL_DEFAULT}")
        self.assertEqual(config.llm_models_source, "legacy_env")
        params = config.llm_model_list[0]["litellm_params"]
        self.assertEqual(params["model"], "__legacy_openai__")
        self.assertEqual(params["api_base"], ANSPIRE_LLM_BASE_URL_DEFAULT)

    @patch("ai_stock.config.setup_env")
    @patch.object(Config, "_parse_litellm_yaml", return_value=[])
    def test_anspire_legacy_overrides_stale_openai_base_url(self, _mock_parse_yaml, _mock_setup_env) -> None:
        env = {
            "ANSPIRE_API_KEYS": "sk-anspire-test-value",
            "OPENAI_BASE_URL": "https://stale-openai-compatible.example/v1",
        }

        with patch.dict(os.environ, env, clear=True):
            config = Config._load_from_env()

        self.assertEqual(config.openai_api_keys, ["sk-anspire-test-value"])
        self.assertEqual(config.openai_base_url, ANSPIRE_LLM_BASE_URL_DEFAULT)
        params = config.llm_model_list[0]["litellm_params"]
        self.assertEqual(params["api_base"], ANSPIRE_LLM_BASE_URL_DEFAULT)

    @patch("ai_stock.config.setup_env")
    @patch.object(Config, "_parse_litellm_yaml", return_value=[])
    def test_anspire_channel_reuses_shared_key_and_defaults(self, _mock_parse_yaml, _mock_setup_env) -> None:
        env = {
            "LLM_CHANNELS": "anspire",
            "ANSPIRE_API_KEYS": "sk-anspire-test-value",
        }

        with patch.dict(os.environ, env, clear=True):
            config = Config._load_from_env()

        self.assertEqual(config.llm_models_source, "llm_channels")
        self.assertEqual(config.llm_channels[0]["protocol"], "openai")
        self.assertEqual(config.llm_channels[0]["api_keys"], ["sk-anspire-test-value"])
        self.assertEqual(config.llm_channels[0]["models"], [f"openai/{ANSPIRE_LLM_MODEL_DEFAULT}"])
        params = config.llm_model_list[0]["litellm_params"]
        self.assertEqual(params["api_base"], ANSPIRE_LLM_BASE_URL_DEFAULT)

    @patch("ai_stock.config.setup_env")
    @patch.object(Config, "_parse_litellm_yaml", return_value=[])
    def test_blank_anspire_channel_enabled_uses_shared_disable_flag(
        self,
        _mock_parse_yaml,
        _mock_setup_env,
    ) -> None:
        env = {
            "LLM_CHANNELS": "anspire",
            "LLM_ANSPIRE_ENABLED": "   ",
            "ANSPIRE_LLM_ENABLED": "false",
            "ANSPIRE_API_KEYS": "sk-anspire-test-value",
        }

        with patch.dict(os.environ, env, clear=True):
            config = Config._load_from_env()

        self.assertEqual(config.openai_api_keys, [])
        self.assertEqual(config.llm_channels, [])
        self.assertEqual(config.llm_model_list, [])

    @patch("ai_stock.config.setup_env")
    @patch.object(Config, "_parse_litellm_yaml", return_value=[])
    def test_disabled_anspire_channel_does_not_fall_back_to_legacy(
        self,
        _mock_parse_yaml,
        _mock_setup_env,
    ) -> None:
        env = {
            "LLM_CHANNELS": "anspire",
            "LLM_ANSPIRE_ENABLED": "false",
            "ANSPIRE_API_KEYS": "sk-anspire-test-value",
        }

        with patch.dict(os.environ, env, clear=True):
            config = Config._load_from_env()

        self.assertEqual(config.openai_api_keys, [])
        self.assertEqual(config.llm_channels, [])
        self.assertEqual(config.llm_model_list, [])

    @patch("ai_stock.config.setup_env")
    @patch.object(Config, "_parse_litellm_yaml", return_value=[])
    def test_protocol_prefixes_bare_model_names(self, _mock_parse_yaml, _mock_setup_env) -> None:
        env = {
            "LLM_CHANNELS": "primary",
            "LLM_PRIMARY_PROTOCOL": "deepseek",
            "LLM_PRIMARY_BASE_URL": "https://api.deepseek.com/v1",
            "LLM_PRIMARY_API_KEY": "sk-test-value",
            "LLM_PRIMARY_MODELS": "deepseek-chat",
        }

        with patch.dict(os.environ, env, clear=True):
            config = Config._load_from_env()

        self.assertEqual(config.llm_models_source, "llm_channels")
        self.assertEqual(config.llm_channels[0]["protocol"], "deepseek")
        self.assertEqual(config.llm_channels[0]["models"], ["deepseek/deepseek-chat"])
        self.assertEqual(config.llm_model_list[0]["litellm_params"]["model"], "deepseek/deepseek-chat")

    @patch("ai_stock.config.setup_env")
    @patch.object(Config, "_parse_litellm_yaml", return_value=[])
    def test_openai_compatible_channel_prefixes_non_provider_slash_models(self, _mock_parse_yaml, _mock_setup_env) -> None:
        env = {
            "LLM_CHANNELS": "siliconflow",
            "LLM_SILICONFLOW_PROTOCOL": "openai",
            "LLM_SILICONFLOW_BASE_URL": "https://api.siliconflow.cn/v1",
            "LLM_SILICONFLOW_API_KEY": "sk-test-value",
            "LLM_SILICONFLOW_MODELS": "Qwen/Qwen3-8B,deepseek-ai/DeepSeek-V3",
        }

        with patch.dict(os.environ, env, clear=True):
            config = Config._load_from_env()

        self.assertEqual(
            config.llm_channels[0]["models"],
            ["openai/Qwen/Qwen3-8B", "openai/deepseek-ai/DeepSeek-V3"],
        )

    @patch("ai_stock.config.setup_env")
    @patch.object(Config, "_parse_litellm_yaml", return_value=[])
    def test_alias_prefixed_models_are_canonicalized_once(self, _mock_parse_yaml, _mock_setup_env) -> None:
        env = {
            "LLM_CHANNELS": "vertex",
            "LLM_VERTEX_PROTOCOL": "vertex_ai",
            "LLM_VERTEX_API_KEY": "sk-test-value",
            "LLM_VERTEX_MODELS": "vertexai/gemini-2.5-flash",
        }

        with patch.dict(os.environ, env, clear=True):
            config = Config._load_from_env()

        self.assertEqual(config.llm_channels[0]["models"], ["vertex_ai/gemini-2.5-flash"])
        self.assertEqual(config.llm_model_list[0]["litellm_params"]["model"], "vertex_ai/gemini-2.5-flash")

    @patch("ai_stock.config.setup_env")
    @patch.object(Config, "_parse_litellm_yaml", return_value=[])
    def test_disabled_channel_is_skipped(self, _mock_parse_yaml, _mock_setup_env) -> None:
        env = {
            "LLM_CHANNELS": "primary",
            "LLM_PRIMARY_PROTOCOL": "openai",
            "LLM_PRIMARY_ENABLED": "false",
            "LLM_PRIMARY_API_KEY": "sk-test-value",
            "LLM_PRIMARY_MODELS": "gpt-4o-mini",
        }

        with patch.dict(os.environ, env, clear=True):
            config = Config._load_from_env()

        self.assertEqual(config.llm_channels, [])
        self.assertEqual(config.llm_model_list, [])

    @patch("ai_stock.config.setup_env")
    @patch.object(Config, "_parse_litellm_yaml", return_value=[])
    def test_ollama_channel_is_rejected(self, _mock_parse_yaml, _mock_setup_env) -> None:
        env = {
            "LLM_CHANNELS": "local",
            "LLM_LOCAL_PROTOCOL": "ollama",
            "LLM_LOCAL_BASE_URL": "http://127.0.0.1:11434",
            "LLM_LOCAL_API_KEY": "",
            "LLM_LOCAL_MODELS": "qwen3:8b",
        }

        with patch.dict(os.environ, env, clear=True):
            config = Config._load_from_env()

        self.assertEqual(config.llm_channels, [])
        self.assertEqual(config.llm_model_list, [])
        self.assertTrue(config.unsupported_ollama_configuration)
        self.assertTrue(
            any(issue.field == "LLM_PROVIDER" for issue in config.validate_structured())
        )

    @patch("ai_stock.config.setup_env")
    @patch.object(Config, "_parse_litellm_yaml", return_value=[])
    def test_ollama_model_prefixes_are_removed_from_channel_routes(
        self, _mock_parse_yaml, _mock_setup_env
    ) -> None:
        env = {
            "LLM_CHANNELS": "primary",
            "LLM_PRIMARY_PROTOCOL": "openai",
            "LLM_PRIMARY_BASE_URL": "https://api.example.com/v1",
            "LLM_PRIMARY_API_KEY": "sk-test-value",
            "LLM_PRIMARY_MODELS": "ollama/qwen3:8b,gpt-5.5",
        }

        with patch.dict(os.environ, env, clear=True):
            config = Config._load_from_env()

        self.assertEqual(config.llm_channels[0]["models"], ["openai/gpt-5.5"])
        self.assertTrue(config.unsupported_ollama_configuration)

    @patch("ai_stock.config.setup_env")
    def test_ollama_routes_in_yaml_and_model_selection_are_rejected(self, _mock_setup_env) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = os.path.join(temp_dir, "litellm.yaml")
            with open(config_path, "w", encoding="utf-8") as config_file:
                config_file.write(
                    "model_list:\n"
                    "  - model_name: local-alias\n"
                    "    litellm_params:\n"
                    "      model: ollama/qwen3:8b\n"
                    "      api_base: http://127.0.0.1:11434\n"
                )
            env = {
                "LITELLM_CONFIG": config_path,
                "LITELLM_MODEL": "local-alias",
                "LITELLM_FALLBACK_MODELS": "ollama/qwen3:8b",
                "AGENT_LITELLM_MODEL": "ollama/qwen3:8b",
                "VISION_MODEL": "ollama/qwen3:8b",
            }

            with patch.dict(os.environ, env, clear=True):
                config = Config._load_from_env()

        self.assertEqual(config.llm_model_list, [])
        self.assertEqual(config.litellm_model, "")
        self.assertEqual(config.litellm_fallback_models, [])
        self.assertEqual(config.agent_litellm_model, "")
        self.assertEqual(config.vision_model, "")
        self.assertTrue(config.unsupported_ollama_configuration)

    def test_system_config_rejects_ollama_routes_and_channel_checks(self) -> None:
        issues = SystemConfigService._validate_llm_runtime_selection(
            {"LITELLM_MODEL": "ollama/qwen3:8b"}
        )
        self.assertTrue(any(issue["code"] == "unsupported_provider" for issue in issues))

        channel_issues, _protocol = SystemConfigService._validate_llm_channel_connection(
            channel_name="local",
            protocol_value="openai",
            base_url_value="http://127.0.0.1:11434",
            api_key_value="",
            model_values=["qwen3:8b"],
            field_prefix="test_channel",
            require_base_url=False,
        )
        self.assertTrue(any(issue["code"] == "unsupported_provider" for issue in channel_issues))

    @patch("ai_stock.config.setup_env")
    @patch.object(Config, "_parse_litellm_yaml", return_value=[])
    def test_llm_temperature_ignores_invalid_value(self, _mock_parse_yaml, _mock_setup_env) -> None:
        env = {
            "GEMINI_API_KEY": "secret-key-value",
            "LLM_TEMPERATURE": "high",
            "GEMINI_TEMPERATURE": "0.25",
        }

        with patch.dict(os.environ, env, clear=True):
            config = Config._load_from_env()

        self.assertAlmostEqual(config.llm_temperature, 0.25)

    def test_gpt5_family_temperature_is_omitted_at_request_build_time(self) -> None:
        directive = resolve_litellm_temperature_directive("openai/gpt5.5-ferr")
        self.assertTrue(directive.omit_temperature)

        call_kwargs = apply_litellm_generation_params(
            {"model": "openai/gpt5.5-ferr", "messages": [], "temperature": 0.2},
            "openai/gpt5.5-ferr",
            0.2,
        )

        self.assertNotIn("temperature", call_kwargs)
        self.assertAlmostEqual(normalize_litellm_temperature("openai/gpt5.5-ferr", 0.2), 0.2)

    def test_gpt5_temperature_directive_resolves_litellm_yaml_alias(self) -> None:
        model_list = [
            {
                "model_name": "future_router",
                "litellm_params": {"model": "openai/gpt-5.5"},
            }
        ]

        directive = resolve_litellm_temperature_directive("future_router", model_list=model_list)
        call_kwargs = apply_litellm_generation_params(
            {"model": "future_router", "messages": []},
            "future_router",
            0.2,
            model_list=model_list,
        )

        self.assertTrue(directive.omit_temperature)
        self.assertNotIn("temperature", call_kwargs)

    @patch("ai_stock.config.setup_env")
    @patch.object(Config, "_parse_litellm_yaml", return_value=[])
    def test_local_openai_compatible_channel_defaults_to_openai_protocol(self, _mock_parse_yaml, _mock_setup_env) -> None:
        """Localhost OpenAI-compatible channels without a protocol default to openai."""
        env = {
            "LLM_CHANNELS": "local",
            "LLM_LOCAL_BASE_URL": "http://127.0.0.1:8000/v1",
            "LLM_LOCAL_API_KEY": "not-needed",
            "LLM_LOCAL_MODELS": "my-model",
        }

        with patch.dict(os.environ, env, clear=True):
            config = Config._load_from_env()

        params = config.llm_model_list[0]["litellm_params"]
        self.assertEqual(params["model"], "openai/my-model")
        self.assertEqual(config.llm_channels[0]["protocol"], "openai")

    @patch("ai_stock.config.setup_env")
    @patch.object(Config, "_parse_litellm_yaml", return_value=[])
    def test_agent_model_empty_inherits_primary_model(self, _mock_parse_yaml, _mock_setup_env) -> None:
        env = {
            "OPENAI_API_KEY": "sk-test-value",
            "OPENAI_MODEL": "gpt-4o-mini",
            "AGENT_LITELLM_MODEL": "",
        }

        with patch.dict(os.environ, env, clear=True):
            config = Config._load_from_env()

        self.assertEqual(config.agent_litellm_model, "")
        self.assertEqual(get_effective_agent_primary_model(config), "openai/gpt-4o-mini")

    @patch("ai_stock.config.setup_env")
    @patch.object(Config, "_parse_litellm_yaml", return_value=[])
    def test_agent_model_without_provider_prefix_is_normalized(self, _mock_parse_yaml, _mock_setup_env) -> None:
        env = {
            "OPENAI_API_KEY": "sk-test-value",
            "OPENAI_MODEL": "gpt-4o-mini",
            "AGENT_LITELLM_MODEL": "deepseek-chat",
        }

        with patch.dict(os.environ, env, clear=True):
            config = Config._load_from_env()

        self.assertEqual(config.agent_litellm_model, "openai/deepseek-chat")
        self.assertEqual(get_effective_agent_primary_model(config), "openai/deepseek-chat")

    @patch("ai_stock.config.setup_env")
    @patch.object(Config, "_parse_litellm_yaml", return_value=[])
    def test_agent_models_to_try_are_deduped_in_order(self, _mock_parse_yaml, _mock_setup_env) -> None:
        env = {
            "OPENAI_API_KEY": "sk-test-value",
            "LITELLM_MODEL": "gemini/gemini-2.5-flash",
            "AGENT_LITELLM_MODEL": "openai/gpt-4o-mini",
            "LITELLM_FALLBACK_MODELS": "openai/gpt-4o-mini,openai/gpt-4o-mini,gemini/gemini-2.5-flash",
        }

        with patch.dict(os.environ, env, clear=True):
            config = Config._load_from_env()

        self.assertEqual(
            get_effective_agent_models_to_try(config),
            ["openai/gpt-4o-mini", "gemini/gemini-2.5-flash"],
        )

    @patch("ai_stock.config.setup_env")
    @patch.object(Config, "_parse_litellm_yaml", return_value=[])
    def test_agent_models_to_try_dedupes_semantically_equivalent_openai_models(self, _mock_parse_yaml, _mock_setup_env) -> None:
        env = {
            "OPENAI_API_KEY": "sk-test-value",
            "LITELLM_MODEL": "gemini/gemini-2.5-flash",
            "AGENT_LITELLM_MODEL": "gpt-4o-mini",
            "LITELLM_FALLBACK_MODELS": "openai/gpt-4o-mini,gpt-4o-mini",
        }

        with patch.dict(os.environ, env, clear=True):
            config = Config._load_from_env()

        self.assertEqual(
            get_effective_agent_models_to_try(config),
            ["openai/gpt-4o-mini"],
        )

    @patch("ai_stock.config.setup_env")
    @patch.object(
        Config,
        "_parse_litellm_yaml",
        return_value=[
            {
                "model_name": "gpt4o",
                "litellm_params": {
                    "model": "openai/gpt-4o-mini",
                    "api_key": "sk-test-value",
                },
            }
        ],
    )
    def test_agent_model_preserves_yaml_alias_without_provider_prefix(self, _mock_parse_yaml, _mock_setup_env) -> None:
        env = {
            "LITELLM_CONFIG": "/tmp/litellm.yaml",
            "AGENT_LITELLM_MODEL": "gpt4o",
            "LITELLM_FALLBACK_MODELS": "openai/gpt-4o-mini",
        }

        with patch.dict(os.environ, env, clear=True):
            config = Config._load_from_env()

        self.assertEqual(config.agent_litellm_model, "gpt4o")
        self.assertEqual(get_effective_agent_primary_model(config), "gpt4o")
        self.assertEqual(
            get_effective_agent_models_to_try(config),
            ["gpt4o", "openai/gpt-4o-mini"],
        )

    def test_llm_base_url_rejects_ambiguous_parser_syntax(self) -> None:
        invalid_urls = [
            "https://127.0.0.1:6666\\@1.1.1.1/",
            "https://user@example.com/v1",
            "https://api.example.com/v1 models",
            "https://api.example.com/v1\tmodels",
            "https://api.example.com/v1\x7fmodels",
        ]

        for value in invalid_urls:
            with self.subTest(value=repr(value)):
                self.assertFalse(SystemConfigService._is_valid_llm_base_url(value))

    def test_llm_base_url_rejects_legacy_numeric_ipv4_aliases(self) -> None:
        invalid_urls = [
            "http://2852039166/v1",
            "http://0xa9fea9fe/v1",
            "http://025177524776/v1",
            "http://0251.0376.0251.0376/v1",
            "http://169.254.0xa9fe/v1",
        ]

        for value in invalid_urls:
            with self.subTest(value=value):
                self.assertFalse(SystemConfigService._is_valid_llm_base_url(value))
                self.assertFalse(SystemConfigService._is_safe_base_url(value))

    def test_llm_base_url_blocks_unicode_idna_metadata_aliases(self) -> None:
        restricted_urls = [
            "http://169。254。169。254/v1",
            "http://①⑥⑨.254.169.254/v1",
            "http://metadata。google。internal/v1",
            "http://ｍetadata.google.internal/v1",
        ]

        for value in restricted_urls:
            with self.subTest(value=value):
                self.assertTrue(SystemConfigService._is_valid_llm_base_url(value))
                self.assertFalse(SystemConfigService._is_safe_base_url(value))

    def test_llm_base_url_accepts_common_openai_compatible_and_local_shapes(self) -> None:
        valid_urls = [
            "https://api.openai.com/v1",
            "https://api.deepseek.com/v1",
            "https://api.siliconflow.cn/v1",
            "https://api.example.com/v1",
            "http://127.0.0.1:11434",
            "http://127.0.0.1:11434/v1",
        ]

        for value in valid_urls:
            with self.subTest(value=value):
                self.assertTrue(SystemConfigService._is_valid_llm_base_url(value), msg=value)
                self.assertTrue(SystemConfigService._is_safe_base_url(value), msg=value)

    @patch("ai_stock.services.system_config_service.requests.get")
    def test_discover_llm_channel_models_blocks_parser_differential_url(self, mock_get) -> None:
        service = SystemConfigService(manager=Mock())

        payload = service.discover_llm_channel_models(
            name="primary",
            protocol="openai",
            base_url="https://127.0.0.1:6666\\@1.1.1.1/",
            api_key="sk-test-value",
        )

        self.assertFalse(payload["success"])
        self.assertEqual(payload["error_code"], "invalid_config")
        self.assertEqual(payload["details"]["reason"], "invalid_url")
        mock_get.assert_not_called()

    @patch("ai_stock.services.system_config_service.requests.get")
    def test_discover_llm_channel_models_blocks_unicode_metadata_alias(self, mock_get) -> None:
        service = SystemConfigService(manager=Mock())

        for value in (
            "http://169。254。169。254/v1",
            "http://①⑥⑨.254.169.254/v1",
        ):
            with self.subTest(value=value):
                payload = service.discover_llm_channel_models(
                    name="primary",
                    protocol="openai",
                    base_url=value,
                    api_key="sk-test-value",
                )

                self.assertFalse(payload["success"])
                self.assertEqual(payload["error_code"], "invalid_config")
                self.assertEqual(payload["details"]["reason"], "ssrf_blocked")
                mock_get.assert_not_called()

    @patch("ai_stock.services.system_config_service.requests.get")
    def test_discover_llm_channel_models_blocks_numeric_metadata_alias(self, mock_get) -> None:
        service = SystemConfigService(manager=Mock())

        payload = service.discover_llm_channel_models(
            name="primary",
            protocol="openai",
            base_url="http://2852039166/v1",
            api_key="sk-test-value",
        )

        self.assertFalse(payload["success"])
        self.assertEqual(payload["error_code"], "invalid_config")
        self.assertEqual(payload["details"]["reason"], "invalid_url")
        mock_get.assert_not_called()

    def test_llm_models_url_rechecks_restricted_and_valid_urls(self) -> None:
        restricted_urls = [
            "http://169.254.169.254/v1",
            "http://[::ffff:169.254.169.254]/v1",
            "http://[::ffff:100.100.100.200]/v1",
        ]
        for value in restricted_urls:
            with self.subTest(value=value):
                self.assertTrue(SystemConfigService._is_valid_llm_base_url(value))
                self.assertFalse(SystemConfigService._is_safe_base_url(value))
                with self.assertRaises(ValueError):
                    SystemConfigService._build_llm_models_url(value)

        self.assertEqual(
            SystemConfigService._build_llm_models_url(
                "https://api.example.com/v1/chat/completions?api-version=1#frag"
            ),
            "https://api.example.com/v1/models",
        )


if __name__ == "__main__":
    unittest.main()
