import os
import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict, List
from .config import Hook
from .plugins import PluginManager

class HookManager:
    """
    Manages the execution of lifecycle hooks defined in the configuration.
    """
    def __init__(self, hooks_config: Dict[str, Hook], plugin_mgr: Optional[PluginManager] = None):
        self.hooks = hooks_config
        self.plugin_mgr = plugin_mgr

    def run_hook(self, hook_name: str, env: Optional[Dict[str, str]] = None) -> bool:
        """
        Executes a specific hook.
        
        Returns:
            True if the hook succeeded (exit code 0), False otherwise.
        """
        # First, try to run hooks from plugins
        if self.plugin_mgr:
            for plugin in self.plugin_mgr.plugins:
                # Plugins can implement a run_hook method
                if hasattr(plugin, 'run_hook'):
                    try:
                        if not plugin.run_hook(hook_name, env):
                            return False
                    except Exception as e:
                        print(f"Error in plugin hook '{hook_name}': {e}", file=sys.stderr)
                        return False

        hook = self.hooks.get(hook_name)
        if not hook or not hook.script:
            # Hook not defined or has no script, consider it successful
            return True

        print(f"Running hook: {hook_name}...")
        
        # Merge current environment with provided one
        current_env = os.environ.copy()
        if env:
            current_env.update(env)

        try:
            # Use shell=True to allow complex scripts and shell built-ins
            result = subprocess.run(  # nosec: B602
                hook.script,
                shell=True,
                env=current_env,
                check=False, # We check return code manually for logging
                capture_output=False # Stream output directly to user
            )
            
            if result.returncode == 0:
                print(f"Hook '{hook_name}' finished successfully.")
                return True
            else:
                print(f"Hook '{hook_name}' failed with exit code {result.returncode}.", file=sys.stderr)
                return False
        except Exception as e:
            print(f"Error executing hook '{hook_name}': {e}", file=sys.stderr)
            return False
