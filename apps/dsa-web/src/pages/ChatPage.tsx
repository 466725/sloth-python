import React, { useState, useRef, useEffect, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import Markdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { ChevronDown, SlidersHorizontal } from 'lucide-react';
import { cn } from '../utils/cn';
import { agentApi } from '../api/agent';
import { systemConfigApi } from '../api/systemConfig';
import { ApiErrorAlert, Badge, Button, ConfirmDialog, EmptyState, InlineAlert, ScrollArea, Tooltip } from '../components/common';
import { getParsedApiError } from '../api/error';
import type { SkillInfo } from '../api/agent';
import { DashboardStateBlock } from '../components/dashboard';
import {
  useAgentChatStore,
  type Message,
  type ProgressStep,
} from '../stores/agentChatStore';
import { downloadSession, formatSessionAsMarkdown } from '../utils/chatExport';
import type { ChatFollowUpContext } from '../utils/chatFollowUp';
import {
  parseFollowUpRecordId,
  resolveChatFollowUpContext,
  sanitizeFollowUpStockCode,
  sanitizeFollowUpStockName,
} from '../utils/chatFollowUp';
import { isNearBottom } from '../utils/chatScroll';
import { useUiLanguage } from '../contexts/UiLanguageContext';
import { formatUiText, type UiLanguage } from '../i18n/uiText';
import { CHAT_TEXT, CHAT_QUICK_QUESTIONS, getChatSkillName, getChatSkillText } from '../locales/chatText';
import { areStockCodesEquivalent } from '../utils/stockCode';

type LocalizedFeedback = string | ((language: UiLanguage) => string);
const resolveFeedback = (feedback: LocalizedFeedback, language: UiLanguage) =>
  typeof feedback === 'function' ? feedback(language) : feedback;

type ActiveStockContext = Pick<ChatFollowUpContext, 'stock_code' | 'stock_name'>;

const getMessageSkillNames = (msg: Message): string[] => {
  if (msg.skillNames?.length) return msg.skillNames;
  if (msg.skillName) return [msg.skillName];
  if (msg.skills?.length) return msg.skills;
  if (msg.skill) return [msg.skill];
  return [];
};

const getMessageSkillLabel = (msg: Message, language: UiLanguage): string =>
  getMessageSkillNames(msg).flatMap((name) => name.split('、')).map((name) => getChatSkillName(name, language)).join(language === 'en' ? ', ' : '、');

const ChatPage: React.FC = () => {
  const { language } = useUiLanguage();
  const text = CHAT_TEXT[language];
  const [searchParams, setSearchParams] = useSearchParams();
  const [skills, setSkills] = useState<SkillInfo[]>([]);
  const [selectedSkillId, setSelectedSkillId] = useState('');
  const [skillsStatus, setSkillsStatus] = useState<'loading' | 'ready' | 'error' | 'empty'>('loading');
  const [skillsLoadAttempt, setSkillsLoadAttempt] = useState(0);
  const [stockCodes, setStockCodes] = useState<string[]>([]);
  const [selectedStockCode, setSelectedStockCode] = useState('');
  const [stocksStatus, setStocksStatus] = useState<'loading' | 'ready' | 'error'>('loading');
  const [stocksLoadAttempt, setStocksLoadAttempt] = useState(0);
  const [showSkillDesc, setShowSkillDesc] = useState<string | null>(null);
  const [mobileSkillPickerOpen, setMobileSkillPickerOpen] = useState(false);
  const [expandedThinking, setExpandedThinking] = useState<Set<string>>(new Set());
  const [deleteConfirmId, setDeleteConfirmId] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [sending, setSending] = useState(false);
  const [isFollowUpContextLoading, setIsFollowUpContextLoading] = useState(false);
  const [sendToast, setSendToast] = useState<{
    type: 'success' | 'error';
    message: LocalizedFeedback;
  } | null>(null);
  const [copiedMessages, setCopiedMessages] = useState<Set<string>>(new Set());
  const [showJumpToBottom, setShowJumpToBottom] = useState(false);
  const [activeStockContext, setActiveStockContext] = useState<ActiveStockContext | null>(null);
  const copyResetTimerRef = useRef<Partial<Record<string, number>>>({});
  const messagesViewportRef = useRef<HTMLDivElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const isMountedRef = useRef(true);
  const sendToastTimerRef = useRef<number | null>(null);
  const followUpHydrationTokenRef = useRef(0);
  const followUpContextRef = useRef<ChatFollowUpContext | null>(null);
  const shouldStickToBottomRef = useRef(false);
  const pendingScrollToTopRef = useRef(true);
  const pendingScrollBehaviorRef = useRef<ScrollBehavior>('auto');

  // Cleanup timers on unmount
  useEffect(() => {
    const timers = copyResetTimerRef.current;
    return () => {
      if (sendToastTimerRef.current !== null) {
        window.clearTimeout(sendToastTimerRef.current);
      }
      Object.values(timers).forEach((timerId) => {
        if (timerId !== undefined) {
          window.clearTimeout(timerId);
        }
      });
    };
  }, []);

  // Set page title
  useEffect(() => {
    document.title = text.documentTitle;
  }, [text.documentTitle]);

  useEffect(() => () => {
    isMountedRef.current = false;
  }, []);

  const {
    messages,
    loading,
    progressSteps,
    sessionId,
    sessions,
    sessionsLoading,
    chatError,
    loadSessions,
    loadInitialSession,
    switchSession,
    startStream,
    clearCompletionBadge,
  } = useAgentChatStore();

  const syncScrollState = useCallback(() => {
    const viewport = messagesViewportRef.current;
    if (!viewport) return;
    if (pendingScrollToTopRef.current) return;
    if (viewport.scrollHeight <= viewport.clientHeight) {
      setShowJumpToBottom(false);
      return;
    }
    const nearBottom = isNearBottom({
      scrollTop: viewport.scrollTop,
      clientHeight: viewport.clientHeight,
      scrollHeight: viewport.scrollHeight,
    });
    shouldStickToBottomRef.current = nearBottom;
    setShowJumpToBottom((prev) => (nearBottom ? false : prev));
  }, []);

  const scrollToBottom = useCallback((behavior: ScrollBehavior = 'auto') => {
    messagesEndRef.current?.scrollIntoView({ behavior });
  }, []);

  const requestScrollToBottom = useCallback((behavior: ScrollBehavior = 'auto') => {
    pendingScrollToTopRef.current = false;
    shouldStickToBottomRef.current = true;
    pendingScrollBehaviorRef.current = behavior;
    setShowJumpToBottom(false);
  }, []);

  const scrollToTop = useCallback(() => {
    pendingScrollToTopRef.current = true;
    shouldStickToBottomRef.current = false;
    pendingScrollBehaviorRef.current = 'auto';
    setShowJumpToBottom(false);
    if (messagesViewportRef.current) {
      messagesViewportRef.current.scrollTop = 0;
    }
  }, []);

  const handleMessagesScroll = useCallback(() => {
    syncScrollState();
  }, [syncScrollState]);

  useEffect(() => {
    pendingScrollToTopRef.current = true;
    shouldStickToBottomRef.current = false;
    pendingScrollBehaviorRef.current = 'auto';
    if (messagesViewportRef.current) {
      messagesViewportRef.current.scrollTop = 0;
    }
  }, [sessionId]);

  useEffect(() => {
    if (pendingScrollToTopRef.current) {
      if (messages.length === 0) return;
      const frame = window.requestAnimationFrame(() => {
        const viewport = messagesViewportRef.current;
        if (!viewport) return;
        viewport.scrollTop = 0;
        shouldStickToBottomRef.current = false;
        pendingScrollToTopRef.current = false;
        setShowJumpToBottom(viewport.scrollHeight > viewport.clientHeight);
      });
      return () => window.cancelAnimationFrame(frame);
    }
    const behavior = pendingScrollBehaviorRef.current;
    const shouldAutoScroll = shouldStickToBottomRef.current;
    if (!shouldAutoScroll) {
      if (messages.length > 0 || progressSteps.length > 0 || loading) {
        setShowJumpToBottom(true);
      }
      return;
    }

    const frame = window.requestAnimationFrame(() => {
      scrollToBottom(behavior);
      pendingScrollBehaviorRef.current = loading ? 'auto' : 'smooth';
    });

    return () => window.cancelAnimationFrame(frame);
  }, [messages, progressSteps, loading, sessionId, scrollToBottom]);

  useEffect(() => {
    if (!loading) {
      pendingScrollBehaviorRef.current = 'smooth';
    }
  }, [loading]);

  useEffect(() => {
    clearCompletionBadge();
  }, [clearCompletionBadge]);

  useEffect(() => {
    loadInitialSession();
  }, [loadInitialSession]);

  useEffect(() => {
    let active = true;
    agentApi.getSkills()
      .then((res) => {
        if (!active) return;
        setSkills(res.skills);
        const defaultId = res.skills.find((skill) => skill.id === 'bull_trend')?.id
          || res.skills.find((skill) => skill.id === res.default_skill_id)?.id
          || res.skills[0]?.id
          || '';
        setSelectedSkillId(defaultId);
        setSkillsStatus(defaultId ? 'ready' : 'empty');
      })
      .catch((error) => {
        if (!active) return;
        console.error('Failed to load chat skills:', error);
        setSkillsStatus('error');
      });
    return () => { active = false; };
  }, [skillsLoadAttempt]);

  useEffect(() => {
    let active = true;
    systemConfigApi.getWatchlist()
      .then((codes) => {
        if (!active) return;
        const uniqueCodes: string[] = [];
        for (const rawCode of codes) {
          const code = rawCode.trim();
          if (code && !uniqueCodes.some((existing) => areStockCodesEquivalent(existing, code))) {
            uniqueCodes.push(code);
          }
          if (uniqueCodes.length === 6) break;
        }
        setStockCodes(uniqueCodes);
        setSelectedStockCode(uniqueCodes[0] ?? '');
        setStocksStatus('ready');
      })
      .catch((error) => {
        if (!active) return;
        console.error('Failed to load chat stocks:', error);
        setStocksStatus('error');
      });
    return () => { active = false; };
  }, [stocksLoadAttempt]);

  const selectedSkill = skills.find((skill) => skill.id === selectedSkillId);
  const promptForSkill = (skill: SkillInfo | undefined) => skill && selectedStockCode
    ? formatUiText(text.generatedPrompt, {
      strategy: getChatSkillText(skill, language).name,
      stock: selectedStockCode,
    })
    : '';
  const generatedPrompt = promptForSkill(selectedSkill);
  const quickQuestions = selectedStockCode ? CHAT_QUICK_QUESTIONS[language]
    .filter((question, index, questions) =>
      questions.findIndex((item) => item.skill === question.skill) === index)
    .flatMap((question) => {
      const skill = skills.find((item) => item.id === question.skill);
      if (!skill) return [];
      return [{
        ...question,
        label: formatUiText(text.quickStockQuestion, { stock: selectedStockCode, strategy: getChatSkillText(skill, language).name }),
      }];
    }) : [];
  const getSkillNames = useCallback(
    (skillIds: string[]) => skillIds.map((id) => skills.find((s) => s.id === id)?.name || id),
    [skills],
  );

  const resetDeletedSession = useCallback(() => {
    followUpContextRef.current = null;
    setActiveStockContext(null);
    scrollToTop();
    useAgentChatStore.getState().resetDeletedSession();
    setSidebarOpen(false);
  }, [scrollToTop]);

  const handleSwitchSession = useCallback((targetSessionId: string) => {
    if (targetSessionId === sessionId) {
      setSidebarOpen(false);
      return;
    }
    followUpContextRef.current = null;
    setActiveStockContext(null);
    scrollToTop();
    switchSession(targetSessionId);
    setSidebarOpen(false);
  }, [scrollToTop, sessionId, switchSession]);

  const confirmDelete = useCallback(() => {
    if (!deleteConfirmId) return;
    agentApi.deleteChatSession(deleteConfirmId)
      .then(() => {
        loadSessions();
        if (deleteConfirmId === sessionId) {
          resetDeletedSession();
        }
      })
      .catch((error) => {
        console.error('Failed to delete chat session:', error);
      });
    setDeleteConfirmId(null);
  }, [deleteConfirmId, sessionId, loadSessions, resetDeletedSession]);

  // Handle follow-up from report page: ?stock=600519&name=贵州茅台&recordId=xxx
  useEffect(() => {
    const stock = sanitizeFollowUpStockCode(searchParams.get('stock'));
    const name = sanitizeFollowUpStockName(searchParams.get('name'));
    const recordId = parseFollowUpRecordId(searchParams.get('recordId'));

    if (!stock) {
      setSearchParams({}, { replace: true });
      return;
    }

    const hydrationToken = ++followUpHydrationTokenRef.current;
    setActiveStockContext({
      stock_code: stock,
      stock_name: name,
    });
    followUpContextRef.current = {
      stock_code: stock,
      stock_name: name,
    };
    if (recordId !== undefined) {
      setIsFollowUpContextLoading(true);
    }
    void resolveChatFollowUpContext({
      stockCode: stock,
      stockName: name,
      recordId,
    }).then((context) => {
      if (!isMountedRef.current || followUpHydrationTokenRef.current !== hydrationToken) {
        return;
      }
      followUpContextRef.current = context;
    }).finally(() => {
      if (isMountedRef.current && followUpHydrationTokenRef.current === hydrationToken) {
        setIsFollowUpContextLoading(false);
      }
    });
    setSearchParams({}, { replace: true });
  }, [searchParams, setSearchParams, language]);

  const handleSend = async (overrideSkillId?: string) => {
    if (loading || skillsStatus !== 'ready' || stocksStatus !== 'ready'
      || !selectedStockCode || !stockCodes.includes(selectedStockCode)) return;
    const usedSkillId = overrideSkillId ?? selectedSkillId;
    const usedSkill = skills.find((skill) => skill.id === usedSkillId);
    if (!usedSkill) {
      console.error('Cannot send chat without an available strategy');
      return;
    }
    const msgText = promptForSkill(usedSkill);
    const usedSkillIds = [usedSkillId];
    const usedSkillNames = getSkillNames(usedSkillIds);

    const matchingContext = [followUpContextRef.current, activeStockContext]
      .find((context) => context && areStockCodesEquivalent(context.stock_code, selectedStockCode));
    const contextForSend = matchingContext ?? { stock_code: selectedStockCode, stock_name: null };
    setActiveStockContext(contextForSend);

    const payload = {
      message: msgText,
      session_id: sessionId,
      skills: usedSkillIds,
      context: { ...contextForSend, lock_stock_scope: true },
    };
    followUpHydrationTokenRef.current += 1;
    followUpContextRef.current = null;
    setIsFollowUpContextLoading(false);

    setMobileSkillPickerOpen(false);
    requestScrollToBottom('smooth');
    await startStream(payload, {
      skillNames: usedSkillNames,
      skillName: usedSkillNames.join('、'),
    });
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleQuickQuestion = (q: { label: string; skill: string }) => {
    setSelectedSkillId(q.skill);
    handleSend(q.skill);
  };

  const showSendFeedback = useCallback((nextToast: { type: 'success' | 'error'; message: LocalizedFeedback }, durationMs: number) => {
    if (sendToastTimerRef.current !== null) {
      window.clearTimeout(sendToastTimerRef.current);
    }
    setSendToast(nextToast);
    sendToastTimerRef.current = window.setTimeout(() => {
      setSendToast(null);
      sendToastTimerRef.current = null;
    }, durationMs);
  }, []);

  const toggleThinking = (msgId: string) => {
    setExpandedThinking((prev) => {
      const next = new Set(prev);
      if (next.has(msgId)) next.delete(msgId);
      else next.add(msgId);
      return next;
    });
  };

  const copyMessageToClipboard = async (msgId: string, content: string) => {
    try {
      await navigator.clipboard.writeText(content);
      setCopiedMessages((prev) => new Set(prev).add(msgId));
      const existingTimer = copyResetTimerRef.current[msgId];
      if (existingTimer !== undefined) {
        window.clearTimeout(existingTimer);
      }
      copyResetTimerRef.current[msgId] = window.setTimeout(() => {
        setCopiedMessages((prev) => {
          const next = new Set(prev);
          next.delete(msgId);
          return next;
        });
        delete copyResetTimerRef.current[msgId];
      }, 2000);
    } catch (err) {
      console.error('Copy failed:', err);
    }
  };

  const downloadMessageAsMarkdown = useCallback((msg: Message) => {
    const skillLabel = getMessageSkillLabel(msg, language);
    const heading = msg.role === 'user' ? text.userMessage : `${text.aiReply}${skillLabel ? ` · ${skillLabel}` : ''}`;
    const content = [heading, '', msg.content].join('\n');
    const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = `${msg.role === 'user' ? 'user' : 'assistant'}-message-${msg.id}.md`;
    document.body.appendChild(anchor);
    anchor.click();
    document.body.removeChild(anchor);
    URL.revokeObjectURL(url);
  }, [language, text.userMessage, text.aiReply]);

  const getCurrentStage = (steps: ProgressStep[]): string => {
    if (steps.length === 0) return text.connecting;
    const last = steps[steps.length - 1];
    if (last.type === 'thinking') return last.message || text.thinking;
    if (last.type === 'tool_start')
      return `${last.display_name || last.tool}...`;
    if (last.type === 'tool_done')
      return formatUiText(text.toolDone, { tool: last.display_name || last.tool || '' });
    if (last.type === 'generating')
      return last.message || text.generating;
    return text.processing;
  };

  const renderThinkingBlock = (msg: Message) => {
    if (!msg.thinkingSteps || msg.thinkingSteps.length === 0) return null;
    const isExpanded = expandedThinking.has(msg.id);
    const toolSteps = msg.thinkingSteps.filter((s) => s.type === 'tool_done');
    const totalDuration = toolSteps.reduce(
      (sum, s) => sum + (s.duration || 0),
      0,
    );
    const summary = formatUiText(text.toolSummary, { count: toolSteps.length, duration: totalDuration.toFixed(1) });

    return (
      <button
        onClick={() => toggleThinking(msg.id)}
        className="flex items-center gap-2 text-xs text-muted-text hover:text-secondary-text transition-colors mb-2 w-full text-left"
      >
        <svg
          className={`w-3 h-3 transition-transform flex-shrink-0 ${isExpanded ? 'rotate-90' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 5l7 7-7 7"
          />
        </svg>
        <span className="flex items-center gap-1.5">
          <span className="opacity-60">{text.thinkingProcess}</span>
          <span className="text-muted-text/50">·</span>
          <span className="opacity-50">{summary}</span>
        </span>
      </button>
    );
  };

  const renderThinkingDetails = (steps: ProgressStep[]) => (
    <div className="mb-3 pl-5 border-l border-border/40 space-y-1.5 animate-fade-in">
      {steps.map((step, idx) => {
        let statusClass = 'chat-progress-item-muted';
        let iconClass = 'chat-progress-dot-muted';
        let stepText = '';
        if (step.type === 'thinking') {
          stepText = step.message || formatUiText(text.thinkingStep, { step: step.step ?? '' });
          statusClass = 'chat-progress-item-thinking';
          iconClass = 'chat-progress-dot-thinking';
        } else if (step.type === 'tool_start') {
          stepText = `${step.display_name || step.tool}...`;
          statusClass = 'chat-progress-item-tool';
          iconClass = 'chat-progress-dot-tool';
        } else if (step.type === 'tool_done') {
          stepText = `${step.display_name || step.tool} (${step.duration}s)`;
          statusClass = step.success ? 'chat-progress-item-success' : 'chat-progress-item-danger';
          iconClass = step.success ? 'chat-progress-dot-success' : 'chat-progress-dot-danger';
        } else if (step.type === 'generating') {
          stepText = step.message || text.generatingAnalysis;
          statusClass = 'chat-progress-item-generating';
          iconClass = 'chat-progress-dot-generating';
        }
        return (
          <div
            key={idx}
            className={cn('chat-progress-item', statusClass)}
          >
            <span className={cn('chat-progress-dot', iconClass)} />
            <span className="leading-relaxed">{stepText}</span>
          </div>
        );
      })}
    </div>
  );

  const sidebarContent = (
    <>
      <div className="flex items-center justify-between border-b border-white/5 bg-white/2 p-3.5">
        <h2 className="text-sm font-semibold text-cyan uppercase tracking-[0.2em] flex items-center gap-2">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {text.history}
        </h2>
      </div>
      <ScrollArea testId="chat-session-list-scroll" viewportClassName="p-3">
        {sessionsLoading ? (
          <DashboardStateBlock
            loading
            compact
            title={text.loadingSessions}
            className="rounded-2xl border border-dashed border-border/50 bg-surface/30"
          />
        ) : sessions.length === 0 ? (
          <DashboardStateBlock
            compact
            title={text.noSessions}
            description={text.noSessionsHint}
            className="rounded-2xl border border-dashed border-border/50 bg-surface/30"
          />
        ) : (
          <div className="space-y-2">
            {sessions.map((s) => (
              <div key={s.session_id} className="session-item-row">
                <button
                  type="button"
                  onClick={() => handleSwitchSession(s.session_id)}
                  className={`session-item ${s.session_id === sessionId ? 'active' : ''}`}
                  aria-label={formatUiText(text.switchSession, { title: s.title })}
                  aria-current={s.session_id === sessionId ? 'page' : undefined}
                >
                  <div className="indicator" />
                  <div className="content">
                    <span className="title">{s.title}</span>
                    <div className="mt-0.5 flex items-center gap-2">
                      <span className="meta">
                        {formatUiText(text.messageCount, { count: s.message_count })}
                      </span>
                      {s.last_active && (
                        <>
                          <span className="separator" />
                          <span className="meta">
                            {new Date(s.last_active).toLocaleDateString(language === 'en' ? 'en-US' : 'zh-CN', { month: 'short', day: 'numeric' })}
                          </span>
                        </>
                      )}
                    </div>
                  </div>
                </button>
                <button
                  type="button"
                  className="delete-btn"
                  onClick={() => {
                    setDeleteConfirmId(s.session_id);
                  }}
                  aria-label={formatUiText(text.deleteSession, { title: s.title })}
                >
                  <svg
                    className="w-3.5 h-3.5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                    />
                  </svg>
                </button>
              </div>
            ))}
          </div>
        )}
      </ScrollArea>
    </>
  );

  const selectedSkillSummary = selectedSkill
    ? getChatSkillText(selectedSkill, language).name
    : getChatSkillName(selectedSkillId, language);

  return (
    <div
      data-testid="chat-workspace"
      className="flex h-[calc(100vh-5rem)] w-full min-w-0 gap-4 overflow-hidden sm:h-[calc(100vh-5.5rem)] lg:h-[calc(100vh-3rem)]"
    >
      {/* Desktop sidebar */}
      <div className="chat-history-panel hidden h-full w-64 flex-shrink-0 flex-col overflow-hidden rounded-[1.25rem] border bg-card/82 shadow-soft-card md:flex">
        {sidebarContent}
      </div>

      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 md:hidden"
          onClick={() => setSidebarOpen(false)}
        >
          <div className="page-drawer-overlay absolute inset-0" />
          <div
            className="chat-history-panel absolute left-0 top-0 bottom-0 w-72 flex flex-col glass-card overflow-hidden bg-card/90 shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            {sidebarContent}
          </div>
        </div>
      )}

      {/* Delete confirmation dialog */}
      <ConfirmDialog
        isOpen={Boolean(deleteConfirmId)}
        title={text.deleteTitle}
        message={text.deleteMessage}
        confirmText={text.delete}
        cancelText={text.cancel}
        isDanger
        onConfirm={confirmDelete}
        onCancel={() => setDeleteConfirmId(null)}
      />

      {/* Main chat area */}
      <div className="flex h-full min-w-0 flex-1 flex-col overflow-hidden">
        <header className="mb-4 flex-shrink-0 space-y-3">
          <div className="flex items-start justify-between gap-4">
            <h1 className="text-2xl font-bold text-foreground flex items-center gap-2">
              <button
                onClick={() => setSidebarOpen(true)}
                className="md:hidden p-1.5 -ml-1 rounded-lg hover:bg-hover transition-colors text-secondary-text hover:text-foreground"
                aria-label={text.history}
              >
                <svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                </svg>
              </button>
              <svg
                className="w-6 h-6 text-cyan"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                />
              </svg>
              {text.title}
            </h1>
            {messages.length > 0 && (
              <div className="flex flex-shrink-0 flex-wrap items-center justify-end gap-2">
                <Tooltip content={text.exportSessionHint}>
                  <span className="inline-flex">
                    <Button
                      variant="action-primary"
                      size="sm"
                      onClick={() => downloadSession(messages, language)}
                      aria-label={text.exportSessionHint}
                    >
                      <svg
                        className="w-4 h-4"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                        />
                      </svg>
                      {text.exportSession}
                    </Button>
                  </span>
                </Tooltip>
                <Tooltip content={text.sendHint}>
                  <span className="inline-flex">
                    <Button
                      variant="action-primary"
                      size="sm"
                      disabled={sending}
                      onClick={async () => {
                        if (sending) return;
                        setSending(true);
                        setSendToast(null);
                        try {
                          const content = formatSessionAsMarkdown(messages, language);
                          await agentApi.sendChat(content);
                          showSendFeedback({ type: 'success', message: (language) => CHAT_TEXT[language].sent }, 3000);
                        } catch (err) {
                          const parsed = getParsedApiError(err);
                          showSendFeedback({
                            type: 'error',
                            message: (language) => parsed.message || CHAT_TEXT[language].sendFailed,
                          }, 5000);
                        } finally {
                          setSending(false);
                        }
                      }}
                      aria-label={text.sendHint}
                    >
                      {sending ? (
                        <svg
                          className="w-4 h-4 animate-spin"
                          fill="none"
                          viewBox="0 0 24 24"
                        >
                          <circle
                            className="opacity-25"
                            cx="12"
                            cy="12"
                            r="10"
                            stroke="currentColor"
                            strokeWidth="4"
                          />
                          <path
                            className="opacity-75"
                            fill="currentColor"
                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                          />
                        </svg>
                      ) : (
                        <svg
                          className="w-4 h-4"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                          />
                        </svg>
                      )}
                      {text.send}
                    </Button>
                  </span>
                </Tooltip>
              </div>
            )}
          </div>
          <p className="text-secondary-text text-sm">
            {text.description}
          </p>
          {sendToast ? (
            <InlineAlert
              variant={sendToast.type === 'success' ? 'success' : 'danger'}
              title={sendToast.type === 'success' ? text.sendSuccess : text.sendFailed}
              message={resolveFeedback(sendToast.message, language)}
              className="max-w-md rounded-xl px-3 py-2 text-xs shadow-none"
            />
          ) : null}
        </header>

        <div className="chat-conversation-panel relative z-10 flex min-h-0 flex-1 flex-col overflow-hidden bg-card/78 glass-card">
          {/* Messages */}
          <ScrollArea
            className="relative z-10 flex-1"
            viewportRef={messagesViewportRef}
            onScroll={handleMessagesScroll}
            viewportClassName="space-y-6 p-4 md:p-6"
            testId="chat-message-scroll"
          >
            {messages.length === 0 && !loading ? (
              <div className="flex h-full items-center justify-center">
                <EmptyState
                  title={text.start}
                  description={text.startHint}
                  className="max-w-2xl border-dashed bg-card/55"
                  icon={(
                    <svg
                      className="h-8 w-8"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={1.5}
                        d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                      />
                    </svg>
                  )}
                  action={(
                    <div className="flex max-w-lg flex-wrap justify-center gap-2">
                      {quickQuestions.map((q, i) => (
                        <button
                          key={i}
                          onClick={() => handleQuickQuestion(q)}
                          disabled={loading || stocksStatus !== 'ready' || skillsStatus !== 'ready'}
                          className="quick-question-btn"
                        >
                         {q.label}
                        </button>
                      ))}
                    </div>
                  )}
                />
              </div>
            ) : (
              messages.map((msg) => {
                const skillLabel = getMessageSkillLabel(msg, language);
                return (
                <div
                  key={msg.id}
                  className={`flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
                >
                  <div
                    className={cn(
                      'flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-[10px] font-bold shadow-sm transition-all',
                      msg.role === 'user' ? 'chat-avatar-user' : 'chat-avatar-ai'
                    )}
                  >
                    {msg.role === 'user' ? 'U' : 'AI'}
                  </div>
                  <div
                    className={cn(
                      'group/message min-w-0 overflow-hidden px-5 py-3.5 transition-colors',
                      msg.role === 'user'
                        ? 'w-fit max-w-[min(100%,48rem)] chat-bubble-user'
                        : 'flex-1 chat-bubble-ai'
                    )}
                  >
                    {msg.role === 'assistant' && skillLabel && (
                      <div className="mb-2">
                        <Badge variant="info" className="chat-skill-badge shadow-none" aria-label={formatUiText(text.skillLabel, { skills: skillLabel })}>
                          <svg
                            className="w-3 h-3"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M13 10V3L4 14h7v7l9-11h-7z"
                            />
                          </svg>
                          {skillLabel}
                        </Badge>
                      </div>
                    )}
                    {msg.role === 'assistant' && renderThinkingBlock(msg)}
                    {msg.role === 'assistant' &&
                      expandedThinking.has(msg.id) &&
                      msg.thinkingSteps &&
                      renderThinkingDetails(msg.thinkingSteps)}
                    {msg.role === 'assistant' ? (
                      <div className="flow-root">
                        <div className="chat-message-actions">
                          <button
                            type="button"
                            onClick={() => copyMessageToClipboard(msg.id, msg.content)}
                            className="chat-copy-btn"
                            aria-label={copiedMessages.has(msg.id) ? text.copied : text.copy}
                          >
                            {copiedMessages.has(msg.id) ? text.copied : text.copy}
                          </button>
                          <button
                            type="button"
                            onClick={() => downloadMessageAsMarkdown(msg)}
                            className="chat-copy-btn"
                            aria-label={text.exportMessage}
                          >
                            {text.export}
                          </button>
                        </div>
                        <div className="chat-prose">
                          <Markdown remarkPlugins={[remarkGfm]}>
                            {msg.content}
                          </Markdown>
                        </div>
                      </div>
                    ) : (
                      msg.content
                        .split('\n')
                        .map((line, i) => (
                          <p
                            key={i}
                            className="mb-1 last:mb-0 leading-relaxed"
                          >
                            {line || '\u00A0'}
                          </p>
                        ))
                    )}
                  </div>
                </div>
                );
              })
            )}

            {loading && (
              <div className="flex gap-4">
                <div className="w-8 h-8 rounded-full bg-elevated text-foreground flex items-center justify-center flex-shrink-0 text-xs font-bold">
                  AI
                </div>
                <div className="min-w-[200px] max-w-[min(100%,48rem)] overflow-hidden rounded-2xl rounded-tl-sm border border-white/6 bg-card/72 px-5 py-4">
                  <div className="flex items-center gap-2.5 text-sm text-secondary-text">
                    <div className="relative w-4 h-4 flex-shrink-0">
                      <div className="absolute inset-0 rounded-full border-2 border-cyan/20" />
                      <div className="absolute inset-0 rounded-full border-2 border-cyan border-t-transparent animate-spin" />
                    </div>
                    <span className="text-secondary-text">
                      {getCurrentStage(progressSteps)}
                    </span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </ScrollArea>

          {showJumpToBottom && (
            <div className="pointer-events-none absolute bottom-[5.75rem] right-4 z-20 md:bottom-24 md:right-6">
              <button
                type="button"
                className="pointer-events-auto chat-copy-btn shadow-soft-card"
                onClick={() => {
                  requestScrollToBottom('smooth');
                  scrollToBottom('smooth');
                }}
                aria-label={text.latestMessage}
              >
                <svg
                  className="h-3.5 w-3.5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 14l-7 7m0 0l-7-7m7 7V3"
                  />
                </svg>
                {text.newMessages}
              </button>
            </div>
          )}

          {/* Input area */}
          <div className="border-t border-white/6 bg-card/88 p-4 md:p-6 relative z-20">
            <div className="space-y-3">
              {chatError ? <ApiErrorAlert error={chatError} /> : null}
              {isFollowUpContextLoading ? (
                <InlineAlert
                  variant="info"
                  title={text.loadingFollowUp}
                  message={text.loadingFollowUpHint}
                  className="rounded-xl px-3 py-2 text-xs shadow-none"
                />
              ) : null}
              {skillsStatus === 'loading' && (
                <p role="status" className="text-xs text-muted-text">{text.strategiesLoading}</p>
              )}
              {(skillsStatus === 'error' || skillsStatus === 'empty') && (
                <InlineAlert
                  variant="danger"
                  message={skillsStatus === 'error' ? text.strategiesLoadFailed : text.strategiesEmpty}
                  action={(
                    <Button
                      variant="secondary"
                      size="xsm"
                      onClick={() => {
                        setSkillsStatus('loading');
                        setSkillsLoadAttempt((attempt) => attempt + 1);
                      }}
                    >
                      {text.retryStrategies}
                    </Button>
                  )}
                  className="rounded-xl px-3 py-2"
                />
              )}
              {skillsStatus === 'ready' && (
                <div className="space-y-2">
                  <button
                    type="button"
                    className="home-surface-button flex h-10 w-full items-center justify-between gap-3 rounded-xl px-3 text-left text-sm text-foreground md:hidden"
                    aria-label={mobileSkillPickerOpen ? text.collapseStrategies : text.expandStrategies}
                    aria-expanded={mobileSkillPickerOpen}
                    aria-controls="chat-skill-picker-panel"
                    onClick={() => setMobileSkillPickerOpen((open) => !open)}
                  >
                    <span className="flex min-w-0 items-center gap-2">
                      <SlidersHorizontal className="h-4 w-4 flex-shrink-0" aria-hidden="true" />
                      <span className="flex-shrink-0 font-medium">{text.strategy}</span>
                      <span className="truncate text-xs text-muted-text">{selectedSkillSummary}</span>
                    </span>
                    <ChevronDown
                      className={cn(
                        'h-4 w-4 flex-shrink-0 text-muted-text transition-transform',
                        mobileSkillPickerOpen ? 'rotate-180' : '',
                      )}
                      aria-hidden="true"
                    />
                  </button>
                  <div
                    id="chat-skill-picker-panel"
                    data-testid="chat-skill-picker-panel"
                    role="radiogroup"
                    aria-labelledby="chat-skill-picker-label"
                    className={cn(
                      mobileSkillPickerOpen ? 'flex' : 'hidden',
                      'max-h-40 flex-wrap items-start gap-x-5 gap-y-2 overflow-y-auto rounded-xl border border-white/6 bg-surface/25 px-3 py-2 md:flex md:max-h-none md:overflow-visible md:border-0 md:bg-transparent md:p-0',
                    )}
                  >
                    <span id="chat-skill-picker-label" className="w-full text-xs text-muted-text font-medium uppercase tracking-wider">
                      {text.strategy}
                    </span>
                    <div className="grid min-w-0 flex-1 grid-cols-2 gap-x-4 gap-y-2 md:grid-cols-4">
                      {skills.map((s) => {
                        const skillText = getChatSkillText(s, language);
                        const checked = selectedSkillId === s.id;
                        return (
                          <label
                            key={s.id}
                            className="flex min-w-0 items-center gap-1.5 cursor-pointer group relative mt-0.5"
                            onMouseEnter={() => setShowSkillDesc(s.id)}
                            onMouseLeave={() => setShowSkillDesc(null)}
                          >
                            <input
                              type="radio"
                              name="skills"
                              value={s.id}
                              checked={checked}
                              onChange={() => setSelectedSkillId(s.id)}
                              className="chat-skill-radio"
                            />
                            <span
                              className={`min-w-0 break-words transition-colors text-sm ${checked ? 'text-foreground font-medium' : 'text-secondary-text group-hover:text-foreground'}`}
                            >
                              {skillText.name}
                            </span>
                            {showSkillDesc === s.id && s.description && (
                              <div className="skill-desc-tooltip">
                                <p className="skill-title">{skillText.name}</p>
                                <p>{skillText.description}</p>
                              </div>
                            )}
                          </label>
                        );
                      })}
                    </div>
                  </div>
                </div>
              )}

              {stocksStatus === 'loading' && (
                <p role="status" className="text-xs text-muted-text">{text.stocksLoading}</p>
              )}
              {stocksStatus === 'error' && (
                <InlineAlert
                  variant="danger"
                  message={text.stocksLoadFailed}
                  action={(
                    <Button variant="secondary" size="xsm" onClick={() => {
                      setStocksStatus('loading');
                      setStocksLoadAttempt((attempt) => attempt + 1);
                    }}>
                      {text.retryStrategies}
                    </Button>
                  )}
                  className="rounded-xl px-3 py-2"
                />
              )}
              {stocksStatus === 'ready' && stockCodes.length === 0 && (
                <InlineAlert variant="info" message={text.stocksEmpty} className="rounded-xl px-3 py-2 text-xs shadow-none" />
              )}
              {stocksStatus === 'ready' && stockCodes.length > 0 && (
                <div role="radiogroup" aria-label={text.stocks} className="flex flex-wrap items-center gap-x-5 gap-y-2 px-3 md:px-0">
                  <span className="text-xs text-muted-text font-medium uppercase tracking-wider">{text.stocks}</span>
                  {stockCodes.map((code) => (
                    <label key={code} className="flex items-center gap-1.5 cursor-pointer text-sm">
                      <input
                        type="radio"
                        name="stock"
                        value={code}
                        checked={selectedStockCode === code}
                        onChange={() => setSelectedStockCode(code)}
                        className="chat-skill-radio"
                      />
                      {code}
                    </label>
                  ))}
                </div>
              )}

              <div className="flex items-end gap-3">
                <textarea
                  value={generatedPrompt}
                  readOnly
                  aria-label={text.promptLabel}
                  onKeyDown={handleKeyDown}
                  placeholder={text.placeholder}
                  disabled={loading}
                  rows={1}
                  className="input-surface input-focus-glow flex-1 min-h-[44px] max-h-[200px] rounded-xl border bg-transparent px-4 py-2.5 text-sm transition-all focus:outline-none resize-none disabled:cursor-not-allowed disabled:opacity-60"
                />
                <Button
                  variant="primary"
                  onClick={() => handleSend()}
                  disabled={!generatedPrompt || loading || skillsStatus !== 'ready' || stocksStatus !== 'ready'}
                  isLoading={loading}
                  loadingText={text.sending}
                  className="btn-primary flex-shrink-0"
                >
                  {text.send}
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
