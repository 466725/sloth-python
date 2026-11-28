# -*- coding: utf-8 -*-
"""
Multi-provider LLM Tool-Calling Adapter.

Normalizes function-calling / tool-use across all providers into a unified
interface consumed by the AgentExecutor, via LiteLLM.
"""

import json
import logging
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Tuple

import litellm
from litellm import Router

from ai_stock.config import (
    extra_litellm_params,
    get_api_keys_for_model,
    get_config,
    get_configured_llm_models,
    get_effective_agent_primary_model,
)
from ai_stock.agent.provider_trace import (
    TRACE_MODEL_KEY,
    TRACE_PROVIDER_KEY,
    resolved_model_provider_identity,
    resolved_provider_namespace,
    trace_model_matches,
)
from ai_stock.llm.errors import call_litellm_with_param_recovery
from ai_stock.llm.generation_params import apply_litellm_generation_params, resolve_litellm_wire_model
from ai_stock.llm.usage import attach_message_hmacs, extract_usage_payload, normalize_litellm_usage
from ai_stock.services.run_diagnostics import sanitize_diagnostic_text

logger = logging.getLogger(__name__)


# ============================================================
# Unified response types
# ============================================================

@dataclass
class ToolCall:
    """A single tool call requested by the LLM."""
    id: str
    name: str
    arguments: Dict[str, Any]
    thought_signature: Optional[str] = None
    provider_specific_fields: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LLMResponse:
    """Normalized response from any LLM provider."""
    content: Optional[str] = None          # text response (final answer)
    tool_calls: List[ToolCall] = field(default_factory=list)  # tool calls to execute
    reasoning_content: Optional[str] = None  # Chain-of-thought (CoT) from DeepSeek thinking mode; must be passed back in multi-turn assistant messages; None for other providers
    provider_blocks: List[Dict[str, Any]] = field(default_factory=list)  # Opaque provider content blocks (e.g. Claude thinking/redacted_thinking)
    usage: Dict[str, Any] = field(default_factory=dict)       # token usage info
    provider: str = ""                     # which provider handled this call
    model: str = ""                        # full model name used (e.g. gemini/gemini-2.0-flash), for report meta
    raw: Any = None                        # raw provider response for debugging


# Models that auto-return reasoning_content; do NOT send extra_body (may cause 400).
_AUTO_THINKING_MODELS: List[str] = ["deepseek-reasoner", "deepseek-r1", "qwq"]

# Models that need explicit opt-in via extra_body; payload decoupled from model name.
_OPT_IN_THINKING_MODELS: Dict[str, dict] = {
    "deepseek-chat": {"thinking": {"type": "enabled"}},
}

_FALLBACK_MODEL_PRICING: Dict[str, Any] = {
    "supports_function_calling": True,
    "supports_vision": False,
    "supports_audio_input": False,
    "supports_audio_output": False,
    "context_window": 100000,
    "max_tokens": 10000,
    "input_cost_per_token": 0.0,
    "output_cost_per_token": 0.0,
}
_FALLBACK_MODEL_PRICING_REGISTERED: set[str] = set()


def _split_provider_model(model: str) -> Tuple[str, str]:
    normalized = (model or "").strip()
    if not normalized:
        return "", ""
    if "/" in normalized:
        provider, remainder = normalized.split("/", 1)
        return provider.lower(), remainder.strip()
    return "openai", normalized


def _object_to_dict(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    if hasattr(value, "model_dump"):
        try:
            dumped = value.model_dump()
            if isinstance(dumped, dict):
                return dumped
        except Exception:
            pass
    if hasattr(value, "dict"):
        try:
            dumped = value.dict()
            if isinstance(dumped, dict):
                return dumped
        except Exception:
            pass
    result: Dict[str, Any] = {}
    for key in ("type", "text", "content", "thinking", "signature", "data"):
        if hasattr(value, key):
            result[key] = getattr(value, key)
    return result


def _provider_specific_fields_from(value: Any) -> Dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return dict(value)
    data = _object_to_dict(value)
    return data if isinstance(data, dict) else {}


def _extract_provider_blocks(choice: Any) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """Return opaque provider blocks and joined text block content, if present."""
    block_sources = []
    message = getattr(choice, "message", None)
    for owner in (message, choice):
        if owner is None:
            continue
        for attr in ("content", "content_blocks", "provider_blocks", "thinking_blocks"):
            value = getattr(owner, attr, None)
            if isinstance(value, list):
                block_sources.append(value)

    blocks: List[Dict[str, Any]] = []
    text_parts: List[str] = []
    for source in block_sources:
        for raw_block in source:
            block = _object_to_dict(raw_block)
            if not block:
                continue
            blocks.append(block)
            block_type = str(block.get("type") or "")
            text = block.get("text") or block.get("content")
            if block_type == "text" and text:
                text_parts.append(str(text))
    return blocks, ("".join(text_parts).strip() or None)


def _message_trace_matches_target(
    message: Dict[str, Any],
    target_model: Optional[str],
    *,
    target_provider: Optional[str] = None,
) -> bool:
    """Whether provider-specific fields in ``message`` can be sent to target."""
    if not target_model:
        return True
    trace_provider = message.get(TRACE_PROVIDER_KEY)
    trace_model = message.get(TRACE_MODEL_KEY)
    if not trace_provider and not trace_model:
        return True
    return trace_model_matches(
        trace_provider,
        trace_model,
        target_model,
        current_provider=target_provider,
    )


def _model_matches(model: str, entries: List[str]) -> bool:
    """Check if model name matches any entry (exact or prefix with version suffix)."""
    if not model:
        return False
    m = model.lower().strip()
    for e in entries:
        if m == e or m.startswith(e + "-"):
            return True
    return False


def _get_opt_in_payload(model: str, opt_in: Dict[str, dict]) -> Optional[dict]:
    """Return extra_body payload for opt-in thinking models, or None."""
    if not model:
        return None
    m = model.lower().strip()
    for key, payload in opt_in.items():
        if m == key or m.startswith(key + "-"):
            return payload
    return None


def get_thinking_extra_body(model: str) -> Optional[dict]:
    """Return extra_body for thinking mode, or None.

    - Auto-thinking models (_AUTO_THINKING_MODELS: deepseek-reasoner, deepseek-r1, qwq):
      These models automatically return reasoning_content in API responses; sending
      extra_body would cause 400 because the API already enables thinking by default.
      Return None to avoid duplicate activation.
    - Opt-in models (_OPT_IN_THINKING_MODELS: deepseek-chat): Return the activation
      payload to explicitly enable thinking mode.
    - All other models: Return None (no thinking mode).
    """
    if _model_matches(model, _AUTO_THINKING_MODELS):
        return None
    return _get_opt_in_payload(model, _OPT_IN_THINKING_MODELS)


def resolve_fallback_litellm_wire_models(
    model: str,
    model_list: Optional[List[Dict[str, Any]]] = None,
) -> List[str]:
    """Resolve all wire models reachable from a configured alias."""
    normalized_model = (model or "").strip()
    if not normalized_model:
        return []

    resolved: List[str] = []
    if model_list:
        for entry in model_list:
            if not isinstance(entry, dict):
                continue
            entry_model_name = str(entry.get("model_name", "") or "").strip()
            if not entry_model_name:
                entry_params = entry.get("litellm_params", {}) or {}
                entry_model_name = str(entry_params.get("model") or "").strip()
            if entry_model_name != normalized_model:
                continue

            entry_params = entry.get("litellm_params", {}) or {}
            wire_model = str(entry_params.get("model") or normalized_model).strip()
            if wire_model and wire_model not in resolved:
                resolved.append(wire_model)

    if not resolved:
        wire_model = resolve_litellm_wire_model(normalized_model, model_list)
        if wire_model and wire_model not in resolved:
            resolved.append(wire_model)
    return resolved


# ============================================================
# LLM Tool Adapter
# ============================================================

class LLMToolAdapter:
    """Unified adapter for tool-calling via LiteLLM.

    Supports providers (Gemini, OpenAI, DeepSeek, etc.) through
    a single litellm.completion() interface with optional channel routing.
    """

    def __init__(self, config=None):
        config = config or get_config()
        self._config = config
        self._router = None
        self._litellm_available = False
        self._init_litellm()
    def _has_channel_config(self) -> bool:
        """Check if multi-channel config (channels / YAML) is active."""
        return bool(self._config.llm_model_list) and not all(
            e.get('model_name', '').startswith('__legacy_') for e in self._config.llm_model_list
        )

    def _init_litellm(self) -> None:
        """Initialize litellm Router from channels / YAML / legacy keys."""
        config = self._config
        litellm_model = get_effective_agent_primary_model(config)
        if not litellm_model:
            logger.warning("Agent LLM: no effective primary model configured")
            return

        self._litellm_available = True

        # --- Channel / YAML path ---
        if self._has_channel_config():
            model_list = config.llm_model_list
            self._router = Router(
                model_list=model_list,
                routing_strategy="simple-shuffle",
                num_retries=2,
            )
            unique_models = list(dict.fromkeys(
                e['litellm_params']['model'] for e in model_list
            ))
            logger.info(
                f"Agent LLM: Router initialized from channels/YAML — "
                f"{len(model_list)} deployment(s), models: {unique_models}"
            )
            return

        # --- Legacy path ---
        keys = get_api_keys_for_model(litellm_model, config)
        if not keys:
            logger.info(
                f"Agent LLM: litellm initialized (model={litellm_model}, "
                f"API key from environment)"
            )
            return

        logger.info(f"Agent LLM: litellm initialized (model={litellm_model})")

    @property
    def is_available(self) -> bool:
        """True if litellm is configured and at least one API key is present."""
        return self._router is not None or self._litellm_available

    @property
    def primary_provider(self) -> str:
        """Provider name extracted from litellm_model prefix."""
        model = get_effective_agent_primary_model(self._config)
        if "/" in model:
            return model.split("/")[0]
        return model or "none"

    # ============================================================
    # Unified call
    # ============================================================

    def call_with_tools(
        self,
        messages: List[Dict[str, Any]],
        tools: List[dict],
        provider: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> LLMResponse:
        """Send messages + tool declarations to LLM, return normalized response.

        Args:
            messages: Conversation history in provider-neutral format:
                      [{"role": "system"/"user"/"assistant"/"tool", "content": ...}, ...]
            tools: OpenAI-format tool declarations; litellm converts to each provider's format.
            provider: Ignored (kept for backward compatibility).

        Returns:
            LLMResponse with either content (final answer) or tool_calls.
        """
        return self.call_completion(messages, tools=tools, provider=provider, timeout=timeout)

    def call_text(
        self,
        messages: List[Dict[str, Any]],
        *,
        provider: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> LLMResponse:
        """Send a text-only completion through the shared routing stack."""
        return self.call_completion(
            messages,
            tools=None,
            provider=provider,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout,
        )

    def call_completion(
        self,
        messages: List[Dict[str, Any]],
        *,
        tools: Optional[List[dict]] = None,
        provider: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> LLMResponse:
        """Shared completion path for both tool and text-only calls."""
        model = get_effective_agent_primary_model(self._config)
        if not model:
            error_msg = (
                "No LLM configured. Please set LITELLM_MODEL, LLM_CHANNELS, "
                "or provider API keys before using Agent."
            )
            logger.error(error_msg)
            return LLMResponse(content=error_msg, provider="error")
        try:
            return self._call_litellm_model(
                messages,
                tools or [],
                model,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=timeout,
            )
        except Exception as exc:
            error_detail = sanitize_diagnostic_text(exc) or type(exc).__name__
            error_msg = f"LLM model {model} failed: {error_detail}"
            logger.error(error_msg)
            return LLMResponse(content=error_msg, provider="error", model=model)

    def _call_litellm_model(
        self,
        messages: List[Dict[str, Any]],
        tools: List[dict],
        model: str,
        *,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> LLMResponse:
        """Call a specific litellm model with OpenAI-format messages and tools."""
        openai_messages = self._convert_messages(messages, target_model=model)

        # Use short model name (without provider prefix) for thinking model lookup
        model_short = model.split("/")[-1] if "/" in model else model
        extra = get_thinking_extra_body(model_short)

        call_kwargs: Dict[str, Any] = {
            "model": model,
            "messages": openai_messages,
        }
        if max_tokens is not None:
            call_kwargs["max_tokens"] = max_tokens
        if timeout is not None:
            call_kwargs["timeout"] = timeout

        if extra:
            call_kwargs["extra_body"] = extra

        if tools:
            call_kwargs["tools"] = tools

        # Use the channel Router where configured, direct litellm for other models.
        use_channel_router = self._has_channel_config()
        _router_model_names = set(get_configured_llm_models(self._config.llm_model_list))
        uses_router = bool(use_channel_router and self._router and model in _router_model_names)
        recovery_model_list = self._config.llm_model_list
        if not uses_router:
            keys = get_api_keys_for_model(model, self._config)
            if keys:
                call_kwargs["api_key"] = keys[0]
            call_kwargs.update(extra_litellm_params(model, self._config))
        call_kwargs = apply_litellm_generation_params(
            call_kwargs,
            model,
            self._get_temperature() if temperature is None else temperature,
            model_list=recovery_model_list,
        )
        register_fallback_model_pricing(
            resolve_fallback_litellm_wire_models(model, self._config.llm_model_list)
        )
        if use_channel_router and self._router and model in _router_model_names:
            # Channel / YAML path: Router manages all models in its model_list
            response = call_litellm_with_param_recovery(
                lambda kwargs: self._router.completion(**kwargs),
                model=model,
                call_kwargs=call_kwargs,
                model_list=recovery_model_list,
                logger=logger,
            )
        else:
            # Legacy/direct-env path: direct call (also handles direct-env
            # providers like groq/ or bedrock/ that are not in the Router
            # model_list even when channel mode is active)
            response = call_litellm_with_param_recovery(
                lambda kwargs: litellm.completion(**kwargs),
                model=model,
                call_kwargs=call_kwargs,
                model_list=self._config.llm_model_list,
                logger=logger,
            )

        return self._parse_litellm_response(
            response,
            model,
            openai_messages,
            model_list=recovery_model_list,
        )

    def _get_temperature(self) -> float:
        """Return the raw configured temperature before per-model normalization."""
        return float(self._config.llm_temperature)

    def _convert_messages(
        self,
        messages: List[Dict[str, Any]],
        *,
        target_model: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Convert internal message format to OpenAI-compatible format for litellm."""
        openai_messages: List[Dict[str, Any]] = []
        target_provider = self._trace_provider_for_target(target_model)
        for msg in messages:
            trace_matches_target = _message_trace_matches_target(
                msg,
                target_model,
                target_provider=target_provider,
            )
            if not trace_matches_target:
                continue
            if msg["role"] == "tool":
                openai_messages.append({
                    "role": "tool",
                    "tool_call_id": msg.get("tool_call_id", ""),
                    "content": msg["content"] if isinstance(msg["content"], str) else json.dumps(msg["content"]),
                })
            elif msg["role"] == "assistant" and msg.get("tool_calls"):
                openai_tc = []
                for tc in msg["tool_calls"]:
                    tc_dict: Dict[str, Any] = {
                        "id": tc.get("id", str(uuid.uuid4())[:8]),
                        "type": "function",
                        "function": {
                            "name": tc["name"],
                            "arguments": json.dumps(tc["arguments"]),
                        },
                    }
                    provider_specific_fields = dict(tc.get("provider_specific_fields") or {})
                    sig = tc.get("thought_signature")
                    if sig is not None:
                        provider_specific_fields.setdefault("thought_signature", sig)
                    if provider_specific_fields:
                        tc_dict["provider_specific_fields"] = provider_specific_fields
                    openai_tc.append(tc_dict)
                content = (
                    msg.get("provider_blocks")
                    if msg.get("provider_blocks")
                    else msg.get("content")
                )
                openai_msg: Dict[str, Any] = {
                    "role": "assistant",
                    "content": content,
                    "tool_calls": openai_tc,
                }
                if msg.get("reasoning_content") is not None:
                    openai_msg["reasoning_content"] = msg["reasoning_content"]
                openai_messages.append(openai_msg)
            else:
                openai_messages.append({
                    "role": msg["role"],
                    "content": msg["content"],
                })
        return openai_messages

    def _trace_provider_for_target(self, target_model: Optional[str]) -> str:
        if not target_model:
            return ""
        model_list = getattr(getattr(self, "_config", None), "llm_model_list", []) or []
        return resolved_provider_namespace(target_model, model_list)

    def _parse_litellm_response(
        self,
        response: Any,
        model: str,
        messages: Optional[List[Dict[str, Any]]] = None,
        *,
        model_list: Optional[List[Dict[str, Any]]] = None,
    ) -> LLMResponse:
        """Parse litellm OpenAI-compatible response into LLMResponse."""
        choice = response.choices[0]
        tool_calls: List[ToolCall] = []

        provider_blocks, provider_text = _extract_provider_blocks(choice)

        text_content = choice.message.content
        if isinstance(text_content, list):
            text_content = provider_text
        if text_content is None:
            text_content = provider_text

        # DeepSeek/Qwen thinking mode; not in standard OpenAI type, accessed via getattr
        reasoning_content = getattr(choice.message, "reasoning_content", None)

        if choice.message.tool_calls:
            for tc in choice.message.tool_calls:
                args: Dict[str, Any] = {}
                if tc.function.arguments:
                    try:
                        args = json.loads(tc.function.arguments)
                    except json.JSONDecodeError:
                        args = {"raw": tc.function.arguments}

                provider_specific_fields = _provider_specific_fields_from(
                    getattr(tc, "provider_specific_fields", None)
                )
                provider_specific_fields.update(
                    _provider_specific_fields_from(
                        getattr(tc.function, "provider_specific_fields", None)
                    )
                )
                sig = provider_specific_fields.get("thought_signature")
                if sig is None:
                    sig = getattr(tc, "thought_signature", None)

                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=args,
                    thought_signature=sig,
                    provider_specific_fields=provider_specific_fields,
                ))

        usage_model_list = (
            model_list
            if model_list is not None
            else getattr(getattr(self, "_config", None), "llm_model_list", []) or []
        )
        usage_model, provider_name = resolved_model_provider_identity(model, usage_model_list)
        usage_payload = extract_usage_payload(response)
        if usage_payload:
            usage = normalize_litellm_usage(
                usage_payload,
                model=usage_model or model,
                provider=provider_name,
            )
            usage = attach_message_hmacs(usage, messages)
        else:
            usage = {}
        return LLMResponse(
            content=text_content,
            tool_calls=tool_calls,
            reasoning_content=reasoning_content,
            provider_blocks=provider_blocks,
            usage=usage,
            provider=provider_name,
            model=model,
            raw=response,
        )


def register_fallback_model_pricing(models: Iterable[str]) -> None:
    """Register zero-cost pricing for unknown OpenAI-compatible models."""
    if not models:
        return
    register = getattr(litellm, "register_model", None)
    if not callable(register):
        return
    cost_map = getattr(litellm, "model_cost", {})
    if not isinstance(cost_map, dict):
        cost_map = {}
    for model in models:
        provider, wire_model = _split_provider_model(str(model))
        if provider != "openai":
            continue
        if not wire_model or wire_model.startswith("__legacy_"):
            continue
        if wire_model in cost_map or wire_model in _FALLBACK_MODEL_PRICING_REGISTERED:
            continue
        try:
            register({wire_model: dict(_FALLBACK_MODEL_PRICING)})
            _FALLBACK_MODEL_PRICING_REGISTERED.add(wire_model)
            logger.debug("Registered fallback pricing for %s", wire_model)
        except Exception as exc:
            logger.debug("Fallback pricing registration skipped for %s: %s", wire_model, exc)
