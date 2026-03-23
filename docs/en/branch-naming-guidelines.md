![toolkit-logo-banner.png](/docs/assets/toolkit-logo-banner.png)

# 🏷️ Branch Naming Guidelines

This document defines the required branch naming convention for the **Git Toolkit** project.

All contributors **must use an approved prefix** when creating branches. This supports:

- CI/CD automation
- Release tooling
- Governance and policy enforcement
- Clear communication across contributors

---

## ✅ Approved Branch Prefixes

| Prefix        | Description                                                  |
|---------------|--------------------------------------------------------------|
| `feat/`       | New features or enhancements                                 |
| `fix/`        | Bug fixes or regressions                                     |
| `docs/`       | Documentation updates (Markdown, guides, READMEs)            |
| `refactor/`   | Code cleanup or restructuring with no behavior change        |
| `chore/`      | Dependencies, formatting, renaming, configuration, etc.      |
| `ci/`         | CI/CD config, GitHub Actions, release workflows              |
| `test/`       | Unit, integration, or regression tests                       |
| `perf/`       | Performance tuning or optimization                           |
| `i18n/`       | Localization and translation changes                         |
| `style/`      | Code styling, spacing, linting, formatting                   |
| `security/`   | Vulnerability patches, secrets removal, hardening steps      |
| `sync/`       | Auto-synced or bulk-generated content (e.g. translations)    |
| `hotfix/`     | Urgent patches targeting `main` or production branches       |

---

## 🧪 Examples

- `feat/plugin-system`
- `fix/tag-generator-bug`
- `docs/code-of-conduct-update`
- `refactor/cli-arg-parser`
- `chore/update-dependencies`
- `ci/test-release-tagging`
- `i18n/es-readme-translation`
- `security/remove-hardcoded-secret`
- `sync/i18n-pull-2025-07-16`

---

## 🔐 Enforcement (Planned)

We aim to enforce these naming rules via:

- Git Toolkit CLI (e.g. `git-toolkit branch create`)
- Git hooks (`pre-push`, `pre-commit`)
- CI branch validation steps

You will be notified during local execution or CI if the branch name violates rules.

---

## 💡 Tips & Best Practices

- Use lowercase and hyphens (not underscores or spaces)
- Be concise and specific
- Reference issues or PRs with numbers (e.g. `fix/login-redirect-#192`)
- Avoid emojis or non-ASCII characters

---

## 📚 Related

- [WORKFLOW.md](./WORKFLOW.md)
- [CONTRIBUTING.md](./CONTRIBUTING.md)
- [GOVERNANCE.md](./GOVERNANCE.md)

---

_Last updated: 2025-07-16_  
_Next review: 2026-07-01_
