# ruff: noqa: F403, F405, PTH, RUF012
import argparse
from pathlib import Path

from antigravity_architect.core.builder import AntigravityGenerator
from antigravity_architect.core.engine import AntigravityEngine
from antigravity_architect.resources.constants import *
from antigravity_architect.resources.templates import *


def build_cli_parser() -> argparse.ArgumentParser:
    """Build the argument parser for CLI mode."""
    parser = argparse.ArgumentParser(
        prog="antigravity-architect",
        description="🌌 Antigravity Architect: Agent-First Project Bootstrapper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  antigravity-architect                           # Interactive mode
  antigravity-architect --name my-app --stack python,react
  antigravity-architect --name my-app --brain-dump ./specs.md --safe
  antigravity-architect --doctor ./existing-project
  antigravity-architect --list-keywords
        """,
    )

    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")

    parser.add_argument("--name", "-n", type=str, help="Project name (required for CLI mode)")
    parser.add_argument(
        "--stack", "-s", type=str, help="Comma-separated tech stack keywords (e.g., python,react,docker)"
    )
    parser.add_argument("--brain-dump", "-b", type=str, help="Path to brain dump file for Knowledge Assimilation")
    parser.add_argument("--safe", action="store_true", help="Enable Safe Update Mode (non-destructive)")
    parser.add_argument("--dry-run", action="store_true", help="Preview actions without creating files")
    parser.add_argument("--templates", "-t", type=str, help="Path to custom templates directory")

    parser.add_argument("--doctor", type=str, metavar="PATH", help="Validate an existing project's .agent/ structure")
    parser.add_argument("--fix", action="store_true", help="Attempt to fix issues found by --doctor")

    parser.add_argument("--list-keywords", action="store_true", help="List all supported tech stack keywords")
    parser.add_argument(
        "--license",
        "-l",
        type=str,
        choices=["mit", "apache", "gpl"],
        default="mit",
        help="Project license (default: mit)",
    )
    parser.add_argument(
        "--blueprint",
        type=str,
        help="Apply a specialized project blueprint (built-in name or git URL)",
    )

    parser.add_argument("--save-preset", type=str, help="Save current arguments as a named preset")
    parser.add_argument("--preset", type=str, help="Load arguments from a saved preset")
    parser.add_argument("--list-presets", action="store_true", help="List all saved presets")
    parser.add_argument("--list-blueprints", action="store_true", help="List all built-in blueprints")

    # Phase 13 & 16: Ecosystem & Governance
    parser.add_argument(
        "--ide", type=str, choices=["jetbrains", "neovim", "zed", "fleet"], help="Generate IDE configuration"
    )
    parser.add_argument("--ci", type=str, choices=["gitlab", "azure"], help="Generate CI pipeline")
    parser.add_argument("--docker", action="store_true", help="Generate Docker Compose configuration")
    parser.add_argument("--personality", type=str, choices=["startup", "enterprise", "minimal"], help="Agent behavior personality pack")
    parser.add_argument("--sbom", type=str, metavar="PATH", help="Generate CycloneDX SBOM for a project")

    return parser


FILE_STACK_MAP = {
    "pyproject.toml": "python",
    "requirements.txt": "python",
    "setup.py": "python",
    "package.json": "node",
    "go.mod": "go",
    "Cargo.toml": "rust",
    "composer.json": "php",
    "Gemfile": "ruby",
    "build.gradle": "java",
    "pom.xml": "java",
    "flake.nix": "nix",
    "Dockerfile": "docker",
    "docker-compose.yml": "docker",
}


def _auto_detect_stack(base_path: Path) -> list[str]:
    """Infers tech stack based on file existence in the directory."""
    detected = set()
    if not base_path.exists():
        return []

    # Check for specific files
    for filename, keyword in FILE_STACK_MAP.items():
        if (base_path / filename).exists():
            detected.add(keyword)

    # Check for directory patterns
    if (base_path / "src").exists() and (base_path / "tests").exists():
        detected.add("python")  # Modern python structure

    if (base_path / "node_modules").exists() or (base_path / "public").exists():
        detected.add("node")

    return list(detected)


def _parse_brain_dump_intent(content: str) -> list[str]:
    """Scans brain dump text for keywords to infer tech stack."""
    detected = set()
    text = content.lower()

    # Check against categorized aliases
    for category, aliases in TECH_ALIASES.items():
        if category in text:
            detected.add(category)
        for alias in aliases:
            if alias in text:
                detected.add(category)
                detected.add(alias)

    # Additional common tech indicators
    if ("api" in text or "endpoint" in text) and "python" in detected:
        detected.add("fastapi")
    elif ("api" in text or "endpoint" in text) and "node" in detected:
        detected.add("express")

    if ("frontend" in text or "ui" in text or "ux" in text) and "node" in detected:
        detected.add("react")

    return list(detected)


def load_custom_templates(templates_path: str | None) -> dict[str, dict[str, str]]:
    """
    Load custom templates from a directory, merging with defaults.

    Returns a dict with keys 'rules', 'workflows', 'skills' containing template overrides.
    """
    if not templates_path:
        home_templates = Path.home() / ANTIGRAVITY_DIR_NAME / "templates"
        if home_templates.exists():
            templates_path = str(home_templates)
        else:
            return {}

    templates_dir = Path(templates_path)
    if not templates_dir.exists():
        import logging

        logging.warning(f"⚠️ Templates directory not found: {templates_path}")
        return {}

    overrides: dict[str, dict[str, str]] = {"rules": {}, "workflows": {}, "skills": {}}

    for category in overrides:
        category_dir = templates_dir / category
        if category_dir.exists():
            import logging

            for file_path in category_dir.glob("*.md"):
                content = file_path.read_text(encoding="utf-8")
                overrides[category][file_path.name] = content
                logging.info(f"📦 Loaded custom template: {category}/{file_path.name}")

    return overrides


def _doctor_check_dir(base_dir: Path, dir_path: str, fix: bool) -> tuple[str | None, str | None, str | None]:
    """Checks directory existence and optionally fixes it."""
    full_path = base_dir / dir_path
    if full_path.exists():
        return f"✅ {dir_path}/ exists", None, None

    msg = f"❌ Missing: {dir_path}/"
    fixed = None
    if fix:
        full_path.mkdir(parents=True, exist_ok=True)
        (full_path / ".gitkeep").touch()
        fixed = f"🔧 Created {dir_path}/"
    return None, msg, fixed


def _doctor_check_file(
    base_dir: Path, file_path: str, template: str | None, fix: bool, optional: bool = False
) -> tuple[str | None, str | None, str | None, str | None]:
    """Checks file health and optionally fixes it."""
    full_path = base_dir / file_path
    is_missing = not full_path.exists()
    is_empty = full_path.exists() and full_path.stat().st_size == 0
    actual_content = "" if is_missing else full_path.read_text(encoding="utf-8")

    passed, warning, issue, fixed_msg = None, None, None, None

    # Phase 11: Diff-Based Doctor Reports (Drift Detection)
    if not is_missing and template:
        actual_hash = AntigravityEngine._get_checksum(actual_content)
        expected_hash = AntigravityEngine._get_checksum(template)
        if actual_hash != expected_hash:
            warning = f"⚠️  Drift: {file_path} differs from template"
            print(f"\n🔍 Drift Detail: {file_path}")
            print(AntigravityEngine.get_diff(actual_content, template))

    if not is_missing and not is_empty and not warning:
        return f"✅ {file_path} matches canonical protocol", None, None, None

    if is_missing:
        if optional:
            warning = f"⚠️  Optional: {file_path} not found"
        else:
            issue = f"❌ Missing: {file_path}"
    elif is_empty:
        warning = f"⚠️  {file_path} is empty"

    if fix and template:
        if is_missing:
            full_path.parent.mkdir(parents=True, exist_ok=True)

        full_path.write_text(template, encoding="utf-8")
        fixed_msg = f"🔧 Generated {file_path}" if is_missing else f"🔧 Restored {file_path}"

    return passed, warning, issue, fixed_msg


def _get_doctor_requirements() -> tuple[list[str], dict[str, tuple[str, str]]]:
    """Returns required directories and files for doctor check."""
    dirs = [
        ".agent/rules",
        ".agent/workflows",
        ".agent/skills",
        ".agent/memory",
    ]

    files = {
        f".agent/rules/{RULE_IDENTITY}": (
            "Agent identity rule",
            AGENT_RULES[RULE_IDENTITY],
        ),
        f".agent/rules/{RULE_SECURITY}": (
            "Security protocol",
            AGENT_RULES[RULE_SECURITY],
        ),
        ".agent/workflows/plan.md": (
            "Plan workflow",
            AGENT_WORKFLOWS["plan.md"],
        ),
    }
    return dirs, files


def _get_doctor_optional_files() -> dict[str, tuple[str, str]]:
    """Returns optional files for doctor check."""
    files = [
        GITIGNORE_FILE,
        README_FILE,
        CHANGELOG_FILE,
        CONTRIBUTING_FILE,
        AUDIT_FILE,
        SECURITY_FILE,
        CODE_OF_CONDUCT_FILE,
        LICENSE_FILE,
    ]
    return dict.fromkeys(files, ("Optional project file", ""))


def _validate_doctor_dirs(base_dir: Path, dirs: list[str], fix: bool) -> tuple[list[str], list[str], list[str]]:
    """Validates and fixes directories."""
    passed, issues, fixed = [], [], []
    for d in dirs:
        p, i, f = _doctor_check_dir(base_dir, d, fix)
        if p:
            passed.append(p)
        if i:
            issues.append(i)
        if f:
            fixed.append(f)
    return passed, issues, fixed


def _validate_doctor_files(
    base_dir: Path, files: dict[str, tuple[str, str]], fix: bool
) -> tuple[list[str], list[str], list[str], list[str]]:
    """Validates and fixes files."""
    passed, warnings, issues, fixed = [], [], [], []
    for f_path, (_, tmpl) in files.items():
        is_optional = False
        p, w, i, f = _doctor_check_file(base_dir, f_path, tmpl, fix, optional=is_optional)
        if p:
            passed.append(p)
        if w:
            warnings.append(w)
        if i:
            issues.append(i)
        if f:
            fixed.append(f)
    return passed, warnings, issues, fixed


def _print_doctor_results(passed: list[str], warnings: list[str], issues: list[str], fixed: list[str]) -> None:
    """Prints the results of the doctor check."""
    print(SEPARATOR)
    print(f"Summary: {len(passed)} passed, {len(warnings)} warnings, {len(issues)} issues")

    if fixed:
        print("\n🔧 Fixes Applied:")
        for fix_msg in fixed:
            print(f"  {fix_msg}")

    if issues:
        print("\n🚨 Issues Found:")
        for issue in issues:
            print(f"  {issue}")

    if warnings:
        print("\n⚠️  Warnings:")
        for warning in warnings:
            print(f"  {warning}")

    print(f"\n{SEPARATOR}")


def doctor_project(project_path: str, fix: bool = False) -> bool:
    """
    Validates the integrity of an Antigravity project.
    """
    base_dir = Path(project_path).resolve()
    print(f"\n🩺 Running Doctor on: {project_path}")
    print(SEPARATOR)

    if not base_dir.exists():
        print(f"❌ Project directory not found: {project_path}")
        return False

    # Phase 11: Auto-Stack Detection during Doctor
    detected_stack = _auto_detect_stack(base_dir)
    if detected_stack:
        print(f"📊 Auto-Detected Stack: {', '.join(detected_stack)}")

    passed: list[str] = []
    issues: list[str] = []
    warnings: list[str] = []
    fixed: list[str] = []

    # Phase 16: Security & Governance Audit
    from antigravity_architect.core.governance import AntigravityGovernance

    print("⚖️  Governance: Checking licenses and environment schema...")

    conflicts = AntigravityGovernance.scan_licenses(str(base_dir))
    for name, msg in conflicts.items():
        warnings.append(f"⚖️  {name}: {msg}")

    env_errors = AntigravityGovernance.validate_env_schema(str(base_dir))
    for err in env_errors:
        issues.append(err)

    req_dirs, req_files = _get_doctor_requirements()

    d_passed, d_issues, d_fixed = _validate_doctor_dirs(base_dir, req_dirs, fix)
    passed.extend(d_passed)
    issues.extend(d_issues)
    fixed.extend(d_fixed)

    f_passed, f_warnings, f_issues, f_fixed = _validate_doctor_files(base_dir, req_files, fix)
    passed.extend(f_passed)
    warnings.extend(f_warnings)
    issues.extend(f_issues)
    fixed.extend(f_fixed)

    opt_files = _get_doctor_optional_files()
    o_passed, o_warnings, o_issues, o_fixed = _validate_doctor_files(base_dir, opt_files, fix)
    passed.extend(o_passed)
    warnings.extend(o_warnings)
    issues.extend(o_issues)
    fixed.extend(o_fixed)

    _print_doctor_results(passed, warnings, issues, fixed)

    remaining_issues = len(issues) - len([f for f in fixed if "Missing" in f or "Regenerated" in f])
    if remaining_issues > 0 and not fix:
        print("❌ Project needs attention! Run with --fix to repair.")
        return False
    elif fixed:
        print("🏆 Project repaired and healthy!")
        return True
    elif issues:
        print("❌ Project needs attention!")
        return False
    else:
        print("🏆 Project is fully healthy!")
        return True


def list_keywords() -> None:
    """Display all supported tech stack keywords."""
    print("\n🛠 Supported Tech Stack Keywords")
    print(SEPARATOR)

    categories = {
        "Languages": ["python", "node", "javascript", "rust", "go", "java", "php", "ruby"],
        "Frameworks": ["react", "nextjs", "django", "flask", "fastapi"],
        "Infrastructure": ["docker", "sql", "postgres"],
        "OS / Platforms": ["macos", "windows", "linux"],
        "IDEs": ["vscode", "idea"],
    }

    for category, keywords in categories.items():
        print(f"\n{category}:")
        print(f"  {', '.join(keywords)}")

    print("\n" + SEPARATOR)
    print("Usage: --stack python,react,docker")


def list_blueprints() -> None:
    """Display all available built-in and marketplace blueprints."""
    print("\n💎 Blueprints Index (Local + Marketplace)")
    print(SEPARATOR)

    all_blueprints = AntigravityEngine.get_all_blueprints()
    for name, data in all_blueprints.items():
        desc = f"Stack: {', '.join(data.get('stack', []))}"
        print(f"  - {name:<12} : {desc}")

    print("\n" + SEPARATOR)
    print("Usage: --blueprint <name> OR --blueprint https://github.com/user/repo")


def run_interactive_mode() -> None:
    """Original interactive mode for backwards compatibility."""
    print(SEPARATOR)
    print(f"   🌌 Antigravity Architect v{VERSION}")
    print("   Dynamic Parsing | Knowledge Distribution | Universal")
    print(SEPARATOR)

    AntigravityEngine.setup_logging()

    print("\n[Optional] Drag & Drop a Brain Dump file (Specs/Notes/Code):")
    brain_dump_path: str | None = input("Path: ").strip().strip("'\"") or None

    raw_name = input("\nProject Name: ")
    project_name = AntigravityEngine.sanitize_name(raw_name)
    if not project_name or (project_name == "antigravity-project" and not raw_name):
        print("❌ Project name is required.")
        return

    manual_keywords: list[str] = []
    if not brain_dump_path:
        print("\nTech Stack (e.g. python, react, aws):")
        k_in = input("Keywords: ")
        manual_keywords = AntigravityEngine.parse_keywords(k_in)

        if not any(x in manual_keywords for x in ("macos", "windows", "linux")):
            manual_keywords.append("linux")

    print("\nLicense (mit, apache, gpl):")
    license_choice = input("Choice [mit]: ").strip().lower() or "mit"

    AntigravityGenerator.generate_project(project_name, manual_keywords, brain_dump_path, license_type=license_choice)


def _print_dry_run_header(project_name: str, keywords: list[str], args: argparse.Namespace) -> None:
    """Prints the dry run header summary."""
    print("\n🔍 DRY RUN MODE - No files will be created")
    print("=" * 60)
    print(f"📦 Project Name: {project_name}")
    print(f"⚙️  Tech Stack: {', '.join(keywords)}")
    print(f"🧠 Brain Dump: {args.brain_dump or 'None'}")
    print(f"🛡️  Safe Mode: {args.safe}")
    print(f"📁 Templates: {args.templates or 'Default (Built-in)'}")
    print(f"📜 License: {args.license}")
    print("=" * 60)


def _print_dry_run_directories(project_name: str) -> None:
    """Prints directories to be created."""
    print("\n📁 Directories that would be created:")
    dirs = [
        "src",
        "tests",
        "docs/imported",
        "context/raw",
        ".github/ISSUE_TEMPLATE",
        ".agent/rules",
        ".agent/workflows",
        ".agent/skills/git_automation",
        ".agent/skills/secrets_manager",
        ".agent/memory",
    ]
    for d in dirs:
        print(f"    📂 {project_name}/{d}/")


def _print_dry_run_files(project_name: str, keywords: list[str]) -> None:
    """Prints core files to be created."""
    print("\n📄 Core Files that would be created:")
    core_files = [
        ".gitignore",
        "README.md",
        "LICENSE",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "AUDIT.md",
        "SECURITY.md",
        "CODE_OF_CONDUCT.md",
        BOOTSTRAP_FILE,
        ".env.example",
    ]
    for f in core_files:
        print(f"    📄 {project_name}/{f}")

    print("\n🤖 AI IDE Configuration Files:")
    ide_files = [
        (".github/copilot-instructions.md", f"Tech Stack: {', '.join(keywords)}"),
    ]
    for f, desc in ide_files:
        print(f"    🤖 {project_name}/{f} ({desc})")


def _print_dry_run_agent(keywords: list[str]) -> None:
    """Prints agent-specific files."""
    print("\n📜 Agent Rules & Workflows:")
    for rule_file in AGENT_RULES:
        print(f"    📜 .agent/rules/{rule_file}")
    print(f"    📜 .agent/rules/01_tech_stack.md (Dynamic: {', '.join(keywords)})")
    for workflow_file in AGENT_WORKFLOWS:
        print(f"    ⚡ .agent/workflows/{workflow_file}")

    print("\n📋 Project Standards & CI/CD:")
    print("    📋 .github/workflows/ci.yml")

    print("\n🛠️  Agent Skills (.agent/skills/):")
    for skill_file in AGENT_SKILLS:
        print(f"    🛠️  {skill_file}")

    print("\n🧠 Agent Memory (.agent/memory/):")
    print("    🧠 scratchpad.md")


def _print_dry_run_templates() -> None:
    """Prints template files."""
    print("\n📋 GitHub Templates (.github/):")
    github_files = [
        "ISSUE_TEMPLATE/bug_report.md",
        "ISSUE_TEMPLATE/feature_request.md",
        "ISSUE_TEMPLATE/question.md",
        "ISSUE_TEMPLATE/config.yml",
        "PULL_REQUEST_TEMPLATE.md",
        "FUNDING.yml",
    ]
    for f in github_files:
        print(f"    📋 {f}")


def _print_dry_run_report(project_name: str, keywords: list[str], args: argparse.Namespace) -> None:
    """Helper to print dry run details."""
    _print_dry_run_header(project_name, keywords, args)
    _print_dry_run_directories(project_name)
    _print_dry_run_files(project_name, keywords)
    _print_dry_run_agent(keywords)
    _print_dry_run_templates()

    print("\n" + "=" * 60)
    print("✅ Dry run complete. No changes made.")
    print("   Run without --dry-run to create the project.")


def run_cli_mode(args: argparse.Namespace) -> None:
    """Run in CLI mode with provided arguments."""
    print("=========================================================")
    print(f"   🌌 Antigravity Architect v{VERSION} (CLI Mode)")
    print("=========================================================")

    AntigravityEngine.setup_logging()

    custom_templates = load_custom_templates(args.templates)
    if custom_templates:
        print(f"📦 Loaded {sum(len(v) for v in custom_templates.values())} custom templates")

    project_name = AntigravityEngine.sanitize_name(args.name)
    if not project_name:
        print("❌ Invalid project name.")
        return

    keywords = AntigravityEngine.parse_keywords(args.stack) if args.stack else []

    # Phase 11: Semantic Intelligence
    if not keywords:
        if args.brain_dump and Path(args.brain_dump).exists():
            dump_content = Path(args.brain_dump).read_text(encoding="utf-8")
            keywords = _parse_brain_dump_intent(dump_content)
            if keywords:
                print(f"🧠 Detected stack from brain dump: {', '.join(keywords)}")

        if not keywords:
            cwd_stack = _auto_detect_stack(Path.cwd())
            if cwd_stack:
                keywords = cwd_stack
                print(f"📂 Detected stack from current directory: {', '.join(keywords)}")

    if not any(x in keywords for x in ("macos", "windows", "linux")):
        keywords.append("linux")

    if args.dry_run:
        _print_dry_run_report(project_name, keywords, args)
        return

    AntigravityGenerator.generate_project(
        project_name,
        keywords,
        args.brain_dump,
        safe_mode=args.safe,
        custom_templates=custom_templates,
        license_type=args.license,
        blueprint=args.blueprint,
        personality=args.personality,
    )

    # Phase 13: IDE & CI Ecosystem
    AntigravityGenerator.generate_ecosystem_files(
        os.getcwd(),
        ide=args.ide,
        ci=args.ci,
        docker=args.docker,
        project_name=project_name,
    )


def main(argv: list[str] | None = None) -> None:
    """Main entry point for the Antigravity Architect."""
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument("--preset", type=str)
    pre_parser.add_argument("--list-presets", action="store_true")
    pre_args, _ = pre_parser.parse_known_args(argv)

    if pre_args.list_presets:
        print("💾 Saved Presets:")
        for p in AntigravityEngine.list_presets():
            print(f"  - {p}")
        return

    defaults = {}
    if pre_args.preset:
        loaded = AntigravityEngine.load_preset(pre_args.preset)
        if loaded:
            defaults = loaded
            print(f"💎 Loaded preset: {pre_args.preset}")

    parser = build_cli_parser()
    if defaults:
        parser.set_defaults(**defaults)

    args = parser.parse_args(argv)

    if args.list_keywords:
        list_keywords()
        return

    if args.list_blueprints:
        list_blueprints()
        return

    if args.doctor:
        doctor_project(args.doctor, fix=args.fix)
        return

    if args.sbom:
        from antigravity_architect.core.governance import AntigravityGovernance

        print(f"📦 Generating SBOM for: {args.sbom}")
        sbom = AntigravityGovernance.generate_sbom(args.sbom, Path(args.sbom).name)
        output_path = os.path.join(args.sbom, "docs", "SBOM.json")
        AntigravityEngine.write_file(output_path, sbom, exist_ok=True)
        print(f"✅ SBOM generated at: {output_path}")
        return

    if args.save_preset:
        preset_data = {
            k: v
            for k, v in vars(args).items()
            if v is not None
            and k not in ("save_preset", "preset", "dry_run", "list_keywords", "list_presets", "doctor", "fix")
        }
        AntigravityEngine.save_preset(args.save_preset, preset_data)

    if args.name:
        run_cli_mode(args)
    else:
        run_interactive_mode()


if __name__ == "__main__":
    main()
