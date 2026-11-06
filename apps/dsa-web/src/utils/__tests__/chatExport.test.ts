import { afterEach, describe, expect, it, vi } from 'vitest';
import { downloadSession, formatSessionAsMarkdown } from '../chatExport';
import { buildFollowUpPrompt } from '../chatFollowUp';
import type { Message } from '../../stores/agentChatStore';

const messages: Message[] = [
  { id: 'user-1', role: 'user', content: '请分析茅台' },
  { id: 'assistant-1', role: 'assistant', content: '原始中文分析', skillName: '默认多头趋势、缠论' },
];

afterEach(() => {
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
});

describe('chat export localization', () => {
  it('uses English headings while preserving the original message bodies', () => {
    const output = formatSessionAsMarkdown(messages, 'en');
    expect(output).toContain('# Ask conversation');
    expect(output).toContain('Generated at:');
    expect(output).toContain('## User');
    expect(output).toContain('## AI (Default bullish trend, Chan theory)');
    expect(output).toContain('请分析茅台');
    expect(output).toContain('原始中文分析');
  });

  it('keeps Chinese as the default for existing callers', () => {
    const output = formatSessionAsMarkdown(messages);
    expect(output).toContain('# 问股会话');
    expect(output).toContain('生成时间:');
    expect(output).toContain('## 用户');
    expect(output).toContain('## AI (默认多头趋势、缠论)');
  });

  it('downloads using a localized filename and revokes the object URL', () => {
    const createObjectURL = vi.fn().mockReturnValue('blob:chat-export');
    const revokeObjectURL = vi.fn();
    vi.stubGlobal('URL', { createObjectURL, revokeObjectURL });
    let filename = '';
    vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(function (this: HTMLAnchorElement) {
      filename = this.download;
    });
    downloadSession(messages, 'en');
    expect(filename).toMatch(/^ask-conversation_\d{8}_\d{4}\.md$/);
    expect(createObjectURL).toHaveBeenCalledWith(expect.any(Blob));
    expect(revokeObjectURL).toHaveBeenCalledWith('blob:chat-export');
    expect(document.querySelector('a[download]')).toBeNull();
  });

  it('localizes generated follow-up prompts without changing stock identity', () => {
    expect(buildFollowUpPrompt('AAPL', 'Apple', 'en')).toBe('Please analyze Apple(AAPL) in depth');
    expect(buildFollowUpPrompt('AAPL', null, 'en')).toBe('Please analyze AAPL in depth');
    expect(buildFollowUpPrompt('600519', '茅台')).toBe('请深入分析 茅台(600519)');
  });
});
