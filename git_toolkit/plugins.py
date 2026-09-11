from __future__ import annotations

import abc
import importlib.metadata
import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

PLUGIN_API_VERSION = "1"


class Plugin(abc.ABC):
    """Stable extension contract for Git Toolkit plugins."""

    api_version = PLUGIN_API_VERSION
    name: str | None = None

    @abc.abstractmethod
    def register_commands(self, subparsers: Any) -> None:
        """Register CLI commands."""

    def run_command(self, args: Any) -> bool:
        return False

    def run_hook(self, hook_name: str, env: dict[str, str] | None = None) -> bool:
        del hook_name, env
        return True


class PluginManager:
    """Discover package entry-point plugins and optionally project-local plugins."""

    ENTRY_POINT_GROUP = "git_toolkit.plugins"

    def __init__(
        self,
        local_plugin_dir: Path | None = None,
        allow_local_plugins: bool = False,
    ) -> None:
        self.plugins: list[Plugin] = []
        self.errors: list[str] = []
        self.local_plugin_dir = local_plugin_dir or Path(".git-toolkit") / "plugins"
        self.allow_local_plugins = allow_local_plugins
        self._load_entry_points()
        if allow_local_plugins:
            self._load_local_plugins()

    def _accept(self, candidate: Any, source: str) -> None:
        try:
            instance = candidate() if isinstance(candidate, type) else candidate
            if not isinstance(instance, Plugin):
                raise TypeError("plugin does not inherit from Plugin")
            if str(getattr(instance, "api_version", "")) != PLUGIN_API_VERSION:
                raise ValueError(
                    f"plugin API {getattr(instance, 'api_version', None)!r} is incompatible "
                    f"with API {PLUGIN_API_VERSION}"
                )
            self.plugins.append(instance)
        except Exception as exc:
            self.errors.append(f"{source}: {exc}")

    def _load_entry_points(self) -> None:
        try:
            points = importlib.metadata.entry_points()
            selected = (
                points.select(group=self.ENTRY_POINT_GROUP)
                if hasattr(points, "select")
                else points.get(self.ENTRY_POINT_GROUP, [])
            )
            for entry_point in selected:
                try:
                    self._accept(entry_point.load(), f"entry point {entry_point.name}")
                except Exception as exc:
                    self.errors.append(f"entry point {entry_point.name}: {exc}")
        except Exception as exc:
            self.errors.append(f"entry point discovery: {exc}")

    def _load_module(self, path: Path) -> ModuleType:
        module_name = f"git_toolkit_local_plugin_{path.stem}"
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            raise ImportError(f"cannot load {path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module

    def _load_local_plugins(self) -> None:
        if not self.local_plugin_dir.exists():
            return
        for path in sorted(self.local_plugin_dir.glob("*.py")):
            if path.name.startswith("_"):
                continue
            try:
                module = self._load_module(path)
                if not hasattr(module, "plugin"):
                    raise AttributeError("module must expose 'plugin'")
                self._accept(module.plugin, f"local plugin {path}")
            except Exception as exc:
                self.errors.append(f"local plugin {path}: {exc}")

    def register_all_commands(self, subparsers: Any) -> None:
        for plugin in self.plugins:
            plugin.register_commands(subparsers)

    def handle_command(self, args: Any) -> bool:
        for plugin in self.plugins:
            if plugin.run_command(args):
                return True
        return False

    def diagnostics(self) -> dict[str, Any]:
        return {
            "api_version": PLUGIN_API_VERSION,
            "local_plugins_enabled": self.allow_local_plugins,
            "plugins": [
                getattr(plugin, "name", None) or plugin.__class__.__name__ for plugin in self.plugins
            ],
            "errors": list(self.errors),
        }
