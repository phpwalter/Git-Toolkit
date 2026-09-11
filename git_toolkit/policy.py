from __future__ import annotations

from dataclasses import dataclass

from .config import Safety


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    rule: str
    reason: str
    remediation: str | None = None

    @classmethod
    def allow(cls, rule: str = "policy.allow") -> "PolicyDecision":
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
            "Use a normal push or explicitly change safety.prevent_force_push for a trusted workflow.",
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
