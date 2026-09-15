from __future__ import annotations

import statistics
import time
from pathlib import Path

from git_toolkit.config import load_config


def _measure(fn, iterations: int = 20) -> dict[str, float]:
    samples: list[float] = []
    for _ in range(iterations):
        started = time.perf_counter()
        fn()
        samples.append((time.perf_counter() - started) * 1000)
    return {
        "min_ms": min(samples),
        "median_ms": statistics.median(samples),
        "max_ms": max(samples),
    }


def benchmark_config_load(path: str = ".git-toolkit.yml") -> dict[str, float]:
    config_path = Path(path)
    return _measure(lambda: load_config(config_path))


def main() -> None:
    result = benchmark_config_load()
    print("config_load", result)
    if result["median_ms"] > 1000:
        raise SystemExit("Configuration loading exceeded the 1000ms median target")


if __name__ == "__main__":
    main()
