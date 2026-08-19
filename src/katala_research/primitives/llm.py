"""LLM primitives — Claude (Anthropic SDK) + Stub.

`generate_text` for free-form text.
`generate_json` for structured output (with prompt-level schema instruction).

v0 deliberately avoids tool-use / streaming / cache control. Add later only if needed.
"""
from __future__ import annotations

import json
import re
from typing import Any, Optional, Protocol

from ..config import ResearchPrefs, resolve_anthropic_api_key


class LLMBackend(Protocol):
    name: str
    model: str

    def generate_text(self, prompt: str, *, system: str = "", max_tokens: int = 2048) -> str: ...

    def generate_json(
        self, prompt: str, *, system: str = "", max_tokens: int = 2048
    ) -> dict[str, Any]: ...


class ClaudeBackend:
    """Anthropic SDK wrapper. Lazy-imports anthropic to keep stub-only paths dep-free."""

    name = "claude"

    def __init__(self, model: str, api_key: Optional[str] = None):
        self.model = model
        self._api_key = api_key or resolve_anthropic_api_key()
        if not self._api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY not found. Set env var or ~/.anthropic/api_key, "
                "or run with --stub to use StubLLM."
            )
        # Lazy import so --stub doesn't require the SDK installed.
        from anthropic import Anthropic  # type: ignore

        self._client = Anthropic(api_key=self._api_key)

    def generate_text(self, prompt: str, *, system: str = "", max_tokens: int = 2048) -> str:
        msg = self._client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system or "You are a helpful research assistant.",
            messages=[{"role": "user", "content": prompt}],
        )
        parts = [b.text for b in msg.content if getattr(b, "type", "") == "text"]
        return "\n".join(parts).strip()

    def generate_json(
        self, prompt: str, *, system: str = "", max_tokens: int = 2048
    ) -> dict[str, Any]:
        sys = (system or "You are a helpful research assistant.").rstrip()
        sys += " Respond with ONLY valid JSON. No prose. No markdown fences."
        text = self.generate_text(prompt, system=sys, max_tokens=max_tokens)
        # Defensive: strip code fences if the model wrapped output despite the instruction.
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.MULTILINE)
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Claude returned non-JSON: {e}\n---\n{text[:500]}") from e


class StubLLMBackend:
    """Deterministic faux responses keyed by prompt content. Used by --stub smoke."""

    name = "stub"
    model = "stub"

    def generate_text(self, prompt: str, *, system: str = "", max_tokens: int = 2048) -> str:
        # Echo a short canned summary so reports render.
        p = prompt.lower()
        if any(k in p for k in (
            "final report", "write a final", "research report",
            "write a research report", "report in markdown",
        )):
            return _stub_report()
        return "Stub LLM response. The actual run requires ANTHROPIC_API_KEY."

    def generate_json(
        self, prompt: str, *, system: str = "", max_tokens: int = 2048
    ) -> dict[str, Any]:
        p = prompt.lower()
        # NOTE: order matters — earlier branches win on overlapping keywords.
        # "rubric judge" must precede "counter" since rubric prompts mention counter-positions.
        if "rubric judge" in p or '"score"' in p:
            # Deterministic varying score so aggregate isn't all 3.
            score = 3 + (hash(prompt) % 3 - 1)  # 2, 3, or 4
            return {"score": max(0, min(5, score)), "rationale": "stub rubric (deterministic)"}
        if "follow-up question" in p or "clarif" in p or "rephrase the brief" in p:
            return {
                "clarified": "Investigate anti-filter-bubble techniques in deep-research agents.",
                "sub_questions": [
                    "What is the formal definition of a filter bubble?",
                    "How is diversity measured in retrieval?",
                    "What benchmarks exist for deep-research agents?",
                ],
                "questions": [
                    "What specific aspect of the topic matters most to you?",
                    "What sources do you already consider authoritative?",
                    "How will you use the finished report?",
                ],
            }
        if "serp queries" in p or "generate up to" in p and "queries" in p:
            return {"queries": [
                {"query": "anti-bubble information retrieval", "researchGoal": "Survey diversity-aware retrieval."},
                {"query": "filter bubble personalization tradeoff", "researchGoal": "Find empirical evidence on the cost of personalization."},
                {"query": "creativity score formula novelty compatibility", "researchGoal": "Locate formal definitions."},
                {"query": "deep research agent benchmark", "researchGoal": "Compare evaluation suites."},
            ]}
        if "counter_queries" in p or "contradictory" in p or "perspective-shifting" in p:
            return {"counter_queries": [
                "personalization benefits empirical study",
                "filter bubble myth debunked",
            ]}
        if "learnings" in p or "extract" in p:
            return {
                "learnings": [
                    "Diversity-aware selection raises perceived novelty without hurting relevance.",
                    "Filter bubbles arise structurally when scoring is preference-only.",
                    "A 25% creativity floor is a common heuristic in recommender literature.",
                ],
                "followUpQuestions": [
                    "What other floor values have been tested?",
                    "How is creativity measured at eval time?",
                ],
            }
        # Catch-all
        return {"result": "stub", "input_len": len(prompt)}


def build_llm(prefs: ResearchPrefs, *, stub: bool = False) -> LLMBackend:
    if stub:
        return StubLLMBackend()
    try:
        return ClaudeBackend(model=prefs.llm_default)
    except RuntimeError:
        # Fall back to stub if Claude isn't reachable. Caller can detect via .name.
        return StubLLMBackend()


def _stub_report() -> str:
    return (
        "# Stub Research Report\n\n"
        "_This report was generated by StubLLM. Run without --stub for real synthesis._\n\n"
        "## Key learnings\n"
        "- Diversity-aware selection raises perceived novelty without hurting relevance.\n"
        "- Filter bubbles arise structurally when scoring is preference-only.\n"
        "- A 25% creativity floor is a common heuristic in recommender literature.\n\n"
        "## Recommendation\n"
        "Use the anti-bubble selector as a structural floor, not a tuning knob.\n"
    )
