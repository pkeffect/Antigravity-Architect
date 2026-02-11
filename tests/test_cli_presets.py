import json
import shutil
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add project root to sys.path to allow importing antigravity_master_setup
sys.path.append(str(Path(__file__).parent.parent))

from antigravity_master_setup import (
    AntigravityResources,
    list_presets,
    load_preset,
    main,
    save_preset,
)

# Setup a temporary presets directory for testing
TEST_PRESETS_DIR = Path("tests/temp_presets")

@pytest.fixture(autouse=True)
def setup_teardown_presets():
    """Fixture to setup and teardown test presets directory."""
    # Override the PRESETS_DIR constant for testing
    original_presets_dir = AntigravityResources.PRESETS_DIR
    AntigravityResources.PRESETS_DIR = TEST_PRESETS_DIR

    if TEST_PRESETS_DIR.exists():
        shutil.rmtree(TEST_PRESETS_DIR)
    TEST_PRESETS_DIR.mkdir(parents=True, exist_ok=True)

    yield

    # Cleanup
    if TEST_PRESETS_DIR.exists():
        shutil.rmtree(TEST_PRESETS_DIR)
    AntigravityResources.PRESETS_DIR = original_presets_dir

def test_save_preset():
    """Test saving a preset."""
    args = {"name": "test-project", "stack": "python,react"}
    assert save_preset("test_save", args) is True

    preset_path = TEST_PRESETS_DIR / "test_save.json"
    assert preset_path.exists()

    with open(preset_path) as f:
        data = json.load(f)
    assert data == args

def test_load_preset():
    """Test loading a preset."""
    preset_path = TEST_PRESETS_DIR / "test_load.json"
    data = {"name": "loaded-project", "license": "mit"}

    with open(preset_path, "w") as f:
        json.dump(data, f)

    loaded = load_preset("test_load")
    assert loaded == data

def test_load_nonexistent_preset():
    """Test loading a missing preset."""
    assert load_preset("nonexistent") is None

def test_list_presets():
    """Test listing presets."""
    (TEST_PRESETS_DIR / "alpha.json").touch()
    (TEST_PRESETS_DIR / "beta.json").touch()
    (TEST_PRESETS_DIR / "not_a_preset.txt").touch()

    presets = list_presets()
    assert "alpha" in presets
    assert "beta" in presets
    assert "not_a_preset" not in presets
    assert len(presets) == 2

@patch("antigravity_master_setup.run_cli_mode")
def test_main_save_preset(mock_run):
    """Test that main() saves a preset when --save-preset is passed."""
    # Simulate: python antigravity_master_setup.py --name p1 --stack python --save-preset my-preset --dry-run
    # We use dry-run to avoid actual execution if run_cli_mode triggers logic
    argv = ["--name", "p1", "--stack", "python", "--save-preset", "my-preset", "--dry-run"]

    main(argv)

    expected_path = TEST_PRESETS_DIR / "my-preset.json"
    assert expected_path.exists()

    with open(expected_path) as f:
        content = json.load(f)

    assert content["name"] == "p1"
    assert content["stack"] == "python"
    # Ensure operational flags are filtered
    assert "save_preset" not in content
    assert "dry_run" not in content

@patch("antigravity_master_setup.run_cli_mode")
def test_main_load_preset(mock_run):
    """Test that main() loads a preset and uses its values."""
    # Create a preset first
    preset_data = {"stack": "rust", "license": "apache"}
    with open(TEST_PRESETS_DIR / "my-rust.json", "w") as f:
        json.dump(preset_data, f)

    # Run with preset but override name
    # python antigravity_master_setup.py --preset my-rust --name rust-project
    argv = ["--preset", "my-rust", "--name", "rust-project"]

    main(argv)

    # Check that run_cli_mode was called with merged args
    args = mock_run.call_args[0][0]
    assert args.name == "rust-project"
    assert args.stack == "rust"     # From preset
    assert args.license == "apache" # From preset
