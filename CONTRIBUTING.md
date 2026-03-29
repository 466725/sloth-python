# Contributing to Sloth Python

Thank you for your interest in contributing to **Sloth Python**! This document provides detailed guidelines to help you get started.

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read and follow our principles:
- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on constructive feedback
- Be patient and helpful with others

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Clone your fork locally
git clone https://github.com/466725/sloth-python.git
cd sloth-python

# Add upstream remote to sync with main repo
git remote add upstream https://github.com/466725/sloth-python.git
```

### 2. Setup Development Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.\.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

### 3. Create a Feature Branch

```bash
# Fetch latest changes from upstream
git fetch upstream
git checkout upstream/main -b feature/your-feature-name

# Examples of good branch names:
# feature/add-quicksort-algorithm
# fix/self-healing-timeout-issue
# docs/update-ai-generation-guide
# refactor/improve-config-loading
```

## Making Changes

### Code Style

We follow **PEP 8** with these conventions:

```python
# Always include type hints
def find_element(page: Page, selector: str) -> Element:
    """Brief description of what the function does.
    
    Longer explanation if needed, including examples of how to use it.
    
    Args:
        page: The Playwright page object
        selector: CSS selector string
        
    Returns:
        The found Element object
        
    Raises:
        TimeoutError: If element not found within timeout
    """
    # Implementation here
    pass

# Use descriptive variable names
user_credentials = {"username": "test", "password": "pass"}

# Add comments for complex logic
# Attempt primary selector, fall back to alternative
```

### What to Include in Your PR

**For Bug Fixes:**
- Description of the bug
- Steps to reproduce
- Root cause analysis (if known)
- Your fix with test cases

**For Features:**
- Clear description of the feature
- Use case and motivation
- Implementation approach
- Test coverage
- Documentation updates

**For Documentation:**
- What's being documented
- Why it's important
- Clear examples
- Links to related sections

### Testing Requirements

All changes must include appropriate test coverage:

```bash
# Run tests locally before submitting PR
pytest -m "unit or api"              # Quick smoke test
pytest --tb=short                    # Full pytest suite
python -m robot robot_demo/calculator/  # Robot tests

# For UI test changes
pytest -m ui --tb=short

# Generate coverage report (optional but helpful)
pytest --cov=algorithms --cov=utils
```

### Commit Message Guidelines

We use **conventional commits** for clear history:

```bash
# Format: type(scope): subject
# Examples:
git commit -m "feat(algorithms): add quicksort implementation"
git commit -m "fix(self-healing): handle timeout in element recovery"
git commit -m "docs(readme): improve AI generation section"
git commit -m "refactor(config): simplify environment variable loading"
git commit -m "test(unit): add csv_reader test cases"

# Keep commits focused and logical
# Each commit should represent one logical change
```

**Commit types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `refactor:` - Code refactoring without behavior change
- `test:` - Test additions or updates
- `chore:` - Build, dependencies, or tooling changes
- `perf:` - Performance improvements

## Submitting Changes

### Before You Submit

1. **Update your branch** with latest upstream:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run all tests locally**:
   ```bash
   pytest --tb=short
   python -m robot robot_demo/
   ```

3. **Format your code** (optional but recommended):
   ```bash
   # If you have ruff installed
   ruff format algorithms/ utils/ pytest_demo/
   ruff check --fix .
   ```

### Creating a Pull Request

1. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open a Pull Request** on GitHub with:
   - **Title**: Clear, concise description (e.g., "Add self-healing for signup page")
   - **Description**: Include:
     - What does this PR do?
     - Why is it needed?
     - How to test it?
     - Any breaking changes?
     - Related issue (e.g., `Fixes #42`)

3. **PR Template** (if provided):
   ```markdown
   ## Description
   Brief explanation of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation
   - [ ] Refactoring
   
   ## Testing
   - [ ] Unit tests pass
   - [ ] Integration tests pass
   - [ ] Manual testing performed
   
   ## Checklist
   - [ ] Code follows PEP 8
   - [ ] Type hints added
   - [ ] Docstrings updated
   - [ ] Tests added/updated
   - [ ] README updated if needed
   ```

## Areas for Contribution

### Algorithms
- Implement new algorithms from `algorithms/` directory
- Include docstrings and type hints
- Add unit tests in `pytest_demo/tests/unit/`
- Reference sources or papers if applicable

**Example:** Adding a new sorting algorithm:
```python
# algorithms/sorts/insertion_sort.py
def insertion_sort(arr: list[int]) -> list[int]:
    """Sort array using insertion sort algorithm.
    
    Time: O(n²) average and worst case, O(n) best case
    Space: O(1) in-place sorting
    """
    # Implementation
```

### Test Automation
- Add new Playwright UI tests in `pytest_demo/tests/ui/`
- Add Robot Framework test cases in `robot_demo/`
- Enhance test fixtures in `pytest_demo/conftest.py`
- Document test patterns and best practices

### Self-Healing Framework
- Improve locator detection algorithms
- Enhance DOM similarity matching
- Add support for new selector strategies
- Performance optimizations

### AI Test Generation
- Improve prompt engineering in `prompt_builder.py`
- Add support for new LLM models
- Enhance context collection in `mcp_context.py`
- Better error handling and fallbacks

### Documentation
- Improve README sections
- Add usage examples
- Create tutorials or guides
- Fix typos or unclear explanations

### CI/CD
- Enhance `.github/workflows/ci.yml`
- Add new test checks or reports
- Improve performance of CI runs

## Code Review Process

### What Reviewers Look For

1. **Code Quality**
   - Follows project conventions
   - Type hints and docstrings present
   - No code duplication
   - Clear variable/function names

2. **Testing**
   - Adequate test coverage
   - Tests are meaningful and not just stubbed
   - Edge cases considered

3. **Documentation**
   - Changes documented in docstrings
   - README or guides updated if needed
   - Complex logic has comments

4. **Performance**
   - No performance regressions
   - Efficient algorithms used
   - No unnecessary dependencies

### Responding to Feedback

- Be open to suggestions
- Ask for clarification if needed
- Make requested changes and push updates
- Don't resolve conversations until both agree

## Troubleshooting

### Common Issues

**My PR has conflicts**
```bash
# Update your branch from upstream
git fetch upstream
git rebase upstream/main

# If there are conflicts, resolve them, then:
git add .
git rebase --continue
git push origin feature/your-branch --force
```

**Tests pass locally but fail in CI**
- Check Python version in CI (currently 3.14)
- Verify all dependencies in `requirements.txt`
- Check for platform-specific issues (Windows/Linux/Mac)
- Review CI logs carefully

**How long until PR is reviewed?**
- We review PRs as time permits
- Critical bug fixes are prioritized
- Be patient and remind us if it's been > 2 weeks

## Questions?

- **GitHub Discussions** - Ask general questions
- **GitHub Issues** - Report bugs or suggest features
- **PR Comments** - Ask clarifying questions during review

## Thank You!

Your contributions make Sloth Python better for everyone. We appreciate your effort and look forward to working with you! 🙌

---

**Happy Contributing!**

