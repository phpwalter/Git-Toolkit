from __future__ import annotations

import subprocess
from pathlib import Path

PROTECTED = {"main", "master", "develop"}


def _run(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def merged_remote_branches(root: Path, remote: str = "origin") -> list[str]:
    output = _run(root, "branch", "-r", "--merged", f"{remote}/main")
    branches: list[str] = []
    for raw in output.splitlines():
        ref = raw.strip()
        if not ref or "->" in ref:
            continue
        prefix = f"{remote}/"
        if not ref.startswith(prefix):
            continue
        name = ref[len(prefix):]
        if name not in PROTECTED:
            branches.append(name)
    return sorted(set(branches))


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    branches = merged_remote_branches(root)
    if not branches:
        print("No merged remote feature branches found.")
        return
    print("Merged remote branches eligible for review and deletion:")
    for branch in branches:
        print(f"- {branch}")
    print("\nThis tool does not delete branches automatically.")
    print("Review each branch before running: git push origin --delete <branch>")


if __name__ == "__main__":
    main()
