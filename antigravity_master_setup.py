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

VERSION = "1.3.0"

# ==============================================================================
# 1. KNOWLEDGE BASE & CONFIGURATION
# ==============================================================================

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
    "idea": "\n# --- JetBrains ---\n.idea/\n*.iml\n",
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
    "skills": ["command", "cli", "tool", "usage", "utility", "script", "automation", "flags", "arguments", "terminal"],
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

AGENT_DIR = ".agent"

# ==============================================================================
# 2. SYSTEM UTILITIES & LOGGING
# ==============================================================================


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


def parse_keywords(input_str: str | None) -> list[str]:
    """Converts comma/space separated string to list of lowercase keywords."""
    if not input_str:
        return []
    raw = re.split(r"[,\s]+", input_str)
    return [w.lower().strip() for w in raw if w.strip()]


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


def write_file(path: str, content: str, exist_ok: bool = False) -> bool:
    """
    Writes a new file, creating parent directories as needed.

    Args:
        path: Destination path
        content: File content
        exist_ok: If True, skip formatting if file exists (Safe Mode).
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
        logging.info(f"📂 Dir Created: {path}")
        return True
    except OSError as e:
        logging.error(f"❌ Error creating folder {path}: {e}")
        return False


# ==============================================================================
# 3. CONTENT BUILDERS (DYNAMIC CONFIG)
# ==============================================================================


def build_gitignore(keywords: list[str]) -> str:
    """Builds a .gitignore file based on detected technology keywords."""
    content = BASE_GITIGNORE
    for k in keywords:
        if k in GITIGNORE_MAP:
            content += GITIGNORE_MAP[k]
        elif k in ("js", "javascript"):
            content += GITIGNORE_MAP.get("node", "")
    return content


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
        if key in NIX_PACKAGE_MAP:
            packages.extend(NIX_PACKAGE_MAP[key])

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


def build_tech_stack_rule(keywords: list[str]) -> str:
    """Builds a dynamic tech stack rule for the agent."""
    return f"""# Technology Stack
Keywords Detected: {", ".join(keywords)}

## Directives
1. **Inference:** Assume standard frameworks for these keywords (e.g., React implies standard hooks/components).
2. **Tooling:** Use the standard CLI tools (pip, npm, cargo, go mod).
3. **Files:** Look for `pyproject.toml`, `package.json`, or similar to confirm versions.
"""


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


# ==============================================================================
# 4. THE ASSIMILATOR (INTELLIGENT PARSING)
# ==============================================================================


def identify_category(text: str) -> str:
    """
    Uses heuristics to decide if text is a Rule, Workflow, Skill, or Doc.

    Returns the category with the highest keyword match score.
    """
    text_lower = text.lower()
    scores: dict[str, int] = dict.fromkeys(CLASSIFICATION_RULES, 0)

    for category, keywords in CLASSIFICATION_RULES.items():
        for k in keywords:
            scores[category] += len(re.findall(r"\b" + re.escape(k) + r"\b", text_lower))

    best_cat = max(scores, key=lambda x: scores[x])
    if scores[best_cat] == 0:
        return "docs"
    return best_cat


def get_destination_path(base_dir: str, category: str, safe_title: str) -> str:
    """Determines the file destination based on category."""
    category_paths: dict[str, str] = {
        "rules": os.path.join(base_dir, AGENT_DIR, "rules", f"imported_{safe_title}.md"),
        "workflows": os.path.join(base_dir, AGENT_DIR, "workflows", f"imported_{safe_title}.md"),
        "skills": os.path.join(base_dir, AGENT_DIR, "skills", f"imported_{safe_title}", "SKILL.md"),
        "docs": os.path.join(base_dir, "docs", "imported", f"{safe_title}.md"),
    }
    return category_paths.get(category, category_paths["docs"])


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
    for k in GITIGNORE_MAP:
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

        category = identify_category(header + "\n" + content)
        safe_title = re.sub(r"[^a-zA-Z0-9]", "_", header).lower().strip("_")[:50]
        dest = get_destination_path(base_dir, category, safe_title)

        formatted = f"<!-- Auto-Assimilated Source -->\n\n{header}\n\n{content}"
        append_file(dest, formatted)

    print("🧠 Assimilation Complete.")
    return list(detected_keywords)


# ==============================================================================
# 5. PROJECT GENERATION
# ==============================================================================


def generate_agent_files(base_dir: str, keywords: list[str], safe_mode: bool = False) -> None:
    """Generates all .agent/ rules, workflows, and skills."""

    # Generate static rules
    for filename, content in AGENT_RULES.items():
        path = os.path.join(base_dir, AGENT_DIR, "rules", filename)
        write_file(path, content, exist_ok=safe_mode)

    # Generate dynamic tech stack rule
    tech_stack_path = os.path.join(base_dir, AGENT_DIR, "rules", "01_tech_stack.md")
    write_file(tech_stack_path, build_tech_stack_rule(keywords), exist_ok=safe_mode)

    # Generate workflows
    for filename, content in AGENT_WORKFLOWS.items():
        path = os.path.join(base_dir, AGENT_DIR, "workflows", filename)
        write_file(path, content, exist_ok=safe_mode)

    # Generate skills
    for filename, content in AGENT_SKILLS.items():
        path = os.path.join(base_dir, AGENT_DIR, "skills", filename)
        write_file(path, content, exist_ok=safe_mode)


def generate_project(
    project_name: str,
    keywords: list[str],
    brain_dump_path: str | None = None,
    safe_mode: bool | None = None,
    custom_templates: dict[str, dict[str, str]] | None = None,
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
        ".idx",
        ".devcontainer",
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
    write_file(os.path.join(base_dir, ".gitignore"), build_gitignore(final_stack), exist_ok=True)
    write_file(os.path.join(base_dir, ".idx", "dev.nix"), build_nix_config(final_stack), exist_ok=safe_mode)
    write_file(os.path.join(base_dir, ".devcontainer", "devcontainer.json"), DEVCONTAINER_JSON, exist_ok=safe_mode)
    write_file(
        os.path.join(base_dir, "README.md"), f"# {project_name}\n\nStack: {', '.join(final_stack)}", exist_ok=True
    )
    write_file(os.path.join(base_dir, ".env.example"), "API_KEY=\nDB_URL=", exist_ok=safe_mode)

    # Generate Community Standards
    write_file(os.path.join(base_dir, "CHANGELOG.md"), CHANGELOG_TEMPLATE, exist_ok=safe_mode)
    write_file(os.path.join(base_dir, "CONTRIBUTING.md"), CONTRIBUTING_TEMPLATE, exist_ok=safe_mode)
    write_file(os.path.join(base_dir, "AUDIT.md"), AUDIT_TEMPLATE, exist_ok=safe_mode)

    # Generate agent files
    generate_agent_files(base_dir, final_stack, safe_mode=safe_mode)

    # Generate memory and bootstrap (scratchpad always preserved)
    write_file(
        os.path.join(base_dir, AGENT_DIR, "memory", "scratchpad.md"),
        build_scratchpad(final_stack, bool(brain_dump_path)),
        exist_ok=True,
    )

    write_file(
        os.path.join(base_dir, "BOOTSTRAP_INSTRUCTIONS.md"),
        """# Agent Start Guide
1. **Context:** Read `.agent/memory/scratchpad.md`.
2. **Knowledge:** Check `docs/imported/` for assimilated rules.
3. **Action:** Run `/bootstrap` to generate the application skeleton.
""",
        exist_ok=safe_mode,
    )

    print(f"\n✨ Success! Project '{project_name}' is fully configured.")
    print(f"👉 To begin: cd {project_name}")
    print("👉 Then open in Antigravity and type: 'Read BOOTSTRAP_INSTRUCTIONS.md'")
    return True


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

    Returns True if healthy, False if issues found.
    """
    print(f"\n🩺 Running Doctor on: {project_path}")
    print("=" * 50)

    base_dir = Path(project_path)
    if not base_dir.exists():
        print(f"❌ Project directory not found: {project_path}")
        return False

    issues: list[str] = []
    warnings: list[str] = []
    passed: list[str] = []

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
                print(f"   🔧 Fixed: Created {dir_path}/")

    required_files = {
        ".agent/rules/00_identity.md": "Agent identity rule",
        ".agent/rules/01_tech_stack.md": "Tech stack rule",
        ".agent/memory/scratchpad.md": "Memory scratchpad",
        "BOOTSTRAP_INSTRUCTIONS.md": "Bootstrap guide",
    }

    for file_path, description in required_files.items():
        full_path = base_dir / file_path
        if full_path.exists():
            if full_path.stat().st_size == 0:
                warnings.append(f"⚠️  {file_path} exists but is empty")
            else:
                passed.append(f"✅ {file_path} exists ({description})")
        else:
            issues.append(f"❌ Missing: {file_path} ({description})")

    optional_files = [
        ".gitignore",
        "README.md",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "AUDIT.md",
    ]

    for file_path in optional_files:
        full_path = base_dir / file_path
        if full_path.exists():
            passed.append(f"✅ {file_path} exists")
        else:
            warnings.append(f"⚠️  Optional: {file_path} not found")

    for item in passed:
        print(item)
    for item in warnings:
        print(item)
    for item in issues:
        print(item)

    print("=" * 50)
    print(f"Summary: {len(passed)} passed, {len(warnings)} warnings, {len(issues)} issues")

    if issues:
        print("\n💡 Tip: Run with --fix to attempt automatic repairs.")
        return False
    elif warnings:
        print("\n✨ Project is healthy with minor recommendations.")
        return True
    else:
        print("\n🏆 Project is fully healthy!")
        return True


def list_keywords() -> None:
    """Display all supported tech stack keywords."""
    print("\n🛠 Supported Tech Stack Keywords")
    print("=" * 50)

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

    print("\n" + "=" * 50)
    print("Usage: --stack python,react,docker")


def run_interactive_mode() -> None:
    """Original interactive mode for backwards compatibility."""
    print("=========================================================")
    print(f"   🌌 Antigravity Architect v{VERSION}")
    print("   Dynamic Parsing | Knowledge Distribution | Universal")
    print("=========================================================")

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

    generate_project(project_name, manual_keywords, brain_dump_path)


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
        print("=" * 50)
        print(f"Project Name: {project_name}")
        print(f"Tech Stack: {', '.join(keywords)}")
        print(f"Brain Dump: {args.brain_dump or 'None'}")
        print(f"Safe Mode: {args.safe}")
        print(f"Templates: {args.templates or 'Default'}")
        print("\nDirectories that would be created:")
        dirs = [
            "src",
            "tests",
            "docs/imported",
            "context/raw",
            ".idx",
            ".devcontainer",
            ".agent/rules",
            ".agent/workflows",
            ".agent/skills",
            ".agent/memory",
        ]
        for d in dirs:
            print(f"  📁 {project_name}/{d}/")
        print("\nFiles that would be created:")
        files = [
            ".gitignore",
            "README.md",
            "CHANGELOG.md",
            "CONTRIBUTING.md",
            "AUDIT.md",
            "BOOTSTRAP_INSTRUCTIONS.md",
            ".env.example",
        ]
        for f in files:
            print(f"  📄 {project_name}/{f}")
        print("\n✅ Dry run complete. No changes made.")
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
