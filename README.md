# 🏗️ Antigravity Architect (Master Edition)

<!-- Project & Build Status -->
[![Version](https://img.shields.io/badge/version-1.4.2-brightgreen.svg)](https://github.com/pkeffect/antigravity-architect/releases)
[![Python](https://img.shields.io/badge/python-3.10--3.14-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![CI Status](https://github.com/pkeffect/antigravity-architect/actions/workflows/ci.yml/badge.svg)](https://github.com/pkeffect/antigravity-architect/actions)

<!-- Code Quality -->
[![Linting: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Type Checking: MyPy](https://img.shields.io/badge/type%20checking-mypy-blue.svg)](http://mypy-lang.org/)
[![Formatting: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests: Pytest](https://img.shields.io/badge/tests-pytest%20%7C%2062%20passed-green.svg)](https://docs.pytest.org/)
[![Code Quality](https://img.shields.io/badge/audit%20score-99%2F100-brightgreen.svg)](AUDIT.md)

<!-- Platform Support -->
[![Windows Tests](https://img.shields.io/badge/Windows-passing-success.svg?logo=windows)](https://github.com/pkeffect/antigravity-architect/actions)
[![macOS Tests](https://img.shields.io/badge/macOS-passing-success.svg?logo=apple)](https://github.com/pkeffect/antigravity-architect/actions)
[![Ubuntu Tests](https://img.shields.io/badge/Ubuntu-passing-success.svg?logo=ubuntu)](https://github.com/pkeffect/antigravity-architect/actions)

<!-- AI IDE Compatibility -->
[![GitHub Copilot](https://img.shields.io/badge/GitHub%20Copilot-compatible-success.svg?logo=github)](https://github.com/features/copilot)
[![Cursor IDE](https://img.shields.io/badge/Cursor%20IDE-compatible-success.svg)](https://cursor.com)
[![Windsurf](https://img.shields.io/badge/Windsurf%20Cascade-compatible-success.svg)](https://windsurf.com)
[![Google IDX](https://img.shields.io/badge/Google%20IDX-compatible-success.svg)](https://idx.dev)

<!-- Architecture & Design -->
[![Architecture](https://img.shields.io/badge/architecture-agent--first-purple.svg)](https://github.com/pkeffect/antigravity-architect)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero%20external-success.svg)](https://github.com/pkeffect/antigravity-architect)

**Antigravity Architect** is the ultimate "Agent-First" bootstrapping tool for modern AI development environments. It generates projects optimized for **GitHub Copilot**, **Cursor IDE**, **Windsurf (Cascade AI)**, **Google IDX**, and any AI coding assistant.

Unlike standard scaffolding tools (like `create-react-app`) that just build code, this script builds a **Brain** for your AI. It constructs a "Self-Describing Repository" that teaches the Agent how to behave, what rules to follow, and automatically assimilates your existing documentation into the Agent's memory.

---

## ✨ Key Features

### 🧠 Knowledge Assimilation (New!)
*   **The Brain Dump:** Drag and drop a massive text file (specs, notes, legacy code snippets). The script parses it, splits it by logical headers, and **automatically classifies** the information into Rules, Workflows, or Documentation.
*   **Raw Context Preservation:** Saves the original dump to `context/raw/` so the Agent can reference the "source of truth."

### 🌐 Universal & Dynamic
*   **Polyglot Support:** Supports Python, Node.js, TypeScript, Rust, Go, Java, PHP, Ruby, Docker, and SQL.
*   **Dynamic Configuration:** Automatically builds `.gitignore`, `.idx/dev.nix`, and `.env` templates based on your input keywords or imported specs.

### 🤖 Full Agent Architecture
*   **Rules:** Generates "Always-On" directives (Persona, Security, Git Conventions, Chain-of-Thought).
*   **Workflows:** Generates callable slash commands (`/plan`, `/bootstrap`, `/commit`, `/review`, `/save`).
*   **Skills:** Generates tool definitions for Git Automation and Secret Management.
*   **Memory:** Initializes a `scratchpad.md` for long-term session memory.
*   **Model Dispatch:** Generates a "Context Handoff" protocol (`99_model_dispatch.md`) that teaches the Agent to request higher-reasoning models (like o1 or Ultra) for complex tasks.

### 🛡️ Production Engineering
*   **The "Git Ghost":** Automatically places `.gitkeep` files in empty directories.
*   **Cloud-Ready:** Generates `.idx/dev.nix` and `.devcontainer/devcontainer.json`.
*   **CI/CD Integrated:** Includes GitHub Actions for linting, type-checking, and automatic testing.
*   **Safety First:** Includes input sanitization, error logging, and non-destructive overwrite protection.
*   **Privacy by Default:** Automatically adds `.agent/` and `context/` to `.gitignore` to prevent leaking your custom agent brain or raw project notes to public repositories.
*   **Safe Update Mode:** Automatically detects existing projects and offers to **Update** (safely inject missing agent files) or **Overwrite** (replace everything).
*   **Community Standards:** Automatically generates `CHANGELOG.md`, `CONTRIBUTING.md`, `AUDIT.md`, `SECURITY.md`, and `CODE_OF_CONDUCT.md` to professionalize your repository from Day 1.
*   **GitHub Templates:** Generates `.github/` with issue templates (bug report, feature request, question), PR template, FUNDING.yml, and **copilot-instructions.md** for AI agent guidance.
*   **License Management:** Select from standard licenses (MIT, Apache, GPL) via CLI flag or interactive prompt.

### 🏗️ Modern Architecture (v1.4.0)
*   **Hybrid Class-Based Design:** Refactored into 5 focused classes while maintaining single-file portability
    - `AntigravityResources` - Centralized templates, constants, and mappings
    - `AntigravityEngine` - File system operations and validation utilities
    - `AntigravityBuilder` - Dynamic configuration generators
    - `AntigravityAssimilator` - Intelligent brain dump parsing
    - `AntigravityGenerator` - High-level project generation orchestration
*   **100% Backward Compatible:** All existing functions preserved via module-level aliases
*   **Improved Maintainability:** 800+ lines reorganized for better code organization and scalability

### 🤖 Universal AI IDE Compatibility (v1.4.1)
*   **GitHub Copilot Support:** Generates `.github/copilot-instructions.md` with project-aware guidance
    - Works in VS Code, Visual Studio, JetBrains IDEs
    - Includes development workflows, security protocols, and commit conventions
    - Dynamically adapts to detected tech stack
*   **Cursor IDE Integration:** Creates `.cursorrules` for AI Composer
    - Optimized for Cursor's inline edits and multi-file Composer mode
    - Includes `@file` reference patterns and keyboard shortcuts
    - Tech stack-specific best practices and conventions
*   **Windsurf (Cascade AI) Support:** Generates `.windsurfrules` for agentic coding
    - Tailored for Cascade's multi-step reasoning and planning
    - Memory persistence and context management guidelines
    - Workflow integration with `.agent/` structure
*   **Google IDX / Gemini CLI:** Native support via `.idx/dev.nix` and `.agent/` architecture
*   **Universal Fallback:** `.agent/` directory structure works with ANY AI coding assistant
    - Rules, workflows, skills, and memory accessible to all AI tools
    - Semantic file organization for optimal RAG (Retrieval Augmented Generation)
    - Human-readable markdown format for maximum compatibility

---

## 🛠️ Development

This project includes a professional development environment with a robust test suite.

### Requirements
*   Python 3.10+
*   `pip install -e .[dev]`

### Running Tests
We use **pytest** for testing (62+ passing tests) across **Windows**, **macOS**, and **Ubuntu**.
We support **Python 3.10** through **3.14-dev**.

```bash
# Run all tests
pytest tests/

# Run with coverage report
pytest tests/ --cov=antigravity_master_setup
```

### Code Quality
We enforce strict quality standards using **Ruff** and **MyPy**.

```bash
# Linting & Formatting
ruff check antigravity_master_setup.py
ruff format antigravity_master_setup.py

# Type Checking
mypy antigravity_master_setup.py --ignore-missing-imports
```

---

## 🚀 Usage

### Interactive Mode (Default)
No external dependencies required. Just run it with Python 3.

```bash
python antigravity_master_setup.py
```

The script will ask for an optional "Brain Dump" file, or you can manually input your stack.

### CLI Mode (v1.3+)
For automation and scripting, use command-line arguments:

```bash
# Basic project creation
python antigravity_master_setup.py --name my-app --stack python,react --license mit

# With brain dump, safe mode, and custom license
python antigravity_master_setup.py --name my-app --brain-dump ./specs.md --safe --license apache

# Preview without creating files
python antigravity_master_setup.py --name my-app --stack python --dry-run

# Use custom templates
python antigravity_master_setup.py --name my-app --templates ~/.antigravity/templates/
```

### Doctor Mode (v1.3+)
Validate an existing project's `.agent/` structure:

```bash
# Check project health
python antigravity_master_setup.py --doctor ./my-project

# Auto-fix missing directories
python antigravity_master_setup.py --doctor ./my-project --fix
```

### Other Commands

```bash
# Show version
python antigravity_master_setup.py --version

# List all supported tech stack keywords
python antigravity_master_setup.py --list-keywords

# Show help
python antigravity_master_setup.py --help
```

### Initialize the Agent
Once the folder is created:
1.  Open the folder in **Google Antigravity** (or Project IDX / VS Code).
2.  Open the **Chat Interface**.
3.  Type the following command to kickstart the AI:

> "Read BOOTSTRAP_INSTRUCTIONS.md and start."

---

## 📂 Generated Architecture

The script creates a specialized folder structure designed for **RAG (Retrieval Augmented Generation)**.

```text
my-project/
├── .agent/                  # 🤖 THE AGENT BRAIN
│   ├── rules/               # Directives injected into System Prompt
│   │   ├── 00_identity.md   # Persona & Goals
│   │   ├── 01_tech_stack.md # Dynamic stack definitions
│   │   ├── 02_security.md   # OWASP & Secret handling
│   │   ├── 03_git.md        # Conventional Commits
│   │   ├── 04_reasoning.md  # Chain-of-Thought enforcer
│   │   ├── 99_model_dispatch.md # Model Handoff Protocol
│   │   └── imported_*.md    # Rules assimilated from your Brain Dump
│   ├── workflows/           # Callable Commands (/slash)
│   │   ├── plan.md          # /plan
│   │   ├── bootstrap.md     # /bootstrap
│   │   ├── commit.md        # /commit
│   │   └── imported_*.md    # Workflows assimilated from your Brain Dump
│   ├── skills/              # Tool definitions
│   │   ├── git_automation/  # Git CLI wrapper
│   │   └── secrets_manager/ # API Key safety tool
│   └── memory/              # Active Session Memory
│       └── scratchpad.md    # The "Save Game" file
├── .idx/                    # ☁️ GOOGLE IDX CONFIG
│   └── dev.nix              # NixOS package definitions
├── .devcontainer/           # 🐳 UNIVERSAL CONTAINER CONFIG
│   └── devcontainer.json    # VS Code / Codespaces config
├── context/
│   └── raw/                 # 📥 DUMP ZONE (Original raw inputs)
├── docs/
│   └── imported/            # 📚 ASSIMILATED KNOWLEDGE
├── src/                     # Source Code
├── CHANGELOG.md             # 📝 History
├── CONTRIBUTING.md          # 🤝 Guidelines
├── AUDIT.md                 # 🛡️ Security Log
├── SECURITY.md              # 🔒 Security Policy
├── CODE_OF_CONDUCT.md       # 🤝 Ethics & Rules
├── LICENSE                  # 📄 Legal
└── BOOTSTRAP_INSTRUCTIONS.md # The "Genie" Prompt
```

---

## 🛠 Supported Keywords

The script parses your input string (or your Brain Dump file) for these keywords to dynamically build `.gitignore` and Cloud Environment packages.

| Category | Keywords (Case Insensitive) |
| :--- | :--- |
| **Languages** | `python`, `node`, `javascript`, `typescript`, `rust`, `go`, `java`, `php`, `ruby` |
| **Frameworks** | `react`, `nextjs`, `vue`, `angular`, `django`, `flask`, `laravel`, `fastapi` |
| **Infrastructure** | `docker`, `sql`, `postgres` |
| **OS / Tools** | `macos`, `windows`, `linux`, `vscode`, `idea` (JetBrains) |

---

## 🤖 Agent Capabilities

Once generated, your AI agent possesses the following capabilities out of the box:

### 🧠 Rules (Always Active)
*   **Security Guard:** Will refuse to print secrets/API keys to chat.
*   **Chain of Thought:** Forced to explain logic *before* writing code.
*   **Git Standards:** Enforces **Conventional Commits** (e.g., `feat: added login`).
*   **Context Awareness:** Automatically checks `docs/imported/` before making decisions.

### ⚡ Workflows (Slash Commands)
Type these in the Antigravity Chat:

| Command | Action |
| :--- | :--- |
| `/plan` | Reads `docs/` and `context/`, then generates a checklist in `scratchpad.md`. |
| `/bootstrap` | Scaffolds "Hello World" code based on the detected Tech Stack. |
| `/review` | Audits the open file for security risks and style violations. |
| `/commit` | Analyzes `git diff` and proposes a formatted commit message. |
| `/save` | Summarizes recent work and updates the `scratchpad.md` memory file. |

---

## ☁️ Environment Details

### For Google Project IDX / Antigravity
The script generates `.idx/dev.nix`.
*   If you selected `python`, the environment boots with Python 3.12, Pip, and Ruff installed.
*   If you selected `node`, it boots with Node 20 and NPM.
*   **Result:** You do not need to manually install system tools; the container builds itself.

### For VS Code / GitHub Codespaces
The script generates `.devcontainer/devcontainer.json`.
*   Uses the standard Microsoft Ubuntu base image.
*   Pre-installs the `google.gemini-code-assist` extension if running in a supported container.

---

## ❓ Troubleshooting

**Q: The script crashes when typing the project name.**
*   **A:** The script sanitizes inputs (removing special characters). Ensure you have write permissions in the folder where you are running the script. Check `antigravity_setup.log` for details.

**Q: The Agent isn't following the rules.**
*   **A:** Ensure you are using a model capable of System Instruction injection (Gemini 1.5 Pro / Ultra recommended). Check that the `.agent` folder is in the root of your workspace.

**Q: Git isn't tracking my `src` folder.**
*   **A:** The script automatically adds `.gitkeep` files to empty folders. If you deleted them manually, Git will ignore the empty folder.

**Q: How does the "Assimilator" work?**
*   **A:** It scans your text file for Markdown headers (e.g., `## Coding Style`). It then scans the content for keywords like "Always", "Workflow", or "CLI". Based on the score, it sorts that section into the `.agent/rules`, `.agent/workflows`, or `.agent/skills` folder automatically.

---

## 🤝 Contributing

We use a **dev branch workflow**:

- **All PRs should target the `dev` branch**
- `main` branch is for stable releases only
- See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines
- See [BRANCH_PROTECTION.md](BRANCH_PROTECTION.md) for branch setup

Quick start:
```bash
git checkout dev
git checkout -b feat/your-feature
# Make changes, commit, push
# Open PR to dev branch (CI will run automatically)
```

---

## 📜 License
This script is open-source. Feel free to modify the `00_identity.md` rule to change your Agent's personality!
