import {expect, test} from '@playwright/test';

test.use({
    viewport: {width: 1844, height: 796},
    launchOptions: {
        ignoreDefaultArgs: ['--hide-scrollbars'],
        args: ['--disable-features=OverlayScrollbar,FluentOverlayScrollbar'],
    },
});

test('keeps the desktop rail in place across routes and scrollbar changes', async ({page}) => {
    await page.addInitScript(() => localStorage.setItem('dsa.uiLanguage', 'en'));
    await page.goto('/');
    const rail = page.getByRole('complementary', {name: 'Desktop sidebar navigation'});
    const main = page.getByRole('main');
    const position = () => rail.evaluate((element) => {
        const {x, y} = element.getBoundingClientRect();
        return {x, y};
    });

    await expect(rail).toBeVisible();
    const homePosition = await position();

    // Force document overflow independently of page data or loading states.
    await main.evaluate((element) => { element.style.minHeight = '200vh'; });
    expect(await position()).toEqual(homePosition);
    await main.evaluate((element) => { element.style.removeProperty('min-height'); });

    for (const route of ['/chat', '/decision-signals', '/backtest', '/alerts', '/usage', '/settings', '/']) {
        const link = rail.locator(`a[href="${route}"]`);
        await link.click();
        await expect(link).toHaveAttribute('aria-current', 'page');
        expect(await position(), `sidebar position on ${route}`).toEqual(homePosition);
    }
});

test('keeps desktop navigation labels and icons in place when the active route changes', async ({page}) => {
    await page.addInitScript(() => localStorage.setItem('dsa.uiLanguage', 'en'));
    await page.goto('/');
    await page.addStyleTag({content: '*, *::before, *::after { transition: none !important; animation: none !important; }'});
    await page.evaluate(() => document.fonts.ready);
    const rail = page.getByRole('complementary', {name: 'Desktop sidebar navigation'});
    await expect(rail).toBeVisible();
    const positions = () => rail.evaluate((element) =>
        Array.from(element.querySelectorAll('nav > a, nav > div > button')).map((item) => {
            const icon = item.querySelector('svg')!.getBoundingClientRect();
            const label = item.querySelector('span')!.getBoundingClientRect();
            return {iconX: icon.x, iconY: icon.y, labelX: label.x, labelY: label.y};
        }),
    );
    const homePositions = await positions();
    expect(homePositions).toHaveLength(9);

    for (const route of ['/decision-signals', '/backtest', '/']) {
        const link = rail.locator(`a[href="${route}"]`);
        await link.click();
        await expect(link).toHaveAttribute('aria-current', 'page');
        expect(await positions(), `navigation positions on ${route}`).toEqual(homePositions);
    }
});
