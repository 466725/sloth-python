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

## Updating the bundled catalog

The generated index is checked in at
[`apps/dsa-web/public/stocks.index.json`](../apps/dsa-web/public/stocks.index.json)
and is served by the Web app. The repository no longer includes a catalog
generation script. To change the bundled catalog, update the JSON asset through
the project's chosen data-maintenance process and review the change before
deploying it.

## Rollback

If an index rebuild is incorrect, restore the previous bundled index from
version control and redeploy the Web assets. Disable remote updates if needed
while investigating. Market-data provider routing and analysis configuration
are unchanged by an index rebuild.
