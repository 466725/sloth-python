# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
<!-- New features -->

### Changed
<!-- Changes in existing functionality -->

### Deprecated
<!-- Soon-to-be removed features -->

### Removed
<!-- Removed features -->

### Fixed
<!-- Bug fixes -->

### Security
<!-- In case of vulnerabilities -->

---

## [0.1.0] - 2026-03-22

### Added
- Initial public release of Sloth Python
- Advanced test automation with Playwright and Robot Framework
- Self-healing locator framework for UI testing
- AI-powered test script generation with MCP support
- Comprehensive algorithm library (data structures, ML, sorting, searching)
- Production-ready CI/CD with GitHub Actions
- Professional documentation and contributing guides

### Features in Initial Release
- **Test Automation**: pytest + Playwright integration with custom fixtures
- **Robot Framework**: Keyword-driven testing with custom libraries
- **Self-Healing**: Automated locator repair with DOM similarity matching
- **AI Generation**: Natural-language to Playwright test script generation
- **Algorithms**: 50+ algorithm implementations with tests
- **Configuration**: Centralized settings with environment variable support
- **CI/CD**: Smoke test + nightly regression workflows

---

## Guidelines for Contributors

When adding entries to the changelog:

1. **Use standard categories** - Added, Changed, Deprecated, Removed, Fixed, Security
2. **Link to PRs** - Reference PR numbers: `([#123](../../pull/123))`
3. **Group by version** - Each release gets its own section
4. **Keep it clear** - Write for end users, not just developers

### Example Changelog Entry

```markdown
## [1.0.0] - 2026-06-15

### Added
- New feature X for improving test performance ([#234](../../pull/234))
- Documentation for AI generation workflow

### Changed
- Updated Playwright dependency to v1.50.0
- Improved self-healing algorithm accuracy

### Fixed
- Bug where cookie banner timeout was not respected ([#245](../../pull/245))
- Incorrect path resolution in Windows environments

### Security
- Updated OpenAI client to address security advisory CVE-2024-XXXXX
```

### Dates Format

Use ISO 8601 format: `YYYY-MM-DD`

### Version Numbering

We follow Semantic Versioning:
- `MAJOR.MINOR.PATCH` (e.g., `1.2.3`)
- `MAJOR` - Breaking changes
- `MINOR` - New features (backward compatible)
- `PATCH` - Bug fixes

---

**Note:** The changelog is maintained by project maintainers with input from contributors. When submitting a PR, you don't need to update the changelog - maintainers will do that during release planning.

