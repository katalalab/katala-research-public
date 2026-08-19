from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / ".github" / "workflows" / "ci.yml"


def _workflow() -> dict:
    return yaml.safe_load(CI.read_text(encoding="utf-8"))


def test_python_runtime_is_pinned_for_ci() -> None:
    assert (ROOT / ".python-version").read_text(encoding="utf-8").strip() == "3.11"

    steps = _workflow()["jobs"]["verify"]["steps"]
    setup_python = next(step for step in steps if step.get("uses") == "actions/setup-python@v6")

    assert setup_python["with"]["python-version-file"] == ".python-version"


def test_ci_uses_locked_uv_verify_entrypoint() -> None:
    workflow = _workflow()
    steps = workflow["jobs"]["verify"]["steps"]

    assert workflow["permissions"] == "read-all"
    assert workflow["jobs"]["verify"]["runs-on"] == "ubuntu-latest"
    assert any(step.get("uses") == "actions/checkout@v7" for step in steps)

    setup_uv = next(step for step in steps if step.get("uses") == "astral-sh/setup-uv@v8")
    assert setup_uv["with"]["enable-cache"] is True
    assert "pyproject.toml" in setup_uv["with"]["cache-dependency-glob"]
    assert "uv.lock" in setup_uv["with"]["cache-dependency-glob"]

    runs = [step.get("run") for step in steps]
    assert "uv sync --locked --extra dev" in runs
    assert "scripts/verify.sh" in runs
