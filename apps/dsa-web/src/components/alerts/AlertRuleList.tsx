import type React from 'react';
import { useState } from 'react';
import { Bell, Trash2 } from 'lucide-react';
import { Badge, Button, Card, ConfirmDialog, EmptyState, Pagination, Select } from '../common';
import { useUiLanguage } from '../../contexts/UiLanguageContext';
import { formatUiText } from '../../i18n/uiText';
import {
  ALERT_ENABLED_FILTER_OPTIONS,
  ALERT_LIST_TEXT,
  ALERT_SEVERITY_LABELS,
  ALERT_TYPE_FILTER_OPTIONS,
  ALERT_TYPE_LABELS,
} from '../../locales/featureText';
import type { AlertRuleItem, AlertType } from '../../types/alerts';
import { formatDateTime } from '../../utils/format';

export type AlertRuleEnabledFilter = 'all' | 'enabled' | 'disabled';
export type AlertTypeFilter = 'all' | AlertType;
export type AlertRuleBusyAction = 'test' | 'toggle' | 'delete';

export interface AlertRuleBusyState {
  id: number;
  action: AlertRuleBusyAction;
}

interface AlertRuleListProps {
  rules: AlertRuleItem[];
  total: number;
  page: number;
  pageSize: number;
  className?: string;
  isLoading?: boolean;
  enabledFilter: AlertRuleEnabledFilter;
  alertTypeFilter: AlertTypeFilter;
  onEnabledFilterChange: (value: AlertRuleEnabledFilter) => void;
  onAlertTypeFilterChange: (value: AlertTypeFilter) => void;
  onPageChange: (page: number) => void;
  onToggleEnabled: (rule: AlertRuleItem) => void;
  onDelete: (rule: AlertRuleItem) => void;
  onTest: (rule: AlertRuleItem) => void;
  busyRule?: AlertRuleBusyState | null;
}

export const AlertRuleList: React.FC<AlertRuleListProps> = ({
  rules,
  total,
  page,
  pageSize,
  className,
  isLoading = false,
  enabledFilter,
  alertTypeFilter,
  onEnabledFilterChange,
  onAlertTypeFilterChange,
  onPageChange,
  onToggleEnabled,
  onDelete,
  onTest,
  busyRule = null,
}) => {
  const { language } = useUiLanguage();
  const text = ALERT_LIST_TEXT[language];
  const [pendingDelete, setPendingDelete] = useState<AlertRuleItem | null>(null);
  const totalPages = Math.max(1, Math.ceil(total / pageSize));
  const isRuleBusy = (rule: AlertRuleItem) => busyRule?.id === rule.id;
  const isRuleActionBusy = (rule: AlertRuleItem, action: AlertRuleBusyAction) => (
    busyRule?.id === rule.id && busyRule.action === action
  );

  return (
    <Card
      title={text.title}
      variant="bordered"
      padding="md"
      className={className}
    >
      <div className="mb-4 grid gap-3 md:grid-cols-2">
        <Select
          label={text.enabledFilter}
          value={enabledFilter}
          options={ALERT_ENABLED_FILTER_OPTIONS[language]}
          onChange={(value) => {
            onEnabledFilterChange(value as AlertRuleEnabledFilter);
          }}
        />
        <Select
          label={text.alertTypeFilter}
          value={alertTypeFilter}
          options={ALERT_TYPE_FILTER_OPTIONS[language]}
          onChange={(value) => {
            if (value === 'all' || value === 'price_change_percent') onAlertTypeFilterChange(value);
          }}
        />
      </div>

      {rules.length === 0 ? (
        <div className="flex min-h-[220px] flex-1 items-center justify-center">
          <EmptyState
            icon={<Bell className="h-6 w-6" />}
            title={isLoading ? text.loadingRules : text.emptyTitle}
            description={text.emptyDescription}
          />
        </div>
      ) : (
        <div className="min-h-0 flex-1 overflow-x-auto">
          <table className="w-full min-w-[820px] text-left text-sm">
            <thead className="border-b border-border/60 text-xs uppercase text-muted-text">
              <tr>
                <th className="px-3 py-2 font-medium">{text.rule}</th>
                <th className="px-3 py-2 font-medium">{text.type}</th>
                <th className="px-3 py-2 font-medium">{text.severity}</th>
                <th className="px-3 py-2 font-medium">{text.status}</th>
                <th className="px-3 py-2 font-medium">{text.updatedAt}</th>
                <th className="px-3 py-2 text-right font-medium">{text.action}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/40">
              {rules.map((rule) => (
                <tr key={rule.id} className="align-top">
                  <td className="px-3 py-3">
                    <div className="font-medium text-foreground">{rule.name}</div>
                  </td>
                  <td className="px-3 py-3">
                    <Badge variant="info">{ALERT_TYPE_LABELS[language][rule.alertType] ?? rule.alertType}</Badge>
                  </td>
                  <td className="px-3 py-3">
                    <Badge variant={rule.severity === 'critical' ? 'danger' : rule.severity === 'warning' ? 'warning' : 'default'}>
                      {ALERT_SEVERITY_LABELS[language][rule.severity] ?? rule.severity}
                    </Badge>
                  </td>
                  <td className="px-3 py-3">
                    <Badge variant={rule.enabled ? 'success' : 'default'}>
                      {rule.enabled ? text.enabled : text.disabled}
                    </Badge>
                  </td>
                  <td className="px-3 py-3 text-xs text-secondary-text">{formatDateTime(rule.updatedAt ?? rule.createdAt)}</td>
                  <td className="px-3 py-3">
                    <div className="flex justify-end gap-2">
                      <Button
                        size="xsm"
                        variant="outline"
                        onClick={() => onTest(rule)}
                        isLoading={isRuleActionBusy(rule, 'test')}
                        loadingText={text.testing}
                        disabled={isRuleBusy(rule) && !isRuleActionBusy(rule, 'test')}
                      >
                        {text.test}
                      </Button>
                      <Button
                        size="xsm"
                        variant={rule.enabled ? 'secondary' : 'primary'}
                        onClick={() => onToggleEnabled(rule)}
                        isLoading={isRuleActionBusy(rule, 'toggle')}
                        loadingText={rule.enabled ? text.disabling : text.enabling}
                        disabled={isRuleBusy(rule) && !isRuleActionBusy(rule, 'toggle')}
                      >
                        {rule.enabled ? text.disable : text.enable}
                      </Button>
                      <Button
                        size="xsm"
                        variant="danger-subtle"
                        aria-label={formatUiText(text.deleteAria, { name: rule.name })}
                        onClick={() => setPendingDelete(rule)}
                        disabled={isRuleBusy(rule)}
                      >
                        <Trash2 className="h-3.5 w-3.5" />
                        {text.delete}
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <Pagination
        currentPage={page}
        totalPages={totalPages}
        onPageChange={onPageChange}
        className="mt-5"
      />

      <ConfirmDialog
        isOpen={pendingDelete != null}
        title={text.deleteTitle}
        message={pendingDelete ? formatUiText(text.deleteMessage, { name: pendingDelete.name }) : ''}
        confirmText={text.delete}
        cancelText={text.cancel}
        isDanger
        onConfirm={() => {
          if (pendingDelete) {
            onDelete(pendingDelete);
          }
          setPendingDelete(null);
        }}
        onCancel={() => setPendingDelete(null)}
      />
    </Card>
  );
};
