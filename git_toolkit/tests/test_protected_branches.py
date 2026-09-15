import pytest

from git_toolkit.config import Safety
from git_toolkit.protected_branches import evaluate_branch_mutation, require_unprotected


def test_unprotected_branch_allows_mutation() -> None:
    decision = evaluate_branch_mutation("feature/test", "rebase", Safety())
    assert decision.allowed is True


def test_protected_branch_blocks_history_rewrite() -> None:
    decision = evaluate_branch_mutation("main", "rebase", Safety())
    assert decision.allowed is False
    assert decision.rule == "rebase.protected_branch"


def test_protected_branch_allows_history_preserving_operation() -> None:
    decision = evaluate_branch_mutation("main", "merge", Safety())
    assert decision.allowed is True


def test_require_unprotected_raises_for_blocked_operation() -> None:
    with pytest.raises(ValueError, match="blocked"):
        require_unprotected("main", "delete", Safety())
