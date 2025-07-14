# 🛠️ Developer Workflow & CI/CD Guide

This document outlines how contributors should work with the Bluewater repositories. It covers source management, branching strategy, coding standards, documentation rules, translations, review flow, CI/CD, and project coordination.

> For multilingual documentation and translation publishing, see [`DOCS_SYNC.md`](../docs/DOCS_SYNC.md).  
> For shared tool and automation sync, see [`SYNC_PROCESS.md`](./SYNC_PROCESS.md).

---

## 🧭 Workflow Summary (At a Glance)

| Area                 | Standard / Source           |
|----------------------|-----------------------------|
| Code Branching       | Trunk-based (`main`)        |
| Docs Directory       | `/docs/{lang}`              |
| Translation Sync     | `sync_docs_structure.py`    |
| Commit Style         | Conventional Commits        |
| Doc Metadata         | Auto-generated header block |
| CI/CD                | GitHub Actions              |
| Issue Tracking       | GitHub Projects + Labels    |

---

## 📦 Codebase Structure

| Path                 | Description                       |
|----------------------|-----------------------------------|
| `/technical/`        | Internal dev & system design docs |
| `/docs/en/`          | Primary English content           |
| `/docs/<lang>/`      | Synced translations               |
| `/git_toolkit/`      | Dev scripts and utilities         |
| `/tools/`            | Helper scripts for CI/Docs/etc.   |

---

## 🌲 Branching Strategy

We follow a **trunk-based model**:

- `main`: Always stable and CI-verified
- `feature/*`: Short-lived for features/fixes
- `hotfix/*`: Urgent/emergency patches

---

## 🧾 Commit Naming Conventions

Use **Conventional Commits**:

```

<type>(optional-scope): description

Types: feat, fix, chore, docs, refactor, test, build, ci
Example: feat(i18n): add new language banners to sync script

````

---

## 📄 Documentation Rules

- All Markdown requires a **metadata block**:
  ```markdown
  ---
  title: Quickstart
  description: Guide to get started with the CLI
  ---
  ````

* Use only approved directory structure
* All new English docs go in `docs/en/`
* Run:

  ```bash
  python3 git_toolkit/tools/i18n/sync_docs_structure.py
  ```

---

## 🌍 Translations

See [`DOCS_SYNC.md`](../docs/DOCS_SYNC.md) for the full translation + publishing pipeline. Key rules:

* Don’t touch `/docs/` — it’s auto-generated
* Sync via `git_toolkit`
* Metadata and language bars are injected automatically
* Navigation must be updated across **all** languages

---

## ✅ PR Process

1. Open PR early; mark WIP if needed
2. Fill out PR template (auto-generated in `.github`)
3. CI runs:

   * Lint, tests, doc header checks, translation validation
4. Get approval from at least 1 reviewer
5. Merge; GitHub deletes the branch

---

## 🔐 CI Rules

* Runs on every push & PR to `main`
* Validates:

  * Markdown lint
  * Metadata headers
  * Sync structure (via `git_toolkit`)
  * No changes to protected paths (e.g. `/docs/`)

---

## 🛡️ Protected Branches

* `main` is protected by:

  * ✅ Required reviews
  * ✅ Status checks (CI)
  * ✅ No force-push
* All PRs must pass validation before merge

---

## 🗃️ Project Management

We use:

* GitHub Projects for roadmap and tracking
* Labels:

  * `needs-docs`, `needs-i18n`, `needs-review`
* Milestones: Only for major feature blocks

---

## 🔗 Related Documents

* [CONTRIBUTING.md](./CONTRIBUTING.md)
* [SYNC\_PROCESS.md](./SYNC_PROCESS.md)
* [DOCS\_SYNC.md](../docs/DOCS_SYNC.md)
* [SECURITY.md](./SECURITY.md)
* [GOVERNANCE.md](./GOVERNANCE.md)

---

_LastUpdate: 2025-07-14_<br>
_Next Review: 2026-07-01_
