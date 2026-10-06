import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { AlertRuleForm } from '../AlertRuleForm';
import { UiLanguageProvider } from '../../../contexts/UiLanguageContext';
import { UI_LANGUAGE_STORAGE_KEY } from '../../../utils/uiLanguage';

describe('AlertRuleForm', () => {
  const onSubmit = vi.fn();

  beforeEach(() => {
    onSubmit.mockReset();
    onSubmit.mockResolvedValue(undefined);
    window.localStorage.clear();
  });

  it('offers only a read-only price change type and single symbol/watchlist scopes', () => {
    render(<AlertRuleForm onSubmit={onSubmit} />);

    expect(screen.getByLabelText('规则类型')).toHaveValue('涨跌幅');
    expect(screen.getByLabelText('规则类型')).toHaveAttribute('readonly');
    expect(within(screen.getByLabelText('目标范围')).getAllByRole('option').filter((option) => !option.hasAttribute('disabled')).map((option) => option.getAttribute('value')))
      .toEqual(['single_symbol', 'watchlist']);
    expect(within(screen.getByLabelText('方向')).getAllByRole('option').filter((option) => !option.hasAttribute('disabled')).map((option) => option.getAttribute('value')))
      .toEqual(['up', 'down']);
    expect(screen.getAllByRole('spinbutton')).toHaveLength(1);
  });

  it('submits an upward price change rule', async () => {
    render(<AlertRuleForm onSubmit={onSubmit} />);
    fireEvent.change(screen.getByLabelText('规则名称'), { target: { value: '茅台涨跌幅' } });
    fireEvent.change(screen.getByLabelText('标的代码'), { target: { value: '600519' } });
    fireEvent.change(screen.getByLabelText('涨跌幅阈值（%）'), { target: { value: '2.5' } });
    fireEvent.click(screen.getByRole('button', { name: '创建规则' }));

    await waitFor(() => expect(onSubmit).toHaveBeenCalledWith({
      name: '茅台涨跌幅',
      targetScope: 'single_symbol',
      target: '600519',
      alertType: 'price_change_percent',
      parameters: { direction: 'up', changePct: 2.5 },
      severity: 'warning',
      enabled: true,
    }));
    expect(screen.getByLabelText('涨跌幅阈值（%）')).toHaveValue(null);
  });

  it('shows only price change controls and positive percentage validation in English', () => {
    window.localStorage.setItem(UI_LANGUAGE_STORAGE_KEY, 'en');
    render(<UiLanguageProvider><AlertRuleForm onSubmit={onSubmit} /></UiLanguageProvider>);
    expect(screen.getByLabelText('Rule type')).toHaveValue('Price change');
    expect(screen.getByLabelText('Rule type')).toHaveAttribute('readonly');
    expect(within(screen.getByLabelText('Target scope')).getAllByRole('option').filter((option) => !option.hasAttribute('disabled')).map((option) => option.textContent))
      .toEqual(['Single symbol', 'Watchlist']);
    expect(screen.getAllByRole('spinbutton')).toHaveLength(1);
    fireEvent.change(screen.getByLabelText('Symbol'), { target: { value: 'AAPL' } });
    fireEvent.change(screen.getByLabelText('Change threshold (%)'), { target: { value: '-2' } });
    fireEvent.click(screen.getByRole('button', { name: 'Create rule' }));
    expect(screen.getByRole('alert')).toHaveTextContent('Change threshold (%) must be a number greater than 0');
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it('submits a downward price change with severity and disabled creation', async () => {
    render(<AlertRuleForm onSubmit={onSubmit} />);
    fireEvent.change(screen.getByLabelText('标的代码'), { target: { value: 'aapl' } });
    fireEvent.change(screen.getByLabelText('方向'), { target: { value: 'down' } });
    fireEvent.change(screen.getByLabelText('涨跌幅阈值（%）'), { target: { value: '3.5' } });
    fireEvent.change(screen.getByLabelText('严重级别'), { target: { value: 'critical' } });
    fireEvent.click(screen.getByLabelText('创建后立即启用'));
    fireEvent.click(screen.getByRole('button', { name: '创建规则' }));

    await waitFor(() => expect(onSubmit).toHaveBeenCalledWith(expect.objectContaining({
      target: 'AAPL',
      parameters: { direction: 'down', changePct: 3.5 },
      severity: 'critical',
      enabled: false,
    })));
  });

  it.each(['', '0', '-3', 'Infinity', 'NaN'])('rejects invalid percentage %j', (value) => {
    render(<AlertRuleForm onSubmit={onSubmit} />);
    fireEvent.change(screen.getByLabelText('标的代码'), { target: { value: '600519' } });
    fireEvent.change(screen.getByLabelText('涨跌幅阈值（%）'), { target: { value } });
    fireEvent.click(screen.getByRole('button', { name: '创建规则' }));
    expect(screen.getByRole('alert')).toHaveTextContent('涨跌幅阈值（%）必须是大于 0 的数字');
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it('rejects invalid stock codes', () => {
    render(<AlertRuleForm onSubmit={onSubmit} />);
    fireEvent.change(screen.getByLabelText('标的代码'), { target: { value: 'aapl-2026' } });
    fireEvent.change(screen.getByLabelText('涨跌幅阈值（%）'), { target: { value: '3' } });
    fireEvent.click(screen.getByRole('button', { name: '创建规则' }));
    expect(screen.getByRole('alert')).toHaveTextContent('股票代码格式不正确');
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it('submits a watchlist rule without requiring a stock code', async () => {
    render(<AlertRuleForm onSubmit={onSubmit} />);
    fireEvent.change(screen.getByLabelText('目标范围'), { target: { value: 'watchlist' } });
    expect(screen.queryByLabelText('标的代码')).not.toBeInTheDocument();
    expect(screen.getByLabelText('目标')).toHaveValue('default');
    fireEvent.change(screen.getByLabelText('涨跌幅阈值（%）'), { target: { value: '10' } });
    fireEvent.click(screen.getByRole('button', { name: '创建规则' }));
    await waitFor(() => expect(onSubmit).toHaveBeenCalledWith(expect.objectContaining({
      targetScope: 'watchlist',
      target: 'default',
      alertType: 'price_change_percent',
      parameters: { direction: 'up', changePct: 10 },
    })));
  });

  it('keeps values when submission fails', async () => {
    onSubmit.mockResolvedValueOnce(false);
    render(<AlertRuleForm onSubmit={onSubmit} />);
    fireEvent.change(screen.getByLabelText('标的代码'), { target: { value: 'aapl' } });
    fireEvent.change(screen.getByLabelText('方向'), { target: { value: 'down' } });
    fireEvent.change(screen.getByLabelText('涨跌幅阈值（%）'), { target: { value: '2' } });
    fireEvent.click(screen.getByRole('button', { name: '创建规则' }));
    await waitFor(() => expect(onSubmit).toHaveBeenCalled());
    expect(screen.getByLabelText('标的代码')).toHaveValue('aapl');
    expect(screen.getByLabelText('涨跌幅阈值（%）')).toHaveValue(2);
    expect(screen.getByLabelText('方向')).toHaveValue('down');
  });
});
