import {expect, test, type Page} from '@playwright/test';

test.use({locale: 'zh-CN'});

const UI_LANGUAGE_STORAGE_KEY = 'dsa.uiLanguage';
const REPORT_MARKDOWN = '# Test report\n\n**Outlook:** Watch\n\n| Metric | Value |\n| --- | --- |\n| Score | 78 |\n\n> Research only.';
const REPORT_PLAIN_TEXT = 'Test report\n\nOutlook: Watch\n\n| Metric | Value |\n\n| Score | 78 |\n\nResearch only.';

test.beforeEach(async ({page}) => {
    const createdAt = new Date().toISOString();
    const item = {
        id: 1,
        query_id: 'playwright-report',
        stock_code: '600519',
        stock_name: 'Playwright report',
        sentiment_score: 78,
        operation_advice: 'Watch',
        created_at: createdAt,
    };
    await page.route(/\/api\/v1\/history(?:\?.*)?$/, async (route) => {
        const params = new URL(route.request().url()).searchParams;
        const items = params.get('stock_code') === 'MARKET' ? [] : [item];
        await route.fulfill({
            json: {total: items.length, page: 1, limit: 20, items},
        });
    });
    await page.route(/\/api\/v1\/history\/stocks(?:\?.*)?$/, async (route) => {
        await route.fulfill({
            json: {total: 1, items: [{...item, analysis_count: 1, last_analysis_time: createdAt}]},
        });
    });
    await page.route(/\/api\/v1\/history\/1$/, async (route) => {
        await route.fulfill({
            json: {
                meta: {...item, report_type: 'detailed', report_language: 'zh'},
                summary: {
                    analysis_summary: 'Test report',
                    operation_advice: 'Watch',
                    trend_prediction: 'Neutral',
                    sentiment_score: 78,
                },
            },
        });
    });
    await page.route(/\/api\/v1\/history\/1\/news(?:\?.*)?$/, async (route) => {
        await route.fulfill({json: {total: 0, items: []}});
    });
    await page.route(/\/api\/v1\/history\/1\/markdown$/, async (route) => {
        await route.fulfill({json: {content: REPORT_MARKDOWN}});
    });
});

async function openApp(page: Page) {
    await page.addInitScript((storageKey) => {
        window.localStorage.setItem(storageKey, 'zh');
    }, UI_LANGUAGE_STORAGE_KEY);

    await page.goto('/');
}

async function ensureHistoryItem(page: Page) {
    await expect(page.getByText('个股栏')).toBeVisible({timeout: 20_000});
    const historyItem = page.getByRole('button', {name: 'Playwright report 600519 历史记录', exact: true});
    await expect(historyItem).toBeVisible({timeout: 10_000});
    await historyItem.click();
}

test.describe('ReportMarkdown component', () => {
    test('copy plain text', async ({page, context}) => {
        // Grant clipboard permissions
        await context.grantPermissions(['clipboard-read', 'clipboard-write']);

        await openApp(page);

        // Ensure there is a history item to work with
        await ensureHistoryItem(page);
        // Wait for detailed report button to be enabled (indicates selection is complete)
        const detailedReportButton = page.getByRole('button', {name: '完整分析报告'});
        await expect(detailedReportButton).toBeEnabled({timeout: 3000});

        // Click the "完整分析报告" button to open the markdown drawer
        await expect(detailedReportButton).toBeVisible({timeout: 5000});
        await detailedReportButton.click();

        // Verify drawer content is visible
        await expect(page.getByRole('dialog').getByText('完整分析报告')).toBeVisible();

        // Click copy plain text button - use dialog-specific locator
        const copyPlainTextButton = page.getByRole('dialog').getByRole('button', {name: '复制纯文本'});
        await expect(copyPlainTextButton).toBeVisible({timeout: 5000});
        await copyPlainTextButton.click();

        await expect.poll(async () => (
            await page.evaluate(() => navigator.clipboard.readText())
        ).replace(/\r\n/g, '\n')).toBe(REPORT_PLAIN_TEXT);

        // Verify checkmark icon is shown
        const checkmarkIcon = page.locator('button[aria-label="复制纯文本"] svg.text-success');
        await expect(checkmarkIcon).toBeVisible();

        // Wait for icon to revert (icon disappears after 2 seconds)
        await expect(checkmarkIcon).not.toBeVisible({timeout: 3500});
    });

    test('buttons are disabled during loading', async ({page}) => {
        let releaseMarkdown!: () => void;
        const markdownReady = new Promise<void>((resolve) => {
            releaseMarkdown = resolve;
        });
        let markRequested!: () => void;
        const markdownRequested = new Promise<void>((resolve) => {
            markRequested = resolve;
        });
        await page.route(/\/api\/v1\/history\/1\/markdown$/, async (route) => {
            markRequested();
            await markdownReady;
            await route.fulfill({json: {content: REPORT_MARKDOWN}});
        });
        await openApp(page);

        // Ensure there is a history item to work with
        await ensureHistoryItem(page);
        // Wait for detailed report button to be enabled (indicates selection is complete)
        const detailedReportButton = page.getByRole('button', {name: '完整分析报告'});
        await expect(detailedReportButton).toBeEnabled({timeout: 3000});

        // Click the "完整分析报告" button to open the markdown drawer
        await expect(detailedReportButton).toBeVisible({timeout: 5000});
        await detailedReportButton.click();

        const copyMarkdownButton = page.getByRole('dialog').getByRole('button', {name: '复制 Markdown 源码'});
        const copyPlainTextButton = page.getByRole('dialog').getByRole('button', {name: '复制纯文本'});

        try {
            await markdownRequested;
            await expect(copyMarkdownButton).toBeDisabled();
            await expect(copyPlainTextButton).toBeDisabled();
        } finally {
            releaseMarkdown();
        }
        await expect(copyMarkdownButton).toBeEnabled({timeout: 5000});
        await expect(copyPlainTextButton).toBeEnabled();
    });
});
