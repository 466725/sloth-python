# -*- coding: utf-8 -*-
"""
===================================
China A-Share Watchlist Analysis System - Main Orchestrator
===================================

Responsibilities:
1. Coordinate modules to complete the stock analysis workflow
2. Schedule a thread pool with low concurrency
3. Handle exceptions globally so a single stock failure does not affect the whole run
4. Provide a command-line entry point

Usage:
    python main.py              # Normal run
    python main.py --debug      # Debug mode
    python main.py --dry-run    # Fetch data only; do not analyze

Trading principles (incorporated into the analysis):
- Strict entry: Do not chase prices; do not buy when deviation exceeds 5%
- Trend trading: Only trade when MA5 > MA10 > MA20 (bullish alignment)
- Prioritize efficiency: Focus on stocks with concentrated holdings
- Preferred entry: Buy on a low-volume pullback to MA5/MA10 support
"""
from __future__ import annotations

import multiprocessing
import os
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from dotenv import dotenv_values
from ai_stock.config import setup_env

_INITIAL_PROCESS_ENV = dict(os.environ)
setup_env()

# Proxy configuration - controlled by the USE_PROXY environment variable; disabled by default
# Proxy configuration is automatically skipped in GitHub Actions
if os.getenv("GITHUB_ACTIONS") != "true" and os.getenv("USE_PROXY", "false").lower() == "true":
    # Enable the proxy in local development (configure PROXY_HOST and PROXY_PORT in .env)
    proxy_host = os.getenv("PROXY_HOST", "127.0.0.1")
    proxy_port = os.getenv("PROXY_PORT", "10809")
    proxy_url = f"http://{proxy_host}:{proxy_port}"
    os.environ["http_proxy"] = proxy_url
    os.environ["https_proxy"] = proxy_url

import argparse
import logging
import sys
import time
import uuid
from datetime import date, datetime, timezone

from ai_stock.webui_frontend import prepare_webui_frontend_assets
from ai_stock.config import get_config, Config
from ai_stock.logging_config import setup_logging
from ai_stock.services.stock_code_utils import resolve_index_stock_code_for_analysis


logger = logging.getLogger(__name__)
_RUNTIME_ENV_FILE_KEYS = set()
_PUBLIC_BIND_HOSTS = frozenset({"0.0.0.0", "::", "[::]", "*"})


def _get_active_env_path() -> Path:
    env_file = os.getenv("ENV_FILE")
    if env_file:
        return Path(env_file)
    return Path(__file__).resolve().parent / ".env"


def _is_public_bind_host(host: str) -> bool:
    return (host or "").strip().lower() in _PUBLIC_BIND_HOSTS


def _warn_if_public_webui(host: str) -> None:
    if not _is_public_bind_host(host):
        return

    logger.warning(
        "WEBUI_HOST=%s binds the Web UI to a public interface, but this service "
        "has no built-in authentication. Keep it behind a trusted network "
        "boundary or an authenticated reverse proxy.",
        host,
    )


def _read_active_env_values() -> Optional[Dict[str, str]]:
    env_path = _get_active_env_path()
    if not env_path.exists():
        return {}

    try:
        values = dotenv_values(env_path)
    except Exception as exc:  # pragma: no cover - defensive branch
        logger.warning("Failed to read config file %s; continuing with current environment variables: %s", env_path, exc)
        return None

    return {
        str(key): "" if value is None else str(value)
        for key, value in values.items()
        if key is not None
    }


_ACTIVE_ENV_FILE_VALUES = _read_active_env_values() or {}
_RUNTIME_ENV_FILE_KEYS = {
    key for key in _ACTIVE_ENV_FILE_VALUES
    if key not in _INITIAL_PROCESS_ENV
}

# setup_env() already ran at import time above.
_env_bootstrapped = True


def _bootstrap_environment() -> None:
    """Load .env and apply optional local proxy settings.

    Guarded to be idempotent so it can safely be called from lazy-import
    paths used by API / bot consumers.
    """
    global _env_bootstrapped
    if _env_bootstrapped:
        return

    from ai_stock.config import setup_env

    setup_env()

    if os.getenv("GITHUB_ACTIONS") != "true" and os.getenv("USE_PROXY", "false").lower() == "true":
        proxy_host = os.getenv("PROXY_HOST", "127.0.0.1")
        proxy_port = os.getenv("PROXY_PORT", "10809")
        proxy_url = f"http://{proxy_host}:{proxy_port}"
        os.environ["http_proxy"] = proxy_url
        os.environ["https_proxy"] = proxy_url

    _env_bootstrapped = True


def _setup_bootstrap_logging(debug: bool = False) -> None:
    """Initialize stderr-only logging before config is loaded.

    File handlers are deferred until ``config.log_dir`` is known (via the
    subsequent ``setup_logging()`` call) so that healthy runs never create
    log files in a hard-coded directory.
    """
    level = logging.DEBUG if debug else logging.INFO
    root = logging.getLogger()
    root.setLevel(level)
    if not any(
        isinstance(h, logging.StreamHandler) and getattr(h, "stream", None) is sys.stderr
        for h in root.handlers
    ):
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(level)
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        )
        root.addHandler(handler)


def _setup_runtime_logging(log_dir: str, debug: bool = False) -> bool:
    """Switch to configured logging, falling back to console on file I/O errors."""
    try:
        setup_logging(log_prefix="stock_analysis", debug=debug, log_dir=log_dir)
        return True
    except OSError as exc:
        logger.warning(
            "File logging initialization failed; falling back to console logging. "
            "The log directory %r is not writable or cannot be created: %s. "
            "The official Docker image entrypoint automatically repairs permissions "
            "on the default mounted directories. If the problem persists, check for "
            "write-restricting environments such as --user, read-only mounts, "
            "rootless Docker, or NFS.",
            log_dir,
            exc,
        )
        return False


def _get_stock_analysis_pipeline():
    """Lazily import StockAnalysisPipeline for external consumers.

    Also ensures env/proxy bootstrap has run so that API / bot consumers
    that never call ``main()`` still get ``USE_PROXY`` applied.
    """
    _bootstrap_environment()
    from ai_stock.core.pipeline import StockAnalysisPipeline as _Pipeline

    return _Pipeline


class _LazyPipelineDescriptor:
    """Descriptor that resolves StockAnalysisPipeline on first attribute access."""

    _resolved = None

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, obj, objtype=None):
        if self._resolved is None:
            self._resolved = _get_stock_analysis_pipeline()
        return self._resolved


class _ModuleExports:
    StockAnalysisPipeline = _LazyPipelineDescriptor()


_exports = _ModuleExports()


def __getattr__(name: str):
    if name == "StockAnalysisPipeline":
        return _exports.StockAnalysisPipeline
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def _reload_env_file_values_preserving_overrides() -> None:
    """Refresh `.env`-managed env vars without clobbering process env overrides."""
    global _RUNTIME_ENV_FILE_KEYS

    latest_values = _read_active_env_values()
    if latest_values is None:
        return

    managed_keys = {
        key for key in latest_values
        if key not in _INITIAL_PROCESS_ENV
    }

    for key in _RUNTIME_ENV_FILE_KEYS - managed_keys:
        os.environ.pop(key, None)

    for key in managed_keys:
        os.environ[key] = latest_values[key]

    _RUNTIME_ENV_FILE_KEYS = managed_keys


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='China A-Share Watchlist Analysis System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main.py                    # Normal run
  python main.py --debug            # Debug mode
  python main.py --dry-run          # Fetch data only; skip AI analysis
  python main.py --stocks 600519,000001  # Analyze specific stocks
  python main.py --no-notify        # Do not send notifications
  python main.py --check-notify     # Check notification settings without sending
  python main.py --single-notify    # Notify immediately after analyzing each stock
  python main.py --schedule         # Enable scheduled mode
  python main.py --market-review    # Run market review only
        '''
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode and output detailed logs'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Fetch data only; skip AI analysis'
    )

    parser.add_argument(
        '--stocks',
        type=str,
        help='Comma-separated stock codes to analyze (overrides the config file)'
    )

    parser.add_argument(
        '--no-notify',
        action='store_true',
        help='Do not send notifications'
    )

    parser.add_argument(
        '--check-notify',
        action='store_true',
        help='Check notification channel settings without sending notifications'
    )

    parser.add_argument(
        '--single-notify',
        action='store_true',
        help='Enable per-stock notifications: send after each analysis instead of sending a summary'
    )

    parser.add_argument(
        '--workers',
        type=int,
        default=None,
        help='Number of concurrent threads (defaults to the configured value)'
    )

    parser.add_argument(
        '--schedule',
        action='store_true',
        help='Enable scheduled mode and run daily'
    )

    parser.add_argument(
        '--no-run-immediately',
        action='store_true',
        help='Do not run immediately when scheduled mode starts'
    )

    parser.add_argument(
        '--market-review',
        action='store_true',
        help='Run market review only'
    )

    parser.add_argument(
        '--no-market-review',
        action='store_true',
        help='Skip market review analysis'
    )

    parser.add_argument(
        '--force-run',
        action='store_true',
        help='Skip the trading-day check and force a full analysis run (Issue #373)'
    )

    parser.add_argument(
        '--webui',
        action='store_true',
        help='Start the Web management interface'
    )

    parser.add_argument(
        '--webui-only',
        action='store_true',
        help='Start the Web service only; do not run automatic analysis'
    )

    parser.add_argument(
        '--serve',
        action='store_true',
        help='Start the FastAPI backend service and run analysis tasks'
    )

    parser.add_argument(
        '--serve-only',
        action='store_true',
        help='Start the FastAPI backend service only; do not run automatic analysis'
    )

    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='FastAPI service port (default: 8000)'
    )

    parser.add_argument(
        '--host',
        type=str,
        default='0.0.0.0',
        help='FastAPI service bind address (default: 0.0.0.0)'
    )

    parser.add_argument(
        '--no-context-snapshot',
        action='store_true',
        help='Do not save analysis context snapshots'
    )

    # === Backtest ===
    parser.add_argument(
        '--backtest',
        action='store_true',
        help='Run a backtest to evaluate historical analysis results'
    )

    parser.add_argument(
        '--backtest-code',
        type=str,
        default=None,
        help='Backtest only the specified stock code'
    )

    parser.add_argument(
        '--backtest-days',
        type=int,
        default=None,
        help='Backtest evaluation window in trading days (defaults to the configured value)'
    )

    parser.add_argument(
        '--backtest-force',
        action='store_true',
        help='Force a backtest, recalculating even if results already exist'
    )

    return parser.parse_args()


def _compute_trading_day_filter(
    config: Config,
    args: argparse.Namespace,
    stock_codes: List[str],
) -> Tuple[List[str], Optional[str], bool]:
    """
    Compute filtered stock list and effective market review region (Issue #373).

    Returns:
        (filtered_codes, effective_region, should_skip_all)
        - effective_region None = use config default (check disabled)
        - effective_region '' = all relevant markets closed, skip market review
        - should_skip_all: skip entire run when no stocks and no market review to run
    """
    force_run = getattr(args, 'force_run', False)
    if force_run or not getattr(config, 'trading_day_check_enabled', True):
        return (stock_codes, None, False)

    from ai_stock.core.trading_calendar import (
        get_market_for_stock,
        get_open_markets_today,
        compute_effective_region,
    )

    open_markets = get_open_markets_today()
    filtered_codes = []
    for code in stock_codes:
        mkt = get_market_for_stock(code)
        if mkt in open_markets or mkt is None:
            filtered_codes.append(code)

    if config.market_review_enabled and not getattr(args, 'no_market_review', False):
        effective_region = compute_effective_region(
            getattr(config, 'market_review_region', 'cn') or 'cn', open_markets
        )
    else:
        effective_region = None

    should_skip_all = (not filtered_codes) and (effective_region or '') == ''
    return (filtered_codes, effective_region, should_skip_all)


def _run_market_review_with_shared_lock(
    config: Config,
    run_market_review_func: Callable[..., Any],
    **kwargs: Any,
) -> Any:
    from ai_stock.core.market_review_lock import (
        release_market_review_lock,
        try_acquire_market_review_lock,
    )

    lock_token = try_acquire_market_review_lock(config)
    if lock_token is None:
        logger.warning("Market review is already running; skipping this run.")
        return None

    try:
        params = dict(kwargs)
        params.setdefault("config", config)
        return run_market_review_func(**params)
    finally:
        release_market_review_lock(lock_token)


def _is_multi_market_region(region: str) -> bool:
    normalized = str(region or "").strip().lower()
    if not normalized:
        return False
    if normalized == "both":
        return True
    parts = {item.strip() for item in normalized.split(",") if item.strip()}
    return len(parts) > 1


def _refresh_stock_index_cache_for_analysis(config: Config) -> None:
    """Best-effort stock-index refresh for CLI/scheduled analysis paths."""
    try:
        from ai_stock.services.stock_index_remote_service import (
            refresh_remote_stock_index_cache,
            settings_from_config,
        )

        result = refresh_remote_stock_index_cache(settings_from_config(config))
        if result.refreshed:
            logger.info("[stock-index] Refreshed the stock index cache before analysis: %s", result.cache_path)
        elif result.error:
            logger.debug("[stock-index] Pre-analysis refresh did not complete; continuing with the local index: %s", result.error)
    except Exception as exc:  # noqa: BLE001 - stock index freshness must not block analysis.
        logger.warning("[stock-index] Failed to refresh the stock index before analysis; continuing: %s", exc)


def _prime_daily_market_context(
    config: Config,
    pipeline: Any,
    *,
    region: str,
    no_market_review: bool,
    allow_generate: bool,
    force_refresh: bool = False,
    target_date: Optional[date] = None,
    return_full_report: bool = False,
    require_current_query_match: bool = False,
) -> Union[str, Tuple[str, str]]:
    """Load/reuse the run's market context, avoiding unbounded background generation."""
    if no_market_review or not region:
        return ("", "") if return_full_report else ""

    from ai_stock.services.daily_market_context import DailyMarketContextService

    if not _is_multi_market_region(region):
        service = getattr(pipeline, "_daily_market_context_service", None)
        if service is None:
            service = DailyMarketContextService(db_manager=pipeline.db)
            pipeline._daily_market_context_service = service
    else:
        service = DailyMarketContextService(db_manager=pipeline.db)

    get_context_kwargs = {
        "region": region,
        "config": config,
        "notifier": pipeline.notifier,
        "analyzer": pipeline.analyzer,
        "search_service": pipeline.search_service,
        "force_refresh": force_refresh,
        "allow_generate": allow_generate,
        "persist_market_review_history": False,
        "target_date": target_date,
        "require_query_id_match": require_current_query_match,
    }
    current_query_id = getattr(pipeline, "query_id", None)
    if isinstance(current_query_id, str) and current_query_id.strip():
        get_context_kwargs["current_query_id"] = current_query_id

    context = service.get_context(**get_context_kwargs)
    if context is None:
        return ("", "") if return_full_report else ""

    # Runtime context generation is preload-only and must not replace the full
    # market review run, except the query-scoped fallback after that run fails.
    if context.source != "analysis_history" and not (
        require_current_query_match and context.source == "market_review_runtime"
    ):
        return ("", "") if return_full_report else ""

    summary = str(getattr(context, "summary", ""))
    full_report = str(getattr(context, "full_report", "") or "")
    if return_full_report:
        return summary, full_report
    return summary


def _can_reuse_market_context_for_review(summary: str, region: str) -> bool:
    if not summary:
        return False
    normalized = str(region or "").strip().lower()
    if normalized == "both":
        return False
    parts = {item.strip() for item in normalized.split(",") if item.strip()}
    return len(parts) <= 1


def _resolve_daily_market_context_target_date(
    region: str,
    current_time: datetime,
) -> date:
    normalized_region = str(region or "cn").strip().lower()
    market = normalized_region if normalized_region in {"cn", "hk", "us"} else "cn"

    from ai_stock.core.trading_calendar import get_effective_trading_date

    return get_effective_trading_date(market, current_time=current_time)


def _market_review_report_text(review_result: Any) -> str:
    if review_result is None:
        return ""
    report = getattr(review_result, "report", None)
    if isinstance(report, str):
        return report
    return review_result if isinstance(review_result, str) else ""


def _save_reused_market_review_report(
    notifier: Any,
    market_report: str,
    *,
    config: Config,
    trigger_source: str,
    region: str,
) -> None:
    body = str(market_report or "").strip()
    if not body:
        return
    title = (
        "# 🎯 Market Review"
        if str(getattr(config, "report_language", "zh")).strip().lower() == "en"
        else "# 🎯 Market Review"
    )
    if not any(body.startswith(item) for item in ("# 🎯 Market Review",)):
        body = f"{title}\n\n{body}"
    try:
        date_str = datetime.now().strftime('%Y%m%d')
        report_filename = f"market_review_{date_str}.md"
        filepath = notifier.save_report_to_file(body, report_filename)
        logger.info(
            "[MarketReview] component=market_review action=save_reused_report "
            "trigger_source=%s region=%s path=%s",
            trigger_source,
            region,
            filepath,
        )
    except Exception as exc:
        logger.warning("Failed to save the market review report using reused market context: %s", exc)


def run_full_analysis(
    config: Config,
    args: argparse.Namespace,
    stock_codes: Optional[List[str]] = None
):
    """
    Run the full analysis workflow (individual stocks + market review).

    This is the main function called by scheduled tasks.
    """
    # Import pipeline modules outside the broad try/except so that import-time
    # failures propagate to the caller instead of being silently swallowed.
    from ai_stock.core.market_review import run_market_review
    from ai_stock.core.pipeline import StockAnalysisPipeline

    try:
        _refresh_stock_index_cache_for_analysis(config)

        # Issue #529: Hot-reload STOCK_LIST from .env on each scheduled run
        if stock_codes is None:
            config.refresh_stock_list()

        # Issue #373: Trading day filter (per-stock, per-market)
        effective_codes = stock_codes if stock_codes is not None else config.stock_list
        filtered_codes, effective_region, should_skip = _compute_trading_day_filter(
            config, args, effective_codes
        )
        if should_skip:
            logger.info(
                "All relevant markets are closed today; skipping this run. "
                "Use --force-run to force execution."
            )
            return
        if set(filtered_codes) != set(effective_codes):
            skipped = set(effective_codes) - set(filtered_codes)
            logger.info("Skipping stocks whose markets are closed today: %s", skipped)
        stock_codes = filtered_codes

        # The --single-notify command-line argument overrides the configuration (#55)
        if getattr(args, 'single_notify', False):
            config.single_stock_notify = True

        # Issue #190: Combine individual stock and market review notifications
        merge_notification = (
            getattr(config, 'merge_email_notification', False)
            and config.market_review_enabled
            and not getattr(args, 'no_market_review', False)
            and not config.single_stock_notify
        )

        # Create the scheduler
        save_context_snapshot = None
        if getattr(args, 'no_context_snapshot', False):
            save_context_snapshot = False
        query_id = uuid.uuid4().hex
        market_review_region = (
            effective_region
            if effective_region is not None
            else (getattr(config, 'market_review_region', 'cn') or 'cn')
        )
        should_run_market_review = (
            config.market_review_enabled
            and not args.no_market_review
            and (market_review_region or '') != ''
        )
        should_use_daily_market_context = (
            should_run_market_review
            and getattr(config, 'daily_market_context_enabled', True)
        )
        analysis_reference_time = datetime.now(timezone.utc)
        daily_market_context_target_date = None
        if should_use_daily_market_context:
            daily_market_context_target_date = _resolve_daily_market_context_target_date(
                market_review_region,
                analysis_reference_time,
            )
        market_report = ""
        market_context_summary = ""
        market_context_full_report = ""
        market_context_generated_during_stock = False
        pipeline = StockAnalysisPipeline(
            config=config,
            max_workers=args.workers,
            query_id=query_id,
            query_source="cli",
            save_context_snapshot=save_context_snapshot,
            daily_market_context_enabled=should_use_daily_market_context,
            daily_market_context_allow_generate=should_use_daily_market_context,
        )
        if should_use_daily_market_context:
            # Prompt-side context can reuse historical summaries, while full-merge
            # content must avoid silently reusing unrelated historical reports.
            _prime_daily_market_context(
                config,
                pipeline=pipeline,
                region=market_review_region,
                no_market_review=args.no_market_review,
                allow_generate=False,
                target_date=daily_market_context_target_date,
                return_full_report=False,
            )
            (
                market_context_summary,
                market_context_full_report,
            ) = _prime_daily_market_context(
                config,
                pipeline=pipeline,
                region=market_review_region,
                no_market_review=args.no_market_review,
                allow_generate=False,
                target_date=daily_market_context_target_date,
                return_full_report=True,
                require_current_query_match=True,
            )

        # 1. Run individual stock analysis
        results = pipeline.run(
            stock_codes=stock_codes,
            dry_run=args.dry_run,
            send_notification=not args.no_notify,
            merge_notification=merge_notification,
            current_time=analysis_reference_time,
        )

        if should_use_daily_market_context and not market_context_summary:
            (
                market_context_summary,
                market_context_full_report,
            ) = _prime_daily_market_context(
                config,
                pipeline=pipeline,
                region=market_review_region,
                no_market_review=args.no_market_review,
                allow_generate=False,
                target_date=daily_market_context_target_date,
                return_full_report=True,
                require_current_query_match=True,
            )
            market_context_generated_during_stock = bool(market_context_summary)

        # Issue #128: Add a delay between individual stock analysis and market review
        analysis_delay = getattr(config, 'analysis_delay', 0)

        # 2. Run market review (if enabled and not in individual-stock-only mode)
        if should_run_market_review:
            schedule_mode = bool(
                getattr(args, 'schedule', False)
                or getattr(config, 'schedule_enabled', False)
            )
            review_trigger_source = "schedule" if schedule_mode else "cli"
            can_reuse_market_context = (
                _can_reuse_market_context_for_review(
                    market_context_summary,
                    market_review_region,
                )
                if should_use_daily_market_context
                else False
            )

            can_skip_market_review = (
                (merge_notification or market_context_generated_during_stock)
                and can_reuse_market_context
                and bool(market_context_full_report or market_context_summary)
            )
            if can_skip_market_review:
                market_report = market_context_full_report or market_context_summary
                logger.info(
                    "Market review context can be reused; skipping duplicate market review and reusing the context."
                )
                _save_reused_market_review_report(
                    pipeline.notifier,
                    market_report,
                    config=config,
                    trigger_source=review_trigger_source,
                    region=market_review_region,
                )
                if (
                    market_context_generated_during_stock
                    and not merge_notification
                    and not args.no_notify
                    and pipeline.notifier.is_available()
                ):
                    if pipeline.notifier.send(
                        f"# 📈 Market Review\n\n{market_report}",
                        email_send_to_all=True,
                        route_type="report",
                    ):
                        logger.info("Successfully sent the market review using this run's market context.")
                    else:
                        logger.warning("Failed to send the market review using this run's market context.")

            review_result = None
            if not can_skip_market_review:
                if analysis_delay > 0:
                    logger.info(f"Waiting {analysis_delay} seconds before market review to avoid API rate limits...")
                    time.sleep(analysis_delay)

                review_result = _run_market_review_with_shared_lock(
                    config,
                    run_market_review,
                    notifier=pipeline.notifier,
                    analyzer=pipeline.analyzer,
                    search_service=pipeline.search_service,
                    send_notification=not args.no_notify,
                    merge_notification=merge_notification,
                    override_region=market_review_region,
                    query_id=query_id,
                    trigger_source=review_trigger_source,
                )
                # If the review still did not succeed, read the history/cache again to avoid a race with concurrent runs.
                if not review_result and should_use_daily_market_context:
                    (
                        market_context_summary,
                        market_context_full_report,
                    ) = _prime_daily_market_context(
                        config,
                        pipeline=pipeline,
                        region=market_review_region,
                        no_market_review=args.no_market_review,
                        allow_generate=False,
                        target_date=daily_market_context_target_date,
                        return_full_report=True,
                        require_current_query_match=True,
                    )
                    can_reuse_market_context = _can_reuse_market_context_for_review(
                        market_context_summary,
                        market_review_region,
                    )
                elif not review_result:
                    can_reuse_market_context = False

            # Store the result in market_report for subsequent Feishu document generation.
            if review_result:
                market_report = _market_review_report_text(review_result)
            elif can_reuse_market_context:
                market_report = market_context_full_report or market_context_summary

        # Issue #190: Combine notifications (individual stocks + market review)
        if merge_notification and (results or market_report) and not args.no_notify:
            parts = []
            if market_report:
                parts.append(f"# 📈 Market Review\n\n{market_report}")
            if results:
                dashboard_content = pipeline.notifier.generate_aggregate_report(
                    results,
                    getattr(config, 'report_type', 'simple'),
                )
                parts.append(f"# 🚀 Stock Decision Dashboard\n\n{dashboard_content}")
            if parts:
                combined_content = "\n\n---\n\n".join(parts)
                if pipeline.notifier.is_available():
                    if pipeline.notifier.send(combined_content, email_send_to_all=True, route_type="report"):
                        logger.info("Combined notification sent (individual stocks + market review).")
                    else:
                        logger.warning("Failed to send the combined notification.")

        # Output a summary
        if results:
            logger.info("\n===== Analysis Results Summary =====")
            for r in sorted(results, key=lambda x: x.sentiment_score, reverse=True):
                emoji = r.get_emoji()
                logger.info(
                    f"{emoji} {r.name}({r.code}): {r.operation_advice} | "
                    f"Score {r.sentiment_score} | {r.trend_prediction}"
                )

        logger.info("\nTask completed.")

        # === Auto backtest ===
        try:
            if getattr(config, 'backtest_enabled', False):
                from ai_stock.services.backtest_service import BacktestService

                logger.info("Starting automatic backtest...")
                service = BacktestService()
                stats = service.run_backtest(
                    force=False,
                    eval_window_days=getattr(config, 'backtest_eval_window_days', 10),
                    min_age_days=getattr(config, 'backtest_min_age_days', 14),
                    limit=200,
                )
                logger.info(
                    f"Automatic backtest completed: processed={stats.get('processed')} saved={stats.get('saved')} "
                    f"completed={stats.get('completed')} insufficient={stats.get('insufficient')} errors={stats.get('errors')}"
                )
        except Exception as e:
            logger.warning(f"Automatic backtest failed (ignored): {e}")

    except Exception as e:
        logger.exception(f"Analysis workflow failed: {e}")


def start_api_server(host: str, port: int, config: Config) -> None:
    """
    Start the FastAPI service in a background thread.

    Args:
        host: Bind address
        port: Listening port
        config: Configuration object
    """
    import socket
    import threading
    import uvicorn

    probe = socket.socket(socket.AF_INET6 if ":" in host else socket.AF_INET, socket.SOCK_STREAM)
    try:
        probe.bind((host, port))
    except OSError as exc:
        raise RuntimeError(f"FastAPI port is not available: {host}:{port}") from exc
    finally:
        probe.close()

    def run_server():
        level_name = (config.log_level or "INFO").lower()
        uvicorn.run(
            "api.app:app",
            host=host,
            port=port,
            log_level=level_name,
            log_config=None,
        )

    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    logger.info(f"FastAPI service started: http://{host}:{port}")


def _is_truthy_env(var_name: str, default: str = "true") -> bool:
    """Parse common truthy / falsy environment values."""
    value = os.getenv(var_name, default).strip().lower()
    return value not in {"0", "false", "no", "off"}




def _resolve_scheduled_stock_codes(stock_codes: Optional[List[str]]) -> Optional[List[str]]:
    """Scheduled runs should always read the latest persisted watchlist."""
    if stock_codes is not None:
        logger.warning(
            "The --stocks argument was detected in scheduled mode; scheduled runs will ignore the startup stock snapshot "
            "and reload the latest STOCK_LIST before each run."
        )
    return None


def _reload_runtime_config() -> Config:
    """Reload config from the latest persisted `.env` values for scheduled runs."""
    _reload_env_file_values_preserving_overrides()
    Config.reset_instance()
    return get_config()


def _build_schedule_time_provider(default_schedule_time: str):
    """Read the latest schedule time directly from the active config file.

    Fallback order:
    1. Process-level env override (set before launch) → honour it.
    2. Persisted config file value (written by WebUI) → use it.
    3. Documented system default ``"18:00"`` → always fall back here so
       that clearing SCHEDULE_TIME in WebUI correctly resets the schedule.
    """
    from ai_stock.core.config_manager import ConfigManager

    _SYSTEM_DEFAULT_SCHEDULE_TIME = "18:00"
    manager = ConfigManager()

    def _provider() -> str:
        if "SCHEDULE_TIME" in _INITIAL_PROCESS_ENV:
            return os.getenv("SCHEDULE_TIME", default_schedule_time)

        config_map = manager.read_config_map()
        schedule_time = (config_map.get("SCHEDULE_TIME", "") or "").strip()
        if schedule_time:
            return schedule_time
        return _SYSTEM_DEFAULT_SCHEDULE_TIME

    return _provider


def main() -> int:
    """
    Main entry point.

    Returns:
        Exit code (0 indicates success).
    """
    # Parse command-line arguments
    args = parse_arguments()

    # Initialize bootstrap logging before loading config so early failures are logged.
    try:
        _setup_bootstrap_logging(debug=args.debug)
    except Exception as exc:
        logging.basicConfig(
            level=logging.DEBUG if getattr(args, "debug", False) else logging.INFO,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            stream=sys.stderr,
        )
        logger.warning("Bootstrap logging initialization failed; falling back to stderr: %s", exc)

    # Load configuration after bootstrap logging so exceptions are logged.
    try:
        config = get_config()
    except Exception as exc:
        logger.exception("Failed to load configuration: %s", exc)
        return 1

    # Configure logging (output to console and file)
    try:
        _setup_runtime_logging(config.log_dir, debug=args.debug)
    except Exception as exc:
        logger.exception("Failed to switch to the configured log directory: %s", exc)
        return 1

    logger.info("=" * 60)
    logger.info("China A-Share Watchlist Analysis System starting")
    logger.info(f"Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)

    # Validate configuration
    warnings = config.validate()
    for warning in warnings:
        logger.warning(warning)

    if getattr(args, "check_notify", False):
        from ai_stock.services.notification_diagnostics import (
            format_notification_diagnostics,
            run_notification_diagnostics,
        )

        result = run_notification_diagnostics(config)
        print(format_notification_diagnostics(result))
        return 0 if result.ok else 1

    # Parse the stock list (normalize to uppercase, Issue #355)
    stock_codes = None
    if args.stocks:
        stock_codes = [
            resolve_index_stock_code_for_analysis(c)
            for c in args.stocks.split(',')
            if (c or "").strip()
        ]
        logger.info(f"Using stock list specified on the command line: {stock_codes}")

    # === Map --webui / --webui-only arguments to --serve / --serve-only ===
    if args.webui:
        args.serve = True
    if args.webui_only:
        args.serve_only = True

    # Support the legacy WEBUI_ENABLED environment variable
    if config.webui_enabled and not (args.serve or args.serve_only):
        args.serve = True

    # === Start the Web service (if enabled) ===
    start_serve = (args.serve or args.serve_only) and os.getenv("GITHUB_ACTIONS") != "true"

    # Support legacy WEBUI_HOST/WEBUI_PORT variables when --host/--port are not specified.
    if start_serve:
        if args.host == '0.0.0.0' and os.getenv('WEBUI_HOST'):
            args.host = os.getenv('WEBUI_HOST')
        if args.port == 8000 and os.getenv('WEBUI_PORT'):
            args.port = int(os.getenv('WEBUI_PORT'))
        _warn_if_public_webui(args.host)

    if start_serve:
        if not prepare_webui_frontend_assets():
            logger.warning("Frontend static assets are not ready; starting the FastAPI service anyway (the Web page may be unavailable).")
        try:
            start_api_server(host=args.host, port=args.port, config=config)
        except Exception as e:
            logger.error(f"Failed to start the FastAPI service: {e}")
            if args.serve_only:
                return 1
            start_serve = False

    # === Web service-only mode: do not run automatic analysis ===
    if args.serve_only:
        logger.info("Mode: Web service only")
        logger.info(f"Web service running: http://{args.host}:{args.port}")
        logger.info("Trigger analysis through the /api/v1/analysis/analyze endpoint")
        logger.info(f"API documentation: http://{args.host}:{args.port}/docs")
        logger.info("Press Ctrl+C to exit...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("\nInterrupted by user; exiting.")
        return 0

    try:
        # Mode 0: Backtest
        if getattr(args, 'backtest', False):
            logger.info("Mode: Backtest")
            from ai_stock.services.backtest_service import BacktestService

            service = BacktestService()
            stats = service.run_backtest(
                code=getattr(args, 'backtest_code', None),
                force=getattr(args, 'backtest_force', False),
                eval_window_days=getattr(args, 'backtest_days', None),
            )
            logger.info(
                f"Backtest completed: processed={stats.get('processed')} saved={stats.get('saved')} "
                f"completed={stats.get('completed')} insufficient={stats.get('insufficient')} errors={stats.get('errors')}"
            )
            return 0

        # Mode 1: Market review only
        if args.market_review:
            from ai_stock.core.market_review import run_market_review
            from ai_stock.core.market_review_runtime import build_market_review_runtime

            # Issue #373: Trading day check for market-review-only mode.
            # Do NOT use _compute_trading_day_filter here: that helper checks
            # config.market_review_enabled, which would wrongly block an
            # explicit --market-review invocation when the flag is disabled.
            effective_region = None
            if not getattr(args, 'force_run', False) and getattr(config, 'trading_day_check_enabled', True):
                from ai_stock.core.trading_calendar import get_open_markets_today, compute_effective_region as _compute_region
                open_markets = get_open_markets_today()
                effective_region = _compute_region(
                    getattr(config, 'market_review_region', 'cn') or 'cn', open_markets
                )
                if effective_region == '':
                    logger.info("All markets relevant to today's market review are closed; skipping. Use --force-run to force execution.")
                    return 0

            logger.info("Mode: Market review only")
            notifier, analyzer, search_service = build_market_review_runtime(config)

            _run_market_review_with_shared_lock(
                config,
                run_market_review,
                notifier=notifier,
                analyzer=analyzer,
                search_service=search_service,
                send_notification=not args.no_notify,
                override_region=effective_region,
                trigger_source="cli",
            )
            return 0

        # Mode 2: Scheduled mode
        if args.schedule or config.schedule_enabled:
            logger.info("Mode: Scheduled")
            logger.info(f"Daily run time: {config.schedule_time}")

            # Determine whether to run immediately:
            # Command line arg --no-run-immediately overrides config if present.
            # Otherwise use config (defaults to True).
            should_run_immediately = config.schedule_run_immediately
            if getattr(args, 'no_run_immediately', False):
                should_run_immediately = False

            logger.info(f"Run immediately on startup: {should_run_immediately}")

            from ai_stock.scheduler import run_with_schedule
            scheduled_stock_codes = _resolve_scheduled_stock_codes(stock_codes)
            schedule_time_provider = _build_schedule_time_provider(config.schedule_time)

            def scheduled_task():
                runtime_config = _reload_runtime_config()
                run_full_analysis(runtime_config, args, scheduled_stock_codes)

            background_tasks = []
            if getattr(config, 'agent_event_monitor_enabled', False):
                from ai_stock.services.alert_worker import AlertWorker

                interval_minutes = max(1, getattr(config, 'agent_event_monitor_interval_minutes', 5))
                alert_worker = AlertWorker(config_provider=_reload_runtime_config)

                def event_monitor_task():
                    stats = alert_worker.run_once()
                    triggered_count = stats.get("triggered", 0)
                    if triggered_count:
                        logger.info("[EventMonitor] Triggered %d alerts this run", triggered_count)

                background_tasks.append({
                    "task": event_monitor_task,
                    "interval_seconds": interval_minutes * 60,
                    "run_immediately": True,
                    "name": "agent_event_monitor",
                })

            run_with_schedule(
                task=scheduled_task,
                schedule_time=config.schedule_time,
                run_immediately=should_run_immediately,
                background_tasks=background_tasks,
                schedule_time_provider=schedule_time_provider,
            )
            return 0

        # Mode 3: Normal one-time run
        if config.run_immediately:
            run_full_analysis(config, args, stock_codes)
        else:
            logger.info("Analysis is configured not to run immediately (RUN_IMMEDIATELY=false)")

        logger.info("\nProgram completed.")

        # Keep the process running if the service is enabled outside scheduled mode.
        keep_running = start_serve and not (args.schedule or config.schedule_enabled)
        if keep_running:
            logger.info("API service running (press Ctrl+C to exit)...")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass

        return 0

    except KeyboardInterrupt:
        logger.info("\nInterrupted by user; exiting.")
        return 130

    except Exception as e:
        logger.exception(f"Program execution failed: {e}")
        return 1


if __name__ == "__main__":
    multiprocessing.freeze_support()
    sys.exit(main())
