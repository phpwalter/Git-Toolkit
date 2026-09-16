# Experimental Web Shell

The `web/` directory is not part of the Git Toolkit 1.0 supported interface. The supported product surface is the `git-toolkit` CLI.

This directory currently provides only a minimal FastAPI status/health boundary for future UI work. Install optional dependencies with:

```bash
python -m pip install -e ".[web]"
```

Then run:

```bash
uvicorn web.main:app --reload
```

Available endpoints:

- `GET /` — product/version/status metadata
- `GET /health` — health check

Do not build new product behavior into the web shell until the CLI, policy engine, configuration model, workflow engine, and cross-platform release gates are stable for 1.0.
