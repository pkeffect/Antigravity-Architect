import shutil
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


import antigravity_master_setup


class TestCliCore:
    """Tests for core CLI functionality and edge cases."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)

    def test_load_custom_templates_errors(self, temp_dir):
        """Test error handling in load_custom_templates (lines 2163-2178)."""
        # Case 1: Template directory does not exist
        missing_dir = temp_dir / "missing_templates"
        overrides = antigravity_master_setup.load_custom_templates(str(missing_dir))
        assert overrides == {}

        # Case 2: Template directory exists but empty categories
        templates_dir = temp_dir / "templates"
        templates_dir.mkdir()
        (templates_dir / "rules").mkdir()

        overrides = antigravity_master_setup.load_custom_templates(str(templates_dir))
        assert overrides == {"rules": {}, "workflows": {}, "skills": {}}

        # Case 3: Valid template loading
        rules_dir = templates_dir / "rules"
        (rules_dir / "test_rule.md").write_text("content", encoding="utf-8")

        overrides = antigravity_master_setup.load_custom_templates(str(templates_dir))
        assert "test_rule.md" in overrides["rules"]
        assert overrides["rules"]["test_rule.md"] == "content"

    def test_doctor_check_dir_exists(self, temp_dir):
        """Test _doctor_check_dir when directory exists (lines 2184-2185)."""
        test_dir = temp_dir / "test_subdir"
        test_dir.mkdir()

        passed, issue, fixed = antigravity_master_setup._doctor_check_dir(temp_dir, "test_subdir", fix=False)
        assert passed is not None
        assert "exists" in passed
        assert issue is None
        assert fixed is None

    def test_doctor_project_missing_dir(self):
        """Test doctor_project with non-existent path (lines 2345-2347)."""
        assert antigravity_master_setup.doctor_project("/non/existent/path") is False

    @patch('antigravity_master_setup.doctor_project')
    def test_main_doctor_args(self, mock_doctor):
        """Test main function with doctor arguments."""
        test_args = ["--doctor", ".", "--fix"]
        with patch.object(sys, 'argv', ["script.py"] + test_args):
             antigravity_master_setup.main(test_args)
             mock_doctor.assert_called_once_with(".", fix=True)

    @patch('antigravity_master_setup.list_keywords')
    def test_main_list_keywords(self, mock_list):
        """Test main function with list-keywords argument."""
        test_args = ["--list-keywords"]
        with patch.object(sys, 'argv', ["script.py"] + test_args):
             antigravity_master_setup.main(test_args)
             mock_list.assert_called_once()

    @patch('antigravity_master_setup.list_blueprints')
    def test_main_list_blueprints(self, mock_list):
        """Test main function with list-blueprints argument."""
        test_args = ["--list-blueprints"]
        with patch.object(sys, 'argv', ["script.py"] + test_args):
             antigravity_master_setup.main(test_args)
             mock_list.assert_called_once()

    @patch('antigravity_master_setup.input', side_effect=["y", "my-project", "python,react", "mit"])
    @patch('antigravity_master_setup.generate_project')
    def test_run_interactive_mode(self, mock_generate, mock_input):
        """Test interactive mode (lines 2427-2458)."""
        antigravity_master_setup.run_interactive_mode()
        mock_generate.assert_called_once()

    def test_safe_mode_handling(self, temp_dir):
        """Test safe mode handling (lines 2020-2023)."""
        project_dir = temp_dir / "existing_project"
        project_dir.mkdir()
        (project_dir / "README.md").write_text("existing", encoding="utf-8")

        # Test abort on safe mode conflict
        with patch('antigravity_master_setup.input', return_value="n"):
            result = antigravity_master_setup.AntigravityGenerator._handle_safe_mode("existing_project", str(project_dir), safe_mode=None)
            assert result is None

    def test_brain_dump_process(self, temp_dir):
        """Test brain dump processing (lines 2044-2046)."""
        dump_file = temp_dir / "specs.md"
        dump_file.write_text("Use python and react.", encoding="utf-8")

        project_dir = temp_dir / "project"
        project_dir.mkdir()

        stack = antigravity_master_setup.process_brain_dump(str(dump_file), str(project_dir))
        assert "python" in stack
        assert "react" in stack

    def test_git_init_capture(self, temp_dir):
        """Test git hook setup (lines 2078)."""
        project_dir = temp_dir / "git_project"
        project_dir.mkdir()
        git_dir = project_dir / ".git"
        git_dir.mkdir()
        (git_dir / "hooks").mkdir()

        antigravity_master_setup.AntigravityGenerator._setup_git_hooks(str(project_dir))

        hook_path = git_dir / "hooks" / "post-commit"
        assert hook_path.exists()
        assert "Antigravity" in hook_path.read_text(encoding="utf-8")

    def test_main_preset_loading(self):
        """Test loading presets in main (lines 2630-2636)."""
        with patch('antigravity_master_setup.load_preset', return_value={"name": "test"}):
            test_args = ["--preset", "test"]
            with patch.object(sys, 'argv', ["script.py"] + test_args):
                with patch('antigravity_master_setup.run_cli_mode') as mock_run:
                    antigravity_master_setup.main(test_args)
                    mock_run.assert_called()

    def test_gitea_dry_run(self):
        """Test dry run with Gitea stack (lines 2532-2533, 2557-2564)."""
        with patch('builtins.print') as mock_print:
            # Test _print_dry_run_agent with gitea
            antigravity_master_setup._print_dry_run_agent(["gitea", "python"])
            # Verify gitea workflow print
            assert any("gitea/workflows/ci.yml" in str(c) for c in mock_print.call_args_list)
            
            mock_print.reset_mock()
            
            # Test _print_dry_run_templates with gitea
            antigravity_master_setup._print_dry_run_templates(["gitea", "python"])
            # Verify gitea templates print
            assert any("issue_template/bug_report.md" in str(c) for c in mock_print.call_args_list)

    def test_brain_dump_integration(self, temp_dir):
        """Test brain dump integration in generate_project (lines 2045)."""
        dump_path = temp_dir / "dump.md"
        dump_path.write_text("Use rust.", encoding="utf-8")
        
        # We mock internal methods to avoid full generation but verify the stack update
        with patch('antigravity_master_setup.process_brain_dump', return_value=["rust"]) as mock_bd:
            with patch('antigravity_master_setup.AntigravityGenerator._generate_core_config_files') as mock_core:
                with patch('antigravity_master_setup.AntigravityGenerator.generate_agent_files'):
                    # Mock other calls to minimal no-ops
                    with patch('antigravity_master_setup.setup_logging'):
                        with patch('antigravity_master_setup.create_folder'):
                             antigravity_master_setup.generate_project("bd_project", [], str(dump_path))
                             
                             mock_bd.assert_called_once()
                             # Verify rust made it into the stack passed to core generation
                             call_args = mock_core.call_args
                             assert "rust" in call_args[0][2]  # final_stack is the 3rd arg

    def test_main_list_presets_flag(self):
        """Test main function with list-presets argument (lines 2624-2628)."""
        with patch('antigravity_master_setup.list_presets', return_value=["p1", "p2"]) as mock_list:
            test_args = ["--list-presets"]
            with patch.object(sys, 'argv', ["script.py"] + test_args):
                 antigravity_master_setup.main(test_args)
                 mock_list.assert_called_once()

    def test_generate_project_fallback(self):
        """Test fallback to 'linux' when no keywords provided (lines 2049-2050)."""
        with patch('antigravity_master_setup.AntigravityGenerator._generate_core_config_files') as mock_core:
             with patch('antigravity_master_setup.AntigravityGenerator.generate_agent_files'):
                with patch('antigravity_master_setup.setup_logging'):
                    with patch('antigravity_master_setup.create_folder'):
                        # Pass empty keywords, no brain dump
                        antigravity_master_setup.generate_project("fallback_project", [])
                        
                        # Verify 'linux' was added
                        call_args = mock_core.call_args
                        assert "linux" in call_args[0][2]
