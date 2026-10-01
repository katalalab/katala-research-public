from __future__ import annotations

import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / ".github" / "workflows" / "ci.yml"
SHA_PIN = re.compile(r"^[0-9a-f]{40}$")


def _workflow() -> dict:
    return yaml.safe_load(CI.read_text(encoding="utf-8"))


def _pinned_step(steps: list[dict], action: str) -> dict:
    """Return the step using ``action``, asserting it is pinned to a full commit SHA."""
    matches = [step for step in steps if str(step.get("uses", "")).partition("@")[0] == action]
    assert len(matches) == 1, f"expected exactly one {action} step"
    ref = matches[0]["uses"].partition("@")[2]
    assert SHA_PIN.match(ref), f"{action} must be pinned to a full commit SHA, got {ref!r}"
    return matches[0]


def test_python_runtime_is_pinned_for_ci() -> None:
    assert (ROOT / ".python-version").read_text(encoding="utf-8").strip() == "3.11"

    steps = _workflow()["jobs"]["verify"]["steps"]
    setup_python = _pinned_step(steps, "actions/setup-python")

    assert setup_python["with"]["python-version-file"] == ".python-version"


def test_ci_uses_locked_uv_verify_entrypoint() -> None:
    workflow = _workflow()
    steps = workflow["jobs"]["verify"]["steps"]

    assert workflow["permissions"] == "read-all"
    assert workflow["jobs"]["verify"]["runs-on"] == "ubuntu-latest"
    _pinned_step(steps, "actions/checkout")

    setup_uv = _pinned_step(steps, "astral-sh/setup-uv")
    assert setup_uv["with"]["enable-cache"] is True
    assert "pyproject.toml" in setup_uv["with"]["cache-dependency-glob"]
    assert "uv.lock" in setup_uv["with"]["cache-dependency-glob"]

    runs = [step.get("run") for step in steps]
    assert "uv sync --locked --extra dev" in runs
    assert "scripts/verify.sh" in runs
