# Git Toolkit 1.0 Support Boundaries

## Supported in 1.0

The supported product surface is the Python command-line interface and its documented configuration, policy, workflow, hook, plugin, logging, and Git-adapter behavior.

Supported environments:

- Python 3.11 through 3.13.
- Linux, macOS, and Windows.
- Standard Git installations compatible with GitPython.
- Git Credential Manager or standard Git credential helpers for transport authentication.

## Experimental

The `web/` package is experimental. It may expose health/status information but is not a supported administration or workflow UI in 1.0.

## Explicitly post-1.0

The following are outside the 1.0 compatibility promise:

- provider-specific OAuth flows;
- a supported GUI/web control plane;
- non-Git VCS backends;
- workflow DAGs, cross-step output passing, and compensation transactions;
- organization-wide advanced analytics;
- automated documentation translation orchestration.

## Compatibility rule

A 1.x change must not silently alter policy semantics, configuration meaning, exit behavior, plugin API compatibility, or destructive Git-operation behavior. Any incompatible change requires a documented migration path and an appropriate major-version decision.

## Security boundary

Project scripts and local plugins execute code from the project workspace and therefore require explicit trust configuration. Git Toolkit does not infer trust from repository location, ownership, or previous execution.
