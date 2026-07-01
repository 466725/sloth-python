# Claude Code Learning Index

## Overview
This folder collects practice projects, notebook-based exercises, and the Claude Certified Architect Foundations practice exam materials used to study Claude Code and related MCP workflows.

Goal: build fluency with Claude Code, MCP tool use, transport options, roots/file access, sampling, and exam-style reasoning.

Reference: https://anthropic.skilljar.com/

---

## Practice Projects

### 001_starter
An introductory MCP project focused on document tools.

Key files:
- [README.md](001_starter/README.md)
- [main.py](001_starter/main.py)
- [tools/document.py](001_starter/tools/document.py)
- [tools/math.py](001_starter/tools/math.py)
- [tests/test_document.py](001_starter/tests/test_document.py)

### 002_cli
A command-line chat application built on Anthropic and MCP.

Key files:
- [README.md](002_cli/README.md)
- [main.py](002_cli/main.py)
- [mcp_client.py](002_cli/mcp_client.py)
- [mcp_server.py](002_cli/mcp_server.py)
- [core/cli.py](002_cli/core/cli.py)

### 003_notifications
A stdio-based MCP demo for notifications and progress updates.

Key files:
- [README.md](003_notifications/README.md)
- [client.py](003_notifications/client.py)
- [server.py](003_notifications/server.py)

### 004_roots
A file-system-aware chat demo that uses MCP roots for controlled access.

Key files:
- [README.md](004_roots/README.md)
- [main.py](004_roots/main.py)
- [mcp_client.py](004_roots/mcp_client.py)
- [mcp_server.py](004_roots/mcp_server.py)
- [core/cli_chat.py](004_roots/core/cli_chat.py)
- [core/video_converter.py](004_roots/core/video_converter.py)

### 005_sampling
A sampling demo showing an MCP client/server flow for model sampling.

Key files:
- [README.md](005_sampling/README.md)
- [client.py](005_sampling/client.py)
- [server.py](005_sampling/server.py)

### 006_transport_http
An HTTP transport demo for MCP interactions.

Key files:
- [README.md](006_transport_http/README.md)
- [main.py](006_transport_http/main.py)
- [index.html](006_transport_http/index.html)

### 007_note_book
A notebook-based study area covering Claude concepts and hands-on exercises.

Notebook topics:
- prompting
- thinking
- tools
- prompt grader evals
- chunking
- caching
- vectordb
- hybrid retrieval
- BM25
- embeddings
- images
- citations
- code execution
- text editor tool
- web search

Supporting files:
- [report.md](007_note_book/report.md)
- [metadata/Claude_Certified_Architect_Foundations_Certification_Exam_Guide.pdf](007_note_book/metadata/Claude_Certified_Architect_Foundations_Certification_Exam_Guide.pdf)

---

## Practice Exam Materials

### 000_Architect_Foundations_Certification_Exam
Community-built practice exam material for Claude Certified Architect Foundations.

Key files:
- [README.md](000_Architect_Foundations_Certification_Exam/README.md)
- [Claude Certification Exam.md](000_Architect_Foundations_Certification_Exam/Claude%20Certification%20Exam.md)
- [cert-exam.skill](000_Architect_Foundations_Certification_Exam/cert-exam.skill)

Exam focus:
- 77 scenario-based questions
- 5 domains
- interactive Claude Code skill for running the exam

---

## Supporting Package

### claude_agent_sdk
The Claude Agent SDK source, tests, examples, and release tooling.

Useful references:
- [README.md](claude_agent_sdk/README.md)
- [examples/quick_start.py](claude_agent_sdk/examples/quick_start.py)
- [tests/test_query.py](claude_agent_sdk/tests/test_query.py)

---

## Study Notes

### Additional Certification Resources
- https://claudecertificationguide.com/
- https://www.youtube.com/watch?v=VvKDoV39jAk&list=PLmiDJB5zE0KGwFtDCSqHfQG7SV6VeQ_31
- https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification

### Themes Covered Across the Folder
- MCP client/server patterns
- tool registration and invocation
- stdio, HTTP, and roots-based transport patterns
- interactive chat loops and command workflows
- notebook-driven prompt and retrieval exercises
- certification-style scenario practice

### Progress Tracker
- [ ] Review the 001-006 practice projects end to end
- [ ] Work through the 007 notebook exercises
- [ ] Complete the 000 practice exam material
- [ ] Revisit the Claude Agent SDK examples and tests

---

## Related Repository Files
- [requirements.txt](requirements.txt)
- [utils/litellm_client.py](utils/litellm_client.py)
- [readme.md](readme.md)

---

*Last Updated: 2026-06-29*
