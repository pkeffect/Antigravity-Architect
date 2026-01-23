# 🏗️ Antigravity Architect (Master Edition)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Platform](https://img.shields.io/badge/Platform-Google%20Antigravity%20%7C%20IDX%20%7C%20VS%20Code-orange) ![Agent-First](https://img.shields.io/badge/Architecture-Agent--First-purple) ![Context-Aware](https://img.shields.io/badge/AI-Context%20Assimilator-green)

**Antigravity Architect** is the ultimate "Agent-First" bootstrapping tool for modern AI development environments. It is designed for **Google Antigravity**, **Project IDX**, **Gemini Code Assist**, and **VS Code**.

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

### 🛡️ Production Engineering
*   **The "Git Ghost":** Automatically places `.gitkeep` files in empty directories so folder structures persist in Git.
*   **Cloud-Ready:** Generates `.idx/dev.nix` (for Google IDX) and `.devcontainer/devcontainer.json` (for GitHub Codespaces/VS Code).
*   **Safety First:** Includes input sanitization, error logging, and non-destructive overwrite protection.

---

## 🚀 Usage

### 1. Run the Script
No external dependencies required. Just run it with Python 3.

```bash
python antigravity_master_setup.py
```

### 2. Follow the Prompt
The script will ask for an optional "Brain Dump" file, or you can manually input your stack.

```text
[Optional] Drag & Drop a Brain Dump file (Specs/Notes/Code):
Path: /Users/me/docs/project_specs.txt

Project Name: my-super-app
```

### 3. Initialize the Agent
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
│   │   ├── 04_reasoning.md  # Chain-of-Thought enforcer
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

## 📜 License
This script is open-source. Feel free to modify the `00_identity.md` rule to change your Agent's personality!
