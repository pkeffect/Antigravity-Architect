#!/usr/bin/env python3
"""
Antigravity Architect: Master Edition

A universal "Agent-First" bootstrapping tool that creates self-describing
repositories for AI-assisted development. Generates project scaffolding with
embedded rules, workflows, skills, and memory for AI agents.

Designed for Google Antigravity, Project IDX, Gemini Code Assist, and VS Code.

Usage:
    python antigravity_master_setup.py

Author: pkeffect
License: MIT
"""

from __future__ import annotations

import logging
import os
import re
import sys
import tempfile
from datetime import datetime

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
# --- Agent / AI ---
.agent/logs/
.agent/tmp/
.agent/memory/history/
agent_setup.log
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


def write_file(path: str, content: str) -> bool:
    """
    Writes a new file, creating parent directories as needed.

    Returns True on success, False on failure.
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        logging.info(f"✅ Created: {path}")
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
        "rules": os.path.join(base_dir, ".agent", "rules", f"imported_{safe_title}.md"),
        "workflows": os.path.join(base_dir, ".agent", "workflows", f"imported_{safe_title}.md"),
        "skills": os.path.join(base_dir, ".agent", "skills", f"imported_{safe_title}", "SKILL.md"),
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
    write_file(raw_dest, full_text)

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


def generate_agent_files(base_dir: str, keywords: list[str]) -> None:
    """Generates all .agent/ rules, workflows, and skills."""

    # Generate static rules
    for filename, content in AGENT_RULES.items():
        path = os.path.join(base_dir, ".agent", "rules", filename)
        write_file(path, content)

    # Generate dynamic tech stack rule
    tech_stack_path = os.path.join(base_dir, ".agent", "rules", "01_tech_stack.md")
    write_file(tech_stack_path, build_tech_stack_rule(keywords))

    # Generate workflows
    for filename, content in AGENT_WORKFLOWS.items():
        path = os.path.join(base_dir, ".agent", "workflows", filename)
        write_file(path, content)

    # Generate skills
    for filename, content in AGENT_SKILLS.items():
        path = os.path.join(base_dir, ".agent", "skills", filename)
        write_file(path, content)


def generate_project(project_name: str, keywords: list[str], brain_dump_path: str | None = None) -> bool:
    """
    Main project generation logic.

    Creates the full project structure with all configurations and agent files.
    Returns True on success, False on failure.
    """
    base_dir = os.path.join(os.getcwd(), project_name)

    # Check for existing directory
    if os.path.exists(base_dir):
        response = input(f"⚠️  '{project_name}' exists. Overwrite? (y/n): ")
        if response.lower() != "y":
            return False

    print(f"\n🚀 Constructing '{project_name}'...")

    # Setup logging in target directory
    setup_logging(base_dir)

    # Create directory structure
    directories = [
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
        ".agent/skills/git_automation",
        ".agent/skills/secrets_manager",
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

    # Generate configuration files
    write_file(os.path.join(base_dir, ".gitignore"), build_gitignore(final_stack))
    write_file(os.path.join(base_dir, ".idx", "dev.nix"), build_nix_config(final_stack))
    write_file(os.path.join(base_dir, ".devcontainer", "devcontainer.json"), DEVCONTAINER_JSON)
    write_file(os.path.join(base_dir, "README.md"), f"# {project_name}\n\nStack: {', '.join(final_stack)}")
    write_file(os.path.join(base_dir, ".env.example"), "API_KEY=\nDB_URL=")

    # Generate agent files
    generate_agent_files(base_dir, final_stack)

    # Generate memory and bootstrap
    write_file(
        os.path.join(base_dir, ".agent", "memory", "scratchpad.md"),
        build_scratchpad(final_stack, bool(brain_dump_path)),
    )

    write_file(
        os.path.join(base_dir, "BOOTSTRAP_INSTRUCTIONS.md"),
        """# Agent Start Guide
1. **Context:** Read `.agent/memory/scratchpad.md`.
2. **Knowledge:** Check `docs/imported/` for assimilated rules.
3. **Action:** Run `/bootstrap` to generate the application skeleton.
""",
    )

    print(f"\n✨ Success! Project '{project_name}' is fully configured.")
    print(f"👉 To begin: cd {project_name}")
    print("👉 Then open in Antigravity and type: 'Read BOOTSTRAP_INSTRUCTIONS.md'")
    return True


# ==============================================================================
# 6. MAIN EXECUTION FLOW
# ==============================================================================


def main() -> None:
    """Main entry point for the Antigravity Architect."""
    print("=========================================================")
    print("   🌌 Antigravity Architect: The Master Script")
    print("   Dynamic Parsing | Knowledge Distribution | Universal")
    print("=========================================================")

    # Initialize logging to temp directory initially
    setup_logging()

    # STEP 1: INPUTS
    print("\n[Optional] Drag & Drop a Brain Dump file (Specs/Notes/Code):")
    brain_dump_path: str | None = input("Path: ").strip().strip("'\"") or None

    raw_name = input("\nProject Name: ")
    project_name = sanitize_name(raw_name)
    if not project_name or project_name == "antigravity-project" and not raw_name:
        print("❌ Project name is required.")
        return

    # Get keywords manually if no brain dump
    manual_keywords: list[str] = []
    if not brain_dump_path:
        print("\nTech Stack (e.g. python, react, aws):")
        k_in = input("Keywords: ")
        manual_keywords = parse_keywords(k_in)
        # Add default OS if none specified
        if not any(x in manual_keywords for x in ("macos", "windows", "linux")):
            manual_keywords.append("linux")

    # STEP 2: GENERATE PROJECT
    generate_project(project_name, manual_keywords, brain_dump_path)


if __name__ == "__main__":
    main()
