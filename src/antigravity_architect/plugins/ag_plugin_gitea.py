"""
Gitea Plugin for Antigravity Architect.

Provides templates and configuration for Gitea Actions CI/CD workflows.
"""
import logging
from pathlib import Path
from typing import Any

from antigravity_architect.core.engine import AntigravityEngine

PLUGIN_DESCRIPTION = "Gitea CI Templates integration"
GITEA_DIR = ".gitea"

GITEA_CI_TEMPLATE = """name: Gitea Action CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - name: Run Build
        run: echo "Building..."
"""

def on_generation_complete(
    project_name: str, base_dir: str, final_stack: list[str], safe_mode: bool, **kwargs: Any  # noqa: ARG001
) -> None:
    """Generates Gitea-specific templates and workflows if requested."""
    if "gitea" not in final_stack:
        return

    logging.debug(f"Gitea Plugin: Generating configuration for {project_name}")

    gitea_dir = Path(base_dir) / GITEA_DIR
    workflow_dir = gitea_dir / "workflows"

    # Create directories
    AntigravityEngine.create_folder(str(workflow_dir))

    templates = {
        workflow_dir / "ci.yml": GITEA_CI_TEMPLATE,
    }

    for path, content in templates.items():
        AntigravityEngine.write_file(str(path), content, exist_ok=safe_mode)
