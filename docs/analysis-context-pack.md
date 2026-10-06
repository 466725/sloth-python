# Analysis Context Pack

The `AnalysisContextPack` is an internal, versioned envelope that describes the
inputs available to a stock analysis and the quality or limitations of those
inputs. The pipeline builds it from artifacts it has already fetched. It does
not introduce another data-fetching path.

The full pack is used to create two separate outputs:

1. A low-sensitivity `analysis_context_pack_summary` for ordinary and Agent
   analysis prompts.
2. A whitelisted `analysis_context_pack_overview` for reports and history APIs.

The full pack is not itself a public API contract. Its version is currently
`PACK_VERSION = "1.0"`. There is no dedicated environment switch for disabling
pack construction or prompt-summary generation.

## Data flow

For ordinary and Agent analysis, `StockAnalysisPipeline` assembles
`PipelineAnalysisArtifacts`, calls `AnalysisContextBuilder.build()`, then
renders the prompt summary and public overview. If pack output generation fails,
the pipeline logs a warning and continues without those outputs.

The builder is an assembler: it consumes the pipeline's current artifacts and
does not independently call the database, fetchers, search services, Agent
tools, or market-data providers. Its main input fields are:

| Artifact | Used for |
| --- | --- |
| `code`, `stock_name`, `market` | The pack subject |
| `phase` | The market-phase context already resolved by the caller |
| `base_context` | Recent daily-bar context |
| `enhanced_context` | Intraday/estimated-bar indicators and quote metadata |
| `realtime_quote` | Quote data and its source/timestamp |
| `trend_result` | Technical-analysis block |
| `chip_data` | Chip-distribution block |
| `fundamental_context` | Fundamental status, coverage, and source chain |
| `news_context`, `news_result_count` | News availability and result count |
| `metadata` | Additional non-payload metadata, including trigger source |

The builder also offers `build_batch()` to assemble multiple packs from the
same artifact structure.

## Pack structure and block behavior

The top-level envelope contains `pack_version`, `subject`, `phase`, `blocks`,
`data_quality`, `metadata`, and `created_at`. The subject contains `code`,
optional `stock_name`, and optional `market`. `created_at` is a datetime
serialized as ISO 8601; item and block timestamps, when present, must also be
ISO 8601 datetimes. A calendar date by itself is kept as a value or metadata,
not as a timestamp.

Each block has a status, items, optional source and timestamp, warnings, and
metadata. Each item has a status and may carry a value, source, timestamp,
fallback source, missing reason, warnings, and metadata. The builder currently
creates these blocks:

| Block | Current inputs and behavior |
| --- | --- |
| `quote` | Uses the existing real-time quote. Explicit stale markers take precedence over fallback markers; otherwise a quote with a fallback source is `fallback`, and an ordinary quote is `available`. Missing quotes are `missing`. |
| `daily_bars` | Uses `base_context.today`, `base_context.yesterday`, and `base_context.date`. Both bars present means `available`; only one means `partial`; neither or an explicit `data_missing` means `missing`. |
| `technical` | Uses `trend_result`. A real-time overlay or an explicitly partial/estimated current bar marks the block `partial`, with an `intraday_realtime_overlay` warning. Missing trend data is `missing`. |
| `chip` | Uses `chip_data`. Missing data is `missing`, unless input metadata explicitly marks chip data unsupported, in which case it is `not_supported`. |
| `fundamentals` | Maps input statuses `ok`/`available`, `not_supported`, `partial`, and `failed` to the corresponding pack states. A failed fundamental pipeline uses the stable reason `fundamental_pipeline_failed`; raw error text is not included. |
| `news` | Non-empty `news_context` is `available`; absent or blank content is `missing`. `news_result_count`, when provided, is recorded in pack metadata. |

`phase` remains a dictionary supplied by the caller; the pack does not define a
separate market-phase enum. Daily market context is a related but separate
pipeline feature: its prompt summary and guardrails are not the same field as
the pack's `phase`.

## Data-quality states and score

The states below describe the quality or availability of input data. They do not
indicate whether the analysis, alert, backtest, or notification operation
succeeded.

| State | Meaning |
| --- | --- |
| `available` | Data is present and usable in the current path. |
| `missing` | Data expected by the current path was not available. |
| `not_supported` | The market, source, or path does not support this data. |
| `fallback` | A secondary source or fallback path supplied the data. |
| `stale` | Data is present but explicitly marked as not fresh enough. |
| `estimated` | The value is an estimate, not a complete observation. |
| `partial` | A block is only partly available, or uses an intraday overlay. |
| `fetch_failed` | A data fetch was attempted and explicitly failed. |

The builder assigns status scores of `available` 100, `partial` 75,
`estimated` 75, `not_supported` 70, `fallback` 65, `stale` 50, `missing` 35,
and `fetch_failed` 25. It calculates the weighted overall score using these
block weights:

| Block | Weight |
| --- | ---: |
| `quote` | 25 |
| `daily_bars` | 25 |
| `technical` | 25 |
| `news` | 10 |
| `fundamentals` | 10 |
| `chip` | 5 |

The overall score is rounded to an integer from 0 to 100. Levels are `good` at
85 or above, `usable` at 70–84, `limited` at 55–69, and `poor` below 55.
Limitations are selected from block states using a separate rule: core blocks
(`quote`, `daily_bars`, `technical`) report stale, fallback, missing,
fetch-failed, partial, or estimated states; auxiliary blocks (`news`,
`fundamentals`, `chip`) report stale, fallback, or fetch-failed states. At most
five limitations are emitted.

These scores are comparative quality signals, not probabilities or guarantees
about the correctness of an analysis.

## Prompt summary and public overview

### Prompt summary

The prompt renderer intentionally ignores item `value` fields. The
`analysis_context_pack_summary` can include the subject, pack version, block
statuses, sources, warning codes, missing reasons, news result count, quality
score/level, limitations, and phase-related data constraints. It is rendered in
the selected report language and passed to ordinary analysis and Agent
workflows.

This restriction applies to the pack summary only. Other analysis prompt
sections may contain input data under their existing contracts.

### Public overview

`render_analysis_context_pack_overview()` projects a whitelist rather than
returning the full pack or prompt summary. The overview includes:

- Pack version, creation time, and subject identifiers.
- Per-block key, label, status, source, warnings, and missing reasons.
- Counts by data-quality status.
- Overall score, quality level, approved block scores, and limitations.
- Top-level warnings and safe metadata such as trigger source and news result
  count.

Persisted overviews are validated and sanitized again when extracted from a
context snapshot. The raw `context_snapshot` API view removes the top-level
overview and market-phase summary because they are exposed as separate
structured fields; it also removes selected context-only fields such as
portfolio and daily-market summaries.

The overview can appear in report details, history responses, analysis
responses, completed task results, and Web report views when available. The Web
report uses the `AnalysisContextSummary` component and presents the overview in
a collapsible panel. Older records or analyses without a saved snapshot may not
have an overview.

## Persistence and configuration

The full pack and `analysis_context_pack_summary` are not written into the
history snapshot. The separately rendered public overview may be stored at the
top level of `analysis_history.context_snapshot` alongside existing diagnostic
and analysis context data.

`SAVE_CONTEXT_SNAPSHOT` defaults to `true`. Setting it to `false`, or using the
CLI option `--no-context-snapshot`, stops saving the history context snapshot.
It does **not** disable pack construction or prompt-summary generation for the
current analysis. With snapshot persistence disabled, historical API responses
may therefore lack the persisted overview and other snapshot-derived context.

No database migration is required for the pack overview. Older snapshots without
the overview or newer data-quality fields remain readable; absent values are
returned as empty or optional fields.

## Related contracts and compatibility

- `analysis_history.context_snapshot.enhanced_context.date` is still consumed
  when the backtest service parses an analysis date. Preserve this legacy
  location unless a migration updates its readers.
- Alert evaluation statuses such as `triggered`, `skipped`, `degraded`, and
  `failed` describe rule evaluation/recording, not input quality. See the
  [alert guide](alerts.md).
- Notification statuses such as `sent`, `no_channel`, and delivery failures
  describe notification outcomes, not input quality. See the
  [notification guide](email_notifications.md).
- The separate daily market context feature can add a low-sensitivity summary
  and apply decision guardrails. It is not a pack block and can be disabled
  independently with `DAILY_MARKET_CONTEXT_ENABLED`.

## Privacy and safe serialization

The complete pack can contain raw analysis values, including quote, technical,
chip, fundamental, and news inputs. Do not expose the full pack or its
`items.value` fields through APIs, Web views, notifications, or logs. Use the
public overview renderer for client-facing summaries.

`AnalysisContextPack.to_safe_dict()` is an internal helper that redacts
sensitive mapping keys recursively. It is not a general secret scanner: it does
not inspect arbitrary string contents or scrub URLs by pattern. Never use it as
a substitute for the public overview projection or for safe handling of
credentials.

## Source map

| Area | Current source |
| --- | --- |
| Pack schema and status enum | [`ai_stock/schemas/analysis_context_pack.py`](../ai_stock/schemas/analysis_context_pack.py) |
| Artifact assembly and quality scoring | [`ai_stock/services/analysis_context_builder.py`](../ai_stock/services/analysis_context_builder.py) |
| Prompt-summary formatting | [`ai_stock/analysis_context_pack_prompt.py`](../ai_stock/analysis_context_pack_prompt.py) |
| Public overview and snapshot sanitization | [`ai_stock/analysis_context_pack_overview.py`](../ai_stock/analysis_context_pack_overview.py) |
| Pipeline integration | [`ai_stock/core/pipeline.py`](../ai_stock/core/pipeline.py) |
| History and analysis API projection | [`api/v1/endpoints/history.py`](../api/v1/endpoints/history.py), [`api/v1/endpoints/analysis.py`](../api/v1/endpoints/analysis.py), [`api/v1/schemas/history.py`](../api/v1/schemas/history.py) |
| Web report overview | [`apps/dsa-web/src/components/report/AnalysisContextSummary.tsx`](../apps/dsa-web/src/components/report/AnalysisContextSummary.tsx) |
| Backtest date compatibility | [`ai_stock/repositories/backtest_repo.py`](../ai_stock/repositories/backtest_repo.py) |

The focused contract tests are under `tests/unit/analyzer/`, including tests
for the schema, builder, prompt renderer, and public overview.
