from __future__ import annotations

import argparse
import re
import subprocess

TAG_PATTERN = re.compile(r"^v\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")


def _git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=False,
        shell=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def verify(tag: str, main_ref: str = "origin/main") -> None:
    if not TAG_PATTERN.fullmatch(tag):
        raise ValueError(f"invalid release tag: {tag}")
    tag_commit = _git("rev-list", "-n", "1", tag)
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", tag_commit, main_ref],
        capture_output=True,
        text=True,
        check=False,
        shell=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"release tag {tag} does not point to a commit reachable from {main_ref}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify a release tag originates from stable main.")
    parser.add_argument("tag")
    parser.add_argument("--main-ref", default="origin/main")
    args = parser.parse_args()
    verify(args.tag, args.main_ref)
    print(f"release ref verified: {args.tag}")


if __name__ == "__main__":
    main()
