import pytest
from unittest.mock import MagicMock, patch
from git_toolkit.plugins import Plugin, PluginManager
from git_toolkit.hooks import HookManager

class MockPlugin(Plugin):
    def __init__(self):
        self.commands_registered = False
        self.command_handled = False
        self.hook_called = False

    def register_commands(self, subparsers):
        self.commands_registered = True

    def run_command(self, args) -> bool:
        if hasattr(args, 'command') and args.command == 'mock':
            self.command_handled = True
            return True
        return False

    def run_hook(self, hook_name, env=None) -> bool:
        self.hook_called = True
        return True

def test_plugin_manager_loading():
    with patch('importlib.metadata.entry_points') as mock_ep:
        mock_entry = MagicMock()
        mock_entry.name = 'mock'
        mock_entry.load.return_value = MockPlugin
        
        # Mocking for Python 3.10+ style
        mock_ep.return_value = [mock_entry]
        
        mgr = PluginManager()
        assert len(mgr.plugins) == 1
        assert isinstance(mgr.plugins[0], MockPlugin)

def test_plugin_manager_loading_legacy():
    with patch('importlib.metadata.entry_points') as mock_ep:
        mock_entry = MagicMock()
        mock_entry.name = 'mock_legacy'
        mock_entry.load.return_value = MockPlugin
        
        # Mocking for Python < 3.10 style
        mock_ep.return_value.get.return_value = [mock_entry]
        
        with patch('sys.version_info', (3, 9)):
            mgr = PluginManager()
            assert len(mgr.plugins) == 1
            assert isinstance(mgr.plugins[0], MockPlugin)

def test_plugin_manager_loading_warning():
    class NotAPlugin:
        pass

    with patch('importlib.metadata.entry_points') as mock_ep:
        mock_entry = MagicMock()
        mock_entry.name = 'not_a_plugin'
        mock_entry.load.return_value = NotAPlugin
        mock_ep.return_value = [mock_entry]
        
        with patch('builtins.print') as mock_print:
            mgr = PluginManager()
            assert len(mgr.plugins) == 0
            mock_print.assert_any_call("Warning: Plugin 'not_a_plugin' does not inherit from Plugin base class.")

def test_plugin_manager_loading_error():
    with patch('importlib.metadata.entry_points') as mock_ep:
        mock_entry = MagicMock()
        mock_entry.name = 'error_plugin'
        mock_entry.load.side_effect = Exception("Load error")
        mock_ep.return_value = [mock_entry]
        
        with patch('builtins.print') as mock_print:
            mgr = PluginManager()
            assert len(mgr.plugins) == 0
            mock_print.assert_any_call("Error loading plugin 'error_plugin': Load error")

def test_plugin_register_commands():
    mgr = PluginManager()
    mock_plugin = MockPlugin()
    mgr.plugins = [mock_plugin]
    
    mock_subparsers = MagicMock()
    mgr.register_all_commands(mock_subparsers)
    assert mock_plugin.commands_registered is True

def test_plugin_handle_command():
    mgr = PluginManager()
    mock_plugin = MockPlugin()
    mgr.plugins = [mock_plugin]
    
    mock_args = MagicMock()
    mock_args.command = 'mock'
    
    assert mgr.handle_command(mock_args) is True
    assert mock_plugin.command_handled is True

def test_plugin_handle_command_not_handled():
    mgr = PluginManager()
    mock_plugin = MockPlugin()
    mgr.plugins = [mock_plugin]
    
    mock_args = MagicMock()
    mock_args.command = 'other'
    
    assert mgr.handle_command(mock_args) is False
    assert mock_plugin.command_handled is False

def test_plugin_base_methods():
    class MinimalPlugin(Plugin):
        def register_commands(self, subparsers):
            subparsers.add_parser("minimal")

    mock_subparsers = MagicMock()
    plugin = MinimalPlugin()
    plugin.register_commands(mock_subparsers)
    mock_subparsers.add_parser.assert_called_with("minimal")
    assert plugin.run_command(None) is False

def test_plugin_hook_integration():
    plugin_mgr = PluginManager()
    mock_plugin = MockPlugin()
    plugin_mgr.plugins = [mock_plugin]
    
    hook_mgr = HookManager(hooks_config={}, plugin_mgr=plugin_mgr)
    assert hook_mgr.run_hook("some_hook") is True
    assert mock_plugin.hook_called is True

def test_plugin_hook_failure_blocks():
    class FailingPlugin(Plugin):
        def register_commands(self, subparsers): pass
        def run_hook(self, hook_name, env=None): return False
    
    plugin_mgr = PluginManager()
    plugin_mgr.plugins = [FailingPlugin()]
    
    hook_mgr = HookManager(hooks_config={}, plugin_mgr=plugin_mgr)
    assert hook_mgr.run_hook("some_hook") is False
