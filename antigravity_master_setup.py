import os
import sys
import re
import logging
import json
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

GITIGNORE_MAP = {
    "python": "\n# --- Python ---\n__pycache__/\n*.pyc\nvenv/\n.venv/\n.pytest_cache/\n.mypy_cache/\n*.egg-info/\n",
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
NIX_PACKAGE_MAP = {
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
# Used to determine if a section of text is a Rule, Workflow, or Skill
CLASSIFICATION_RULES = {
    "rules": ["always", "never", "must", "style", "convention", "standard", "protocol", "policy", "lint", "formatting", "security"],
    "workflows": ["step", "guide", "process", "workflow", "how-to", "deploy", "setup", "run", "execution", "plan", "roadmap"],
    "skills": ["command", "cli", "tool", "usage", "utility", "script", "automation", "flags", "arguments", "terminal"],
    "docs": ["overview", "architecture", "introduction", "background", "context", "diagram", "concept", "summary"]
}

# ==============================================================================
# 2. SYSTEM UTILITIES & LOGGING
# ==============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("antigravity_setup.log", mode='w', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

def sanitize_name(name):
    """Ensures project name is valid for file system."""
    if not name: return "antigravity-project"
    clean = re.sub(r'\s+', '_', name.strip())
    clean = re.sub(r'[^a-zA-Z0-9_\-]', '', clean)
    return clean

def parse_keywords(input_str):
    """Converts comma/space separated string to list of keywords."""
    if not input_str: return []
    raw = re.split(r'[,\s]+', input_str)
    return [w.lower().strip() for w in raw if w.strip()]

def write_file(path, content):
    """Writes a new file. Overwrites if exists."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        logging.info(f"✅ Created: {path}")
    except OSError as e:
        logging.error(f"❌ Error writing {path}: {e}")

def append_file(path, content):
    """Appends content to a file (used for Assimilation)."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write("\n\n" + content.strip() + "\n")
        logging.info(f"🔗 Appended to: {path}")
    except OSError as e:
        logging.error(f"❌ Error appending {path}: {e}")

def create_folder(path):
    """Creates a folder and adds .gitkeep so Git tracks it."""
    try:
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, ".gitkeep"), "w") as f:
            f.write("") 
        logging.info(f"📂 Dir Created: {path}")
    except OSError as e:
        logging.error(f"❌ Error creating folder {path}: {e}")

# ==============================================================================
# 3. CONTENT BUILDERS (DYNAMIC CONFIG)
# ==============================================================================

def build_gitignore(keywords):
    content = BASE_GITIGNORE
    for k in keywords:
        if k in GITIGNORE_MAP: content += GITIGNORE_MAP[k]
        elif k in ["js", "javascript"]: content += GITIGNORE_MAP.get("node", "")
    return content

def build_nix_config(keywords):
    packages = ["pkgs.git", "pkgs.curl", "pkgs.jq", "pkgs.openssl"]
    for k in keywords:
        key = k
        if k in ["js", "javascript", "react", "nextjs"]: key = "node"
        if k in ["django", "flask", "fastapi"]: key = "python"
        if key in NIX_PACKAGE_MAP: packages.extend(NIX_PACKAGE_MAP[key])
    
    package_str = "\n    ".join(sorted(list(set(packages))))
    return f"""
# Google Project IDX Environment Configuration
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

def build_tech_stack_rule(keywords):
    return f"""
# Technology Stack
Keywords Detected: {', '.join(keywords)}

## Directives
1. **Inference:** Assume standard frameworks for these keywords (e.g., React implies standard hooks/components).
2. **Tooling:** Use the standard CLI tools (pip, npm, cargo, go mod).
3. **Files:** Look for `pyproject.toml`, `package.json`, or similar to confirm versions.
"""

# ==============================================================================
# 4. THE ASSIMILATOR (INTELLIGENT PARSING)
# ==============================================================================

def identify_category(text):
    """Heuristics to decide if text is a Rule, Workflow, or Skill."""
    text = text.lower()
    scores = {key: 0 for key in CLASSIFICATION_RULES}
    
    for category, keywords in CLASSIFICATION_RULES.items():
        for k in keywords:
            scores[category] += len(re.findall(r'\b' + re.escape(k) + r'\b', text))
            
    best_cat = max(scores, key=scores.get)
    if scores[best_cat] == 0: return "docs"
    return best_cat

def process_brain_dump(filepath, base_dir):
    """Reads a big file, splits by headers, and distributes to .agent/ folders."""
    if not filepath or not os.path.exists(filepath):
        return []

    print(f"\n🧠 Assimilating knowledge from: {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            full_text = f.read()
    except Exception as e:
        logging.error(f"Could not read brain dump: {e}")
        return []

    # 1. Archive Raw Content
    raw_dest = os.path.join(base_dir, "context", "raw", "master_brain_dump.md")
    write_file(raw_dest, full_text)

    # 2. Extract Tech Stack Keywords
    detected_keywords = set()
    for k in GITIGNORE_MAP.keys():
        if re.search(r'\b' + re.escape(k) + r'\b', full_text.lower()):
            detected_keywords.add(k)

    # 3. Split & Distribute
    # Splits on lines starting with # (Markdown headers)
    sections = re.split(r'(^#+\s+.*$)', full_text, flags=re.MULTILINE)
    
    for i in range(1, len(sections), 2):
        if i+1 >= len(sections): break
        header = sections[i].strip()
        content = sections[i+1].strip()
        if not content: continue

        category = identify_category(header + "\n" + content)
        safe_title = re.sub(r'[^a-zA-Z0-9]', '_', header).lower().strip('_')[:50]
        
        if category == "rules":
            dest = os.path.join(base_dir, ".agent", "rules", f"imported_{safe_title}.md")
        elif category == "workflows":
            dest = os.path.join(base_dir, ".agent", "workflows", f"imported_{safe_title}.md")
        elif category == "skills":
            dest = os.path.join(base_dir, ".agent", "skills", f"imported_{safe_title}", "SKILL.md")
        else:
            dest = os.path.join(base_dir, "docs", "imported", f"{safe_title}.md")

        formatted = f"<!-- Auto-Assimilated Source -->\n\n{header}\n\n{content}"
        append_file(dest, formatted)

    print("🧠 Assimilation Complete.")
    return list(detected_keywords)

# ==============================================================================
# 5. MAIN EXECUTION FLOW
# ==============================================================================

def main():
    print("=========================================================")
    print("   🌌 Antigravity Architect: The Master Script")
    print("   Dynamic Parsing | Knowledge Distribution | Universal")
    print("=========================================================")

    # --- STEP 1: INPUTS ---
    print("\n[Optional] Drag & Drop a Brain Dump file (Specs/Notes/Code):")
    brain_dump_path = input("Path: ").strip().strip("'\"")

    raw_name = input("\nProject Name: ")
    project_name = sanitize_name(raw_name)
    if not project_name: return

    manual_keywords = []
    if not brain_dump_path:
        print("\nTech Stack (e.g. python, react, aws):")
        k_in = input("Keywords: ")
        manual_keywords = parse_keywords(k_in)
        if not any(x in manual_keywords for x in ["macos", "windows", "linux"]):
            manual_keywords.append("linux")

    # --- STEP 2: SCAFFOLDING ---
    base_dir = os.path.join(os.getcwd(), project_name)
    if os.path.exists(base_dir):
        if input(f"⚠️  '{project_name}' exists. Overwrite? (y/n): ").lower() != 'y': return

    print(f"\n🚀 Constructing '{project_name}'...")

    # Create All Directories (With .gitkeep)
    dirs = [
        "src", "tests", "docs/imported", 
        "context/raw", 
        ".idx", ".devcontainer",
        ".agent/rules", ".agent/workflows", ".agent/skills", ".agent/memory",
        ".agent/skills/git_automation", ".agent/skills/secrets_manager"
    ]
    for d in dirs: create_folder(os.path.join(base_dir, d))

    # --- STEP 3: ASSIMILATION & CONFIG ---
    detected_stack = []
    if brain_dump_path and os.path.exists(brain_dump_path):
        detected_stack = process_brain_dump(brain_dump_path, base_dir)
    
    final_stack = list(set(manual_keywords + detected_stack))
    if not final_stack: final_stack = ["linux"]
    print(f"⚙️  Final Tech Stack: {', '.join(final_stack)}")

    # Write Configs
    write_file(os.path.join(base_dir, ".gitignore"), build_gitignore(final_stack))
    write_file(os.path.join(base_dir, ".idx", "dev.nix"), build_nix_config(final_stack))
    write_file(os.path.join(base_dir, ".devcontainer", "devcontainer.json"), """
{
  "name": "Antigravity Universal",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": { "ghcr.io/devcontainers/features/common-utils:2": {} }
}
""")
    write_file(os.path.join(base_dir, "README.md"), f"# {project_name}\n\nStack: {', '.join(final_stack)}")
    write_file(os.path.join(base_dir, ".env.example"), "API_KEY=\nDB_URL=")

    # --- STEP 4: GENERATE STATIC AGENT BRAIN ---
    # These are the "Immutable" rules that exist regardless of the brain dump.

    # Rule: Identity
    write_file(os.path.join(base_dir, ".agent", "rules", "00_identity.md"), """
# System Identity
You are a Senior Polyglot Software Engineer and Product Architect.
- **Safety:** Never delete data without asking. Never leak secrets.
- **Context:** Always check `docs/imported` and `context/raw` before coding.
""")

    # Rule: Security
    write_file(os.path.join(base_dir, ".agent", "rules", "02_security.md"), """
# Security Protocols
1. **Secrets:** Never output API keys. Use `.env`.
2. **Inputs:** Validate all inputs.
3. **Dependencies:** Warn if using deprecated libraries.
""")

    # Rule: Git Conventions
    write_file(os.path.join(base_dir, ".agent", "rules", "03_git.md"), """
# Git Conventions
- Use Conventional Commits (`feat:`, `fix:`, `docs:`).
- Never commit to main without testing.
""")

    # Rule: Chain of Thought
    write_file(os.path.join(base_dir, ".agent", "rules", "04_reasoning.md"), """
# Reasoning Protocol
1. **Pause:** Analyze the request.
2. **Plan:** Break it down step-by-step.
3. **Check:** Verify against `docs/` constraints.
4. **Execute:** Write code.
""")

    # Dynamic Rule: Tech Stack
    write_file(os.path.join(base_dir, ".agent", "rules", "01_tech_stack.md"), build_tech_stack_rule(final_stack))

    # --- STEP 5: GENERATE WORKFLOWS ---

    write_file(os.path.join(base_dir, ".agent", "workflows", "plan.md"), """
---
trigger: /plan
---
# Plan Workflow
1. Read `docs/imported/` and `context/raw/`.
2. Break request into atomic tasks.
3. Check against `.agent/rules/`.
4. Output plan and update `scratchpad.md`.
""")

    write_file(os.path.join(base_dir, ".agent", "workflows", "bootstrap.md"), """
---
trigger: /bootstrap
---
# Bootstrap Workflow
1. Read `.agent/rules/01_tech_stack.md`.
2. Generate boilerplate code for the detected stack.
3. Ensure `.gitignore` is respected.
""")

    write_file(os.path.join(base_dir, ".agent", "workflows", "commit.md"), """
---
trigger: /commit
---
# Smart Commit
1. Run `git status`.
2. Analyze diffs.
3. Generate Conventional Commit message.
4. Ask for approval.
""")

    write_file(os.path.join(base_dir, ".agent", "workflows", "review.md"), """
---
trigger: /review
---
# Code Review
1. Check for Security risks (Rule 02).
2. Check for Code Style (Rule 01).
3. Report issues sorted by severity.
""")

    write_file(os.path.join(base_dir, ".agent", "workflows", "save.md"), """
---
trigger: /save
---
# Save Memory
1. Summarize recent actions.
2. Update `.agent/memory/scratchpad.md`.
""")

    # --- STEP 6: GENERATE SKILLS ---

    write_file(os.path.join(base_dir, ".agent", "skills", "git_automation", "SKILL.md"), """
---
name: git_automation
description: Safe git operations.
---
# Git Skill
**Commands:** `git status`, `git diff`, `git add`, `git commit`.
**Rule:** Always verify status before adding.
""")

    write_file(os.path.join(base_dir, ".agent", "skills", "secrets_manager", "SKILL.md"), """
---
name: secrets_manager
description: Handle API keys.
---
# Secrets Skill
**Action:** Detect secrets in code. Move them to `.env`. Replace with `os.getenv()`.
""")

    # --- STEP 7: MEMORY & BOOTSTRAP ---

    write_file(os.path.join(base_dir, ".agent", "memory", "scratchpad.md"), f"""
# Project Scratchpad
*Last Updated: {datetime.now()}*
## Status
- Project initialized.
- Tech Stack: {', '.join(final_stack)}.
- Imported Knowledge: {'Yes' if brain_dump_path else 'No'}.
""")

    write_file(os.path.join(base_dir, "BOOTSTRAP_INSTRUCTIONS.md"), """
# Agent Start Guide
1. **Context:** Read `.agent/memory/scratchpad.md`.
2. **Knowledge:** Check `docs/imported/` for assimilated rules.
3. **Action:** Run `/bootstrap` to generate the application skeleton.
""")

    print(f"\n✨ Success! Project '{project_name}' is fully configured.")
    print(f"👉 To begin: cd {project_name}")
    print("👉 Then open in Antigravity and type: 'Read BOOTSTRAP_INSTRUCTIONS.md'")

if __name__ == "__main__":
    main()
