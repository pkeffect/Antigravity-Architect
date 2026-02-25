"""
Antigravity Architect - VS Code Sidecar Plugin
Provides configuration generation for Visual Studio Code (.vscode and .devcontainer).
"""

import os
from typing import Any

PLUGIN_DESCRIPTION = "Provides Visual Studio Code and DevContainer configurations."

# Constants moved from AntigravityResources
VSCODE_DIR = ".vscode"
DEVCONTAINER_DIR = ".devcontainer"
DEVCONTAINER_FILE = "devcontainer.json"

EXT_ESLINT = "dbaeumer.vscode-eslint"
EXT_PRETTIER = "esbenp.prettier-vscode"

DEVCONTAINER_JSON = """{
  "name": "Antigravity Universal",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": { "ghcr.io/devcontainers/features/common-utils:2": {} }
}
"""

VSCODE_EXTENSIONS_MAP: dict[str, list[str]] = {
    "python": ["ms-python.python", "ms-python.vscode-pylance", "charliermarsh.ruff"],
    "node": [EXT_ESLINT, EXT_PRETTIER],
    "javascript": [EXT_ESLINT, EXT_PRETTIER],
    "typescript": [EXT_ESLINT, EXT_PRETTIER],
    "docker": ["ms-azuretools.vscode-docker"],
    "react": ["dsznajder.es7-react-js-snippets"],
    "general": [
        "donjayamanne.githistory",
        "eamodio.gitlens",
        "usernamehw.errorlens",
        "pkief.material-icon-theme",
        "christian-kohler.path-intellisense",
    ],
}

VSCODE_SETTINGS_TEMPLATE = """{{
    "files.exclude": {{
        "**/.git": true,
        "**/.svn": true,
        "**/.hg": true,
        "**/CVS": true,
        "**/.DS_Store": true,
        "**/Thumbs.db": true,
        ".agent/**": false,
        "context/**": false
    }},
    "files.watcherExclude": {{
        "**/.git/objects/**": true,
        "**/.git/subtree-cache/**": true,
        "**/node_modules/*/**": true,
        "**/.venv/**": true,
        "**/.agent/**": true
    }},
    "search.exclude": {{
        "**/node_modules": true,
        "**/bower_components": true,
        "**/.venv": true,
        "**/.agent": true
    }},
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "{default_formatter}",
    "editor.bracketPairColorization.enabled": true,
    "editor.guides.bracketPairs": "active",
    "files.trimTrailingWhitespace": true,
    "editor.rulers": [
        80,
        120
    ],
    "[python]": {{
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.codeActionsOnSave": {{
            "source.organizeImports": "explicit"
        }}
    }},
    "editor.semanticHighlighting.enabled": true,
    "editor.inlineSuggest.enabled": true,
    "terminal.integrated.fontSize": 14,
    "workbench.colorCustomizations": {{
        "statusBar.background": "#1e1e1e",
        "statusBar.foreground": "#ffffff"
    }}
}}"""

VSCODE_SNIPPETS_TEMPLATE = """{{
    "Antigravity Agent Commands": {{
        "prefix": "/",
        "body": [
            "/{1|plan,sync,save,review,commit,doctor,help|}"
        ],
        "description": "Quick access to Antigravity Agent commands"
    }}
}}"""

VSCODE_LAUNCH_TEMPLATE = """{{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    "version": "0.2.0",
    "configurations": [
{configurations}
    ]
}}"""

VSCODE_TASKS_TEMPLATE = """{{
    "version": "2.0.0",
    "tasks": [
{tasks}
    ]
}}"""


def build_vscode_config(keywords: list[str]) -> dict[str, str]:
    """Builds all .vscode/ configuration files."""
    files: dict[str, str] = {}

    # 1. extensions.json
    extensions: list[str] = []

    extensions.extend(VSCODE_EXTENSIONS_MAP["general"])
    for k in keywords:
        key = k.lower()
        if key in VSCODE_EXTENSIONS_MAP:
            extensions.extend(VSCODE_EXTENSIONS_MAP[key])

    ext_str = ",\n        ".join(f'"{ext}"' for ext in sorted(set(extensions)))
    files["extensions.json"] = f"""{{
    "recommendations": [
        {ext_str}
    ]
}}"""

    # 2. settings.json (Dynamic default formatter)
    default_formatter = "esbenp.prettier-vscode"
    if "python" in keywords and "node" not in keywords and "javascript" not in keywords:
        default_formatter = "charliermarsh.ruff"

    files["settings.json"] = VSCODE_SETTINGS_TEMPLATE.format(default_formatter=default_formatter)

    # 3. launch.json
    files["launch.json"] = VSCODE_LAUNCH_TEMPLATE.format(configurations="")

    # 4. tasks.json
    files["tasks.json"] = VSCODE_TASKS_TEMPLATE.format(tasks="")

    # 5. antigravity.code-snippets
    files["antigravity.code-snippets"] = VSCODE_SNIPPETS_TEMPLATE

    return files


def on_generation_complete(**kwargs: Any) -> None:
    """
    Plugin Hook: Called after core files are generated.
    """
    base_dir = kwargs.get("base_dir")
    final_stack = kwargs.get("final_stack", [])
    safe_mode = kwargs.get("safe_mode", False)

    if not base_dir:
        return

    # Create VSCode Dir
    vscode_path = os.path.join(base_dir, VSCODE_DIR)
    os.makedirs(vscode_path, exist_ok=True)

    # 1. Generate VSCode Config Files
    vscode_files = build_vscode_config(final_stack)
    for filename, content in vscode_files.items():
        filepath = os.path.join(vscode_path, filename)
        if safe_mode and os.path.exists(filepath):
            continue
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
        except OSError:
            pass

    # 2. Generate Devcontainer File
    devcontainer_path = os.path.join(base_dir, DEVCONTAINER_DIR)
    os.makedirs(devcontainer_path, exist_ok=True)
    devcontainer_file_path = os.path.join(devcontainer_path, DEVCONTAINER_FILE)

    if not (safe_mode and os.path.exists(devcontainer_file_path)):
        try:
            with open(devcontainer_file_path, "w", encoding="utf-8") as f:
                f.write(DEVCONTAINER_JSON)
        except OSError:
            pass
