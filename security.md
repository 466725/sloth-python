# Security Policy

## Supported Scope

This project is maintained as an educational and reference repository for Python algorithms, test automation, AI-assisted testing, Playwright, Robot Framework, and Claude/MCP examples.

Security reports are welcome for issues that could affect users of this repository, including:

- Exposed secrets or unsafe handling of credentials
- Dependency or supply-chain vulnerabilities
- Unsafe file, network, browser, or subprocess behavior
- Insecure example code that could reasonably be copied into real projects
- CI/CD, test artifact, or configuration issues that could leak sensitive data

## Reporting a Vulnerability

Please do not report security vulnerabilities through public GitHub issues, pull requests, or discussions.

Use a private channel instead:

1. Use GitHub's **Report a vulnerability** option from the repository **Security** tab, if available.
2. Contact the maintainers privately if a maintainer contact method is listed in the repository or organization profile.

If no private contact method is available, open a public issue only to ask for a secure reporting channel. Do not include vulnerability details in that issue.

## What to Include

To help us validate and address the issue quickly, please include:

- A clear description of the vulnerability
- The affected file, package, workflow, or example
- Steps to reproduce the issue
- The expected and actual behavior
- Potential impact and realistic attack scenario
- Any relevant logs, screenshots, or proof of concept
- Suggested remediation, if you have one

Please keep proof-of-concept material minimal and avoid sharing secrets, destructive payloads, or exploit steps that are not necessary to demonstrate the issue.

## Response Process

We aim to handle reports using the following timeline:

| Stage | Target |
|---|---|
| Acknowledge receipt | Within 48 hours |
| Initial triage | Within 7 days |
| Remediation plan | Within 14 days |
| Fix or mitigation | Typically within 30 days, depending on severity and complexity |

After triage, we will share whether the report is accepted, needs more information, or is out of scope. For confirmed issues, we will coordinate disclosure timing and credit with the reporter where appropriate.

## Researcher Guidelines

When testing this project, please:

- Test only against your own fork, local clone, or authorized environment.
- Do not access, modify, delete, or exfiltrate data that does not belong to you.
- Do not attempt denial-of-service, spam, social engineering, or credential attacks.
- Do not publish vulnerability details before a fix or agreed disclosure date.
- Stop testing and report promptly if you encounter sensitive data.

Good-faith research that follows these guidelines is appreciated.

## Secure Usage Guidance

When using or extending this repository:

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

### AI and Browser Automation

- Review generated AI code before running or committing it.
- Avoid sending secrets, private data, or proprietary content to external models unless you are authorized to do so.
- Keep Playwright, Robot Framework, and browser automation tests scoped to approved targets.

## Security Advisories

Confirmed vulnerabilities may be documented through GitHub Security Advisories after a fix or mitigation is available.

## Previous Advisories

There are currently no published security advisories for this project.

---

Thank you for helping keep Sloth Python secure.
