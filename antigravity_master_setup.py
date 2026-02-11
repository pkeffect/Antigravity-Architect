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
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

VERSION = "1.7.0"

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
    ANTIGRAVITY_DIR_NAME = ".antigravity"
    PRESETS_DIR = Path.home() / ANTIGRAVITY_DIR_NAME / "presets"

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
    AGENT_MANIFEST = "manifest.json"

    BOOTSTRAP_FILE = "BOOTSTRAP_INSTRUCTIONS.md"
    VSCODE_DIR = ".vscode"
    GITEA_DIR = ".gitea"
    RULE_ARCHITECTURE = "05_architecture.md"
    RULE_SECURITY_EXPERT = "07_security_expert.md"
    RULE_IDENTITY = "00_identity.md"
    RULE_TECH_STACK = "01_tech_stack.md"
    RULE_SECURITY = "02_security.md"

    # Extension Constants
    EXT_ESLINT = "dbaeumer.vscode-eslint"
    EXT_PRETTIER = "esbenp.prettier-vscode"

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
        "docker": "\n# --- Docker ---\n.docker/\n",
        "postgres": "",
        "react": "\n# --- React ---\nbuild/\n.env.local\n",
        "nextjs": "\n# --- NextJS ---\n.next/\nout/\n",
        "macos": "\n# --- macOS ---\n.DS_Store\n.AppleDouble\n",
        "windows": "\n# --- Windows ---\nThumbs.db\nehthumbs.db\n*.exe\n*.dll\n",
        "linux": "\n# --- Linux ---\n*~\n.fuse_hidden*\n",
        "vscode": f"\n# --- VS Code ---\n{VSCODE_DIR}/\n",
        "gitea": f"\n# --- Gitea ---\n{GITEA_DIR}/\n",
    }

    # Alias Mapping for Intelligent Tech Detection
    TECH_ALIASES: dict[str, list[str]] = {
        "python": [
            "django",
            "flask",
            "fastapi",
            "numpy",
            "pandas",
            "pytorch",
            "tensorflow",
            "scipy",
            "pytest",
            "poetry",
        ],
        "node": [
            "javascript",
            "typescript",
            "react",
            "vue",
            "svelte",
            "sveltekit",
            "nextjs",
            "express",
            "nest",
            "npm",
            "yarn",
            "pnpm",
        ],
        "docker": ["container", "dockerfile", "docker-compose", "kubernetes", "k8s"],
        "sql": ["postgres", "postgresql", "sqlite", "mysql", "mariadb", "oracle", "db2"],
        "cloud": ["aws", "azure", "gcp", "google cloud", "lambda", "s3", "ec2"],
    }

    # B. Nix Packages (For Google Project IDX / Cloud Environments)
    NIX_PACKAGE_MAP: dict[str, list[str]] = {
        "python": ["pkgs.python312", "pkgs.python312Packages.pip", "pkgs.ruff", "pkgs.python312Packages.virtualenv"],
        "node": ["pkgs.nodejs_20", "pkgs.nodePackages.nodemon", "pkgs.nodePackages.typescript"],
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
### Added
- Initial release

### Changed
-

### Deprecated
-

### Removed
-

### Fixed
-

### Security
-
"""

    AGENT_MANIFEST_TEMPLATE = """{{
  "protocol": "2.0.0",
  "project": "{project_name}",
  "capabilities": {{
    "reasoning_tier": "3",
    "mcp_support": true
  }},
  "structure": {{
    "rules": ".agent/rules/",
    "workflows": ".agent/workflows/",
    "skills": ".agent/skills/",
    "memory": ".agent/memory/"
  }},
  "ruleset": {{
    "layered": true,
    "priority": [
      "00_identity.md",
      "01_tech_stack.md",
      "02_security.md",
      "08_boundaries.md"
    ]
  }}
}}
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

    GRAVEYARD_TEMPLATE = """# Dependency & Logic Graveyard
Track rejected technologies, failed implementations, or deprecated patterns here.

## Rejected Dependencies
| Library | Date | Reason |
| :--- | :--- | :--- |
| example-pkg | 2026-02-08 | High latency / Security risk |

## Failed Implementations
- **Logic X**: Replaced by **Logic Y** due to edge case failure in production.
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

    LINKS_TEMPLATE = """# 🌉 Multi-Repo Context Bridge
This file tracks sister repositories within the same workspace to allow for cross-repo intelligence.

## 📁 Sibling Repositories
{sibling_repos}

## 📜 Usage
The AI Agent is authorized to read rules and tech stacks from these directories to maintain architectural synchronization across the workspace.
"""

    SENTINEL_PY = """#!/usr/bin/env python3
# 🛡️ Antigravity Sentinel (v1.7.0)
import os
import subprocess
import sys

CRITICAL_FILES = [".env", ".agent/rules/", "antigravity_master_setup.py", "SECURITY.md"]

def run_audit():
    print("🛡️ Sentinel: Security-critical change detected. Running /doctor audit...")
    result = subprocess.run(["python", "antigravity_master_setup.py", "--doctor", ".", "--fix"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("❌ Sentinel: Audit failed. Check security constraints.")
        # sys.exit(1) # Uncomment to block commits if audit fails

if __name__ == "__main__":
    run_audit()
"""

    EVOLUTION_TEMPLATE = """# 🧬 Evolution Log: Autonomous Refactoring
Track background refactoring tasks and legacy code migrations here.

## 📋 Active Tasks
| Task ID | Component | Status | Target Rule |
| :--- | :--- | :--- | :--- |
| EVO-001 | Example Module | Pending | Rule 05 |

## 📜 Methodology
1. **Register:** Create a task in this log.
2. **Execute:** Run `/evolve` to apply changes incrementally.
3. **Verify:** Run `/review` to ensure no regressions.
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

    GITHUB_CI_TEMPLATE = """name: CI
on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
      - name: Lint with Ruff
        run: |
          pip install ruff
          ruff check .
      - name: Test with pytest
        run: |
          pip install pytest
          pytest
"""

    GITEA_CI_TEMPLATE = """name: Gitea Action CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - name: Run Build
        run: echo "Building..."
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
        "00_identity.md": """---
layer: 0
type: identity
priority: mandatory
---
# System Identity
You are a Senior Polyglot Software Engineer and Product Architect.
- **Safety:** Never delete data without asking. Never leak secrets.
- **Context:** Always check `docs/imported` and `context/raw` before coding.
- **Dynamic Optimization:** You are expected to keep `docs/TECH_STACK.md` and `.agent/memory/scratchpad.md` updated as the project evolves.
- **Self-Correction:** You are authorized to propose updates to your own rules in `.agent/rules/` if you identify architectural drift or improved patterns.
""",
        "02_security.md": """---
layer: 0
type: protocol
priority: mandatory
---
# Security Protocols
1. **Secrets:** Never output API keys. Use `.env`.
2. **Inputs:** Validate all inputs.
3. **Dependencies:** Warn if using deprecated libraries.
""",
        "03_git.md": """---
layer: 1
type: workflow
priority: standard
---
# Git Conventions
- Use Conventional Commits (`feat:`, `fix:`, `docs:`).
- Never commit to main without testing.
""",
        "04_reasoning.md": """---
layer: 1
type: cognition
priority: mandatory
---
# Reasoning Protocol
1. **Pause:** Analyze the request.
2. **Plan:** Break it down step-by-step.
3. **Check:** Verify against `docs/` constraints.
4. **Execute:** Write code.
""",
        RULE_ARCHITECTURE: """---
layer: 2
type: persona
priority: expert
---
# Architecture Expert Persona
Focus on SoC (Separation of Concerns), DRY (Don't Repeat Yourself), and SOLID principles.
Always prioritize modularity and testability in system design.
""",
        "06_ux.md": """---
layer: 2
type: persona
priority: expert
---
# UX Specialist Persona
Focus on user flow, accessibility (a11y), and intuitive interface design.
Ensure that all interactive elements have clear feedback and state representation.
""",
        RULE_SECURITY_EXPERT: """---
layer: 2
type: persona
priority: expert
---
# Security Hardening Persona
Conduct deep audits for OWASP Top 10 vulnerabilities.
Enforce strict validation, sanitization, and least-privilege principles.
""",
        "08_boundaries.md": """---
layer: 0
type: safety
priority: mandatory
---
# Workspace Boundary Enforcement
1. **Absolute Path Restriction:** You are strictly forbidden from reading, writing, or executing anything outside of the current project root directory.
2. **Command Safety:** Before running any command, verify it does not attempt to access `../` or absolute system paths like `/etc/` or `C:\\Windows\\`.
3. **Environment Isolation:** Do not attempt to modify system-level configurations, install non-project global dependencies, or access files in other workspaces unless explicitly authorized.
4. **Data Integrity:** Never delete files or move them outside the project boundaries.
""",
        "09_cross_repo.md": """---
layer: 1
type: context
priority: standard
---
# Multi-Repo Context Bridge
1. **Sister Repositories:** Refer to `context/links.md` for a list of related repositories in the same scratch space.
2. **Knowledge Sharing:** You are authorized to read `.agent/rules/` and `docs/TECH_STACK.md` from linked repositories to ensure architectural consistency.
3. **Dependency Mapping:** If a linked repository is a dependency (e.g., a shared library), prioritize its interface definitions over assumptions.
4. **No Mutation:** You may READ from sister repos, but never WRITE to them unless explicitly instructed to perform a cross-repo refactor.
""",
        "10_evolution.md": """---
layer: 1
type: protocol
priority: standard
---
# Autonomous Evolution Protocols
1. **Task Registration:** Before starting a background refactor, register the "Evolution Task" in `.agent/memory/evolution.md`.
2. **Incrementalism:** Never refactor an entire module at once. Apply changes in atomic steps (one function or class at a time).
3. **Regression Testing:** After every evolution step, you MUST run existing tests. If tests fail, ROLL BACK immediately.
4. **Rule Alignment:** The primary goal of evolution is to bring legacy code into compliance with the latest `.agent/rules/`.
""",
        "99_model_dispatch.md": """---
layer: 0
type: cognition
priority: safety
---
# Model Dispatch Protocol
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
        "sync.md": """---
trigger: /sync
---
# Semantic Sync Workflow
1. Scan `src/` and `docs/` for recent changes.
2. Cross-reference with `docs/TECH_STACK.md` and `.agent/rules/`.
3. If inconsistencies are found, update the documentation or propose rule changes.
4. Update `.agent/memory/scratchpad.md` with the latest project heartbeat.
""",
        "evolve.md": """---
trigger: /evolve
---
# Autonomous Evolution Workflow
1. Read `.agent/memory/evolution.md` for active tasks.
2. Select the highest priority 'Pending' task.
3. Apply refactoring according to Rule 10.
4. Verify with tests and update task status to 'Completed'.
""",
        "help.md": """---
trigger: /help
---
# Agent Help
Available Commands:
- `/plan`: Generate tasks from specs.
- `/bootstrap`: Create project skeleton.
- `/review`: Audit code quality/security.
- `/commit`: Smart commit message generator.
- `/save`: Update project memory.
- `/sync`: Harmonize docs, rules, code, and memory.
- `/evolve`: Background refactoring and tech-debt reduction.
- `/doctor`: Run automated health audit.
- `/help`: Show this guide.
""",
        "doctor.md": """---
trigger: /doctor
---
# Self-Doctor Workflow
1. Run the system `doctor` command.
2. Analyze report for missing files or rules.
3. Propose fixes and execute them using available skills.
""",
    }

    # Blueprint Definitions
    BLUEPRINTS: dict[str, dict[str, list[str]]] = {
        "audio": {
            "dirs": ["src/audio", "src/dsp", "resources/samples"],
            "stack": ["python", "numpy", "scipy", "librosa"],
            "rules": [RULE_ARCHITECTURE],
        },
        "medical": {
            "dirs": ["src/encryption", "src/hipaa", "docs/compliance"],
            "stack": ["python", "cryptography", "postgres"],
            "rules": [RULE_SECURITY, RULE_SECURITY_EXPERT],
        },
        "performance": {
            "dirs": ["src/benchmarks", "src/opt"],
            "stack": ["python", "rust"],
            "rules": [RULE_ARCHITECTURE],
        },
        "nextjs": {
            "dirs": ["app", "components", "lib", "public", "styles"],
            "stack": ["nextjs", "react", "tailwind", "typescript"],
            "rules": [RULE_ARCHITECTURE],
        },
        "fastapi": {
            "dirs": ["app/api", "app/core", "app/models", "app/schemas", "tests"],
            "stack": ["python", "fastapi", "pydantic", "sqlalchemy"],
            "rules": [RULE_ARCHITECTURE],
        },
        "go-fiber": {
            "dirs": ["cmd/server", "internal/handlers", "internal/models", "internal/routes", "pkg/utils"],
            "stack": ["go", "fiber", "gorm", "docker"],
            "rules": [RULE_ARCHITECTURE],
        },
        "rust-axum": {
            "dirs": ["src/handlers", "src/models", "src/routes", "src/utils", "tests"],
            "stack": ["rust", "axum", "tokio", "serde"],
            "rules": [RULE_ARCHITECTURE],
        },
    }

    # Mermaid Templates
    MERMAID_PROJECT_MAP = """graph TD
    Root["{project_name}"] --> Agent[".agent/"]
    Root --> Docs["docs/"]
    Root --> Src["src/"]
    Root --> Context["context/"]

    Agent --> Rules[".agent/rules/"]
    Agent --> Workflows[".agent/workflows/"]
    Agent --> Skills[".agent/skills/"]
    Agent --> Memory[".agent/memory/"]

    Rules --> R00["Identity"]
    Rules --> R01["Stack"]
    Rules --> R02["Security"]

    Memory --> Scratch["scratchpad.md"]
    Memory --> Grave["graveyard.md"]
"""

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
        "bridge/bridge.py": """# Antigravity Skill Bridge
# Standardized execution runner for AI agent skills.
import os
import subprocess

def run_skill(command):
    return subprocess.run(command, shell=True, capture_output=True, text=True)
""",
    }

    DEVCONTAINER_JSON = """{
  "name": "Antigravity Universal",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": { "ghcr.io/devcontainers/features/common-utils:2": {} }
}
"""

    VSCODE_EXTENSIONS_MAP: dict[str, list[str]] = {
        "python": ["ms-python.python", "ms-python.vscode-pylance", "charliermarsh.ruff"],
        "node": [EXT_ESLINT, EXT_PRETTIER],
        "javascript": [EXT_ESLINT, EXT_PRETTIER],
        "typescript": [EXT_ESLINT, EXT_PRETTIER],
        "docker": ["ms-azuretools.vscode-docker"],
        "react": ["dsznajder.es7-react-js-snippets"],
        "general": [
            "donjayamanne.githistory",
            "eamodio.gitlens",
            "usernamehw.errorlens",
            "pkief.material-icon-theme",
            "christian-kohler.path-intellisense",
        ],
    }

    VSCODE_SETTINGS_TEMPLATE = """{{
    "files.exclude": {{
        "**/.git": true,
        "**/.svn": true,
        "**/.hg": true,
        "**/CVS": true,
        "**/.DS_Store": true,
        "**/Thumbs.db": true,
        ".agent/**": false,
        "context/**": false
    }},
    "files.watcherExclude": {{
        "**/.git/objects/**": true,
        "**/.git/subtree-cache/**": true,
        "**/node_modules/*/**": true,
        "**/.venv/**": true,
        "**/.agent/**": true
    }},
    "search.exclude": {{
        "**/node_modules": true,
        "**/bower_components": true,
        "**/.venv": true,
        "**/.agent": true
    }},
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "{default_formatter}",
    "editor.bracketPairColorization.enabled": true,
    "editor.guides.bracketPairs": "active",
    "files.trimTrailingWhitespace": true,
    "editor.rulers": [
        80,
        120
    ],
    "[python]": {{
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.codeActionsOnSave": {{
            "source.organizeImports": "explicit"
        }}
    }},
    "editor.semanticHighlighting.enabled": true,
    "editor.inlineSuggest.enabled": true,
    "terminal.integrated.fontSize": 14,
    "workbench.colorCustomizations": {{
        "statusBar.background": "#1e1e1e",
        "statusBar.foreground": "#ffffff"
    }}
}}"""

    VSCODE_SNIPPETS_TEMPLATE = """{{
    "Antigravity Agent Commands": {{
        "prefix": "/",
        "body": [
            "/{1|plan,sync,save,review,commit,doctor,help|}"
        ],
        "description": "Quick access to Antigravity Agent commands"
    }}
}}"""

    PROFESSIONAL_README_TEMPLATE = """# {project_name}

[![Version](https://img.shields.io/badge/version-1.0.0-brightgreen.svg)]()
[![Stack](https://img.shields.io/badge/stack-{tech_stack}-blue.svg)]()

## 🚀 Overview
{project_name} is an AI-first project bootstrapped with **Antigravity Architect**.

## ✨ Features
- **Agent Optimized**: Built-in rules and workflows for AI agents.
- **Multi-Platform**: Native support for **GitHub**, **Gitea**, **VS Code**, and **Project IDX**.
- **Production Ready**: Includes CI/CD boilerplates and community standards.

## 🛠️ Tech Stack
- **Primary**: {tech_stack}
- **Architecture Details**: See `docs/TECH_STACK.md` for deep-dive details.

## 🤖 AI Agent Guide
To start working with an AI agent in this repo:
1. Open the project in your IDE.
2. Read `BOOTSTRAP_INSTRUCTIONS.md`.
3. Use `/help` to see available agent commands.

## 📂 Project Structure
- `.agent/`: AI Agent rules, memory, and workflows.
- `.github/` & `.gitea/`: Platform-specific CI/CD and templates.
- `src/`: Core source code.
- `docs/`: Project documentation and `TECH_STACK.md`.
- `context/`: Raw specifications and brain dumps.

## 📄 License
This project is licensed under the MIT License.
"""

    VSCODE_LAUNCH_TEMPLATE = """{{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    "version": "0.2.0",
    "configurations": [
{configurations}
    ]
}}"""

    VSCODE_TASKS_TEMPLATE = """{{
    "version": "2.0.0",
    "tasks": [
{tasks}
    ]
}}"""


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

        # Use force=True to allow re-configuring logging (Python 3.8+)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(log_path, mode="w", encoding="utf-8"),
                logging.StreamHandler(sys.stdout),
            ],
            force=True,
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

    @staticmethod
    def save_preset(name: str, args: dict) -> bool:
        """Saves current CLI arguments as a named preset."""
        try:
            path = AntigravityResources.PRESETS_DIR / f"{name}.json"
            os.makedirs(path.parent, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(args, f, indent=4)
            logging.info(f"💾 Preset saved: {name}")
            return True
        except Exception as e:
            logging.error(f"❌ Error saving preset {name}: {e}")
            return False

    @staticmethod
    def load_preset(name: str) -> dict | None:
        """Loads a preset by name."""
        try:
            path = AntigravityResources.PRESETS_DIR / f"{name}.json"
            if not path.exists():
                logging.error(f"❌ Preset not found: {name}")
                return None
            with open(path, encoding="utf-8") as f:
                data: dict[Any, Any] = json.load(f)
                return data
        except Exception as e:
            logging.error(f"❌ Error loading preset {name}: {e}")
            return None

    @staticmethod
    def list_presets() -> list[str]:
        """Lists available presets."""
        try:
            if not AntigravityResources.PRESETS_DIR.exists():
                return []
            return [f.stem for f in AntigravityResources.PRESETS_DIR.glob("*.json")]
        except Exception as e:
            logging.error(f"❌ Error listing presets: {e}")
            return []

    @staticmethod
    def fetch_remote_blueprint(url: str) -> dict | None:
        """
        Fetches a remote blueprint via git clone.
        Expects a 'antigravity_blueprint.json' in the repo root.
        """
        temp_dir = Path(tempfile.mkdtemp(prefix="antigravity_blueprint_"))
        try:
            logging.info(f"⬇️  Fetching remote blueprint: {url}")
            subprocess.check_call(
                ["git", "clone", "--depth", "1", url, str(temp_dir)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            blueprint_path = temp_dir / "antigravity_blueprint.json"
            if not blueprint_path.exists():
                logging.error("❌ Remote repo missing 'antigravity_blueprint.json'")
                return None

            with open(blueprint_path, encoding="utf-8") as f:
                data: dict[Any, Any] = json.load(f)
                logging.info(f"✅ Loaded remote blueprint: {data.get('name', 'Unknown')}")
                return data

        except subprocess.CalledProcessError:
            logging.error(f"❌ Failed to clone {url}")
            return None
        except Exception as e:
            logging.error(f"❌ Error fetching blueprint: {e}")
            return None
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


# Maintain backward compatibility with module-level functions
setup_logging = AntigravityEngine.setup_logging
sanitize_name = AntigravityEngine.sanitize_name
parse_keywords = AntigravityEngine.parse_keywords
validate_file_path = AntigravityEngine.validate_file_path
write_file = AntigravityEngine.write_file
append_file = AntigravityEngine.append_file
create_folder = AntigravityEngine.create_folder
save_preset = AntigravityEngine.save_preset
load_preset = AntigravityEngine.load_preset
list_presets = AntigravityEngine.list_presets


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
1. **Source of Truth:** Always refer to `docs/TECH_STACK.md` for architectural deep-dives.
2. **Inference:** Assume standard frameworks for these keywords (e.g., React implies standard hooks/components).
3. **Tooling:** Use the standard CLI tools (pip, npm, cargo, go mod).
4. **Files:** Look for `pyproject.toml`, `package.json`, or similar to confirm versions.
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

    @staticmethod
    def build_vscode_config(keywords: list[str]) -> dict[str, str]:
        """Builds all .vscode/ configuration files."""
        extensions = []

        # Map framework aliases
        keyword_aliases = {
            "js": "javascript",
            "ts": "typescript",
            "nextjs": "react",
            "fastapi": "python",
            "django": "python",
            "flask": "python",
        }

        # Extensions
        extensions.extend(AntigravityResources.VSCODE_EXTENSIONS_MAP["general"])

        default_formatter = "none"

        for k in keywords:
            key = keyword_aliases.get(k, k)
            if key in AntigravityResources.VSCODE_EXTENSIONS_MAP:
                extensions.extend(AntigravityResources.VSCODE_EXTENSIONS_MAP[key])

            if key == "python":
                default_formatter = "charliermarsh.ruff"
            elif key in ("javascript", "typescript", "react", "node") and default_formatter == "none":
                default_formatter = AntigravityResources.EXT_PRETTIER

        extensions = sorted(set(extensions))

        files = {}
        files["extensions.json"] = json.dumps({"recommendations": extensions}, indent=4)
        files["settings.json"] = AntigravityResources.VSCODE_SETTINGS_TEMPLATE.format(
            default_formatter=default_formatter
        )
        files["launch.json"] = AntigravityResources.VSCODE_LAUNCH_TEMPLATE.format(configurations="")
        files["tasks.json"] = AntigravityResources.VSCODE_TASKS_TEMPLATE.format(tasks="")
        files["antigravity.code-snippets"] = AntigravityResources.VSCODE_SNIPPETS_TEMPLATE

        return files

    @staticmethod
    def build_docs_index(docs_dir: str) -> str:
        """Generates a summary index of all files in docs/imported."""
        content = "# Documentation Index\n\n"
        if not os.path.exists(docs_dir):
            return content + "_No documents imported yet._"

        files = sorted(os.listdir(docs_dir))
        if not files:
            return content + "_No documents imported yet._"

        content += "## Assimilated Knowledge\n"
        for f in files:
            if f.endswith(".md") and f != "INDEX.md":
                title = f.replace(".md", "").replace("_", " ").title()
                content += f"- [{title}]({f})\n"
        return content

    @staticmethod
    def build_architecture_diagram(project_name: str) -> str:
        """Builds a Mermaid diagram of the project structure."""
        return AntigravityResources.MERMAID_PROJECT_MAP.format(project_name=project_name)

    @staticmethod
    def build_links(project_name: str) -> str:
        """Scan parent directory for other projects and build context/links.md."""
        parent_dir = Path(os.getcwd())
        siblings = []

        try:
            for item in parent_dir.iterdir():
                if item.is_dir() and item.name != project_name:
                    # Check if it's an Antigravity project
                    if (item / ".agent").exists():
                        siblings.append(f"- **{item.name}** (linked: `../{item.name}`) - *Antigravity Project*")
                    elif (item / ".git").exists():
                        siblings.append(f"- **{item.name}** (linked: `../{item.name}`) - *Git Repository*")
        except Exception as e:
            logging.debug(f"Error scanning for siblings: {e}")

        sibling_str = "\n".join(siblings) if siblings else "_No sibling repositories detected in this scratch space._"
        return AntigravityResources.LINKS_TEMPLATE.format(sibling_repos=sibling_str)


# Maintain backward compatibility with module-level functions
build_gitignore = AntigravityBuilder.build_gitignore
build_nix_config = AntigravityBuilder.build_nix_config
build_tech_stack_rule = AntigravityBuilder.build_tech_stack_rule
build_scratchpad = AntigravityBuilder.build_scratchpad
build_vscode_config = AntigravityBuilder.build_vscode_config


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
    def detect_tech_stack(text: str) -> list[str]:
        """
        Intelligently detects technology keywords using primary keys and aliases.
        """
        detected = set()
        text_lower = text.lower()

        # Check primary keywords from mappings
        primary_sources = set(AntigravityResources.GITIGNORE_MAP.keys()) | set(
            AntigravityResources.NIX_PACKAGE_MAP.keys()
        )

        for k in primary_sources:
            if re.search(r"\b" + re.escape(k) + r"\b", text_lower):
                detected.add(k)

        # Check aliases for deeper detection
        for primary, aliases in AntigravityResources.TECH_ALIASES.items():
            for alias in aliases:
                if re.search(r"\b" + re.escape(alias) + r"\b", text_lower):
                    detected.add(primary)
                    break

        return list(detected)

    @staticmethod
    def build_tech_deep_dive(keywords: list[str], full_text: str) -> str:
        """
        Generates a deep-dive TECH_STACK.md based on detected keywords and text analysis.
        """
        content = "# 🛠️ Technical Stack Deep-Dive\n\n"
        content += "## 🚀 Primary Technologies\n"
        for k in sorted(keywords):
            content += f"- **{k.title()}**\n"

        content += "\n## 🔍 Contextual Observations\n"
        text_lower = full_text.lower()

        observation_map = {
            "architecture": "Structural architectural specifications detected.",
            "security": "Security-sensitive components or requirements identified.",
            "auth": "Security-sensitive components or requirements identified.",
            "database": "Data persistence layers identified.",
            "sql": "Data persistence layers identified.",
            "api": "API surfaces or integrations identified.",
            "endpoint": "API surfaces or integrations identified.",
        }

        observations = set()
        for key, obs in observation_map.items():
            if key in text_lower:
                observations.add(obs)

        if observations:
            for obs in sorted(observations):
                content += f"- {obs}\n"
        else:
            content += "- Standard project structure with generic tech stack.\n"

        content += "\n## ⚠️ Technical Debt & Tracking\n"
        debt_keywords = ["todo", "fixme", "refactor", "deprecated", "legacy", "optimization needed"]
        debts = [k for k in debt_keywords if k in text_lower]

        if debts:
            content += "Potential technical debt or optimization areas identified:\n"
            for d in debts:
                content += f"- {d.title()}\n"
        else:
            content += "No immediate technical debt keywords identified in source documents.\n"

        content += "\n## 🤖 Agent Interaction Map\n"
        content += "Agents should prioritize rules in `.agent/rules/` and use `TECH_STACK.md` as the primary architectural reference.\n"

        return content

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

        logging.info(f"🧠 Assimilating knowledge from: {filepath}...")

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
        detected_keywords = AntigravityAssimilator.detect_tech_stack(full_text)
        logging.info(f"🔍 Detected Tech Stack from Source: {', '.join(detected_keywords)}")

        # 3. Generate TECH_STACK.md (The Documentation Genie)
        tech_stack_path = os.path.join(base_dir, "docs", "TECH_STACK.md")
        tech_stack_content = AntigravityAssimilator.build_tech_deep_dive(detected_keywords, full_text)
        write_file(tech_stack_path, tech_stack_content, exist_ok=True)

        # 4. Split & Distribute
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

        logging.info("🧠 Assimilation Complete.")
        return detected_keywords


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
    def generate_agent_files(base_dir: str, project_name: str, keywords: list[str], safe_mode: bool = False) -> None:
        """Generates all .agent/ rules, workflows, and skills."""

        # v1.6.2 Standardized Agent API Manifest
        manifest_path = os.path.join(base_dir, AGENT_DIR, AntigravityResources.AGENT_MANIFEST)
        manifest_content = AntigravityResources.AGENT_MANIFEST_TEMPLATE.format(project_name=project_name)
        write_file(manifest_path, manifest_content, exist_ok=safe_mode)

        # Generate static rules
        for filename, content in AntigravityResources.AGENT_RULES.items():
            path = os.path.join(base_dir, AGENT_DIR, "rules", filename)
            write_file(path, content, exist_ok=safe_mode)

        # Generate dynamic tech stack rule
        tech_stack_path = os.path.join(base_dir, AGENT_DIR, "rules", AntigravityResources.RULE_TECH_STACK)
        write_file(tech_stack_path, build_tech_stack_rule(keywords), exist_ok=safe_mode)

        # Generate workflows
        for filename, content in AntigravityResources.AGENT_WORKFLOWS.items():
            path = os.path.join(base_dir, AGENT_DIR, "workflows", filename)
            write_file(path, content, exist_ok=safe_mode)

        # Generate skills
        for filename, content in AntigravityResources.AGENT_SKILLS.items():
            path = os.path.join(base_dir, AGENT_DIR, "skills", filename)
            write_file(path, content, exist_ok=safe_mode)

        # v1.6.2 Consolidated Memory Generation
        scratchpad_path = os.path.join(base_dir, AGENT_DIR, "memory", "scratchpad.md")
        write_file(scratchpad_path, build_scratchpad(keywords, False), exist_ok=safe_mode)

        write_file(
            os.path.join(base_dir, AGENT_DIR, "memory", "graveyard.md"),
            AntigravityResources.GRAVEYARD_TEMPLATE,
            exist_ok=safe_mode,
        )
        write_file(
            os.path.join(base_dir, AGENT_DIR, "memory", "evolution.md"),
            AntigravityResources.EVOLUTION_TEMPLATE,
            exist_ok=safe_mode,
        )

        # v1.6.2 Sentinel Protection Script
        write_file(
            os.path.join(base_dir, "scripts", "sentinel.py"), AntigravityResources.SENTINEL_PY, exist_ok=safe_mode
        )

    @staticmethod
    def _resolve_blueprint(blueprint: str | None) -> dict:
        """Helper to resolve blueprint data from name or URL."""
        if not blueprint:
            return {}

        if blueprint.startswith("http://") or blueprint.startswith("https://"):
            return AntigravityEngine.fetch_remote_blueprint(blueprint) or {}

        return AntigravityResources.BLUEPRINTS.get(blueprint, {})

    @staticmethod
    def generate_community_standards(base_dir: str, safe_mode: bool = False) -> None:
        """Generates standard legal and community files."""
        files = {
            AntigravityResources.CHANGELOG_FILE: AntigravityResources.CHANGELOG_TEMPLATE,
            AntigravityResources.CONTRIBUTING_FILE: AntigravityResources.CONTRIBUTING_TEMPLATE,
            AntigravityResources.AUDIT_FILE: AntigravityResources.AUDIT_TEMPLATE,
            AntigravityResources.SECURITY_FILE: AntigravityResources.SECURITY_TEMPLATE,
            AntigravityResources.CODE_OF_CONDUCT_FILE: AntigravityResources.CODE_OF_CONDUCT_TEMPLATE,
        }
        for filename, content in files.items():
            write_file(os.path.join(base_dir, filename), content, exist_ok=safe_mode)

    @staticmethod
    def generate_github_templates(base_dir: str, final_stack: list[str], safe_mode: bool = False) -> None:
        """Generates GitHub-specific templates and workflows."""
        github_dir = os.path.join(base_dir, ".github")
        workflow_dir = os.path.join(github_dir, "workflows")
        create_folder(workflow_dir)

        issue_template_dir = os.path.join(github_dir, "ISSUE_TEMPLATE")
        create_folder(issue_template_dir)

        templates = {
            os.path.join(issue_template_dir, "bug_report.md"): AntigravityResources.GITHUB_BUG_REPORT,
            os.path.join(issue_template_dir, "feature_request.md"): AntigravityResources.GITHUB_FEATURE_REQUEST,
            os.path.join(issue_template_dir, "question.md"): AntigravityResources.GITHUB_QUESTION,
            os.path.join(issue_template_dir, "config.yml"): AntigravityResources.GITHUB_ISSUE_CONFIG,
            os.path.join(github_dir, "PULL_REQUEST_TEMPLATE.md"): AntigravityResources.GITHUB_PR_TEMPLATE,
            os.path.join(github_dir, "FUNDING.yml"): AntigravityResources.GITHUB_FUNDING,
            os.path.join(
                github_dir, "copilot-instructions.md"
            ): AntigravityResources.GITHUB_COPILOT_INSTRUCTIONS.format(tech_stack=", ".join(final_stack)),
            os.path.join(workflow_dir, "ci.yml"): AntigravityResources.GITHUB_CI_TEMPLATE,
        }
        for path, content in templates.items():
            write_file(path, content, exist_ok=safe_mode)

    @staticmethod
    def _handle_safe_mode(project_name: str, base_dir: str, safe_mode: bool | None) -> bool | None:
        """Handles user interaction for existing project directories."""
        if safe_mode is None and os.path.exists(base_dir):
            print(f"\n⚠️  Project '{project_name}' already exists.")
            choice = input("Select mode: [U]pdate (Safe) / [O]verwrite (Risky) / [C]ancel: ").lower()

            if choice == "u":
                print("🛡️  Safe Update Mode Active: Only missing files will be created.")
                return True
            elif choice == "o":
                confirm = input("💥 WARNING: This will overwrite files. Type 'yes' to confirm: ")
                if confirm.lower() != "yes":
                    return None  # Cancel
                return False
            else:
                return None  # Cancel
        elif safe_mode is None:
            return False
        return safe_mode

    @staticmethod
    def _get_directory_structure(blueprint_data: dict) -> list[str]:
        """Returns the list of directories to create."""
        directories = [
            "src",
            "tests",
            "docs/imported",
            "context/raw",
            AntigravityResources.VSCODE_DIR,
            AntigravityResources.IDX_DIR,
            AntigravityResources.DEVCONTAINER_DIR,
            AntigravityResources.GITEA_DIR,
            f"{AntigravityResources.GITEA_DIR}/workflows",
            ".github/workflows",
            f"{AGENT_DIR}/rules",
            f"{AGENT_DIR}/workflows",
            f"{AGENT_DIR}/skills",
            f"{AGENT_DIR}/memory",
            f"{AGENT_DIR}/skills/git_automation",
            f"{AGENT_DIR}/skills/secrets_manager",
            f"{AGENT_DIR}/skills/bridge",
            "scripts",
        ]
        if blueprint_data:
            directories.extend(blueprint_data.get("dirs", []))
        return directories

    @staticmethod
    def _inherit_global_rules(base_dir: str, safe_mode: bool) -> None:
        """Copies global rules from ~/.antigravity/rules if they exist."""
        global_agent_rules = Path.home() / ".antigravity" / "rules"
        if global_agent_rules.exists():
            logging.info("🌐 Inheriting Global Rules from ~/.antigravity")
            for rule_file in global_agent_rules.glob("*.md"):
                dest_path = os.path.join(base_dir, AGENT_DIR, "rules", f"global_{rule_file.name}")
                with open(rule_file, encoding="utf-8") as rf:
                    write_file(dest_path, rf.read(), exist_ok=safe_mode)

    @staticmethod
    def _generate_core_config_files(base_dir: str, project_name: str, final_stack: list[str], safe_mode: bool) -> None:
        """Generates core configuration files like .gitignore, README, env, etc."""
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
            AntigravityResources.PROFESSIONAL_README_TEMPLATE.format(
                project_name=project_name, tech_stack=", ".join(final_stack)
            ),
            exist_ok=True,
        )
        write_file(
            os.path.join(base_dir, AntigravityResources.ENV_EXAMPLE_FILE), "API_KEY=\nDB_URL=", exist_ok=safe_mode
        )
        # Bridge and Architecture docs
        write_file(
            os.path.join(base_dir, AGENT_DIR, "skills", "bridge", "bridge.py"),
            AntigravityResources.AGENT_SKILLS["bridge/bridge.py"],
            exist_ok=safe_mode,
        )
        write_file(
            os.path.join(base_dir, "docs", "ARCHITECTURE.md"),
            AntigravityResources.MERMAID_PROJECT_MAP.format(project_name=project_name),
            exist_ok=safe_mode,
        )
        write_file(
            os.path.join(base_dir, "context", "links.md"),
            AntigravityBuilder.build_links(project_name),
            exist_ok=safe_mode,
        )
        # 4. Semantic RAG Index
        write_file(
            os.path.join(base_dir, "docs", "imported", "INDEX.md"),
            AntigravityBuilder.build_docs_index(os.path.join(base_dir, "docs", "imported")),
            exist_ok=True,
        )
        # Bootstrap Guide
        write_file(
            os.path.join(base_dir, AntigravityResources.BOOTSTRAP_FILE),
            """# Agent Start Guide

1. **Protocol:** Review `.agent/manifest.json` for project structure.
2. **Context:** Read `.agent/memory/scratchpad.md` and `.agent/memory/evolution.md`.
3. **Safety:** Ensure `scripts/sentinel.py` is running for monitoring.
4. **Action:** Use `/plan` to break down tasks or `/bootstrap` for code generation.
5. **Standards:** Follow the v2.0.0 Agent Protocol in `.agent/rules/`.
""",
            exist_ok=safe_mode,
        )

    @staticmethod
    def _generate_license(base_dir: str, license_type: str, safe_mode: bool) -> None:
        """Generates the LICENSE file."""
        license_content = AntigravityResources.LICENSE_TEMPLATES.get(
            license_type, AntigravityResources.LICENSE_TEMPLATES["mit"]
        )
        if license_type == "mit":
            license_content = license_content.format(year=datetime.now().year, author="pkeffect")
        write_file(os.path.join(base_dir, AntigravityResources.LICENSE_FILE), license_content, exist_ok=safe_mode)

    @staticmethod
    def _setup_git_hooks(base_dir: str) -> None:
        """Sets up the post-commit git hook."""
        git_dir = os.path.join(base_dir, ".git")
        if os.path.exists(git_dir):
            hook_path = os.path.join(git_dir, "hooks", "post-commit")
            hook_content = "#!/usr/bin/env python3\n# Antigravity Time-Travel hook\nimport os\nprint('🌌 Antigravity: Syncing session memory...')\n"
            try:
                with open(hook_path, "w", encoding="utf-8") as hf:
                    hf.write(hook_content)
                os.chmod(hook_path, 0o755)
            except Exception:
                pass

    @staticmethod
    def _generate_vscode_config(base_dir: str, final_stack: list[str], safe_mode: bool = False) -> None:
        """Generates VS Code configuration files."""
        vscode_files = build_vscode_config(final_stack)
        for filename, content in vscode_files.items():
            write_file(os.path.join(base_dir, AntigravityResources.VSCODE_DIR, filename), content, exist_ok=safe_mode)

    @staticmethod
    def _apply_blueprint_rules(base_dir: str, blueprint_data: dict) -> None:
        """Applies agent rules defined in the blueprint."""
        if not blueprint_data:
            return

        for rule in blueprint_data.get("rules", []):
            if rule in AntigravityResources.AGENT_RULES:
                write_file(
                    os.path.join(base_dir, AGENT_DIR, "rules", rule),
                    AntigravityResources.AGENT_RULES[rule],
                    exist_ok=False,
                )

    @staticmethod
    def generate_project(
        project_name: str,
        keywords: list[str],
        brain_dump_path: str | None = None,
        safe_mode: bool | None = None,
        custom_templates: dict[str, dict[str, str]] | None = None,
        license_type: str = "mit",
        blueprint: str | None = None,
    ) -> bool:
        """
        Main project generation logic (v1.6.0 Orchestration).
        """
        base_dir = os.path.join(os.getcwd(), project_name)

        # Handle safe_mode
        safe_mode_result = AntigravityGenerator._handle_safe_mode(project_name, base_dir, safe_mode)
        if safe_mode_result is None:
            return False
        safe_mode = safe_mode_result

        logging.info(f"🚀 Constructing '{project_name}' (v1.6.1)...")

        # Setup logging in target directory
        setup_logging(base_dir)

        # 1. Blueprint Application (Ancestry Override)
        blueprint_data = AntigravityGenerator._resolve_blueprint(blueprint)

        if blueprint_data:
            logging.info(f"💎 Applying Blueprint: {blueprint_data.get('name', blueprint)}")
            keywords.extend(blueprint_data.get("stack", []))

        # Create directory structure
        directories = AntigravityGenerator._get_directory_structure(blueprint_data)
        for d in directories:
            create_folder(os.path.join(base_dir, d))

        # Process brain dump
        detected_stack: list[str] = []
        if brain_dump_path:
            detected_stack = process_brain_dump(brain_dump_path, base_dir)

        # Merge keywords
        final_stack = list(set(keywords + detected_stack))
        if not final_stack:
            final_stack = ["linux"]
        logging.info(f"⚙️  Final Tech Stack: {', '.join(final_stack)}")

        # 2. Inheritance: Copy global rules
        AntigravityGenerator._inherit_global_rules(base_dir, safe_mode)

        # Generate configuration files
        AntigravityGenerator._generate_core_config_files(base_dir, project_name, final_stack, safe_mode)

        # Generate License
        AntigravityGenerator._generate_license(base_dir, license_type, safe_mode)

        # Community Standards
        AntigravityGenerator.generate_community_standards(base_dir, safe_mode=safe_mode)

        # GitHub Templates
        AntigravityGenerator.generate_github_templates(base_dir, final_stack, safe_mode=safe_mode)

        # VS Code Configuration
        AntigravityGenerator._generate_vscode_config(base_dir, final_stack, safe_mode)

        # Agent files
        AntigravityGenerator.generate_agent_files(base_dir, project_name, final_stack, safe_mode=safe_mode)

        # Apply Blueprint Rules
        AntigravityGenerator._apply_blueprint_rules(base_dir, blueprint_data)

        # Time-Travel: Git Initialization hook
        AntigravityGenerator._setup_git_hooks(base_dir)

        print(f"\n✅ Project '{project_name}' ready (v1.6.0)!")
        print(f"📂 Location: {os.path.abspath(base_dir)}\n")
        return True


# Maintain backward compatibility with module-level functions
build_docs_index = AntigravityBuilder.build_docs_index
build_architecture_diagram = AntigravityBuilder.build_architecture_diagram
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
    parser.add_argument(
        "--blueprint",
        type=str,
        help="Apply a specialized project blueprint (built-in name or git URL)",
    )

    parser.add_argument("--save-preset", type=str, help="Save current arguments as a named preset")
    parser.add_argument("--preset", type=str, help="Load arguments from a saved preset")
    parser.add_argument("--list-presets", action="store_true", help="List all saved presets")
    parser.add_argument("--list-blueprints", action="store_true", help="List all built-in blueprints")

    return parser


def load_custom_templates(templates_path: str | None) -> dict[str, dict[str, str]]:
    """
    Load custom templates from a directory, merging with defaults.

    Returns a dict with keys 'rules', 'workflows', 'skills' containing template overrides.
    """
    if not templates_path:
        home_templates = Path.home() / AntigravityResources.ANTIGRAVITY_DIR_NAME / "templates"
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


def _doctor_check_dir(base_dir: Path, dir_path: str, fix: bool) -> tuple[str | None, str | None, str | None]:
    """Checks directory existence and optionally fixes it."""
    full_path = base_dir / dir_path
    if full_path.exists():
        return f"✅ {dir_path}/ exists", None, None

    msg = f"❌ Missing: {dir_path}/"
    fixed = None
    if fix:
        full_path.mkdir(parents=True, exist_ok=True)
        (full_path / ".gitkeep").touch()
        fixed = f"🔧 Created {dir_path}/"
    return None, msg, fixed


def _doctor_check_file(
    base_dir: Path, file_path: str, template: str | None, fix: bool, optional: bool = False
) -> tuple[str | None, str | None, str | None, str | None]:
    """Checks file health and optionally fixes it."""
    full_path = base_dir / file_path
    is_missing = not full_path.exists()
    is_empty = full_path.exists() and full_path.stat().st_size == 0

    passed, warning, issue, fixed_msg = None, None, None, None

    if not is_missing and not is_empty:
        return f"✅ {file_path} exists", None, None, None

    if is_missing:
        if optional:
            warning = f"⚠️  Optional: {file_path} not found"
        else:
            issue = f"❌ Missing: {file_path}"
    elif is_empty:
        warning = f"⚠️  {file_path} is empty"

    if fix and template:
        if is_missing:
            full_path.parent.mkdir(parents=True, exist_ok=True)

        # Only write if we're fixing missing or empty files
        full_path.write_text(template, encoding="utf-8")

        fixed_msg = f"🔧 Generated {file_path}" if is_missing else f"🔧 Restored content to {file_path}"

    return passed, warning, issue, fixed_msg


def _get_doctor_requirements() -> tuple[list[str], dict[str, tuple[str, str]]]:
    """Returns required directories and files for doctor check."""
    dirs = [
        ".agent/rules",
        ".agent/workflows",
        ".agent/skills",
        ".agent/memory",
    ]

    files = {
        f".agent/rules/{AntigravityResources.RULE_IDENTITY}": (
            "Agent identity rule",
            AntigravityResources.AGENT_RULES[AntigravityResources.RULE_IDENTITY],
        ),
        f".agent/rules/{AntigravityResources.RULE_SECURITY}": (
            "Security protocol",
            AntigravityResources.AGENT_RULES[AntigravityResources.RULE_SECURITY],
        ),
        ".agent/workflows/plan.md": (
            "Plan workflow",
            AntigravityResources.AGENT_WORKFLOWS["plan.md"],
        ),
        "antigravity_master_setup.py": (
            "Master script",
            "",
        ),  # Content empty implies no auto-fix for script itself
    }
    return dirs, files


def _get_doctor_optional_files() -> dict[str, tuple[str, str]]:
    """Returns optional files for doctor check."""
    files = [
        AntigravityResources.GITIGNORE_FILE,
        AntigravityResources.README_FILE,
        AntigravityResources.CHANGELOG_FILE,
        AntigravityResources.CONTRIBUTING_FILE,
        AntigravityResources.AUDIT_FILE,
        AntigravityResources.SECURITY_FILE,
        AntigravityResources.CODE_OF_CONDUCT_FILE,
        AntigravityResources.LICENSE_FILE,
    ]
    return dict.fromkeys(files, ("Optional project file", ""))


def _validate_doctor_dirs(base_dir: Path, dirs: list[str], fix: bool) -> tuple[list[str], list[str], list[str]]:
    """Validates and fixes directories."""
    passed, issues, fixed = [], [], []
    for d in dirs:
        p, i, f = _doctor_check_dir(base_dir, d, fix)
        if p:
            passed.append(p)
        if i:
            issues.append(i)
        if f:
            fixed.append(f)
    return passed, issues, fixed


def _validate_doctor_files(
    base_dir: Path, files: dict[str, tuple[str, str]], fix: bool
) -> tuple[list[str], list[str], list[str], list[str]]:
    """Validates and fixes files."""
    passed, warnings, issues, fixed = [], [], [], []
    for f_path, (_, tmpl) in files.items():
        # Optional file check logic can be expanded here if needed
        is_optional = False
        p, w, i, f = _doctor_check_file(base_dir, f_path, tmpl, fix, optional=is_optional)
        if p:
            passed.append(p)
        if w:
            warnings.append(w)
        if i:
            issues.append(i)
        if f:
            fixed.append(f)
    return passed, warnings, issues, fixed


def _print_doctor_results(passed: list[str], warnings: list[str], issues: list[str], fixed: list[str]) -> None:
    """Prints the results of the doctor check."""
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


def doctor_project(project_path: str, fix: bool = False) -> bool:
    """
    Validates the integrity of an Antigravity project.

    Checks for required directories and files.
    If `fix` is True, attempts to repair missing structure and regenerate files.
    """
    base_dir = Path(project_path).resolve()
    print(f"\n🩺 Running Doctor on: {project_path}")
    print(AntigravityResources.SEPARATOR)

    if not base_dir.exists():
        print(f"❌ Project directory not found: {project_path}")
        return False

    # Initialize result lists
    passed: list[str] = []
    issues: list[str] = []
    warnings: list[str] = []
    fixed: list[str] = []

    # 1. Check Directories & Files (Required)
    req_dirs, req_files = _get_doctor_requirements()

    d_passed, d_issues, d_fixed = _validate_doctor_dirs(base_dir, req_dirs, fix)
    passed.extend(d_passed)
    issues.extend(d_issues)
    fixed.extend(d_fixed)

    f_passed, f_warnings, f_issues, f_fixed = _validate_doctor_files(base_dir, req_files, fix)
    passed.extend(f_passed)
    warnings.extend(f_warnings)
    issues.extend(f_issues)
    fixed.extend(f_fixed)

    # 2. Check Optional Files
    opt_files = _get_doctor_optional_files()
    o_passed, o_warnings, o_issues, o_fixed = _validate_doctor_files(base_dir, opt_files, fix)
    passed.extend(o_passed)
    warnings.extend(o_warnings)
    issues.extend(o_issues)
    fixed.extend(o_fixed)

    # 3. Print Results
    _print_doctor_results(passed, warnings, issues, fixed)

    # 4. Final Verdict
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


def list_blueprints() -> None:
    """Display all available built-in blueprints."""
    print("\n💎 Available Blueprints")
    print(AntigravityResources.SEPARATOR)

    for name, data in AntigravityResources.BLUEPRINTS.items():
        desc = f"Stack: {', '.join(data.get('stack', []))}"
        print(f"  - {name:<12} : {desc}")

    print("\n" + AntigravityResources.SEPARATOR)
    print("Usage: --blueprint <name> OR --blueprint https://github.com/user/repo")


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


def _print_dry_run_header(project_name: str, keywords: list[str], args: argparse.Namespace) -> None:
    """Prints the dry run header summary."""
    print("\n🔍 DRY RUN MODE - No files will be created")
    print("=" * 60)
    print(f"📦 Project Name: {project_name}")
    print(f"⚙️  Tech Stack: {', '.join(keywords)}")
    print(f"🧠 Brain Dump: {args.brain_dump or 'None'}")
    print(f"🛡️  Safe Mode: {args.safe}")
    print(f"📁 Templates: {args.templates or 'Default (Built-in)'}")
    print(f"📜 License: {args.license}")
    print("=" * 60)


def _print_dry_run_directories(project_name: str) -> None:
    """Prints directories to be created."""
    print("\n📁 Directories that would be created:")
    dirs = [
        "src",
        "tests",
        "docs/imported",
        "context/raw",
        ".idx",
        ".devcontainer",
        AntigravityResources.VSCODE_DIR,
        ".github/ISSUE_TEMPLATE",
        ".agent/rules",
        ".agent/workflows",
        ".agent/skills/git_automation",
        ".agent/skills/secrets_manager",
        ".agent/memory",
    ]
    for d in dirs:
        print(f"    📂 {project_name}/{d}/")


def _print_dry_run_files(project_name: str, keywords: list[str]) -> None:
    """Prints core files to be created."""
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
        AntigravityResources.BOOTSTRAP_FILE,
        ".env.example",
    ]
    for f in core_files:
        print(f"    📄 {project_name}/{f}")

    print("\n🤖 AI IDE Configuration Files:")
    ide_files = [
        (".github/copilot-instructions.md", f"Tech Stack: {', '.join(keywords)}"),
    ]
    for f, desc in ide_files:
        print(f"    🤖 {project_name}/{f} ({desc})")


def _print_dry_run_agent(keywords: list[str]) -> None:
    """Prints agent-specific files."""
    print("\n📜 Agent Rules & Workflows:")
    for rule_file in AntigravityResources.AGENT_RULES:
        print(f"    📜 .agent/rules/{rule_file}")
    print(f"    📜 .agent/rules/01_tech_stack.md (Dynamic: {', '.join(keywords)})")
    for workflow_file in AntigravityResources.AGENT_WORKFLOWS:
        print(f"    ⚡ .agent/workflows/{workflow_file}")

    print("\n📋 Project Standards & CI/CD:")
    print("    📋 .github/workflows/ci.yml")
    if "gitea" in keywords:
        print(f"    📋 {AntigravityResources.GITEA_DIR}/workflows/ci.yml")

    print("\n🛠️  Agent Skills (.agent/skills/):")
    for skill_file in AntigravityResources.AGENT_SKILLS:
        print(f"    🛠️  {skill_file}")

    print("\n🧠 Agent Memory (.agent/memory/):")
    print("    🧠 scratchpad.md")


def _print_dry_run_templates(keywords: list[str]) -> None:
    """Prints template files."""
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

    if "gitea" in keywords:
        print(f"\n📋 Gitea Templates ({AntigravityResources.GITEA_DIR}/):")
        gitea_files = [
            "issue_template/bug_report.md",
            "issue_template/feature_request.md",
        ]
        for f in gitea_files:
            print(f"    📋 {f}")


def _print_dry_run_report(project_name: str, keywords: list[str], args: argparse.Namespace) -> None:
    """Helper to print dry run details."""
    _print_dry_run_header(project_name, keywords, args)
    _print_dry_run_directories(project_name)
    _print_dry_run_files(project_name, keywords)
    _print_dry_run_agent(keywords)
    _print_dry_run_templates(keywords)

    print("\n" + "=" * 60)
    print("✅ Dry run complete. No changes made.")
    print("   Run without --dry-run to create the project.")


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
        _print_dry_run_report(project_name, keywords, args)
        return

    generate_project(
        project_name,
        keywords,
        args.brain_dump,
        safe_mode=args.safe,
        custom_templates=custom_templates,
        license_type=args.license,
        blueprint=args.blueprint,
    )


def main(argv: list[str] | None = None) -> None:
    """Main entry point for the Antigravity Architect."""
    # 1. First pass: Check for immediate actions or preset loading
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument("--preset", type=str)
    pre_parser.add_argument("--list-presets", action="store_true")
    pre_args, _ = pre_parser.parse_known_args(argv)

    if pre_args.list_presets:
        print("💾 Saved Presets:")
        for p in list_presets():
            print(f"  - {p}")
        return

    # 2. Load preset defaults if requested
    defaults = {}
    if pre_args.preset:
        loaded = load_preset(pre_args.preset)
        if loaded:
            defaults = loaded
            print(f"💎 Loaded preset: {pre_args.preset}")

    # 3. Build full parser with defaults
    parser = build_cli_parser()
    if defaults:
        parser.set_defaults(**defaults)

    args = parser.parse_args(argv)

    if args.list_keywords:
        list_keywords()
        return

    if args.list_blueprints:
        list_blueprints()
        return

    if args.doctor:
        doctor_project(args.doctor, fix=args.fix)
        return

    # 4. Handle Save Preset
    if args.save_preset:
        # Filter out operational flags
        preset_data = {
            k: v
            for k, v in vars(args).items()
            if v is not None
            and k not in ("save_preset", "preset", "dry_run", "list_keywords", "list_presets", "doctor", "fix")
        }
        save_preset(args.save_preset, preset_data)
        # Continue execution? Yes, commonly users might want to run AND save.

    if args.name:
        run_cli_mode(args)
    else:
        run_interactive_mode()


if __name__ == "__main__":
    main()
