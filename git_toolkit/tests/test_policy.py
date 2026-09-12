from git_toolkit.config import Safety
from git_toolkit.policy import (
    evaluate_branch_name,
    evaluate_clean_worktree,
    evaluate_force_push,
    evaluate_remote,
    remote_host,
)


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


def test_branch_pattern_is_optional() -> None:
    decision = evaluate_branch_name("anything/is-allowed", Safety())
    assert decision.allowed is True
    assert decision.rule == "branch.name.unconfigured"


def test_branch_pattern_accepts_and_rejects_deterministically() -> None:
    safety = Safety(branch_name_pattern=r"(main|feature/[a-z0-9-]+)")
    assert evaluate_branch_name("feature/safe-name", safety).allowed is True

    decision = evaluate_branch_name("Feature/Unsafe", safety)
    assert decision.allowed is False
    assert decision.rule == "branch.name.invalid"


def test_invalid_branch_pattern_fails_closed() -> None:
    decision = evaluate_branch_name("feature/example", Safety(branch_name_pattern="["))
    assert decision.allowed is False
    assert decision.rule == "branch.name.invalid_policy"


def test_remote_host_parses_https_and_ssh() -> None:
    assert remote_host("https://github.com/example/repo.git") == "github.com"
    assert remote_host("git@github.com:example/repo.git") == "github.com"
    assert remote_host("ssh://git@gitlab.example.com/example/repo.git") == "gitlab.example.com"


def test_remote_denylist_takes_precedence() -> None:
    safety = Safety(
        allowed_remote_hosts=["github.com"],
        denied_remote_hosts=["github.com"],
    )
    decision = evaluate_remote("https://github.com/example/repo.git", safety)
    assert decision.allowed is False
    assert decision.rule == "remote.host.denied"


def test_remote_allowlist_blocks_unlisted_host() -> None:
    safety = Safety(allowed_remote_hosts=["github.com"])
    decision = evaluate_remote("git@gitlab.com:example/repo.git", safety)
    assert decision.allowed is False
    assert decision.rule == "remote.host.not_allowed"


def test_remote_policy_allows_standard_host_when_unrestricted() -> None:
    decision = evaluate_remote("https://github.com/example/repo.git", Safety())
    assert decision.allowed is True
    assert decision.rule == "remote.host.allowed"
