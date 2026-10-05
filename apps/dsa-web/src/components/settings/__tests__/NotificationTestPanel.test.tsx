import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import type { ReactNode } from 'react';
import { useUiLanguage, UiLanguageProvider } from '../../../contexts/UiLanguageContext';
import { UI_LANGUAGE_STORAGE_KEY } from '../../../utils/uiLanguage';
import { NotificationTestPanel } from '../NotificationTestPanel';

const testNotificationChannel = vi.hoisted(() => vi.fn());

vi.mock('../../../api/systemConfig', () => ({
  systemConfigApi: { testNotificationChannel },
}));

const items = [{ key: 'EMAIL_SENDER', value: 'sender@example.com' }];

const SwitchHarness = ({ children }: { children: ReactNode }) => {
  const { setLanguage } = useUiLanguage();
  return (
    <div>
      <button type="button" onClick={() => setLanguage('en')}>switch-en</button>
      {children}
    </div>
  );
};

describe('NotificationTestPanel', () => {
  beforeEach(() => {
    localStorage.setItem(UI_LANGUAGE_STORAGE_KEY, 'zh');
    testNotificationChannel.mockReset();
    testNotificationChannel.mockResolvedValue({
      success: true,
      message: 'ok',
      errorCode: null,
      stage: 'notification_send',
      retryable: false,
      latencyMs: 12,
      attempts: [{
        channel: 'email',
        success: true,
        message: 'sent',
        target: 's***@example.com',
        errorCode: null,
        stage: 'notification_send',
        retryable: false,
        latencyMs: 12,
        httpStatus: null,
      }],
    });
  });

  it('offers only email and submits draft email settings', async () => {
    render(<NotificationTestPanel items={items} maskToken="******" />);

    const channelInput = screen.getByLabelText('渠道');
    expect(channelInput).toHaveValue('邮件');
    expect(channelInput).toHaveAttribute('readonly');
    expect(screen.queryByRole('combobox')).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: /发送测试/ }));
    await waitFor(() => expect(testNotificationChannel).toHaveBeenCalledWith(expect.objectContaining({
      channel: 'email',
      items,
      maskToken: '******',
      timeoutSeconds: 20,
    })));
    expect(await screen.findByText('测试成功')).toBeInTheDocument();
    expect(screen.getByText('s***@example.com')).toBeInTheDocument();
  });

  it('uses translated defaults after a language change', async () => {
    render(
      <UiLanguageProvider>
        <SwitchHarness>
          <NotificationTestPanel items={items} maskToken="******" />
        </SwitchHarness>
      </UiLanguageProvider>,
    );

    const titleInput = screen.getByLabelText('标题');
    const contentInput = screen.getByLabelText('正文');
    expect(titleInput).toHaveValue('DSA 通知测试');
    fireEvent.click(screen.getByRole('button', { name: 'switch-en' }));

    await waitFor(() => {
      expect(titleInput).toHaveValue('DSA notification test');
      expect(contentInput).toHaveValue('This is a test notification from the DSA Web settings page.');
    });
    expect(screen.getByLabelText('Channel')).toHaveValue('Email');
    fireEvent.click(screen.getByRole('button', { name: /Send test/ }));
    await waitFor(() => expect(testNotificationChannel).toHaveBeenCalledWith(expect.objectContaining({
      channel: 'email',
      title: 'DSA notification test',
      content: 'This is a test notification from the DSA Web settings page.',
    })));
  });

  it('preserves user-edited values when language switches', () => {
    render(
      <UiLanguageProvider>
        <SwitchHarness>
          <NotificationTestPanel items={items} maskToken="******" />
        </SwitchHarness>
      </UiLanguageProvider>,
    );

    const titleInput = screen.getByLabelText('标题');
    const contentInput = screen.getByLabelText('正文');
    fireEvent.change(titleInput, { target: { value: '自定义标题' } });
    fireEvent.change(contentInput, { target: { value: '自定义正文' } });
    fireEvent.click(screen.getByRole('button', { name: 'switch-en' }));
    expect(titleInput).toHaveValue('自定义标题');
    expect(contentInput).toHaveValue('自定义正文');
  });

  it('renders retryable email timeout diagnostics', async () => {
    testNotificationChannel.mockResolvedValueOnce({
      success: false,
      message: 'Email send timed out',
      errorCode: 'timeout',
      stage: 'notification_send',
      retryable: true,
      latencyMs: null,
      attempts: [{
        channel: 'email',
        success: false,
        message: 'timeout',
        target: 's***@example.com',
        errorCode: 'timeout',
        stage: 'notification_send',
        retryable: true,
        latencyMs: null,
        httpStatus: null,
      }],
    });
    render(<NotificationTestPanel items={items} maskToken="******" />);
    fireEvent.click(screen.getByRole('button', { name: /发送测试/ }));
    expect(await screen.findByText('测试失败')).toBeInTheDocument();
    expect(screen.getAllByText('timeout').length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText('s***@example.com')).toBeInTheDocument();
  });

  it('does not allow sending while disabled', () => {
    render(<NotificationTestPanel items={items} maskToken="******" disabled />);
    expect(screen.getByRole('button', { name: /发送测试/ })).toBeDisabled();
    expect(testNotificationChannel).not.toHaveBeenCalled();
  });
});
