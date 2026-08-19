"""Config loader sanity tests."""
from __future__ import annotations

from pathlib import Path

import yaml

from katala_research.config import (
    CreativityConfig,
    ResearchPrefs,
    load_prefs,
)


def test_defaults_have_anti_bubble_weights():
    p = ResearchPrefs()
    w = p.creativity.weights
    # The whole point: discovery must be non-trivial.
    assert 0.20 <= w.discovery <= 0.50
    assert w.relevance + w.discovery + w.risk > 0.0
    # Risk weight should be smaller than discovery (we penalize but don't dominate).
    assert w.risk < w.discovery


def test_load_prefs_from_yaml(tmp_path: Path):
    cfg = {
        "language": "en",
        "default-breadth": 6,
        "creativity": {"weights": {"relevance": 0.6, "discovery": 0.3, "risk": 0.1}},
    }
    f = tmp_path / "prefs.yaml"
    f.write_text(yaml.safe_dump(cfg))
    p = load_prefs(f)
    assert p.language == "en"
    assert p.default_breadth == 6
    assert p.creativity.weights.discovery == 0.3


def test_load_prefs_falls_back_to_example(tmp_path: Path):
    """When no user file exists, the bundled example.yaml should load cleanly."""
    nonexistent = tmp_path / "nope.yaml"
    p = load_prefs(nonexistent)
    # Defaults / example must be valid.
    assert isinstance(p, ResearchPrefs)
    assert isinstance(p.creativity, CreativityConfig)


def test_selector_constraints_are_meaningful():
    p = ResearchPrefs()
    s = p.creativity.selector
    assert 0.0 < s.discovery_floor_ratio < 1.0
    assert 0.0 < s.domain_cap_ratio < 1.0
    assert 0.0 < s.paradigm_cap_ratio < 1.0
    assert s.must_include_counter is True
