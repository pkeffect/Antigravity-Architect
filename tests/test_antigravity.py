"""
Comprehensive test suite for Antigravity Architect.

Tests all core utility functions, content builders, and assimilation logic.
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

# Add parent directory to path so we can import the module
sys.path.insert(0, str(Path(__file__).parent.parent))

import logging

import antigravity_master_setup as ag  # noqa: E402

# ==============================================================================
# FIXTURES
# ==============================================================================


@pytest.fixture(autouse=True)
def cleanup_logging():
    """Ensure logging handlers are closed after each test to prevent file locking."""
    yield
    logging.shutdown()
    for handler in logging.getLogger().handlers[:]:
        handler.close()
        logging.getLogger().removeHandler(handler)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_brain_dump(temp_dir):
    """Create a sample brain dump file for testing."""
    content = """# Coding Standards

Always use type hints in Python code.
Never commit secrets to the repository.

# Deployment Workflow

## Step 1: Build
Run the build command.

## Step 2: Deploy
Deploy to production server.

# CLI Tool Usage

The command `antigravity --help` shows all flags and arguments.
Use the terminal to run automation scripts.

# Project Overview

This is an introduction to the architecture.
The background context explains the design decisions.
"""
    filepath = os.path.join(temp_dir, "brain_dump.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


# ==============================================================================
# TEST: sanitize_name()
# ==============================================================================


class TestSanitizeName:
    """Tests for the sanitize_name function."""

    def test_empty_input_returns_default(self):
        """Empty string should return default project name."""
        assert ag.sanitize_name("") == "antigravity-project"

    def test_none_input_returns_default(self):
        """None should return default project name."""
        assert ag.sanitize_name(None) == "antigravity-project"

    def test_strips_special_characters(self):
        """Special characters should be removed."""
        assert ag.sanitize_name("my@project!") == "myproject"
        assert ag.sanitize_name("test#$%name") == "testname"

    def test_converts_spaces_to_underscores(self):
        """Spaces should be converted to underscores."""
        assert ag.sanitize_name("my project") == "my_project"
        assert ag.sanitize_name("hello   world") == "hello_world"

    def test_preserves_hyphens(self):
        """Hyphens should be preserved."""
        assert ag.sanitize_name("my-project") == "my-project"

    def test_preserves_underscores(self):
        """Underscores should be preserved."""
        assert ag.sanitize_name("my_project") == "my_project"

    def test_path_traversal_stripped(self):
        """Path traversal characters are stripped, making input safe."""
        # The regex strips dots and slashes, leaving just the safe part
        assert ag.sanitize_name("../escape") == "escape"
        assert ag.sanitize_name("..\\escape") == "escape"

    def test_slashes_stripped(self):
        """Slashes are stripped from input."""
        # Slashes are removed by the regex sanitization
        assert ag.sanitize_name("/root/path") == "rootpath"
        assert ag.sanitize_name("\\windows\\path") == "windowspath"

    def test_strips_whitespace(self):
        """Leading/trailing whitespace should be stripped."""
        assert ag.sanitize_name("  myproject  ") == "myproject"


# ==============================================================================
# TEST: parse_keywords()
# ==============================================================================


class TestParseKeywords:
    """Tests for the parse_keywords function."""

    def test_empty_string_returns_empty_list(self):
        """Empty string should return empty list."""
        assert ag.parse_keywords("") == []

    def test_none_returns_empty_list(self):
        """None should return empty list."""
        assert ag.parse_keywords(None) == []

    def test_comma_separated(self):
        """Comma-separated keywords should be parsed."""
        result = ag.parse_keywords("python, react, docker")
        assert result == ["python", "react", "docker"]

    def test_space_separated(self):
        """Space-separated keywords should be parsed."""
        result = ag.parse_keywords("python react docker")
        assert result == ["python", "react", "docker"]

    def test_mixed_separators(self):
        """Mixed separators should be handled."""
        result = ag.parse_keywords("python, react docker,go")
        assert result == ["python", "react", "docker", "go"]

    def test_converts_to_lowercase(self):
        """Keywords should be converted to lowercase."""
        result = ag.parse_keywords("Python, REACT, Docker")
        assert result == ["python", "react", "docker"]

    def test_strips_whitespace(self):
        """Whitespace should be stripped from keywords."""
        result = ag.parse_keywords("  python  ,  react  ")
        assert result == ["python", "react"]


# ==============================================================================
# TEST: validate_file_path()
# ==============================================================================


class TestValidateFilePath:
    """Tests for the validate_file_path function."""

    def test_none_returns_false(self):
        """None should return False."""
        assert ag.validate_file_path(None) is False

    def test_empty_string_returns_false(self):
        """Empty string should return False."""
        assert ag.validate_file_path("") is False

    def test_nonexistent_file_returns_false(self):
        """Non-existent file should return False."""
        assert ag.validate_file_path("/nonexistent/path/to/file.txt") is False

    def test_valid_file_returns_true(self, temp_dir):
        """Valid readable file should return True."""
        filepath = os.path.join(temp_dir, "test.txt")
        with open(filepath, "w") as f:
            f.write("test content")
        assert ag.validate_file_path(filepath) is True

    def test_directory_returns_false(self, temp_dir):
        """Directory path should return False."""
        assert ag.validate_file_path(temp_dir) is False


# ==============================================================================
# TEST: identify_category()
# ==============================================================================


class TestIdentifyCategory:
    """Tests for the identify_category function."""

    def test_rules_category(self):
        """Text with rule keywords should return 'rules'."""
        text = "You must always follow security standards. Never skip formatting."
        assert ag.identify_category(text) == "rules"

    def test_workflows_category(self):
        """Text with workflow keywords should return 'workflows'."""
        text = "Step 1: Deploy the application. Step 2: Run the setup process."
        assert ag.identify_category(text) == "workflows"

    def test_skills_category(self):
        """Text with skill keywords should return 'skills'."""
        text = "Use the CLI command with flags. The terminal script handles automation."
        assert ag.identify_category(text) == "skills"

    def test_docs_category(self):
        """Text with doc keywords should return 'docs'."""
        text = "This is an overview of the architecture. Background context included."
        assert ag.identify_category(text) == "docs"

    def test_unknown_returns_docs(self):
        """Unknown text without keywords should return 'docs'."""
        text = "Lorem ipsum dolor sit amet."
        assert ag.identify_category(text) == "docs"

    def test_case_insensitive(self):
        """Category detection should be case-insensitive."""
        text = "You MUST ALWAYS follow SECURITY STANDARDS."
        assert ag.identify_category(text) == "rules"


# ==============================================================================
# TEST: build_gitignore()
# ==============================================================================


class TestBuildGitignore:
    """Tests for the build_gitignore function."""

    def test_empty_keywords_returns_base(self):
        """Empty keywords should return only base gitignore."""
        result = ag.build_gitignore([])
        assert ".DS_Store" in result
        assert "__pycache__" not in result

    def test_python_keywords(self):
        """Python keyword should add Python-specific ignores."""
        result = ag.build_gitignore(["python"])
        assert "__pycache__/" in result
        assert "venv/" in result

    def test_node_keywords(self):
        """Node keyword should add Node-specific ignores."""
        result = ag.build_gitignore(["node"])
        assert "node_modules/" in result

    def test_javascript_alias(self):
        """JavaScript should be aliased to node."""
        result = ag.build_gitignore(["javascript"])
        assert "node_modules/" in result

    def test_js_alias(self):
        """JS should be aliased to node."""
        result = ag.build_gitignore(["js"])
        assert "node_modules/" in result

    def test_multiple_keywords(self):
        """Multiple keywords should combine their ignores."""
        result = ag.build_gitignore(["python", "node"])
        assert "__pycache__/" in result
        assert "node_modules/" in result


# ==============================================================================
# TEST: build_nix_config()
# ==============================================================================


class TestBuildNixConfig:
    """Tests for the build_nix_config function."""

    def test_base_packages_included(self):
        """Base packages should always be included."""
        result = ag.build_nix_config([])
        assert "pkgs.git" in result
        assert "pkgs.curl" in result
        assert "pkgs.jq" in result

    def test_python_packages(self):
        """Python keyword should add Python packages."""
        result = ag.build_nix_config(["python"])
        assert "pkgs.python312" in result

    def test_django_uses_python(self):
        """Django should be aliased to Python packages."""
        result = ag.build_nix_config(["django"])
        assert "pkgs.python312" in result

    def test_react_uses_node(self):
        """React should be aliased to Node packages."""
        result = ag.build_nix_config(["react"])
        assert "pkgs.nodejs_20" in result


# ==============================================================================
# TEST: build_tech_stack_rule()
# ==============================================================================


class TestBuildTechStackRule:
    """Tests for the build_tech_stack_rule function."""

    def test_single_keyword(self):
        """Single keyword should appear in output."""
        result = ag.build_tech_stack_rule(["python"])
        assert "python" in result
        assert "Keywords Detected: python" in result

    def test_multiple_keywords(self):
        """Multiple keywords should appear comma-separated."""
        result = ag.build_tech_stack_rule(["python", "react"])
        assert "python" in result
        assert "react" in result

    def test_contains_directives(self):
        """Output should contain directive sections."""
        result = ag.build_tech_stack_rule(["python"])
        assert "Directives" in result
        assert "Inference" in result
        assert "Tooling" in result


# ==============================================================================
# TEST: get_destination_path()
# ==============================================================================


class TestGetDestinationPath:
    """Tests for the get_destination_path function."""

    def test_rules_path(self):
        """Rules category should go to .agent/rules."""
        result = ag.get_destination_path("/base", "rules", "test_rule")
        assert ".agent" in result
        assert "rules" in result
        assert "imported_test_rule.md" in result

    def test_workflows_path(self):
        """Workflows category should go to .agent/workflows."""
        result = ag.get_destination_path("/base", "workflows", "test_workflow")
        assert "workflows" in result
        assert "imported_test_workflow.md" in result

    def test_skills_path(self):
        """Skills category should go to .agent/skills with SKILL.md."""
        result = ag.get_destination_path("/base", "skills", "test_skill")
        assert "skills" in result
        assert "SKILL.md" in result

    def test_docs_path(self):
        """Docs category should go to docs/imported."""
        result = ag.get_destination_path("/base", "docs", "test_doc")
        assert "docs" in result
        assert "imported" in result


# ==============================================================================
# TEST: File I/O Functions
# ==============================================================================


class TestFileIO:
    """Tests for file I/O utility functions."""

    def test_write_file_creates_file(self, temp_dir):
        """write_file should create a new file."""
        filepath = os.path.join(temp_dir, "test.txt")
        result = ag.write_file(filepath, "test content")
        assert result is True
        assert os.path.exists(filepath)
        with open(filepath) as f:
            assert "test content" in f.read()

    def test_write_file_creates_parent_dirs(self, temp_dir):
        """write_file should create parent directories."""
        filepath = os.path.join(temp_dir, "nested", "path", "test.txt")
        result = ag.write_file(filepath, "test content")
        assert result is True
        assert os.path.exists(filepath)

    def test_append_file_appends_content(self, temp_dir):
        """append_file should append to existing file."""
        filepath = os.path.join(temp_dir, "test.txt")
        ag.write_file(filepath, "first")
        ag.append_file(filepath, "second")
        with open(filepath) as f:
            content = f.read()
        assert "first" in content
        assert "second" in content

    def test_write_file_safe_mode_skips_existing(self, temp_dir):
        """write_file with exist_ok=True should skip existing files."""
        filepath = os.path.join(temp_dir, "existing.txt")
        with open(filepath, "w") as f:
            f.write("original content")

        # Try to write new content in safe mode
        result = ag.write_file(filepath, "new content", exist_ok=True)

        assert result is True
        # Content should NOT change
        with open(filepath) as f:
            assert f.read() == "original content"

    def test_write_file_overwrite_mode_replaces_existing(self, temp_dir):
        """write_file with exist_ok=False should overwrite existing files."""
        filepath = os.path.join(temp_dir, "overwrite.txt")
        with open(filepath, "w") as f:
            f.write("original content")

        # Try to write new content in overwrite mode
        result = ag.write_file(filepath, "new content", exist_ok=False)

        assert result is True
        # Content SHOULD change
        with open(filepath) as f:
            assert f.read().strip() == "new content"

    def test_create_folder_creates_directory(self, temp_dir):
        """create_folder should create directory with .gitkeep."""
        folderpath = os.path.join(temp_dir, "new_folder")
        result = ag.create_folder(folderpath)
        assert result is True
        assert os.path.isdir(folderpath)
        assert os.path.exists(os.path.join(folderpath, ".gitkeep"))

    @patch("builtins.input", return_value="u")
    def test_generate_project_safe_update(self, mock_input, temp_dir):
        """generate_project should respect safe update mode when directory exists."""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            project_name = "existing_project"
            base_dir = os.path.join(temp_dir, project_name)

            # Create existing project with a file
            os.makedirs(base_dir)
            existing_file = os.path.join(base_dir, "README.md")
            with open(existing_file, "w") as f:
                f.write("# Original README")

            # Run generator in update mode
            # We need to mock setup_logging to avoid file conflicts or clutter
            with patch("antigravity_master_setup.setup_logging"):
                result = ag.generate_project(project_name, ["python"])

            assert result is True

            # Check that README was NOT overwritten
            with open(existing_file) as f:
                assert f.read() == "# Original README"

            # Check that other files WERE created (e.g., .gitignore)
            assert os.path.exists(os.path.join(base_dir, ".gitignore"))
        finally:
            os.chdir(original_cwd)


# ==============================================================================
# TEST: process_brain_dump()
# ==============================================================================


class TestProcessBrainDump:
    """Tests for the process_brain_dump function."""

    def test_none_path_returns_empty(self, temp_dir):
        """None path should return empty list."""
        result = ag.process_brain_dump(None, temp_dir)
        assert result == []

    def test_invalid_path_returns_empty(self, temp_dir):
        """Invalid path should return empty list."""
        result = ag.process_brain_dump("/nonexistent/file.md", temp_dir)
        assert result == []

    def test_detects_keywords(self, sample_brain_dump, temp_dir):
        """Should detect technology keywords from content."""
        # Create a brain dump with python keyword
        content = "This project uses python for backend development."
        filepath = os.path.join(temp_dir, "tech_dump.md")
        with open(filepath, "w") as f:
            f.write(f"# Overview\n\n{content}")

        result = ag.process_brain_dump(filepath, temp_dir)
        assert "python" in result

    def test_creates_raw_archive(self, sample_brain_dump, temp_dir):
        """Should create raw archive in context/raw."""
        ag.process_brain_dump(sample_brain_dump, temp_dir)
        raw_path = os.path.join(temp_dir, "context", "raw", "master_brain_dump.md")
        assert os.path.exists(raw_path)


# ==============================================================================
# TEST: generate_agent_files()
# ==============================================================================


class TestGenerateAgentFiles:
    """Tests for the generate_agent_files function."""

    def test_creates_rule_files(self, temp_dir):
        """Should create all rule files."""
        ag.generate_agent_files(temp_dir, ["python"])

        rules_dir = os.path.join(temp_dir, ".agent", "rules")
        assert os.path.exists(os.path.join(rules_dir, "00_identity.md"))
        assert os.path.exists(os.path.join(rules_dir, "01_tech_stack.md"))
        assert os.path.exists(os.path.join(rules_dir, "02_security.md"))

    def test_creates_workflow_files(self, temp_dir):
        """Should create all workflow files."""
        ag.generate_agent_files(temp_dir, ["python"])

        workflows_dir = os.path.join(temp_dir, ".agent", "workflows")
        assert os.path.exists(os.path.join(workflows_dir, "plan.md"))
        assert os.path.exists(os.path.join(workflows_dir, "bootstrap.md"))
        assert os.path.exists(os.path.join(workflows_dir, "commit.md"))

    def test_creates_skill_files(self, temp_dir):
        """Should create all skill files."""
        ag.generate_agent_files(temp_dir, ["python"])

        skills_dir = os.path.join(temp_dir, ".agent", "skills")
        assert os.path.exists(os.path.join(skills_dir, "git_automation", "SKILL.md"))
        assert os.path.exists(os.path.join(skills_dir, "secrets_manager", "SKILL.md"))


# ==============================================================================
# TEST: Integration
# ==============================================================================


class TestIntegration:
    """Integration tests for full project generation."""

    def test_generate_project_creates_structure(self, temp_dir):
        """generate_project should create complete project structure."""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)

            with patch("builtins.input", return_value="n"):
                # First call should succeed (no existing dir)
                result = ag.generate_project("test-project", ["python"])

            assert result is True
            project_dir = os.path.join(temp_dir, "test-project")

            # Check essential files exist
            assert os.path.exists(os.path.join(project_dir, ".gitignore"))
            assert os.path.exists(os.path.join(project_dir, "README.md"))
            assert os.path.exists(os.path.join(project_dir, ".env.example"))
            assert os.path.exists(os.path.join(project_dir, "CHANGELOG.md"))
            assert os.path.exists(os.path.join(project_dir, "CONTRIBUTING.md"))
            assert os.path.exists(os.path.join(project_dir, "AUDIT.md"))
            assert os.path.exists(os.path.join(project_dir, "BOOTSTRAP_INSTRUCTIONS.md"))

            # Check GitHub templates exist
            assert os.path.exists(os.path.join(project_dir, ".github", "PULL_REQUEST_TEMPLATE.md"))
            assert os.path.exists(os.path.join(project_dir, ".github", "FUNDING.yml"))
            assert os.path.exists(os.path.join(project_dir, ".github", "copilot-instructions.md"))

            # Check AI IDE compatibility files exist
            assert os.path.exists(os.path.join(project_dir, ".cursorrules"))
            assert os.path.exists(os.path.join(project_dir, ".windsurfrules"))

            # Verify copilot instructions content
            copilot_file = os.path.join(project_dir, ".github", "copilot-instructions.md")
            with open(copilot_file, "r", encoding="utf-8") as f:
                content = f.read()
                assert "GitHub Copilot Instructions" in content
                assert "Development Workflow" in content
                assert "python" in content  # Tech stack should be included

            # Verify Cursor rules content
            cursor_file = os.path.join(project_dir, ".cursorrules")
            with open(cursor_file, "r", encoding="utf-8") as f:
                content = f.read()
                assert "Cursor IDE Rules" in content
                assert "python" in content

            # Verify Windsurf rules content
            windsurf_file = os.path.join(project_dir, ".windsurfrules")
            with open(windsurf_file, "r", encoding="utf-8") as f:
                content = f.read()
                assert "Windsurf IDE Rules" in content
                assert "Cascade" in content
                assert "python" in content

            # Check directories exist
            assert os.path.isdir(os.path.join(project_dir, "src"))
            assert os.path.isdir(os.path.join(project_dir, "tests"))
            assert os.path.isdir(os.path.join(project_dir, ".agent"))

        finally:
            os.chdir(original_cwd)
