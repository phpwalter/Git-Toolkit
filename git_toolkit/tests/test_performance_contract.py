from __future__ import annotations

from unittest.mock import patch

from benchmarks.benchmark_core import _measure, benchmark_config_load


def test_measure_returns_min_median_and_max() -> None:
    readings = iter([1.0, 1.001, 2.0, 2.002, 3.0, 3.003])
    with patch("benchmarks.benchmark_core.time.perf_counter", side_effect=lambda: next(readings)):
        result = _measure(lambda: None, iterations=3)
    assert result["min_ms"] == 1.0
    assert result["median_ms"] == 2.0
    assert result["max_ms"] == 3.0


def test_config_load_benchmark_invokes_loader(tmp_path) -> None:
    config_path = tmp_path / ".git-toolkit.yml"
    config_path.write_text("repositories: []\n", encoding="utf-8")
    with patch("benchmarks.benchmark_core.load_config") as loader:
        result = benchmark_config_load(str(config_path))
    assert loader.call_count == 20
    assert result["median_ms"] >= 0
