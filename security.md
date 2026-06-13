# Security Policy

## Reporting a Vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.**

Instead, please report security issues responsibly by:

1. **Email** - Contact the maintainers directly (if contact info is provided)
2. **GitHub Security Advisory** - Use the "Report a vulnerability" option under Security tab
3. **Private Message** - Reach out to maintainers via private channels if available

## What to Include in a Security Report

When reporting a vulnerability, please provide:

- **Description** - Clear explanation of the security issue
- **Affected Versions** - Which versions are affected?
- **Steps to Reproduce** - How can we verify the vulnerability?
- **Impact** - What's the potential impact if exploited?
- **Suggested Fix** - Do you have any ideas for fixing it?
- **Proof of Concept** - Example code that demonstrates the issue (if safe)

## Response Timeline

- **Acknowledgment** - We'll acknowledge receipt within 48 hours
- **Investigation** - We'll work to understand and reproduce the issue
- **Fix** - We aim to release a fix within 30 days
- **Disclosure** - We'll coordinate a responsible disclosure timeline with you

## Security Best Practices

When using Sloth Python:

### Environment Variables
- **Never commit secrets** (API keys, passwords, tokens) to the repository
- Use `.env` files (git-ignored) for local development
- Use GitHub Secrets for CI/CD pipelines
- Rotate secrets regularly

### Dependencies
- Keep dependencies updated: `pip install --upgrade -r requirements.txt`
- Monitor for security advisories: `pip-audit` or similar tools
- Review changelogs before major updates

### Test Data
- Use non-sensitive test data in examples
- Never hardcode credentials in test files
- Use environment variables for sensitive configurations

## Known Issues

There are currently no known security vulnerabilities in this project.

## Security Advisories

Security advisories will be published in the GitHub Security section once fixes are released.

## Previous Advisories

None at this time.

---

Thank you for helping keep Sloth Python secure! 🔒

