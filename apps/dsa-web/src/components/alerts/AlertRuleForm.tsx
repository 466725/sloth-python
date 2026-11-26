import type React from 'react';
import { useEffect, useState } from 'react';
import { getParsedApiError, type ParsedApiError } from '../../api/error';
import { systemConfigApi } from '../../api/systemConfig';
import type { AlertDirection, AlertRuleCreateRequest, AlertSeverity } from '../../types/alerts';
import { useUiLanguage } from '../../contexts/UiLanguageContext';
import { formatUiText } from '../../i18n/uiText';
import {
  ALERT_CHANGE_DIRECTION_OPTIONS,
  ALERT_FORM_TEXT,
  ALERT_SCOPE_LABELS,
  ALERT_SEVERITY_OPTIONS,
  ALERT_TYPE_LABELS,
} from '../../locales/featureText';
import { validateStockCode } from '../../utils/validation';
import { ApiErrorAlert, Button, Card, Checkbox, Input, Select } from '../common';

interface AlertRuleFormProps {
  onSubmit: (payload: AlertRuleCreateRequest) => Promise<boolean | void> | boolean | void;
  isSubmitting?: boolean;
}

export const AlertRuleForm: React.FC<AlertRuleFormProps> = ({ onSubmit, isSubmitting = false }) => {
  const { language } = useUiLanguage();
  const text = ALERT_FORM_TEXT[language];
  const [target, setTarget] = useState('');
  const [stockCodes, setStockCodes] = useState<string[]>([]);
  const [stockCodesLoading, setStockCodesLoading] = useState(true);
  const [stockCodesError, setStockCodesError] = useState<ParsedApiError | null>(null);
  const [severity, setSeverity] = useState<AlertSeverity>('warning');
  const [enabled, setEnabled] = useState(true);
  const [changeDirection, setChangeDirection] = useState<AlertDirection>('up');
  const [changePct, setChangePct] = useState('');
  const [formError, setFormError] = useState<
    { kind: 'stockCode'; message?: string } | { kind: 'threshold' } | null
  >(null);
  const formErrorMessage = formError?.kind === 'stockCode'
    ? language === 'en' ? text.invalidStockCode : formError.message ?? text.invalidStockCode
    : formError?.kind === 'threshold'
      ? formatUiText(text.positiveNumber, { label: text.changePctThreshold })
      : null;

  useEffect(() => {
    let cancelled = false;
    void systemConfigApi.getWatchlist()
      .then((codes) => {
        if (!cancelled) setStockCodes(codes);
      })
      .catch((error) => {
        if (!cancelled) setStockCodesError(getParsedApiError(error));
      })
      .finally(() => {
        if (!cancelled) setStockCodesLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const stockCodeOptions = Array.from(new Set(stockCodes))
    .map((stockCode) => ({ value: stockCode, label: stockCode }));

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const validation = validateStockCode(target);
    if (!validation.valid) {
      setFormError({ kind: 'stockCode', message: validation.message });
      return;
    }
    const parsedChangePct = Number(changePct);
    if (!Number.isFinite(parsedChangePct) || parsedChangePct <= 0) {
      setFormError({ kind: 'threshold' });
      return;
    }
    setFormError(null);
    const submitted = await onSubmit({
      targetScope: 'single_symbol',
      target: validation.normalized,
      alertType: 'price_change_percent',
      parameters: { direction: changeDirection, changePct: parsedChangePct },
      severity,
      enabled,
    });
    if (submitted === false) return;
    setTarget('');
    setChangePct('');
    setChangeDirection('up');
    setEnabled(true);
  };

  return (
    <Card title={text.cardTitle} subtitle={text.cardSubtitle} variant="bordered" padding="md">
      <form className="space-y-4" noValidate onSubmit={(event) => void handleSubmit(event)}>
        <div className="grid gap-4 md:grid-cols-2">
          <Select
            label={text.targetCode}
            value={target}
            options={stockCodeOptions}
            disabled={isSubmitting || stockCodesLoading || Boolean(stockCodesError) || stockCodes.length === 0}
            onChange={setTarget}
          />
          <Select
            label={text.severity}
            value={severity}
            options={ALERT_SEVERITY_OPTIONS[language]}
            disabled={isSubmitting}
            onChange={(value) => {
              if (value === 'info' || value === 'warning' || value === 'critical') setSeverity(value);
            }}
          />
          <Select
            label={text.direction}
            value={changeDirection}
            options={ALERT_CHANGE_DIRECTION_OPTIONS[language]}
            disabled={isSubmitting}
            onChange={(value) => {
              if (value === 'up' || value === 'down') setChangeDirection(value);
            }}
          />
          <Input
            label={text.changePctThreshold}
            type="number"
            min="0"
            step="0.01"
            value={changePct}
            onChange={(event) => setChangePct(event.target.value)}
            disabled={isSubmitting}
          />
          <Input label={text.targetScope} value={ALERT_SCOPE_LABELS[language].single_symbol} readOnly />
          <Input label={text.ruleType} value={ALERT_TYPE_LABELS[language].price_change_percent} readOnly />
        </div>
        {stockCodesLoading ? (
          <p role="status" className="text-sm text-secondary-text">{text.loadingStocks}</p>
        ) : null}
        {stockCodesError ? <ApiErrorAlert error={stockCodesError} /> : null}
        {!stockCodesLoading && !stockCodesError && stockCodes.length === 0 ? (
          <p role="status" className="text-sm text-secondary-text">{text.noStocksConfigured}</p>
        ) : null}
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <Checkbox
            label={text.enableAfterCreate}
            checked={enabled}
            onChange={(event) => setEnabled(event.target.checked)}
            disabled={isSubmitting}
          />
          <Button type="submit" isLoading={isSubmitting} loadingText={text.creating}>{text.create}</Button>
        </div>
        {formErrorMessage ? <p role="alert" className="text-sm text-danger">{formErrorMessage}</p> : null}
      </form>
    </Card>
  );
};
