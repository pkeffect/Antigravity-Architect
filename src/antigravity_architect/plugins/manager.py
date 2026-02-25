
import importlib.util
import logging
from pathlib import Path
from typing import Any, ClassVar


class PluginManager:
    """Discovers, loads, and executes Antigravity sidecar plugins."""

    _plugins: ClassVar[dict[str, Any]] = {}

    @classmethod
    def load_plugins(cls, project_dir: str | None = None) -> None:
        """Looks for ag_plugin_*.py files in the tool directory or project directory."""
        # Find the root plugins directory (same as this file)
        root_plugins_dir = Path(__file__).parent

        search_dirs = [root_plugins_dir]
        if project_dir:
            search_dirs.append(Path(project_dir) / "ag_plugins")

        for d in search_dirs:
            if not d.exists() or not d.is_dir():
                continue
            for plugin_file in d.glob("ag_plugin_*.py"):
                plugin_name = plugin_file.stem
                if plugin_name in cls._plugins:
                    continue

                try:
                    spec = importlib.util.spec_from_file_location(plugin_name, plugin_file)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        cls._plugins[plugin_name] = module
                        logging.debug(f"Loaded sidecar plugin: {plugin_name}")
                except Exception as e:
                    logging.error(f"Failed to load plugin {plugin_file.name}: {e}")

    @classmethod
    def display_loaded_plugins(cls) -> list[str]:
        """Returns a list of descriptions for loaded plugins."""
        info = []
        for name, module in cls._plugins.items():
            desc = getattr(module, "PLUGIN_DESCRIPTION", "No description provided.")
            info.append(f"  * {name}: {desc}")
        return info

    @classmethod
    def trigger(cls, hook_name: str, **kwargs: Any) -> dict[str, Any]:
        """
        Executes a specific hook on all loaded plugins.
        Returns a dictionary of plugin_name -> result.
        """
        results = {}
        for name, module in cls._plugins.items():
            if hasattr(module, hook_name):
                hook = getattr(module, hook_name)
                try:
                    logging.debug(f"Triggering {hook_name} on {name}")
                    results[name] = hook(**kwargs)
                except Exception as e:
                    logging.error(f"Plugin {name} failed on hook {hook_name}: {e}")
        return results
