#!/usr/bin/env python3
"""
Antigravity Architect: Master Edition

A universal "Agent-First" bootstrapping tool that creates self-describing
repositories for AI-assisted development. Generates project scaffolding with
embedded rules, workflows, skills, and memory for AI agents.

Designed for Google Antigravity, Project IDX, Gemini Code Assist, and VS Code.

Usage:
    python antigravity_master_setup.py                      # Interactive mode
    python antigravity_master_setup.py --name my-project    # CLI mode
    python antigravity_master_setup.py --doctor ./project   # Validate project
    python antigravity_master_setup.py --list-keywords      # Show supported keywords

Author: pkeffect
License: MIT
"""

from __future__ import annotations

import argparse
import logging
import os
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path

VERSION = "1.4.3"

# ==============================================================================
# 1. KNOWLEDGE BASE & CONFIGURATION
# ==============================================================================


class AntigravityResources:
    """
    Static resource container for all templates, mappings, and constants.

    This class serves as the centralized knowledge base for the Antigravity
    Architect, containing all configuration data, templates, and mapping rules
    needed for project generation.
    """

    # Core Constants
    VERSION = VERSION
    AGENT_DIR = ".agent"

    # Filename Constants
    GITIGNORE_FILE = ".gitignore"
    README_FILE = "README.md"
    DEVCONTAINER_DIR = ".devcontainer"
    DEVCONTAINER_FILE = "devcontainer.json"
    IDX_DIR = ".idx"
    NIX_FILE = "dev.nix"
    ENV_EXAMPLE_FILE = ".env.example"
    LICENSE_FILE = "LICENSE"
    CHANGELOG_FILE = "CHANGELOG.md"
    CONTRIBUTING_FILE = "CONTRIBUTING.md"
    AUDIT_FILE = "AUDIT.md"
    SECURITY_FILE = "SECURITY.md"
    CODE_OF_CONDUCT_FILE = "CODE_OF_CONDUCT.md"
    BOOTSTRAP_FILE = "BOOTSTRAP_INSTRUCTIONS.md"

    # UI Constants
    SEPARATOR = "=========================================="

    # A. Standard Gitignore Blocks (Universal + Language Specific)
    BASE_GITIGNORE = """
# --- Universal ---
.DS_Store
Thumbs.db
*~
*.swp
*.swo
.env
.env.*
!.env.example

# --- Agent / AI (Full Privacy) ---
.agent/
context/
antigravity_setup.log
"""

    GITIGNORE_MAP: dict[str, str] = {
        "python": "\n# --- Python ---\n__pycache__/\n*.pyc\nvenv/\n.venv/\n.pytest_cache/\n.mypy_cache/\n.ruff_cache/\n*.egg-info/\n",
        "node": "\n# --- Node/JS ---\nnode_modules/\ndist/\nbuild/\ncoverage/\n.npm/\n.eslintcache\n.yarn-integrity\n",
        "rust": "\n# --- Rust ---\n/target\nCargo.lock\n**/*.rs.bk\n",
        "go": "\n# --- Go ---\n/bin/\n/pkg/\n/dist/\n",
        "java": "\n# --- Java ---\n*.class\n*.jar\n*.war\nbuild/\n.gradle/\n",
        "php": "\n# --- PHP ---\n/vendor/\n.phpunit.result.cache\n",
        "ruby": "\n# --- Ruby ---\n/.bundle/\n/vendor/bundle/\n",
        "docker": "\n# --- Docker ---\n.docker/\n",
        "postgres": "",
        "react": "\n# --- React ---\nbuild/\n.env.local\n",
        "nextjs": "\n# --- NextJS ---\n.next/\nout/\n",
        "django": "\n# --- Django ---\n*.log\nlocal_settings.py\ndb.sqlite3\nmedia/\nstaticfiles/\n",
        "flask": "\n# --- Flask ---\ninstance/\n.webassets-cache\n",
        "macos": "\n# --- macOS ---\n.DS_Store\n.AppleDouble\n",
        "windows": "\n# --- Windows ---\nThumbs.db\nehthumbs.db\n*.exe\n*.dll\n",
        "linux": "\n# --- Linux ---\n*~\n.fuse_hidden*\n",
        "vscode": "\n# --- VS Code ---\n.vscode/\n",
        "idea": "\n# ---JetBrains ---\n.idea/\n*.iml\n",
    }

    # B. Nix Packages (For Google Project IDX / Cloud Environments)
    NIX_PACKAGE_MAP: dict[str, list[str]] = {
        "python": ["pkgs.python312", "pkgs.python312Packages.pip", "pkgs.ruff", "pkgs.python312Packages.virtualenv"],
        "node": ["pkgs.nodejs_20", "pkgs.nodePackages.nodemon", "pkgs.nodePackages.typescript"],
        "rust": ["pkgs.cargo", "pkgs.rustc", "pkgs.rustfmt"],
        "go": ["pkgs.go", "pkgs.gopls"],
        "java": ["pkgs.jdk17", "pkgs.maven"],
        "php": ["pkgs.php", "pkgs.php82Packages.composer"],
        "ruby": ["pkgs.ruby"],
        "docker": ["pkgs.docker", "pkgs.docker-compose"],
        "sql": ["pkgs.sqlite", "pkgs.postgresql"],
    }

    # C. Heuristic Classification Keywords
    CLASSIFICATION_RULES: dict[str, list[str]] = {
        "rules": [
            "always",
            "never",
            "must",
            "style",
            "convention",
            "standard",
            "protocol",
            "policy",
            "lint",
            "formatting",
            "security",
        ],
        "workflows": [
            "step",
            "guide",
            "process",
            "workflow",
            "how-to",
            "deploy",
            "setup",
            "run",
            "execution",
            "plan",
            "roadmap",
        ],
        "skills": [
            "command",
            "cli",
            "tool",
            "usage",
            "utility",
            "script",
            "automation",
            "flags",
            "arguments",
            "terminal",
        ],
        "docs": ["overview", "architecture", "introduction", "background", "context", "diagram", "concept", "summary"],
    }

    # D. Template Definitions for Generated Files
    CHANGELOG_TEMPLATE = """# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
- Initial release
"""

    CONTRIBUTING_TEMPLATE = """# Contributing to the Project

## Getting Started
1. Clone the repo
2. Install dependencies
3. Run tests

## Workflow
- Use Conventional Commits
- Create feature branches
- Submit PRs for review
"""

    AUDIT_TEMPLATE = """# Security & Quality Audit Log

| Date | Auditor | Score | Notes |
|------|---------|-------|-------|
| TBA  | System  | -/100 | Initial Generation |
"""

    SECURITY_TEMPLATE = """# Security Policy

## Supported Versions

The following versions of this project are currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0.x | :x:                |

## Reporting a Vulnerability

Please report security vulnerabilities by opening a private issue or contacting the maintainers directly.
"""

    CODE_OF_CONDUCT_TEMPLATE = """# Contributor Covenant Code of Conduct

## Our Pledge

We as members, contributors, and leaders pledge to make participation in our community a harassment-free experience for everyone, regardless of age, body size, visible or invisible disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.
"""

    # GitHub Templates - Issue Templates, PR Template, FUNDING
    GITHUB_BUG_REPORT = """---
name: 🐛 Bug Report
about: Report a bug or unexpected behavior
title: "[BUG] "
labels: bug
assignees: ''
---

## 🐛 Bug Description
<!-- A clear description of what the bug is. -->

## 📋 Steps to Reproduce
1. Run `...`
2. Enter '...'
3. See error

## ✅ Expected Behavior
<!-- What you expected to happen. -->

## ❌ Actual Behavior
<!-- What actually happened. -->

## 🖥️ Environment
- **OS:** <!-- e.g., Windows 11, macOS, Ubuntu 22.04 -->
- **Python Version:** <!-- e.g., 3.12 -->

## 📜 Error Output
```
[Paste error here]
```
"""

    GITHUB_FEATURE_REQUEST = """---
name: ✨ Feature Request
about: Suggest a new feature or enhancement
title: "[FEATURE] "
labels: enhancement
assignees: ''
---

## ✨ Feature Description
<!-- A clear description of the feature you'd like. -->

## 🎯 Problem Statement
<!-- What problem does this feature solve? -->

## 💡 Proposed Solution
<!-- Describe how you envision this feature working. -->

## 🔄 Alternatives Considered
<!-- Any alternative solutions or workarounds? -->

## 📋 Checklist
- [ ] I have searched existing issues to ensure this is not a duplicate
"""

    GITHUB_QUESTION = """---
name: ❓ Question
about: Ask a question about usage
title: "[QUESTION] "
labels: question
assignees: ''
---

## ❓ Question
<!-- What would you like to know? -->

## 📋 Context
<!-- What are you trying to accomplish? -->

## 🔍 What I've Tried
<!-- Have you checked the docs? Tried anything? -->
"""

    GITHUB_PR_TEMPLATE = """## 📋 Description
<!-- Brief summary of the changes in this PR. -->

## 🔗 Related Issue
<!-- Link to related issue: Closes #123 -->

## 🏷️ Type of Change
- [ ] 🐛 Bug fix
- [ ] ✨ New feature
- [ ] 💥 Breaking change
- [ ] 📚 Documentation update

## ✅ Checklist
- [ ] My code follows the project's coding style
- [ ] I have added/updated tests for my changes
- [ ] All tests pass
- [ ] I have updated documentation (if applicable)
- [ ] My commits follow Conventional Commits

## 🧪 How Has This Been Tested?
<!-- Describe how you verified your changes. -->
"""

    GITHUB_FUNDING = """# Funding links
# github: [username]
# ko_fi:
# patreon:
# open_collective:
# custom: ["https://example.com"]
"""

    GITHUB_ISSUE_CONFIG = """blank_issues_enabled: false
contact_links:
  - name: 📚 Documentation
    url: https://github.com/{owner}/{repo}#readme
    about: Check the README for usage instructions
"""

    GITHUB_COPILOT_INSTRUCTIONS = """# GitHub Copilot Instructions

## Project Context

This project uses **{tech_stack}** as its core technology stack. All code should follow the conventions and patterns established in the existing codebase.

## Development Workflow

### Before Making Changes
1. Check `docs/imported/` for project-specific documentation
2. Review `context/raw/` for original specifications
3. Consult `.agent/rules/` for coding standards and conventions
4. Read `CONTRIBUTING.md` for contribution guidelines

### Testing
```bash
# Run tests before committing
# [Add your test command here]
```

### Code Quality
```bash
# Lint and format code
# [Add your linting commands here]
```

## Project-Specific Patterns

### File Organization
- Source code: `src/`
- Tests: `tests/`
- Documentation: `docs/`
- Configuration: Root directory

### Coding Standards
1. **Security First**: Never commit secrets, API keys, or credentials
   - Use `.env` for environment variables
   - Reference `.env.example` for required variables
2. **Type Safety**: Use type hints/annotations where applicable
3. **Error Handling**: Always validate inputs and handle edge cases
4. **Documentation**: Add comments for complex logic

### Commit Conventions
Use [Conventional Commits](https://www.conventionalcommits.org/) format:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Test additions/updates
- `chore:` Maintenance tasks

**Examples:**
```
feat: add user authentication
fix: resolve memory leak in data processor
docs: update API documentation
```

## Common Tasks

### Adding a New Feature
1. Create a feature branch: `git checkout -b feat/feature-name`
2. Review related files in `src/` for patterns
3. Write tests first (TDD approach recommended)
4. Implement the feature
5. Run tests and linting
6. Commit with conventional commit message

### Fixing a Bug
1. Reproduce the bug with a failing test
2. Review `SECURITY.md` if security-related
3. Fix the issue
4. Verify all tests pass
5. Document the fix in `CHANGELOG.md`

### Refactoring Code
1. Ensure all tests pass before starting
2. Make incremental changes
3. Run tests after each change
4. Update documentation if public APIs change

## Integration Points

### Environment Variables
Required variables are documented in `.env.example`. Never hardcode:
- API keys
- Database credentials
- Service endpoints
- Secret tokens

### External Dependencies
- Review existing dependencies before adding new ones
- Prefer stable, well-maintained packages
- Document why each dependency is needed

## AI Agent Workflows

This project includes AI agent workflows in `.agent/workflows/`. Use these commands:

- `/plan` - Generate project plan from specifications
- `/bootstrap` - Create initial code structure
- `/review` - Audit code for security and quality
- `/commit` - Generate conventional commit messages
- `/save` - Update project memory/scratchpad

## Key Files Reference

- [README.md](README.md) - Project overview and setup
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [SECURITY.md](SECURITY.md) - Security policies
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [.env.example](.env.example) - Environment configuration

## Quick Tips

1. **Read First, Code Second**: Always check existing patterns before writing new code
2. **Test Coverage Matters**: Aim for comprehensive test coverage
3. **Security is Paramount**: When in doubt, ask before handling sensitive data
4. **Document Decisions**: Use comments to explain "why", not "what"
5. **Follow the Stack**: Stick to {tech_stack} unless discussing alternatives
"""

    CURSOR_RULES = """# Cursor IDE Rules

You are an expert AI coding assistant working in Cursor IDE with access to this **{tech_stack}** project.

## Core Directives

### Security & Safety
- Never output API keys, tokens, or credentials in chat or code
- Always use environment variables (`.env`) for sensitive data
- Validate all user inputs before processing
- Check for common vulnerabilities (SQL injection, XSS, CSRF)

### Code Quality Standards
- Follow the tech stack conventions for {tech_stack}
- Use type hints/annotations where applicable
- Write self-documenting code with clear variable names
- Add comments only to explain "why", not "what"
- Maintain consistent code style throughout the project

### Git Workflow
Use Conventional Commits format:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation only
- `refactor:` - Code restructuring
- `test:` - Test additions/updates
- `chore:` - Maintenance tasks

Example: `feat: add user authentication system`

### Development Workflow
1. **Before Coding**: Check `.agent/rules/` for project-specific guidelines
2. **Context Awareness**: Review `docs/imported/` and `context/raw/` for specifications
3. **Testing First**: Write or update tests before implementing features (TDD)
4. **Incremental Changes**: Make small, focused commits
5. **Code Review**: Self-review changes before committing

### Project Structure
- Source code: `src/`
- Tests: `tests/`
- Documentation: `docs/`
- Agent rules: `.agent/rules/`
- Workflows: `.agent/workflows/`
- Configuration: Root directory

### AI Agent Workflows
This project includes callable workflows in `.agent/workflows/`:
- `/plan` - Generate implementation plan from requirements
- `/bootstrap` - Create initial code scaffolding
- `/review` - Security and quality audit
- `/commit` - Generate conventional commit messages
- `/save` - Update project memory/scratchpad

### Key Files to Reference
- [README.md](README.md) - Project overview
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [SECURITY.md](SECURITY.md) - Security policies
- `.agent/rules/01_tech_stack.md` - Tech stack specifics
- `.env.example` - Required environment variables

### When to Ask for Clarification
- Ambiguous requirements or edge cases
- Security-sensitive operations
- Breaking changes to public APIs
- Architecture decisions affecting multiple components

### Cursor-Specific Features
- Use `Cmd/Ctrl+K` for inline edits
- Use `Cmd/Ctrl+L` for chat with context
- Reference files with `@filename` in chat
- Use Composer mode for multi-file edits

## Tech Stack: {tech_stack}

Adhere to best practices and conventions specific to this technology stack.
"""

    WINDSURF_RULES = """# Windsurf IDE Rules (Cascade AI)

You are Cascade, the AI coding agent in Windsurf IDE, working on a **{tech_stack}** project.

## Identity & Capabilities
- You are a senior software engineer with expertise in {tech_stack}
- You have agentic capabilities: planning, reasoning, multi-step execution
- You can read, write, and refactor code across multiple files
- You understand project architecture and dependencies

## Core Principles

### 1. Security-First Development
```
✅ DO:
- Store secrets in `.env` files (never commit)
- Use environment variables via `os.getenv()` or similar
- Validate and sanitize all user inputs
- Follow OWASP security best practices

❌ DON'T:
- Print or log sensitive credentials
- Hardcode API keys or passwords
- Trust user input without validation
- Ignore security warnings
```

### 2. Code Quality Standards
- **Readability**: Clear variable/function names over brevity
- **Type Safety**: Use type hints (Python), TypeScript, or equivalent
- **Error Handling**: Graceful degradation with proper error messages
- **Testing**: Write tests alongside features (TDD preferred)
- **Documentation**: Update docs when changing public APIs

### 3. Git Conventions
All commits must follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <description>

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation only
- refactor: Code restructure without behavior change
- test: Adding or updating tests
- chore: Tooling, dependencies, config

Examples:
feat: add JWT authentication middleware
fix: resolve race condition in data processor
docs: update API endpoint documentation
```

### 4. Cascade Workflow Integration

#### Before Starting Work
1. Review `.agent/rules/` for project-specific guidelines
2. Check `docs/imported/` for requirements and specifications
3. Read `context/raw/` for original design documents
4. Examine `.agent/workflows/` for standard procedures

#### During Development
- Make incremental changes with clear reasoning
- Run tests after each significant change
- Keep the user informed of progress and blockers
- Ask for clarification on ambiguous requirements

#### After Completion
- Self-review code for quality and security
- Update relevant documentation
- Suggest next steps or improvements
- Update `.agent/memory/scratchpad.md` with decisions made

## Project Structure
```
src/          # Source code
tests/        # Test suites
docs/         # Documentation
.agent/       # AI agent configuration
  rules/      # Always-active directives
  workflows/  # Callable procedures
  skills/     # Tool definitions
  memory/     # Session persistence
context/raw/  # Original specifications
```

## Agent Workflows (Slash Commands)
Invoke these for common tasks:

- `/plan` → Generate detailed implementation plan
- `/bootstrap` → Scaffold code structure for feature
- `/review` → Security and quality audit
- `/commit` → Create conventional commit message
- `/save` → Persist session context and decisions

## Technology Stack
**Active Stack**: {tech_stack}

### Stack-Specific Guidelines
Refer to `.agent/rules/01_tech_stack.md` for:
- Framework versions and conventions
- Preferred libraries and tools
- File organization patterns
- Build and deployment processes

## Environment Configuration
Required environment variables are documented in `.env.example`:
- Copy to `.env` for local development
- Never commit `.env` to version control
- Use secret management for production

## Key Reference Files
| File | Purpose |
|------|---------|
| [README.md](README.md) | Project overview & setup |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Development guidelines |
| [SECURITY.md](SECURITY.md) | Security policies |
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| `.agent/rules/00_identity.md` | Agent persona & goals |

## Memory & Context
- **Session Memory**: `.agent/memory/scratchpad.md`
- **Long-term Context**: `context/raw/` directory
- **Imported Knowledge**: `docs/imported/` directory

Update scratchpad with:
- Architectural decisions and rationale
- Unresolved questions or blockers
- Next steps and TODOs
- Lessons learned during development

## Windsurf-Specific Features
- **Cascade Flow**: Multi-step agentic reasoning
- **Context Awareness**: Automatic codebase understanding
- **Multi-file Editing**: Coordinated changes across files
- **Memory Persistence**: Long-term project context

## When to Escalate
Ask the user before:
- Making breaking changes to public APIs
- Modifying core architecture
- Adding new major dependencies
- Implementing security-sensitive features
- Deleting or renaming existing functionality

---

**Remember**: You are Cascade, an intelligent coding agent. Think step-by-step, reason about trade-offs, and always prioritize code quality and security.
"""

    LICENSE_TEMPLATES: dict[str, str] = {
        "mit": """MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
""",
        "apache": """                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/
""",
        "gpl": """                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
""",
    }

    AGENT_RULES: dict[str, str] = {
        "00_identity.md": """# System Identity
You are a Senior Polyglot Software Engineer and Product Architect.
- **Safety:** Never delete data without asking. Never leak secrets.
- **Context:** Always check `docs/imported` and `context/raw` before coding.
""",
        "02_security.md": """# Security Protocols
1. **Secrets:** Never output API keys. Use `.env`.
2. **Inputs:** Validate all inputs.
3. **Dependencies:** Warn if using deprecated libraries.
""",
        "03_git.md": """# Git Conventions
- Use Conventional Commits (`feat:`, `fix:`, `docs:`).
- Never commit to main without testing.
""",
        "04_reasoning.md": """# Reasoning Protocol
1. **Pause:** Analyze the request.
2. **Plan:** Break it down step-by-step.
3. **Check:** Verify against `docs/` constraints.
4. **Execute:** Write code.
""",
        "99_model_dispatch.md": """# Model Dispatch Protocol
## Concept
You are a multi-model intelligence. You must identify when your current capabilities are insufficient and request a "Context Handoff."

## Capability Tiers
1. **Tier 1 (Speed):** GPT-OSS, Gemini Flash. Use for: Chat, simple functions, docs.
2. **Tier 2 (Logic):** Claude Sonnet, Gemini Pro. Use for: Refactoring, coding, standard planning.
3. **Tier 3 (Reasoning):** Claude Opus (Thinking), Gemini Ultra. Use for: Architecture, security audits, root cause analysis.

## Protocol
IF a request exceeds your current Tier:
1. **STOP.**
2. Output: "🛑 **Context Handoff Required** -> [Target Tier]"
3. Wait for the user to switch models.
""",
    }

    AGENT_WORKFLOWS: dict[str, str] = {
        "plan.md": """---
trigger: /plan
---
# Plan Workflow
1. Read `docs/imported/` and `context/raw/`.
2. Break request into atomic tasks.
3. Check against `.agent/rules/`.
4. Output plan and update `scratchpad.md`.
""",
        "bootstrap.md": """---
trigger: /bootstrap
---
# Bootstrap Workflow
1. Read `.agent/rules/01_tech_stack.md`.
2. Generate boilerplate code for the detected stack.
3. Ensure `.gitignore` is respected.
""",
        "commit.md": """---
trigger: /commit
---
# Smart Commit
1. Run `git status`.
2. Analyze diffs.
3. Generate Conventional Commit message.
4. Ask for approval.
""",
        "review.md": """---
trigger: /review
---
# Code Review
1. Check for Security risks (Rule 02).
2. Check for Code Style (Rule 01).
3. Report issues sorted by severity.
""",
        "save.md": """---
trigger: /save
---
# Save Memory
1. Summarize recent actions.
2. Update `.agent/memory/scratchpad.md`.
""",
    }

    AGENT_SKILLS: dict[str, str] = {
        "git_automation/SKILL.md": """---
name: git_automation
description: Safe git operations.
---
# Git Skill
**Commands:** `git status`, `git diff`, `git add`, `git commit`.
**Rule:** Always verify status before adding.
""",
        "secrets_manager/SKILL.md": """---
name: secrets_manager
description: Handle API keys.
---
# Secrets Skill
**Action:** Detect secrets in code. Move them to `.env`. Replace with `os.getenv()`.
""",
    }

    DEVCONTAINER_JSON = """{
  "name": "Antigravity Universal",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": { "ghcr.io/devcontainers/features/common-utils:2": {} }
}
"""


# Maintain backward compatibility with module-level constants
AGENT_DIR = AntigravityResources.AGENT_DIR

# ==============================================================================
# 2. SYSTEM UTILITIES & LOGGING
# ==============================================================================


class AntigravityEngine:
    """
    Low-level utilities for file system operations and input validation.

    This class contains all the foundational operations needed by the Antigravity
    Architect, including sanitization, validation, file I/O, and logging setup.
    All methods are static as they don't require instance state.
    """

    @staticmethod
    def setup_logging(log_dir: str | None = None) -> None:
        """Configure logging to both file and stdout."""
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
            log_path = os.path.join(log_dir, "antigravity_setup.log")
        else:
            log_path = os.path.join(tempfile.gettempdir(), "antigravity_setup.log")

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(log_path, mode="w", encoding="utf-8"),
                logging.StreamHandler(sys.stdout),
            ],
        )

    @staticmethod
    def sanitize_name(name: str | None) -> str:
        """
        Ensures project name is valid and safe for file system.

        Prevents path traversal attacks and invalid characters.
        """
        if not name:
            return "antigravity-project"

        clean = re.sub(r"\s+", "_", name.strip())
        clean = re.sub(r"[^a-zA-Z0-9_\-]", "", clean)

        # Security: Prevent path traversal attempts
        if ".." in clean or clean.startswith(("/", "\\")):
            logging.warning("⚠️ Potential path traversal detected, using default name")
            return "antigravity-project"

        # Security: Prevent empty result after sanitization
        if not clean:
            return "antigravity-project"

        return clean

    @staticmethod
    def slugify_title(title: str) -> str:
        """
        Converts a markdown header or arbitrary title into a safe filename slug.

        Handles special characters, unicode, and edge cases for cross-platform safety.
        Used primarily by the Assimilator for Brain Dump section titles.
        """
        # Remove markdown header markers
        slug = re.sub(r"^#+\s*", "", title)
        # Convert to lowercase and replace spaces/special chars with underscores
        slug = re.sub(r"[^a-zA-Z0-9]", "_", slug.lower())
        # Collapse multiple underscores
        slug = re.sub(r"_+", "_", slug)
        # Strip leading/trailing underscores
        slug = slug.strip("_")
        # Ensure non-empty and reasonable length
        if not slug:
            slug = "untitled"
        return slug[:50]

    @staticmethod
    def parse_keywords(input_str: str | None) -> list[str]:
        """Converts comma/space separated string to list of lowercase keywords."""
        if not input_str:
            return []
        raw = re.split(r"[,\s]+", input_str)
        return [w.lower().strip() for w in raw if w.strip()]

    @staticmethod
    def validate_file_path(filepath: str | None) -> bool:
        """
        Validates that a file path is safe and accessible.

        Returns True if the path is a valid, readable file.
        """
        if not filepath:
            return False

        # Resolve to absolute path and check it's a regular file
        try:
            abs_path = os.path.abspath(filepath)
            if not os.path.isfile(abs_path):
                logging.warning(f"⚠️ Not a valid file: {filepath}")
                return False
            if not os.access(abs_path, os.R_OK):
                logging.warning(f"⚠️ File not readable: {filepath}")
                return False
            return True
        except (OSError, ValueError) as e:
            logging.warning(f"⚠️ Invalid file path: {e}")
            return False

    @staticmethod
    def write_file(path: str, content: str, exist_ok: bool = False) -> bool:
        """
        Writes a new file, creating parent directories as needed.

        Args:
            path: Destination path
            content: File content
            exist_ok: If True, skip if file exists (Safe Mode).
                      If False, overwrite existing file (Default).

        Returns True on success/creation, False on failure or skipped.
        """
        try:
            if exist_ok and os.path.exists(path):
                logging.info(f"⏭️  Skipped (Exists): {path}")
                return True

            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content.strip() + "\n")

            icon = "✅" if not os.path.exists(path) else "📝"
            logging.info(f"{icon} Wrote: {path}")
            return True
        except OSError as e:
            logging.error(f"❌ Error writing {path}: {e}")
            return False

    @staticmethod
    def append_file(path: str, content: str) -> bool:
        """
        Appends content to a file (used for Assimilation).

        Returns True on success, False on failure.
        """
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "a", encoding="utf-8") as f:
                f.write("\n\n" + content.strip() + "\n")
            logging.info(f"🔗 Appended to: {path}")
            return True
        except OSError as e:
            logging.error(f"❌ Error appending {path}: {e}")
            return False

    @staticmethod
    def create_folder(path: str) -> bool:
        """
        Creates a folder and adds .gitkeep so Git tracks it.

        Returns True on success, False on failure.
        """
        try:
            os.makedirs(path, exist_ok=True)
            gitkeep_path = os.path.join(path, ".gitkeep")
            with open(gitkeep_path, "w") as f:
                f.write("")
            logging.info(f"📁 Directory: {path}")
            return True
        except OSError as e:
            logging.error(f"❌ Error creating folder {path}: {e}")
            return False


# Maintain backward compatibility with module-level functions
setup_logging = AntigravityEngine.setup_logging
sanitize_name = AntigravityEngine.sanitize_name
parse_keywords = AntigravityEngine.parse_keywords
validate_file_path = AntigravityEngine.validate_file_path
write_file = AntigravityEngine.write_file
append_file = AntigravityEngine.append_file
create_folder = AntigravityEngine.create_folder


# ==============================================================================
# 3. CONFIGURATION BUILDERS
# ==============================================================================


class AntigravityBuilder:
    """
    Dynamic configuration and content generators.

    This class contains all the "build_*" functions that generate configuration
    files and content based on detected technology keywords and user preferences.
    All methods are static as they don't require instance state.
    """

    @staticmethod
    def build_gitignore(keywords: list[str]) -> str:
        """Builds a .gitignore file based on detected technology keywords."""
        content = AntigravityResources.BASE_GITIGNORE
        for k in keywords:
            if k in AntigravityResources.GITIGNORE_MAP:
                content += AntigravityResources.GITIGNORE_MAP[k]
            elif k in ("js", "javascript"):
                content += AntigravityResources.GITIGNORE_MAP.get("node", "")
        return content

    @staticmethod
    def build_nix_config(keywords: list[str]) -> str:
        """Builds a dev.nix configuration for Google Project IDX."""
        packages = ["pkgs.git", "pkgs.curl", "pkgs.jq", "pkgs.openssl"]

        # Map framework keywords to their base language
        keyword_aliases: dict[str, str] = {
            "js": "node",
            "javascript": "node",
            "react": "node",
            "nextjs": "node",
            "django": "python",
            "flask": "python",
            "fastapi": "python",
        }

        for k in keywords:
            key = keyword_aliases.get(k, k)
            if key in AntigravityResources.NIX_PACKAGE_MAP:
                packages.extend(AntigravityResources.NIX_PACKAGE_MAP[key])

        package_str = "\n    ".join(sorted(set(packages)))
        return f"""# Google Project IDX Environment Configuration
{{ pkgs, ... }}: {{
  channel = "stable-23.11";
  packages = [
    {package_str}
  ];
  env = {{}};
  idx = {{
    extensions = ["google.gemini-code-assist"];
    workspace = {{
      onCreate = {{
        setup = "echo 'Antigravity Environment Ready'";
      }};
    }};
  }};
}}
"""

    @staticmethod
    def build_tech_stack_rule(keywords: list[str]) -> str:
        """Builds a dynamic tech stack rule for the agent."""
        return f"""# Technology Stack
Keywords Detected: {", ".join(keywords)}

## Directives
1. **Inference:** Assume standard frameworks for these keywords (e.g., React implies standard hooks/components).
2. **Tooling:** Use the standard CLI tools (pip, npm, cargo, go mod).
3. **Files:** Look for `pyproject.toml`, `package.json`, or similar to confirm versions.
"""

    @staticmethod
    def build_scratchpad(keywords: list[str], has_brain_dump: bool) -> str:
        """Builds the initial scratchpad memory file."""
        return f"""# Project Scratchpad
*Last Updated: {datetime.now().isoformat()}*

## Status
- Project initialized.
- Tech Stack: {", ".join(keywords)}.
- Imported Knowledge: {"Yes" if has_brain_dump else "No"}.

## Model Roles Map
| Role | Recommended Model | User Selection (Fill this in) |
| :--- | :--- | :--- |
| **Architect** | Tier 3 (Opus/Ultra/o1) | [YOUR SELECTION HERE] |
| **Builder** | Tier 2 (Sonnet/Pro) | [YOUR SELECTION HERE] |
| **Assistant** | Tier 1 (Flash/Mini) | [YOUR SELECTION HERE] |
"""


# Maintain backward compatibility with module-level functions
build_gitignore = AntigravityBuilder.build_gitignore
build_nix_config = AntigravityBuilder.build_nix_config
build_tech_stack_rule = AntigravityBuilder.build_tech_stack_rule
build_scratchpad = AntigravityBuilder.build_scratchpad


# ==============================================================================
# 4. THE ASSIMILATOR (INTELLIGENT PARSING)
# ==============================================================================


class AntigravityAssimilator:
    """
    Intelligent brain dump parsing and knowledge distribution.

    This class handles the "Assimilator" feature - parsing large text dumps,
    categorizing content using heuristics, and distributing it to appropriate
    .agent/ directories based on detected content type.
    All methods are static as they don't require instance state.
    """

    @staticmethod
    def identify_category(text: str) -> str:
        """
        Uses heuristics to decide if text is a Rule, Workflow, Skill, or Doc.

        Returns the category with the highest keyword match score.
        """
        text_lower = text.lower()
        scores: dict[str, int] = dict.fromkeys(AntigravityResources.CLASSIFICATION_RULES, 0)

        for category, keywords in AntigravityResources.CLASSIFICATION_RULES.items():
            for k in keywords:
                scores[category] += len(re.findall(r"\b" + re.escape(k) + r"\b", text_lower))

        best_cat = max(scores, key=lambda x: scores[x])
        if scores[best_cat] == 0:
            return "docs"
        return best_cat

    @staticmethod
    def get_destination_path(base_dir: str, category: str, safe_title: str) -> str:
        """Determines the file destination based on category."""
        category_paths: dict[str, str] = {
            "rules": os.path.join(base_dir, AGENT_DIR, "rules", f"imported_{safe_title}.md"),
            "workflows": os.path.join(base_dir, AGENT_DIR, "workflows", f"imported_{safe_title}.md"),
            "skills": os.path.join(base_dir, AGENT_DIR, "skills", f"imported_{safe_title}", "SKILL.md"),
            "docs": os.path.join(base_dir, "docs", "imported", f"{safe_title}.md"),
        }
        return category_paths.get(category, category_paths["docs"])

    @staticmethod
    def process_brain_dump(filepath: str | None, base_dir: str) -> list[str]:
        """
        Reads a brain dump file, splits by headers, and distributes to .agent/ folders.

        Returns a list of detected technology keywords from the content.
        """
        if not validate_file_path(filepath):
            return []

        # Type narrowing: after validation, filepath is confirmed to be str
        assert filepath is not None

        print(f"\n🧠 Assimilating knowledge from: {filepath}...")

        try:
            with open(filepath, encoding="utf-8", errors="replace") as f:
                full_text = f.read()
        except Exception as e:
            logging.error(f"Could not read brain dump: {e}")
            return []

        # 1. Archive Raw Content
        raw_dest = os.path.join(base_dir, "context", "raw", "master_brain_dump.md")
        write_file(raw_dest, full_text, exist_ok=True)

        # 2. Extract Tech Stack Keywords
        detected_keywords: set[str] = set()
        for k in AntigravityResources.GITIGNORE_MAP:
            if re.search(r"\b" + re.escape(k) + r"\b", full_text.lower()):
                detected_keywords.add(k)

        # 3. Split & Distribute
        sections = re.split(r"(^#+\s+.*$)", full_text, flags=re.MULTILINE)

        for i in range(1, len(sections), 2):
            if i + 1 >= len(sections):
                break
            header = sections[i].strip()
            content = sections[i + 1].strip()
            if not content:
                continue

            category = AntigravityAssimilator.identify_category(header + "\n" + content)
            safe_title = AntigravityEngine.slugify_title(header)
            dest = AntigravityAssimilator.get_destination_path(base_dir, category, safe_title)

            formatted = f"<!-- Auto-Assimilated Source -->\n\n{header}\n\n{content}"
            append_file(dest, formatted)

        print("🧠 Assimilation Complete.")
        return list(detected_keywords)


# Maintain backward compatibility with module-level functions
identify_category = AntigravityAssimilator.identify_category
get_destination_path = AntigravityAssimilator.get_destination_path
process_brain_dump = AntigravityAssimilator.process_brain_dump


# ==============================================================================
# 5. PROJECT GENERATION ORCHESTRATION
# ==============================================================================


class AntigravityGenerator:
    """
    High-level project generation orchestration.

    This class coordinates all the other components (Resources, Engine, Builder,
    Assimilator) to generate complete project structures. It handles the full
    workflow from directory creation through file generation and brain dump processing.
    All methods are static as they orchestrate other static classes.
    """

    @staticmethod
    def generate_agent_files(base_dir: str, keywords: list[str], safe_mode: bool = False) -> None:
        """Generates all .agent/ rules, workflows, and skills."""

        # Generate static rules
        for filename, content in AntigravityResources.AGENT_RULES.items():
            path = os.path.join(base_dir, AGENT_DIR, "rules", filename)
            write_file(path, content, exist_ok=safe_mode)

        # Generate dynamic tech stack rule
        tech_stack_path = os.path.join(base_dir, AGENT_DIR, "rules", "01_tech_stack.md")
        write_file(tech_stack_path, build_tech_stack_rule(keywords), exist_ok=safe_mode)

        # Generate workflows
        for filename, content in AntigravityResources.AGENT_WORKFLOWS.items():
            path = os.path.join(base_dir, AGENT_DIR, "workflows", filename)
            write_file(path, content, exist_ok=safe_mode)

        # Generate skills
        for filename, content in AntigravityResources.AGENT_SKILLS.items():
            path = os.path.join(base_dir, AGENT_DIR, "skills", filename)
            write_file(path, content, exist_ok=safe_mode)

    @staticmethod
    def generate_project(
        project_name: str,
        keywords: list[str],
        brain_dump_path: str | None = None,
        safe_mode: bool | None = None,
        custom_templates: dict[str, dict[str, str]] | None = None,
        license_type: str = "mit",
    ) -> bool:
        """
        Main project generation logic.

        Creates the full project structure with all configurations and agent files.
        Args:
            project_name: Name of the project to create.
            keywords: List of tech stack keywords.
            brain_dump_path: Optional path to a brain dump file.
            safe_mode: If True, non-destructive. If None, prompt user if dir exists.
            custom_templates: Optional dict of custom template overrides.
            license_type: Project license type (mit, apache, gpl).
        Returns True on success, False on failure.
        """
        base_dir = os.path.join(os.getcwd(), project_name)

        # Handle safe_mode: if not explicitly set and directory exists, prompt user
        if safe_mode is None and os.path.exists(base_dir):
            print(f"\n⚠️  Project '{project_name}' already exists.")
            choice = input("Select mode: [U]pdate (Safe) / [O]verwrite (Risky) / [C]ancel: ").lower()

            if choice == "u":
                print("🛡️  Safe Update Mode Active: Only missing files will be created.")
                safe_mode = True
            elif choice == "o":
                confirm = input("💥 WARNING: This will overwrite files. Type 'yes' to confirm: ")
                if confirm.lower() != "yes":
                    return False
                safe_mode = False
            else:
                return False
        elif safe_mode is None:
            safe_mode = False

        print(f"\n🚀 Constructing '{project_name}'...")

        # Setup logging in target directory
        setup_logging(base_dir)

        # Create directory structure (Safe to do even if exists)
        directories = [
            "src",
            "tests",
            "docs/imported",
            "context/raw",
            AntigravityResources.IDX_DIR,
            AntigravityResources.DEVCONTAINER_DIR,
            f"{AGENT_DIR}/rules",
            f"{AGENT_DIR}/workflows",
            f"{AGENT_DIR}/skills",
            f"{AGENT_DIR}/memory",
            f"{AGENT_DIR}/skills/git_automation",
            f"{AGENT_DIR}/skills/secrets_manager",
        ]
        for d in directories:
            create_folder(os.path.join(base_dir, d))

        # Process brain dump if provided
        detected_stack: list[str] = []
        if brain_dump_path:
            detected_stack = process_brain_dump(brain_dump_path, base_dir)

        # Merge keywords
        final_stack = list(set(keywords + detected_stack))
        if not final_stack:
            final_stack = ["linux"]
        print(f"⚙️  Final Tech Stack: {', '.join(final_stack)}")

        # Generate configuration files - Safe Mode applies here
        # Note: .gitignore and README always use exist_ok=True to prevent overwriting user customizations
        write_file(
            os.path.join(base_dir, AntigravityResources.GITIGNORE_FILE), build_gitignore(final_stack), exist_ok=True
        )
        write_file(
            os.path.join(base_dir, AntigravityResources.IDX_DIR, AntigravityResources.NIX_FILE),
            build_nix_config(final_stack),
            exist_ok=safe_mode,
        )
        write_file(
            os.path.join(base_dir, AntigravityResources.DEVCONTAINER_DIR, AntigravityResources.DEVCONTAINER_FILE),
            AntigravityResources.DEVCONTAINER_JSON,
            exist_ok=safe_mode,
        )
        write_file(
            os.path.join(base_dir, AntigravityResources.README_FILE),
            f"# {project_name}\n\nStack: {', '.join(final_stack)}",
            exist_ok=True,
        )
        write_file(
            os.path.join(base_dir, AntigravityResources.ENV_EXAMPLE_FILE), "API_KEY=\nDB_URL=", exist_ok=safe_mode
        )

        # Generate License
        license_content = AntigravityResources.LICENSE_TEMPLATES.get(
            license_type, AntigravityResources.LICENSE_TEMPLATES["mit"]
        )
        if license_type == "mit":
            license_content = license_content.format(year=datetime.now().year, author="pkeffect")
        write_file(os.path.join(base_dir, AntigravityResources.LICENSE_FILE), license_content, exist_ok=safe_mode)

        # Generate Community Standards
        write_file(
            os.path.join(base_dir, AntigravityResources.CHANGELOG_FILE),
            AntigravityResources.CHANGELOG_TEMPLATE,
            exist_ok=safe_mode,
        )
        write_file(
            os.path.join(base_dir, AntigravityResources.CONTRIBUTING_FILE),
            AntigravityResources.CONTRIBUTING_TEMPLATE,
            exist_ok=safe_mode,
        )
        write_file(
            os.path.join(base_dir, AntigravityResources.AUDIT_FILE),
            AntigravityResources.AUDIT_TEMPLATE,
            exist_ok=safe_mode,
        )
        write_file(
            os.path.join(base_dir, AntigravityResources.SECURITY_FILE),
            AntigravityResources.SECURITY_TEMPLATE,
            exist_ok=safe_mode,
        )
        write_file(
            os.path.join(base_dir, AntigravityResources.CODE_OF_CONDUCT_FILE),
            AntigravityResources.CODE_OF_CONDUCT_TEMPLATE,
            exist_ok=safe_mode,
        )

        # Generate GitHub Templates (Professional Repository Standards)
        github_dir = os.path.join(base_dir, ".github")
        issue_template_dir = os.path.join(github_dir, "ISSUE_TEMPLATE")
        create_folder(issue_template_dir)

        write_file(
            os.path.join(issue_template_dir, "bug_report.md"),
            AntigravityResources.GITHUB_BUG_REPORT,
            exist_ok=safe_mode,
        )
        write_file(
            os.path.join(issue_template_dir, "feature_request.md"),
            AntigravityResources.GITHUB_FEATURE_REQUEST,
            exist_ok=safe_mode,
        )
        write_file(
            os.path.join(issue_template_dir, "question.md"),
            AntigravityResources.GITHUB_QUESTION,
            exist_ok=safe_mode,
        )
        write_file(
            os.path.join(issue_template_dir, "config.yml"),
            AntigravityResources.GITHUB_ISSUE_CONFIG,
            exist_ok=safe_mode,
        )
        write_file(
            os.path.join(github_dir, "PULL_REQUEST_TEMPLATE.md"),
            AntigravityResources.GITHUB_PR_TEMPLATE,
            exist_ok=safe_mode,
        )
        write_file(
            os.path.join(github_dir, "FUNDING.yml"),
            AntigravityResources.GITHUB_FUNDING,
            exist_ok=safe_mode,
        )
        write_file(
            os.path.join(github_dir, "copilot-instructions.md"),
            AntigravityResources.GITHUB_COPILOT_INSTRUCTIONS.format(tech_stack=", ".join(final_stack)),
            exist_ok=safe_mode,
        )

        # Generate Cursor and Windsurf Rules (AI IDE Compatibility)
        write_file(
            os.path.join(base_dir, ".cursorrules"),
            AntigravityResources.CURSOR_RULES.format(tech_stack=", ".join(final_stack)),
            exist_ok=safe_mode,
        )
        write_file(
            os.path.join(base_dir, ".windsurfrules"),
            AntigravityResources.WINDSURF_RULES.format(tech_stack=", ".join(final_stack)),
            exist_ok=safe_mode,
        )

        # Generate agent files
        AntigravityGenerator.generate_agent_files(base_dir, final_stack, safe_mode=safe_mode)

        # Generate memory and bootstrap (scratchpad always preserved)
        write_file(
            os.path.join(base_dir, AGENT_DIR, "memory", "scratchpad.md"),
            build_scratchpad(final_stack, bool(brain_dump_path)),
            exist_ok=True,
        )

        write_file(
            os.path.join(base_dir, AntigravityResources.BOOTSTRAP_FILE),
            """# Agent Start Guide
1. **Context:** Read `.agent/memory/scratchpad.md`.
2. **Knowledge:** Check `docs/imported/` for assimilated rules.
3. **Action:** Run `/bootstrap` to generate the application skeleton.
""",
            exist_ok=safe_mode,
        )

        print(f"\n✅ Project '{project_name}' ready!")
        print(f"📂 Location: {os.path.abspath(base_dir)}\n")
        return True


# Maintain backward compatibility with module-level functions
generate_agent_files = AntigravityGenerator.generate_agent_files
generate_project = AntigravityGenerator.generate_project


# ==============================================================================
# 6. CLI, DOCTOR MODE, AND MAIN EXECUTION
# ==============================================================================


def build_cli_parser() -> argparse.ArgumentParser:
    """Build the argument parser for CLI mode."""
    parser = argparse.ArgumentParser(
        prog="antigravity_master_setup.py",
        description="🌌 Antigravity Architect: Agent-First Project Bootstrapper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python antigravity_master_setup.py                           # Interactive mode
  python antigravity_master_setup.py --name my-app --stack python,react
  python antigravity_master_setup.py --name my-app --brain-dump ./specs.md --safe
  python antigravity_master_setup.py --doctor ./existing-project
  python antigravity_master_setup.py --list-keywords
        """,
    )

    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")

    parser.add_argument("--name", "-n", type=str, help="Project name (required for CLI mode)")
    parser.add_argument(
        "--stack", "-s", type=str, help="Comma-separated tech stack keywords (e.g., python,react,docker)"
    )
    parser.add_argument("--brain-dump", "-b", type=str, help="Path to brain dump file for Knowledge Assimilation")
    parser.add_argument("--safe", action="store_true", help="Enable Safe Update Mode (non-destructive)")
    parser.add_argument("--dry-run", action="store_true", help="Preview actions without creating files")
    parser.add_argument("--templates", "-t", type=str, help="Path to custom templates directory")

    parser.add_argument("--doctor", type=str, metavar="PATH", help="Validate an existing project's .agent/ structure")
    parser.add_argument("--fix", action="store_true", help="Attempt to fix issues found by --doctor")

    parser.add_argument("--list-keywords", action="store_true", help="List all supported tech stack keywords")
    parser.add_argument(
        "--license",
        "-l",
        type=str,
        choices=["mit", "apache", "gpl"],
        default="mit",
        help="Project license (default: mit)",
    )

    return parser


def load_custom_templates(templates_path: str | None) -> dict[str, dict[str, str]]:
    """
    Load custom templates from a directory, merging with defaults.

    Returns a dict with keys 'rules', 'workflows', 'skills' containing template overrides.
    """
    if not templates_path:
        home_templates = Path.home() / ".antigravity" / "templates"
        if home_templates.exists():
            templates_path = str(home_templates)
        else:
            return {}

    templates_dir = Path(templates_path)
    if not templates_dir.exists():
        logging.warning(f"⚠️ Templates directory not found: {templates_path}")
        return {}

    overrides: dict[str, dict[str, str]] = {"rules": {}, "workflows": {}, "skills": {}}

    for category in overrides:
        category_dir = templates_dir / category
        if category_dir.exists():
            for file_path in category_dir.glob("*.md"):
                content = file_path.read_text(encoding="utf-8")
                overrides[category][file_path.name] = content
                logging.info(f"📦 Loaded custom template: {category}/{file_path.name}")

    return overrides


def doctor_project(project_path: str, fix: bool = False) -> bool:
    """
    Validate an existing project's .agent/ structure.

    In fix mode, regenerates missing or empty required files from internal templates.
    Returns True if healthy, False if issues found.
    """
    print(f"\n🩺 Running Doctor on: {project_path}")
    print(AntigravityResources.SEPARATOR)

    base_dir = Path(project_path)
    if not base_dir.exists():
        print(f"❌ Project directory not found: {project_path}")
        return False

    issues: list[str] = []
    warnings: list[str] = []
    passed: list[str] = []
    fixed: list[str] = []

    required_dirs = [
        ".agent/rules",
        ".agent/workflows",
        ".agent/skills",
        ".agent/memory",
    ]

    for dir_path in required_dirs:
        full_path = base_dir / dir_path
        if full_path.exists():
            passed.append(f"✅ {dir_path}/ exists")
        else:
            issues.append(f"❌ Missing: {dir_path}/")
            if fix:
                full_path.mkdir(parents=True, exist_ok=True)
                (full_path / ".gitkeep").touch()
                fixed.append(f"🔧 Created {dir_path}/")

    # Required files with their regeneration templates
    required_files_templates: dict[str, tuple[str, str]] = {
        ".agent/rules/00_identity.md": (
            "Agent identity rule",
            AntigravityResources.AGENT_RULES.get("00_identity.md", ""),
        ),
        ".agent/rules/01_tech_stack.md": (
            "Tech stack rule",
            build_tech_stack_rule(["linux"]),  # Default fallback stack
        ),
        ".agent/memory/scratchpad.md": (
            "Memory scratchpad",
            build_scratchpad(["linux"], False),
        ),
        AntigravityResources.BOOTSTRAP_FILE: (
            "Bootstrap guide",
            """# Agent Start Guide\n1. **Context:** Read `.agent/memory/scratchpad.md`.\n2. **Knowledge:** Check `docs/imported/` for assimilated rules.\n3. **Action:** Run `/bootstrap` to generate the application skeleton.\n""",
        ),
    }

    for file_path, (_description, template) in required_files_templates.items():
        full_path = base_dir / file_path
        is_missing = not full_path.exists()
        is_empty = full_path.exists() and full_path.stat().st_size == 0

        if is_missing:
            issues.append(f"❌ Missing: {file_path}")
            if fix and template:
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(template, encoding="utf-8")
                fixed.append(f"🔧 Regenerated {file_path}")
        elif is_empty:
            warnings.append(f"⚠️  {file_path} is empty")
            if fix and template:
                full_path.write_text(template, encoding="utf-8")
                fixed.append(f"🔧 Restored content to {file_path}")
        else:
            passed.append(f"✅ {file_path} exists")

    # Check IDE configuration files (can be regenerated)
    ide_files: dict[str, str] = {
        ".cursorrules": AntigravityResources.CURSOR_RULES.format(tech_stack="linux"),
        ".windsurfrules": AntigravityResources.WINDSURF_RULES.format(tech_stack="linux"),
    }

    for file_path, template in ide_files.items():
        full_path = base_dir / file_path
        is_missing = not full_path.exists()
        is_empty = full_path.exists() and full_path.stat().st_size == 0

        if is_missing:
            warnings.append(f"⚠️  Optional: {file_path} not found")
            if fix:
                full_path.write_text(template, encoding="utf-8")
                fixed.append(f"🔧 Generated {file_path}")
        elif is_empty:
            warnings.append(f"⚠️  {file_path} is empty")
            if fix:
                full_path.write_text(template, encoding="utf-8")
                fixed.append(f"🔧 Restored content to {file_path}")
        else:
            passed.append(f"✅ {file_path} exists")

    optional_files = [
        AntigravityResources.GITIGNORE_FILE,
        AntigravityResources.README_FILE,
        AntigravityResources.CHANGELOG_FILE,
        AntigravityResources.CONTRIBUTING_FILE,
        AntigravityResources.AUDIT_FILE,
        AntigravityResources.SECURITY_FILE,
        AntigravityResources.CODE_OF_CONDUCT_FILE,
        AntigravityResources.LICENSE_FILE,
    ]

    for file_path in optional_files:
        full_path = base_dir / file_path
        if full_path.exists():
            passed.append(f"✅ {file_path} exists")
        else:
            warnings.append(f"⚠️  Optional: {file_path} not found")

    print(AntigravityResources.SEPARATOR)
    print(f"Summary: {len(passed)} passed, {len(warnings)} warnings, {len(issues)} issues")

    if fixed:
        print("\n🔧 Fixes Applied:")
        for fix_msg in fixed:
            print(f"  {fix_msg}")

    if issues:
        print("\n🚨 Issues Found:")
        for issue in issues:
            print(f"  {issue}")

    if warnings:
        print("\n⚠️  Warnings:")
        for warning in warnings:
            print(f"  {warning}")

    print(f"\n{AntigravityResources.SEPARATOR}")

    # After fixes, re-evaluate health
    remaining_issues = len(issues) - len([f for f in fixed if "Missing" in f or "Regenerated" in f])
    if remaining_issues > 0 and not fix:
        print("❌ Project needs attention! Run with --fix to repair.")
        return False
    elif fixed:
        print("🏆 Project repaired and healthy!")
        return True
    elif issues:
        print("❌ Project needs attention!")
        return False
    else:
        print("🏆 Project is fully healthy!")
        return True


def list_keywords() -> None:
    """Display all supported tech stack keywords."""
    print("\n🛠 Supported Tech Stack Keywords")
    print(AntigravityResources.SEPARATOR)

    categories = {
        "Languages": ["python", "node", "javascript", "rust", "go", "java", "php", "ruby"],
        "Frameworks": ["react", "nextjs", "django", "flask", "fastapi"],
        "Infrastructure": ["docker", "sql", "postgres"],
        "OS / Platforms": ["macos", "windows", "linux"],
        "IDEs": ["vscode", "idea"],
    }

    for category, keywords in categories.items():
        print(f"\n{category}:")
        print(f"  {', '.join(keywords)}")

    print("\n" + AntigravityResources.SEPARATOR)
    print("Usage: --stack python,react,docker")


def run_interactive_mode() -> None:
    """Original interactive mode for backwards compatibility."""
    print(AntigravityResources.SEPARATOR)
    print(f"   🌌 Antigravity Architect v{VERSION}")
    print("   Dynamic Parsing | Knowledge Distribution | Universal")
    print(AntigravityResources.SEPARATOR)

    setup_logging()

    print("\n[Optional] Drag & Drop a Brain Dump file (Specs/Notes/Code):")
    brain_dump_path: str | None = input("Path: ").strip().strip("'\"") or None

    raw_name = input("\nProject Name: ")
    project_name = sanitize_name(raw_name)
    if not project_name or project_name == "antigravity-project" and not raw_name:
        print("❌ Project name is required.")
        return

    manual_keywords: list[str] = []
    if not brain_dump_path:
        print("\nTech Stack (e.g. python, react, aws):")
        k_in = input("Keywords: ")
        manual_keywords = parse_keywords(k_in)

        if not any(x in manual_keywords for x in ("macos", "windows", "linux")):
            manual_keywords.append("linux")

    print("\nLicense (mit, apache, gpl):")
    license_choice = input("Choice [mit]: ").strip().lower() or "mit"

    generate_project(project_name, manual_keywords, brain_dump_path, license_type=license_choice)


def run_cli_mode(args: argparse.Namespace) -> None:
    """Run in CLI mode with provided arguments."""
    print("=========================================================")
    print(f"   🌌 Antigravity Architect v{VERSION} (CLI Mode)")
    print("=========================================================")

    setup_logging()

    custom_templates = load_custom_templates(args.templates)
    if custom_templates:
        print(f"📦 Loaded {sum(len(v) for v in custom_templates.values())} custom templates")

    project_name = sanitize_name(args.name)
    if not project_name:
        print("❌ Invalid project name.")
        return

    keywords = parse_keywords(args.stack) if args.stack else []
    if not any(x in keywords for x in ("macos", "windows", "linux")):
        keywords.append("linux")

    if args.dry_run:
        print("\n🔍 DRY RUN MODE - No files will be created")
        print("=" * 60)
        print(f"📦 Project Name: {project_name}")
        print(f"⚙️  Tech Stack: {', '.join(keywords)}")
        print(f"🧠 Brain Dump: {args.brain_dump or 'None'}")
        print(f"🛡️  Safe Mode: {args.safe}")
        print(f"📁 Templates: {args.templates or 'Default (Built-in)'}")
        print(f"📜 License: {args.license}")
        print("=" * 60)

        print("\n📁 Directories that would be created:")
        dirs = [
            "src",
            "tests",
            "docs/imported",
            "context/raw",
            ".idx",
            ".devcontainer",
            ".github/ISSUE_TEMPLATE",
            ".agent/rules",
            ".agent/workflows",
            ".agent/skills/git_automation",
            ".agent/skills/secrets_manager",
            ".agent/memory",
        ]
        for d in dirs:
            print(f"    � {project_name}/{d}/")

        print("\n📄 Core Files that would be created:")
        core_files = [
            ".gitignore",
            "README.md",
            "LICENSE",
            "CHANGELOG.md",
            "CONTRIBUTING.md",
            "AUDIT.md",
            "SECURITY.md",
            "CODE_OF_CONDUCT.md",
            "BOOTSTRAP_INSTRUCTIONS.md",
            ".env.example",
        ]
        for f in core_files:
            print(f"    📄 {project_name}/{f}")

        print("\n🤖 AI IDE Configuration Files:")
        ide_files = [
            (".cursorrules", f"Tech Stack: {', '.join(keywords)}"),
            (".windsurfrules", f"Tech Stack: {', '.join(keywords)}"),
            (".github/copilot-instructions.md", f"Tech Stack: {', '.join(keywords)}"),
        ]
        for f, desc in ide_files:
            print(f"    🤖 {project_name}/{f} ({desc})")

        print("\n📜 Agent Rules (.agent/rules/):")
        for rule_file in AntigravityResources.AGENT_RULES:
            print(f"    📜 {rule_file}")
        print(f"    📜 01_tech_stack.md (Dynamic: {', '.join(keywords)})")

        print("\n⚡ Agent Workflows (.agent/workflows/):")
        for workflow_file in AntigravityResources.AGENT_WORKFLOWS:
            print(f"    ⚡ {workflow_file}")

        print("\n🛠️  Agent Skills (.agent/skills/):")
        for skill_file in AntigravityResources.AGENT_SKILLS:
            print(f"    🛠️  {skill_file}")

        print("\n🧠 Agent Memory (.agent/memory/):")
        print("    🧠 scratchpad.md")

        print("\n📋 GitHub Templates (.github/):")
        github_files = [
            "ISSUE_TEMPLATE/bug_report.md",
            "ISSUE_TEMPLATE/feature_request.md",
            "ISSUE_TEMPLATE/question.md",
            "ISSUE_TEMPLATE/config.yml",
            "PULL_REQUEST_TEMPLATE.md",
            "FUNDING.yml",
        ]
        for f in github_files:
            print(f"    📋 {f}")

        print("\n" + "=" * 60)
        print("✅ Dry run complete. No changes made.")
        print("   Run without --dry-run to create the project.")
        return

    generate_project(
        project_name,
        keywords,
        args.brain_dump,
        safe_mode=args.safe,
        custom_templates=custom_templates,
    )


def main() -> None:
    """Main entry point for the Antigravity Architect."""
    parser = build_cli_parser()
    args = parser.parse_args()

    if args.list_keywords:
        list_keywords()
        return

    if args.doctor:
        doctor_project(args.doctor, fix=args.fix)
        return

    if args.name:
        run_cli_mode(args)
    else:
        run_interactive_mode()


if __name__ == "__main__":
    main()
