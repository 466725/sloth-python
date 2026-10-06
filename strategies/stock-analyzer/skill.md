---
name: stock-analyzer
display_name: Stock Analyzer
description: Analyze an individual stock using available market data, technical signals, relevant context, and explicit risk controls.
category: framework
user-invocable: true
default-active: false
default-priority: 100
---

# Stock Analysis

Use this skill when the user asks for an analysis of a specific stock or a follow-up about a stock already in context. Apply the guidance below alongside the DSA Agent's system instructions and required response format.

## Analysis workflow

1. **Confirm the subject and context.** Use the stock code, name, market, and time horizon supplied by the user or present in the conversation. If the subject cannot be identified reliably, ask for clarification rather than guessing.
2. **Gather evidence.** Use the available Agent tools to inspect relevant current quotes, historical prices, technical indicators, and—when available and relevant—fundamentals, news, and market context. Prefer tool results over assumptions.
3. **Check data quality.** Consider timestamps, market session, missing fields, and any stale, estimated, partial, or failed data. State material limitations and lower confidence when evidence is incomplete or out of date.
4. **Evaluate the setup.** Consider trend direction and strength, price relative to meaningful support and resistance, volume confirmation, and relevant catalysts or risks. Separate observed facts from interpretation.
5. **Form a conditional view.** Explain what supports the conclusion, what would invalidate it, and what evidence would change the view. Distinguish advice for a user with no position from risk management for an existing position when relevant.
6. **Respect the response contract.** Preserve the output format and language required by the DSA Agent and the user's request. Do not replace or omit fields required by the application.

## Decision and risk discipline

- Do not recommend buying solely because a score is high, a stock rose recently, or a single indicator turned positive.
- Avoid encouraging a purchase after an extended move. Prefer waiting for a supported pullback or a confirmed breakout when the available evidence warrants it.
- Favor a neutral, wait, or observe conclusion when price is between key levels, signals conflict, or the evidence does not establish a clear advantage.
- Treat a break of meaningful support, persistent selling pressure, deteriorating fundamentals, and material negative events as risks; explain their relevance rather than presenting them as certain outcomes.
- Give specific price levels only when they can be grounded in available data. Label them as conditional reference levels, not guaranteed entry, stop-loss, or target prices.
- Never invent quotes, indicators, news, financial results, dates, or tool outputs. If evidence is unavailable, say so and continue only with clearly identified limitations.
- Present analysis as informational, not as a guarantee of returns or a substitute for the user's independent judgment.
