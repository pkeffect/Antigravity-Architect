import difflib
import hashlib
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from antigravity_architect.resources.constants import PRESETS_DIR


class AntigravityEngine:
    """
    Low-level utilities for file system operations and input validation.

    This class contains all the foundational operations needed by the Antigravity
    Architect, including sanitization, validation, file I/O, and logging setup.
    All methods are static as they don't require instance state.
    """

    @staticmethod
    def setup_logging(log_dir: str | None = None) -> None:
        """Configure logging to both file and stdout."""
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
            log_path = os.path.join(log_dir, "antigravity_setup.log")
        else:
            log_path = os.path.join(tempfile.gettempdir(), "antigravity_setup.log")

        # Use force=True to allow re-configuring logging (Python 3.8+)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(log_path, mode="w", encoding="utf-8"),
                logging.StreamHandler(sys.stdout),
            ],
            force=True,
        )

    @staticmethod
    def sanitize_name(name: str | None) -> str:
        """
        Ensures project name is valid and safe for file system.

        Prevents path traversal attacks and invalid characters.
        """
        if not name:
            return "antigravity-project"

        clean = re.sub(r"\s+", "_", name.strip())
        clean = re.sub(r"[^a-zA-Z0-9_\-]", "", clean)

        # Security: Prevent path traversal attempts
        if ".." in clean or clean.startswith(("/", "\\")):
            logging.warning("⚠️ Potential path traversal detected, using default name")
            return "antigravity-project"

        # Security: Prevent empty result after sanitization
        if not clean:
            return "antigravity-project"

        return clean

    @staticmethod
    def slugify_title(title: str) -> str:
        """
        Converts a markdown header or arbitrary title into a safe filename slug.

        Handles special characters, unicode, and edge cases for cross-platform safety.
        Used primarily by the Assimilator for Brain Dump section titles.
        """
        # Remove markdown header markers
        slug = re.sub(r"^#+\s*", "", title)
        # Convert to lowercase and replace spaces/special chars with underscores
        slug = re.sub(r"[^a-zA-Z0-9]", "_", slug.lower())
        # Collapse multiple underscores
        slug = re.sub(r"_+", "_", slug)
        # Strip leading/trailing underscores
        slug = slug.strip("_")
        # Ensure non-empty and reasonable length
        if not slug:
            slug = "untitled"
        return slug[:50]

    @staticmethod
    def parse_keywords(input_str: str | None) -> list[str]:
        """Converts comma/space separated string to list of lowercase keywords."""
        if not input_str:
            return []
        raw = re.split(r"[,\s]+", input_str)
        return [w.lower().strip() for w in raw if w.strip()]

    @staticmethod
    def validate_file_path(filepath: str | None) -> bool:
        """
        Validates that a file path is safe and accessible.

        Returns True if the path is a valid, readable file.
        """
        if not filepath:
            return False

        # Resolve to absolute path and check it's a regular file
        try:
            abs_path = os.path.abspath(filepath)
            if not os.path.isfile(abs_path):
                logging.warning(f"⚠️ Not a valid file: {filepath}")
                return False
            if not os.access(abs_path, os.R_OK):
                logging.warning(f"⚠️ File not readable: {filepath}")
                return False
            return True
        except (OSError, ValueError) as e:
            logging.warning(f"⚠️ Invalid file path: {e}")
            return False

    @staticmethod
    def get_diff(actual: str, expected: str) -> str:
        """Returns a unified diff between two strings for drift analysis."""
        return "\n".join(
            difflib.unified_diff(
                actual.splitlines(), expected.splitlines(), fromfile="actual", tofile="expected", lineterm=""
            )
        )

    @staticmethod
    def _get_checksum(content: str) -> str:
        """Returns SHA-256 checksum of normalized content."""
        # Normalize line endings to avoid OS-specific checksum drift
        normalized = content.strip().replace("\r\n", "\n")
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    @staticmethod
    def write_file(path: str, content: str, exist_ok: bool = False, smart_overwrite: bool = True) -> bool:
        """
        Writes a new file, creating parent directories as needed.

        Args:
            path: Destination path
            content: File content
            exist_ok: If True, skip if file exists (Legacy Safe Mode).
            smart_overwrite: If True, only overwrite if content hash differs.

        Returns True on success/creation, False on failure or skipped.
        """
        try:
            if exist_ok and os.path.exists(path):
                logging.info(f"⏭️  Skipped (Exists): {path}")
                return True

            if smart_overwrite and os.path.exists(path):
                with open(path, encoding="utf-8") as f:
                    existing = f.read()

                if AntigravityEngine._get_checksum(existing) == AntigravityEngine._get_checksum(content):
                    logging.info(f"✨ Unchanged: {path}")
                    return True

            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content.strip() + "\n")

            icon = "✅" if not os.path.exists(path) else "📝"
            logging.info(f"{icon} Wrote: {path}")
            return True
        except OSError as e:
            logging.error(f"❌ Error writing {path}: {e}")
            return False

    @staticmethod
    def append_file(path: str, content: str) -> bool:
        """
        Appends content to a file (used for Assimilation).

        Returns True on success, False on failure.
        """
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "a", encoding="utf-8") as f:
                f.write("\n\n" + content.strip() + "\n")
            logging.info(f"🔗 Appended to: {path}")
            return True
        except OSError as e:
            logging.error(f"❌ Error appending {path}: {e}")
            return False

    @staticmethod
    def get_template(category: str, name: str) -> str:
        """Retrieves a template from the resource manager."""
        from antigravity_architect.resources.templates import (
            AGENT_MEMORIES,
            AGENT_RULES,
            AGENT_SKILLS,
            AGENT_WORKFLOWS,
            BLUEPRINTS,
            DOC_TEMPLATES,
            LazyTemplateDict,
        )

        mapping = {
            "rules": AGENT_RULES,
            "workflows": AGENT_WORKFLOWS,
            "skills": AGENT_SKILLS,
            "memory": AGENT_MEMORIES,
            "docs": DOC_TEMPLATES,
            "blueprints": BLUEPRINTS,
        }

        # Pipelines is special as it's not a global LazyTemplateDict yet
        if category == "pipelines":
            try:
                pipeline_val = LazyTemplateDict("pipelines").get(name, "")
                return str(pipeline_val)
            except Exception:
                return ""

        cat_dict = mapping.get(category)
        if cat_dict:
            return str(cat_dict.get(name, ""))
        return ""

    @staticmethod
    def create_folder(path: str) -> bool:
        """
        Creates a folder and adds .gitkeep so Git tracks it.

        Returns True on success, False on failure.
        """
        try:
            os.makedirs(path, exist_ok=True)
            gitkeep_path = os.path.join(path, ".gitkeep")
            with open(gitkeep_path, "w") as f:
                f.write("")
            logging.info(f"📁 Directory: {path}")
            return True
        except OSError as e:
            logging.error(f"❌ Error creating folder {path}: {e}")
            return False

    @staticmethod
    def save_preset(name: str, args: dict) -> bool:
        """Saves current CLI arguments as a named preset."""
        try:
            path = PRESETS_DIR / f"{name}.json"
            os.makedirs(path.parent, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(args, f, indent=4)
            logging.info(f"💾 Preset saved: {name}")
            return True
        except Exception as e:
            logging.error(f"❌ Error saving preset {name}: {e}")
            return False

    @staticmethod
    def load_preset(name: str) -> dict | None:
        """Loads a preset by name."""
        try:
            path = PRESETS_DIR / f"{name}.json"
            if not path.exists():
                logging.error(f"❌ Preset not found: {name}")
                return None
            with open(path, encoding="utf-8") as f:
                data: dict[Any, Any] = json.load(f)
                return data
        except Exception as e:
            logging.error(f"❌ Error loading preset {name}: {e}")
            return None

    @staticmethod
    def list_presets() -> list[str]:
        """Lists available presets."""
        try:
            if not PRESETS_DIR.exists():
                return []
            return [f.stem for f in PRESETS_DIR.glob("*.json")]
        except Exception as e:
            logging.error(f"❌ Error listing presets: {e}")
            return []

    @staticmethod
    def fetch_remote_blueprint(url: str) -> dict | None:
        """
        Fetches a remote blueprint via git clone.
        Expects a 'antigravity_blueprint.json' in the repo root.
        """
        temp_dir = Path(tempfile.mkdtemp(prefix="antigravity_blueprint_"))
        try:
            logging.info(f"⬇️  Fetching remote blueprint: {url}")
            subprocess.check_call(
                ["git", "clone", "--depth", "1", url, str(temp_dir)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            blueprint_path = temp_dir / "antigravity_blueprint.json"
            if not blueprint_path.exists():
                logging.error("❌ Remote repo missing 'antigravity_blueprint.json'")
                return None

            with open(blueprint_path, encoding="utf-8") as f:
                data: dict[Any, Any] = json.load(f)
                logging.info(f"✅ Loaded remote blueprint: {data.get('name', 'Unknown')}")
                return data

        except subprocess.CalledProcessError:
            logging.error(f"❌ Failed to clone {url}")
            return None
        except Exception as e:
            logging.error(f"❌ Error fetching blueprint: {e}")
            return None
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    @staticmethod
    def fetch_remote_blueprints(url: str = "https://raw.githubusercontent.com/antigravity/market/main/index.json") -> dict:
        """Phase 17: Fetches the Blueprint Marketplace Index."""
        try:
            import urllib.request
            with urllib.request.urlopen(url, timeout=5) as response:
                result = json.loads(response.read().decode("utf-8"))
                if isinstance(result, dict):
                    return result
                return {}
        except Exception:
            # Fallback to local if remote is unreachable
            return {}

    @staticmethod
    def get_all_blueprints() -> dict:
        """Merges local and remote blueprints."""
        from antigravity_architect.resources.templates import BLUEPRINTS
        local = dict(BLUEPRINTS.items())
        # Try to fetch remote (async-like or with timeout)
        remote = AntigravityEngine.fetch_remote_blueprints()
        local.update(remote)
        return local
