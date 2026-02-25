# 🏗️ Antigravity Architect (v3.0.1)

> [!CAUTION]
> **DISCLAIMER**
>
> This project and its code were created using artificial intelligence (AI) tools. The development was audited using a hybrid Gemini/Claude workflow to ensure maximum security and quality.
>
> For future development and major releases, we repeat this rigorous process to ensure continued architectural integrity.

<!-- Project & Build Status -->
[![Version](https://img.shields.io/badge/version-3.0.1-brightgreen.svg)](https://github.com/pkeffect/antigravity-architect/releases)
[![Python](https://img.shields.io/badge/python-3.10--3.14-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![CI Status](https://github.com/pkeffect/antigravity-architect/actions/workflows/ci.yml/badge.svg)](https://github.com/pkeffect/antigravity-architect/actions)
[![Test Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](AUDIT.md)
[![Audit Score](https://img.shields.io/badge/audit%20score-100%2F100-brightgreen.svg)](AUDIT.md)

<!-- Code Quality -->
[![Linting: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Type Checking: MyPy](https://img.shields.io/badge/type%20checking-mypy-blue.svg)](http://mypy-lang.org/)
[![Formatting: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests: Pytest](https://img.shields.io/badge/tests-111%20passed-success.svg)](https://docs.pytest.org/)

---

## What Is Antigravity Architect?

**[Antigravity Architect](https://github.com/pkeffect/antigravity-architect)** is the definitive **Agent-First** project engine. It is a modular, zero-dependency Python package that generates **Living Repositories**—complete development environments designed from the ground up to be self-describing, self-protecting, and self-evolving for AI coding agents like Gemini, Claude, and GPT-4.

Traditional scaffolding tools generate files and walk away. Antigravity generates an entire **Intelligence Layer**: a declarative governance system, a semantic repository map, autonomic memory management, background security sentinels, cross-repository context bridges, and a full suite of agent rules, workflows, and executable skills. The result is a repository that doesn't just contain code—it *teaches the AI how to work on itself*.

### Key Design Principles

- **Zero Runtime Dependencies**: Built entirely on the Python standard library. No `pip install` surprises.
- **Agent-First Architecture**: Every generated file is designed to be consumed by an AI agent, not just a human developer.
- **Modular Plugin System**: Extend generation capabilities without touching the core engine.
- **Cross-Platform Intelligence**: Automatically adapts to Windows, macOS, and Linux environments.
- **Protocol-Driven**: All agent behavior is governed by a versioned manifest (`protocol: 3.0.0`) ensuring reproducibility and auditability.

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/pkeffect/antigravity-architect.git
cd antigravity-architect
pip install -e .
```

### Generate a Project

```bash
# Interactive mode - guided step-by-step
antigravity-architect

# CLI one-liner
antigravity-architect --name my-project --stack python,react,docker

# With a brain dump specification file
antigravity-architect --name my-project --brain-dump ./specs.md --safe

# Apply a specialized blueprint
antigravity-architect --name my-api --stack python --blueprint fastapi

# Preview what would be generated without writing files
antigravity-architect --name my-project --stack python --dry-run
```

### Start the Agent

Open the generated folder in any AI-ready IDE (VS Code with Gemini Code Assist, Cursor, Windsurf, or Google Project IDX) and type:

> "Read BOOTSTRAP_INSTRUCTIONS.md and start."

---

## ✨ Complete Feature Reference

### 🧠 Protocol v3.0 — The Intelligence Layer

The v3.0 release transforms every generated repository into a self-describing, declarative intelligence layer for AI agents.

#### Declarative Governance (`.agent/tools.json`)

Every generated project includes a tool permission matrix that explicitly restricts what an AI agent can and cannot do. Tools are classified into three tiers:

- **Safe**: Read-only operations (e.g., `list_dir`, `view_file`, `grep_search`)
- **Sensitive**: Write operations requiring caution (e.g., `write_to_file`, `run_command`)
- **Restricted**: Destructive operations with hard limits (e.g., `delete_file` with a configurable max deletion count)

Built-in guardrails prevent agents from modifying protected paths (`.git/`, `.venv/`, `private/`).

#### Semantic Repository Mapping (`AGENT_MAP.yaml`)

A pre-computed, human-readable YAML digest of the entire repository's structure and intent. Instead of burning tokens on recursive directory listing (`ls -R`), agents read a single file to understand what every directory and key file does. Generated automatically during project creation.

#### Autonomic Memory Compaction (Rule 11)

AI agents accumulate task history in `.agent/memory/scratchpad.md`. Rule 11 enforces an automated compaction protocol:

- **Trigger**: When `scratchpad.md` exceeds 100 lines or 10 completed tasks.
- **Action**: Summarize completed tasks into a high-level history block, consolidate sub-tasks, and purge stale notes.
- **Goal**: Maintain a high signal-to-noise ratio in the agent's context window.

#### Neural Bridge (`context/links.md`)

Automatically discovers sibling projects in the parent directory and scans for global knowledge lakes at `~/.antigravity/knowledge_lake/`. The generated `context/links.md` file provides cross-repository architectural syncing, enabling agents to understand the broader ecosystem a project lives in.

#### Lifecycle State Machine

The `.agent/manifest.json` tracks repository maturity through explicit lifecycle states:

- **INIT**: Freshly generated; agent operates with maximum caution.
- **STABLE**: Production-ready; agent can operate with full autonomy.
- **ARCHIVED**: Read-only; agent should not make modifications.

#### Atomic Documentation

All generated Markdown templates include machine-readable `<!-- ID: [name] -->` HTML comment tags in their headers. This enables LLMs to surgically extract or modify specific documentation sections without parsing entire files.

---

### 🔌 Plugin Ecosystem

Antigravity operates on a dynamic sidecar plugin architecture managed by the `PluginManager` class.

#### How It Works

1. **Auto-Discovery**: On startup, the `PluginManager` scans for any Python file matching the `ag_plugin_*.py` naming convention.
2. **Lifecycle Hooks**: Plugins register hooks (e.g., `post_generation`) that execute at specific points in the generation pipeline.
3. **Graceful Degradation**: If a plugin's dependencies are missing, it logs a warning and skips execution—never crashing the engine.
4. **User-Extensible**: Drop a new `ag_plugin_*.py` into your project's `ag_plugins/` directory and it will be loaded automatically.

#### Built-In Plugins

| Plugin | Description |
| :--- | :--- |
| `ag_plugin_vscode` | Generates hardened `.vscode/settings.json`, recommended extensions, and custom code snippets for the detected tech stack. |
| `ag_plugin_github` | Scaffolds complete `.github/` directory: CI/CD Actions workflows, bug report and feature request issue templates, PR templates, and Dependabot configuration. |
| `ag_plugin_gitea` | Generates Gitea-native CI pipeline configurations and workflow files for self-hosted enterprise Git. |
| `ag_plugin_idx` | Creates `.idx/dev.nix` environment configurations for Google Project IDX cloud workspaces. |

---

### 🗺️ Blueprint Marketplace

Blueprints are pre-configured project templates that override default directory structures, inject extra dependencies, and apply domain-specific rules.

#### 14 Built-In Blueprints

| Blueprint | Stack | Description |
| :--- | :--- | :--- |
| `fastapi` | Python | FastAPI project with `src/` layout, routers, and models |
| `nextjs` | Node | Next.js 15 app with TypeScript and App Router |
| `go-fiber` | Go | Go Fiber web server with modular handlers |
| `rust-axum` | Rust | Axum web framework with Tokio async runtime |
| `rust-complex` | Rust | Multi-crate Rust workspace with shared libraries |
| `java-spring` | Java | Spring Boot application with Gradle build system |
| `csharp-dotnet` | C# | .NET 8 Web API with Entity Framework Core |
| `elixir-phoenix` | Elixir | Phoenix LiveView application with Ecto |
| `flutter` | Dart | Flutter cross-platform app with Material Design |
| `c-minimal` | C | Minimal C project with CMake build system |
| `zig` | Zig | Zig project with `build.zig` configuration |
| `audio` | Multi | Audio/DSP project scaffold with JUCE or FAUST |
| `medical` | Multi | HIPAA-aware medical software scaffold |
| `performance` | Multi | Performance-critical project with benchmarking |

#### Remote Blueprints

Fetch any community blueprint directly from a Git URL:

```bash
antigravity-architect --name my-app --blueprint https://github.com/user/my-custom-blueprint
```

The engine clones the repository, reads the `antigravity_blueprint.json` manifest, and merges the blueprint's directories, files, and rules with the standard Antigravity output.

---

### 🤖 Agent Rules System (14 Templates)

Every generated project includes a layered, priority-ordered rule system in `.agent/rules/`. Rules are conditionally loaded based on the detected tech stack—a Python project won't receive Node.js linting rules.

| Rule | Layer | Purpose |
| :--- | :--- | :--- |
| `00_identity.md` | 0 (Mandatory) | Agent persona, primary directives, and safety constraints |
| `01_tech_stack.md` | 1 (High) | Dynamically generated conventions for the detected stack |
| `02_security.md` | 1 (High) | OWASP foundations, secret protection, and input validation |
| `03_git.md` | 2 (Standard) | Conventional commits, branch strategies, and PR etiquette |
| `04_reasoning.md` | 2 (Standard) | Step-by-step logic and chain-of-thought requirements |
| `05_architecture.md` | 2 (Standard) | Modular design constraints and separation of concerns |
| `05_environment.md` | 1 (High) | OS-specific behaviors and cross-platform adaptations |
| `06_ux.md` | 2 (Standard) | User experience and interface design guidelines |
| `07_security_expert.md` | 2 (Standard) | Advanced security persona for threat modeling |
| `08_boundaries.md` | 1 (High) | Hard limits on agent autonomy and destructive actions |
| `09_cross_repo.md` | 2 (Standard) | Multi-repository context sharing protocols |
| `10_evolution.md` | 2 (Standard) | Self-improvement and technical debt tracking |
| `11_self_learning.md` | 1 (High) | Autonomic compaction and knowledge internalization |
| `99_model_dispatch.md` | 3 (Low) | Model-specific optimizations (Gemini, Claude, GPT-4) |

#### Adaptive Rule Weighting

The `_generate_priority_list()` function dynamically reorders and filters rules based on the project's tech stack. Security-heavy stacks (e.g., `docker`, `cloud`) automatically promote security rules to higher priority. Minimal stacks suppress verbose rules to reduce token overhead.

#### Personality Packs

The `--personality` flag adjusts the agent's behavioral tone:

- **`startup`**: Favors speed and iteration over perfection.
- **`enterprise`**: Enforces strict compliance, extensive documentation, and change management.
- **`minimal`**: Strips non-essential rules for lightweight projects.

---

### ⚡ Agent Workflows (10 Templates)

Pre-built, actionable routines that agents can invoke by command:

| Workflow | Trigger | Description |
| :--- | :--- | :--- |
| `plan.md` | `/plan` | Read context, break request into atomic tasks, check rules |
| `bootstrap.md` | `/bootstrap` | Full project initialization sequence |
| `commit.md` | `/commit` | Stage, validate, and commit with conventional messages |
| `review.md` | `/review` | Code review checklist with security and quality gates |
| `save.md` | `/save` | Checkpoint project state to memory files |
| `sync.md` | `/sync` | Synchronize context across sibling repositories |
| `evolve.md` | `/evolve` | Identify and execute background refactoring tasks |
| `doctor.md` | `/doctor` | Run structural health checks on the `.agent/` directory |
| `compress.md` | `/compress` | Trigger autonomic memory compaction |
| `help.md` | `/help` | Display all available commands and their descriptions |

---

### 🛠️ Agent Skills (4 Executable Modules)

Skills are executable Python scripts that agents can run directly for automation tasks:

| Skill | Description |
| :--- | :--- |
| `bridge/` | Core inter-agent communication handler for cross-repository context sharing |
| `secrets_manager/` | Entropy-based secret detector that scans for exposed API keys, passwords, and tokens |
| `env_context/` | Dynamic OS and environment detection (Windows/macOS/Linux, shell type, Python version) |
| `git_automation/` | Automated Git operations: staging, diffing, and conventional commit message generation |

---

### 🛡️ Security & Governance

#### Sentinel Monitoring (`scripts/sentinel.py`)

A daemon script that watches critical repository files (`.env`, security rules, `cli.py`, `sentinel.py` itself). If unauthorized modifications are detected, it triggers an immediate `--doctor` audit with auto-fix.

#### CycloneDX SBOM Generation

Generate a Software Bill of Materials in CycloneDX 1.4 format:

```bash
antigravity-architect --sbom ./my-project
```

The `AntigravityGovernance.generate_sbom()` method scans `requirements.txt` for pinned dependencies and produces a machine-readable JSON SBOM.

#### License Conflict Scanning

`AntigravityGovernance.scan_licenses()` scans dependency files for known GPL-incompatible licenses and flags potential conflicts before they become legal issues.

#### Environment Schema Validation

`AntigravityGovernance.validate_env_schema()` enforces `.env.schema` compliance: if a project defines required environment variables in `.env.schema`, the governance module verifies they exist in the actual `.env` file.

---

### 🧪 Brain Dump Assimilator

The **Assimilator** transforms unstructured specification documents into structured, categorized agent knowledge.

```bash
antigravity-architect --name my-project --brain-dump ./specs.md
```

#### How It Works

1. **Archive**: The raw brain dump is saved to `context/raw/master_brain_dump.md` for reference.
2. **Tech Detection**: `detect_tech_stack()` scans the text using primary keywords and 50+ aliases (e.g., "Django" → `python`, "Kubernetes" → `docker`) to identify the project's technology stack.
3. **Deep-Dive Generation**: `build_tech_deep_dive()` produces a `docs/TECH_STACK.md` with primary technologies, contextual observations (API surfaces, security requirements, database layers), and technical debt tracking.
4. **Heuristic Classification**: Each section is scored against keyword rules for `rules`, `workflows`, `skills`, and `docs` to determine the correct `.agent/` subdirectory.
5. **Distribution**: Classified sections are written to their appropriate locations with `<!-- Auto-Assimilated Source -->` provenance tags.

---

### 🏥 Doctor Mode

Validate and repair any Antigravity-generated project's structural health:

```bash
# Diagnose issues
antigravity-architect --doctor ./my-project

# Diagnose and auto-fix
antigravity-architect --doctor ./my-project --fix
```

Doctor mode checks for:

- Missing `.agent/` directories (rules, workflows, skills, memory)
- Missing or corrupted critical files (manifest, identity rule, security rule)
- Structural drift from the expected Antigravity protocol
- Auto-generates missing files from templates when `--fix` is applied

---

### 💾 Preset System

Save and reuse complex CLI configurations:

```bash
# Save current arguments as a preset
antigravity-architect --name api --stack python,docker --blueprint fastapi --save-preset my-api

# Load and run a saved preset
antigravity-architect --preset my-api

# List all saved presets
antigravity-architect --list-presets
```

Presets are stored in `~/.antigravity/presets/` as JSON files, enabling team-wide standardization of project generation.

---

### 📦 Smart File Operations

The `AntigravityEngine` provides hardened, cross-platform file I/O:

- **Path Traversal Protection**: `sanitize_name()` strips `../`, `./`, null bytes, and special characters from all project names.
- **SHA-256 Smart Overwrite**: `write_file()` computes content hashes before writing. If the file hasn't changed, the write is skipped entirely—preventing unnecessary Git diffs.
- **Unified Diff Analysis**: `get_diff()` produces unified diffs for drift detection in Doctor mode.
- **Lazy Template Loading**: The `LazyTemplateDict` class defers template file I/O until first access, reducing startup time for large template directories.

---

## 📋 Full CLI Reference

```text
usage: antigravity-architect [-h] [--version] [--name NAME] [--stack STACK]
                             [--brain-dump BRAIN_DUMP] [--safe] [--dry-run]
                             [--templates TEMPLATES] [--doctor PATH] [--fix]
                             [--list-keywords] [--license {mit,apache,gpl}]
                             [--blueprint BLUEPRINT] [--save-preset NAME]
                             [--preset NAME] [--list-presets]
                             [--list-blueprints]
                             [--ide {jetbrains,neovim,zed,fleet}]
                             [--ci {gitlab,azure}] [--docker]
                             [--personality {startup,enterprise,minimal}]
                             [--sbom PATH]
```

| Flag | Description |
| :--- | :--- |
| `--name`, `-n` | Project name (required for CLI mode) |
| `--stack`, `-s` | Comma-separated tech stack keywords (e.g., `python,react,docker`) |
| `--brain-dump`, `-b` | Path to a specification file for Knowledge Assimilation |
| `--safe` | Enable Safe Update Mode (non-destructive, never overwrites) |
| `--dry-run` | Preview all actions without writing any files |
| `--templates`, `-t` | Path to a custom templates directory for rule/workflow overrides |
| `--doctor PATH` | Validate an existing project's `.agent/` structural integrity |
| `--fix` | Auto-repair issues found by `--doctor` |
| `--list-keywords` | Display all supported tech stack keywords and aliases |
| `--list-blueprints` | Display all built-in and marketplace blueprints |
| `--license`, `-l` | Project license: `mit`, `apache`, or `gpl` (default: `mit`) |
| `--blueprint` | Apply a built-in blueprint name or remote Git URL |
| `--save-preset` | Save the current CLI arguments as a named preset |
| `--preset` | Load and execute a saved preset by name |
| `--list-presets` | List all saved presets in `~/.antigravity/presets/` |
| `--ide` | Generate IDE configs: `jetbrains`, `neovim`, `zed`, or `fleet` |
| `--ci` | Generate CI pipeline: `gitlab` or `azure` |
| `--docker` | Generate `docker-compose.yml` configuration |
| `--personality` | Agent behavior pack: `startup`, `enterprise`, or `minimal` |
| `--sbom PATH` | Generate a CycloneDX SBOM for an existing project |
| `--version` | Display the current version |

---

## 📂 Complete Project Structure

### Generated Output (What Your Project Gets)

```text
my-project/
├── .agent/                             # 🤖 THE AGENT BRAIN
│   ├── manifest.json                   #   Protocol version, capabilities, lifecycle state
│   ├── tools.json                      #   Declarative tool permissions (safe/sensitive/restricted)
│   ├── rules/                          #   Behavioral constraints and coding standards
│   │   ├── 00_identity.md              #     Agent persona and primary safety directives
│   │   ├── 01_tech_stack.md            #     Dynamically generated stack-specific conventions
│   │   ├── 02_security.md              #     OWASP foundations and secret protection
│   │   ├── 03_git.md                   #     Conventional commits and branch strategies
│   │   ├── 04_reasoning.md             #     Chain-of-thought and step-by-step logic
│   │   ├── 05_architecture.md          #     Modular design and separation of concerns
│   │   ├── 05_environment.md           #     OS-specific behaviors and adaptations
│   │   ├── 06_ux.md                    #     User experience guidelines
│   │   ├── 07_security_expert.md       #     Advanced threat modeling persona
│   │   ├── 08_boundaries.md            #     Agent autonomy limits and safeguards
│   │   ├── 09_cross_repo.md            #     Multi-repository context sharing
│   │   ├── 10_evolution.md             #     Self-improvement and tech debt tracking
│   │   ├── 11_self_learning.md         #     Autonomic compaction protocol
│   │   └── 99_model_dispatch.md        #     Model-specific optimizations
│   ├── workflows/                      #   Actionable agent routines
│   │   ├── plan.md                     #     Task breakdown and context gathering
│   │   ├── bootstrap.md                #     Full project initialization
│   │   ├── commit.md                   #     Conventional commit workflow
│   │   ├── review.md                   #     Code review with quality gates
│   │   ├── save.md                     #     Checkpoint state to memory
│   │   ├── sync.md                     #     Cross-repo context synchronization
│   │   ├── evolve.md                   #     Background refactoring identification
│   │   ├── doctor.md                   #     Structural health validation
│   │   ├── compress.md                 #     Memory compaction trigger
│   │   └── help.md                     #     Command reference
│   ├── skills/                         #   Executable automation scripts
│   │   ├── bridge/SKILL.md             #     Inter-agent communication handler
│   │   ├── secrets_manager/SKILL.md    #     Entropy-based secret scanner
│   │   ├── env_context/SKILL.md        #     Dynamic OS and environment detection
│   │   └── git_automation/SKILL.md     #     Automated Git operations
│   └── memory/                         #   Agent state tracking
│       ├── scratchpad.md               #     Short-term focus, active tasks, immediate roadmap
│       └── evolution.md                #     Long-term tech debt and refactoring goals
├── AGENT_MAP.yaml                      # 🗺️ Semantic repository digest for zero-cost discovery
├── BOOTSTRAP_INSTRUCTIONS.md           # 📖 The first file the AI reads to initialize
├── context/                            # 🌉 Neural Bridge
│   ├── raw/                            #     Archived brain dump source material
│   └── links.md                        #     Sibling project and knowledge lake references
├── docs/                               # 📚 Architectural documentation
│   ├── imported/                       #     Assimilated external specifications
│   ├── TECH_STACK.md                   #     Auto-generated technology deep-dive
│   └── SBOM.json                       #     CycloneDX software bill of materials
├── scripts/                            # 🛡️ DevOps utilities
│   └── sentinel.py                     #     Background file modification watchdog
├── .github/                            # 🐙 GitHub Actions and templates (via plugin)
│   ├── workflows/ci.yml                #     Automated CI/CD pipeline
│   ├── ISSUE_TEMPLATE/                 #     Bug report and feature request templates
│   └── dependabot.yml                  #     Automated dependency updates
├── .vscode/                            # 🛠️ VS Code workspace (via plugin)
│   ├── settings.json                   #     Hardened editor settings
│   └── extensions.json                 #     Recommended extensions for the stack
├── .devcontainer/                      # 📦 Dev Containers configuration
├── src/                                # 💻 Primary source code
├── tests/                              # 🧪 Test suite scaffolding
├── .gitignore                          #     Stack-aware exclusion patterns
├── .env.example                        #     Environment variable template
├── .pre-commit-config.yaml             #     Pre-commit hook configuration
├── pyproject.toml                      #     Python package metadata (or equivalent)
├── docker-compose.yml                  #     Container orchestration (if --docker)
├── README.md                           #     Professional README with badges
├── CHANGELOG.md                        #     Versioned change log
├── CONTRIBUTING.md                     #     Contributor guidelines
├── CODE_OF_CONDUCT.md                  #     Community standards
├── SECURITY.md                         #     Vulnerability reporting policy
├── AUDIT.md                            #     Security and quality audit report
└── LICENSE                             #     MIT, Apache, or GPL license
```

### Antigravity Package Source (For Contributors)

```text
src/antigravity_architect/
├── __init__.py                         # Package version exposure
├── cli.py                              # CLI entrypoint, argument parsing, interactive/doctor modes
├── core/
│   ├── __init__.py                     # Core module exports
│   ├── assimilator.py                  # Brain dump parsing, tech detection, heuristic classification
│   ├── builder.py                      # Dynamic config generators and project orchestration
│   ├── engine.py                       # Sanitized file I/O, presets, blueprints, diffing
│   └── governance.py                   # SBOM generation, license scanning, env schema validation
├── plugins/
│   ├── __init__.py                     # Plugin module exports
│   ├── manager.py                      # Dynamic plugin discovery, lifecycle hooks, error isolation
│   ├── ag_plugin_vscode.py             # VS Code / Cursor workspace generator
│   ├── ag_plugin_github.py             # GitHub Actions, templates, and Dependabot
│   ├── ag_plugin_gitea.py              # Gitea CI pipeline generator
│   └── ag_plugin_idx.py                # Google Project IDX environment generator
└── resources/
    ├── __init__.py                     # Resource module exports
    ├── constants.py                    # VERSION, directory names, tech aliases, classification rules
    ├── templates.py                    # Lazy template loader and common template accessors
    └── templates/                      # Raw template files
        ├── rules/          (14 files)  #   Agent behavioral rule templates
        ├── workflows/      (10 files)  #   Agent workflow templates
        ├── skills/         (4 dirs)    #   Agent skill SKILL.md templates
        ├── blueprints/     (14 files)  #   Project blueprint JSON definitions
        ├── memory/                     #   Agent memory file templates
        ├── agent/                      #   Manifest and tools.json templates
        ├── common/         (13 files)  #   Shared templates (gitignore, licenses, sentinel, etc.)
        ├── docs/                       #   Documentation templates
        ├── ide/                        #   IDE configuration templates
        └── pipelines/                  #   CI/CD pipeline templates
```

---

## 🧪 Comprehensive Test Suite

The package is backed by **111 passing tests** across 8 test modules with **100% code coverage**.

```bash
# Install development dependencies
pip install -e .[dev]

# Run the full suite
pytest tests/ -v

# Run with coverage reporting
pytest tests/ --cov=antigravity_architect --cov-report=term-missing
```

### Test Modules

| Module | Tests | What It Covers |
| :--- | :--- | :--- |
| `test_antigravity.py` | Core | Full generation flow integration tests: directory creation, file content, template injection, brain dump assimilation |
| `test_cli_core.py` | CLI | Argument parsing, interactive mode, version display, keyword listing, preset save/load |
| `test_cli_doctor.py` | Doctor | Health checks, missing file detection, auto-fix verification, drift analysis |
| `test_cli_presets.py` | Presets | Preset creation, loading, listing, and JSON persistence |
| `test_blueprints.py` | Blueprints | Built-in blueprint application, remote blueprint fetching, blueprint inheritance |
| `test_features.py` | Intelligence | Autonomic compaction, sentinel installation, neural bridge links, governance hooks |
| `test_extended.py` | Extended | Edge cases: empty stacks, special characters, path traversal prevention, large inputs |
| `test_plugins.py` | Plugins | Plugin discovery, lifecycle hook execution, graceful missing dependency handling |

### Static Analysis (100% Compliance)

```bash
# Linting
ruff check src/antigravity_architect/

# Type checking
mypy src/antigravity_architect/

# Formatting
black --check src/antigravity_architect/
```

---

## 🆚 Why Antigravity Architect?

### vs. Traditional Scaffolding (Cookiecutter, Yeoman, Create React App)

| Dimension | Traditional | Antigravity |
| :--- | :--- | :--- |
| Output | Static files | Living Repository with embedded AI governance |
| Post-Generation | Tool disappears | Sentinel monitors, Doctor heals, Agent evolves |
| AI Awareness | None | Full agent rule system, semantic maps, memory |
| Customization | Template variables | Brain dump assimilation + blueprint marketplace |
| Cross-Project | Isolated | Neural Bridge links sibling repos automatically |

Traditional scaffolding generates **dead code**. Once the tool runs, you're on your own. There's no ongoing governance, no health checks, no way for an AI to understand *how* to work on the project. Antigravity generates the code *and* the instruction manual for the AI that will maintain it.

### vs. AI IDE Assistants (Cursor, Windsurf, GitHub Copilot)

| Dimension | AI IDE | Antigravity |
| :--- | :--- | :--- |
| Governance | Global UI settings | Repository-level declarative rules |
| Safety | User-configured | Tiered tool permissions with hard limits |
| Context | Whole-file scanning | Pre-computed semantic map + agent memory |
| Consistency | Varies by session | Protocol-versioned, reproducible, auditable |
| Portability | Locked to one IDE | Works in any AI-capable environment |

IDE-level AI assistants are powerful but operate on generic, global settings. They don't understand *your project's* specific security posture, architectural boundaries, or quality requirements. Antigravity embeds those constraints *inside the repository itself*, so any agent—regardless of IDE—must conform to the project's rules.

### vs. Agent Frameworks (LangChain, CrewAI, AutoGen)

| Dimension | Frameworks | Antigravity |
| :--- | :--- | :--- |
| Focus | Runtime orchestration | Repository-level architecture |
| Dependencies | Heavy (dozens of packages) | Zero (Python stdlib only) |
| Scope | Agent execution logic | Agent *environment* and governance |
| Complement | Runs agents | Prepares the workspace agents run in |

Agent frameworks orchestrate *what agents do at runtime*. Antigravity Architect prepares *where agents work*. They are complementary: use Antigravity to generate the governed, self-describing repository, then use any framework to run agents within it.

---

## 🤖 AI Contributors

This project was built using a hybrid AI development workflow. The following AI systems contributed significantly to the architecture, code, testing, and documentation:

| Contributor | Role | Attribution |
| :--- | :--- | :--- |
| **Claude** (Anthropic) | Architecture, code generation, testing, documentation, and code review | `Co-authored-by: Claude <noreply@anthropic.com>` |
| **Gemini** (Google DeepMind) | Architecture, code generation, refactoring, linting, and release engineering | `Co-authored-by: Gemini <noreply@google.com>` |

> [!NOTE]
> All AI-generated code was audited for security, correctness, and adherence to best practices. See [`AUDIT.md`](AUDIT.md) for the full audit report.

---

## 🤝 Contributing

We welcome community blueprints and core engine improvements! Please review our [Contribution Guide](CONTRIBUTING.md) to understand our "Agent-First" development workflow and branch strategies.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
