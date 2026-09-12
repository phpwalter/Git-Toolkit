from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urlparse

from .config import Safety


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    rule: str
    reason: str
    remediation: str | None = None

    @classmethod
    def allow(cls, rule: str = "policy.allow") -> PolicyDecision:
        return cls(True, rule, "Operation allowed")


def evaluate_force_push(branch: str, force: bool, safety: Safety | None) -> PolicyDecision:
    if not force:
        return PolicyDecision.allow("push.normal")
    if safety is None:
        return PolicyDecision.allow("push.force.unconfigured")
    if safety.prevent_force_push:
        return PolicyDecision(
            False,
            "push.force.disabled",
            "Force push is disabled by project policy.",
            (
                "Use a normal push or explicitly change "
                "safety.prevent_force_push for a trusted workflow."
            ),
        )
    if branch in safety.protect_branches:
        return PolicyDecision(
            False,
            "push.force.protected_branch",
            f"Force push to protected branch '{branch}' is blocked.",
            "Push a new commit normally or perform history repair on an unprotected branch.",
        )
    return PolicyDecision.allow("push.force.with_lease")


def evaluate_clean_worktree(
    *,
    is_dirty: bool,
    safety: Safety | None,
    operation: str,
) -> PolicyDecision:
    if not is_dirty:
        return PolicyDecision.allow(f"{operation}.clean")
    if safety is None or not safety.require_clean_worktree:
        return PolicyDecision.allow(f"{operation}.dirty.allowed")
    return PolicyDecision(
        False,
        f"{operation}.dirty.blocked",
        f"{operation} requires a clean working tree.",
        "Commit, stash, or discard local changes before retrying.",
    )


def evaluate_branch_name(branch: str, safety: Safety | None) -> PolicyDecision:
    """Validate a branch name against an optional project regex."""
    if safety is None or not safety.branch_name_pattern:
        return PolicyDecision.allow("branch.name.unconfigured")
    try:
        matches = re.fullmatch(safety.branch_name_pattern, branch) is not None
    except re.error as exc:
        return PolicyDecision(
            False,
            "branch.name.invalid_policy",
            f"Configured branch_name_pattern is invalid: {exc}",
            "Correct safety.branch_name_pattern before retrying.",
        )
    if matches:
        return PolicyDecision.allow("branch.name.valid")
    return PolicyDecision(
        False,
        "branch.name.invalid",
        f"Branch '{branch}' does not satisfy the configured naming policy.",
        f"Use a branch name matching: {safety.branch_name_pattern}",
    )


def remote_host(remote_url: str) -> str:
    """Extract a normalized host from HTTPS, SSH URL, or SCP-like Git remote syntax."""
    value = remote_url.strip()
    if "://" in value:
        return (urlparse(value).hostname or "").lower()
    if "@" in value and ":" in value:
        return value.split("@", 1)[1].split(":", 1)[0].lower()
    return ""


def evaluate_remote(remote_url: str, safety: Safety | None) -> PolicyDecision:
    """Apply remote host allow/deny rules. Deny rules take precedence."""
    if safety is None:
        return PolicyDecision.allow("remote.unconfigured")
    host = remote_host(remote_url)
    if not host:
        return PolicyDecision(
            False,
            "remote.host.unrecognized",
            f"Could not determine remote host from '{remote_url}'.",
            "Use a standard HTTPS or SSH Git remote URL.",
        )

    denied = {item.lower() for item in safety.denied_remote_hosts}
    allowed = {item.lower() for item in safety.allowed_remote_hosts}
    if host in denied:
        return PolicyDecision(
            False,
            "remote.host.denied",
            f"Remote host '{host}' is explicitly denied by project policy.",
            "Use an approved remote or change safety.denied_remote_hosts.",
        )
    if allowed and host not in allowed:
        return PolicyDecision(
            False,
            "remote.host.not_allowed",
            f"Remote host '{host}' is not in the project allowlist.",
            f"Use one of the approved hosts: {', '.join(sorted(allowed))}",
        )
    return PolicyDecision.allow("remote.host.allowed")
