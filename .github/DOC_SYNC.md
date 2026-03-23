<!--
 file: DOC_SYNC.md
 path: L:/var/www/Git-Toolkit/.github/DOC_SYNC.md
 version: 1.0.0
 date: 2026-03-13
 author: Walter Torres
 copyright: Copyright 2026, Git-Toolkit.
 license: MIT
 maintainer: Git-Toolkit Team
 status: dev

 Defines how English and translated documentation is structured, maintained, and synchronized across Git Toolkit repositories.
-->

![toolkit-logo-banner.png](../docs/assets/toolkit-logo-banner.png)

# 🌐 Git Toolkit Documentation Sync Policy

This document defines how English and translated documentation is structured, maintained, and synchronized across Git Toolkit repositories.

It outlines folder layout rules, localization strategies, publishing workflows, and commit discipline to ensure a consistent contributor and reader experience across languages.

---

## 🧭 Key Repositories & Tooling

| Repository         | Purpose                                          |
|--------------------|--------------------------------------------------|
| `git-toolkit`      | Primary source of documentation (English + i18n) |
| `git-toolkit-docs` | (Optional) GitHub Pages deployment repo          |
| `docs-sync-tools/` | CLI tools to check structure, sync content, etc. |

Tools involved:
- `sync_docs_structure.py`
- `validate_headers.py`
- `banner_injector.sh`
- Optional MkDocs or custom i18n build tool

---

## 🗂 Folder Rules

### 🔤 Canonical Language: English

All authoritative documentation lives in:

```

docs/en/

```

> 📢 Do **not** edit `docs/fr/`, `docs/es/`, etc. directly—translate from English source only.

### 🏗 Recommended Editable Sources

If editing outside `docs/en/`, use a clean separation:

```

docs-src/           # Editable Markdown sources
docs/en/            # Canonical rendered version
docs/<lang>/        # Auto-generated localized docs

````

---

## 🔄 Documentation Sync Workflow

1. ✍️ English sources are updated under `docs/en/`
2. 🔃 Run `sync_docs_structure.py` to mirror folder names to all supported languages
3. 🌍 Translate new or changed Markdown files
4. 🚫 Avoid modifying auto-generated translations manually
5. ✅ CI validates structure, file parity, and headers

---

## 🧠 Structure Enforcement

Use `sync_docs_structure.py` to:

- Ensure all folders in `docs/en/` exist in `docs/<lang>/`
- Warn if `.md` files are missing in translated folders
- Provide an optional dry-run mode for preview

Run via:

```bash
python docs/tools/i18n/sync_docs_structure.py
````

---

## 📄 Navigation Rules

* Each language must have its own `mkdocs.yml` (or equivalent nav config)
* Navigation order must match English
* Top-level documents (`README.md`, `CONTRIBUTING.md`, etc.) should be present in all languages
* Icons, banner assets, and headers must be synced

---

## 📦 Publishing Workflow (Optional)

If using GitHub Pages or external site deployment:

* Publish from `git-toolkit-docs/`
* Docs are pulled from `git-toolkit/docs/` via Action
* CI should validate and inject headers before push

---

## 🧾 Docs Sync Checklist

Use this before every milestone:

* [ ] ✅ English docs updated (`docs/en/`)
* [ ] ✅ All headings follow title case and include icons
* [ ] ✅ Structure synced via `sync_docs_structure.py`
* [ ] ✅ Localized folders created and populated
* [ ] ✅ CI linting and structure validation pass
* [ ] ✅ No manual edits to `/docs/<lang>/`
* [ ] ✅ Banner images and language bars injected
* [ ] ✅ Navigation files (`mkdocs.yml`) match across languages

---

## 🔗 Related Domains & Policies

* [CHARTER](../CHARTER.md)
* [GOVERNANCE](./GOVERNANCE.md)
* [CONTRIBUTING](./CONTRIBUTING.md)
* [SYNC_PROCESS.md](./SYNC_PROCESS.md)
* [TRANSLATION STATUS POLICY](../docs/en/architecture/translation-status-policy.md)
* [HEADER POLICY](../docs/en/architecture/header-policy.md)

---

_Last updated: 2025-07-16_<br>
_Next review: 2026-07-01_
