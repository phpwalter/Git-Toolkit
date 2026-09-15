from __future__ import annotations

import argparse
import re
import tarfile
import zipfile
from pathlib import Path

REQUIRED_WHEEL_MEMBERS = {
    "git_toolkit/__init__.py",
    "git_toolkit/cli.py",
    "git_toolkit/config.py",
    "git_toolkit/git_wrapper.py",
    "git_toolkit/version.py",
}


def _normalized_wheel_members(path: Path) -> set[str]:
    with zipfile.ZipFile(path) as archive:
        return {name for name in archive.namelist() if not name.endswith("/")}


def _normalized_sdist_members(path: Path) -> set[str]:
    with tarfile.open(path, "r:gz") as archive:
        names = {member.name for member in archive.getmembers() if member.isfile()}
    return {name.split("/", 1)[1] for name in names if "/" in name}


def verify_wheel(path: Path) -> list[str]:
    members = _normalized_wheel_members(path)
    errors = [f"wheel missing required member: {member}" for member in sorted(REQUIRED_WHEEL_MEMBERS - members)]
    entry_points = [name for name in members if name.endswith(".dist-info/entry_points.txt")]
    if len(entry_points) != 1:
        errors.append("wheel must contain exactly one dist-info/entry_points.txt")
    return errors


def verify_sdist(path: Path) -> list[str]:
    members = _normalized_sdist_members(path)
    required = {"pyproject.toml", "README.md", "git_toolkit/cli.py", "git_toolkit/version.py"}
    return [f"sdist missing required member: {member}" for member in sorted(required - members)]


def version_from_filename(path: Path) -> str | None:
    match = re.search(r"git[_-]toolkit-([0-9][A-Za-z0-9.!+_-]*)", path.name)
    return match.group(1).replace("_", "-") if match else None


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify Git Toolkit distribution artifacts.")
    parser.add_argument("dist", type=Path, nargs="?", default=Path("dist"))
    args = parser.parse_args()

    wheels = sorted(args.dist.glob("*.whl"))
    sdists = sorted(args.dist.glob("*.tar.gz"))
    errors: list[str] = []
    if len(wheels) != 1:
        errors.append(f"expected exactly one wheel, found {len(wheels)}")
    if len(sdists) != 1:
        errors.append(f"expected exactly one sdist, found {len(sdists)}")
    if wheels:
        errors.extend(verify_wheel(wheels[0]))
    if sdists:
        errors.extend(verify_sdist(sdists[0]))
    if wheels and sdists and version_from_filename(wheels[0]) != version_from_filename(sdists[0]):
        errors.append("wheel and sdist versions do not match")

    if errors:
        raise SystemExit("\n".join(errors))
    print("distribution artifacts verified")


if __name__ == "__main__":
    main()
