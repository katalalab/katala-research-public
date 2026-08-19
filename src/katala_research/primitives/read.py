"""Read primitives — Jina Reader, Defuddle, Scrapling, PdfInspector, Stub.

Per the catalog routing: Defuddle (if installed locally) → Jina Reader (free) → Firecrawl.
Defuddle is optional; v0 default chain is Jina → Defuddle → Stub.

v0.1 additions (optional):
- ScraplingBackend: Python anti-bot scraper for JS-heavy / lightly-defended sites.
  Lazy-loaded; install via `uv sync --extra scrape`.
- PdfInspectorBackend: detects scanned-vs-text PDFs, routes accordingly.
  Lazy-loaded; install via `uv sync --extra scrape`.
"""
from __future__ import annotations

import shutil
import subprocess
from typing import Protocol

import httpx

from ..config import ResearchPrefs
from ..types import FetchedPage


class ReadBackend(Protocol):
    name: str

    def read(self, url: str) -> FetchedPage: ...


class JinaReaderBackend:
    """Free Jina Reader: https://r.jina.ai/<url> → markdown."""

    name = "jina"

    def __init__(self, timeout: float = 20.0):
        self.timeout = timeout

    def read(self, url: str) -> FetchedPage:
        try:
            resp = httpx.get(
                f"https://r.jina.ai/{url}",
                timeout=self.timeout,
                follow_redirects=True,
                headers={"Accept": "text/markdown"},
            )
            resp.raise_for_status()
            md = resp.text or ""
            return FetchedPage(url=url, markdown=md, backend=self.name)
        except httpx.HTTPError as e:
            return FetchedPage(url=url, error=f"jina: {e}", backend=self.name)


class DefuddleBackend:
    """Local `defuddle parse <url> --md` subprocess. Optional."""

    name = "defuddle"

    def __init__(self, timeout: float = 30.0):
        self.timeout = timeout
        self.available = shutil.which("defuddle") is not None

    def read(self, url: str) -> FetchedPage:
        if not self.available:
            return FetchedPage(url=url, error="defuddle not installed", backend=self.name)
        try:
            result = subprocess.run(
                ["defuddle", "parse", url, "--md"],
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
            if result.returncode != 0:
                return FetchedPage(
                    url=url, error=f"defuddle exit {result.returncode}: {result.stderr[:200]}",
                    backend=self.name,
                )
            return FetchedPage(url=url, markdown=result.stdout, backend=self.name)
        except subprocess.TimeoutExpired:
            return FetchedPage(url=url, error="defuddle timeout", backend=self.name)
        except OSError as e:
            return FetchedPage(url=url, error=f"defuddle: {e}", backend=self.name)


class StubReadBackend:
    """Returns the URL slug as faux markdown content. Used by --stub smoke."""

    name = "stub"

    def read(self, url: str) -> FetchedPage:
        slug = url.rsplit("/", 1)[-1] or url
        body = (
            f"# Stub content for {url}\n\n"
            f"This is canned markdown returned by the StubReadBackend so the pipeline "
            f"can run end-to-end without external services. Topic slug: {slug}.\n\n"
            f"Key points:\n"
            f"- Diversity-aware selection improves discovery.\n"
            f"- Filter bubbles arise when preference scores dominate.\n"
            f"- A 25% creativity floor + domain caps mitigates this.\n"
        )
        return FetchedPage(url=url, title=slug, markdown=body, backend=self.name)


class ScraplingBackend:
    """Anti-bot Python scraper. Optional dep; falls back to error if not installed.

    Targets JS-heavy / lightly-defended sites that Jina Reader can't render. For
    Cloudflare-tier defenses, prefer CloakBrowser (separate backend, future).
    """

    name = "scrapling"

    def __init__(self, timeout: float = 30.0):
        self.timeout = timeout
        try:
            from scrapling import Fetcher  # type: ignore
            self._fetcher_cls = Fetcher
            self.available = True
        except Exception:
            self._fetcher_cls = None
            self.available = False

    def read(self, url: str) -> FetchedPage:
        if not self.available:
            return FetchedPage(url=url, error="scrapling not installed", backend=self.name)
        try:
            page = self._fetcher_cls().get(url, timeout=self.timeout)
            # Scrapling's Adaptor exposes .text (raw HTML) and .get_all_text()
            text = ""
            for attr in ("get_all_text", "text"):
                v = getattr(page, attr, None)
                if callable(v):
                    text = v() or ""
                    break
                if isinstance(v, str) and v.strip():
                    text = v
                    break
            if not text:
                return FetchedPage(url=url, error="scrapling: empty text", backend=self.name)
            return FetchedPage(url=url, markdown=text[:50_000], backend=self.name)
        except Exception as e:
            return FetchedPage(url=url, error=f"scrapling: {e}", backend=self.name)


class PdfInspectorBackend:
    """Detect scanned-vs-text PDFs and extract text from the latter.

    Conceptual port of firecrawl/pdf-inspector (Rust) in Python via pypdf.
    Optional dep; non-PDF URLs are passed through as errors so the chain moves on.
    """

    name = "pdf_inspector"

    def __init__(self, timeout: float = 60.0, scanned_threshold: int = 200):
        self.timeout = timeout
        self.scanned_threshold = scanned_threshold
        try:
            import pypdf  # type: ignore
            self._pypdf = pypdf
            self.available = True
        except Exception:
            self._pypdf = None
            self.available = False

    def read(self, url: str) -> FetchedPage:
        if not self.available:
            return FetchedPage(url=url, error="pypdf not installed", backend=self.name)
        if not _looks_like_pdf(url):
            return FetchedPage(url=url, error="pdf_inspector: non-PDF URL", backend=self.name)
        # Download.
        try:
            resp = httpx.get(url, timeout=self.timeout, follow_redirects=True)
            resp.raise_for_status()
            data = resp.content
        except httpx.HTTPError as e:
            return FetchedPage(url=url, error=f"pdf_inspector: download {e}", backend=self.name)
        # Parse.
        try:
            from io import BytesIO
            reader = self._pypdf.PdfReader(BytesIO(data))
            chunks: list[str] = []
            for page in reader.pages:
                try:
                    chunks.append(page.extract_text() or "")
                except Exception:
                    continue
            text = "\n\n".join(c for c in chunks if c.strip())
            if len(text) < self.scanned_threshold:
                return FetchedPage(
                    url=url,
                    error=(
                        f"pdf_inspector: extracted only {len(text)} chars — "
                        f"likely scanned PDF, OCR not available in v0.1"
                    ),
                    backend=self.name,
                )
            return FetchedPage(url=url, markdown=text[:80_000], backend=self.name)
        except Exception as e:
            return FetchedPage(url=url, error=f"pdf_inspector: parse {e}", backend=self.name)


def _looks_like_pdf(url: str) -> bool:
    u = (url or "").lower()
    if u.endswith(".pdf"):
        return True
    # Common preprint server PDF paths
    return any(seg in u for seg in ("/pdf/", "arxiv.org/pdf"))


def build_read_chain(prefs: ResearchPrefs) -> list[ReadBackend]:
    chain: list[ReadBackend] = []
    for name in prefs.read_backend_order:
        if name == "jina":
            chain.append(JinaReaderBackend())
        elif name == "defuddle":
            chain.append(DefuddleBackend())
        elif name == "scrapling":
            chain.append(ScraplingBackend())
        elif name == "pdf_inspector":
            chain.append(PdfInspectorBackend())
        elif name == "stub":
            chain.append(StubReadBackend())
    if not chain:
        chain.append(StubReadBackend())
    return chain


def read_with_fallback(chain: list[ReadBackend], url: str) -> FetchedPage:
    """First backend that returns content without error wins."""
    last_err: str = ""
    for backend in chain:
        page = backend.read(url)
        if page.markdown and not page.error:
            return page
        if page.error:
            last_err = f"{backend.name}: {page.error}"
    return FetchedPage(url=url, error=last_err or "no read backend succeeded")
