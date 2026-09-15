from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class CommitMessagePolicy:
    pattern: str = r"^(feat|fix|docs|test|refactor|build|ci|chore|perf)(\([a-z0-9._-]+\))?: .{1,72}$"
    min_length: int = 3
    max_subject_length: int = 100


@dataclass(frozen=True)
class CommitMessageDecision:
    allowed: bool
    rule: str
    reason: str


def evaluate_commit_message(message: str, policy: CommitMessagePolicy | None = None) -> CommitMessageDecision:
    policy = policy or CommitMessagePolicy()
    subject = message.splitlines()[0].strip() if message.strip() else ""
    if len(subject) < policy.min_length:
        return CommitMessageDecision(False, "commit.message.too_short", "Commit subject is too short.")
    if len(subject) > policy.max_subject_length:
        return CommitMessageDecision(False, "commit.message.too_long", "Commit subject exceeds the configured maximum length.")
    try:
        matches = re.fullmatch(policy.pattern, subject) is not None
    except re.error as exc:
        return CommitMessageDecision(False, "commit.message.invalid_policy", f"Invalid commit-message pattern: {exc}")
    if not matches:
        return CommitMessageDecision(False, "commit.message.invalid", "Commit subject does not satisfy the configured pattern.")
    return CommitMessageDecision(True, "commit.message.valid", "Commit message is valid.")
