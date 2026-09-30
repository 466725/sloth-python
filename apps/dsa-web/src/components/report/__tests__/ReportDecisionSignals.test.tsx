import { act, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import type React from 'react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { decisionSignalsApi } from '../../../api/decisionSignals';
import { UiLanguageProvider } from '../../../contexts/UiLanguageContext';
import type {
  DecisionSignalFeedbackItem,
  DecisionSignalItem,
  DecisionSignalOutcomeItem,
} from '../../../types/decisionSignals';
import { ReportDecisionSignals } from '../ReportDecisionSignals';

vi.mock('../../../api/decisionSignals', () => ({
  decisionSignalsApi: {
    list: vi.fn(),
    getSignalOutcomes: vi.fn(),
    getFeedback: vi.fn(),
  },
}));

const signal: DecisionSignalItem = {
  id: 21,
  stockCode: 'HK00700',
  stockName: '腾讯控股',
  market: 'hk',
  sourceType: 'analysis',
  sourceReportId: 5,
  marketPhase: 'postmarket',
  triggerSource: 'history',
  action: 'watch',
  actionLabel: null,
  confidence: 0.6,
  score: 70,
  horizon: '5d',
  entryLow: null,
  entryHigh: null,
  stopLoss: null,
  targetPrice: null,
  invalidation: null,
  watchConditions: '观察回购强度',
  reason: '结构等待确认',
  riskSummary: '缺少成交量确认',
  catalystSummary: null,
  evidence: undefined,
  dataQualitySummary: undefined,
  planQuality: 'partial',
  status: 'active',
  expiresAt: null,
  createdAt: '2026-06-17T08:00:00',
  updatedAt: '2026-06-17T08:00:00',
  metadata: undefined,
};

const nextSignal: DecisionSignalItem = {
  ...signal,
  id: 22,
  stockCode: 'AAPL',
  stockName: 'Apple',
  market: 'us',
  reason: '第二条信号理由',
  riskSummary: '等待财报确认',
};

const outcome: DecisionSignalOutcomeItem = {
  id: 120,
  signalId: 21,
  horizon: '5d',
  engineVersion: 'decision-signal-v1',
  evalStatus: 'completed',
  outcome: 'hit',
  directionExpected: 'not_down',
  directionCorrect: true,
  holdingState: 'holding',
};

const nextOutcome: DecisionSignalOutcomeItem = {
  ...outcome,
  id: 121,
  signalId: 22,
  outcome: 'neutral',
};

const feedback: DecisionSignalFeedbackItem = {
  signalId: 21,
  feedbackValue: 'useful',
  reasonCode: null,
  note: null,
  source: 'web',
};

const emptyFeedback: DecisionSignalFeedbackItem = {
  signalId: 21,
  feedbackValue: null,
  reasonCode: null,
  note: null,
  source: null,
};

function renderComponent(props: React.ComponentProps<typeof ReportDecisionSignals>) {
  return render(
    <UiLanguageProvider>
      <ReportDecisionSignals {...props} />
    </UiLanguageProvider>,
  );
}

function deferredPromise<T>() {
  let resolve!: (value: T) => void;
  const promise = new Promise<T>((res) => {
    resolve = res;
  });
  return { promise, resolve };
}

beforeEach(() => {
  window.localStorage.clear();
  window.localStorage.setItem('dsa.uiLanguage', 'zh');
  vi.clearAllMocks();
  vi.mocked(decisionSignalsApi.list).mockResolvedValue({
    items: [signal],
    total: 1,
    page: 1,
    pageSize: 20,
  });
  vi.mocked(decisionSignalsApi.getSignalOutcomes).mockResolvedValue({
    items: [outcome],
    total: 1,
    page: 1,
    pageSize: 20,
  });
  vi.mocked(decisionSignalsApi.getFeedback).mockResolvedValue(feedback);
});

describe('ReportDecisionSignals', () => {
  it('loads and renders analysis-bound signals for a report record', async () => {
    renderComponent({ recordId: 5, reportType: 'detailed' });

    expect(await screen.findByText('腾讯控股')).toBeInTheDocument();
    expect(screen.getByText('缺少成交量确认')).toBeInTheDocument();
    expect(screen.getByText('5 日')).toBeInTheDocument();
    expect(screen.getByText('计划质量: 部分')).toBeInTheDocument();
    expect(screen.getByText('阶段: 盘后')).toBeInTheDocument();
    expect(screen.queryByText('5d')).not.toBeInTheDocument();
    expect(screen.queryByText('postmarket')).not.toBeInTheDocument();
    expect(screen.queryByText('partial')).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: '查看 腾讯控股 AI 建议详情' }));
    expect(within(await screen.findByRole('dialog')).getByText('结构等待确认')).toBeInTheDocument();
    expect(await within(screen.getByRole('dialog')).findByText('命中')).toBeInTheDocument();
    expect(within(screen.getByRole('dialog')).getByText('有用')).toBeInTheDocument();
    expect(decisionSignalsApi.getSignalOutcomes).toHaveBeenCalledWith(21);
    expect(decisionSignalsApi.getFeedback).toHaveBeenCalledWith(21);
    expect(decisionSignalsApi.list).toHaveBeenCalledWith({
      sourceReportId: 5,
      sourceType: 'analysis',
      page: 1,
      pageSize: 20,
    });
  });

  it('does not show a previous signal sidecar while the next signal details are loading', async () => {
    const nextOutcomes = deferredPromise<{
      items: DecisionSignalOutcomeItem[];
      total: number;
      page: number;
      pageSize: number;
    }>();
    const nextFeedback = deferredPromise<DecisionSignalFeedbackItem>();
    vi.mocked(decisionSignalsApi.list).mockResolvedValueOnce({
      items: [signal, nextSignal],
      total: 2,
      page: 1,
      pageSize: 20,
    });
    vi.mocked(decisionSignalsApi.getSignalOutcomes).mockImplementation((signalId: number) => {
      if (signalId === 21) {
        return Promise.resolve({
          items: [outcome],
          total: 1,
          page: 1,
          pageSize: 20,
        });
      }
      return nextOutcomes.promise;
    });
    vi.mocked(decisionSignalsApi.getFeedback).mockImplementation((signalId: number) => {
      if (signalId === 21) return Promise.resolve(feedback);
      return nextFeedback.promise;
    });

    renderComponent({ recordId: 5, reportType: 'detailed' });

    fireEvent.click(await screen.findByRole('button', { name: '查看 腾讯控股 AI 建议详情' }));
    let dialog = await screen.findByRole('dialog');
    expect(await within(dialog).findByText('命中')).toBeInTheDocument();
    expect(within(dialog).getByText('有用')).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: '查看 Apple AI 建议详情' }));
    dialog = await screen.findByRole('dialog');

    expect(within(dialog).getByText('第二条信号理由')).toBeInTheDocument();
    expect(within(dialog).queryByText('命中')).not.toBeInTheDocument();
    expect(within(dialog).queryByText('有用')).not.toBeInTheDocument();
    expect(within(dialog).getAllByText(/正在加载/).length).toBeGreaterThanOrEqual(2);
  });

  it('keeps loaded sidecar data when selecting the current signal again', async () => {
    renderComponent({ recordId: 5, reportType: 'detailed' });

    fireEvent.click(await screen.findByRole('button', { name: '查看 腾讯控股 AI 建议详情' }));
    const dialog = await screen.findByRole('dialog');
    expect(await within(dialog).findByText('命中')).toBeInTheDocument();
    expect(within(dialog).getByText('有用')).toBeInTheDocument();
    expect(decisionSignalsApi.getSignalOutcomes).toHaveBeenCalledTimes(1);
    expect(decisionSignalsApi.getFeedback).toHaveBeenCalledTimes(1);

    fireEvent.click(screen.getByRole('button', { name: '查看 腾讯控股 AI 建议详情' }));

    expect(within(dialog).getByText('命中')).toBeInTheDocument();
    expect(within(dialog).getByText('有用')).toBeInTheDocument();
    expect(within(dialog).queryByText(/正在加载/)).not.toBeInTheDocument();
    expect(decisionSignalsApi.getSignalOutcomes).toHaveBeenCalledTimes(1);
    expect(decisionSignalsApi.getFeedback).toHaveBeenCalledTimes(1);
  });

  it('ignores stale sidecar responses after selecting another report signal', async () => {
    const firstOutcomes = deferredPromise<{
      items: DecisionSignalOutcomeItem[];
      total: number;
      page: number;
      pageSize: number;
    }>();
    const firstFeedback = deferredPromise<DecisionSignalFeedbackItem>();
    vi.mocked(decisionSignalsApi.list).mockResolvedValueOnce({
      items: [signal, nextSignal],
      total: 2,
      page: 1,
      pageSize: 20,
    });
    vi.mocked(decisionSignalsApi.getSignalOutcomes).mockImplementation((signalId: number) => {
      if (signalId === 21) return firstOutcomes.promise;
      return Promise.resolve({
        items: [nextOutcome],
        total: 1,
        page: 1,
        pageSize: 20,
      });
    });
    vi.mocked(decisionSignalsApi.getFeedback).mockImplementation((signalId: number) => {
      if (signalId === 21) return firstFeedback.promise;
      return Promise.resolve({
        ...emptyFeedback,
        signalId: 22,
      });
    });

    renderComponent({ recordId: 5, reportType: 'detailed' });

    fireEvent.click(await screen.findByRole('button', { name: '查看 腾讯控股 AI 建议详情' }));
    fireEvent.click(screen.getByRole('button', { name: '查看 Apple AI 建议详情' }));
    const dialog = await screen.findByRole('dialog');
    expect(await within(dialog).findByText('第二条信号理由')).toBeInTheDocument();
    expect(await within(dialog).findByText('中性')).toBeInTheDocument();

    await act(async () => {
      firstOutcomes.resolve({
        items: [outcome],
        total: 1,
        page: 1,
        pageSize: 20,
      });
      firstFeedback.resolve(feedback);
      await Promise.all([firstOutcomes.promise, firstFeedback.promise]);
    });

    expect(within(dialog).queryByText('命中')).not.toBeInTheDocument();
    expect(within(dialog).queryByText('有用')).not.toBeInTheDocument();
    expect(within(dialog).getByText('暂无反馈')).toBeInTheDocument();
  });

  it('shows independent sidecar error and empty feedback states', async () => {
    vi.mocked(decisionSignalsApi.getSignalOutcomes).mockRejectedValueOnce(new Error('outcomes down'));
    vi.mocked(decisionSignalsApi.getFeedback).mockResolvedValueOnce(emptyFeedback);

    renderComponent({ recordId: 5, reportType: 'detailed' });

    fireEvent.click(await screen.findByRole('button', { name: '查看 腾讯控股 AI 建议详情' }));
    const dialog = await screen.findByRole('dialog');

    expect(await within(dialog).findByText('outcomes down')).toBeInTheDocument();
    expect(within(dialog).getByText('暂无反馈')).toBeInTheDocument();
  });

  it('shows an empty state when the report has no extracted signals', async () => {
    vi.mocked(decisionSignalsApi.list).mockResolvedValueOnce({
      items: [],
      total: 0,
      page: 1,
      pageSize: 20,
    });

    renderComponent({ recordId: 5, reportType: 'detailed' });

    expect(await screen.findByText('本报告暂无决策信号')).toBeInTheDocument();
  });

  it('clears previous report signals while loading another report', async () => {
    const secondLoad = deferredPromise<{
      items: DecisionSignalItem[];
      total: number;
      page: number;
      pageSize: number;
    }>();
    vi.mocked(decisionSignalsApi.list)
      .mockResolvedValueOnce({
        items: [signal],
        total: 1,
        page: 1,
        pageSize: 20,
      })
      .mockReturnValueOnce(secondLoad.promise);

    const { rerender } = render(
      <UiLanguageProvider>
        <ReportDecisionSignals recordId={5} reportType="detailed" />
      </UiLanguageProvider>,
    );

    expect(await screen.findByText('腾讯控股')).toBeInTheDocument();

    rerender(
      <UiLanguageProvider>
        <ReportDecisionSignals recordId={6} reportType="detailed" />
      </UiLanguageProvider>,
    );

    await waitFor(() => {
      expect(decisionSignalsApi.list).toHaveBeenLastCalledWith({
        sourceReportId: 6,
        sourceType: 'analysis',
        page: 1,
        pageSize: 20,
      });
    });
    expect(screen.queryByText('腾讯控股')).not.toBeInTheDocument();

    secondLoad.resolve({
      items: [],
      total: 0,
      page: 1,
      pageSize: 20,
    });
    expect(await screen.findByText('本报告暂无决策信号')).toBeInTheDocument();
  });

  it('shows an error state when loading report signals fails', async () => {
    vi.mocked(decisionSignalsApi.list).mockRejectedValueOnce(new Error('network down'));

    renderComponent({ recordId: 5, reportType: 'detailed' });

    const alert = await screen.findByRole('alert');
    expect(alert).toHaveTextContent('报告信号加载失败');
    expect(alert).toHaveTextContent('network down');
  });

  it('does not render or request without a record id', () => {
    const { container } = renderComponent({ reportType: 'detailed' });

    expect(container).toBeEmptyDOMElement();
    expect(decisionSignalsApi.list).not.toHaveBeenCalled();
  });

  it('does not render or request for market review reports', async () => {
    const { container } = renderComponent({ recordId: 5, reportType: 'market_review' });

    await waitFor(() => expect(decisionSignalsApi.list).not.toHaveBeenCalled());
    expect(container).toBeEmptyDOMElement();
  });
});
