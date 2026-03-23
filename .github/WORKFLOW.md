<!--
 file: WORKFLOW.md
 path: L:/var/www/Git-Toolkit/.github/WORKFLOW.md
 version: 1.0.0
 date: 2026-03-13
 author: Walter Torres
 copyright: Copyright 2026, Git-Toolkit.
 license: MIT
 maintainer: Git-Toolkit Team
 status: dev

 Outlines the official development workflow for the Git Toolkit project.
-->

# ⚙️ Project Workflow

This document outlines the official development workflow for the **Git Toolkit** project, including branching strategy, pull request process, release automation, CI/CD policies, and contributor roles.

---

## 📑 Table of Contents

- [🚧 Workflow Overview](#-workflow-overview)
- [🌲 Branching Strategy](#-branching-strategy)
- [🔁 Pull Request Process](#-pull-request-process)
- [🚀 Release Process](#-release-process)
- [🔄 CI/CD Integration](#-cicd-integration)
- [🛠️ Tools Used](#️tools-used)
- [👥 Roles & Responsibilities](#-roles--responsibilities)
- [🔗 Related Policies](#-related-policies)

---

## 🚧 Workflow Overview

We follow a **trunk-based development model**:

- All work starts from the `main` branch
- Contributors create topic branches (`feat/*`, `fix/*`, etc.)
- Pull requests (PRs) must pass all checks and reviews before merging
- Releases are driven by commit history and managed automatically

This model encourages small, frequent, and verifiable contributions.

---

## 🌲 Branching Strategy

All branches are created from `main`. Work should be isolated, specific, and short-lived.

### 🏷️ Branch Naming

Branch names **must begin with an approved prefix** to support automation and enforce consistent practices. Examples include:

- `feat/`: New features
- `fix/`: Bug fixes
- `docs/`: Documentation changes
- `refactor/`   : Code cleanup or restructuring with no behavior change
- `chore/`     : Dependencies, formatting, renaming, configuration, etc.
- `ci/`        : CI/CD config, GitHub Actions, release workflows
- `test/`      : Unit, integration, or regression tests
- `perf/`      : Performance tuning or optimization
- `i18n/`      : Localization and translation changes
- `style/`     : Code styling, spacing, linting, formatting
- `security/`  : Vulnerability patches, secrets removal, hardening steps
- `sync/`      : Auto-synced or bulk-generated content (e.g. translations)
- `hotfix/`    : Urgent patches targeting `main` or production branches

📘 For the full list of accepted prefixes, best practices, and enforcement plans, see:  
👉 [`Branch Naming Guidelines`](../docs/en/branch-naming-guidelines.md)
[//]: # (auto-link-to-branch-naming-guidelines)

---

## 🔁 Pull Request Process

1. Create a new branch from `main` using an approved prefix
2. Use semantic commit messages (e.g., `feat:`, `fix:`)
3. Push and open a PR with a clear title and body
4. PR must pass:
   - ✅ Linting (`black`, `flake8`)
   - ✅ Tests (`pytest`)
   - ✅ Review by at least one maintainer
5. Follow the preferred merge strategy (squash, rebase, or merge — see [GOVERNANCE.md](./GOVERNANCE.md))

---

## 🚀 Release Process

- All merges to `main` are versioned automatically using semantic-release
- PRs tagged with `feat:` or `fix:` will increment version numbers accordingly
- `release.yml` handles tagging, changelog updates, and distribution
- Monthly release cadence with exceptions for urgent fixes

---

## 🔄 CI/CD Integration

Our CI/CD is powered by **GitHub Actions** and includes:

| Trigger                | Actions                                  |
|------------------------|------------------------------------------|
| PR to `main`           | Lint, test, coverage check               |
| Push to branch         | Branch validation, testing               |
| Tag creation           | Release pipeline, changelog, packaging   |
| Nightly/monthly runs   | Auto-sync docs, stale branch cleanup     |

We use `release.yml`, `ci.yml`, and `docs-sync.yml` under `.github/workflows/`.

---

<a id="tools-used"></a>
### 🛠️ Tools Used

| Tool           | Purpose                     |
|----------------|-----------------------------|
| Git Toolkit    | CLI wrapper & config runner |
| GitPython      | Git automation layer        |
| black          | Python formatter            |
| flake8         | Linting and static analysis |
| pytest         | Test runner                 |
| Codecov        | Coverage reporting          |
| GitHub Actions | CI/CD automation            |

---

## 👥 Roles & Responsibilities

| Role         | Responsibilities                                          |
|--------------|-----------------------------------------------------------|
| Maintainers  | Review/merge PRs, manage roadmap, enforce standards       |
| Contributors | Submit PRs, follow all guidelines, participate in reviews |
| CI Bot       | Run all validation, format/lint, sync, and release flows  |

---

## 🔗 Related Policies

- [CONTRIBUTING](./CONTRIBUTING.md)
- [CODE of CONDUCT](./CODE_OF_CONDUCT.md)
- [GOVERNANCE](./GOVERNANCE.md)
- [Branch Naming Guidelines](../docs/en/branch-naming-guidelines.md)
- [DOC SYNC](./DOC_SYNC.md)
- [SYNC PROCESS](./SYNC_PROCESS.md)

---

_Last updated: 2025-07-16_  
_Next review: 2026-07-01_
