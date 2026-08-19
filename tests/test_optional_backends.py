"""Scrapling / pdf-inspector must fail gracefully when their optional deps are missing."""
from __future__ import annotations

from katala_research.primitives.read import (
    PdfInspectorBackend,
    ScraplingBackend,
    StubReadBackend,
    read_with_fallback,
)


def test_scrapling_unavailable_when_dep_missing():
    """If scrapling is not installed, backend should report error but not crash."""
    s = ScraplingBackend()
    # We can't reliably assert which state we're in, but we CAN assert that
    # whatever the state, .read() doesn't raise.
    page = s.read("https://example.com/")
    if not s.available:
        assert page.error and "scrapling" in page.error.lower()
    else:
        # If installed in the test env, accept either success or graceful error.
        assert page.markdown or page.error


def test_pdf_inspector_unavailable_when_dep_missing():
    p = PdfInspectorBackend()
    page = p.read("https://example.com/foo.pdf")
    if not p.available:
        assert page.error and "pypdf" in page.error.lower()
    else:
        assert page.markdown or page.error


def test_pdf_inspector_rejects_non_pdf():
    p = PdfInspectorBackend()
    if not p.available:
        return  # skip if pypdf isn't installed
    page = p.read("https://example.com/")
    assert page.error and "non-pdf" in page.error.lower()


def test_read_chain_falls_through_unavailable():
    """Even if all optional backends are unavailable, stub should catch."""
    chain = [ScraplingBackend(), PdfInspectorBackend(), StubReadBackend()]
    page = read_with_fallback(chain, "https://example.com/something")
    assert page.markdown
    assert "Stub content" in page.markdown
