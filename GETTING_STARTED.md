# Getting Started as a Contributor

Welcome to Sloth Python! 👋 This guide will help you make your first contribution.

## Prerequisites

Before you start, make sure you have:
- A GitHub account
- Git installed on your machine
- Python 3.12+ installed
- Basic familiarity with Git and Python

## Step-by-Step Guide for Your First Contribution

### 1. Fork the Repository

1. Go to [Sloth Python Repository](https://github.com/yourusername/sloth-python)
2. Click the **Fork** button in the top-right corner
3. This creates your own copy of the repository

### 2. Clone Your Fork

```bash
# Replace YOUR_USERNAME with your GitHub username
git clone https://github.com/YOUR_USERNAME/sloth-python.git
cd sloth-python
```

### 3. Set Up Development Environment

```bash
# Create a virtual environment
python -m venv .venv

# Activate it (Windows)
.\.venv\Scripts\activate

# Activate it (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

### 4. Create a Feature Branch

```bash
# First, sync with the latest changes
git fetch origin
git checkout -b feature/your-feature-name

# Good branch names:
# feature/add-bubble-sort
# fix/typo-in-readme
# docs/improve-setup-guide
```

### 5. Make Your Changes

Edit files following these guidelines:
- PEP 8 style (use spaces, not tabs)
- Add type hints to functions
- Write docstrings for public functions
- Keep commits focused and logical

Example:

```python
def calculate_sum(numbers: list[int]) -> int:
    """Calculate the sum of all numbers in a list.
    
    Args:
        numbers: List of integers to sum
        
    Returns:
        The sum of all numbers
        
    Example:
        >>> calculate_sum([1, 2, 3])
        6
    """
    return sum(numbers)
```

### 6. Test Your Changes

```bash
# Run tests related to your changes
pytest -q

# Run a specific test file
pytest pytest_demo/tests/unit/test_csv_reader.py -q

# Run Robot Framework tests (if applicable)
python -m robot robot_demo/calculator/
```

### 7. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with a clear message
git commit -m "feat: add bubble sort algorithm"
git commit -m "fix: correct typo in documentation"
git commit -m "docs: improve installation instructions"

# Format: type(scope): description
# Types: feat, fix, docs, refactor, test, chore, perf
```

### 8. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 9. Create a Pull Request

1. Go to your fork on GitHub
2. Click **Compare & pull request**
3. Fill in the PR description:
   - What does this change do?
   - Why is it needed?
   - Any related issues?
4. Click **Create pull request**

## Getting Help

If you get stuck:

1. **Check the docs** - Read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines
2. **Search existing issues** - Your question might already be answered
3. **Ask in Discussions** - Use GitHub Discussions for questions
4. **Comment on your PR** - Ask maintainers for help if needed

## Common Scenarios

### I want to fix a typo

1. Create a branch: `git checkout -b fix/typo-in-readme`
2. Edit the file with the typo
3. Commit: `git commit -m "fix: correct spelling in README"`
4. Push and create a PR

### I want to add a new algorithm

1. Create a branch: `git checkout -b feature/add-merge-sort`
2. Add your algorithm in `algorithms/sorts/merge_sort.py`
3. Add a docstring and type hints
4. Create tests in `pytest_demo/tests/unit/test_merge_sort.py`
5. Run tests: `pytest pytest_demo/tests/unit/test_merge_sort.py`
6. Commit and push
7. Create a PR describing your algorithm

### I found a bug

1. Create a branch: `git checkout -b fix/issue-description`
2. Fix the bug
3. Add a test that reproduces the bug (to prevent regression)
4. Ensure all tests pass
5. Commit: `git commit -m "fix: describe what was fixed"`
6. Create a PR with steps to reproduce and how you fixed it

### I want to improve documentation

1. Create a branch: `git checkout -b docs/improve-section`
2. Edit the relevant `.md` files
3. Check that links and formatting work
4. Commit: `git commit -m "docs: improve X section"`
5. Create a PR

## Best Practices

✅ **Do:**
- Keep PRs focused on one change
- Write clear commit messages
- Test your changes before submitting
- Ask questions if confused
- Follow the Code of Conduct

❌ **Don't:**
- Mix multiple unrelated changes in one PR
- Commit directly to main (use branches!)
- Push sensitive data (API keys, passwords)
- Make large refactors without discussion
- Use profanity or disrespect

## How Your PR Gets Reviewed

1. **Automated checks** - CI runs tests and checks code style
2. **Code review** - A maintainer reviews your changes
3. **Discussion** - You might be asked to make changes
4. **Approval** - Once approved, your PR is merged!

## After Your PR is Merged

Congratulations! 🎉

- Your code is now part of the project
- You'll be listed as a contributor
- Your name appears in the project history
- Feel free to take on more contributions!

## Common Git Commands

```bash
# Update your branch with latest changes
git fetch origin
git rebase origin/main

# Undo last commit (keep changes)
git reset --soft HEAD~1

# See what changed
git diff

# Check your branch status
git status

# See commit history
git log --oneline
```

## Questions?

- **GitHub Discussions** - For questions and ideas
- **GitHub Issues** - For bug reports and feature requests
- **Comment on PR** - Ask maintainers directly on your PR
- **Read Contributing Guide** - For detailed technical guidelines

---

**We're excited to have you contribute to Sloth Python!** 🚀

Even small contributions like fixing typos or improving documentation are valuable and appreciated. Thank you for helping make this project better!

