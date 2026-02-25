import json
import os
from pathlib import Path
from typing import Any

# Unused constants are available via .constants if needed,
# but we remove them from here to satisfy linter.

TEMPLATE_BASE = Path(__file__).parent / "templates"

class LazyTemplateDict(dict):
    """Lazily loads template files from a specific category directory."""
    def __init__(self, category: str) -> None:
        self.category = category
        self._data: dict | None = None

    def _load(self) -> None:
        if self._data is None:
            self._data = {}
            cat_path = TEMPLATE_BASE / self.category
            if not cat_path.exists():
                return

            # Special handling for skills which can have subdirectories
            if self.category == "skills":
                for root, _, files in os.walk(cat_path):
                    for file in files:
                        full_path = Path(root) / file
                        rel_path = full_path.relative_to(cat_path)
                        key = str(rel_path).replace("\\", "/")
                        self._data[key] = full_path.read_text(encoding="utf-8")
            else:
                for item in cat_path.iterdir():
                    if item.is_file():
                        content = item.read_text(encoding="utf-8")
                        # Only parse JSON and use stem for blueprints
                        if item.suffix == ".json" and self.category == "blueprints":
                            self._data[item.stem] = json.loads(content)
                        else:
                            self._data[item.name] = content

    def __getitem__(self, key: str) -> Any:
        self._load()
        return self._data[key]

    def get(self, key: str, default: Any | None = None) -> Any:
        self._load()
        return self._data.get(key, default)

    def items(self) -> Any:
        self._load()
        return self._data.items()

    def values(self) -> Any:
        self._load()
        return self._data.values()

    def keys(self) -> Any:
        self._load()
        return self._data.keys()

    def __iter__(self) -> Any:
        self._load()
        return iter(self._data)

    def __len__(self) -> int:
        self._load()
        return len(self._data)

    def __contains__(self, key: str) -> bool:
        self._load()
        return key in self._data

def load_common(name: str) -> str:
    path = TEMPLATE_BASE / "common" / name
    return path.read_text(encoding="utf-8") if path.exists() else ""

# --- Mapping Dicts (Lazy) ---
AGENT_RULES = LazyTemplateDict("rules")
AGENT_WORKFLOWS = LazyTemplateDict("workflows")
AGENT_SKILLS = LazyTemplateDict("skills")
AGENT_MEMORIES = LazyTemplateDict("memory")
AGENT_CONFIGS = LazyTemplateDict("agent")
BLUEPRINTS = LazyTemplateDict("blueprints")
DOC_TEMPLATES = LazyTemplateDict("docs")

# --- Common Templates (Eager/Loaded once) ---
BASE_GITIGNORE = load_common("gitignore")
CHANGELOG_TEMPLATE = load_common("changelog.md")
CONTRIBUTING_TEMPLATE = load_common("contributing.md")
AUDIT_TEMPLATE = load_common("audit.md")
SECURITY_TEMPLATE = load_common("security.md")
CODE_OF_CONDUCT_TEMPLATE = load_common("coc.md")
PROFESSIONAL_README_TEMPLATE = load_common("readme.md")
SENTINEL_PY = load_common("sentinel.py")
LINKS_TEMPLATE = load_common("links.md")
GRAVEYARD_TEMPLATE = load_common("graveyard.md")
EVOLUTION_TEMPLATE = load_common("evolution.md")

# Static legacy placeholders required for backward compatibility
AGENT_MANIFEST_TEMPLATE = ""

def _load_json_resource(category: str, name: str) -> dict:
    path = TEMPLATE_BASE / category / name
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

GITIGNORE_MAP = _load_json_resource("common", "gitignore_map.json")
LICENSE_TEMPLATES = _load_json_resource("common", "licenses.json")
MERMAID_PROJECT_MAP = ""
