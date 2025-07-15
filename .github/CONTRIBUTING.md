
# 🤝 Contributing to Git-Toolkit

Thanks for your interest in improving **Git-Toolkit**! Whether it's code, documentation, or ideas—your input matters! 🚀

---

## 🧭 Table of Contents

1. [Code of Conduct](#code-of-conduct)  
2. [Where to Start](#where-to-start)  
3. [General Guidelines](#general-guidelines)  
4. [Script Style & Standards](#script-style--standards)  
5. [Documentation Standards](#documentation-standards)  
6. [Development Process](#development-process)  
7. [Pull Requests](#pull-requests)  
8. [Issues & Feature Requests](#issues--feature-requests)  
9. [Sync, Integration & Tooling](#sync-integration--tooling)  
10. [Licensing](#licensing)  
11. [Community & Code of Conduct](#community--code-of-conduct)  
12. [Getting Help](#getting-help)  
13. [🌍 Translations](#-translations)

---

## 📜 Code of Conduct

All contributors must follow our [Code of Conduct](CODE_OF_CONDUCT.md).  
Be kind, inclusive, and constructive.

---

## 🧭 Where to Start

- Read the [README.md](../README.md) for project overview
- Browse [open issues](../../issues) and [pull requests](../../pulls)
- See [Governance](GOVERNANCE.md) for project leadership and decision-making

---

## 📌 General Guidelines

- Always be respectful and professional
- Search for existing issues before creating new ones
- Open a discussion or issue before starting major work
- Contributions can include code, docs, ideas, or bug reports

---

## ⚙️ Script Style & Standards

If your contribution includes scripts:

- **Preferred Language**: Python  
- Use Bash/Shell/Batch only when necessary
- Ensure cross-platform compatibility
- Top-of-file comments must include:
  - Script language
  - Author
  - Brief description
- Follow:
  - [PEP8](https://peps.python.org/pep-0008/)
  - Shell/Batch best practices
- Avoid destructive operations
- Validate inputs, avoid hardcoded secrets
- Include example usage in comments or docstrings

---

## 📘 Documentation Standards

Place documentation in appropriate language folders:

```

docs/{lang}/
└── technical/ or architecture/

````

Required for each tool/script:

- Description of purpose
- Configuration options
- Installation and execution
- Any platform-specific notes
- Markdown (`.md`) format only

---

## 🔁 Sync, Integration & Tooling

This repo may be used by:

- CI/CD pipelines
- Git hooks
- Local automation
- Other Bluewater repos

Do not break backward compatibility or dependencies without discussion.  
Ensure automation is robust and clearly logs output/errors.

---

## 🔨 Development Process

1. Fork & branch:
   ```bash
   git clone <repo>
   git checkout -b feature/my-change
   ````

2. Keep your fork updated:

   ```bash
   git remote add upstream <repo>
   git fetch upstream
   git merge upstream/main
   ```
3. Branch naming:

   * `bugfix/...`, `feature/...`, `docs/...`

---

## 📥 Pull Requests

* Use the correct PR template
* PRs must:

  * Be small and focused
  * Reference issues (`Closes #123`)
  * Include related documentation changes
  * Pass lint, tests, and CI
* Clearly describe purpose and impact

---

## 🐞 Issues & Feature Requests

* Check [issues](../../issues) before posting
* Use templates for bugs, features
* Explain how the change will help
* Include affected files or workflows

---

## 📄 Licensing

* All contributions fall under the [Open Software License (OSL 3.0)](LICENSE)
* You must own the code or have the right to submit it
* Preserve license headers where applicable

---

## 🧑‍🤝‍🧑 Community & Code of Conduct

Our values are defined in [CODE\_OF\_CONDUCT.md](CODE_OF_CONDUCT.md).
We enforce a harassment-free and inclusive space for everyone.

---

## 🆘 Getting Help

* Use [GitHub Discussions](../../discussions)
* For security matters, see [SECURITY.md](SECURITY.md)
* Or email: `contact@example.org`

---

## 🌍 Translations

Looking for this guide in another language?

* 🇪🇸 [Español – Cómo contribuir](../docs/es/cómo-contribuir.md)
* 🇫🇷 [Français – Contribuer](../docs/fr/contribuer.md)

For other translated materials:

* [Código de conducta (ES)](../docs/es/código-de-conducta.md)
* [Code de conduite (FR)](../docs/fr/code-de-conduite.md)
* [Gobernanza (ES)](../docs/es/gobernanza.md)
* [Gouvernance (FR)](../docs/fr/gouvernance.md)
* [Seguridad (ES)](../docs/es/seguridad.md)
* [Sécurité (FR)](../docs/fr/sécurité.md)

---

> 🙏 Thank you for helping make this project awesome!

---

_LastUpdate: 2025-07-14_<br>
_Next Review: 2026-07-01_
