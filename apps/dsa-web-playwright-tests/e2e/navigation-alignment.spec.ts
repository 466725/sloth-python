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
