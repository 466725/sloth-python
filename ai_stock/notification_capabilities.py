# -*- coding: utf-8 -*-
"""Notification channel rendering capability profiles.

This module intentionally uses plain channel strings instead of importing
``NotificationChannel`` from ``src.notification``.  The notification service may
import these profiles later without creating a circular dependency.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional, Tuple


@dataclass(frozen=True)
class ChannelProfile:
    """Static rendering capabilities for one notification channel."""

    channel: str
    markdown: str
    default_mode: str
    max_text_chars: Optional[int] = None
    max_text_bytes: Optional[int] = None
    supports_card: bool = False
    supports_image: bool = False
    supports_file: bool = False
    supports_link: bool = True
    notes: str = ""


@dataclass(frozen=True)
class PreparedMessage:
    """A channel-specific prepared notification message.

    The object describes how a message is ready to be sent for a channel without
    changing the original report semantics.  Senders can consume the fields they
    support and fall back to ``fallback_text`` or ``text`` when a richer payload
    is unavailable.
    """

    channel: str
    text: str
    formatted_text: Optional[str] = None
    card_payload: Optional[Mapping[str, Any]] = None
    fallback_text: Optional[str] = None
    attachments: Tuple[Any, ...] = ()
    diagnostics: Tuple[str, ...] = ()

    @property
    def content_for_text_send(self) -> str:
        """Return the best text payload for legacy text senders."""

        return self.formatted_text or self.fallback_text or self.text


@dataclass(frozen=True)
class RendererPreset:
    """Reserved renderer plan for one notification channel.

    Presets document the intended renderer shape without changing today's
    runtime send path.  A future opt-in implementation can use these names to
    wire platform-specific renderers while keeping the legacy text fallback.
    """

    channel: str
    text_renderer: str
    markdown: str
    enabled_by_default: bool = False
    rich_renderer: Optional[str] = None
    image_renderer: Optional[str] = None
    fallback_renderer: str = "legacy_text"
    notes: str = ""


CHANNEL_PROFILES: Dict[str, ChannelProfile] = {
    "email": ChannelProfile(
        channel="email",
        markdown="html",
        default_mode="full_html",
        supports_image=True,
        supports_file=True,
        supports_link=True,
        notes="Email remains the high-fidelity full-report carrier.",
    ),
    "unknown": ChannelProfile(
        channel="unknown",
        markdown="plain_text",
        default_mode="plain_fallback",
        supports_link=False,
    ),
}


CHANNEL_RENDERER_PRESETS: Dict[str, RendererPreset] = {
    "email": RendererPreset(
        channel="email",
        text_renderer="email_html",
        markdown="html",
        rich_renderer="email_html",
        image_renderer="inline_image",
        enabled_by_default=True,
    ),
}


def normalize_channel_name(channel: Any) -> str:
    """Normalize enum-like or string channel values into profile keys."""

    value = getattr(channel, "value", channel)
    return str(value or "").strip().lower() or "unknown"


def get_channel_profile(channel: Any) -> ChannelProfile:
    """Return the channel profile, falling back to ``unknown``."""

    name = normalize_channel_name(channel)
    return CHANNEL_PROFILES.get(name, CHANNEL_PROFILES["unknown"])


def all_channel_profiles() -> Tuple[ChannelProfile, ...]:
    """Return all profiles in deterministic declaration order."""

    return tuple(CHANNEL_PROFILES.values())


def get_renderer_preset(channel: Any) -> RendererPreset:
    """Return the reserved renderer preset for ``channel``.

    Unknown channels use a plain text fallback preset and stay disabled.
    """

    name = normalize_channel_name(channel)
    return CHANNEL_RENDERER_PRESETS.get(
        name,
        RendererPreset(
            channel=name,
            text_renderer="plain_text",
            markdown="plain_text",
            notes="Fallback preset for channels without a dedicated renderer plan.",
        ),
    )


def all_renderer_presets() -> Tuple[RendererPreset, ...]:
    """Return all reserved renderer presets in deterministic declaration order."""

    return tuple(CHANNEL_RENDERER_PRESETS.values())
