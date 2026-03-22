# Placeholder Update Guide

This guide lists all occurrences of `yourusername` and other placeholders that need to be replaced before public release.

## 🔍 Search and Replace Guide

### Step 1: Replace Repository Username

**Search**: `yourusername`
**Replace**: Your actual GitHub username (e.g., `johnsmith`)

**Files to update:**
1. README.md - 3 occurrences
2. CONTRIBUTING.md - 2 occurrences
3. SECURITY.md - 1 occurrence
4. ISSUES_AND_PULL_REQUESTS.md - 1 occurrence
5. .github/dependabot.yml - 1 occurrence
6. .github/workflows/welcome.yml - 2 occurrences
7. .github/ISSUE_TEMPLATE/question.md - 1 occurrence

### Step 2: Replace Sponsorship Handles (Optional)

**File**: `.github/FUNDING.yml`

Replace:
- `your-ko-fi-handle` with your Ko-fi username (if using)
- `your-bmc-handle` with your Buy Me a Coffee username (if using)

Or delete the lines if not setting up sponsorship.

### Step 3: Configure Security Contact (Optional)

**File**: `SECURITY.md`

Add your email address for security vulnerability reports in the "Email" section.

---

## 🔧 Detailed Placeholder Locations

### README.md

**Location 1** - Clone instruction
```markdown
git clone https://github.com/yourusername/sloth-python.git
```
Replace with:
```markdown
git clone https://github.com/YOUR_GITHUB_USERNAME/sloth-python.git
```

**Location 2** - SSH alternative
```bash
git clone git@github.com:yourusername/sloth-python.git
```
Replace with:
```bash
git clone git@github.com:YOUR_GITHUB_USERNAME/sloth-python.git
```

**Location 3** - CI badge
```markdown
[![CI Status](https://github.com/yourusername/sloth-python/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/sloth-python/actions)
```
Replace with:
```markdown
[![CI Status](https://github.com/YOUR_GITHUB_USERNAME/sloth-python/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_GITHUB_USERNAME/sloth-python/actions)
```

### CONTRIBUTING.md

**Location 1** - Fork instruction
```markdown
# Fork the repository on GitHub
# Clone your fork locally
git clone https://github.com/YOUR_USERNAME/sloth-python.git
```
This is already shown as `YOUR_USERNAME` - good!

**Location 2** - Upstream remote
```bash
git remote add upstream https://github.com/yourusername/sloth-python.git
```
Replace with:
```bash
git remote add upstream https://github.com/YOUR_GITHUB_USERNAME/sloth-python.git
```

### SECURITY.md

**Location 1** - GitHub security advisory
```markdown
- **[GitHub Security Advisory](https://github.com/yourusername/sloth-python/security)** - Report a vulnerability
```
Replace with:
```markdown
- **[GitHub Security Advisory](https://github.com/YOUR_GITHUB_USERNAME/sloth-python/security)** - Report a vulnerability
```

### ISSUES_AND_PULL_REQUESTS.md

**Location 1** - Discussion links
```markdown
For general discussions and conversations, consider using [GitHub Discussions](https://github.com/yourusername/sloth-python/discussions) instead!
```
Replace with:
```markdown
For general discussions and conversations, consider using [GitHub Discussions](https://github.com/YOUR_GITHUB_USERNAME/sloth-python/discussions) instead!
```

### .github/dependabot.yml

**Location 1** - Reviewer assignment
```yaml
reviewers:
  - "yourusername"
```
Replace with:
```yaml
reviewers:
  - "YOUR_GITHUB_USERNAME"
```

### .github/workflows/welcome.yml

**Location 1** - Issue message link
```markdown
- Read the [Contributing Guide](CONTRIBUTING.md) for more details

- Discuss in our [Discussions](https://github.com/yourusername/sloth-python/discussions).
```
Replace with:
```markdown
- Read the [Contributing Guide](CONTRIBUTING.md) for more details

- Discuss in our [Discussions](https://github.com/YOUR_GITHUB_USERNAME/sloth-python/discussions).
```

### .github/FUNDING.yml

**Optional** - Sponsorship configuration
```yaml
# GitHub Sponsors (if you set up a profile)
# github: yourusername

# Ko-fi - Support the project
ko_fi: your-ko-fi-handle

# Buy Me a Coffee
buy_me_a_coffee: your-bmc-handle
```

Options:
- If using GitHub Sponsors: Uncomment and replace `yourusername`
- If using Ko-fi: Replace `your-ko-fi-handle` with your handle
- If using Buy Me a Coffee: Replace `your-bmc-handle` with your handle
- If not using: Delete the lines

### .github/ISSUE_TEMPLATE/question.md

**Location 1** - Discussion link
```markdown
Note:** For general discussions and conversations, consider using [GitHub Discussions](https://github.com/yourusername/sloth-python/discussions) instead!
```
Replace with:
```markdown
**Note:** For general discussions and conversations, consider using [GitHub Discussions](https://github.com/YOUR_GITHUB_USERNAME/sloth-python/discussions) instead!
```

---

## 🔄 Quick Search and Replace (in IDE)

### Using Find and Replace

**In most IDEs (VS Code, PyCharm):**

1. Open Find and Replace (`Ctrl+H` or `Cmd+H`)
2. Find: `yourusername`
3. Replace with: `YOUR_GITHUB_USERNAME`
4. Click "Replace All"

**In PowerShell (command line):**

```powershell
# Dry run - see what would be replaced
Get-ChildItem -Path . -Recurse -Include "*.md", "*.yml", "*.yaml" | 
  Select-String "yourusername" | 
  Select-Object Path, Line

# Actually replace (be careful!)
Get-ChildItem -Path . -Recurse -Include "*.md", "*.yml", "*.yaml" | 
  ForEach-Object {
    (Get-Content $_) -replace "yourusername", "YOUR_GITHUB_USERNAME" | 
    Set-Content $_
  }
```

**In Bash/Shell:**

```bash
# Dry run
grep -r "yourusername" . --include="*.md" --include="*.yml"

# Actually replace (be careful!)
find . -type f \( -name "*.md" -o -name "*.yml" \) -exec sed -i 's/yourusername/YOUR_GITHUB_USERNAME/g' {} \;
```

---

## ✅ Verification After Update

```bash
# Verify all replacements were made
grep -r "yourusername" . --include="*.md" --include="*.yml"

# Should return: (no results)

# Check a few critical files
grep "YOUR_GITHUB_USERNAME" README.md
grep "YOUR_GITHUB_USERNAME" CONTRIBUTING.md
grep "YOUR_GITHUB_USERNAME" .github/dependabot.yml

# All should return matches showing your username
```

---

## 📝 Checklist

- [ ] Replace all `yourusername` with actual GitHub username
- [ ] Update sponsorship handles in `.github/FUNDING.yml` (or delete lines if not using)
- [ ] Add security contact email to `SECURITY.md` (optional)
- [ ] Verify replacements with grep/search
- [ ] Test clone command works
- [ ] Review README links are valid
- [ ] Commit changes: `git commit -m "docs: update GitHub URLs for public release"`
- [ ] Push to GitHub

---

**After updating**, your repository will be ready for public release! 🚀

