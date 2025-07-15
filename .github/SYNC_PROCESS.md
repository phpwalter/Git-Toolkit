# 🔄 Script & Tool Synchronization Process

This document defines how we synchronize shared scripts, Git hooks, workflows, and reusable automation components across Bluewater repositories.

> For multilingual documentation and translation publishing workflows, see [`DOCS_SYNC.md`](../docs/DOCS_SYNC.md).

---

## 📦 What Gets Synced?

The following items are synced from source repositories (typically `bluewater-scripts` or `bluewater-framework`) into downstream projects:

| Path / File             | Purpose                               |
|-------------------------|----------------------------------------|
| `git_toolkit/`          | Shared CLI tools, Git hook logic       |
| `.github/`              | GitHub workflows, issue templates      |
| `config_default.yaml`   | Baseline config for onboarding scripts |

---

## 🧰 Manual Sync Steps

Recommended for low-frequency changes or ad hoc updates:

```bash
cd ~/code/target-repo

# Sync scripts
rsync -av --exclude '__pycache__' ../bluewater-scripts/git_toolkit/ ./git_toolkit/
rsync -av ../bluewater-scripts/.github/ ./.github/

# Commit
git add .
git commit -m "chore(sync): update shared scripts from bluewater-scripts"
````

> 🧠 Always review diffs before pushing to prevent overwriting repo-specific changes.

---

## 🤖 Automated Sync via GitHub Actions

You can automate weekly or on-demand updates using a workflow like this:

```yaml
name: Sync Shared Tooling

on:
  schedule:
    - cron: '0 4 * * 1'  # Mondays at 4am UTC
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Source
        uses: actions/checkout@v4
        with:
          repository: org/bluewater-scripts
          token: ${{ secrets.GH_PAT }}
          path: bluewater-scripts

      - name: Checkout Target
        uses: actions/checkout@v4
        with:
          path: target

      - name: Perform Sync
        run: |
          rsync -av bluewater-scripts/git_toolkit/ target/git_toolkit/
          rsync -av bluewater-scripts/.github/ target/.github/
          cd target
          git config user.name "sync-bot"
          git config user.email "bot@example.org"
          git add .
          git commit -m "chore(sync): weekly sync from bluewater-scripts" || echo "No changes"
          git push origin main
```

> Requires `GH_PAT` secret with write access to target repo.

---

## ⏱️ Recommended Sync Frequencies

| Component            | Frequency | Sync Type |
| -------------------- | --------- | --------- |
| `git_toolkit/`       | Weekly    | Automated |
| `.github/` workflows | Monthly   | Automated |
| Config files         | As needed | Manual    |

---

## ✅ Commit Guidelines

* Use: `chore(sync): <brief description>`
* Include upstream references if non-trivial
* Do not combine sync commits with local logic or features

---

## 🛠 Tooling Integration

Many of the tools synchronized here support or enforce workflows used in:

* `pre-commit` hooks across repos
* GitHub Action template enforcement
* CI build consistency
* Input validation and API safety

> These scripts may also support multilingual validation. See [`DOCS_SYNC.md`](../docs/DOCS_SYNC.md) for translation-related sync processes.

---

## 🔗 Related Sync Domains

* [`DOCS_SYNC.md`](../docs/DOCS_SYNC.md): Translations, multilingual structure, and publishing
* [`CONTRIBUTING.md`](../.github/CONTRIBUTING.md)
* [`SECURITY.md`](../.github/SECURITY.md)
* [`GOVERNANCE.md`](../.github/GOVERNANCE.md)

---

_LastUpdate: 2025-07-12_<br>
_Next Review: 2026-07-01_
