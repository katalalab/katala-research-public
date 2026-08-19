"""Selector stage — diversity-aware top-K with creativity floor + caps + counter slot.

The selector is the only stage that looks at the whole batch. Per x-algorithm
convention, scoring stays candidate-isolated; diversity logic lives here.

Constraints enforced (in order):
  1. domain_cap_ratio:    ≤ ceil(K · domain_cap_ratio) from any one domain
  2. paradigm_cap_ratio:  ≤ ceil(K · paradigm_cap_ratio) from "preferred set"
  3. discovery_floor:     ≥ ceil(K · discovery_floor_ratio) with Discovery ≥ θ
  4. must_include_counter: ≥ 1 high-semantic_novelty candidate present
"""
from __future__ import annotations

import math
from collections import Counter
from typing import Optional

from ..config import CreativitySelector
from ..types import Candidate


def _is_preferred(c: Candidate, preferred: list[str]) -> bool:
    d = (c.domain or "").lower()
    return any(d.endswith(p.lower()) for p in preferred)


def _peer_review_class(c: Candidate) -> Optional[bool]:
    """True (peer-reviewed) / False (preprint) / None (unknown)."""
    return c.meta.peer_reviewed


def select(
    candidates: list[Candidate],
    *,
    k: int,
    selector_cfg: CreativitySelector,
    preferred_sources: list[str],
) -> list[Candidate]:
    """Apply caps, then floor, then counter — in that order — to produce top-K.

    paradigm_cap is enforced on TWO axes simultaneously (v0.1):
      • preferred-sources vs others
      • peer-reviewed vs preprint (vs unknown, which is uncapped)
    """
    if not candidates or k <= 0:
        return []

    # 1) Sort by total score desc.
    pool = sorted(candidates, key=lambda c: c.score.total, reverse=True)

    domain_cap = max(1, math.ceil(k * selector_cfg.domain_cap_ratio))
    paradigm_cap = max(1, math.ceil(k * selector_cfg.paradigm_cap_ratio))
    floor_n = max(1, math.ceil(k * selector_cfg.discovery_floor_ratio))

    selected: list[Candidate] = []
    domain_counts: Counter[str] = Counter()
    preferred_count = 0
    peer_reviewed_count = 0
    preprint_count = 0

    # 2) Greedy fill respecting caps (both axes).
    for c in pool:
        if len(selected) >= k:
            break
        d = c.domain or "unknown"
        if domain_counts[d] >= domain_cap:
            continue
        if _is_preferred(c, preferred_sources) and preferred_count >= paradigm_cap:
            continue
        pr = _peer_review_class(c)
        if pr is True and peer_reviewed_count >= paradigm_cap:
            continue
        if pr is False and preprint_count >= paradigm_cap:
            continue

        selected.append(c)
        domain_counts[d] += 1
        if _is_preferred(c, preferred_sources):
            preferred_count += 1
        if pr is True:
            peer_reviewed_count += 1
        elif pr is False:
            preprint_count += 1

    # If caps blocked filling K, relax paradigm caps but keep domain cap.
    if len(selected) < k:
        for c in pool:
            if len(selected) >= k:
                break
            if c in selected:
                continue
            d = c.domain or "unknown"
            if domain_counts[d] >= domain_cap:
                continue
            selected.append(c)
            domain_counts[d] += 1
            if _is_preferred(c, preferred_sources):
                preferred_count += 1
            pr = _peer_review_class(c)
            if pr is True:
                peer_reviewed_count += 1
            elif pr is False:
                preprint_count += 1

    # 3) Discovery floor: if too few "discovery" candidates, swap.
    def is_discovery(c: Candidate) -> bool:
        return c.score.discovery >= selector_cfg.discovery_threshold

    selected = _enforce_floor(
        selected=selected,
        pool=pool,
        floor_n=floor_n,
        predicate=is_discovery,
        domain_counts=domain_counts,
        domain_cap=domain_cap,
        preferred_sources=preferred_sources,
        paradigm_cap=paradigm_cap,
    )

    # 4) Counter-evidence: at least one candidate with high semantic novelty.
    if selector_cfg.must_include_counter:
        counter_threshold = 0.55
        has_counter = any(c.score.semantic_novelty >= counter_threshold for c in selected)
        if not has_counter:
            selected = _enforce_floor(
                selected=selected,
                pool=pool,
                floor_n=1,
                predicate=lambda c: c.score.semantic_novelty >= counter_threshold,
                domain_counts=domain_counts,
                domain_cap=domain_cap,
                preferred_sources=preferred_sources,
                paradigm_cap=paradigm_cap,
            )

    # Final sort by total for stable presentation.
    selected.sort(key=lambda c: c.score.total, reverse=True)
    return selected[:k]


def _enforce_floor(
    *,
    selected: list[Candidate],
    pool: list[Candidate],
    floor_n: int,
    predicate,
    domain_counts: Counter,
    domain_cap: int,
    preferred_sources: list[str],
    paradigm_cap: int,
) -> list[Candidate]:
    """Swap-in helper: ensure at least `floor_n` of `selected` satisfy `predicate`.

    Swaps lowest-total non-satisfying selected with highest-total satisfying non-selected,
    while respecting domain and paradigm caps.
    """
    selected_set = {id(c) for c in selected}
    have = sum(1 for c in selected if predicate(c))
    need = floor_n - have
    if need <= 0:
        return selected

    candidates_to_add = [
        c for c in pool
        if predicate(c) and id(c) not in selected_set
    ]
    # Highest-total discovery candidates first.
    candidates_to_add.sort(key=lambda c: c.score.total, reverse=True)

    # Bottom of selected to swap out: lowest-total non-satisfying first.
    swappable = [c for c in selected if not predicate(c)]
    swappable.sort(key=lambda c: c.score.total)  # ascending — drop lowest first

    swapped = 0
    new_selected = list(selected)
    for incoming in candidates_to_add:
        if swapped >= need:
            break
        if not swappable:
            break
        # Find a swap-out that, if removed, allows the incoming to fit caps.
        d_in = incoming.domain or "unknown"
        in_pref = _is_preferred(incoming, preferred_sources)
        for outgoing in list(swappable):
            d_out = outgoing.domain or "unknown"
            out_pref = _is_preferred(outgoing, preferred_sources)
            # Project counts after the swap.
            projected_domain = domain_counts.copy()
            projected_domain[d_out] -= 1
            projected_domain[d_in] += 1
            projected_pref = sum(
                1 for c in new_selected if c is not outgoing and _is_preferred(c, preferred_sources)
            ) + (1 if in_pref else 0)
            if projected_domain[d_in] > domain_cap:
                continue
            if projected_pref > paradigm_cap:
                continue
            # Perform swap.
            idx = new_selected.index(outgoing)
            new_selected[idx] = incoming
            domain_counts.clear()
            domain_counts.update(c.domain or "unknown" for c in new_selected)
            swappable.remove(outgoing)
            selected_set.discard(id(outgoing))
            selected_set.add(id(incoming))
            swapped += 1
            break

    return new_selected
