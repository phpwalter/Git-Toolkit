# Git Toolkit Project Policies

## Security

Report suspected vulnerabilities privately through the repository security channel. Do not open public issues containing credentials, exploit details, or unredacted sensitive logs.

Supported security controls include dependency auditing, Bandit scanning, trust-gated project scripts/local plugins, protected-branch policy, remote-host policy, and credential-safe remote handling.

## Contributions

All changes must be developed on a feature branch, include tests for behavioral changes, and pass the full CI quality gate before merge. New dependencies require justification and must pass dependency audit.

## Maintainers

Maintainers are responsible for release integrity, branch protection, issue triage, dependency/security review, policy compatibility, and keeping documentation aligned with runtime behavior.

## Support

The supported 1.0 surface is the Python CLI and documented configuration/plugin interfaces. Experimental web code is not a supported production interface.

## Releases

Releases originate only from a green `main` commit. Version, tag, package artifact, changelog entry, and GitHub release must identify the same source commit.

## Community conduct

Project participation requires professional, respectful collaboration focused on technical merit. Harassment, threats, discriminatory conduct, deliberate disruption, and disclosure of private information are not acceptable.

## Issue templates

Bug reports should include version, OS/Python/Git versions, command, configuration excerpt with secrets removed, expected behavior, actual behavior, and reproduction steps.

Feature requests should state the user problem, desired behavior, scope boundary, alternatives considered, and compatibility implications.
