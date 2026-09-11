from __future__ import annotations

import os
import subprocess
import sys
from typing import Optional

from .config import Hook
from .plugins import PluginManager


class HookManager:
    """Manage lifecycle hooks from plugins and trusted project configuration."""

    def __init__(
        self,
        hooks_config: dict[str, Hook],
        plugin_mgr: Optional[PluginManager] = None,
        allow_project_scripts: bool = False,
    ) -> None:
        self.hooks = hooks_config
        self.plugin_mgr = plugin_mgr
        self.allow_project_scripts = allow_project_scripts

    def run_hook(self, hook_name: str, env: Optional[dict[str, str]] = None) -> bool:
        if self.plugin_mgr:
            for plugin in self.plugin_mgr.plugins:
                try:
                    if not plugin.run_hook(hook_name, env):
                        return False
                except Exception as exc:
                    print(f"Error in plugin hook '{hook_name}': {exc}", file=sys.stderr)
                    return False

        hook = self.hooks.get(hook_name)
        if not hook or not hook.script:
            return True

        if not self.allow_project_scripts:
            print(
                f"Hook '{hook_name}' is blocked because project scripts are disabled. "
                "Set security.allow_project_scripts: true only for trusted repositories.",
                file=sys.stderr,
            )
            return False

        current_env = os.environ.copy()
        if env:
            current_env.update(env)

        try:
            result = subprocess.run(  # nosec B602 - explicitly trusted project hook
                hook.script,
                shell=True,
                env=current_env,
                check=False,
                capture_output=False,
            )
            return result.returncode == 0
        except Exception as exc:
            print(f"Error executing hook '{hook_name}': {exc}", file=sys.stderr)
            return False
