import json
import shutil
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from antigravity_master_setup import (
    AntigravityEngine,
    AntigravityGenerator,
    AntigravityResources,
    list_blueprints,
)

# Setup a temporary blueprints directory for testing
TEST_TEMP_DIR = Path("tests/temp_blueprints")

@pytest.fixture(autouse=True)
def setup_teardown_blueprints():
    """Fixture to setup and teardown test directories."""
    if TEST_TEMP_DIR.exists():
        shutil.rmtree(TEST_TEMP_DIR)
    TEST_TEMP_DIR.mkdir(parents=True, exist_ok=True)

    yield

    # Cleanup
    if TEST_TEMP_DIR.exists():
        shutil.rmtree(TEST_TEMP_DIR)

def test_builtin_blueprints_exist():
    """Verify that new built-in blueprints are registered."""
    assert "nextjs" in AntigravityResources.BLUEPRINTS
    assert "fastapi" in AntigravityResources.BLUEPRINTS
    assert "go-fiber" in AntigravityResources.BLUEPRINTS
    assert "rust-axum" in AntigravityResources.BLUEPRINTS

def test_builtin_blueprints_structure():
    """Verify built-in blueprints have required keys."""
    for name, data in AntigravityResources.BLUEPRINTS.items():
        assert "stack" in data, f"Blueprint {name} missing 'stack'"
        assert "dirs" in data, f"Blueprint {name} missing 'dirs'"
        assert "rules" in data, f"Blueprint {name} missing 'rules'"
        assert isinstance(data["stack"], list)
        assert isinstance(data["dirs"], list)

@patch("subprocess.check_call")
@patch("tempfile.mkdtemp")
def test_fetch_remote_blueprint_success(mock_mkdtemp, mock_check_call):
    """Test successful remote blueprint fetch."""
    # Mock temp dir creation
    mock_mkdtemp.return_value = str(TEST_TEMP_DIR)

    # Create a fake blueprint file in the temp dir
    blueprint_data = {
        "name": "remote-test",
        "stack": ["python", "django"],
        "dirs": ["app"],
        "rules": []
    }

    (TEST_TEMP_DIR / "antigravity_blueprint.json").write_text(json.dumps(blueprint_data))

    # Call the function
    url = "https://github.com/test/repo.git"
    result = AntigravityEngine.fetch_remote_blueprint(url)

    # Verify git clone was called
    mock_check_call.assert_called_once()
    args = mock_check_call.call_args[0][0]
    assert args[:4] == ["git", "clone", "--depth", "1"]
    assert args[4] == url

    # Verify result
    assert result == blueprint_data

@patch("subprocess.check_call")
def test_fetch_remote_blueprint_failure(mock_check_call):
    """Test remote blueprint fetch failure (git error)."""
    mock_check_call.side_effect = subprocess.CalledProcessError(1, ["git", "clone"])

    result = AntigravityEngine.fetch_remote_blueprint("https://github.com/bad/repo.git")
    assert result is None

def test_list_blueprints(capsys):
    """Test list_blueprints output."""
    list_blueprints()
    captured = capsys.readouterr()
    assert "Available Blueprints" in captured.out
    assert "nextjs" in captured.out
    assert "fastapi" in captured.out
    assert "rust-axum" in captured.out

@patch("antigravity_master_setup.AntigravityGenerator._resolve_blueprint")
@patch("antigravity_master_setup.create_folder")
@patch("antigravity_master_setup.AntigravityGenerator._generate_vscode_config")
@patch("antigravity_master_setup.AntigravityGenerator._apply_blueprint_rules")
@patch("antigravity_master_setup.AntigravityGenerator.generate_agent_files")
@patch("antigravity_master_setup.AntigravityGenerator._generate_core_config_files")
@patch("antigravity_master_setup.AntigravityGenerator._generate_license")
@patch("antigravity_master_setup.AntigravityGenerator.generate_community_standards")
@patch("antigravity_master_setup.AntigravityGenerator.generate_github_templates")
@patch("antigravity_master_setup.AntigravityGenerator._setup_git_hooks")
@patch("antigravity_master_setup.AntigravityGenerator._handle_safe_mode")
@patch("antigravity_master_setup.setup_logging")
def test_generate_project_with_remote_blueprint(
    mock_logging, mock_safe, mock_hooks, mock_github, mock_community,
    mock_license, mock_core, mock_agent, mock_apply_rules, mock_vscode,
    mock_create_folder, mock_resolve
):
    """Test generate_project using a resolved blueprint."""
    # Setup mocks
    mock_safe.return_value = False
    mock_resolve.return_value = {
        "name": "remote-project",
        "stack": ["remote-stack"],
        "dirs": ["remote-dir"],
        "rules": []
    }

    # Run generation
    AntigravityGenerator.generate_project("test-project", keywords=["python"], blueprint="http://example.com/repo")

    # Verify resolution called
    mock_resolve.assert_called_with("http://example.com/repo")

    # Verify stack merging (mock_core receives final stack)
    # We can inspect the calls to see if 'remote-stack' made it into the keywords list logic
    # But since we mock everything, we just check flow.

    # Verify rules application called
    mock_apply_rules.assert_called_once()
