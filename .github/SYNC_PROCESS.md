# 🔄 Git-Toolkit Script & Tool Synchronization Process

This document describes how we synchronize and distribute shared scripts, Git hooks, workflows, and automation tooling across the Bluewater project ecosystem.

---

## 🧩 What Gets Synced?

- `git_toolkit/` → Shared Git automation tools and hooks
- `.github/` → GitHub workflows, issue/PR templates, and community docs
- `config_default.yaml` → Bootstrap configuration

---

## ⚙️ Manual Sync Instructions

```bash
cd ~/code/target-repo
rsync -av --exclude '__pycache__' ../bluewater-scripts/git_toolkit/ ./git_toolkit/
rsync -av ../bluewater-scripts/.github/ ./.github/
git add .
git commit -m "chore(sync): update shared scripts from bluewater-scripts"
````

> 💡 Always verify diffs before pushing. No blind overwrites!

---

## 🤖 GitHub Actions – Automated Sync

```yaml
name: Weekly Sync from Bluewater Scripts

on:
  schedule:
    - cron: '0 4 * * 1'
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

      - name: Sync
        run: |
          rsync -av bluewater-scripts/git_toolkit/ target/git_toolkit/
          rsync -av bluewater-scripts/.github/ target/.github/
          cd target
          git config user.name "sync-bot"
          git config user.email "bot@example.org"
          git add .
          git commit -m "chore(sync): weekly update from bluewater-scripts" || echo "No changes"
          git push origin main
```

---

## 📅 Sync Frequency Recommendations

| Item             | Frequency | Sync Type     |
| ---------------- | --------- | ------------- |
| Git hooks / CLI  | Weekly    | Bot or manual |
| GitHub workflows | Monthly   | Bot           |
| Config templates | As needed | Manual        |

---

## ✅ Commit Guidelines

* Format: `chore(sync): ...`
* Only include synced assets, not repo-specific changes
* Link to sync source and changelog when applicable

---

## 📚 References

* [GOVERNANCE.md](../.github/GOVERNANCE.md)
* [SECURITY.md](../.github/SECURITY.md)
* [Translation Process](./DOCS_SYNC.md)

---

*LastUpdate: 2025-07-12*<br>
*Next Review: 2026-07-01*
