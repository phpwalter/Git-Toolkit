from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Any


class ExitCode(IntEnum):
    OK = 0
    OPERATION_FAILED = 1
    USAGE = 2
    CONFIGURATION = 3
    POLICY = 4
    AUTHENTICATION = 5
    GIT = 6
    INTERNAL = 70


@dataclass(frozen=True)
class ErrorContext:
    command: str | None = None
    repository: str | None = None
    path: str | None = None
    rule: str | None = None
    details: dict[str, Any] | None = None


class ToolkitError(Exception):
    code = "toolkit.error"
    exit_code = ExitCode.OPERATION_FAILED

    def __init__(
        self,
        message: str,
        *,
        remediation: str | None = None,
        context: ErrorContext | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.remediation = remediation
        self.context = context or ErrorContext()

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "code": self.code,
            "message": self.message,
            "exit_code": int(self.exit_code),
        }
        if self.remediation:
            payload["remediation"] = self.remediation
        context = {
            key: value
            for key, value in self.context.__dict__.items()
            if value is not None
        }
        if context:
            payload["context"] = context
        return payload

    def render(self) -> str:
        parts = [f"{self.code}: {self.message}"]
        if self.context.repository:
            parts.append(f"repository={self.context.repository}")
        if self.context.command:
            parts.append(f"command={self.context.command}")
        if self.context.rule:
            parts.append(f"rule={self.context.rule}")
        if self.remediation:
            parts.append(f"remediation={self.remediation}")
        return " | ".join(parts)


class UsageError(ToolkitError):
    code = "usage.invalid"
    exit_code = ExitCode.USAGE


class ConfigurationError(ToolkitError):
    code = "config.invalid"
    exit_code = ExitCode.CONFIGURATION


class ValidationError(ToolkitError):
    code = "validation.failed"
    exit_code = ExitCode.USAGE


class PolicyError(ToolkitError):
    code = "policy.denied"
    exit_code = ExitCode.POLICY


class AuthenticationError(ToolkitError):
    code = "auth.failed"
    exit_code = ExitCode.AUTHENTICATION


class GitOperationError(ToolkitError):
    code = "git.operation_failed"
    exit_code = ExitCode.GIT


def error_result(error: ToolkitError, *, name: str = "toolkit") -> dict[str, Any]:
    return {
        "name": name,
        "success": False,
        "message": error.render(),
        "error": error.to_dict(),
    }
