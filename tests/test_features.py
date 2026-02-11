"""
Tests for advanced features: Sentinel, Evolution, Context Bridge, and Documentation Genie.
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

# Add parent directory to path so we can import the module
sys.path.insert(0, str(Path(__file__).parent.parent))

import antigravity_master_setup as ag


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


class TestAdvancedFeatures:
    """Tests for advanced features introduced in v1.6+."""

    def test_build_links_discovery(self, temp_dir):
        """Should discover sibling directories and create links.md."""
        # Create sibling directories with .git to be recognized
        os.makedirs(os.path.join(temp_dir, "sibling-1", ".git"))
        os.makedirs(os.path.join(temp_dir, "sibling-2", ".agent"))

        # Create current project dir
        project_dir = os.path.join(temp_dir, "current-project")
        os.makedirs(project_dir)

        # Original directory
        original_cwd = os.getcwd()
        try:
            # Run from temp_dir (the workspace) to discover current-project's siblings
            os.chdir(temp_dir)
            builder = ag.AntigravityBuilder()
            links_content = builder.build_links("current-project")

            assert "sibling-1" in links_content
            assert "sibling-2" in links_content
            assert "Git Repository" in links_content
            assert "Antigravity Project" in links_content
        finally:
            os.chdir(original_cwd)

    def test_tech_stack_deep_dive_generation(self):
        """Should generate accurate TECH_STACK.md content."""
        assimilator = ag.AntigravityAssimilator()
        keywords = ["python", "docker", "react"]
        raw_text = "This project uses FastAPI for the backend and React for the frontend."

        deep_dive = assimilator.build_tech_deep_dive(keywords, raw_text)

        assert "Python" in deep_dive
        assert "Docker" in deep_dive
        assert "React" in deep_dive
        assert "API" in deep_dive

    def test_doctor_validation_fail(self, temp_dir):
        """Should identify missing agent files and return False."""
        # Create a project dir but it's empty

        # Run doctor
        result = ag.doctor_project(temp_dir)

        # Should have found many missing files and returned False
        assert result is False

    def test_generate_agent_files_v162(self, temp_dir):
        """Should create Sentinel, Evolution, and Manifest files."""
        ag.generate_agent_files(temp_dir, "test-v162", ["python"])

        agent_dir = os.path.join(temp_dir, ".agent")
        rules_dir = os.path.join(agent_dir, "rules")
        workflows_dir = os.path.join(agent_dir, "workflows")
        memory_dir = os.path.join(agent_dir, "memory")
        scripts_dir = os.path.join(temp_dir, "scripts")

        # Check manifest
        assert os.path.exists(os.path.join(agent_dir, "manifest.json"))

        # Check new rules
        assert os.path.exists(os.path.join(rules_dir, "08_boundaries.md"))
        assert os.path.exists(os.path.join(rules_dir, "10_evolution.md"))

        # Check new workflows
        assert os.path.exists(os.path.join(workflows_dir, "evolve.md"))

        # Check new memory
        assert os.path.exists(os.path.join(memory_dir, "evolution.md"))

        # Check sentinel script
        assert os.path.exists(os.path.join(scripts_dir, "sentinel.py"))

    def test_detect_tech_stack_aliases(self):
        """Should detect technologies using aliases (e.g. sveltekit -> node)."""
        assimilator = ag.AntigravityAssimilator()
        text = "This is a sveltekit application with fastapi endpoint."

        keywords = assimilator.detect_tech_stack(text)

        assert "node" in keywords  # sveltekit -> node
        assert "python" in keywords  # fastapi -> python

    def test_list_keywords(self):
        """Should run list_keywords without error via main()."""
        with patch("builtins.print") as mock_print:
            ag.main(["--list-keywords"])
            assert mock_print.called

    def test_cli_doctor_integration(self, temp_dir):
        """Test CLI --doctor entry point."""
        with patch("antigravity_master_setup.doctor_project", return_value=True) as mock_doctor:
            with patch("builtins.print"):
                with patch("sys.exit"):
                    ag.main(["--doctor", temp_dir])
                    mock_doctor.assert_called_once()
                    args, kwargs = mock_doctor.call_args
                    assert args[0] == temp_dir
                    assert kwargs.get("fix") is False

    def test_detect_tech_stack_no_match(self):
        """Should return empty list for unknown tech."""
        assimilator = ag.AntigravityAssimilator()
        text = "This project uses alien-technology-x."
        keywords = assimilator.detect_tech_stack(text)
        assert len(keywords) == 0

    def test_build_tech_deep_dive_no_observations(self):
        """Should provide generic response when no tech patterns match."""
        assimilator = ag.AntigravityAssimilator()
        deep_dive = assimilator.build_tech_deep_dive([], "Just some text.")
        assert "Standard project structure" in deep_dive


if __name__ == "__main__":
    pytest.main([__file__])
