from unittest.mock import patch

from git_toolkit.config import Config, Repository, Step, Workflow
from git_toolkit.workflow_runner import execute_step, run_workflow


def test_branch_condition_skips_nonmatching_repo() -> None:
    repo = Repository(name="repo", path=".")
    config = Config(repositories=[repo])
    step = Step(name="only-main", script="echo hello", **{"if": "branch == main"})

    with patch("git_toolkit.workflow_runner.get_repo_status") as status, patch(
        "git_toolkit.workflow_runner.run_shell_command"
    ) as shell:
        status.return_value = {"branch": "develop", "is_dirty": False, "exists": True}
        result = execute_step(step, repo, config, dry_run=False)

    assert "Skipped" in result
    shell.assert_not_called()


def test_script_retry_stops_after_success() -> None:
    repo = Repository(name="repo", path=".")
    config = Config(repositories=[repo])
    step = Step(name="retry", script="test", retries=2)

    with patch("git_toolkit.workflow_runner.run_shell_command") as shell:
        shell.side_effect = [
            {"success": False, "message": "failed"},
            {"success": True, "message": "done"},
        ]
        result = execute_step(step, repo, config, dry_run=False)

    assert "OK" in result
    assert shell.call_count == 2


def test_failure_policy_stops_later_steps() -> None:
    repo = Repository(name="repo", path=".")
    workflow = Workflow(
        failure_policy="stop",
        steps=[Step(command="status"), Step(command="fetch")],
    )
    config = Config(repositories=[repo], workflows={"test": workflow})

    with patch("git_toolkit.workflow_runner.execute_step") as execute:
        execute.return_value = "repo: FAILED - problem"
        results = run_workflow(workflow, config)

    assert results == ["repo: FAILED - problem"]
    assert execute.call_count == 1


def test_parallel_workflow_executes_each_repo() -> None:
    repos = [Repository(name="a", path="."), Repository(name="b", path=".")]
    workflow = Workflow(steps=[Step(command="status")])
    config = Config(repositories=repos)

    with patch("git_toolkit.workflow_runner.execute_step", return_value="OK") as execute:
        results = run_workflow(workflow, config, parallel=True, workers=2)

    assert len(results) == 2
    assert execute.call_count == 2


def test_repo_clean_condition() -> None:
    repo = Repository(name="repo", path=".")
    config = Config(repositories=[repo])
    step = Step(script="echo ok", **{"if": "repo.clean"})

    with patch("git_toolkit.workflow_runner.get_repo_status") as status, patch(
        "git_toolkit.workflow_runner.run_shell_command"
    ) as shell:
        status.return_value = {"is_dirty": False, "exists": True, "branch": "main"}
        shell.return_value = {"success": True, "message": "Command succeeded."}
        result = execute_step(step, repo, config, dry_run=False)

    assert "OK" in result
    shell.assert_called_once()
