# -*- coding: utf-8 -*-
"""Helpers for exposing configured Agent model deployments."""

from __future__ import annotations

from typing import Any, Dict, List

from ai_stock.config import get_effective_agent_primary_model


_PLACEHOLDER_TO_PROVIDER = {
    "__legacy_gemini__": "gemini",
    "__legacy_openai__": "openai",
    "__legacy_deepseek__": "deepseek",
}
_MANAGED_LEGACY_PROVIDERS = set(_PLACEHOLDER_TO_PROVIDER.values())


def _get_models_source(config) -> str:
    source = getattr(config, "llm_models_source", "")
    if source in {"litellm_config", "llm_channels", "legacy_env"}:
        return source
    return "legacy_env"


def _get_model_provider(model_name: str) -> str:
    if not model_name:
        return "unknown"
    if "/" in model_name:
        return model_name.split("/", 1)[0]
    return "openai"


def _build_non_legacy_deployments(config) -> List[Dict[str, Any]]:
    source = _get_models_source(config)
    primary_model = get_effective_agent_primary_model(config)
    deployments: List[Dict[str, Any]] = []

    for index, entry in enumerate(getattr(config, "llm_model_list", []) or []):
        params = entry.get("litellm_params", {}) or {}
        model_name = str(params.get("model") or "").strip()
        if not model_name or model_name.startswith("__legacy_"):
            continue

        api_base = params.get("api_base")
        deployment_name = entry.get("model_name")
        deployments.append(
            {
                "deployment_id": f"{source}:{index}",
                "model": model_name,
                "provider": _get_model_provider(model_name),
                "source": source,
                "api_base": str(api_base).strip() if api_base else None,
                "deployment_name": str(deployment_name).strip() if deployment_name else None,
                "is_primary": model_name == primary_model,
                "is_fallback": False,
            }
        )

    return deployments


def _build_legacy_deployments(config) -> List[Dict[str, Any]]:
    primary_model = get_effective_agent_primary_model(config)
    if not primary_model:
        return []

    placeholder_counts = {provider: 0 for provider in _PLACEHOLDER_TO_PROVIDER.values()}
    for entry in getattr(config, "llm_model_list", []) or []:
        provider = _PLACEHOLDER_TO_PROVIDER.get(entry.get("model_name"))
        if provider:
            placeholder_counts[provider] += 1

    provider = _get_model_provider(primary_model)
    deployment_count = placeholder_counts.get(provider, 0)
    if deployment_count <= 0:
        if provider in _MANAGED_LEGACY_PROVIDERS:
            return []
        deployment_count = 1

    api_base = getattr(config, "openai_base_url", None) if provider == "openai" else None
    return [
        {
            "deployment_id": f"legacy:{provider}:{index}:{primary_model}",
            "model": primary_model,
            "provider": provider,
            "source": "legacy_env",
            "api_base": api_base,
            "deployment_name": f"legacy_{provider}_{index + 1}",
            "is_primary": True,
            "is_fallback": False,
        }
        for index in range(deployment_count)
    ]


def list_agent_model_deployments(config) -> List[Dict[str, Any]]:
    """Return configured Agent model deployments without exposing secrets."""
    deployments = _build_non_legacy_deployments(config)
    if not deployments:
        deployments = _build_legacy_deployments(config)

    return sorted(
        deployments,
        key=lambda item: (
            not item["is_primary"],
            item["source"],
            item["model"],
            item["api_base"] or "",
            item["deployment_name"] or "",
            item["deployment_id"],
        ),
    )
