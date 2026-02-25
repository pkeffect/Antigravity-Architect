# 🤝 Contributing to Antigravity Architect

Thank you for your interest in contributing! This guide will help you get started.

---

## 📋 Table of Contents

- [Getting Started](#-getting-started)
- [Development Workflow](#-development-workflow)
- [Code Standards](#-code-standards)
- [Submitting Changes](#-submitting-changes)
- [Versioning](#-versioning)
- [Need Help](#-need-help)

---

## 🚀 Getting Started

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/antigravity-architect.git
cd antigravity-architect
git checkout main  # Work on main branch
```

### 2. Install Dev Dependencies

```bash
pip install -e .[dev]
```

### 3. Run the Test Suite

```bash
pytest tests/
```

---

## 🛠️ Development Workflow

This project adheres to **"Agent-First"** principles.

### Core Rules

1. **Modular Architecture** - Maintain the package structure in `src/antigravity_architect/`
2. **Zero External Dependencies** - Standard library only
3. **Backward Compatibility** - Don't break existing function signatures

### Quality Checks

```bash
# Linting & Formatting (required)
ruff check src/antigravity_architect/
ruff format src/antigravity_architect/

# Type Checking (required)
mypy src/antigravity_architect/

# All Tests (required)
pytest tests/
```

All checks must pass before submitting a PR.

---

## 📝 Code Standards

### Style

- **Formatter:** Ruff (Black-compatible)
- **Line Length:** 120 characters
- **Quotes:** Double quotes
- **Type Hints:** Required for all new functions

### Architecture

The codebase uses a hybrid class-based architecture:

| Class | Purpose |
| :--- | :--- |
| `AntigravityResources` | Constants, templates, mappings |
| `AntigravityEngine` | File operations, validation |
| `AntigravityBuilder` | Dynamic config generation |
| `AntigravityAssimilator` | Brain dump parsing |
| `AntigravityGenerator` | Project generation orchestration |

Add new features to the appropriate class.

---

## 🔄 Submitting Changes

### 1. Create a Branch

```bash
# Make sure you're on main branch first
git checkout main
git pull origin main

# Create your feature branch from main
git checkout -b feat/my-new-feature
```

### 2. Make Your Changes

- Follow the code standards above
- Add tests for new functionality
- Update documentation if needed

### 3. Commit with Conventional Commits

```bash
git commit -m "feat: add new protocol v3 feature"
git commit -m "fix: resolve path issue on Windows"
git commit -m "docs: update README badges"
```

**Commit Types:**

| Type | Description |
| :--- | :--- |
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `test` | Adding or updating tests |
| `chore` | Maintenance tasks |

### 4. Push and Create PR

```bash
git push origin feat/my-new-feature
```

**Important:** Open your Pull Request against the `main` branch.

All development happens on feature branches that are merged into `main` after passing CI and security checks.

---

## 🏷️ Versioning

We use [Semantic Versioning](https://semver.org/) and `bump2version` for automated version management.

### Version Bumping (Maintainers Only)

```bash
# Patch release (3.0.0 → 3.0.1) - Bug fixes
bump2version patch

# Minor release (3.0.0 → 3.1.0) - New features
bump2version minor

# Major release (3.0.0 → 4.0.0) - Breaking changes
bump2version major
```

This automatically updates:

- `src/antigravity_architect/resources/constants.py` (VERSION constant)
- `pyproject.toml` (version field)
- `README.md` (version badge)
- Creates a git commit and tag

---

## ❓ Need Help

- **Questions?** Open a [Question Issue](https://github.com/pkeffect/antigravity-architect/issues/new?template=question.md)
- **Bug Found?** Open a [Bug Report](https://github.com/pkeffect/antigravity-architect/issues/new?template=bug_report.md)
- **Feature Idea?** Open a [Feature Request](https://github.com/pkeffect/antigravity-architect/issues/new?template=feature_request.md)

---

## 🙏 Thank You

Every contribution, no matter how small, helps make Antigravity Architect better. We appreciate your time and effort!
