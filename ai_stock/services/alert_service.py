# -*- coding: utf-8 -*-
"""Service layer for Alert API MVP."""

from __future__ import annotations

import asyncio
import json
import logging
import math
import re
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict, Optional

from ai_stock.agent.events import (
    EventMonitor,
    PriceChangeAlert,
    _read_quote_float,
    validate_event_alert_rule,
)
from ai_stock.analysis_context_pack_overview import (
    ANALYSIS_CONTEXT_PACK_OVERVIEW_KEY,
    extract_analysis_context_pack_overview,
)
from ai_stock.market_phase_summary import MARKET_PHASE_SUMMARY_KEY, extract_market_phase_summary
from ai_stock.repositories.alert_repo import AlertRepository

from ai_stock.services.decision_signal_summary import summarize_decision_signal
from ai_stock.storage import (
    AlertCooldownRecord,
    AlertNotificationRecord,
    AlertRuleRecord,
    AlertTriggerRecord,
    DatabaseManager,
)
from ai_stock.utils.sanitize import sanitize_diagnostic_text

SUPPORTED_ALERT_TYPES = frozenset({"price_change_percent"})
SUPPORTED_TARGET_SCOPES = frozenset({"single_symbol"})
SUPPORTED_SEVERITIES = frozenset({"info", "warning", "critical"})
NULLABLE_RULE_UPDATE_FIELDS = frozenset({"cooldown_policy", "notification_policy"})

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RuntimeAlertPayload:
    """Runtime rule plus the identity used for cooldown/history."""

    key: str
    rule: Any
    effective_target: str
    display_target: str


class AlertServiceError(ValueError):
    """Raised when alert service input is invalid."""

    error_code = "validation_error"


class AlertNotFoundError(AlertServiceError):
    """Raised when an alert resource does not exist."""

    error_code = "not_found"


class UnsupportedAlertTypeError(AlertServiceError):
    """Raised when a caller requests an alert type other than price change."""

    error_code = "unsupported_alert_type"


class AlertService:
    """Business logic for alert rule CRUD and dry-run evaluation."""

    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db = db_manager or DatabaseManager.get_instance()
        self.repo = AlertRepository(self.db)

    def create_rule(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        fields = self._normalize_rule_payload(payload)
        return self._serialize_rule(self.repo.create_rule(fields))

    def get_rule(self, rule_id: int) -> Dict[str, Any]:
        row = self.repo.get_rule(rule_id)
        if row is None:
            raise AlertNotFoundError(f"Alert rule not found: {rule_id}")
        return self._serialize_rule(row)

    def update_rule(self, rule_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        row = self.repo.get_rule(rule_id)
        if row is None:
            raise AlertNotFoundError(f"Alert rule not found: {rule_id}")
        if not payload:
            raise AlertServiceError("No fields provided for update")
        self._validate_rule_update_payload(payload)

        merged = self._serialize_rule_base(row)
        merged.update(payload)
        fields = self._normalize_rule_payload(merged, source=merged.get("source") or "api")
        fields["name"] = row.name
        updated = self.repo.update_rule(rule_id, fields)
        if updated is None:
            raise AlertNotFoundError(f"Alert rule not found: {rule_id}")
        return self._serialize_rule(updated)

    def delete_rule(self, rule_id: int) -> bool:
        return self.repo.delete_rule(rule_id)

    def enable_rule(self, rule_id: int, enabled: bool) -> Dict[str, Any]:
        updated = self.repo.update_rule(rule_id, {"enabled": enabled})
        if updated is None:
            raise AlertNotFoundError(f"Alert rule not found: {rule_id}")
        return self._serialize_rule(updated)

    def list_rules(
        self,
        *,
        enabled: Optional[bool] = None,
        alert_type: Optional[str] = None,
        target_scope: Optional[str] = None,
        target: Optional[str] = None,
        source: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        rows, total = self.repo.list_rules(
            enabled=enabled,
            alert_type=alert_type,
            target_scope=target_scope,
            target=target,
            source=source,
            page=page,
            page_size=page_size,
        )
        return {
            "items": [self._serialize_rule(row) for row in rows],
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    def test_rule(self, rule_id: int) -> Dict[str, Any]:
        row = self.repo.get_rule(rule_id)
        if row is None:
            raise AlertNotFoundError(f"Alert rule not found: {rule_id}")

        payload = self.build_runtime_payload(row)
        if payload is None:
            return {
                "rule_id": rule_id,
                "target_scope": None,
                "status": "evaluation_error",
                "triggered": False,
                "observed_value": None,
                "message": "Alert rule has an unsupported target scope or type",
                "evaluated_count": 0,
                "triggered_count": 0,
                "degraded_count": 0,
                "skipped_count": 0,
                "target_results": [],
            }
        monitor = EventMonitor()
        try:
            result = asyncio.run(self._evaluate_rule(payload.rule, monitor, daily_cache=None))
            return self._dry_run_response_for_single(payload, result)
        except Exception as exc:
            sanitized_message = self._sanitize_text(str(exc) or "Alert evaluation failed")
            return {
                "rule_id": rule_id,
                "target_scope": row.target_scope,
                "status": "evaluation_error",
                "record_status": "failed",
                "triggered": False,
                "observed_value": None,
                "threshold": None,
                "data_source": None,
                "data_timestamp": None,
                "reason": sanitized_message,
                "message": sanitized_message,
                "evaluated_count": 0,
                "triggered_count": 0,
                "degraded_count": 0,
                "skipped_count": 0,
                "target_results": [],
            }

    async def _evaluate_rule(
        self,
        rule,
        monitor: EventMonitor,
        daily_cache: Optional[Dict[Any, Any]] = None,
    ) -> Dict[str, Any]:
        if isinstance(rule, PriceChangeAlert):
            return await self._evaluate_price_change(rule, monitor)
        return self._evaluation_error(rule, f"unsupported runtime alert type: {rule.alert_type}")

    @staticmethod
    def _dry_run_response_for_single(payload: RuntimeAlertPayload, result: Dict[str, Any]) -> Dict[str, Any]:
        target_result = {
            "target": payload.effective_target,
            "display_target": payload.display_target,
            "status": result.get("status") or "evaluation_error",
            "record_status": result.get("record_status"),
            "triggered": bool(result.get("triggered")),
            "observed_value": result.get("observed_value"),
            "threshold": result.get("threshold"),
            "message": result.get("message") or result.get("reason") or "",
        }
        response = {
            "rule_id": result.get("rule_id") or 0,
            "target_scope": "single_symbol",
            "status": result.get("status") or "evaluation_error",
            "triggered": bool(result.get("triggered")),
            "observed_value": result.get("observed_value"),
            "message": result.get("message") or result.get("reason") or "",
            "evaluated_count": 1,
            "triggered_count": 1 if result.get("triggered") else 0,
            "degraded_count": 1 if result.get("record_status") == "degraded" else 0,
            "skipped_count": 1 if result.get("record_status") == "skipped" else 0,
            "target_results": [target_result],
        }
        return response


    async def _evaluate_price_change(self, rule: PriceChangeAlert, monitor: EventMonitor) -> Dict[str, Any]:
        threshold = abs(float(rule.change_pct))
        try:
            quote = await monitor._get_realtime_quote(rule.stock_code)
        except Exception as exc:
            return self._evaluation_error(
                rule,
                exc,
                threshold=threshold,
                data_source="realtime_quote",
            )
        if quote is None:
            return self._not_triggered(
                rule,
                None,
                "No realtime quote available",
                record_status="skipped",
                threshold=threshold,
                data_source="realtime_quote",
            )

        current_change_pct = _read_quote_float(
            quote,
            "change_pct",
            "change_percent",
            "pct_chg",
            "change_rate",
        )
        if current_change_pct is None:
            return self._not_triggered(
                rule,
                None,
                "No valid realtime change percent available",
                record_status="skipped",
                threshold=threshold,
                data_source="realtime_quote",
                data_timestamp=self._extract_quote_datetime(quote),
            )

        direction = rule.direction.lower()
        triggered = (
            (direction == "up" and current_change_pct >= threshold)
            or (direction == "down" and current_change_pct <= -threshold)
        )
        if triggered:
            return self._triggered(
                rule,
                current_change_pct,
                f"{rule.stock_code} change {direction} {threshold:.2f}%: current = {current_change_pct:+.2f}%",
                threshold=threshold,
                data_source="realtime_quote",
                data_timestamp=self._extract_quote_datetime(quote),
            )
        return self._not_triggered(
            rule,
            current_change_pct,
            f"{rule.stock_code} change {current_change_pct:+.2f}% did not cross {direction} {threshold:.2f}%",
            threshold=threshold,
            data_source="realtime_quote",
            data_timestamp=self._extract_quote_datetime(quote),
        )



    def _triggered(
        self,
        rule,
        observed_value: Any,
        message: str,
        *,
        threshold: Optional[float] = None,
        data_source: Optional[str] = None,
        data_timestamp: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        sanitized_message = self._sanitize_text(message)
        return {
            "rule_id": self._runtime_rule_id(rule),
            "status": "triggered",
            "record_status": "triggered",
            "triggered": True,
            "observed_value": observed_value,
            "threshold": threshold,
            "data_source": data_source,
            "data_timestamp": data_timestamp,
            "reason": sanitized_message,
            "message": sanitized_message,
        }

    def _not_triggered(
        self,
        rule,
        observed_value: Any,
        message: str,
        *,
        record_status: Optional[str] = None,
        threshold: Optional[float] = None,
        data_source: Optional[str] = None,
        data_timestamp: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        sanitized_message = self._sanitize_text(message)
        return {
            "rule_id": self._runtime_rule_id(rule),
            "status": "not_triggered",
            "record_status": record_status,
            "triggered": False,
            "observed_value": observed_value,
            "threshold": threshold,
            "data_source": data_source,
            "data_timestamp": data_timestamp,
            "reason": sanitized_message,
            "message": sanitized_message,
        }

    def _evaluation_error(
        self,
        rule,
        exc: Any,
        *,
        threshold: Optional[float] = None,
        data_source: Optional[str] = None,
        data_timestamp: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        sanitized_message = self._sanitize_text(str(exc) or "Alert evaluation failed")
        return {
            "rule_id": self._runtime_rule_id(rule),
            "status": "evaluation_error",
            "record_status": "failed",
            "triggered": False,
            "observed_value": None,
            "threshold": threshold if threshold is not None else self._threshold_for_rule(rule),
            "data_source": data_source if data_source is not None else self._data_source_for_rule(rule),
            "data_timestamp": data_timestamp,
            "reason": sanitized_message,
            "message": sanitized_message,
        }

    @staticmethod
    def _runtime_rule_id(rule) -> int:
        return int(rule.metadata.get("persisted_rule_id", 0) or 0)

    @staticmethod
    def _threshold_for_rule(rule) -> Optional[float]:
        if isinstance(rule, PriceChangeAlert):
            return abs(float(rule.change_pct))
        return None

    @staticmethod
    def _data_source_for_rule(rule) -> Optional[str]:
        if isinstance(rule, PriceChangeAlert):
            return "realtime_quote"
        return None

    @classmethod
    def _extract_quote_datetime(cls, quote: Any) -> Optional[datetime]:
        for field_name in (
            "data_timestamp",
            "timestamp",
            "quote_time",
            "trade_time",
            "update_time",
            "updated_at",
            "datetime",
            "date",
        ):
            raw_value = cls._read_quote_field(quote, field_name)
            parsed = cls._coerce_datetime(raw_value)
            if parsed is not None:
                return parsed
        return None

    @staticmethod
    def _read_quote_field(quote: Any, field_name: str) -> Any:
        if quote is None:
            return None
        if isinstance(quote, dict):
            return quote.get(field_name)
        raw_value = getattr(quote, field_name, None)
        if raw_value is not None:
            return raw_value
        if hasattr(quote, "to_dict"):
            try:
                return quote.to_dict().get(field_name)
            except Exception:
                return None
        return None


    @staticmethod
    def _coerce_datetime(value: Any) -> Optional[datetime]:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.replace(tzinfo=None) if value.tzinfo is not None else value
        if isinstance(value, date):
            return datetime.combine(value, datetime.min.time())
        if hasattr(value, "to_pydatetime"):
            try:
                parsed = value.to_pydatetime()
                return parsed.replace(tzinfo=None) if parsed.tzinfo is not None else parsed
            except Exception:
                return None
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            try:
                if isinstance(value, float):
                    if not value.is_integer():
                        return None
                    numeric_value = int(value)
                else:
                    numeric_value = int(value)
            except (OverflowError, ValueError):
                return None
            # Numeric provider timestamps are ambiguous (seconds, millis, or
            # compact trade dates). Only accept the explicit YYYYMMDD shape.
            numeric_text = str(numeric_value)
            if re.fullmatch(r"\d{8}", numeric_text):
                try:
                    return datetime.strptime(numeric_text, "%Y%m%d")
                except ValueError:
                    return None
            return None

        text = str(value).strip()
        if not text:
            return None
        if re.fullmatch(r"\d{8}", text):
            try:
                return datetime.strptime(text, "%Y%m%d")
            except ValueError:
                return None
        try:
            parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
            return parsed.replace(tzinfo=None) if parsed.tzinfo is not None else parsed
        except ValueError:
            return None

    def list_triggers(
        self,
        *,
        rule_id: Optional[int] = None,
        target: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        rows, total = self.repo.list_triggers(
            rule_id=rule_id,
            target=target,
            status=status,
            page=page,
            page_size=page_size,
        )
        return {
            "items": [self._serialize_trigger(row) for row in rows],
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    def list_notifications(
        self,
        *,
        trigger_id: Optional[int] = None,
        channel: Optional[str] = None,
        success: Optional[bool] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        rows, total = self.repo.list_notifications(
            trigger_id=trigger_id,
            channel=channel,
            success=success,
            page=page,
            page_size=page_size,
        )
        return {
            "items": [self._serialize_notification(row) for row in rows],
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    def _normalize_rule_payload(self, payload: Dict[str, Any], *, source: str = "api") -> Dict[str, Any]:
        target_scope = str(payload.get("target_scope") or "single_symbol").strip()
        if target_scope not in SUPPORTED_TARGET_SCOPES:
            raise AlertServiceError(f"unsupported target_scope: {target_scope}")

        target = str(payload.get("target") or "").strip()
        if not target:
            raise AlertServiceError("target is required")

        alert_type = str(payload.get("alert_type") or "").strip().lower()
        if alert_type not in SUPPORTED_ALERT_TYPES:
            raise UnsupportedAlertTypeError(f"unsupported alert_type for Alert API: {alert_type or '<empty>'}")

        severity = str(payload.get("severity") or "warning").strip().lower()
        if severity not in SUPPORTED_SEVERITIES:
            raise AlertServiceError(f"unsupported severity: {severity}")

        parameters = self._normalize_parameters(alert_type, payload.get("parameters") or {})
        target = target.strip()
        serialized_rule = {"stock_code": target, "alert_type": alert_type, **parameters}
        try:
            validate_event_alert_rule(serialized_rule)
        except ValueError as exc:
            raise AlertServiceError(str(exc)) from exc

        return {
            "name": self._default_rule_name(target=target, alert_type=alert_type, parameters=parameters),
            "target_scope": target_scope,
            "target": target,
            "alert_type": alert_type,
            "parameters": self._dump_json(parameters),
            "severity": severity,
            "enabled": bool(payload.get("enabled", True)),
            "source": str(source or "api")[:16],
            "cooldown_policy": self._dump_json_or_none(payload.get("cooldown_policy")),
            "notification_policy": self._dump_json_or_none(payload.get("notification_policy")),
        }

    def _validate_rule_update_payload(self, payload: Dict[str, Any]) -> None:
        for field_name, value in payload.items():
            if value is None and field_name not in NULLABLE_RULE_UPDATE_FIELDS:
                raise AlertServiceError(f"{field_name} must not be null")


    def _normalize_parameters(self, alert_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(parameters, dict):
            raise AlertServiceError("parameters must be an object")

        if alert_type == "price_change_percent":
            direction = str(parameters.get("direction") or "up").strip().lower()
            if direction not in {"up", "down"}:
                raise AlertServiceError(f"invalid direction: {direction}")
            return {
                "direction": direction,
                "change_pct": self._positive_float(parameters.get("change_pct"), "change_pct"),
            }

        raise UnsupportedAlertTypeError(f"unsupported alert_type for Alert API: {alert_type}")

    @staticmethod
    def _positive_float(value: Any, field_name: str) -> float:
        try:
            number = float(value)
        except (TypeError, ValueError) as exc:
            raise AlertServiceError(f"invalid {field_name}: {value}") from exc
        if not math.isfinite(number) or number <= 0:
            raise AlertServiceError(f"{field_name} must be finite and > 0")
        return number

    def build_runtime_payload(self, row: AlertRuleRecord) -> RuntimeAlertPayload | None:
        data = self._serialize_rule_base(row)
        if data["target_scope"] not in SUPPORTED_TARGET_SCOPES or data["alert_type"] not in SUPPORTED_ALERT_TYPES:
            logger.info(
                "[AlertService] Skipping retired alert rule %s with scope=%s type=%s",
                data["id"],
                data["target_scope"],
                data["alert_type"],
            )
            return None
        parent_key = self._semantic_key(
            data["target_scope"],
            data["target"],
            data["alert_type"],
            data["parameters"],
        )
        rule = self._to_runtime_rule(row, data)
        effective_target = str(data["target"])
        return RuntimeAlertPayload(
            key=parent_key,
            rule=rule,
            effective_target=effective_target,
            display_target=effective_target,
        )

    def _to_runtime_rule(self, row: AlertRuleRecord, data: Optional[Dict[str, Any]] = None):
        data = data or self._serialize_rule_base(row)
        parameters = data["parameters"]
        metadata = {
            "persisted_rule_id": data["id"],
            "target_scope": data.get("target_scope"),
            "parent_target": row.target,
            "effective_target": data.get("target"),
        }
        if data["alert_type"] == "price_change_percent":
            return PriceChangeAlert(
                stock_code=data["target"],
                direction=str(parameters["direction"]),
                change_pct=float(parameters["change_pct"]),
                metadata=metadata,
            )
        raise UnsupportedAlertTypeError(f"unsupported alert_type for Alert API: {data['alert_type']}")

    @staticmethod
    def _semantic_key(target_scope: str, target: str, alert_type: str, parameters: Dict[str, Any]) -> str:
        canonical_params = json.dumps(parameters or {}, ensure_ascii=False, sort_keys=True)
        return f"{target_scope}:{target}:{alert_type}:{canonical_params}"

    def _serialize_rule(self, row: AlertRuleRecord) -> Dict[str, Any]:
        data = self._serialize_rule_base(row)
        cooldown_summary = self._cooldown_summary_for_rule(row)
        data.update({
            "last_triggered_at": cooldown_summary.get("last_triggered_at"),
            "cooldown_until": cooldown_summary.get("cooldown_until"),
            "cooldown_active": cooldown_summary.get("cooldown_active"),
        })
        return data

    def _serialize_rule_base(self, row: AlertRuleRecord) -> Dict[str, Any]:
        parameters = self._load_json(row.parameters, default={})
        name = row.name
        if (
            row.alert_type == "price_change_percent"
            and "direction" in parameters
            and "change_pct" in parameters
            and name == f"{row.target} change {parameters['direction']} {parameters['change_pct']}%"
        ):
            name = self._default_rule_name(
                target=row.target,
                alert_type=row.alert_type,
                parameters=parameters,
            )
        return {
            "id": row.id,
            "name": name,
            "target_scope": row.target_scope,
            "target": row.target,
            "alert_type": row.alert_type,
            "parameters": parameters,
            "severity": row.severity,
            "enabled": bool(row.enabled),
            "source": row.source,
            "cooldown_policy": self._load_json(row.cooldown_policy, default=None),
            "notification_policy": self._load_json(row.notification_policy, default=None),
            "created_at": row.created_at.isoformat() if row.created_at else None,
            "updated_at": row.updated_at.isoformat() if row.updated_at else None,
        }

    def _cooldown_summary_for_rule(self, row: AlertRuleRecord) -> Dict[str, Any]:
        try:
            cooldown = self.repo.get_rule_cooldown_summary(
                rule_id=int(row.id),
                target=str(row.target),
                severity=str(row.severity) if row.severity else None,
            )
        except Exception as exc:
            logger.warning(
                "[AlertService] Failed to load alert cooldown summary for rule %s: %s",
                getattr(row, "id", "?"),
                self._sanitize_text(str(exc) or "cooldown summary read failed"),
            )
            return {"last_triggered_at": None, "cooldown_until": None, "cooldown_active": False}
        return self._serialize_cooldown_summary(cooldown)

    @staticmethod
    def _serialize_cooldown_summary(row: Optional[AlertCooldownRecord]) -> Dict[str, Any]:
        if row is None:
            return {"last_triggered_at": None, "cooldown_until": None, "cooldown_active": False}
        cooldown_active = bool(
            row.state == "active"
            and row.cooldown_until is not None
            and row.cooldown_until > datetime.now()
        )
        return {
            "last_triggered_at": row.last_triggered_at.isoformat() if row.last_triggered_at else None,
            "cooldown_until": row.cooldown_until.isoformat() if row.cooldown_until else None,
            "cooldown_active": cooldown_active,
        }

    def _serialize_trigger(self, row: AlertTriggerRecord) -> Dict[str, Any]:
        visibility = self._parse_analysis_visibility(row.diagnostics)
        return {
            "id": row.id,
            "rule_id": row.rule_id,
            "target": row.target,
            "observed_value": row.observed_value,
            "threshold": row.threshold,
            "reason": row.reason,
            "data_source": row.data_source,
            "data_timestamp": row.data_timestamp.isoformat() if row.data_timestamp else None,
            "triggered_at": row.triggered_at.isoformat() if row.triggered_at else None,
            "status": row.status,
            "diagnostics": self._sanitize_text(row.diagnostics) if row.diagnostics else None,
            "market_phase_summary": visibility.get("market_phase_summary"),
            "analysis_context_pack_overview": visibility.get("analysis_context_pack_overview"),
            "analysis_visibility_source": visibility.get("analysis_visibility_source"),
            "decision_signal_summary": visibility.get("decision_signal_summary"),
        }

    @staticmethod
    def _parse_analysis_visibility(diagnostics: Optional[str]) -> Dict[str, Any]:
        result = {
            "market_phase_summary": None,
            "analysis_context_pack_overview": None,
            "analysis_visibility_source": None,
            "decision_signal_summary": None,
        }
        if not diagnostics:
            return result
        try:
            parsed = json.loads(diagnostics)
        except (TypeError, ValueError, json.JSONDecodeError):
            result["analysis_visibility_source"] = "legacy_text"
            return result
        if not isinstance(parsed, dict):
            result["analysis_visibility_source"] = "legacy_text"
            return result
        result["decision_signal_summary"] = summarize_decision_signal(parsed.get("decision_signal_summary"))
        visibility = parsed.get("analysis_visibility")
        if not isinstance(visibility, dict):
            return result
        phase = extract_market_phase_summary({MARKET_PHASE_SUMMARY_KEY: visibility.get("market_phase_summary")})
        overview = extract_analysis_context_pack_overview(
            {ANALYSIS_CONTEXT_PACK_OVERVIEW_KEY: visibility.get("analysis_context_pack_overview")}
        )
        result["market_phase_summary"] = phase
        result["analysis_context_pack_overview"] = overview
        result["analysis_visibility_source"] = visibility.get("source")
        return result

    def _serialize_notification(self, row: AlertNotificationRecord) -> Dict[str, Any]:
        return {
            "id": row.id,
            "trigger_id": row.trigger_id,
            "channel": row.channel,
            "attempt": row.attempt,
            "success": bool(row.success),
            "error_code": row.error_code,
            "retryable": bool(row.retryable),
            "latency_ms": row.latency_ms,
            "diagnostics": self._sanitize_text(row.diagnostics) if row.diagnostics else None,
            "created_at": row.created_at.isoformat() if row.created_at else None,
        }

    @staticmethod
    def _default_rule_name(*, target: str, alert_type: str, parameters: Dict[str, Any]) -> str:
        if alert_type == "price_change_percent":
            return f"{target} {parameters['direction']} {parameters['change_pct']}%"
        return f"{target} {alert_type}"

    @staticmethod
    def _dump_json(value: Dict[str, Any]) -> str:
        return json.dumps(value, ensure_ascii=False, sort_keys=True)

    def _dump_json_or_none(self, value: Optional[Dict[str, Any]]) -> Optional[str]:
        if value is None:
            return None
        if not isinstance(value, dict):
            raise AlertServiceError("policy fields must be objects")
        return self._dump_json(value)

    @staticmethod
    def _load_json(raw: Optional[str], *, default: Any) -> Any:
        if raw is None or raw == "":
            return default
        try:
            return json.loads(raw)
        except (TypeError, json.JSONDecodeError):
            return default

    @staticmethod
    def _sanitize_text(text: Any) -> str:
        return sanitize_diagnostic_text(text)
