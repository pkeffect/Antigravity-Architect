"""
Google Project IDX Integration Plugin for Antigravity Architect
"""
import logging
import os
from typing import Any

from antigravity_architect.core.engine import AntigravityEngine

PLUGIN_DESCRIPTION = "Google Project IDX Integration (dev.nix)"

NIX_PACKAGE_MAP = {
    "python": ["pkgs.python312", "pkgs.python312Packages.pip", "pkgs.ruff", "pkgs.python312Packages.virtualenv"],
    "node": ["pkgs.nodejs_20", "pkgs.nodePackages.nodemon", "pkgs.nodePackages.typescript"],
    "docker": ["pkgs.docker", "pkgs.docker-compose"],
    "sql": ["pkgs.sqlite", "pkgs.postgresql"],
}

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

def on_generation_complete(**kwargs: Any) -> None:
    """Triggered after core project generation is complete."""
    base_dir = kwargs.get("base_dir")
    final_stack = kwargs.get("final_stack", [])
    safe_mode = kwargs.get("safe_mode", False)

    if not base_dir:
        return

    idx_dir = os.path.join(base_dir, ".idx")
    AntigravityEngine.create_folder(idx_dir)

    nix_path = os.path.join(idx_dir, "dev.nix")
    AntigravityEngine.write_file(nix_path, build_nix_config(final_stack), exist_ok=safe_mode)
    logging.info("  ↳ Generated Google Project IDX configuration (.idx/dev.nix)")
