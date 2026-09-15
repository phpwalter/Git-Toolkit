import pytest

from git_toolkit.validation import (
    validate_branch_name,
    validate_host,
    validate_positive_int,
    validate_tag_name,
)


def test_branch_validation_accepts_common_names() -> None:
    assert validate_branch_name("feature/add-validation") == "feature/add-validation"


def test_branch_validation_rejects_invalid_names() -> None:
    with pytest.raises(ValueError):
        validate_branch_name("bad branch")
    with pytest.raises(ValueError):
        validate_branch_name("../escape")


def test_tag_validation_rejects_whitespace() -> None:
    with pytest.raises(ValueError):
        validate_tag_name("v1 bad")


def test_host_validation_normalizes_case() -> None:
    assert validate_host("GitHub.COM") == "github.com"


def test_positive_integer_validation() -> None:
    assert validate_positive_int(4, field="workers") == 4
    with pytest.raises(ValueError):
        validate_positive_int(0, field="workers")
