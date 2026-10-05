# Email notifications

SMTP email is the only supported notification transport for analysis reports and
event-driven alerts. Other channel senders, settings, and notification test options
have been removed. Local report saving remains available without email credentials.

## Configuration

Set these values in `.env`, the process environment, or Web Settings → Notifications:

```dotenv
EMAIL_SENDER=sender@example.com
EMAIL_PASSWORD=your_smtp_authorization_code
EMAIL_RECEIVERS=recipient@example.com
EMAIL_SENDER_NAME=DSA
```

Use an SMTP authorization/app password where required. Never commit real
credentials. The SMTP host is detected from the sender's domain. Supported
providers include QQ, 163, and Gmail. OAuth2-only Outlook/Exchange tenants are
not supported.

`EMAIL_SENDER` and `EMAIL_PASSWORD` must both be configured. `EMAIL_RECEIVERS` is a
comma-separated list; leaving it empty sends to the sender. `EMAIL_SENDER_NAME`
controls the displayed sender name.

## Testing and delivery diagnostics

The Web notification test sends a real email using the current settings draft.
It does not save the draft. Only `email` is accepted by
`POST /api/v1/system/config/notification/test-channel`; other channel names fail
request validation.

Run `python main.py --check-notify` for read-only configuration diagnostics.
SMTP delivery failures are reported without exposing credentials or invalidating
the analysis report. Report history retains delivery diagnostics.

## Recipient groups and report options

Numbered stock/email groups are supported in `.env` or the process environment:

```dotenv
STOCK_GROUP_1=600519,300750
EMAIL_GROUP_1=team@example.com
```

Groups select recipients, not the analysis universe: `STOCK_LIST` still controls
which stocks are analyzed. Unmatched stocks use the default recipients. Aggregate
reports are generated separately for each recipient group; a failed group does
not prevent later groups from receiving their reports.

Existing report controls remain supported: `SINGLE_STOCK_NOTIFY`, `REPORT_TYPE`,
`REPORT_LANGUAGE`, `REPORT_SUMMARY_ONLY`, `REPORT_SHOW_LLM_MODEL`, and
`MERGE_EMAIL_NOTIFICATION`. Template, integrity, and history-comparison controls
are unchanged.

For inline-image emails, set `MARKDOWN_TO_IMAGE_CHANNELS=email` and install the
conversion tool required by `MD2IMG_ENGINE`. Conversion failures fall back to the
regular email report. `MARKDOWN_TO_IMAGE_MAX_CHARS` limits conversion size.

## Routing and noise controls

`NOTIFICATION_REPORT_CHANNELS`, `NOTIFICATION_ALERT_CHANNELS`, and
`NOTIFICATION_SYSTEM_ERROR_CHANNELS` accept only `email` or an empty value.
Empty means use the configured email transport. The system-error route remains
reserved for future producers.

Deduplication, cooldown, quiet hours/timezone, and minimum severity remain
available through `NOTIFICATION_DEDUP_TTL_SECONDS`,
`NOTIFICATION_COOLDOWN_SECONDS`, `NOTIFICATION_QUIET_HOURS`,
`NOTIFICATION_TIMEZONE`, and `NOTIFICATION_MIN_SEVERITY`.
`NOTIFICATION_DAILY_DIGEST_ENABLED` is reserved and does not send a daily digest.

## Migration and deployment

- Remove old bot, webhook, and push-provider notification variables from local,
  Docker, Desktop, and GitHub Actions configurations. Existing `.env` files are
  not automatically rewritten; retired variables are ignored at startup with a
  warning and excluded from both settings values and the schema.
- Update/import requests containing retired channel settings are rejected with
  `unsupported_notification_setting`. Clean old backups before importing them.
  Raw `.env` export remains a backup of the original file, including obsolete
  assignments that have not yet been removed.
- Replace old route lists and image-channel lists with `email` or clear them.
  An old route containing only removed channels does not enable email implicitly.
- The [disabled daily-analysis workflow](../.github/workflows/disabled/00-daily-analysis.yml)
  now maps only email transport settings plus routing/noise controls. It remains
  disabled; this change does not enable scheduling or add permissions.
- Restart/rebuild the backend and Web app after deployment to replace previously
  served settings/UI assets. Desktop uses the same configuration API.

To roll back this intentional removal, restore the preceding application version
and its frontend assets. Retain a private configuration backup if needed; do not
restore obsolete secrets into source control.

## GitHub Actions environment mapping

This table describes the disabled daily-analysis workflow, not an active schedule.

<!-- notification-actions-env-table:start -->

| Key | Tier | Channel / feature | Actions source | Default |
| --- | --- | --- | --- | --- |
| `EMAIL_SENDER` | minimal | email | Variable or Secret | - |
| `EMAIL_PASSWORD` | minimal | email | Secret | - |
| `EMAIL_RECEIVERS` | advanced | email | Variable or Secret | - |
| `EMAIL_SENDER_NAME` | advanced | email | Variable or Secret | `daily_stock_analysis股票分析助手` |
| `NOTIFICATION_REPORT_CHANNELS` | advanced | routing | Variable or Secret | - |
| `NOTIFICATION_ALERT_CHANNELS` | advanced | routing | Variable or Secret | - |
| `NOTIFICATION_SYSTEM_ERROR_CHANNELS` | advanced | routing | Variable or Secret | - |
| `NOTIFICATION_DEDUP_TTL_SECONDS` | advanced | noise | Variable or Secret | `0` |
| `NOTIFICATION_COOLDOWN_SECONDS` | advanced | noise | Variable or Secret | `0` |
| `NOTIFICATION_QUIET_HOURS` | advanced | noise | Variable or Secret | - |
| `NOTIFICATION_TIMEZONE` | advanced | noise | Variable or Secret | - |
| `NOTIFICATION_MIN_SEVERITY` | advanced | noise | Variable or Secret | - |
| `NOTIFICATION_DAILY_DIGEST_ENABLED` | advanced | noise | Variable or Secret | `false` |

<!-- notification-actions-env-table:end -->
