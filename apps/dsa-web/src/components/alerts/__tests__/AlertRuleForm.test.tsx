import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { AlertRuleForm } from '../AlertRuleForm';
import { systemConfigApi } from '../../../api/systemConfig';
import { UiLanguageProvider, useUiLanguage } from '../../../contexts/UiLanguageContext';
import { UI_LANGUAGE_STORAGE_KEY } from '../../../utils/uiLanguage';

vi.mock('../../../api/systemConfig', () => ({
  systemConfigApi: {
    getWatchlist: vi.fn(),
  },
}));

function LanguageControls() {
  const { setLanguage } = useUiLanguage();
  return <button onClick={() => setLanguage('en')}>English</button>;
}

describe('AlertRuleForm', () => {
  const onSubmit = vi.fn();

  beforeEach(() => {
    onSubmit.mockReset();
    onSubmit.mockResolvedValue(undefined);
    vi.mocked(systemConfigApi.getWatchlist).mockReset();
    vi.mocked(systemConfigApi.getWatchlist).mockResolvedValue(['600519', 'AAPL']);
    window.localStorage.clear();
  });

  it('offers stock list symbols and fixes the target scope to a read-only single symbol input', async () => {
    render(<AlertRuleForm onSubmit={onSubmit} />);

    await screen.findByRole('option', { name: '600519' });
    expect(screen.queryByText('Web 告警中心')).not.toBeInTheDocument();
    const controlGrid = screen.getByLabelText('标的代码').closest('.grid');
    expect(controlGrid).toHaveClass('md:grid-cols-2', 'lg:grid-cols-3');
    expect(screen.queryByLabelText('规则名称')).not.toBeInTheDocument();
    const orderedControls = [
      screen.getByLabelText('标的代码'),
      screen.getByLabelText('严重级别'),
      screen.getByLabelText('方向'),
      screen.getByLabelText('涨跌幅阈值（%）'),
      screen.getByLabelText('创建后立即启用'),
      screen.getByRole('button', { name: '创建规则' }),
    ];
    for (let index = 0; index < orderedControls.length - 1; index += 1) {
      expect(
        orderedControls[index].compareDocumentPosition(orderedControls[index + 1])
          & Node.DOCUMENT_POSITION_FOLLOWING,
      ).toBeTruthy();
    }
    expect(screen.getByLabelText('规则类型')).toHaveValue('涨跌幅');
    expect(screen.getByLabelText('规则类型')).toHaveAttribute('readonly');
    expect(screen.getByLabelText('目标范围')).toHaveValue('单标的');
    expect(screen.getByLabelText('目标范围').tagName).toBe('INPUT');
    expect(screen.getByLabelText('目标范围')).toHaveAttribute('readonly');
    expect(screen.getByLabelText('标的代码').tagName).toBe('SELECT');
    expect(Array.from((screen.getByLabelText('标的代码') as HTMLSelectElement).options).map((option) => option.value))
      .toEqual(['', '600519', 'AAPL']);
    expect(within(screen.getByLabelText('方向')).getAllByRole('option').filter((option) => !option.hasAttribute('disabled')).map((option) => option.getAttribute('value')))
      .toEqual(['up', 'down']);
    expect(screen.getAllByRole('spinbutton')).toHaveLength(1);
  });

  it('submits an upward price change rule', async () => {
    render(<AlertRuleForm onSubmit={onSubmit} />);
    await screen.findByRole('option', { name: '600519' });
    fireEvent.change(screen.getByLabelText('标的代码'), { target: { value: '600519' } });
    fireEvent.change(screen.getByLabelText('涨跌幅阈值（%）'), { target: { value: '2.5' } });
    fireEvent.click(screen.getByRole('button', { name: '创建规则' }));

    await waitFor(() => expect(onSubmit).toHaveBeenCalledWith({
      targetScope: 'single_symbol',
      target: '600519',
      alertType: 'price_change_percent',
      parameters: { direction: 'up', changePct: 2.5 },
      severity: 'warning',
      enabled: true,
    }));
    expect(screen.getByLabelText('涨跌幅阈值（%）')).toHaveValue(null);
  });

  it('shows only price change controls and positive percentage validation in English', async () => {
    window.localStorage.setItem(UI_LANGUAGE_STORAGE_KEY, 'en');
    render(<UiLanguageProvider><AlertRuleForm onSubmit={onSubmit} /></UiLanguageProvider>);
    await screen.findByRole('option', { name: 'AAPL' });
    expect(screen.getByLabelText('Rule type')).toHaveValue('Price change');
    expect(screen.getByLabelText('Rule type')).toHaveAttribute('readonly');
    expect(screen.getByLabelText('Target scope')).toHaveValue('Single symbol');
    expect(screen.getByLabelText('Target scope').tagName).toBe('INPUT');
    expect(screen.getByLabelText('Target scope')).toHaveAttribute('readonly');
    expect(screen.getAllByRole('spinbutton')).toHaveLength(1);
    fireEvent.change(screen.getByLabelText('Symbol'), { target: { value: 'AAPL' } });
    fireEvent.change(screen.getByLabelText('Change threshold (%)'), { target: { value: '-2' } });
    fireEvent.click(screen.getByRole('button', { name: 'Create rule' }));
    expect(screen.getByRole('alert')).toHaveTextContent('Change threshold (%) must be a number greater than 0');
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it('submits a downward price change with severity and disabled creation', async () => {
    render(<AlertRuleForm onSubmit={onSubmit} />);
    await screen.findByRole('option', { name: 'AAPL' });
    fireEvent.change(screen.getByLabelText('标的代码'), { target: { value: 'AAPL' } });
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

  it.each(['', '0', '-3', 'Infinity', 'NaN'])('rejects invalid percentage %j', async (value) => {
    render(<AlertRuleForm onSubmit={onSubmit} />);
    await screen.findByRole('option', { name: '600519' });
    fireEvent.change(screen.getByLabelText('标的代码'), { target: { value: '600519' } });
    fireEvent.change(screen.getByLabelText('涨跌幅阈值（%）'), { target: { value } });
    fireEvent.click(screen.getByRole('button', { name: '创建规则' }));
    expect(screen.getByRole('alert')).toHaveTextContent('涨跌幅阈值（%）必须是大于 0 的数字');
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it('rejects invalid stock codes that appear in the configured list', async () => {
    vi.mocked(systemConfigApi.getWatchlist).mockResolvedValueOnce(['aapl-2026']);
    render(<AlertRuleForm onSubmit={onSubmit} />);
    await screen.findByRole('option', { name: 'aapl-2026' });
    fireEvent.change(screen.getByLabelText('标的代码'), { target: { value: 'aapl-2026' } });
    fireEvent.change(screen.getByLabelText('涨跌幅阈值（%）'), { target: { value: '3' } });
    fireEvent.click(screen.getByRole('button', { name: '创建规则' }));
    expect(screen.getByRole('alert')).toHaveTextContent('股票代码格式不正确');
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it.each(['stockCode', 'threshold'])('retranslates an existing %s validation error without resetting inputs', async (kind) => {
    window.localStorage.setItem(UI_LANGUAGE_STORAGE_KEY, 'zh');
    vi.mocked(systemConfigApi.getWatchlist).mockResolvedValueOnce(['invalid-code', 'AAPL']);
    render(
      <UiLanguageProvider>
        <LanguageControls />
        <AlertRuleForm onSubmit={onSubmit} />
      </UiLanguageProvider>,
    );
    await screen.findByRole('option', { name: 'invalid-code' });
    const target = kind === 'stockCode' ? 'invalid-code' : 'AAPL';
    fireEvent.change(screen.getByLabelText('标的代码'), { target: { value: target } });
    fireEvent.change(screen.getByLabelText('涨跌幅阈值（%）'), { target: { value: '-2' } });
    fireEvent.click(screen.getByRole('button', { name: '创建规则' }));
    expect(screen.getByRole('alert')).toHaveTextContent(kind === 'stockCode' ? '股票代码格式不正确' : '涨跌幅阈值（%）必须是大于 0 的数字');
    fireEvent.click(screen.getByRole('button', { name: 'English' }));
    expect(screen.getByRole('alert')).toHaveTextContent(kind === 'stockCode' ? 'Invalid stock code format' : 'Change threshold (%) must be a number greater than 0');
    expect(screen.getByLabelText('Symbol')).toHaveValue(target);
    expect(screen.getByLabelText('Change threshold (%)')).toHaveValue(-2);
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it('shows a visible error when the configured stock list cannot be loaded', async () => {
    vi.mocked(systemConfigApi.getWatchlist).mockRejectedValueOnce(new Error('stock list unavailable'));
    render(<AlertRuleForm onSubmit={onSubmit} />);

    expect(await screen.findByRole('alert')).toHaveTextContent('stock list unavailable');
    expect(screen.getByLabelText('标的代码')).toBeDisabled();
  });

  it('explains when no stock symbols are configured', async () => {
    vi.mocked(systemConfigApi.getWatchlist).mockResolvedValueOnce([]);
    render(<AlertRuleForm onSubmit={onSubmit} />);

    expect(await screen.findByText(/STOCK_LIST/)).toBeInTheDocument();
    expect(screen.getByLabelText('标的代码')).toBeDisabled();
  });

  it('keeps values when submission fails', async () => {
    onSubmit.mockResolvedValueOnce(false);
    render(<AlertRuleForm onSubmit={onSubmit} />);
    await screen.findByRole('option', { name: 'AAPL' });
    fireEvent.change(screen.getByLabelText('标的代码'), { target: { value: 'AAPL' } });
    fireEvent.change(screen.getByLabelText('方向'), { target: { value: 'down' } });
    fireEvent.change(screen.getByLabelText('涨跌幅阈值（%）'), { target: { value: '2' } });
    fireEvent.click(screen.getByRole('button', { name: '创建规则' }));
    await waitFor(() => expect(onSubmit).toHaveBeenCalled());
    expect(screen.getByLabelText('标的代码')).toHaveValue('AAPL');
    expect(screen.getByLabelText('涨跌幅阈值（%）')).toHaveValue(2);
    expect(screen.getByLabelText('方向')).toHaveValue('down');
  });
});
