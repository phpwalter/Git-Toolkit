![toolkit-logo-banner.png](../docs/assets/toolkit-logo-banner.png)

# 🛡️ Security Policy – Git Toolkit

We take the security of our users and contributors seriously. This document outlines the official policy for reporting vulnerabilities and how they are handled by the Git Toolkit maintainers.

---

## 📦 Supported Versions

We currently support **only the `main` branch** and the latest tagged release of Git Toolkit.

| Version               | Supported? |
|-----------------------|------------|
| `main`                | ✅          |
| Latest tagged release | ✅          |
| Older versions        | ❌          |

---

## 🕵️‍♂️ Reporting a Vulnerability

If you discover a potential security issue in Git Toolkit, please **report it privately and responsibly.**  
Do **not** disclose it publicly until it has been reviewed and fixed.

### 🔐 GitHub (Preferred)

If available, please use GitHub’s [Private Vulnerability Reporting](https://github.com/phpwalter/Git-Toolkit/security/advisories).

### 📧 Email

Alternatively, contact the **Git Toolkit Security Team**:

**Email:** [security@bluewatermvc.org](mailto:security@bluewatermvc.org)

> We commit to responding within **5 working days** to any valid security issue.

---

## 📝 Suggested Email Template

```

Subject: \[SECURITY] Vulnerability Report for Git Toolkit

Git Toolkit version: \[e.g. 0.3.0]
Environment: \[OS, Python version, context]

Issue Summary:
\[A concise but clear summary of the issue.]

Steps to Reproduce:
\[Optional — only if reproduction is non-obvious.]

Impact:
\[What could an attacker do? Is this high/medium/low severity?]

Suggested Fix (if known):
\[Any recommendation or PR idea.]

Reporter Info:
\[Name, GitHub handle (optional), contact email]

```

---

## 🔄 What Happens Next?

- You will receive confirmation of your report within 1–2 business days.
- The maintainers will investigate and verify the issue.
- A fix will be proposed, tested, and merged privately (if possible).
- A CVE will be requested (if needed).
- The issue will be publicly disclosed only **after the patch is released.**

---

## ⚖️ Coordinated Disclosure

We believe in responsible disclosure.

We aim to resolve all critical vulnerabilities within **14 days**.  
Please avoid public disclosure until we confirm a fix is deployed or communicate otherwise.

---

## 🎯 Scope

Security issues include (but are not limited to):
- Arbitrary code execution via Git Toolkit commands or config
- Unsafe default behavior or YAML injection vectors
- Permission escalation when running tool commands
- Remote command execution via hooks/plugins

---

## 🛡️ Preventive Practices

Git Toolkit enforces:
- Protected branch rules and no-force-push defaults
- Isolation of plugins and restricted shell execution
- Regular dependency checks and code scans via CI/CD
- Code linting, bandit scans, and automated tests with ≥80% coverage (target)

---

## 📘 Licensing

Git Toolkit is licensed under the [MIT License](../LICENSE).

---

## 🔗 Related Policies

- [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)  
- [CONTRIBUTING.md](./CONTRIBUTING.md)  
- [GOVERNANCE.md](./GOVERNANCE.md)  
- [CHARTER.md](../CHARTER.md)  
- [SYNC_PROCESS.md](./SYNC_PROCESS.md)

---

_Last updated: 2025-07-16_  
_Next review: 2026-07-01_
