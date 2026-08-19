"""OpenReviewSource — ICLR / NeurIPS / COLM submissions + public reviews.

Uses OpenReview API v2 (`https://api2.openreview.net`). Public venues work
without auth. If OPENREVIEW_USERNAME/PASSWORD set, broader access.

The unique value: review COMMENTS are extracted into meta.review_comments,
which the SideEffect can turn into Learning entries — that's "what peer
reviewers actually said about this paper", which no other source provides.
"""
from __future__ import annotations

from typing import Optional

import httpx

from ..config import resolve_env
from ..types import SearchHit
from .base import detect_domain_tag, make_meta


OPENREVIEW_API = "https://api2.openreview.net/notes/search"
OPENREVIEW_NOTES = "https://api2.openreview.net/notes"


class OpenReviewSource:
    name = "openreview"
    peer_review_default = True  # OpenReview venues are peer-reviewed (or under review)
    domain_tags = ["cs"]         # primarily ML/CS venues

    def __init__(self, timeout: float = 20.0):
        self.timeout = timeout
        self.username = resolve_env("OPENREVIEW_USERNAME")
        self.password = resolve_env("OPENREVIEW_PASSWORD")

    def search(self, query: str, *, limit: int = 10) -> list[SearchHit]:
        params = {
            "term": query,
            "limit": min(limit, 25),
            "source": "all",
            "type": "terms",
        }
        try:
            resp = httpx.get(OPENREVIEW_API, params=params, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
        except (httpx.HTTPError, ValueError):
            return []

        hits: list[SearchHit] = []
        for i, note in enumerate(data.get("notes", [])[:limit]):
            hit = self._parse_note(note, rank=i)
            if hit:
                hits.append(hit)
        return hits

    def _parse_note(self, note: dict, *, rank: int) -> Optional[SearchHit]:
        content = note.get("content", {}) or {}
        # OpenReview content is wrapped: {field: {"value": ...}}
        def _v(field: str) -> str:
            f = content.get(field, {})
            return (f.get("value") if isinstance(f, dict) else f) or ""

        title = _v("title")
        abstract = _v("abstract")
        forum_id = note.get("forum") or note.get("id")
        if not forum_id:
            return None
        url = f"https://openreview.net/forum?id={forum_id}"

        venue = _v("venue") or note.get("invitation", "").split("/")[-1]
        publication_date = None
        pdate = note.get("pdate")
        if pdate:
            # ms epoch
            try:
                from datetime import datetime, timezone
                publication_date = datetime.fromtimestamp(pdate / 1000, tz=timezone.utc).date().isoformat()
            except Exception:
                publication_date = None

        # Try to pull a few review comments — best-effort, lightweight.
        review_comments = self._fetch_review_excerpts(forum_id)

        domain_tag = detect_domain_tag(f"{title} {abstract} {venue}")
        meta = make_meta(
            peer_reviewed=True,                 # OpenReview implies review (even if rejected)
            source_type="review" if review_comments else "peer-reviewed",
            venue=venue or "OpenReview",
            publication_date=publication_date,
            domain_tag=domain_tag or "cs",
            review_comments=review_comments,
        )
        return SearchHit(
            url=url,
            title=title,
            snippet=abstract[:500],
            rank=rank,
            backend=self.name,
            meta=meta,
        )

    def _fetch_review_excerpts(self, forum_id: str, *, max_reviews: int = 3) -> list[str]:
        """Fetch up to N review excerpts for a forum. Returns [] on any failure."""
        try:
            resp = httpx.get(
                OPENREVIEW_NOTES,
                params={"forum": forum_id, "limit": 10, "details": "replyCount"},
                timeout=self.timeout,
            )
            resp.raise_for_status()
            data = resp.json()
        except (httpx.HTTPError, ValueError):
            return []
        out: list[str] = []
        for n in data.get("notes", []):
            content = n.get("content", {}) or {}
            inv = n.get("invitation", "").lower()
            # Only keep notes that look like reviews / meta-reviews.
            if not any(k in inv for k in ("review", "meta_review", "decision")):
                continue
            for field in ("summary", "summary_of_strengths", "summary_of_weaknesses",
                          "main_review", "comment", "review"):
                f = content.get(field)
                text = (f.get("value") if isinstance(f, dict) else f) or ""
                if isinstance(text, str) and text.strip():
                    excerpt = text.strip()[:400]
                    out.append(excerpt)
                    break
            if len(out) >= max_reviews:
                break
        return out
