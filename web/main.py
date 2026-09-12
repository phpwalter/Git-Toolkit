"""Experimental Git Toolkit web shell.

The CLI remains the supported product surface for the 1.0 release. This module
exists only to provide a stable health/status boundary for future UI work.
Install the optional ``web`` dependency group before running it.
"""

from fastapi import FastAPI

from git_toolkit.version import __version__

app = FastAPI(title="Git Toolkit Experimental Web", version=__version__)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "Git Toolkit",
        "version": __version__,
        "status": "experimental",
        "supported_interface": "git-toolkit CLI",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}
