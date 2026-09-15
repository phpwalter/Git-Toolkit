from __future__ import annotations

import subprocess
from pathlib import Path

FORBIDDEN_TRACKED_PATTERNS = (
    ".coverage",
    "coverage.xml",
    ".pytest_cache/",
    "__pycache__/",
    ".git-toolkit/history.json",
    ".git-toolkit/logs/",
    ".git-toolkit/cache/",
    ".egg-info/",
    "dist/",
    "build/",
)


def tracked_files(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    return [line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()]


def violations(files: list[str]) -> list[str]:
    found: list[str] = []
    for path in files:
        if any(pattern in path for pattern in FORBIDDEN_TRACKED_PATTERNS):
            found.append(path)
    return sorted(found)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    found = violations(tracked_files(root))
    if found:
        print("Generated/runtime artifacts are tracked:")
        for path in found:
            print(f"- {path}")
        raise SystemExit(1)
    print("Repository hygiene check passed.")


if __name__ == "__main__":
    main()
