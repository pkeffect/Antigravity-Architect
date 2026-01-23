import os
import sys
import re
import logging
from datetime import datetime

# ==========================================
# 1. CONFIGURATION DATA (The Knowledge Base)
# ==========================================

# A. Gitignore Rules (Universal + Language Specific)
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
    # Languages
    "python": "\n# --- Python ---\n__pycache__/\n*.pyc\nvenv/\n.venv/\n.pytest_cache/\n.mypy_cache/\n*.egg-info/\n",
    "node": "\n# --- Node/JS ---\nnode_modules/\ndist/\nbuild/\ncoverage/\n.npm/\n.eslintcache\n.yarn-integrity\n",
    "typescript": "\n# --- TypeScript ---\n*.tsbuildinfo\n",
    "rust": "\n# --- Rust ---\n/target\nCargo.lock\n**/*.rs.bk\n",
    "go": "\n# --- Go ---\n/bin/\n/pkg/\n/dist/\n",
    "java": "\n# --- Java ---\n*.class\n*.jar\n*.war\nbuild/\n.gradle/\n",
    "php": "\n# --- PHP ---\n/vendor/\n.phpunit.result.cache\n",
    "ruby": "\n# --- Ruby ---\n/.bundle/\n/vendor/bundle/\n",
    
    # Frameworks
    "django": "\n# --- Django ---\n*.log\nlocal_settings.py\ndb.sqlite3\nmedia/\nstaticfiles/\n",
    "flask": "\n# --- Flask ---\ninstance/\n.webassets-cache\n",
    "react": "\n# --- React ---\nbuild/\n.env.local\n",
    "nextjs": "\n# --- NextJS ---\n.next/\nout/\n",
    "vue": "\n# --- Vue ---\n.nuxt/\ndist/\n",
    "angular": "\n# --- Angular ---\n.angular/\n",
    "laravel": "\n# --- Laravel ---\n/vendor\n/node_modules\n.env\n",
    
    # OS / Editors
    "macos": "\n# --- macOS ---\n.DS_Store\n.AppleDouble\n",
    "windows": "\n# --- Windows ---\nThumbs.db\nehthumbs.db\n*.exe\n*.dll\n",
    "linux": "\n# --- Linux ---\n*~\n.fuse_hidden*\n",
    "vscode": "\n# --- VS Code ---\n.vscode/\n",
    "idea": "\n# --- JetBrains ---\n.idea/\n*.iml\n",
}

# B. Nix Packages (For Google IDX / Antigravity Cloud)
# Maps keywords to NixOS package names
NIX_PACKAGE_MAP = {
    "python": ["pkgs.python312", "pkgs.python312Packages.pip", "pkgs.python312Packages.virtualenv", "pkgs.ruff"],
    "node": ["pkgs.nodejs_20", "pkgs.nodePackages.nodemon"],
    "typescript": ["pkgs.nodePackages.typescript"],
    "rust": ["pkgs.cargo", "pkgs.rustc", "pkgs.rustfmt"],
    "go": ["pkgs.go", "pkgs.gopls"],
    "java": ["pkgs.jdk17", "pkgs.maven"],
    "php": ["pkgs.php", "pkgs.php82Packages.composer"],
    "ruby": ["pkgs.ruby"],
    "docker": ["pkgs.docker", "pkgs.docker-compose"],
    "sql": ["pkgs.sqlite", "pkgs.postgresql"],
}

# ==========================================
# 2. SYSTEM UTILITIES
# ==========================================

# Configure logging to file AND console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("antigravity_setup.log", mode='w', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

def sanitize_name(name):
    """Ensure project name is safe for the filesystem."""
    if not name: return None
    # Replace spaces with underscores
    clean = re.sub(r'\s+', '_', name.strip())
    # Remove anything that isn't alphanumeric, underscore, or dash
    clean = re.sub(r'[^a-zA-Z0-9_\-]', '', clean)
    return clean

def parse_keywords(input_str):
    """Convert comma-separated string to list of lowercase keywords."""
    if not input_str: return []
    # Split by comma or whitespace
    raw = re.split(r'[,\s]+', input_str)
    # Clean and remove empty strings
    return [w.lower().strip() for w in raw if w.strip()]

def write_file(path, content):
    """Write content to file with UTF-8 encoding."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        logging.info(f"✅ Created File: {path}")
    except OSError as e:
        logging.error(f"❌ Error writing {path}: {e}")

def create_folder(path):
    """Create a folder and add .gitkeep so Git tracks it."""
    try:
        os.makedirs(path, exist_ok=True)
        # Create .gitkeep
        with open(os.path.join(path, ".gitkeep"), "w") as f:
            f.write("") 
        logging.info(f"📂 Created Dir:  {path} (Verified with .gitkeep)")
    except OSError as e:
        logging.error(f"❌ Error creating folder {path}: {e}")

# ==========================================
# 3. CONTENT BUILDERS
# ==========================================

def build_gitignore_content(keywords):
    """Dynamically assemble .gitignore based on stack."""
    content = BASE_GITIGNORE
    for k in keywords:
        # Direct match
        if k in GITIGNORE_MAP:
            content += GITIGNORE_MAP[k]
        # Aliases
        elif k in ["js", "javascript"]: 
            content += GITIGNORE_MAP.get("node", "")
        elif k in ["ts"]:
            content += GITIGNORE_MAP.get("typescript", "")
        elif k in ["py"]:
            content += GITIGNORE_MAP.get("python", "")
            
    return content

def build_nix_config(keywords):
    """Dynamically assemble .idx/dev.nix for Cloud IDEs."""
    packages = ["pkgs.git", "pkgs.curl", "pkgs.jq", "pkgs.openssl", "pkgs.zip"]
    
    for k in keywords:
        key = k
        # Map aliases to keys
        if k in ["js", "javascript", "react", "nextjs", "vue", "angular"]: key = "node"
        if k in ["ts"]: key = "typescript"
        if k in ["django", "flask", "fastapi"]: key = "python"
        
        if key in NIX_PACKAGE_MAP:
            packages.extend(NIX_PACKAGE_MAP[key])
    
    # Deduplicate and sort
    packages = sorted(list(set(packages)))
    package_list_str = "\n    ".join(packages)

    return f"""
# Google Project IDX / Antigravity Environment Definition
{{ pkgs, ... }}: {{
  # Use Stable Channel
  channel = "stable-23.11";
  
  # Tools available to the Agent
  packages = [
    {package_list_str}
  ];
  
  # Environment Variables
  env = {{}};
  
  # Editor Configuration
  idx = {{
    extensions = [
      "google.gemini-code-assist"
      "ms-azuretools.vscode-docker"
    ];
    workspace = {{
      onCreate = {{
        # Runs once when workspace is created
        setup = "echo 'Antigravity Environment Initialized'";
      }};
    }};
  }};
}}
"""

def build_tech_stack_rule(keywords):
    stack_list = ", ".join(keywords)
    return f"""
# Dynamic Tech Stack Configuration

The user has explicitly defined the following technology keywords:
**{stack_list}**

## Directives for the Agent:
1. **Inference:** Based on these keywords, assume standard frameworks (e.g., 'react' implies `create-react-app` or `vite` structures).
2. **Tooling:** Use the standard CLI tools associated with these keywords (pip, npm, cargo, etc).
3. **Files:** Look for standard configuration files (`pyproject.toml`, `package.json`) to confirm specific versions.
"""

# ==========================================
# 4. MAIN SETUP LOGIC
# ==========================================

def setup_project():
    print("=========================================================")
    print("   🚀 Google Antigravity: The Master Setup Script")
    print("   Dynamic | Universal | Git-Ready | Memory-Enabled")
    print("=========================================================")

    # --- STEP 1: GATHER INPUT ---
    raw_name = input("1. Enter Project Name: ")
    project_name = sanitize_name(raw_name)
    if not project_name:
        logging.critical("Invalid Project Name. Aborting.")
        return

    base_dir = os.path.join(os.getcwd(), project_name)
    if os.path.exists(base_dir):
        if input(f"⚠️  Folder '{project_name}' exists. Overwrite? (y/n): ").strip().lower() != 'y':
            print("Aborting.")
            return

    print("\n2. Tech Stack & Environment")
    print("   (Enter keywords separated by commas, e.g.: python, react, postgres, macos)")
    keywords_input = input("   Keywords: ")
    keywords = parse_keywords(keywords_input)
    
    # Add defaults if missing
    if not any(k in keywords for k in ["macos", "windows", "linux"]):
        keywords.append("linux") # Default to Linux for cloud environments

    print(f"\n⚙️  Configuring project for: {', '.join(keywords)}...")

    # --- STEP 2: CREATE DIRECTORY STRUCTURE ---
    # We create folders with .gitkeep so they persist
    dirs_to_create = [
        os.path.join(base_dir, "src"),
        os.path.join(base_dir, "tests"),
        os.path.join(base_dir, "docs"),
        os.path.join(base_dir, "scripts"),
        os.path.join(base_dir, "context", "raw"),         # For dumping raw user notes
        os.path.join(base_dir, ".idx"),                   # Google IDX
        os.path.join(base_dir, ".devcontainer"),          # Universal Container
        os.path.join(base_dir, ".agent", "rules"),        # Agent Brain
        os.path.join(base_dir, ".agent", "workflows"),    # Agent Hands
        os.path.join(base_dir, ".agent", "skills", "git_automation"),
        os.path.join(base_dir, ".agent", "skills", "secrets_manager"),
        os.path.join(base_dir, ".agent", "skills", "database_manager"),
        os.path.join(base_dir, ".agent", "memory"),       # Agent Memory
    ]

    print("\n📂 Building Directory Tree...")
    for d in dirs_to_create:
        create_folder(d)

    # --- STEP 3: GENERATE CONFIGURATION FILES ---
    
    # 1. Version Control & Environment
    write_file(os.path.join(base_dir, ".gitignore"), build_gitignore_content(keywords))
    write_file(os.path.join(base_dir, ".idx", "dev.nix"), build_nix_config(keywords))
    
    # 2. Universal DevContainer (VS Code / Codespaces compatibility)
    write_file(os.path.join(base_dir, ".devcontainer", "devcontainer.json"), """
{
  "name": "Antigravity Universal",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "customizations": {
    "vscode": {
      "extensions": ["google.gemini-code-assist"]
    }
  }
}
""")

    # 3. Project Root Files
    write_file(os.path.join(base_dir, "README.md"), f"# {project_name}\n\nGenerated by Antigravity Master Setup.\n\n## Tech Stack\n{', '.join(keywords)}")
    write_file(os.path.join(base_dir, ".env.example"), "# Define your secrets here\nAPI_KEY=\nDATABASE_URL=")
    write_file(os.path.join(base_dir, "docs", "architecture.md"), "# Architecture\n\n[Describe high level design here]")

    # --- STEP 4: GENERATE AGENT BRAIN (The Rules) ---
    
    write_file(os.path.join(base_dir, ".agent", "rules", "00_identity.md"), """
# System Identity & Persona
You are a **Principal Software Engineer** and **Product Architect**.
- **Tone:** Professional, Concise, Helpful.
- **Safety:** You never delete data without confirmation. You never commit secrets.
- **Goal:** Production-ready code, not just prototypes.
""")

    write_file(os.path.join(base_dir, ".agent", "rules", "01_tech_stack.md"), build_tech_stack_rule(keywords))

    write_file(os.path.join(base_dir, ".agent", "rules", "02_security.md"), """
# Security Protocols (OWASP)
1. **Secrets:** Never output API keys or passwords in chat. Use `.env`.
2. **Injection:** Sanitize all SQL/Shell inputs.
3. **Dependencies:** Warn the user if a package is known to be insecure.
""")

    write_file(os.path.join(base_dir, ".agent", "rules", "03_git_conventions.md"), """
# Git Conventions
- Use **Conventional Commits**:
  - `feat: ...`
  - `fix: ...`
  - `docs: ...`
  - `refactor: ...`
- Never commit broken code to the main branch.
""")

    write_file(os.path.join(base_dir, ".agent", "rules", "04_reasoning.md"), """
# Chain of Thought (Reasoning)
1. **Pause:** Before writing code, analyze the request.
2. **Plan:** If complex, list steps in markdown.
3. **Execute:** Write the code.
4. **Verify:** Explain how you would test this change.
""")

    # --- STEP 5: GENERATE AGENT HANDS (Workflows) ---

    write_file(os.path.join(base_dir, ".agent", "workflows", "plan.md"), """
---
description: Create a roadmap for a feature.
trigger: /plan
---
# Planning Workflow
1. Read `docs/architecture.md` and `context/raw/`.
2. Break request into atomic steps.
3. Update `.agent/memory/scratchpad.md` with the new plan.
4. Ask for approval.
""")

    write_file(os.path.join(base_dir, ".agent", "workflows", "bootstrap.md"), """
---
description: Scaffolds the initial code structure.
trigger: /bootstrap
---
# Bootstrap Workflow
1. Read `.agent/rules/01_tech_stack.md`.
2. Generate boilerplate code (main entry point, config files).
3. Create a basic test file.
4. Log completion to scratchpad.
""")

    write_file(os.path.join(base_dir, ".agent", "workflows", "review.md"), """
---
description: Review code for security and style.
trigger: /review
---
# Code Review
1. Check against `02_security.md`.
2. Check against `03_git_conventions.md`.
3. List issues by severity: [Critical, Major, Minor].
""")

    write_file(os.path.join(base_dir, ".agent", "workflows", "commit.md"), """
---
description: Stage and commit changes safely.
trigger: /commit
---
# Smart Commit
1. Run `git status` via `git_automation` skill.
2. Generate a Conventional Commit message based on the diff.
3. Ask user: "Ready to commit with message: <msg>?"
""")

    write_file(os.path.join(base_dir, ".agent", "workflows", "save_memory.md"), """
---
description: Save current progress to memory.
trigger: /save
---
# Save State
1. Summarize what was just done.
2. Update `.agent/memory/scratchpad.md`.
""")

    # --- STEP 6: GENERATE AGENT TOOLS (Skills) ---

    write_file(os.path.join(base_dir, ".agent", "skills", "git_automation", "SKILL.md"), """
---
name: git_automation
description: Handle git operations.
---
# Git Skill
**Commands:** `git status`, `git diff`, `git add`, `git commit`.
**Rule:** Always check status before adding.
""")

    write_file(os.path.join(base_dir, ".agent", "skills", "secrets_manager", "SKILL.md"), """
---
name: secrets_manager
description: Manage API keys safely.
---
# Secrets Skill
**Instruction:** If user provides a key, do NOT write it to code. Write it to `.env` (adding to .gitignore if needed).
""")

    # --- STEP 7: MEMORY & BOOTSTRAP ---

    write_file(os.path.join(base_dir, ".agent", "memory", "scratchpad.md"), f"""
# Project Scratchpad
*Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*

## Status
- Project Initialized with keywords: {', '.join(keywords)}
- Directory structure built.

## Next Steps
- [ ] Run `/bootstrap` to generate code skeleton.
- [ ] Fill out `docs/architecture.md`.
""")

    write_file(os.path.join(base_dir, "BOOTSTRAP_INSTRUCTIONS.md"), """
# Agent Start Guide

**Welcome, Agent.**
This project is configured for Antigravity.

**Immediate Actions:**
1. Read `.agent/rules/01_tech_stack.md`.
2. Read `.agent/memory/scratchpad.md`.
3. Check `context/raw/` for any user notes.
4. Execute the `/bootstrap` workflow to create the "Hello World" application for this stack.
""")

    print("\n✅ Setup Complete!")
    print(f"👉 To start: cd {project_name}")
    print("👉 Then: Open in Antigravity/IDX and type 'Read BOOTSTRAP_INSTRUCTIONS.md'")

if __name__ == "__main__":
    setup_project()
