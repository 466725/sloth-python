from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Protocol

NewsItem = Dict[str, Any]


class NewsFetcher(Protocol):
    """Protocol for concrete news fetchers."""

    def fetch_company_news(self, symbol: str, market: str = "cn", limit: int = 20) -> List[NewsItem]:
        ...


@dataclass
class FetchResult:
    source: str
    items: List[NewsItem]


def utc_iso_from_epoch(value: Any) -> Optional[str]:
    """Convert epoch seconds to UTC ISO string if possible."""
    if value is None:
        return None
    try:
        return datetime.fromtimestamp(float(value), tz=timezone.utc).isoformat()
    except (TypeError, ValueError, OSError):
        return None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def deduplicate_news(items: List[NewsItem]) -> List[NewsItem]:
    """Deduplicate by URL first, then by normalized title."""
    seen = set()
    result: List[NewsItem] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        url = normalize_text(item.get("url"))
        title = normalize_text(item.get("title")).lower()
        key = (url or "", title)
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def limit_news(items: List[NewsItem], limit: int) -> List[NewsItem]:
    if limit <= 0:
        return []
    return items[:limit]
