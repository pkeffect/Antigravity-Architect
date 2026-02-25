# ruff: noqa: F403, F405, PTH, RUF012
import logging
import os
from datetime import datetime
from pathlib import Path

from antigravity_architect.core.assimilator import AntigravityAssimilator
from antigravity_architect.core.engine import AntigravityEngine
from antigravity_architect.plugins.manager import PluginManager
from antigravity_architect.resources.constants import *
from antigravity_architect.resources.templates import *


class AntigravityBuilder:
    """
    Dynamic configuration and content generators.

    This class contains all the "build_*" functions that generate configuration
    files and content based on detected technology keywords and user preferences.
    All methods are static as they don't require instance state.
    """

    @staticmethod
    def build_gitignore(keywords: list[str]) -> str:
        """Builds a .gitignore file based on detected technology keywords."""
        content = BASE_GITIGNORE
        for k in keywords:
            if k in GITIGNORE_MAP:
                content += GITIGNORE_MAP[k]
            elif k in ("js", "javascript"):
                content += GITIGNORE_MAP.get("node", "")
        return content

    @staticmethod
    def build_tech_stack_rule(keywords: list[str]) -> str:
        """Builds a dynamic tech stack rule for the agent."""
        return f"""# Technology Stack
Keywords Detected: {", ".join(keywords)}

## Directives
1. **Source of Truth:** Always refer to `docs/TECH_STACK.md` for architectural deep-dives.
2. **Inference:** Assume standard frameworks for these keywords (e.g., React implies standard hooks/components).
3. **Tooling:** Use the standard CLI tools (pip, npm, cargo, go mod).
4. **Files:** Look for `pyproject.toml`, `package.json`, or similar to confirm versions.
"""

    @staticmethod
    def build_scratchpad(keywords: list[str], has_brain_dump: bool) -> str:
        """Builds the initial scratchpad memory file."""
        return f"""# Project Scratchpad <!-- ID: scratchpad -->
*Last Updated: {datetime.now().isoformat()}*

## Status <!-- ID: project_status -->
- Project initialized.
- Tech Stack: {", ".join(keywords)}.
- Imported Knowledge: {"Yes" if has_brain_dump else "No"}.

## Model Roles Map <!-- ID: model_roles -->
| Role | Recommended Model | User Selection (Fill this in) |
| :--- | :--- | :--- |
| **Architect** | Tier 3 (Opus/Ultra/o1) | [YOUR SELECTION HERE] |
| **Builder** | Tier 2 (Sonnet/Pro) | [YOUR SELECTION HERE] |
| **Assistant** | Tier 1 (Flash/Mini) | [YOUR SELECTION HERE] |
"""

    @staticmethod
    def build_docs_index(docs_dir: str) -> str:
        """Generates a summary index of all files in docs/imported."""
        content = "# Documentation Index\n\n"
        if not os.path.exists(docs_dir):
            return content + "_No documents imported yet._"

        files = sorted(os.listdir(docs_dir))
        if not files:
            return content + "_No documents imported yet._"

        content += "## Assimilated Knowledge\n"
        for f in files:
            if f.endswith(".md") and f != "INDEX.md":
                title = f.replace(".md", "").replace("_", " ").title()
                content += f"- [{title}]({f})\n"
        return content

    @staticmethod
    def build_architecture_diagram(project_name: str) -> str:
        """Builds a Mermaid diagram of the project structure."""
        return MERMAID_PROJECT_MAP.format(project_name=project_name)

    @staticmethod
    def build_links(project_name: str) -> str:
        """Scan parent directory for other projects and build context/links.md."""
        parent_dir = Path(os.getcwd())
        siblings = []
        knowledge_lake_str = "_No global knowledge lake detected._"

        try:
            for item in parent_dir.iterdir():
                if item.is_dir() and item.name != project_name:
                    # Check if it's an Antigravity project
                    if (item / ".agent").exists():
                        siblings.append(f"- **{item.name}** (linked: `../{item.name}`) - *Antigravity Project*")
                    elif (item / ".git").exists():
                        siblings.append(f"- **{item.name}** (linked: `../{item.name}`) - *Git Repository*")

            # Check for global knowledge lake
            if KNOWLEDGE_LAKE_DIR.exists():
                knowledge_lake_str = f"- **Global Context** (linked: `{KNOWLEDGE_LAKE_DIR}`) - *Shared System Memory*"
        except Exception as e:
            logging.debug(f"Error scanning for siblings: {e}")

        sibling_str = "\n".join(siblings) if siblings else "_No sibling repositories detected in this scratch space._"
        return LINKS_TEMPLATE.format(sibling_repos=sibling_str, knowledge_lake=knowledge_lake_str)


class AntigravityGenerator:
    """
    High-level project generation orchestration.

    This class coordinates all the other components (Resources, Engine, Builder,
    Assimilator) to generate complete project structures. It handles the full
    workflow from directory creation through file generation and brain dump processing.
    """

    @staticmethod
    def _calculate_token_budget(contents: list[str]) -> int:
        """Rough estimation of token count (chars / 4)."""
        total_chars = sum(len(c) for c in contents)
        return total_chars // 4

    @staticmethod
    def _generate_priority_list(keywords: list[str]) -> list[str]:
        """Adaptive Rule Weighting: Reorders and filters rules based on tech stack (v2.0.0)."""
        base_priority = [RULE_IDENTITY, RULE_TECH_STACK, RULE_SECURITY, "05_environment.md", "08_boundaries.md"]

        filtered_rules = []
        for rule_name, content in AGENT_RULES.items():
            # Parse frontmatter
            if content.startswith("---"):
                try:
                    parts = content.split("---")
                    if len(parts) >= 3:
                        import yaml  # type: ignore

                        metadata = yaml.safe_load(parts[1])
                        applies_to = metadata.get("applies_to", "*")

                        if applies_to == "*":
                            filtered_rules.append(rule_name)
                        else:
                            tags = [t.strip() for t in applies_to.split(",")]
                            if any(tag in keywords for tag in tags):
                                filtered_rules.append(rule_name)
                except Exception:
                    filtered_rules.append(rule_name)
            else:
                filtered_rules.append(rule_name)

        # Merge with high-priority order
        final_list = []
        for rule in base_priority:
            if rule in filtered_rules:
                final_list.append(rule)

        for rule in filtered_rules:
            if rule not in final_list:
                final_list.append(rule)

        return final_list

    @staticmethod
    def generate_agent_files(
        base_dir: str,
        project_name: str,
        keywords: list[str],
        safe_mode: bool = False,
        custom_templates: dict[str, dict[str, str]] | None = None,
        personality: str | None = None,
    ) -> None:
        """Generates all .agent/ rules, workflows, and skills with adaptive intelligence."""
        custom = custom_templates or {"rules": {}, "workflows": {}, "skills": {}}

        # Calculate token budget for all generated files
        all_contents = list(AGENT_RULES.values()) + list(AGENT_WORKFLOWS.values()) + list(AGENT_SKILLS.values())
        token_budget = AntigravityGenerator._calculate_token_budget(all_contents)
        priority_rules = AntigravityGenerator._generate_priority_list(keywords)

        # Phase 12: High-Performance Parallel Generation
        from concurrent.futures import ThreadPoolExecutor

        write_queue = []

        # v1.8.0 Adaptive Manifest
        manifest_path = os.path.join(base_dir, AGENT_DIR, AGENT_MANIFEST)
        import json

        manifest_data = {
            "protocol": "3.0.0",
            "project": project_name,
            "lifecycle": "INIT",
            "stats": {
                "token_budget_est": token_budget,
                "rule_count": len(AGENT_RULES),
                "generated_at": datetime.now().isoformat(),
            },
            "capabilities": {
                "reasoning_tier": "3",
                "mcp_support": True,
                "adaptive_priority": True,
                "declarative_governance": True,
            },
            "structure": {
                "rules": ".agent/rules/",
                "workflows": ".agent/workflows/",
                "skills": ".agent/skills/",
                "memory": ".agent/memory/",
                "configs": ".agent/",
                "map": "AGENT_MAP.yaml",
            },
            "ruleset": {"layered": True, "priority": priority_rules},
        }
        write_queue.append((manifest_path, json.dumps(manifest_data, indent=2)))

        # Rule sets
        for filename, content in AGENT_RULES.items():
            path = os.path.join(base_dir, AGENT_DIR, "rules", filename)
            final_content = custom.get("rules", {}).get(filename, content)
            write_queue.append((path, final_content))

        tech_stack_path = os.path.join(base_dir, AGENT_DIR, "rules", RULE_TECH_STACK)
        write_queue.append((tech_stack_path, AntigravityBuilder.build_tech_stack_rule(keywords)))

        # Workflows
        for filename, content in AGENT_WORKFLOWS.items():
            path = os.path.join(base_dir, AGENT_DIR, "workflows", filename)
            final_content = custom.get("workflows", {}).get(filename, content)
            write_queue.append((path, final_content))

        # Phase 17: Skill Chaining
        final_skill_names = set()
        from typing import Any

        skill_contents: dict[str, list[tuple[str, str]]] = {}
        skill_metadata: dict[str, dict[str, Any]] = {}

        # Pre-parse skill metadata from SKILL.md files
        for skill_path, content in AGENT_SKILLS.items():
            skill_name = skill_path.split("/")[0] if "/" in skill_path else skill_path
            if skill_path.endswith("SKILL.md") and "---" in content:
                try:
                    parts = content.split("---")
                    if len(parts) >= 3:
                        import yaml

                        meta = yaml.safe_load(parts[1])
                        skill_metadata[skill_name] = meta
                except Exception:
                    pass

            # Map all files belonging to this skill
            if skill_name not in skill_contents:
                skill_contents[skill_name] = []
            skill_contents[skill_name].append((skill_path, content))

        def resolve_skill_deps(skill_name: str) -> None:
            if skill_name in final_skill_names:
                return
            meta = skill_metadata.get(skill_name, {})
            deps = meta.get("depends_on", [])
            for dep in deps:
                resolve_skill_deps(dep)
            final_skill_names.add(skill_name)

        # Initial selection logic (Phase 11/17)
        # Default skills for all projects
        resolve_skill_deps("env_context")

        # Adaptive selection based on keywords
        if any(kw in keywords for kw in ["security", "vault", "secrets"]):
            resolve_skill_deps("secrets_manager")
        if any(kw in keywords for kw in ["git", "github", "gitlab"]):
            resolve_skill_deps("git_automation")
        if any(kw in keywords for kw in ["bridge", "handoff", "multi-repo"]):
            resolve_skill_deps("bridge")

        # Add resolved skills to write_queue
        for skill_name in final_skill_names:
            if skill_name in skill_contents:
                for skill_path, content in skill_contents[skill_name]:
                    path = os.path.join(base_dir, AGENT_DIR, "skills", skill_path)
                    final_content = custom.get("skills", {}).get(skill_path, content)
                    write_queue.append((path, final_content))

        # Phase 17: Personality Packs
        if personality:
            personality_rule = f"# Personality: {personality.capitalize()}\n"
            if personality == "startup":
                personality_rule += "1. **Speed:** Prioritize functional code over exhaustive documentation.\n2. **Pragmatism:** Use 80/20 rule for testing.\n"
            elif personality == "enterprise":
                personality_rule += "1. **Compliance:** Every change MUST have an ADR in `DECISIONS.md`.\n2. **Quality:** 100% test coverage mandatory for new features.\n"

            personality_path = os.path.join(base_dir, AGENT_DIR, "rules", "personality.md")
            write_queue.append((personality_path, personality_rule))

        # Phase 20: Declarative Governance
        for filename, content in AGENT_CONFIGS.items():
            path = os.path.join(base_dir, AGENT_DIR, filename)
            write_queue.append((path, content))

        # Memory & Protocols
        for filename, content in AGENT_MEMORIES.items():
            path = os.path.join(base_dir, AGENT_DIR, "memory", filename)
            write_queue.append((path, content))

        scratchpad_path = os.path.join(base_dir, AGENT_DIR, "memory", "scratchpad.md")
        write_queue.append((scratchpad_path, AntigravityBuilder.build_scratchpad(keywords, False)))
        write_queue.append((os.path.join(base_dir, AGENT_DIR, "memory", "graveyard.md"), GRAVEYARD_TEMPLATE))
        write_queue.append((os.path.join(base_dir, AGENT_DIR, "memory", "evolution.md"), EVOLUTION_TEMPLATE))

        # Sentinel
        write_queue.append((os.path.join(base_dir, "scripts", "sentinel.py"), SENTINEL_PY))

        # EXECUTOR
        def _execute_write(item: tuple[str, str]) -> None:
            path, content = item
            AntigravityEngine.write_file(path, content, exist_ok=safe_mode)

        with ThreadPoolExecutor() as executor:
            executor.map(_execute_write, write_queue)

    @staticmethod
    def generate_ecosystem_files(
        base_dir: str,
        ide: str | None = None,
        ci: str | None = None,
        docker: bool = False,
        project_name: str = "project",
    ) -> None:
        """Phase 13: IDE & CI Ecosystem - generates platform-specific configs."""
        write_queue = []

        # IDE Configs
        if ide == "jetbrains":
            write_queue.append(
                (
                    os.path.join(base_dir, ".idea", f"{project_name}.iml"),
                    AntigravityEngine.get_template("ide", "jetbrains_modules.xml"),
                )
            )
        elif ide == "neovim":
            write_queue.append(
                (
                    os.path.join(base_dir, ".config", "nvim", "lua", "plugins", "lsp.lua"),
                    AntigravityEngine.get_template("ide", "neovim.lua"),
                )
            )
        elif ide == "zed":
            write_queue.append(
                (os.path.join(base_dir, ".zed", "tasks.json"), AntigravityEngine.get_template("ide", "zed_tasks.json"))
            )
        elif ide == "fleet":
            write_queue.append(
                (os.path.join(base_dir, ".fleet", "run.json"), AntigravityEngine.get_template("ide", "fleet_run.json"))
            )

        # CI/CD Pipelines
        if ci == "gitlab":
            write_queue.append(
                (
                    os.path.join(base_dir, ".gitlab-ci.yml"),
                    AntigravityEngine.get_template("pipelines", "gitlab-ci.yml"),
                )
            )
        elif ci == "azure":
            write_queue.append(
                (
                    os.path.join(base_dir, "azure-pipelines.yml"),
                    AntigravityEngine.get_template("pipelines", "azure-pipelines.yml"),
                )
            )

        # Docker
        if docker:
            write_queue.append(
                (
                    os.path.join(base_dir, "docker-compose.yml"),
                    AntigravityEngine.get_template("pipelines", "docker-compose.yml"),
                )
            )

        # Execute Parallel Writes
        from concurrent.futures import ThreadPoolExecutor

        def _execute_write(item: tuple[str, str]) -> None:
            path, content = item
            AntigravityEngine.write_file(path, content, exist_ok=True)

        if write_queue:
            with ThreadPoolExecutor() as executor:
                executor.map(_execute_write, write_queue)

    @staticmethod
    def _resolve_blueprint(blueprint: str | None) -> dict:
        """Helper to resolve blueprint data from name or URL, with support for inheritance."""
        if not blueprint:
            return {}

        data = {}
        if blueprint.startswith("http://") or blueprint.startswith("https://"):
            data = AntigravityEngine.fetch_remote_blueprint(blueprint) or {}
        else:
            data = BLUEPRINTS.get(blueprint, {})

        # v1.8.0 Blueprint Inheritance
        parent_name = data.get("base")
        if parent_name:
            parent_data = AntigravityGenerator._resolve_blueprint(parent_name)
            # Merge parent data with child data
            # Lists (dirs, stack, rules) are combined
            for key in ["dirs", "stack", "rules"]:
                data[key] = list(set(parent_data.get(key, []) + data.get(key, [])))

        return data

    @staticmethod
    def _generate_dependency_doc(base_dir: str) -> None:
        """Phase 11: Dependency Graph Awareness - scans for lockfiles."""
        base = Path(base_dir)
        deps = []

        mapping = {
            "requirements.txt": "Python (pip)",
            "package.json": "Node.js (npm/yarn)",
            "go.mod": "Go",
            "Cargo.toml": "Rust",
            "composer.json": "PHP",
            "Gemfile": "Ruby",
            "build.gradle": "Java (Gradle)",
            "pom.xml": "Java (Maven)",
            "pyproject.toml": "Python (Poetry/Ruff)",
        }

        found = False
        for file, lang in mapping.items():
            if (base / file).exists():
                deps.append(f"- **{file}**: Detects {lang} ecosystem.")
                found = True

        if not found:
            return

        content = "# 📦 Project Dependency Manifest\n\n"
        content += "This project uses the following package managers and dependency definitions:\n\n"
        content += "\n".join(deps)
        content += "\n\n---\n*Generated by Antigravity v1.8.0 Dependency Awareness Protocol*"

        AntigravityEngine.write_file(os.path.join(base_dir, "docs", "DEPENDENCIES.md"), content, exist_ok=True)

    @staticmethod
    def _generate_agent_map(base_dir: str, project_name: str, stack: list[str]) -> None:
        """Phase 21: Semantic Repository Mapping - helps agents understand the repo layout."""
        semantic_hints = {
            ".agent/manifest.json": "Core agent protocol and project metadata.",
            ".agent/rules/": "Agent behavioral constraints and coding standards.",
            ".agent/workflows/": "Step-by-step guides for common dev tasks.",
            ".agent/skills/": "Executable tools and automation scripts.",
            ".agent/tools.json": "Declarative tool permissions and guardrails.",
            "docs/": "Architectural manifest and decision records.",
            "tests/": "Pytest suite for quality assurance.",
            "src/": "Primary source code directory.",
            ".github/workflows/": "CI/CD pipeline definitions.",
            ".idx/dev.nix": "Google Project IDX environment config.",
            "scripts/sentinel.py": "Security and compliance watchdog.",
            "README.md": "Human-readable project overview.",
            "DEPENDENCIES.md": "Project dependency graph and tech stack overview.",
            "pyproject.toml": "Python package metadata and dependency list.",
            "package.json": "Node.js dependency and script manifest.",
        }

        from typing import Any

        import yaml

        content: dict[str, Any] = {
            "project": project_name,
            "version": VERSION,
            "intent": "Agent-First High-Reasoning Repository",
            "stack": stack,
            "semantic_map": {},
        }

        # Scan what actually exists
        for path, hint in semantic_hints.items():
            if os.path.exists(os.path.join(base_dir, path)):
                content["semantic_map"][path] = hint

        map_path = os.path.join(base_dir, "AGENT_MAP.yaml")
        AntigravityEngine.write_file(map_path, yaml.dump(content, sort_keys=False), exist_ok=True)

    @staticmethod
    def generate_community_standards(base_dir: str, safe_mode: bool = False) -> None:
        """Generates standard legal and community files."""
        files = {
            CHANGELOG_FILE: CHANGELOG_TEMPLATE,
            CONTRIBUTING_FILE: CONTRIBUTING_TEMPLATE,
            AUDIT_FILE: AUDIT_TEMPLATE,
            SECURITY_FILE: SECURITY_TEMPLATE,
            CODE_OF_CONDUCT_FILE: CODE_OF_CONDUCT_TEMPLATE,
            "docs/ARCHITECTURE.md": DOC_TEMPLATES.get("architecture.md", ""),
            "docs/DECISIONS.md": DOC_TEMPLATES.get("decisions.md", ""),
            "docs/TESTING.md": DOC_TEMPLATES.get("testing.md", ""),
        }
        for filename, content in files.items():
            AntigravityEngine.write_file(os.path.join(base_dir, filename), content, exist_ok=safe_mode)

    @staticmethod
    def _handle_safe_mode(project_name: str, base_dir: str, safe_mode: bool | None) -> bool | None:
        """Handles user interaction for existing project directories."""
        if safe_mode is None and os.path.exists(base_dir):
            print(f"\n⚠️  Project '{project_name}' already exists.")
            choice = input("Select mode: [U]pdate (Safe) / [O]verwrite (Risky) / [C]ancel: ").lower()

            if choice == "u":
                print("🛡️  Safe Update Mode Active: Only missing files will be created.")
                return True
            elif choice == "o":
                confirm = input("💥 WARNING: This will overwrite files. Type 'yes' to confirm: ")
                if confirm.lower() != "yes":
                    return None  # Cancel
                return False
            else:
                return None  # Cancel
        elif safe_mode is None:
            return False
        return safe_mode

    @staticmethod
    def _get_directory_structure(blueprint_data: dict) -> list[str]:
        """Returns the list of directories to create."""
        directories = [
            "src",
            "tests",
            "docs/imported",
            "context/raw",
            f"{AGENT_DIR}/rules",
            f"{AGENT_DIR}/workflows",
            f"{AGENT_DIR}/skills",
            f"{AGENT_DIR}/memory",
            f"{AGENT_DIR}/skills/git_automation",
            f"{AGENT_DIR}/skills/secrets_manager",
            f"{AGENT_DIR}/skills/bridge",
            f"{AGENT_DIR}/skills/env_context",
            "scripts",
        ]
        if blueprint_data:
            directories.extend(blueprint_data.get("dirs", []))
        return directories

    @staticmethod
    def _inherit_global_rules(base_dir: str, safe_mode: bool) -> None:
        """Copies global rules from ~/.antigravity/rules if they exist."""
        global_agent_rules = Path.home() / ".antigravity" / "rules"
        if global_agent_rules.exists():
            logging.info("🌐 Inheriting Global Rules from ~/.antigravity")
            for rule_file in global_agent_rules.glob("*.md"):
                dest_path = os.path.join(base_dir, AGENT_DIR, "rules", f"global_{rule_file.name}")
                with open(rule_file, encoding="utf-8") as rf:
                    AntigravityEngine.write_file(dest_path, rf.read(), exist_ok=safe_mode)

    @staticmethod
    def _generate_core_config_files(base_dir: str, project_name: str, final_stack: list[str], safe_mode: bool) -> None:
        """Generates core configuration files like .gitignore, README, env, etc."""
        AntigravityEngine.write_file(
            os.path.join(base_dir, GITIGNORE_FILE), AntigravityBuilder.build_gitignore(final_stack), exist_ok=True
        )

        AntigravityEngine.write_file(
            os.path.join(base_dir, README_FILE),
            PROFESSIONAL_README_TEMPLATE.format(project_name=project_name, tech_stack=", ".join(final_stack)),
            exist_ok=True,
        )
        AntigravityEngine.write_file(os.path.join(base_dir, ENV_EXAMPLE_FILE), "API_KEY=\nDB_URL=", exist_ok=safe_mode)
        # Bridge and Architecture docs
        AntigravityEngine.write_file(
            os.path.join(base_dir, AGENT_DIR, "skills", "bridge", "bridge.py"),
            AGENT_SKILLS["bridge/bridge.py"],
            exist_ok=safe_mode,
        )
        AntigravityEngine.write_file(
            os.path.join(base_dir, "docs", "ARCHITECTURE.md"),
            MERMAID_PROJECT_MAP.format(project_name=project_name),
            exist_ok=safe_mode,
        )
        AntigravityEngine.write_file(
            os.path.join(base_dir, "context", "links.md"),
            AntigravityBuilder.build_links(project_name),
            exist_ok=safe_mode,
        )
        # 4. Semantic RAG Index
        AntigravityEngine.write_file(
            os.path.join(base_dir, "docs", "imported", "INDEX.md"),
            AntigravityBuilder.build_docs_index(os.path.join(base_dir, "docs", "imported")),
            exist_ok=True,
        )
        # Bootstrap Guide
        AntigravityEngine.write_file(
            os.path.join(base_dir, BOOTSTRAP_FILE),
            """# Agent Start Guide

1. **Protocol:** Review `.agent/manifest.json` for project structure.
2. **Context:** Read `.agent/memory/scratchpad.md` and `.agent/memory/evolution.md`.
3. **Safety:** Ensure `scripts/sentinel.py` is running for monitoring.
4. **Action:** Use `/plan` to break down tasks or `/bootstrap` for code generation.
5. **Standards:** Follow the v2.0.0 Agent Protocol in `.agent/rules/`.
""",
            exist_ok=safe_mode,
        )

    @staticmethod
    def _generate_license(base_dir: str, license_type: str, safe_mode: bool) -> None:
        """Generates the LICENSE file."""
        license_content = LICENSE_TEMPLATES.get(license_type, LICENSE_TEMPLATES["mit"])
        if license_type == "mit":
            license_content = license_content.format(year=datetime.now().year, author="pkeffect")
        AntigravityEngine.write_file(os.path.join(base_dir, LICENSE_FILE), license_content, exist_ok=safe_mode)

    @staticmethod
    def _setup_git_hooks(base_dir: str) -> None:
        """Sets up the post-commit git hook."""
        git_dir = os.path.join(base_dir, ".git")
        if os.path.exists(git_dir):
            hook_path = os.path.join(git_dir, "hooks", "post-commit")
            hook_content = "#!/usr/bin/env python3\n# Antigravity Time-Travel hook\nimport os\nprint('🌌 Antigravity: Syncing session memory...')\n"
            try:
                with open(hook_path, "w", encoding="utf-8") as hf:
                    hf.write(hook_content)
                os.chmod(hook_path, 0o755)
            except Exception:
                pass

    @staticmethod
    def _apply_blueprint_rules(base_dir: str, blueprint_data: dict) -> None:
        """Applies agent rules defined in the blueprint."""
        if not blueprint_data:
            return

        for rule in blueprint_data.get("rules", []):
            if rule in AGENT_RULES:
                AntigravityEngine.write_file(
                    os.path.join(base_dir, AGENT_DIR, "rules", rule),
                    AGENT_RULES[rule],
                    exist_ok=False,
                )

    @staticmethod
    def _generate_health_badge(base_dir: str, project_name: str) -> None:
        """Phase 17: Generates a project health badge (local SVG)."""
        badge_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="120" height="20">
  <linearGradient id="b" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <mask id="a">
    <rect width="120" height="20" rx="3" fill="#fff"/>
  </mask>
  <g mask="url(#a)">
    <path fill="#555" d="M0 0h60v20H0z"/>
    <path fill="#4c1" d="M60 0h60v20H60z"/>
    <path fill="url(#b)" d="M0 0h120v20H0z"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
    <text x="30" y="15" fill="#010101" fill-opacity=".3">architect</text>
    <text x="30" y="14">architect</text>
    <text x="90" y="15" fill="#010101" fill-opacity=".3">v{VERSION}</text>
    <text x="90" y="14">v{VERSION}</text>
    <!-- Project: {project_name} -->
  </g>
</svg>"""
        output_path = os.path.join(base_dir, "docs", "health_badge.svg")
        AntigravityEngine.write_file(output_path, badge_svg, exist_ok=True)

    @staticmethod
    def generate_project(
        project_name: str,
        keywords: list[str],
        brain_dump_path: str | None = None,
        safe_mode: bool | None = None,
        custom_templates: dict[str, dict[str, str]] | None = None,
        license_type: str = "mit",
        blueprint: str | None = None,
        personality: str | None = None,
    ) -> bool:
        """
        Main project generation logic (v1.6.0 Orchestration).
        """
        base_dir = os.path.join(os.getcwd(), project_name)

        # Handle safe_mode
        safe_mode_result = AntigravityGenerator._handle_safe_mode(project_name, base_dir, safe_mode)
        if safe_mode_result is None:
            return False
        safe_mode = safe_mode_result

        logging.info(f"🚀 Constructing '{project_name}' (v{VERSION})...")

        # Setup logging in target directory
        AntigravityEngine.setup_logging(base_dir)

        # 1. Blueprint Application (Ancestry Override)
        blueprint_data = AntigravityGenerator._resolve_blueprint(blueprint)

        if blueprint_data:
            logging.info(f"💎 Applying Blueprint: {blueprint_data.get('name', blueprint)}")
            keywords.extend(blueprint_data.get("stack", []))

        # Create directory structure
        directories = AntigravityGenerator._get_directory_structure(blueprint_data)
        for d in directories:
            AntigravityEngine.create_folder(os.path.join(base_dir, d))

        # Process brain dump
        detected_stack: list[str] = []
        if brain_dump_path:
            detected_stack = AntigravityAssimilator.process_brain_dump(brain_dump_path, base_dir)

        # Merge keywords
        final_stack = list(set(keywords + detected_stack))
        if not final_stack:
            final_stack = ["linux"]
        logging.info(f"⚙️  Final Tech Stack: {', '.join(final_stack)}")

        # 2. Inheritance: Copy global rules
        AntigravityGenerator._inherit_global_rules(base_dir, safe_mode)

        # Generate configuration files
        AntigravityGenerator._generate_core_config_files(base_dir, project_name, final_stack, safe_mode)

        # Generate License
        AntigravityGenerator._generate_license(base_dir, license_type, safe_mode)

        # Community Standards
        AntigravityGenerator.generate_community_standards(base_dir, safe_mode=safe_mode)

        # Phase 11: Dependency Graph Awareness
        AntigravityGenerator._generate_dependency_doc(base_dir)

        # Phase 15: API Documentation for web stacks
        web_keywords = ["fastapi", "nextjs", "react", "node", "go-fiber"]
        if any(kw in final_stack for kw in web_keywords):
            api_doc = DOC_TEMPLATES.get("api.md", "").format(project_name=project_name, stack=", ".join(final_stack))
            AntigravityEngine.write_file(os.path.join(base_dir, "docs", "API.md"), api_doc, exist_ok=safe_mode)

        # Agent files
        AntigravityGenerator.generate_agent_files(
            base_dir,
            project_name,
            final_stack,
            safe_mode=safe_mode,
            custom_templates=custom_templates,
            personality=personality,
        )

        # Phase 17: Health Badge
        AntigravityGenerator._generate_health_badge(base_dir, project_name)

        # Phase 21: Semantic Repository Map
        AntigravityGenerator._generate_agent_map(base_dir, project_name, final_stack)

        # Apply Blueprint Rules
        AntigravityGenerator._apply_blueprint_rules(base_dir, blueprint_data)

        # Plugins: Trigger post-generation hooks
        PluginManager.load_plugins()
        PluginManager.trigger(
            "on_generation_complete",
            project_name=project_name,
            base_dir=base_dir,
            final_stack=final_stack,
            safe_mode=safe_mode,
        )

        # Time-Travel: Git Initialization hook
        AntigravityGenerator._setup_git_hooks(base_dir)

        print(f"\n✅ Project '{project_name}' ready (v{VERSION})!")
        print(f"📂 Location: {os.path.abspath(base_dir)}\n")
        return True
