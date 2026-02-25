import os

from antigravity_architect.cli import main
from antigravity_architect.core.builder import AntigravityBuilder, AntigravityGenerator
from antigravity_architect.core.engine import AntigravityEngine
from antigravity_architect.plugins.manager import PluginManager


def test_cli_dry_run(tmp_path, capsys):
    """Test the dry run mode."""
    main(["--name", "dry-run-test", "--dry-run"])
    captured = capsys.readouterr()
    assert "DRY RUN MODE" in captured.out
    assert "dry-run-test" in captured.out
    assert not (tmp_path / "dry-run-test").exists()


def test_cli_doctor_fix(tmp_path, capsys):
    """Test doctor fix logic on empty project."""
    test_proj = tmp_path / "doctor_test"
    test_proj.mkdir()

    # Run doctor with fix
    main(["--doctor", str(test_proj), "--fix"])

    # Assert
    assert (test_proj / ".agent" / "rules").exists()
    assert (test_proj / ".agent" / "workflows").exists()
    assert (test_proj / ".agent" / "rules" / "00_identity.md").exists()


def test_cli_presets(tmp_path, capsys):
    """Test saving and loading presets."""
    os.environ["ANTIGRAVITY_HOME"] = str(tmp_path)
    main(["--name", "preset-b", "--save-preset", "mypreset", "--stack", "go", "--dry-run"])

    main(["--preset", "mypreset", "--dry-run"])
    captured = capsys.readouterr()
    assert "go" in captured.out
    assert "preset-b" in captured.out


def test_cli_list_commands(capsys):
    """Test list keywords and blueprints."""
    main(["--list-keywords"])
    main(["--list-blueprints"])
    captured = capsys.readouterr()
    assert "FastAPI" in captured.out or "Blueprints Index" in captured.out
    assert "Supported Tech Stack" in captured.out


def test_engine_create_error(tmp_path):
    """Test engine handling creation error."""
    # Write to a file as if it were a directory
    f = tmp_path / "file.txt"
    f.touch()
    assert not AntigravityEngine.create_folder(str(f))


def test_builder_links(tmp_path):
    old = os.getcwd()
    os.chdir(str(tmp_path))
    try:
        (tmp_path / "sibling").mkdir()
        (tmp_path / "sibling" / ".git").mkdir()
        res = AntigravityBuilder.build_links("test")
        assert "sibling" in res
    finally:
        os.chdir(old)


def test_plugin_load_error(tmp_path):
    # Simulate a bad plugin
    p = tmp_path / "ag_plugin_bad.py"
    p.write_text("1/0", encoding="utf-8")
    PluginManager._plugins.clear()
    PluginManager.load_plugins(project_dir=str(tmp_path))
    assert "ag_plugin_bad" not in PluginManager._plugins


def test_generator_safe_mode_cancel(monkeypatch, tmp_path):
    """Mock user input to test safe mode cancellation."""
    test_dir = tmp_path / "exist"
    test_dir.mkdir()
    monkeypatch.setattr("builtins.input", lambda _: "c")
    res = AntigravityGenerator._handle_safe_mode("test", str(test_dir), None)
    assert res is None
