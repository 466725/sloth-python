import { describe, expect, it } from 'vitest';
import {
  LLM_PROVIDER_CAPABILITY_LABELS,
  LLM_PROVIDER_TEMPLATE_BY_ID,
  LLM_PROVIDER_TEMPLATES,
  MODEL_PLACEHOLDERS_BY_PROTOCOL,
  getProviderTemplate,
  getProviderCapabilityMeta,
  isKnownProviderTemplate,
} from '../llmProviderTemplates';

describe('llmProviderTemplates', () => {
  it('localizes every preset and capability without changing provider configuration', () => {
    for (const template of LLM_PROVIDER_TEMPLATES) {
      const localized = getProviderTemplate(template.channelId, 'en');
      expect(localized).toMatchObject({
        channelId: template.channelId,
        protocol: template.protocol,
        baseUrl: template.baseUrl,
        placeholderModels: template.placeholderModels,
        capabilities: template.capabilities,
        officialSources: template.officialSources,
      });
      expect(localized?.label).not.toMatch(/\p{Script=Han}/u);
      if (template.configHint) {
        expect(localized?.configHint).toBeTruthy();
        expect(localized?.configHint).not.toMatch(/\p{Script=Han}/u);
      }
      for (const capability of template.capabilities) {
        const metadata = getProviderCapabilityMeta(capability, 'en');
        expect(metadata.label).not.toMatch(/\p{Script=Han}/u);
        expect(metadata.hint).not.toMatch(/\p{Script=Han}/u);
        expect(getProviderCapabilityMeta(capability, 'zh')).toEqual(LLM_PROVIDER_CAPABILITY_LABELS[capability]);
      }
      expect(getProviderTemplate(template.channelId, 'zh')).toBe(template);
    }
  });

  it('keeps provider template order aligned with the existing preset dropdown order', () => {
    expect(LLM_PROVIDER_TEMPLATES.map((template) => template.channelId)).toEqual([
      'aihubmix',
      'anspire',
      'deepseek',
      'gemini',
      'openai',
      'custom',
    ]);
  });

  it('derives lookup keys from unique channel ids', () => {
    const channelIds = LLM_PROVIDER_TEMPLATES.map((template) => template.channelId);

    expect(new Set(channelIds).size).toBe(channelIds.length);
    for (const template of LLM_PROVIDER_TEMPLATES) {
      expect(LLM_PROVIDER_TEMPLATE_BY_ID[template.channelId]).toBe(template);
    }
  });

  it('does not offer removed providers', () => {
    expect(getProviderTemplate('anthropic')).toBeUndefined();
    expect(MODEL_PLACEHOLDERS_BY_PROTOCOL).not.toHaveProperty('anthropic');
    expect(getProviderTemplate('ollama')).toBeUndefined();
    expect(MODEL_PLACEHOLDERS_BY_PROTOCOL).not.toHaveProperty('ollama');
  });

  it('exposes safe helpers for known, custom, and unknown channel ids', () => {
    expect(getProviderTemplate('deepseek')).toBe(LLM_PROVIDER_TEMPLATE_BY_ID.deepseek);
    expect(getProviderTemplate('custom')).toBe(LLM_PROVIDER_TEMPLATE_BY_ID.custom);
    expect(getProviderTemplate('unknown-provider')).toBeUndefined();
    expect(getProviderTemplate('constructor')).toBeUndefined();
    expect(getProviderTemplate('toString')).toBeUndefined();

    expect(isKnownProviderTemplate('deepseek')).toBe(true);
    expect(isKnownProviderTemplate('custom')).toBe(false);
    expect(isKnownProviderTemplate('unknown-provider')).toBe(false);
    expect(isKnownProviderTemplate('constructor')).toBe(false);
    expect(isKnownProviderTemplate('toString')).toBe(false);
  });

  it('only defines static provider-template capabilities for P2 UI hints', () => {
    expect(Object.keys(LLM_PROVIDER_CAPABILITY_LABELS).sort()).toEqual([
      'aggregator',
      'model-discovery',
      'official-api',
      'openai-compatible',
      'vision',
    ]);
    expect(LLM_PROVIDER_CAPABILITY_LABELS).not.toHaveProperty('json');
    expect(LLM_PROVIDER_CAPABILITY_LABELS).not.toHaveProperty('tools');
    expect(LLM_PROVIDER_CAPABILITY_LABELS).not.toHaveProperty('stream');
  });

  it('keeps focused config hints on providers with common setup pitfalls', () => {
    expect(LLM_PROVIDER_TEMPLATE_BY_ID.openai.configHint).toBeUndefined();
  });

  it('keeps basic metadata on non-custom provider templates', () => {
    for (const template of LLM_PROVIDER_TEMPLATES.filter((item) => item.channelId !== 'custom')) {
      expect(template.capabilities.length).toBeGreaterThan(0);
      expect(template.officialSources.length).toBeGreaterThan(0);
    }
  });

  it('keeps protocol-level fallback placeholders centralized', () => {
    expect(MODEL_PLACEHOLDERS_BY_PROTOCOL).toMatchObject({
      openai: 'gpt-5.5,qwen3.6-plus',
      deepseek: 'deepseek-v4-flash,deepseek-v4-pro',
      gemini: 'gemini-3.1-pro-preview,gemini-3-flash-preview',
      vertex_ai: 'gemini-3.1-pro-preview',
    });
  });
});
