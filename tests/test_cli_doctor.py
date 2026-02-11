"""
Tests for CLI and Doctor mode to increase coverage to 80%+.
"""

import logging
import os
from collections.abc import Generator
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

import antigravity_master_setup as ag


@pytest.fixture(autouse=True)
def cleanup_logging() -> Generator[None, None, None]:
    """Ensure logging handlers are closed after each test to prevent file locking."""
    yield
    logging.shutdown()
    for handler in logging.getLogger().handlers[:]:
        handler.close()
        logging.getLogger().removeHandler(handler)

@pytest.fixture
def temp_workspace():
    """Create a temporary workspace for doctor tests."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            # Global mock for setup_logging to avoid WinError 32
            with patch("antigravity_master_setup.setup_logging"):
                yield Path(tmpdir)
        finally:
            os.chdir(original_cwd)

class TestDoctorModeExtended:
    """Extended tests for doctor_project functionality."""

    def test_doctor_fix_missing_dirs(self, temp_workspace):
        """Should create missing directories when fix=True."""
        project_name = "fix-me"
        project_path = temp_workspace / project_name
        os.makedirs(project_path)

        # Run doctor without fix - should fail
        assert ag.doctor_project(str(project_path), fix=False) is False

        # Run doctor with fix
        assert ag.doctor_project(str(project_path), fix=True) is True

        # Verify directories created
        assert (project_path / ".agent" / "rules").exists()
        assert (project_path / ".agent" / "memory").exists()

    def test_doctor_fix_missing_files(self, temp_workspace):
        """Should regenerate missing required files when fix=True."""
        project_name = "fix-files"
        project_path = temp_workspace / project_name
        ag.generate_project(project_name, ["python"])

        # Delete a required file
        identity_path = project_path / ".agent" / "rules" / "00_identity.md"
        os.remove(identity_path)

        assert ag.doctor_project(str(project_path), fix=True) is True
        assert identity_path.exists()

    def test_doctor_reports_warnings_and_issues(self, temp_workspace):
        """Should report warnings for empty files and issues for missing ones."""
        project_name = "report-me"
        project_path = temp_workspace / project_name
        os.makedirs(project_path / ".agent" / "rules", exist_ok=True)
        os.makedirs(project_path / ".agent" / "memory", exist_ok=True)
        os.makedirs(project_path / ".agent" / "workflows", exist_ok=True)
        os.makedirs(project_path / ".agent" / "skills", exist_ok=True)

        # Create empty identity file (warning)
        identity_path = project_path / ".agent" / "rules" / "00_identity.md"
        identity_path.touch()

        with patch("builtins.print") as mock_print:
            ag.doctor_project(str(project_path), fix=False)

            # Check for summary output
            print_calls = [call.args[0] for call in mock_print.call_args_list if call.args]
            summary = [s for s in print_calls if "Summary:" in s]
            assert len(summary) > 0
            assert "warnings" in summary[0]
            assert "issues" in summary[0]

class TestCLIModeExtended:
    """Extended tests for CLI execution and main entry point."""

    def test_main_cli_generation(self, temp_workspace):
        """Should run full generation via CLI arguments."""
        project_name = "cli-project"
        with patch("sys.exit"), patch("antigravity_master_setup.setup_logging"):
            ag.main(["--name", project_name, "--stack", "python", "--license", "mit"])
            assert (temp_workspace / project_name / "README.md").exists()
            assert (temp_workspace / project_name / ".agent" / "manifest.json").exists()

    def test_main_interactive_fallback(self):
        """Should fall back to interactive mode when no args provided."""
        with patch("antigravity_master_setup.run_interactive_mode") as mock_interactive:
            ag.main([])
            mock_interactive.assert_called_once()

    def test_run_cli_mode_dry_run(self, temp_workspace):
        """Should run dry run report via CLI."""
        project_name = "dry-run-project"
        args = MagicMock()
        args.name = project_name
        args.stack = "python,docker"
        args.brain_dump = None
        args.safe = False
        args.templates = None
        args.license = "mit"
        args.blueprint = None
        args.dry_run = True

        with patch("antigravity_master_setup.setup_logging"), patch("builtins.print") as mock_print:
            ag.run_cli_mode(args)
            print_calls = [call.args[0] for call in mock_print.call_args_list if call.args]
            assert any("DRY RUN MODE" in s for s in print_calls)
            # Verify no directory created
            assert not (temp_workspace / project_name).exists()

    def test_run_cli_mode_invalid_name(self):
        """Should handle cases where project name might be problematic."""
        # Since sanitize_name usually has a fallback, we test with a MagicMock
        # that returns empty to trigger the error path for coverage.
        args = MagicMock()
        args.name = "!!!@@@!!!"
        args.stack = "python"
        args.templates = None
        args.dry_run = False

        with patch("antigravity_master_setup.sanitize_name", return_value=""):
            with patch("builtins.print") as mock_print:
                ag.run_cli_mode(args)
                mock_print.assert_any_call("❌ Invalid project name.")

        # Also test with a valid name but ensure it proceeds (coverage)
        args.name = "valid-name"
        with patch("antigravity_master_setup.generate_project") as mock_gen:
            ag.run_cli_mode(args)
            mock_gen.assert_called()

    def test_main_list_keywords(self):
        """Verify list-keywords entry point in main."""
        with patch("antigravity_master_setup.list_keywords") as mock_list:
            ag.main(["--list-keywords"])
            mock_list.assert_called_once()

    def test_main_doctor_entry(self):
        """Verify doctor entry point in main."""
        with patch("antigravity_master_setup.doctor_project") as mock_doctor:
            ag.main(["--doctor", ".", "--fix"])
            mock_doctor.assert_called_once_with(".", fix=True)

class TestInteractiveMode:
    """Tests for the interactive input mode."""

    def test_run_interactive_mode_success(self, temp_workspace):
        """Should generate project based on interactive inputs."""
        inputs = [
            "",               # Brain dump path (empty)
            "inter-project",  # Project name
            "python,node",    # Tech stack
            "mit"             # License
        ]
        with patch("builtins.input", side_effect=inputs), patch("antigravity_master_setup.setup_logging"):
            with patch("builtins.print"):
                ag.run_interactive_mode()

        assert (temp_workspace / "inter-project" / "README.md").exists()
        assert (temp_workspace / "inter-project" / ".agent" / "manifest.json").exists()

    def test_run_interactive_mode_no_name(self):
        """Should exit if no project name provided in interactive mode."""
        inputs = ["", "", ""] # No brain dump, no name
        with patch("builtins.input", side_effect=inputs), patch("antigravity_master_setup.setup_logging"):
            with patch("builtins.print") as mock_print:
                ag.run_interactive_mode()
                mock_print.assert_any_call("❌ Project name is required.")
