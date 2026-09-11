import abc
import importlib.metadata
from typing import List, Dict, Type, Optional
import sys

class Plugin(abc.ABC):
    """
    Base class for Git Toolkit plugins.
    Plugins can extend the toolkit by registering new commands or hooks.
    """
    @abc.abstractmethod
    def register_commands(self, subparsers):
        """
        Register new commands with the CLI subparsers.
        """
        pass

    def run_command(self, args) -> bool:
        """
        Execute the plugin's command logic.
        Returns True if handled, False otherwise.
        """
        return False

class PluginManager:
    """
    Discovers and loads Git Toolkit plugins using entry points.
    """
    ENTRY_POINT_GROUP = 'git_toolkit.plugins'

    def __init__(self):
        self.plugins: List[Plugin] = []
        self._load_plugins()

    def _load_plugins(self):
        """
        Loads plugins defined in the 'git_toolkit.plugins' entry point group.
        """
        if sys.version_info >= (3, 10):
            entry_points = importlib.metadata.entry_points(group=self.ENTRY_POINT_GROUP)
        else:
            # For Python < 3.10, entry_points returns a dict
            eps = importlib.metadata.entry_points()
            entry_points = eps.get(self.ENTRY_POINT_GROUP, [])

        for entry_point in entry_points:
            try:
                plugin_class = entry_point.load()
                if issubclass(plugin_class, Plugin):
                    self.plugins.append(plugin_class())
                else:
                    print(f"Warning: Plugin '{entry_point.name}' does not inherit from Plugin base class.")
            except Exception as e:
                print(f"Error loading plugin '{entry_point.name}': {e}")

    def register_all_commands(self, subparsers):
        """
        Registers commands from all loaded plugins.
        """
        for plugin in self.plugins:
            plugin.register_commands(subparsers)

    def handle_command(self, args) -> bool:
        """
        Delegates command execution to the appropriate plugin.
        """
        for plugin in self.plugins:
            if plugin.run_command(args):
                return True
        return False
