"""Backward-compatible import for the renamed qTest client module."""

from .client import QTestClient

__all__ = ["QTestClient"]
