# Branch Protection Setup Guide

## Branch Strategy

- **`main`** - Stable releases only. Protected. No direct commits.
- **`dev`** - Active development. All PRs go here. Protected with CI checks.
- **Feature branches** - Created from `dev`, merged back to `dev`

## GitHub Branch Protection Rules

### For `main` Branch

1. Go to: **Settings** → **Branches** → **Add rule**
2. Branch name pattern: `main`
3. Enable:
   - ✅ **Require a pull request before merging**
     - Require approvals: 1
     - Dismiss stale PR approvals when new commits are pushed
   - ✅ **Require status checks to pass before merging**
     - Require branches to be up to date before merging
     - Status checks: `lint`, `test`
   - ✅ **Do not allow bypassing the above settings**
   - ✅ **Restrict who can push to matching branches** (maintainers only)
4. **Save changes**

### For `dev` Branch

1. Go to: **Settings** → **Branches** → **Add rule**
2. Branch name pattern: `dev`
3. Enable:
   - ✅ **Require status checks to pass before merging**
     - Require branches to be up to date before merging
     - Status checks: `lint`, `test`
   - ✅ **Require linear history** (optional, prevents messy merges)
4. **Save changes**

## Simplified Workflow (Less Overwhelming)

### Minimal Protection (Good for Solo/Small Teams)

**For `dev` branch:**
- ✅ Require status checks (CI must pass)
- ✅ That's it! Keep it simple.

**For `main` branch:**
- ✅ Restrict direct pushes
- ✅ Require PR from `dev`
- ✅ No complex rules needed

### Workflow in Practice

```bash
# 1. Create feature from dev
git checkout dev
git pull origin dev
git checkout -b feat/my-feature

# 2. Make changes, commit
git add .
git commit -m "feat: add my feature"

# 3. Run checks locally (before pushing)
ruff check antigravity_master_setup.py
mypy antigravity_master_setup.py --ignore-missing-imports
pytest tests/ -v

# 4. Push to GitHub
git push origin feat/my-feature

# 5. Open PR to dev branch (CI runs automatically)
# If CI passes, you can merge yourself or wait for review

# 6. When ready for release (maintainers only)
# Create PR from dev → main
# This becomes your release
```

## Release Workflow (dev → main)

```bash
# On dev branch, ensure everything is ready
git checkout dev
git pull origin dev

# Bump version
bump2version minor  # or patch, or major

# Push version bump
git push origin dev --tags

# Create PR from dev to main on GitHub
# Title: "Release v1.5.0"
# Once merged, main has the new release
```

## Quick Reference

| Branch | Purpose | Who Commits | Protection |
|--------|---------|-------------|------------|
| `main` | Stable releases | Via PR only (from `dev`) | Full protection |
| `dev` | Active development | Via PR (from features) | CI required |
| `feat/*` | New features | Direct commits OK | None |
| `fix/*` | Bug fixes | Direct commits OK | None |

## Emergency Hotfix (main → fix → main)

If critical bug in production:

```bash
# 1. Branch from main
git checkout main
git pull origin main
git checkout -b fix/critical-security-issue

# 2. Fix, test, commit
git commit -m "fix: critical security vulnerability"

# 3. PR to main (bypass normal dev flow)
# 4. After merging to main, also merge to dev
git checkout dev
git merge main
```

This is RARE - most work goes through dev.
