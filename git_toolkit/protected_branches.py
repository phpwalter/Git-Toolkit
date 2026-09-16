from __future__ import annotations

from dataclasses import dataclass

from .config import Safety


@dataclass(frozen=True)
class BranchProtectionDecision:
    allowed: bool
    rule: str
    reason: str


def evaluate_branch_mutation(branch: str, operation: str, safety: Safety | None) -> BranchProtectionDecision:
    if safety is None or branch not in safety.protect_branches:
        return BranchProtectionDecision(True, f"{operation}.branch.allowed", "Branch is not protected")

    blocked = {"delete", "force-push", "rebase", "reset", "rewrite"}
    if operation in blocked:
        return BranchProtectionDecision(
            False,
            f"{operation}.protected_branch",
            f"{operation} is blocked on protected branch '{branch}'.",
        )
    return BranchProtectionDecision(
        True,
        f"{operation}.protected_branch.allowed",
        "Operation preserves protected history",
    )


def require_unprotected(branch: str, operation: str, safety: Safety | None) -> None:
    decision = evaluate_branch_mutation(branch, operation, safety)
    if not decision.allowed:
        raise ValueError(decision.reason)
