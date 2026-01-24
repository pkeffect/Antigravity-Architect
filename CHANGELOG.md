# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.4.0] - 2026-01-24

### Changed
- **Major Refactoring**: Transformed script into hybrid class-based architecture
  - Created `AntigravityResources` class for all templates, constants, and mappings
  - Created `AntigravityEngine` class for file system operations and validation
  - Created `AntigravityBuilder` class for dynamic configuration generators
  - Created `AntigravityAssimilator` class for brain dump parsing logic
  - Created `AntigravityGenerator` class for project generation orchestration
- **Architecture**: Reorganized ~800+ lines into 5 focused, maintainable classes
- **Compatibility**: Maintained 100% backward compatibility via module-level function aliases

### Technical
- All 59 tests passing (100% regression-free)
- Zero external dependencies added
- Single-file portability preserved
- Improved code organization and maintainability

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
