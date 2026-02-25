import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest

from antigravity_architect.plugins.manager import PluginManager


@pytest.fixture
def temp_project_dir():
    """Create a temporary directory for project generation."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)


class TestPlugins:
    def test_plugin_discovery_and_execution(self, temp_project_dir):
        """Test that the plugin manager can discover and execute plugins."""
        PluginManager.load_plugins()
        
        # Test IDX plugin
        PluginManager.trigger(
            "on_generation_complete", 
            project_name="test_project", 
            base_dir=temp_project_dir, 
            final_stack=["idx"], 
            safe_mode=False
        )
        assert os.path.exists(os.path.join(temp_project_dir, ".idx", "dev.nix"))

        # Test VS Code plugin
        PluginManager.trigger(
            "on_generation_complete", 
            project_name="test_project", 
            base_dir=temp_project_dir, 
            final_stack=["vscode"], 
            safe_mode=False
        )
        assert os.path.exists(os.path.join(temp_project_dir, ".vscode", "extensions.json"))
        assert os.path.exists(os.path.join(temp_project_dir, ".devcontainer", "devcontainer.json"))

        # Test GitHub Plugin
        PluginManager.trigger(
            "on_generation_complete", 
            project_name="test_project", 
            base_dir=temp_project_dir, 
            final_stack=["github"], 
            safe_mode=False
        )
        assert os.path.exists(os.path.join(temp_project_dir, ".github", "workflows", "ci.yml"))
        assert os.path.exists(os.path.join(temp_project_dir, ".github", "ISSUE_TEMPLATE", "bug_report.md"))

        # Test Gitea Plugin
        PluginManager.trigger(
            "on_generation_complete", 
            project_name="test_project", 
            base_dir=temp_project_dir, 
            final_stack=["gitea"], 
            safe_mode=False
        )
        assert os.path.exists(os.path.join(temp_project_dir, ".gitea", "workflows", "ci.yml"))

    def test_plugin_graceful_missing_dependencies(self, temp_project_dir):
        """Test that plugins do not execute if their prerequisites (keywords) aren't met."""
        PluginManager.load_plugins()
        
        # Calling with an empty final stack
        PluginManager.trigger(
            "on_generation_complete", 
            project_name="test_project", 
            base_dir=temp_project_dir, 
            final_stack=["python"], 
            safe_mode=False
        )
        
        # Global plugins (IDX, VS Code, GitHub) should generate unconditionally
        assert os.path.exists(os.path.join(temp_project_dir, ".idx"))
        assert os.path.exists(os.path.join(temp_project_dir, ".vscode"))
        assert os.path.exists(os.path.join(temp_project_dir, ".github"))
        
        # Conditional plugins (Gitea) should NOT execute when missing keywords
        assert not os.path.exists(os.path.join(temp_project_dir, ".gitea"))
