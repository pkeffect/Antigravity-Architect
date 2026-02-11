# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.7.0] - 2026-02-11

### Added (v1.7.0)

- **Community Blueprint Marketplace:** Expanded `--blueprint` support.
  - **New Built-ins:** Added `nextjs`, `fastapi`, `go-fiber`, and `rust-axum` project templates.
  - **Remote Fetching:** Added support for git URLs (e.g., `--blueprint https://github.com/user/repo`).
  - **Discovery:** Added `--list-blueprints` flag to show available templates.
- **CLI Presets:** Added `--save-preset` and `--preset` to save/load project configurations.

### Changed (v1.7.0)

- **Refactoring:** Significantly reduced cognitive complexity in `generate_project` by extracting helper methods (`_resolve_blueprint`, `_generate_vscode_config`, `_apply_blueprint_rules`).
- **Roadmap:** Updated roadmap to reflect completed milestones.

### Deprecated (v1.7.0)

- None

### Removed (v1.7.0)

- None

### Fixed (v1.7.0)

- **Markdown Linting:** Fixed formatting issues in documentation files.
- **Code Duplication:** Resolved repeated string literals in `antigravity_master_setup.py`.

### Security (v1.7.0)

- None

## [1.6.4] - 2026-02-10

### Added (v1.6.4)

- **Dogfooding:** The Antigravity Architect project itself now follows the Standardized Agent Protocol (v2.0.0).
- **Manifest:** Real `.agent/manifest.json` added to the repository.
- **Protocol Headers:** All `.agent/rules/` updated with machine-readable layer/type/priority metadata.
- **Modernized Bootstrap:** `BOOTSTRAP_INSTRUCTIONS.md` updated to reflect the new agent workflows.
- **CLI Presets:** Added `--save-preset` and `--preset` to save/load project configurations.
- **Refactoring:** Significantly reduced cognitive complexity in `generate_project` and `build_tech_deep_dive`.

## [1.6.3] - 2026-02-10

### Added (v1.6.3)

- **Standardized Agent API**: Formalized `.agent/` into a machine-readable protocol (v2.0.0).
- **Protocol Manifest**: Automated generation of `manifest.json` for every new project.
- **Layered Rules**: All agent rules now include YAML frontmatter with priority and layer metadata.
- **Extended Test Suite**: New tests for CLI, Doctor mode, and Interactive mode.

### Fixed (v1.6.3)

- **70% -> 86% Coverage**: Increased test coverage by 16% through exhaustive edge-case testing.
- **Windows File Locking**: Implemented robust logging cleanup in test suites to prevent WinError 32.

## [1.6.2] - 2026-02-10

### Added (v1.6.2)

- **LF Line-Ending Enforcement**: Added `.gitattributes` to guarantee consistent formatting between Windows and Linux CI environments.
- **Local Quality Enforcement (Pre-commit)**: Added `.pre-commit-config.yaml` to automate Ruff formatting, linting, and safety checks locally.
- **AI Development Transparency**: Added prominent `[!CAUTION]` disclaimer to `README.md` detailing the Gemini/Claude hybrid development and audit workflow.
- **Comprehensive Project Maps**: Expanded `README.md` to show the full 45+ item directory tree of the generated Living Repository.
- **Integrated Knowledge Links**: Added direct hyperlinks to [Open WebUI](https://github.com/open-webui/open-webui) and [Antigravity Architect](https://github.com/pkeffect/antigravity-architect) in all core documentation.
- **Hardened Commit Workflow**: Mandated `ruff format .` and `pytest` in the `/commit` workflow to prevent CI drift and regression.
- **Sentinel Mode (Self-Protection)**: Introduced proactive security auditing for critical files via `scripts/sentinel.py`.
- **Autonomous Evolution**: Added background refactoring framework (Rule 10) for systematic tech debt reduction.
- **Documentation Genie**: Automated deep-dive `TECH_STACK.md` generation during project configuration.
- **Multi-Repo Context Bridge**: Automated sibling repository discovery and architectural synchronization.

### Fixed (v1.6.2)

- **CI Formatting Drift**: Resolved recurring `ruff format --check` failures by standardizing on `LF` line endings project-wide.
- **Naming Inconsistency**: Resolved `AttributeError` for `SENTINEL_PY` constant reference mismatch.
- **Generator Integrity**: Fixed duplicated bootstrap file writing logic in `generate_project`.
- **Markdown Standards Compliance**: Fixed 40+ linting errors (MD022, MD030, MD031, MD032, MD040) in `README.md` and workflows.
- **Cognitive Complexity**: Significantly reduced script complexity by refactoring monolithic generation logic into modular static methods.

### Changed (v1.6.2)

- **Code Refactor**: Replaced brittle literal string filenames for agent rules with robust class constants (`RULE_ARCHITECTURE`, `RULE_SECURITY`, etc.).
- **Tech Stack Mandate**: Updated Rule 01 to strictly mandate `ruff format` and `mypy` as pre-commit requirements.
- **Test Suite Growth**: Expanded verification suite to 68+ passing tests with 100% regression-free status.

## [1.6.0] - 2026-02-08

### Added (v1.6.0)

- **Dynamic Rule Evolution**: Enabled self-correcting AI behavior.
- **Multi-Agent Persona Orchestra**: Added Architect, UX, and Security specialists.
- **Project Ancestry**: Added global rule inheritance from `~/.antigravity`.
- **Dependency Graveyard**: Added tracking for failed implementations.
- **Doctor-Led Audits**: Added `/doctor` command for automated health checks.
- **Semantic RAG Pre-Optimization**: Automatic indexing of imported docs.
- **Integrated Skill Bridge**: Standardized skill runner for AI agents.
- **Blueprint Marketplace**: Added `--blueprint` flag for specialized stacks.
- **Visual Context Mapping**: Generated Mermaid architecture diagrams.
- **Time-Travel Memory**: Git-integrated session history.

## [1.5.4] - 2026-02-08

### Documentation (v1.5.4)

- **Gitea Focus**: Added a dedicated "Gitea Support" section to `README.md`.
- **Template Update**: Updated `PROFESSIONAL_README_TEMPLATE` to highlight Gitea capabilities.
- **Badge**: Added Gitea badge to `README.md`.

## [1.5.3] - 2026-02-07

### Documentation (v1.5.3)

- Updated `README.md` "Generated Architecture" to include `.gitea/` and `.github/` structures.
- Updated `PROFESSIONAL_README_TEMPLATE` to reference platform configuration directories.

## [1.5.2] - 2026-02-07

### Fixed (v1.5.2)

- Applied `ruff format` to ensure stylistic consistency.

## [1.5.1] - 2026-02-07

### Fixed (v1.5.1)

- Fixed whitespace lints (W293) in `antigravity_master_setup.py`.
- Corrected f-string placeholders in dry-run report.

## [1.5.0] - 2026-02-07

### Added (v1.5.0)

- **Gitea Support**: Added native support for Gitea (local versioning) including auto-generation of `.gitea/` directories and issue templates.
- **Enhanced Platform Support**: Improved cross-platform support for local development environments.
- **Full Project Audit**: Completed a line-by-line professional audit (AUDIT.md) to ensure 100/100 production readiness.

### Changed (v1.5.0)

- **Version Bump**: Synchronized versioning across all core files to v1.5.0.

## [1.4.5] - 2026-02-02

### Changed (v1.4.5)

- **Streamlined Architecture**: Stripped out support for non-core environments (Cursor, Windsurf) and languages (Rust, Go, PHP, etc.) to focus exclusively on **GitHub**, **VS Code**, and **Antigravity** workflows.
- **Focused Support**: `GITIGNORE_MAP`, `NIX_PACKAGE_MAP`, and `VSCODE_EXTENSIONS_MAP` now only support Python, Node.js/Web, and essential tools (Docker).
- **Refactoring**: Removed unused constants and templates (`CURSOR_RULES`, `WINDSURF_RULES`) to reduce script size and complexity.

## [1.4.4] - 2026-01-25

### Added (v1.4.4)

- **VS Code Integration**: Auto-generates `.vscode/` directory with:
  - `extensions.json` (detected tech stack recommendations)
  - `settings.json` (formatter config, exclusions)
  - `launch.json` and `tasks.json` placeholders
- **Refactoring**: Reduced cognitive complexity in `doctor_project` and `run_cli_mode`
- **Helper Functions**: Added `_doctor_check_dir` and `_doctor_check_file`

### Changed (v1.4.4)

- **Cleaner Code**: Removed duplicate string literals via `AntigravityResources` constants
- **Linting**: Fixed nested `if` and redundant types to satisfy stricter linting rules

## [1.4.3] - 2026-01-24

### Added (v1.4.3)

- **Doctor Regeneration**: `--doctor` with `--fix` now regenerates missing/empty required files
- **Safe Brain Dumps**: Introduced `slugify_title` for safer assimilated filenames
- **Verbose Dry Run**: Expanded `--dry-run` output to show every file generated

### Changed (v1.4.3)

- **Final Polish**: Designated as definitive single-file architecture

## [1.4.2] - 2026-01-24

### Changed (v1.4.2)

- Version synchronization across all project files
- Documentation consistency improvements

## [1.4.1] - 2026-01-24

### Added (v1.4.1)

- **AI IDE Compatibility**: Auto-generates `.cursorrules` and `.windsurfrules` for maximum compatibility
  - Cursor IDE support with dedicated rules file and Composer mode guidance
  - Windsurf IDE support with Cascade AI-specific workflows and memory integration
  - Comprehensive instructions tailored to each IDE's unique features
- **GitHub Copilot Instructions**: Auto-generates `.github/copilot-instructions.md` for all new projects
  - Provides comprehensive AI agent guidance with project context
  - Includes development workflows, coding standards, and commit conventions
  - Documents common tasks, integration points, and key file references
  - Template dynamically includes detected tech stack
- **Universal AI Assistant Support**: Projects now work seamlessly across multiple AI coding tools
  - GitHub Copilot (VS Code, Visual Studio, JetBrains)
  - Cursor IDE with AI Composer
  - Windsurf with Cascade AI agent
  - Google Gemini CLI / Project IDX
  - Generic AI assistants via .agent/ structure

### Changed (v1.4.1)

- **GitHub Templates**: AI instruction files now part of standard scaffolding
- **Documentation**: Updated README with AI IDE compatibility matrix
- **Test Coverage**: Added tests for .cursorrules and .windsurfrules generation

### Technical (v1.4.1)

- All 62+ tests passing (100% regression-free)
- Zero external dependencies added
- Single-file portability preserved
- Script size: ~1,700 lines, 62KB

## [1.4.0] - 2026-01-24

### Added (v1.4.0)

- **GitHub Templates**: Auto-generates `.github/` with professional templates
  - Issue templates: bug report, feature request, question
  - Pull request template with checklist
  - FUNDING.yml for sponsorship links
  - Issue config.yml for template configuration
- **Versioning Automation**: Added bump2version configuration to pyproject.toml
  - Auto-updates VERSION in script, pyproject.toml, and README badge
  - Creates git commit and tag automatically

### Changed (v1.4.0)

- **Major Refactoring**: Transformed script into hybrid class-based architecture
  - Created `AntigravityResources` class for all templates, constants, and mappings
  - Created `AntigravityEngine` class for file system operations and validation
  - Created `AntigravityBuilder` class for dynamic configuration generators
  - Created `AntigravityAssimilator` class for brain dump parsing logic
  - Created `AntigravityGenerator` class for project generation orchestration
- **Architecture**: Reorganized ~800+ lines into 5 focused, maintainable classes
- **Compatibility**: Maintained 100% backward compatibility via module-level function aliases
- **CONTRIBUTING.md**: Expanded with full guidelines, architecture docs, and versioning info

### Technical (v1.4.0)

- All 59 tests passing (100% regression-free)
- Zero external dependencies added
- Single-file portability preserved
- Script size: 1,393 lines, 48.3KB

## [1.3.0] - 2026-01-24

### Added (v1.3.0)

- **CLI Mode:** Full command-line interface with argparse.
  - `--name`, `--stack`, `--brain-dump`, `--safe` for scripted project creation.
  - `--dry-run` to preview actions without creating files.
  - `--templates` for custom template directories.
  - `--version` flag.
- **Doctor Mode:** Validate existing projects with `--doctor ./path`.
  - Reports missing directories, files, and empty files.
  - `--fix` flag to auto-repair issues.
- **License Selection:** Added `--license` flag (mit, apache, gpl) and interactive choice.
- **Community Standards Expansion:** Auto-generation of `SECURITY.md` and `CODE_OF_CONDUCT.md`.
- **Aesthetics:** Added GitHub badges for Ruff, Black, and Python support to README.
- **Doctor Improvements:** Expanded health check to validate all 16 core files/folders.
- **CLI Project Creation:** Added `--license` command.
- **Bug Fix:** Resolved `argparse` action type error.

### Changed (v1.3.0)

- `generate_project()` now accepts `safe_mode` and `custom_templates` parameters.
- Interactive mode preserved for backwards compatibility (run with no arguments).
- Version number now embedded in script as `VERSION = "1.3.0"`.

## [1.0.0] - 2026-01-24

### Added (v1.0.0)

- **Core Script:** Single-file `antigravity_master_setup.py` with zero external dependencies.
- **Knowledge Assimilation:** Intelligent parsing of "Brain Dumps" into Rules/Workflows/Docs.
- **Agent Architecture:** Auto-generation of `.agent/` structure (Memory, Skills, Rules, Workflows).
- **Privacy Controls:** Automatic `.gitignore` of `.agent/` and `context/` directories.
- **Model Dispatch Protocol:** "Context Handoff" system for switching between Logic/Reasoning models.
- **Safe Update Mode:** Non-destructive updates for existing projects.
- **Community Standards:** Auto-generation of `CHANGELOG.md`, `CONTRIBUTING.md`, and `AUDIT.md`.
- **Production Engineering:**
  - CI/CD workflows (GitHub Actions).
  - Ruff linting and Black formatting.
  - Pytest test suite (59 tests, cross-platform).
  - MyPy type checking.
- **Cloud-Ready:** `.idx/dev.nix` for Google IDX and `.devcontainer/` for VS Code/Codespaces.
- **Polyglot Support:** Python, Node.js, Rust, Go, Java, PHP, Ruby, Docker, SQL.
