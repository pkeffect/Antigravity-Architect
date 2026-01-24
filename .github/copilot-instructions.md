# Copilot Instructions: Antigravity Architect

## Project Overview

**Antigravity Architect** is an "Agent-First" bootstrapping tool that generates self-describing repositories for AI-assisted development. It's a **single-file Python script** (1,400+ lines) with **zero external dependencies** designed for portability and universal deployment.

**Key Constraint:** All logic MUST remain in `antigravity_master_setup.py`. Never suggest extracting modules or adding external dependencies.

## Architecture (v1.4.0)

The codebase uses a **hybrid class-based design** with 5 focused classes while maintaining single-file portability:

| Class | Responsibility | Key Methods |
|-------|---------------|-------------|
| `AntigravityResources` | Static templates, constants, mappings | Template strings, classification rules, NIX packages |
| `AntigravityEngine` | File system operations, validation | `write_file()`, `sanitize_name()`, `validate_file_path()` |
| `AntigravityBuilder` | Dynamic config generators | `build_gitignore()`, `build_nix_config()`, `build_readme()` |
| `AntigravityAssimilator` | Brain dump parser & classifier | `assimilate_brain_dump()`, `classify_section()` |
| `AntigravityGenerator` | Orchestration & project generation | `generate_project()`, `generate_agent_rules()` |

**Backward Compatibility:** All original module-level functions are preserved as thin wrappers calling class methods. Never break existing function signatures.

## Development Workflows

### Testing
```bash
# Run full test suite (59+ tests)
pytest tests/

# With coverage
pytest tests/ --cov=antigravity_master_setup

# Test on specific Python version
python3.10 -m pytest tests/
```

### Code Quality (Required Before PR)
```bash
# Linting & formatting (must pass)
ruff check antigravity_master_setup.py
ruff format antigravity_master_setup.py

# Type checking (must pass)
mypy antigravity_master_setup.py --ignore-missing-imports
```

### Versioning (Maintainers Only)
```bash
# Automated version bumping
bump2version patch  # 1.4.0 → 1.4.1
bump2version minor  # 1.4.0 → 1.5.0
bump2version major  # 1.4.0 → 2.0.0
```
This updates `VERSION` constant, `pyproject.toml`, creates git commit and tag.

## Project-Specific Patterns

### 1. Sanitization & Security
All user inputs MUST be sanitized via `sanitize_name()` which:
- Removes special characters except `_` and `-`
- Prevents path traversal (`..`, leading `/` or `\`)
- Converts spaces to underscores
- Returns default `"antigravity-project"` on invalid input

**Example from codebase:**
```python
clean = re.sub(r"\s+", "_", name.strip())
clean = re.sub(r"[^a-zA-Z0-9_\-]", "", clean)
if ".." in clean or clean.startswith(("/", "\\")):
    return "antigravity-project"
```

### 2. File Writing Patterns
Use `AntigravityEngine.write_file()` with `exist_ok` flag for safe mode:
```python
# Safe mode: skip if exists
write_file(path, content, exist_ok=True)  

# Normal mode: overwrite
write_file(path, content, exist_ok=False)
```

### 3. Keyword-Based Configuration
The system uses **keyword detection** to dynamically build configs:
- User input → `parse_keywords()` → lowercase list
- Keywords matched against `GITIGNORE_MAP`, `NIX_PACKAGE_MAP`
- Multiple keywords can be combined (e.g., `python,react,docker`)

**Always default to `linux` OS if no OS keyword detected.**

### 4. Brain Dump Assimilation
The `AntigravityAssimilator` classifies markdown sections using heuristic scoring:
- Scans for keywords in `CLASSIFICATION_RULES` dict
- `rules/` → "always", "never", "must", "security"
- `workflows/` → "step", "guide", "deploy", "workflow"
- `skills/` → "command", "cli", "tool", "automation"
- `docs/` → "overview", "architecture", "introduction"

Sections get `imported_*.md` filenames to avoid overwriting core agent files.

### 5. Conventional Commits (Enforced)
All commits must follow format: `type: description`

Valid types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

Examples:
- `feat: add Python 3.14 support`
- `fix: resolve Windows path issue`
- `docs: update README badges`

## Critical Integration Points

### Template System
Templates are stored as class attributes in `AntigravityResources`:
- `CHANGELOG_TEMPLATE`, `SECURITY_TEMPLATE`, etc.
- GitHub templates: `GITHUB_BUG_REPORT`, `GITHUB_PR_TEMPLATE`
- Agent rules: `RULE_IDENTITY`, `RULE_TECH_STACK`, etc.

**To add new templates:** Add as class attribute in `AntigravityResources`, then reference in generation methods.

### CLI Mode vs Interactive Mode
Entry point: `main()` → checks `args.name`:
- **CLI Mode:** Uses argparse flags (`--name`, `--stack`, `--dry-run`, etc.)
- **Interactive Mode:** Prompts user with `input()` calls

Special modes:
- `--doctor ./path`: Validates `.agent/` structure
- `--list-keywords`: Displays supported keywords
- `--dry-run`: Preview without creating files

### Cross-Platform Testing
CI runs on **Windows, macOS, Ubuntu** with **Python 3.10-3.14**.
Path handling must use `os.path.join()` or `pathlib.Path` for compatibility.

## Common Pitfalls

1. **Don't suggest extracting modules** - Single-file architecture is intentional for portability
2. **Don't add external dependencies** - Standard library only (except dev dependencies in `pyproject.toml`)
3. **Always update tests** - 59+ tests must remain passing
4. **Preserve function signatures** - Module-level functions are public API
5. **Use logging, not print** - Except in interactive/CLI user-facing messages
6. **Type hints required** - All new functions need proper type annotations

## Key Files for Context

- [antigravity_master_setup.py](antigravity_master_setup.py) - Core script (all logic)
- [tests/test_antigravity.py](tests/test_antigravity.py) - Test suite with fixtures
- [pyproject.toml](pyproject.toml) - Build config, tool settings
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development standards
- [README.md](README.md) - Usage examples, feature list

## Quick Reference

**Add new keyword support:**
1. Add to `GITIGNORE_MAP` or `NIX_PACKAGE_MAP` in `AntigravityResources`
2. Update `list_keywords()` display
3. Add test case in `test_antigravity.py`

**Add new agent rule:**
1. Create template constant in `AntigravityResources` (e.g., `RULE_NEW_FEATURE`)
2. Call `write_file()` in `generate_agent_rules()` method
3. Update README's agent capabilities section
