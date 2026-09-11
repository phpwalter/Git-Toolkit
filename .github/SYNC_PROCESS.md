<!--
 file: SYNC_PROCESS.md
 path: L:/var/www/Git-Toolkit/.github/SYNC_PROCESS.md
 version: 1.0.0
 date: 2026-03-13
 author: Walter Torres
 copyright: Copyright 2026, Git-Toolkit.
 license: MIT
 maintainer: Git-Toolkit Team
 status: dev

 Outlines how the Git Toolkit project manages code, documentation, and workflow synchronization across downstream repositories.
-->

![toolkit-logo-banner.png](../docs/assets/toolkit-logo-banner.png)

# 🔄 Git Toolkit Sync Process

This document outlines how the **Git Toolkit** project manages code, documentation, and workflow synchronization across downstream repositories. It defines what gets synced, how syncing is performed (manually and automatically), and which policies govern these operations.

---

## 📦 What Gets Synced?

The following project components are maintained **upstream** (in the Git Toolkit canonical repo) and are periodically synchronized downstream into client and dependent repositories:

### From `.github/`

- GitHub Actions workflows (`ci.yml`, `release.yml`, `lint.yml`, etc.)
- Issue templates and community files
- Security, contributing, governance, and charter docs

### From `git_toolkit/`

- Shared CLI logic, plugin structure, and base hooks
- Default configuration schema
- Safety and automation scaffolding

### From `docs/en/`

- Canonical English documentation pages
- Code of Conduct, Security Policy, Governance, Charter
- Translation stubs and sync policies

---

## 🧰 Manual Sync Process

Downstream repositories can be updated from the Git Toolkit upstream by performing the following:

```bash
git remote add upstream https://github.com/phpwalter/git-toolkit.git
git fetch upstream
git checkout -b sync-upstream
git checkout upstream/main -- .github/
git checkout upstream/main -- git_toolkit/
git checkout upstream/main -- docs/en/
````

> 📘 You may exclude or restore specific files using `git restore`, `git rm`, or `.syncignore` rules.

Once complete:

```bash
git commit -m "🔄 Sync from git-toolkit upstream"
git push origin sync-upstream
```

Open a pull request titled:

```
🔄 Sync with Upstream: .github/, git_toolkit/, docs/
```

---

## 🤖 Automated Sync via GitHub Actions

All repositories that wish to **auto-sync** from Git Toolkit can enable the scheduled `sync.yml` GitHub Action:

```yaml
name: Sync from Upstream
on:
  schedule:
    - cron: '0 12 * * 1'  # Every Monday
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Pull upstream content
        run: |
          git config user.name "Git Toolkit Sync Bot"
          git config user.email "sync-bot@git-toolkit.dev"
          git remote add upstream https://github.com/phpwalter/git-toolkit.git
          git fetch upstream
          git checkout -b auto-sync
          git checkout upstream/main -- .github/
          git checkout upstream/main -- git_toolkit/
          git checkout upstream/main -- docs/en/
          git commit -am "🔄 Auto-sync from upstream"
          git push origin auto-sync
```

---

## ⏱️ Sync Frequency Guide

| Target Repo Type       | Suggested Sync Interval     |
|------------------------|-----------------------------|
| Client applications    | Weekly (manual or CI)       |
| Plugin/extension repos | Bi-weekly or monthly        |
| Documentation mirrors  | On-demand or before release |
| Translation branches   | Before milestone cutoff     |

---

## 🧾 Commit & PR Guidelines

Always include:

* `🔄` emoji in commit or PR title
* Summary of synced folders
* Note of exclusions (if any)
* Reviewer tag (if special approvals required)

---

## 🧩 Tooling Integration

To streamline and standardize sync behavior, Git Toolkit may include:

* `.syncignore` — to ignore paths that shouldn't be overwritten
* `sync.sh` or `sync.py` — CLI wrapper for sync actions
* A `Makefile` task (e.g. `make sync-upstream`)
* Git aliases or VS Code tasks

---

## 🔗 Related Sync Domains

| File/Policy                       | Description                                       |
|-----------------------------------|---------------------------------------------------|
| [CHARTER](../CHARTER.md)          | Project scope and lifecycle goals                 |
| [GOVERNANCE](./GOVERNANCE.md)     | Maintainer roles and sync ownership               |
| [CONTRIBUTING](./CONTRIBUTING.md) | Contribution process including sync participation |
| [DOC SYNC](./DOC_SYNC.md)         | Translation, localization, and docs sync policies |

---

_Last updated: 2025-07-16_
_Next review: 2026-07-01_
