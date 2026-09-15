from git_toolkit.errors import (
    ConfigurationError,
    ErrorContext,
    ExitCode,
    GitOperationError,
    PolicyError,
    error_result,
)


def test_error_serialization_includes_context_and_remediation() -> None:
    error = PolicyError(
        "blocked",
        remediation="use another branch",
        context=ErrorContext(command="push", repository="repo", rule="push.force.disabled"),
    )
    payload = error.to_dict()
    assert payload["code"] == "policy.denied"
    assert payload["exit_code"] == int(ExitCode.POLICY)
    assert payload["context"]["repository"] == "repo"
    assert payload["context"]["rule"] == "push.force.disabled"
    assert "remediation=use another branch" in error.render()


def test_error_result_is_machine_readable() -> None:
    result = error_result(GitOperationError("failed"), name="repo")
    assert result["success"] is False
    assert result["name"] == "repo"
    assert result["error"]["code"] == "git.operation_failed"


def test_specific_error_exit_codes_are_stable() -> None:
    assert ConfigurationError("bad").exit_code == ExitCode.CONFIGURATION
    assert GitOperationError("bad").exit_code == ExitCode.GIT
