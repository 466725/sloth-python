# Security Policy

## Supported Scope

This project is maintained as an educational and reference repository for Python algorithms, test automation, AI-assisted testing, Playwright, Robot Framework, and Claude/MCP examples.

### Secrets and Environment Variables

- Never commit API keys, passwords, tokens, cookies, or private credentials.
- Store local secrets in `.env` files that are excluded from Git.
- Use GitHub Actions secrets or environment-level secrets for CI/CD.
- Rotate credentials immediately if they may have been exposed.

### Dependencies

- Keep dependencies current.
- Review dependency updates before merging them.
- Use tools such as `pip-audit`, `uv`, Dependabot, or GitHub security alerts to monitor known vulnerabilities.

### Test and Demo Data

- Use synthetic or non-sensitive data in examples, notebooks, fixtures, and screenshots.
- Avoid committing real customer data, production URLs with credentials, or internal system details.
- Prefer environment variables for configurable service endpoints and tokens.

---

Thank you for helping keep Sloth Python secure.
