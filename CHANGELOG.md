# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.4.4] - 2026-01-25

### Added

- **VS Code Integration**: Auto-generates `.vscode/` directory with:
  - `extensions.json` (detected tech stack recommendations)
  - `settings.json` (formatter config, exclusions)
  - `launch.json` and `tasks.json` placeholders
- **Refactoring**: Reduced cognitive complexity in `doctor_project` and `run_cli_mode`
- **Helper Functions**: Added `_doctor_check_dir` and `_doctor_check_file`

### Changed

- **Cleaner Code**: Removed duplicate string literals via `AntigravityResources` constants
- **Linting**: Fixed nested `if` and redundant types to satisfy stricter linting rules

## [1.4.3] - 2026-01-24

### Added

- **Doctor Regeneration**: `--doctor` with `--fix` now regenerates missing/empty required files
- **Safe Brain Dumps**: Introduced `slugify_title` for safer assimilated filenames
- **Verbose Dry Run**: Expanded `--dry-run` output to show every file generated

### Changed

- **Final Polish**: Designated as definitive single-file architecture

## [1.4.2] - 2026-01-24

### Changed

- Version synchronization across all project files
- Documentation consistency improvements

## [1.4.1] - 2026-01-24

### Added

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

### Changed

- **GitHub Templates**: AI instruction files now part of standard scaffolding
- **Documentation**: Updated README with AI IDE compatibility matrix
- **Test Coverage**: Added tests for .cursorrules and .windsurfrules generation

### Technical

- All 62+ tests passing (100% regression-free)
- Zero external dependencies added
- Single-file portability preserved
- Script size: ~1,700 lines, 62KB

## [1.4.0] - 2026-01-24

### Added

- **GitHub Templates**: Auto-generates `.github/` with professional templates
  - Issue templates: bug report, feature request, question
  - Pull request template with checklist
  - FUNDING.yml for sponsorship links
  - Issue config.yml for template configuration
- **Versioning Automation**: Added bump2version configuration to pyproject.toml
  - Auto-updates VERSION in script, pyproject.toml, and README badge
  - Creates git commit and tag automatically

### Changed

- **Major Refactoring**: Transformed script into hybrid class-based architecture
  - Created `AntigravityResources` class for all templates, constants, and mappings
  - Created `AntigravityEngine` class for file system operations and validation
  - Created `AntigravityBuilder` class for dynamic configuration generators
  - Created `AntigravityAssimilator` class for brain dump parsing logic
  - Created `AntigravityGenerator` class for project generation orchestration
- **Architecture**: Reorganized ~800+ lines into 5 focused, maintainable classes
- **Compatibility**: Maintained 100% backward compatibility via module-level function aliases
- **CONTRIBUTING.md**: Expanded with full guidelines, architecture docs, and versioning info

### Technical

- All 59 tests passing (100% regression-free)
- Zero external dependencies added
- Single-file portability preserved
- Script size: 1,393 lines, 48.3KB

## [1.3.0] - 2026-01-24

### Added

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

### Changed

- `generate_project()` now accepts `safe_mode` and `custom_templates` parameters.
- Interactive mode preserved for backwards compatibility (run with no arguments).
- Version number now embedded in script as `VERSION = "1.3.0"`.

## [1.0.0] - 2026-01-24

### Added

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
