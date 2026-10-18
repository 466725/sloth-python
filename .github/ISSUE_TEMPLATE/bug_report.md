---
name: Bug 报告 / Bug Report
about: 报告一个问题帮助我们改进 / Report a problem to help us improve
title: '[Bug] '
labels: bug
assignees: ''
---

<!--
请用中文或英文填写下方表单，并删除不适用的提示。
Fill in the form in Chinese or English and remove prompts that do not apply.
-->

## 提交前检查 / Before You Submit

请先更新到最新版本并确认问题仍然存在，避免重复报告已修复的问题。

Update to the latest version and confirm the issue still occurs before filing.

Fork 用户请先同步上游代码；如果问题发生在 GitHub Actions 中，请使用最新代码重新运行工作流。

Fork users: sync with upstream first. For GitHub Actions issues, rerun the workflow on the latest code.

## 版本信息 / Version Information（必填 / Required）

- [ ] 我已更新到最新代码，并确认问题仍然存在 / I updated to the latest code and confirmed the issue still occurs.
- 提交版本 / Commit hash:
  - 本地 / Local: `git rev-parse --short HEAD` →
  - GitHub Actions: 工作流日志顶部显示的提交哈希 / commit hash at the top of the workflow log:

## 问题摘要 / Problem Summary

简要说明问题及其影响。

Summarize the problem and its impact.

## 复现步骤 / Steps to Reproduce

1. 执行的命令或操作 / Command or action:
2. 使用的配置或输入 / Configuration or input:
3. 观察到的结果 / Observed result:

## 期望结果与实际结果 / Expected and Actual Behavior

- 期望结果 / Expected:
- 实际结果 / Actual:

## 错误日志 / Error Logs（可选 / Optional）

```text
粘贴相关日志 / Paste relevant logs
```

请先删除日志中的密码、令牌、API 密钥和个人信息。

Remove passwords, tokens, API keys, and personal information before posting logs.

## 环境信息 / Environment Information

- 操作系统 / OS: [例如 Ubuntu 22.04、Windows 11、macOS 14 / e.g. Ubuntu 22.04, Windows 11, macOS 14]
- Python 版本 / Python version:
- 运行方式 / Run mode: [本地、Docker、GitHub Actions / Local, Docker, GitHub Actions]
- 相关 AI 模型或数据源 / Relevant AI model or data source:
- 相关配置（请勿包含密钥）/ Relevant configuration (no secrets):

## 补充信息 / Additional Context（可选 / Optional）

- 参考链接或截图 / Reference links or screenshots:
- 其他背景 / Other context:
