import type React from 'react';
import { useCallback, useEffect, useRef, useState } from 'react';
import { Activity } from 'lucide-react';
import { decisionSignalsApi } from '../../api/decisionSignals';
import { getParsedApiError, type ParsedApiError } from '../../api/error';
import { ApiErrorAlert, Card, Drawer, EmptyState } from '../common';
import {
  DecisionSignalCard,
  DecisionSignalDetails,
} from '../decision-signals/DecisionSignalDisplay';
import { useUiLanguage } from '../../contexts/UiLanguageContext';
import type { ReportType } from '../../types/analysis';
import type {
  DecisionSignalFeedbackItem,
  DecisionSignalItem,
  DecisionSignalOutcomeItem,
} from '../../types/decisionSignals';

interface ReportDecisionSignalsProps {
  recordId?: number;
  reportType?: ReportType;
}

type DetailSidecarState = {
  signalId: number | null;
  outcomes: {
    items: DecisionSignalOutcomeItem[];
    loading: boolean;
    error: ParsedApiError | null;
  };
  feedback: {
    item: DecisionSignalFeedbackItem | null;
    loading: boolean;
    error: ParsedApiError | null;
  };
};

function createDetailSidecarState(signalId: number | null = null, loading = false): DetailSidecarState {
  return {
    signalId,
    outcomes: {
      items: [],
      loading,
      error: null,
    },
    feedback: {
      item: null,
      loading,
      error: null,
    },
  };
}

export const ReportDecisionSignals: React.FC<ReportDecisionSignalsProps> = ({
  recordId,
  reportType,
}) => {
  const { t } = useUiLanguage();
  const [items, setItems] = useState<DecisionSignalItem[]>([]);
  const [selected, setSelected] = useState<DecisionSignalItem | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<ParsedApiError | null>(null);
  const [detailSidecar, setDetailSidecar] = useState<DetailSidecarState>(() => createDetailSidecarState());
  const requestIdRef = useRef(0);
  const detailRequestIdRef = useRef(0);
  const shouldRender = Boolean(recordId) && reportType !== 'market_review';

  const loadSignals = useCallback(async () => {
    if (!recordId || reportType === 'market_review') return;
    const requestId = requestIdRef.current + 1;
    requestIdRef.current = requestId;
    setLoading(true);
    setItems([]);
    setSelected(null);
    detailRequestIdRef.current += 1;
    setDetailSidecar(createDetailSidecarState());
    setError(null);
    try {
      const response = await decisionSignalsApi.list({
        sourceReportId: recordId,
        sourceType: 'analysis',
        page: 1,
        pageSize: 20,
      });
      if (requestIdRef.current !== requestId) return;
      setItems(response.items);
      setError(null);
    } catch (err) {
      if (requestIdRef.current !== requestId) return;
      setError(getParsedApiError(err));
      setItems([]);
    } finally {
      if (requestIdRef.current === requestId) {
        setLoading(false);
      }
    }
  }, [recordId, reportType]);

  useEffect(() => {
    if (!shouldRender) {
      requestIdRef.current += 1;
      setLoading(false);
      setItems([]);
      setSelected(null);
      detailRequestIdRef.current += 1;
      setDetailSidecar(createDetailSidecarState());
      setError(null);
      return;
    }
    void loadSignals();
    return () => {
      requestIdRef.current += 1;
    };
  }, [loadSignals, shouldRender]);

  useEffect(() => {
    if (!selected) {
      detailRequestIdRef.current += 1;
      setDetailSidecar(createDetailSidecarState());
      return;
    }

    const signalId = selected.id;
    const requestId = detailRequestIdRef.current + 1;
    detailRequestIdRef.current = requestId;
    setDetailSidecar(createDetailSidecarState(signalId, true));

    void decisionSignalsApi.getSignalOutcomes(signalId)
      .then((response) => {
        if (detailRequestIdRef.current !== requestId) return;
        setDetailSidecar((current) => (
          current.signalId === signalId
            ? {
              ...current,
              outcomes: {
                items: response.items,
                loading: false,
                error: null,
              },
            }
            : current
        ));
      })
      .catch((err) => {
        if (detailRequestIdRef.current !== requestId) return;
        const parsed = getParsedApiError(err);
        setDetailSidecar((current) => (
          current.signalId === signalId
            ? {
              ...current,
              outcomes: {
                items: [],
                loading: false,
                error: parsed,
              },
            }
            : current
        ));
      });

    void decisionSignalsApi.getFeedback(signalId)
      .then((response) => {
        if (detailRequestIdRef.current !== requestId) return;
        setDetailSidecar((current) => (
          current.signalId === signalId
            ? {
              ...current,
              feedback: {
                item: response,
                loading: false,
                error: null,
              },
            }
            : current
        ));
      })
      .catch((err) => {
        if (detailRequestIdRef.current !== requestId) return;
        const parsed = getParsedApiError(err);
        setDetailSidecar((current) => (
          current.signalId === signalId
            ? {
              ...current,
              feedback: {
                item: null,
                loading: false,
                error: parsed,
              },
            }
            : current
        ));
      });
  }, [selected]);

  const handleSelectSignal = useCallback((item: DecisionSignalItem) => {
    if (selected?.id === item.id) return;
    detailRequestIdRef.current += 1;
    setSelected(item);
    setDetailSidecar(createDetailSidecarState(item.id, true));
  }, [selected?.id]);

  const handleCloseDetails = useCallback(() => {
    detailRequestIdRef.current += 1;
    setSelected(null);
    setDetailSidecar(createDetailSidecarState());
  }, []);

  if (!shouldRender) {
    return null;
  }

  const sidecarMatches = selected !== null && detailSidecar.signalId === selected.id;
  const detailOutcomes = sidecarMatches
    ? detailSidecar.outcomes
    : { items: [], loading: Boolean(selected), error: null };
  const detailFeedback = sidecarMatches
    ? detailSidecar.feedback
    : { item: null, loading: Boolean(selected), error: null };

  return (
    <>
      <Card
        title={t('decisionSignals.reportSectionTitle')}
        subtitle={t('decisionSignals.reportSectionDescription')}
        padding="md"
      >
        {error ? (
          <ApiErrorAlert
            error={{ ...error, title: t('decisionSignals.reportErrorTitle') }}
            actionLabel={t('common.retry')}
            onAction={() => void loadSignals()}
          />
        ) : null}
        {loading && items.length === 0 ? (
          <div className="grid gap-3">
            <div className="h-24 animate-pulse rounded-2xl border border-border/70 bg-card/60" />
            <div className="h-24 animate-pulse rounded-2xl border border-border/70 bg-card/60" />
          </div>
        ) : null}
        {!loading && !error && items.length === 0 ? (
          <EmptyState
            className="border-none bg-transparent py-6 shadow-none"
            title={t('decisionSignals.reportEmptyTitle')}
            description={t('decisionSignals.reportEmptyDescription')}
            icon={<Activity className="h-6 w-6" />}
          />
        ) : null}
        {items.length > 0 ? (
          <div className="grid gap-3 lg:grid-cols-2">
            {items.map((item) => (
              <DecisionSignalCard
                key={item.id}
                item={item}
                onSelect={handleSelectSignal}
                selected={selected?.id === item.id}
              />
            ))}
          </div>
        ) : null}
      </Card>

      <Drawer
        isOpen={Boolean(selected)}
        onClose={handleCloseDetails}
        title={t('decisionSignals.detailTitle')}
        width="max-w-3xl"
      >
        {selected ? (
          <DecisionSignalDetails
            item={selected}
            outcomes={detailOutcomes.items}
            outcomesLoading={detailOutcomes.loading}
            outcomesError={detailOutcomes.error?.message ?? null}
            feedback={detailFeedback.item}
            feedbackLoading={detailFeedback.loading}
            feedbackError={detailFeedback.error?.message ?? null}
          />
        ) : null}
      </Drawer>
    </>
  );
};
