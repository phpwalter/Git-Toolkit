# Security Policy

## Supported versions

Security fixes are provided for the current supported release line and the active development branch preparing the next supported release. Pre-1.0 development snapshots are supported only when they are the current stabilization target.

## Reporting a vulnerability

Do not open a public issue for a suspected security vulnerability that could expose credentials, enable command execution, bypass policy enforcement, or damage repositories.

Use GitHub's private vulnerability reporting capability when available. Include:

- affected Git Toolkit version or commit;
- operating system and Python version;
- affected command or workflow;
- minimal reproduction steps;
- expected and observed behavior;
- security impact;
- whether credentials, repository data, or remote execution are involved.

Do not include real credentials, access tokens, private repository contents, or other secrets in a report.

## Security boundaries

Git Toolkit treats the following as security-sensitive boundaries:

- shell execution;
- project-local scripts and plugins;
- credentials and authentication material;
- force-push and protected-branch operations;
- remote-host allow/deny policy;
- release artifacts and publication workflows.

Project-local scripts and local plugins are disabled by default and must be explicitly enabled for repositories the operator trusts. Git transport authentication remains delegated to Git and the platform credential manager; Git Toolkit must not inject secrets into remote URLs.

## Response policy

A confirmed vulnerability is triaged according to exploitability and impact. Security fixes must not weaken mandatory policy, quality, package-integrity, or release gates merely to restore compatibility.
