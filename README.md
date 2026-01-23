# 🏗️ Antigravity Architect (Master Setup)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Platform](https://img.shields.io/badge/Platform-Google%20Antigravity%20%7C%20IDX%20%7C%20VS%20Code-orange) ![Agent-First](https://img.shields.io/badge/Architecture-Agent--First-purple)

**Antigravity Architect** is a universal project bootstrapper designed specifically for AI-augmented development environments (Google Antigravity, Project IDX, Gemini Code Assist).

Unlike standard scaffolding tools (like `create-react-app`), this script does not just generate code; **it generates a brain for your AI Agent.** It constructs a "Self-Describing Repository" that teaches the AI how to behave, what rules to follow, and how to understand your specific project context.

---

## ✨ Key Features

*   **🌐 Universal & Dynamic:** Supports Python, Node.js, Rust, Go, Java, PHP, Ruby, and more. It adapts the `.gitignore` and Environment configs based on your input keywords.
*   **🧠 Agent Brain Generation:** Creates a robust `.agent` directory with **Rules** (Persona, Security), **Workflows** (Plans, Commits), and **Skills** (Tools).
*   **☁️ Cloud-Ready:** Automatically generates `.idx/dev.nix` (for Google IDX) and `.devcontainer/devcontainer.json` (for VS Code/GitHub Codespaces).
*   **👻 The "Git Ghost" Fix:** Automatically places `.gitkeep` files in empty directories (like `src/` or `tests/`) so they are tracked by Git immediately.
*   **💾 Memory System:** Initializes a `scratchpad.md` and a "Context Dump" folder, giving the AI long-term memory and a place to read raw notes.
*   **🛡️ Production Safety:** Includes sanitized project naming, error logging, and idempotent file generation.

---

## 🚀 Usage

### 1. Run the Script
No external dependencies required. Just run it with Python 3.

```bash
python antigravity_master_setup.py
```

### 2. Follow the Prompt
The script will perform a dynamic interview:

```text
1. Enter Project Name: my-new-saas
2. Tech Stack: python, react, postgres, macos
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
│   │   └── 04_reasoning.md  # Chain-of-Thought enforcer
│   ├── workflows/           # Callable Commands (/slash)
│   │   ├── plan.md          # /plan
│   │   ├── bootstrap.md     # /bootstrap
│   │   └── commit.md        # /commit
│   ├── skills/              # Tool definitions
│   └── memory/              # Active Session Memory
│       └── scratchpad.md    # The "Save Game" file
├── .idx/                    # ☁️ CLOUD ENV CONFIG
│   └── dev.nix              # NixOS package definitions
├── context/
│   └── raw/                 # 📥 DUMP ZONE (Paste PDFs, notes here)
├── src/                     # Source Code
├── docs/                    # Architecture Documentation
└── BOOTSTRAP_INSTRUCTIONS.md # The "Genie" Prompt
```

---

## 🛠 Supported Keywords

The script parses your input string for these keywords to dynamically build `.gitignore` and Cloud Environment packages.

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

### ⚡ Workflows (Slash Commands)
Type these in the Antigravity Chat:

| Command | Action |
| :--- | :--- |
| `/plan` | Reads `docs/` and `context/`, then generates a checklist in `scratchpad.md`. |
| `/bootstrap` | Scaffolds "Hello World" code based on the detected Tech Stack. |
| `/review` | audits the open file for security risks and style violations. |
| `/commit` | Analyzes `git diff` and proposes a formatted commit message. |
| `/save` | Summarizes recent work and updates the `scratchpad.md` memory file. |

---

## ☁️ Environment Details

### For Google Project IDX / Antigravity
The script generates `.idx/dev.nix`.
*   If you selected `python`, the environment boots with Python 3.12, Pip, and Ruff installed.
*   If you selected `node`, it boots with Node 20 and NPM.
*   **Result:** You do not need to manually install system tools.

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
*   **A:** The script automatically adds `.gitkeep` files to empty folders. If you deleted them, Git will ignore the empty folder.

---

## 📜 License
This script is open-source. Feel free to modify the `00_identity.md` rule to change your Agent's personality!
