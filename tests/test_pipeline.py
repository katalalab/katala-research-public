"""Tests for pipeline stages outside of scoring/selector (covered separately)."""
from __future__ import annotations

from katala_research.pipeline.filter import prefilter_by_banned_domains
from katala_research.primitives.read import StubReadBackend, read_with_fallback
from katala_research.primitives.search import StubSearchBackend
from katala_research.pipeline.hydrator import hydrate
from katala_research.types import Candidate


def test_banned_domain_prefilter():
    cands = [
        Candidate(url="https://medium.com/post"),
        Candidate(url="https://arxiv.org/abs/1"),
        Candidate(url="https://quora.com/q"),
    ]
    kept, rejected = prefilter_by_banned_domains(cands, ["medium.com", "quora.com"])
    assert len(kept) == 1
    assert kept[0].url == "https://arxiv.org/abs/1"
    assert len(rejected) == 2
    for r in rejected:
        assert any("banned-domain" in f for f in r.score.gate_failures)


def test_stub_search_returns_diverse_results():
    backend = StubSearchBackend()
    hits = backend.search("filter bubble", limit=8)
    assert len(hits) >= 5
    domains = {h.url.split("/")[2] for h in hits}
    # The stub corpus is intentionally diverse — should hit multiple domains.
    assert len(domains) >= 5


def test_stub_search_is_deterministic_per_query():
    backend = StubSearchBackend()
    a = backend.search("filter bubble", limit=5)
    b = backend.search("filter bubble", limit=5)
    assert [h.url for h in a] == [h.url for h in b]


def test_hydrate_with_stub_reader_fills_content():
    hits = StubSearchBackend().search("anti bubble", limit=3)
    chain = [StubReadBackend()]
    cands = hydrate(hits, chain, fetch=True)
    assert len(cands) == 3
    for c in cands:
        assert c.content
        assert "Stub content" in c.content


def test_read_fallback_chain_short_circuits():
    chain = [StubReadBackend()]
    page = read_with_fallback(chain, "https://example.com/x")
    assert page.markdown
    assert not page.error
