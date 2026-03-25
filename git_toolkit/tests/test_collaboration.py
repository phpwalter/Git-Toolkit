import pytest
import json
from unittest.mock import patch, MagicMock
from git_toolkit.config import Config, Repository, Workflow, Step
from git_toolkit.cli import send_webhook_notification

def test_repository_grouping():
    repo1 = Repository(name="repo1", path="path1", groups=["frontend"])
    repo2 = Repository(name="repo2", path="path2", groups=["backend"])
    repo3 = Repository(name="repo3", path="path3", groups=["frontend", "shared"])

    config = Config(repositories=[repo1, repo2, repo3])

    frontend_repos = [r for r in config.repositories if "frontend" in r.groups]
    assert len(frontend_repos) == 2
    assert repo1 in frontend_repos
    assert repo3 in frontend_repos

    backend_repos = [r for r in config.repositories if "backend" in r.groups]
    assert len(backend_repos) == 1
    assert repo2 in backend_repos

@patch("urllib.request.urlopen")
@patch("urllib.request.Request")
def test_send_webhook_notification(mock_request, mock_urlopen):
    mock_response = MagicMock()
    mock_response.status = 200
    mock_urlopen.return_value.__enter__.return_value = mock_response

    url = "https://example.test/webhook"
    workflow_name = "deploy"
    results = ["repo1: Success", "repo2: Success"]

    send_webhook_notification(url, workflow_name, results)

    mock_request.assert_called_once()
    args, kwargs = mock_request.call_args
    assert args[0] == url

    sent_data = json.loads(kwargs['data'].decode('utf-8'))
    assert sent_data["workflow"] == workflow_name
    assert sent_data["results"] == results
    assert kwargs['headers'] == {'Content-Type': 'application/json'}
    assert kwargs['method'] == 'POST'

def test_workflow_webhook_config():
    workflow = Workflow(
        description="Test Workflow",
        steps=[Step(command="status")],
        webhook_url="https://example.com/webhook"
    )
    assert workflow.webhook_url == "https://example.com/webhook"

    config_dict = {
        "repositories": [{"name": "r1", "path": ".", "groups": ["g1"]}],
        "workflows": {
            "test": {
                "description": "desc",
                "steps": [{"command": "status"}],
                "webhook_url": "https://example.com/webhook"
            }
        }
    }
    config = Config(**config_dict)
    assert config.workflows["test"].webhook_url == "https://example.com/webhook"
    assert "g1" in config.repositories[0].groups
