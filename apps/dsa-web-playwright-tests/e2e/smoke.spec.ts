import {expect, test, type Page} from '@playwright/test';

async function openApp(page: Page) {
    await page.addInitScript(() => {
        if (window.localStorage.getItem('dsa.uiLanguage') === null) {
            window.localStorage.setItem('dsa.uiLanguage', 'zh');
        }
    });
    await page.goto('/');
    await expect(page.getByPlaceholder('输入股票代码或名称，如 600519、贵州茅台、AAPL')).toBeVisible({timeout: 20_000});
}

test.describe('web smoke', () => {
    test.use({locale: 'zh-CN'});


    test('home page shows analysis entry and history panel', async ({page}) => {
        await openApp(page);

        const stockInput = page.getByPlaceholder('输入股票代码或名称，如 600519、贵州茅台、AAPL');
        await expect(stockInput).toBeVisible({timeout: 10_000});
        await expect(page.getByRole('link', {name: '首页'})).toBeVisible();
        await expect(page.getByRole('link', {name: '问股'})).toBeVisible();
        await expect(page.getByText('个股栏')).toBeVisible();

        await stockInput.fill('600519');
        const analyzeButton = page.getByRole('button', {name: '分析', exact: true});
        await expect(analyzeButton).toBeVisible();
    });

    test('chat page sends the generated prompt for the selected stock and strategy', async ({page}) => {
        await openApp(page);
        await page.route('**/api/v1/stocks/watchlist', (route) =>
            route.fulfill({json: {stock_codes: ['600519', 'AAPL']}}));
        await page.route('**/api/v1/agent/skills', (route) =>
            route.fulfill({json: {
                skills: [{id: 'bull_trend', name: '默认多头趋势', description: '趋势分析'}],
                default_skill_id: 'bull_trend',
            }}));
        await page.route('**/api/v1/agent/chat/stream', (route) =>
            route.fulfill({contentType: 'text/event-stream', body: 'data: {"type":"done","content":"测试结果"}\n\n'}));

        // Navigate to chat page by clicking the link
        await page.getByRole('link', {name: '问股'}).click();

        await expect(page.getByTestId('chat-workspace')).toBeVisible({timeout: 10_000});
        await expect(page.getByTestId('chat-session-list-scroll')).toBeVisible();
        await expect(page.getByTestId('chat-message-scroll')).toBeVisible();

        const input = page.getByRole('textbox', {name: '自动生成的分析提示'});
        await expect(input).toBeVisible({timeout: 5000});
        await page.getByRole('radio', {name: 'AAPL'}).check();
        const prompt = '使用策略 默认多头趋势 分析股票 AAPL';
        await expect(input).toHaveValue(prompt);
        await expect(input).toHaveAttribute('readonly');
        await input.pressSequentially('TSLA');
        await expect(input).toHaveValue(prompt);
        const requestPromise = page.waitForRequest('**/api/v1/agent/chat/stream');
        await page.getByRole('button', {name: '发送'}).click();
        const payload = (await requestPromise).postDataJSON();
        expect(payload).toMatchObject({
            message: prompt,
            skills: ['bull_trend'],
            context: {stock_code: 'AAPL', lock_stock_scope: true},
        });
        await expect(page.locator('p').filter({hasText: prompt}).last()).toBeVisible({timeout: 5000});
    });

    test('chat page uses accessible labels instead of native title attributes for key actions', async ({page}) => {
        await openApp(page);

        await page.getByRole('link', {name: '问股'}).click();

        const sendButton = page.getByRole('button', {name: '发送'});
        const composer = page.getByRole('textbox', {name: '自动生成的分析提示'});

        await expect(page.getByTestId('chat-workspace')).toBeVisible({timeout: 10_000});
        await expect(sendButton).toBeVisible({timeout: 10_000});
        await expect(composer).toBeVisible({timeout: 10_000});

        await expect(sendButton).not.toHaveAttribute('title', /.+/);
        await expect(composer).not.toHaveAttribute('title', /.+/);
    });

    test('assistant responses use the available width on desktop and mobile', async ({page}) => {
        await page.addInitScript(() => {
            localStorage.setItem('dsa.uiLanguage', 'en');
            localStorage.setItem('dsa_chat_session_id', 'test-session');
        });
        await page.route('**/api/v1/agent/chat/sessions?*', (route) =>
            route.fulfill({json: {sessions: [{
                session_id: 'test-session', title: 'Test', message_count: 2,
                created_at: null, last_active: null,
            }]}}));
        await page.route('**/api/v1/agent/chat/sessions/test-session', (route) =>
            route.fulfill({json: {messages: [
                {id: 'user', role: 'user', content: 'Analyze stock', created_at: null},
                {id: 'assistant', role: 'assistant', content: `# Analysis\n\n${'Stock analysis details. '.repeat(100)}`, created_at: null},
            ]}}));
        await page.goto('/chat');
        const assistant = page.locator('.chat-bubble-ai');
        const user = page.locator('.chat-bubble-user');
        await expect(assistant).toBeVisible();
        for (const width of [1440, 390]) {
            await page.setViewportSize({width, height: 900});
            const geometry = await assistant.evaluate((bubble) => {
                const row = bubble.parentElement!.getBoundingClientRect();
                const rect = bubble.getBoundingClientRect();
                const prose = bubble.querySelector('.chat-prose')!;
                const actions = bubble.querySelector('.chat-message-actions')!.getBoundingClientRect();
                const texts = document.createTreeWalker(prose, NodeFilter.SHOW_TEXT);
                let overlapsActions = false;
                while (texts.nextNode()) {
                    const range = document.createRange();
                    range.selectNodeContents(texts.currentNode);
                    for (const textRect of range.getClientRects()) {
                        if (textRect.left < actions.right && textRect.right > actions.left
                            && textRect.top < actions.bottom && textRect.bottom > actions.top) {
                            overlapsActions = true;
                        }
                    }
                }
                return {
                    rowRight: row.right,
                    bubbleRight: rect.right,
                    prosePaddingRight: getComputedStyle(prose).paddingRight,
                    overlapsActions,
                };
            });
            expect(Math.abs(geometry.rowRight - geometry.bubbleRight)).toBeLessThanOrEqual(1);
            expect(geometry.prosePaddingRight).toBe('0px');
            expect(geometry.overlapsActions).toBe(false);
            const userWidth = (await user.boundingBox())!.width;
            const assistantWidth = (await assistant.boundingBox())!.width;
            expect(userWidth).toBeLessThan(assistantWidth);
        }
        await assistant.hover();
        await expect(assistant.getByRole('button', {name: 'Copy'})).toBeVisible();
        await expect(assistant.getByRole('button', {name: 'Export this message as Markdown'})).toBeVisible();
    });

    test('mobile shell opens navigation drawer', async ({page}) => {
        await page.setViewportSize({width: 390, height: 844});
        await openApp(page);

        // Try to open navigation menu
        const menuButton = page.getByRole('button', {name: /打开导航|菜单/i});
        if (await menuButton.isVisible({timeout: 2000}).catch(() => false)) {
            await menuButton.click();
        }

        // Check if navigation is visible
        await expect(page.getByRole('link', {name: '回测'})).toBeVisible({timeout: 5000});
    });

    test('language switch updates UI copy and persists after page refresh', async ({page}) => {
        await openApp(page);

        const languageToggle = page.getByRole('button', {name: '切换界面语言'});
        await expect(languageToggle).toBeVisible();
        await expect(page.getByRole('link', {name: '设置'})).toBeVisible();
        await expect(page.getByRole('link', {name: '首页'})).toBeVisible();

        await languageToggle.click();

        const englishLanguageToggle = page.getByRole('button', {name: 'Switch UI language'});
        await expect(englishLanguageToggle).toBeVisible();
        await expect(page.getByRole('link', {name: 'Settings'})).toBeVisible();
        await expect(page.getByRole('link', {name: 'Home'})).toBeVisible();
        expect(await page.evaluate(() => localStorage.getItem('dsa.uiLanguage'))).toBe('en');

        await page.reload();
        await page.waitForLoadState('domcontentloaded');

        await expect(englishLanguageToggle).toBeVisible();
        await expect(page.getByRole('link', {name: 'Settings'})).toBeVisible();
        await expect(page.getByRole('link', {name: 'Home'})).toBeVisible();

        await page.getByRole('link', {name: 'Settings'}).click();

        await expect(page.getByRole('heading', {name: 'System settings'})).toBeVisible({timeout: 10_000});

        // Navigate to the Notifications category to find the Send test button
        const notificationsTab = page.getByRole('button', {name: /^Notifications\b/});
        await expect(notificationsTab).toBeVisible({timeout: 10_000});
        await notificationsTab.click();
        await expect(page.getByRole('button', {name: 'Send test'})).toBeVisible({timeout: 10_000});
        await expect(page.getByRole('textbox', {name: 'Title'})).toHaveValue('DSA notification test');
    });

    test('backtest page renders filter controls', async ({page}) => {
        await openApp(page);

        // Navigate to backtest page by clicking the link
        await page.getByRole('link', {name: '回测'}).click();

        // Check for filter controls
        const filterInput = page.getByPlaceholder('按股票代码筛选（留空表示全部）');
        await expect(filterInput).toBeVisible({timeout: 10_000});
        await expect(page.getByRole('button', {name: '筛选'})).toBeVisible();
        await expect(page.getByRole('button', {name: '运行回测'})).toBeVisible();
    });
});
