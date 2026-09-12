from pathlib import Path
from unittest.mock import MagicMock, patch

from git_toolkit.hooks import HookManager
from git_toolkit.plugins import PLUGIN_API_VERSION, Plugin, PluginManager


class MockPlugin(Plugin):
    name = "mock"

    def __init__(self) -> None:
        self.commands_registered = False
        self.command_handled = False
        self.hook_called = False

    def register_commands(self, subparsers) -> None:
        self.commands_registered = True

    def run_command(self, args) -> bool:
        if getattr(args, "command", None) == "mock":
            self.command_handled = True
            return True
        return False

    def run_hook(self, hook_name: str, env=None) -> bool:
        self.hook_called = True
        return True


def _entry_points_with(plugin_class):
    selected = MagicMock()
    entry = MagicMock()
    entry.name = "mock"
    entry.load.return_value = plugin_class
    selected.select.return_value = [entry]
    return selected


def test_entry_point_plugin_loading(tmp_path: Path) -> None:
    with patch("importlib.metadata.entry_points", return_value=_entry_points_with(MockPlugin)):
        manager = PluginManager(local_plugin_dir=tmp_path / "none")
    assert len(manager.plugins) == 1
    assert isinstance(manager.plugins[0], MockPlugin)


def test_incompatible_plugin_is_rejected(tmp_path: Path) -> None:
    class IncompatiblePlugin(MockPlugin):
        api_version = "999"

    with patch("importlib.metadata.entry_points", return_value=_entry_points_with(IncompatiblePlugin)):
        manager = PluginManager(local_plugin_dir=tmp_path / "none")
    assert manager.plugins == []
    assert "incompatible" in manager.errors[0]


def test_local_plugins_are_disabled_by_default(tmp_path: Path) -> None:
    plugin_dir = tmp_path / "plugins"
    plugin_dir.mkdir()
    (plugin_dir / "local.py").write_text("raise RuntimeError('must not execute')\n", encoding="utf-8")
    with patch("importlib.metadata.entry_points") as entry_points:
        entry_points.return_value.select.return_value = []
        manager = PluginManager(local_plugin_dir=plugin_dir)
    assert manager.plugins == []
    assert manager.errors == []


def test_local_plugin_discovery_when_trusted(tmp_path: Path) -> None:
    plugin_dir = tmp_path / "plugins"
    plugin_dir.mkdir()
    plugin_file = plugin_dir / "local.py"
    plugin_file.write_text(
        "from git_toolkit.plugins import Plugin\n"
        "class LocalPlugin(Plugin):\n"
        "    name = 'local'\n"
        "    def register_commands(self, subparsers):\n"
        "        return None\n"
        "plugin = LocalPlugin\n",
        encoding="utf-8",
    )
    with patch("importlib.metadata.entry_points") as entry_points:
        entry_points.return_value.select.return_value = []
        manager = PluginManager(local_plugin_dir=plugin_dir, allow_local_plugins=True)
    assert [plugin.name for plugin in manager.plugins] == ["local"]


def test_plugin_command_and_hook_dispatch(tmp_path: Path) -> None:
    with patch("importlib.metadata.entry_points") as entry_points:
        entry_points.return_value.select.return_value = []
        manager = PluginManager(local_plugin_dir=tmp_path / "none")
    plugin = MockPlugin()
    manager.plugins = [plugin]

    subparsers = MagicMock()
    manager.register_all_commands(subparsers)
    assert plugin.commands_registered is True

    args = MagicMock(command="mock")
    assert manager.handle_command(args) is True
    assert plugin.command_handled is True

    hooks = HookManager(hooks_config={}, plugin_mgr=manager)
    assert hooks.run_hook("pre_push") is True
    assert plugin.hook_called is True


def test_diagnostics_report_api_and_errors(tmp_path: Path) -> None:
    with patch("importlib.metadata.entry_points") as entry_points:
        entry_points.return_value.select.return_value = []
        manager = PluginManager(local_plugin_dir=tmp_path / "none")
    manager.errors.append("example error")
    diagnostics = manager.diagnostics()
    assert diagnostics["api_version"] == PLUGIN_API_VERSION
    assert diagnostics["local_plugins_enabled"] is False
    assert diagnostics["errors"] == ["example error"]
