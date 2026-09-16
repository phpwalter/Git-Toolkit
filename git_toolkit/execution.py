from __future__ import annotations

import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CommandSpec:
    argv: list[str] | None = None
    shell_command: str | None = None
    timeout: int | None = None

    def __post_init__(self) -> None:
        if bool(self.argv) == bool(self.shell_command):
            raise ValueError("Specify exactly one of argv or shell_command")


def parse_argv(command: str) -> list[str]:
    parts = shlex.split(command, posix=True)
    if not parts:
        raise ValueError("command must not be empty")
    return parts


def run_command(
    cwd: str | Path,
    spec: CommandSpec,
    *,
    allow_shell: bool = False,
    dry_run: bool = False,
) -> dict[str, object]:
    working_dir = Path(cwd)
    if not working_dir.exists():
        return {"success": False, "message": f"Working directory does not exist: {working_dir}"}

    if spec.shell_command is not None and not allow_shell:
        return {
            "success": False,
            "message": "Shell execution is disabled; use argv execution or explicitly enable trusted shell execution.",
        }

    if dry_run:
        rendered = spec.shell_command if spec.shell_command is not None else " ".join(spec.argv or [])
        return {"success": True, "message": f"[DRY-RUN] Would run: {rendered}"}

    try:
        if spec.argv is not None:
            result = subprocess.run(
                spec.argv,
                cwd=working_dir,
                capture_output=True,
                text=True,
                check=False,
                timeout=spec.timeout,
                shell=False,
            )
        else:
            result = subprocess.run(
                spec.shell_command or "",
                cwd=working_dir,
                capture_output=True,
                text=True,
                check=False,
                timeout=spec.timeout,
                shell=True,  # nosec B602 - explicitly gated trusted shell mode
            )
    except subprocess.TimeoutExpired:
        return {"success": False, "message": f"Command timed out after {spec.timeout}s."}

    return {
        "success": result.returncode == 0,
        "message": "Command succeeded." if result.returncode == 0 else f"Command failed with code {result.returncode}.",
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode,
    }
