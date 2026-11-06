import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import AlertsPage from '../AlertsPage';
import { UiLanguageProvider, useUiLanguage } from '../../contexts/UiLanguageContext';
import { UI_LANGUAGE_STORAGE_KEY } from '../../utils/uiLanguage';
import {
  ALERT_HISTORY_TEXT,
  ALERT_NOTIFICATION_CHANNEL_LABELS,
  ALERT_NOTIFICATION_STATUS_LABELS,
  ALERT_PAGE_TEXT,
  ALERT_TRIGGER_STATUS_LABELS,
} from '../../locales/featureText';

function LanguageControls() {
  const { setLanguage } = useUiLanguage();
  return (
    <>
      <button onClick={() => setLanguage('en')}>English</button>
      <button onClick={() => setLanguage('zh')}>Chinese</button>
    </>
  );
}

function renderLocalizedPage(language: 'en' | 'zh' = 'en') {
  localStorage.setItem(UI_LANGUAGE_STORAGE_KEY, language);
  return render(
    <UiLanguageProvider>
      <LanguageControls />
      <AlertsPage />
    </UiLanguageProvider>,
  );
}

const {
  listRules,
  createRule,
  deleteRule,
  enableRule,
  disableRule,
  testRule,
  listTriggers,
  listNotifications,
} = vi.hoisted(() => ({
  listRules: vi.fn(),
  createRule: vi.fn(),
  deleteRule: vi.fn(),
  enableRule: vi.fn(),
  disableRule: vi.fn(),
  testRule: vi.fn(),
  listTriggers: vi.fn(),
  listNotifications: vi.fn(),
}));

vi.mock('../../api/alerts', () => ({
  alertsApi: {
    listRules,
    createRule,
    deleteRule,
    enableRule,
    disableRule,
    testRule,
    listTriggers,
    listNotifications,
  },
}));

const parsedError = {
  title: '加载失败',
  message: '告警 API 不可用',
  rawMessage: '告警 API 不可用',
  category: 'http_error' as const,
  status: 500,
};

const rule = {
  id: 1,
  name: '茅台涨跌幅',
  targetScope: 'single_symbol' as const,
  target: '600519',
  alertType: 'price_change_percent' as const,
  parameters: { direction: 'up' as const, changePct: 3 },
  severity: 'warning' as const,
  enabled: true,
  source: 'api',
  createdAt: '2026-05-18T09:00:00',
  updatedAt: '2026-05-18T09:30:00',
};

function createDeferred<T>() {
  let resolve!: (value: T) => void;
  const promise = new Promise<T>((promiseResolve) => {
    resolve = promiseResolve;
  });
  return { promise, resolve };
}

beforeEach(() => {
  localStorage.removeItem(UI_LANGUAGE_STORAGE_KEY);
  vi.clearAllMocks();
  listRules.mockResolvedValue({ items: [rule], total: 1, page: 1, pageSize: 20 });
  listTriggers.mockResolvedValue({
    items: [
      {
        id: 10,
        ruleId: 1,
        target: '600519',
        observedValue: 3.1,
        threshold: 3,
        reason: '600519 price up 3%',
        dataSource: 'realtime_quote',
        dataTimestamp: '2026-05-18T09:30:00',
        triggeredAt: '2026-05-18T09:30:01',
        status: 'triggered',
      },
    ],
    total: 1,
    page: 1,
    pageSize: 20,
  });
  listNotifications.mockResolvedValue({ items: [], total: 0, page: 1, pageSize: 20 });
  testRule.mockResolvedValue({
    ruleId: 1,
    status: 'triggered',
    triggered: true,
    observedValue: 3.1,
    message: '600519 price up 3%',
  });
  createRule.mockResolvedValue(rule);
  disableRule.mockResolvedValue({ ...rule, enabled: false });
  enableRule.mockResolvedValue(rule);
  deleteRule.mockResolvedValue({ deleted: 1 });
});

afterEach(() => {
  localStorage.removeItem(UI_LANGUAGE_STORAGE_KEY);
});

describe('AlertsPage', () => {
  it('keeps all Alert Center translation keys complete in English', () => {
    for (const dictionary of [
      ALERT_PAGE_TEXT,
      ALERT_HISTORY_TEXT,
      ALERT_TRIGGER_STATUS_LABELS,
      ALERT_NOTIFICATION_CHANNEL_LABELS,
      ALERT_NOTIFICATION_STATUS_LABELS,
    ]) {
      expect(Object.keys(dictionary.en).sort()).toEqual(Object.keys(dictionary.zh).sort());
      expect(JSON.stringify(dictionary.en)).not.toMatch(/\p{Script=Han}/u);
    }
  });

  it('renders the whole empty page in persisted English', async () => {
    listRules.mockResolvedValue({ items: [], total: 0, page: 1, pageSize: 20 });
    listTriggers.mockResolvedValue({ items: [], total: 0, page: 1, pageSize: 20 });
    const { container } = renderLocalizedPage();

    expect(await screen.findByText('No notification attempts')).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Alert Center' })).toBeInTheDocument();
    expect(screen.getByText('No trigger history')).toBeInTheDocument();
    expect(screen.getByText('Evaluation records')).toBeInTheDocument();
    expect(screen.getByText('No alert rules')).toBeInTheDocument();
    expect(document.title).toBe('Alert Center - DSA');
    expect(container.textContent).not.toMatch(/\p{Script=Han}/u);
  });

  it('updates loaded history, phase, notifications and form drafts without refetching on language changes', async () => {
    listRules.mockResolvedValue({ items: [{ ...rule, name: 'Price alert' }], total: 1, page: 1, pageSize: 20 });
    listTriggers.mockResolvedValue({
      items: ['triggered', 'skipped', 'degraded', 'failed', 'future_status'].map((status, index) => ({
        id: index + 10,
        target: 'AAPL',
        status,
        reason: 'Provider details',
        marketPhaseSummary: { phase: 'intraday', market: 'US', warnings: [] },
        analysisContextPackOverview: {
          dataQuality: { level: 'usable', blockScores: {}, limitations: ['Delayed quote', 'Partial data'] },
        },
      })),
      total: 5,
    });
    listNotifications.mockResolvedValue({
      items: [
        { id: 1, channel: '__cooldown__', success: false, errorCode: 'cooldown_active' },
        { id: 2, channel: '__cooldown_read_failed__', success: false, errorCode: 'cooldown_read_failed' },
        { id: 3, channel: '__noise_suppressed__', success: false, errorCode: 'noise_suppressed' },
        { id: 4, channel: '__no_channel__', success: false, errorCode: 'no_channel' },
        { id: 5, channel: '__dispatch__', success: false, errorCode: 'unexpected_error' },
        { id: 6, channel: '__context__', success: true },
        { id: 7, channel: 'email', success: true, latencyMs: 42, diagnostics: 'Provider details' },
      ],
      total: 7,
    });
    const { container } = renderLocalizedPage();
    await screen.findByText('Alert cooldown');
    expect(screen.getAllByText('US · Intraday')).toHaveLength(5);
    expect(screen.getAllByText('Quality: usable')).toHaveLength(5);
    expect(screen.getAllByText('Delayed quote; Partial data')).toHaveLength(5);
    expect(screen.getByText('future_status')).toBeInTheDocument();
    expect(screen.getByText('email')).toBeInTheDocument();
    expect(screen.getByText('42ms')).toBeInTheDocument();
    for (const label of Object.values(ALERT_TRIGGER_STATUS_LABELS.en)) {
      expect(screen.getAllByText(label).length).toBeGreaterThan(0);
    }
    for (const label of Object.values(ALERT_NOTIFICATION_CHANNEL_LABELS.en)) {
      expect(screen.getAllByText(label).length).toBeGreaterThan(0);
    }
    for (const label of Object.values(ALERT_NOTIFICATION_STATUS_LABELS.en)) {
      expect(screen.getAllByText(label).length).toBeGreaterThan(0);
    }
    expect(container.textContent).not.toMatch(/\p{Script=Han}/u);

    fireEvent.change(screen.getByLabelText('Symbol'), { target: { value: 'aapl' } });
    fireEvent.change(screen.getByLabelText('Change threshold (%)'), { target: { value: '2.5' } });
    fireEvent.click(screen.getByRole('button', { name: 'Chinese' }));
    expect(screen.getByRole('heading', { name: '告警中心' })).toBeInTheDocument();
    expect(screen.getByText('触发历史')).toBeInTheDocument();
    expect(screen.getAllByText('US · 盘中')).toHaveLength(5);
    expect(screen.getAllByText('质量：usable')).toHaveLength(5);
    expect(screen.getByText('业务冷却')).toBeInTheDocument();
    expect(screen.getByText('冷却抑制')).toBeInTheDocument();
    expect(screen.getByLabelText('标的代码')).toHaveValue('aapl');
    expect(screen.getByLabelText('涨跌幅阈值（%）')).toHaveValue(2.5);
    expect(document.title).toBe('告警中心 - DSA');

    fireEvent.click(screen.getByRole('button', { name: 'English' }));
    expect(screen.getByLabelText('Symbol')).toHaveValue('aapl');
    expect(container.textContent).not.toMatch(/\p{Script=Han}/u);
    expect(listRules).toHaveBeenCalledTimes(1);
    expect(listTriggers).toHaveBeenCalledTimes(1);
    expect(listNotifications).toHaveBeenCalledTimes(1);
    expect(createRule).not.toHaveBeenCalled();
  });

  it('retranslates existing creation and batch test feedback without repeating mutations', async () => {
    listRules.mockResolvedValue({ items: [{ ...rule, name: 'Price alert' }], total: 1, page: 1, pageSize: 20 });
    createRule.mockResolvedValue({ ...rule, name: 'Created alert' });
    testRule.mockResolvedValue({
      ruleId: 1,
      status: 'triggered',
      triggered: true,
      observedValue: 3.1,
      message: 'Evaluated two symbols',
      evaluatedCount: 2,
      triggeredCount: 1,
      degradedCount: 1,
      skippedCount: 0,
      targetResults: [
        { target: 'AAPL', status: 'triggered', recordStatus: 'triggered' },
        { target: 'MSFT', status: 'not_triggered', recordStatus: 'degraded' },
      ],
    });
    renderLocalizedPage();
    fireEvent.click(await screen.findByRole('button', { name: 'Test' }));
    expect(await screen.findByText('Test result')).toBeInTheDocument();
    expect(screen.getByText(/Status: triggered · Triggered: Yes · Observed value: 3.1/)).toBeInTheDocument();
    expect(screen.getByText('Evaluated 2 · Triggered 1 · Degraded 1 · Skipped 0')).toBeInTheDocument();
    expect(screen.getByText('not_triggered / degraded')).toBeInTheDocument();

    fireEvent.change(screen.getByLabelText('Symbol'), { target: { value: 'aapl' } });
    fireEvent.change(screen.getByLabelText('Change threshold (%)'), { target: { value: '2' } });
    fireEvent.click(screen.getByRole('button', { name: 'Create rule' }));
    expect(await screen.findByText('Created alert rule "Created alert"')).toBeInTheDocument();
    expect(createRule).toHaveBeenCalledWith(expect.objectContaining({ target: 'AAPL', parameters: { direction: 'up', changePct: 2 } }));
    fireEvent.click(screen.getByRole('button', { name: 'Chinese' }));
    expect(screen.getByText('已创建告警规则「Created alert」')).toBeInTheDocument();
    expect(screen.getByText('测试结果')).toBeInTheDocument();
    expect(screen.getByText('评估 2 · 触发 1 · 降级 1 · 跳过 0')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'English' }));
    expect(screen.getByText('Created alert rule "Created alert"')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Close' }));
    expect(screen.queryByText('Created alert rule "Created alert"')).not.toBeInTheDocument();
    expect(createRule).toHaveBeenCalledTimes(1);
    expect(testRule).toHaveBeenCalledTimes(1);
  });

  it('renders loading history and notification labels in English', async () => {
    const pendingTriggers = createDeferred<{ items: []; total: number }>();
    const pendingNotifications = createDeferred<{ items: []; total: number }>();
    listRules.mockResolvedValue({ items: [], total: 0 });
    listTriggers.mockReturnValue(pendingTriggers.promise);
    listNotifications.mockReturnValue(pendingNotifications.promise);
    renderLocalizedPage();
    expect(await screen.findByText('Loading trigger history')).toBeInTheDocument();
    expect(screen.getByText('Loading notification attempts')).toBeInTheDocument();
    pendingTriggers.resolve({ items: [], total: 0 });
    pendingNotifications.resolve({ items: [], total: 0 });
    expect(await screen.findByText('No trigger history')).toBeInTheDocument();
    expect(await screen.findByText('No notification attempts')).toBeInTheDocument();
  });

  it('loads rules, trigger history, and notification empty state', async () => {
    render(<AlertsPage />);

    expect(screen.getByText('管理单标的和自选股涨跌幅告警，执行一次性测试，并查看后台评估任务记录的触发历史与邮件通知诊断。')).toBeInTheDocument();
    expect(await screen.findByText('茅台涨跌幅')).toBeInTheDocument();
    expect(await screen.findByText('600519 price up 3%')).toBeInTheDocument();
    expect(await screen.findByText('暂无通知尝试记录')).toBeInTheDocument();
    expect(listRules).toHaveBeenCalledWith({
      enabled: undefined,
      alertType: undefined,
      page: 1,
      pageSize: 20,
    });
    expect(listTriggers).toHaveBeenCalledWith({ page: 1, pageSize: 20 });
    expect(listNotifications).toHaveBeenCalledWith({ page: 1, pageSize: 20 });
  });

  it('runs a dry-run test and renders only declared response fields', async () => {
    listTriggers.mockResolvedValueOnce({ items: [], total: 0, page: 1, pageSize: 20 });
    render(<AlertsPage />);

    fireEvent.click(await screen.findByRole('button', { name: '测试' }));

    await waitFor(() => expect(testRule).toHaveBeenCalledWith(1));
    expect(await screen.findByText('测试结果')).toBeInTheDocument();
    expect(screen.getByText(/600519 price up 3%/)).toBeInTheDocument();
    expect(screen.getByText(/观察值：3\.1/)).toBeInTheDocument();
    expect(screen.queryByText(/realtime_quote/)).not.toBeInTheDocument();
  });

  it('renders batch dry-run summary and target results', async () => {
    testRule.mockResolvedValueOnce({
      ruleId: 1,
      targetScope: 'watchlist',
      status: 'triggered',
      triggered: true,
      observedValue: 11,
      message: 'Evaluated 2 targets',
      evaluatedCount: 2,
      triggeredCount: 1,
      degradedCount: 1,
      skippedCount: 0,
      targetResults: [
        {
          target: '600519',
          displayTarget: '自选股 - 600519',
          status: 'triggered',
          recordStatus: 'triggered',
          triggered: true,
          observedValue: 11,
          message: 'triggered',
        },
        {
          target: '000001',
          displayTarget: '自选股 - 000001',
          status: 'not_triggered',
          recordStatus: 'degraded',
          triggered: false,
          observedValue: null,
          message: 'degraded',
        },
      ],
    });
    render(<AlertsPage />);

    fireEvent.click(await screen.findByRole('button', { name: '测试' }));

    expect(await screen.findByText(/评估 2 · 触发 1 · 降级 1 · 跳过 0/)).toBeInTheDocument();
    expect(screen.getByText('自选股 - 600519')).toBeInTheDocument();
    expect(screen.getByText(/not_triggered \/ degraded/)).toBeInTheDocument();
  });

  it('creates a rule through the page form and reloads rules', async () => {
    render(<AlertsPage />);

    await screen.findByText('茅台涨跌幅');
    fireEvent.change(screen.getByLabelText('标的代码'), { target: { value: 'aapl' } });
    fireEvent.change(screen.getByLabelText('涨跌幅阈值（%）'), { target: { value: '2' } });
    fireEvent.click(screen.getByRole('button', { name: '创建规则' }));

    await waitFor(() => {
      expect(createRule).toHaveBeenCalledWith(expect.objectContaining({
        target: 'AAPL',
        alertType: 'price_change_percent',
        parameters: { direction: 'up', changePct: 2 },
      }));
    });
    expect(await screen.findByText(/已创建告警规则/)).toBeInTheDocument();
  });

  it('keeps create form values when create API fails', async () => {
    createRule.mockRejectedValueOnce({ parsedError });
    render(<AlertsPage />);

    await screen.findByText('茅台涨跌幅');
    fireEvent.change(screen.getByLabelText('标的代码'), { target: { value: 'aapl' } });
    fireEvent.change(screen.getByLabelText('涨跌幅阈值（%）'), { target: { value: '2' } });
    fireEvent.click(screen.getByRole('button', { name: '创建规则' }));

    expect(await screen.findByText('加载失败')).toBeInTheDocument();
    expect(screen.getByLabelText('标的代码')).toHaveValue('aapl');
    expect(screen.getByLabelText('涨跌幅阈值（%）')).toHaveValue(2);
  });

  it('clamps rules pagination when a mutation leaves the current page empty', async () => {
    const page2Rule = { ...rule, id: 2, name: '第二页规则', target: 'AAPL' };
    listRules
      .mockResolvedValueOnce({ items: [rule], total: 21, page: 1, pageSize: 20 })
      .mockResolvedValueOnce({ items: [page2Rule], total: 21, page: 2, pageSize: 20 })
      .mockResolvedValueOnce({ items: [], total: 20, page: 2, pageSize: 20 })
      .mockResolvedValue({ items: [rule], total: 20, page: 1, pageSize: 20 });

    render(<AlertsPage />);

    expect(await screen.findByText('茅台涨跌幅')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: '2' }));
    expect(await screen.findByText('第二页规则')).toBeInTheDocument();
    fireEvent.click(screen.getByLabelText('删除 第二页规则'));
    fireEvent.click(await screen.findByRole('button', { name: '删除' }));

    await waitFor(() => expect(deleteRule).toHaveBeenCalledWith(2));
    await waitFor(() => {
      expect(listRules).toHaveBeenCalledWith({
        enabled: undefined,
        alertType: undefined,
        page: 1,
        pageSize: 20,
      });
    });
    expect(await screen.findByText('茅台涨跌幅')).toBeInTheDocument();
  });

  it('keeps the latest rules response when filter requests resolve out of order', async () => {
    const initialRequest = createDeferred<{ items: Array<typeof rule>; total: number; page: number; pageSize: number }>();
    const filteredRequest = createDeferred<{ items: Array<typeof rule>; total: number; page: number; pageSize: number }>();
    const staleRule = { ...rule, id: 3, name: '旧筛选规则', enabled: true };
    const filteredRule = { ...rule, id: 4, name: '停用规则', enabled: false };
    listRules
      .mockReset()
      .mockReturnValueOnce(initialRequest.promise)
      .mockReturnValueOnce(filteredRequest.promise);

    render(<AlertsPage />);

    fireEvent.change(screen.getByLabelText('启停状态'), { target: { value: 'disabled' } });
    await waitFor(() => expect(listRules).toHaveBeenCalledTimes(2));

    filteredRequest.resolve({ items: [filteredRule], total: 1, page: 1, pageSize: 20 });
    expect(await screen.findByText('停用规则')).toBeInTheDocument();

    initialRequest.resolve({ items: [staleRule], total: 1, page: 1, pageSize: 20 });
    await waitFor(() => expect(screen.queryByText('旧筛选规则')).not.toBeInTheDocument());
    expect(screen.getByText('停用规则')).toBeInTheDocument();
  });

  it('renders API errors through ApiErrorAlert', async () => {
    listRules.mockRejectedValueOnce({ parsedError });

    render(<AlertsPage />);

    expect(await screen.findByText('加载失败')).toBeInTheDocument();
    expect(screen.getByText('告警 API 不可用')).toBeInTheDocument();
  });
});
