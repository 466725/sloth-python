import { render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { UiLanguageProvider } from '../../../contexts/UiLanguageContext';
import { UI_LANGUAGE_STORAGE_KEY } from '../../../utils/uiLanguage';
import { SettingsCategoryNav } from '../SettingsCategoryNav';

describe('SettingsCategoryNav', () => {
  afterEach(() => {
    localStorage.removeItem(UI_LANGUAGE_STORAGE_KEY);
  });

  it.each([
    ['en', 'Configurations', 'System configuration grouped by module.'],
    ['zh', '配置', '按模块整理系统配置。'],
  ])('keeps the category title without its description in %s', (language, title, description) => {
    localStorage.setItem(UI_LANGUAGE_STORAGE_KEY, language);
    render(
      <UiLanguageProvider>
        <SettingsCategoryNav categories={[]} itemsByCategory={{}} activeCategory="" onSelect={vi.fn()} />
      </UiLanguageProvider>,
    );

    expect(screen.getByText(title)).toBeInTheDocument();
    expect(screen.queryByText(description)).not.toBeInTheDocument();
  });
});
