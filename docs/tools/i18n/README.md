![toolkit-logo-banner.png](/docs/assets/toolkit-logo-banner.png)

# 🌐 Internationalization Tools (i18n)

This folder contains helper scripts and automation tools used to manage translated documentation for the Git Toolkit project.

The goal is to ensure that all supported languages maintain **structural parity** with the canonical English documentation and are properly linted, checked, and bannered before release.

---

## 📂 Folder Overview

```

docs/
├── en/                 # Canonical English docs (source of truth)
├── es/                 # Spanish translations
├── fr/                 # French translations
└── tools/
└── i18n/
├── sync\_docs\_structure.py     # Clone folder layout
├── validate\_headers.py        # Lint titles, headers, metadata
├── banner\_injector.sh         # Add banner to all files
└── README.md                  # You are here

````

---

## 🔧 Available Scripts

### 🧱 `sync_docs_structure.py`

🔄 **Syncs folder structure from English docs into other languages.**  
- Ensures each folder in `docs/en/` exists in every `docs/<lang>/`
- Creates empty `.placeholder` files as needed
- Does **not** copy Markdown files—only folder hierarchy

```bash
python docs/tools/i18n/sync_docs_structure.py
````

✅ Output: mirrored folder layout across `docs/fr/`, `docs/es/`, etc.

---

### 🧠 `validate_headers.py`

🔍 **Checks all Markdown files for proper metadata, headers, and icons.**

* Validates title case
* Ensures icons appear in first-level headings
* Confirms presence of required metadata blocks
* Lints inline formatting, heading levels, spacing

```bash
python docs/tools/i18n/validate_headers.py
```

✅ Output: warnings or errors if files are missing required structure.

---

### 🖼 `banner_injector.sh`

🖼 **Automatically inserts the Git Toolkit logo/banner at the top of every Markdown file.**

* Skips already-bannered files
* Supports multiple languages

```bash
bash docs/tools/i18n/banner_injector.sh
```

✅ Output: updated `.md` files with standardized top banner block.

---

## 🚦 Workflow Overview

```text
Step 1: Edit docs in English (`/docs/en/`)
Step 2: Run sync_docs_structure.py to scaffold language folders
Step 3: Translate Markdown manually or with tooling
Step 4: Run validate_headers.py and banner_injector.sh
Step 5: CI verifies doc structure and metadata
```

---

## 📦 Related Files
* [WORKFLOW](/.github/WORKFLOW.md)
* [DOC SYNC](/.github/DOC_SYNC.md)
* [TRANSLATION STATUS POLICY](../../en/architecture/translation-status-policy.md)
* [HEADER POLICY](../../en/architecture/header-policy.md)

---

## 📜 Guidelines

* Never commit changes directly into `/docs/<lang>/` without syncing with `/docs/en/`
* All top-level headings must include section icons (e.g. `## 🔧 Installation`)
* Each translated folder must contain `README.md`, even if minimal
* Use `.syncignore` (coming soon) to skip folders or files from sync validation

---

*Last updated: 2025-07-16*
*Maintainer: @phpwalter*
