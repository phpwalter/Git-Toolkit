from git_toolkit.commit_policy import CommitMessagePolicy, evaluate_commit_message


def test_default_policy_accepts_conventional_subject() -> None:
    decision = evaluate_commit_message("feat(cli): add branch command")
    assert decision.allowed is True
    assert decision.rule == "commit.message.valid"


def test_default_policy_rejects_invalid_subject() -> None:
    decision = evaluate_commit_message("updated stuff")
    assert decision.allowed is False
    assert decision.rule == "commit.message.invalid"


def test_length_limits_are_enforced() -> None:
    short = evaluate_commit_message("x")
    assert short.rule == "commit.message.too_short"

    policy = CommitMessagePolicy(max_subject_length=10)
    long = evaluate_commit_message("feat: this subject is too long", policy)
    assert long.rule == "commit.message.too_long"


def test_invalid_regex_fails_closed() -> None:
    decision = evaluate_commit_message("feat: ok", CommitMessagePolicy(pattern="["))
    assert decision.allowed is False
    assert decision.rule == "commit.message.invalid_policy"
