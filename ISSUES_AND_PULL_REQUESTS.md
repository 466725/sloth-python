# Issues and Pull Requests

## Bug Report Template

When reporting a bug, please include:

```markdown
## Description
Brief description of the bug you encountered.

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should have happened?

## Actual Behavior
What actually happened?

## Environment
- Python version: 3.14
- OS: Windows 11 / Ubuntu 22.04 / macOS 13
- Framework: Pytest / Robot Framework / Playwright
- Other relevant info:

## Error Message / Logs
```
Paste full error message and stack trace here
```

## Additional Context
Any other information that might help us understand the issue?

## Possible Fix
Do you have any ideas for how to fix this?
```

## Feature Request Template

When suggesting a feature, please include:

```markdown
## Description
Clear description of the feature you want to see.

## Motivation
Why do you need this feature? What problem does it solve?

## Proposed Solution
How should this feature work? Any specific implementation details?

## Alternatives Considered
Have you considered other approaches? Why is your solution better?

## Example Usage
How would someone use this feature?

```python
# Show example code if applicable
```

## Additional Context
Any other information or links to related issues?
```

## Pull Request Template

When submitting code changes, please include:

```markdown
## Description
What changes are you making? Why are they needed?

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)

## Related Issues
Closes #(issue number)

## Changes Made
List the key changes:
- Change 1
- Change 2
- Change 3

## Testing
How have you tested these changes?
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing performed

## Test Coverage
- [ ] Added new test cases
- [ ] Updated existing test cases
- [ ] All tests passing

## Documentation
- [ ] Updated README if needed
- [ ] Added/updated docstrings
- [ ] Updated type hints
- [ ] Added code comments for complex logic

## Screenshots (if applicable)
Paste screenshots for UI changes

## Checklist
- [ ] Code follows PEP 8 style guidelines
- [ ] Type hints included where applicable
- [ ] Docstrings added/updated
- [ ] No new warnings generated
- [ ] No breaking changes
- [ ] Commit messages follow conventional commits
- [ ] Ready for review
```

## GitHub Labels

We use the following labels to organize issues:

### Priority
- `priority/critical` - Critical, needs immediate attention
- `priority/high` - Important, should be addressed soon
- `priority/medium` - Standard priority
- `priority/low` - Nice to have, can wait

### Type
- `type/bug` - Something isn't working
- `type/feature` - New functionality
- `type/enhancement` - Improvement to existing feature
- `type/documentation` - Documentation updates
- `type/question` - Question or discussion

### Area
- `area/algorithms` - Related to algorithms directory
- `area/test-automation` - Pytest or Robot Framework tests
- `area/self-healing` - Self-healing locator framework
- `area/ai-generation` - AI test script generation
- `area/ci-cd` - GitHub Actions or CI/CD
- `area/config` - Configuration and environment variables

### Status
- `status/help-wanted` - Community help needed
- `status/in-progress` - Currently being worked on
- `status/blocked` - Waiting for something else
- `status/review-needed` - Awaiting code review
- `status/waiting-feedback` - Waiting for more information

### Special
- `good-first-issue` - Good for new contributors
- `duplicate` - Duplicate of another issue
- `wontfix` - Will not be fixed
- `invalid` - Not valid or out of scope

## Discussion Guidelines

When participating in discussions:

1. **Stay on topic** - Keep discussions focused on the subject
2. **Search first** - Check if your question was already answered
3. **Be clear** - Provide enough context for others to understand
4. **Provide examples** - Use code blocks for clarity
5. **Be respectful** - Follow the Code of Conduct
6. **No spam** - Avoid advertising or off-topic content

## Getting Help

- **Questions** → Use GitHub Discussions
- **Bug reports** → Open an Issue with `type/bug` label
- **Feature requests** → Open an Issue with `type/feature` label
- **Need help?** → Label with `status/help-wanted` and `good-first-issue` if appropriate

## Issue Lifecycle

1. **Created** - Issue opened with relevant details
2. **Triage** - Maintainer labels and prioritizes
3. **Discussion** - Community discusses approach
4. **Implementation** - Someone works on a fix or feature
5. **Review** - Code is reviewed and tested
6. **Merged** - Changes are merged to main
7. **Closed** - Issue is resolved and closed

---

Thank you for helping improve Sloth Python! 🚀

