from git_toolkit.config import Safety
from git_toolkit.policy import evaluate_clean_worktree, evaluate_force_push


def test_normal_push_allowed() -> None:
    decision = evaluate_force_push("main", False, Safety())
    assert decision.allowed is True
    assert decision.rule == "push.normal"


def test_force_push_disabled_by_default() -> None:
    decision = evaluate_force_push("feature", True, Safety())
    assert decision.allowed is False
    assert decision.rule == "push.force.disabled"
    assert decision.remediation


def test_force_push_protected_branch_is_blocked() -> None:
    safety = Safety(prevent_force_push=False, protect_branches=["main"])
    decision = evaluate_force_push("main", True, safety)
    assert decision.allowed is False
    assert decision.rule == "push.force.protected_branch"


def test_force_with_lease_allowed_on_unprotected_branch() -> None:
    safety = Safety(prevent_force_push=False, protect_branches=["main"])
    decision = evaluate_force_push("feature", True, safety)
    assert decision.allowed is True
    assert decision.rule == "push.force.with_lease"


def test_dirty_tree_blocked_for_sensitive_operation() -> None:
    decision = evaluate_clean_worktree(
        is_dirty=True,
        safety=Safety(require_clean_worktree=True),
        operation="sync",
    )
    assert decision.allowed is False
    assert decision.rule == "sync.dirty.blocked"
    assert "Commit, stash, or discard" in (decision.remediation or "")
