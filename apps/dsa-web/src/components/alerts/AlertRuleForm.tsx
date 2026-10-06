import type React from 'react';
import { useState } from 'react';
import type { AlertDirection, AlertRuleCreateRequest, AlertSeverity, AlertTargetScope } from '../../types/alerts';
import { useUiLanguage } from '../../contexts/UiLanguageContext';
import { formatUiText } from '../../i18n/uiText';
import {
  ALERT_CHANGE_DIRECTION_OPTIONS,
  ALERT_FORM_TEXT,
  ALERT_SEVERITY_OPTIONS,
  ALERT_TARGET_SCOPE_OPTIONS,
  ALERT_TYPE_LABELS,
} from '../../locales/featureText';
import { validateStockCode } from '../../utils/validation';
import { Button, Card, Checkbox, Input, Select } from '../common';

interface AlertRuleFormProps {
  onSubmit: (payload: AlertRuleCreateRequest) => Promise<boolean | void> | boolean | void;
  isSubmitting?: boolean;
}

export const AlertRuleForm: React.FC<AlertRuleFormProps> = ({ onSubmit, isSubmitting = false }) => {
  const { language } = useUiLanguage();
  const text = ALERT_FORM_TEXT[language];
  const [name, setName] = useState('');
  const [targetScope, setTargetScope] = useState<AlertTargetScope>('single_symbol');
  const [target, setTarget] = useState('');
  const [severity, setSeverity] = useState<AlertSeverity>('warning');
  const [enabled, setEnabled] = useState(true);
  const [changeDirection, setChangeDirection] = useState<AlertDirection>('up');
  const [changePct, setChangePct] = useState('');
  const [formError, setFormError] = useState<string | null>(null);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    let resolvedTarget = 'default';
    if (targetScope === 'single_symbol') {
      const validation = validateStockCode(target);
      if (!validation.valid) {
        setFormError(language === 'en' ? text.invalidStockCode : (validation.message ?? text.invalidStockCode));
        return;
      }
      resolvedTarget = validation.normalized;
    }
    const parsedChangePct = Number(changePct);
    if (!Number.isFinite(parsedChangePct) || parsedChangePct <= 0) {
      setFormError(formatUiText(text.positiveNumber, { label: text.changePctThreshold }));
      return;
    }
    setFormError(null);
    const submitted = await onSubmit({
      name: name.trim() || undefined,
      targetScope,
      target: resolvedTarget,
      alertType: 'price_change_percent',
      parameters: { direction: changeDirection, changePct: parsedChangePct },
      severity,
      enabled,
    });
    if (submitted === false) return;
    setName('');
    setTarget('');
    setChangePct('');
    setChangeDirection('up');
    setEnabled(true);
  };

  return (
    <Card title={text.cardTitle} subtitle={text.cardSubtitle} variant="bordered" padding="md">
      <form className="space-y-4" noValidate onSubmit={(event) => void handleSubmit(event)}>
        <div className="grid gap-4 md:grid-cols-2">
          <Input
            label={text.ruleName}
            value={name}
            onChange={(event) => setName(event.target.value)}
            placeholder={text.ruleNamePlaceholder}
            disabled={isSubmitting}
          />
          <Select
            label={text.targetScope}
            value={targetScope}
            options={ALERT_TARGET_SCOPE_OPTIONS[language]}
            disabled={isSubmitting}
            onChange={(value) => {
              if (value !== 'single_symbol' && value !== 'watchlist') return;
              setTargetScope(value);
              setChangeDirection('up');
              setChangePct('');
              setFormError(null);
            }}
          />
          {targetScope === 'single_symbol' ? (
            <Input
              label={text.targetCode}
              value={target}
              onChange={(event) => setTarget(event.target.value)}
              placeholder="600519 / AAPL / hk00700"
              disabled={isSubmitting}
            />
          ) : (
            <Input label={text.target} value="default" disabled />
          )}
          <Input label={text.ruleType} value={ALERT_TYPE_LABELS[language].price_change_percent} readOnly />
          <Select
            label={text.severity}
            value={severity}
            options={ALERT_SEVERITY_OPTIONS[language]}
            disabled={isSubmitting}
            onChange={(value) => {
              if (value === 'info' || value === 'warning' || value === 'critical') setSeverity(value);
            }}
          />
        </div>
        <div className="grid gap-4 md:grid-cols-2">
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
        </div>
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <Checkbox
            label={text.enableAfterCreate}
            checked={enabled}
            onChange={(event) => setEnabled(event.target.checked)}
            disabled={isSubmitting}
          />
          <Button type="submit" isLoading={isSubmitting} loadingText={text.creating}>{text.create}</Button>
        </div>
        {formError ? <p role="alert" className="text-sm text-danger">{formError}</p> : null}
      </form>
    </Card>
  );
};
