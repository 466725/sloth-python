# Stock Autocomplete Catalog

The Web app searches a local catalog served at `/stocks.index.json`. The bundled
[index](../apps/dsa-web/public/stocks.index.json) supports stock codes, names,
aliases, full pinyin, and pinyin initials. Searching this catalog does not call
a market-data provider or require a provider token.

## Runtime updates

`STOCK_INDEX_REMOTE_UPDATE_ENABLED=true` enables best-effort updates from the
built-in GitHub main source. The backend caches the downloaded catalog locally.
On failure it retains the existing cache or uses the bundled index. Remote
updates are separate from quote retrieval and stock analysis.

## Rebuild from local CSV files

Supply UTF-8 CSV exports under `ai_stock/stock_data/`:

| File | Required identity fields |
| --- | --- |
| `stock_list_a.csv` | `ts_code`, `name` (for example, `600519.SH`) |
| `stock_list_hk.csv` | `ts_code`, `name` (for example, `00700.HK`) |
| `stock_list_us.csv` | `ts_code`, `enname`; optional localized `name` (for example, `AAPL`) |

`ts_code` is the catalog's instrument identifier column, not an API dependency.
Additional fields such as `delist_date` and aliases are used when present.
JP/KR seed files under [scripts/stock_index_seeds/](../scripts/stock_index_seeds/)
supplement the catalog. The generator requires all three catalog files and
valid rows for each market before replacing the index, so a missing local
export cannot reduce the bundled catalog to just the seeds.

Install the existing project dependencies, including `pypinyin`, then validate:

```powershell
python scripts\refresh_stock_index.py --test
```

To rebuild and synchronize the local static index:

```powershell
python scripts\refresh_stock_index.py
```

This command reads local files only; it does not download fresh listings.
Maintain those CSV exports separately. Missing catalog files or missing
dependencies produce an error and leave the existing index untouched.

An existing AkShare export under `logs/stock_basic_*.csv` can also be used:

```powershell
python scripts\generate_index_from_csv.py --source akshare --test
```

This path uses the latest matching export and only covers its contents; it is
not a substitute for the full multi-market catalog. Remove `--test` only if that
coverage is intentional.

## Rollback

If an index rebuild is incorrect, restore the previous bundled index from
version control and redeploy the Web assets. Disable remote updates if needed
while investigating. Market-data provider routing and analysis configuration
are unchanged by an index rebuild.
