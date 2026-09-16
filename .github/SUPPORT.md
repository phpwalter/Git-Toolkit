# Support

Git Toolkit is maintained as a public open-source project.

## Where to ask for help

Use GitHub Issues for reproducible defects, documentation problems, feature requests, and compatibility reports. Include the Git Toolkit version, operating system, Python version, Git version, command executed, relevant configuration with secrets removed, and the complete error output.

## Security reports

Do not file suspected credential exposure or exploitable security defects as public issues. Follow the process in `.github/SECURITY.md`.

## Supported surface

The command-line interface and documented Python package behavior are the supported product surface for the 1.0 line. The `web/` directory is experimental and may change without compatibility guarantees.

## Support boundaries

Git Toolkit cannot override Git hosting-provider rules such as GitHub Push Protection, protected-branch rules, required status checks, or organization policy. When Git rejects an operation, Git Toolkit should surface the underlying reason rather than bypass it.
