"""Config / preferences loader.

Reads ~/.agents/research-prefs.yaml (falling back to the bundled example).
Resolves ANTHROPIC_API_KEY from env → ~/.anthropic/api_key → ~/.claude/config.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field


def _load_dotenv(path: Path) -> None:
    """Minimal .env loader — no python-dotenv dependency.

    Only sets variables that aren't already in os.environ (so real env wins).
    Ignores comments, blank lines, and malformed entries.
    """
    if not path.exists():
        return
    try:
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value
    except OSError:
        pass


# Load .env from common locations the moment this module is imported.
# Order: project-local first, then user-global. project-local wins.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
for _p in (
    _PROJECT_ROOT / ".env",
    Path.home() / ".agents" / "katala-research.env",
    Path.home() / ".katala-research" / ".env",
):
    _load_dotenv(_p)


class CreativityWeights(BaseModel):
    relevance: float = 0.50
    discovery: float = 0.35
    risk: float = 0.15


class CreativityGates(BaseModel):
    topical_fit_min: float = 0.30
    content_gap_max: float = 0.50
    source_risk_max: float = 0.60
    reading_cost_max: float = 0.70


class CreativitySelector(BaseModel):
    discovery_floor_ratio: float = 0.25
    discovery_threshold: float = 0.45
    domain_cap_ratio: float = 0.40
    paradigm_cap_ratio: float = 0.50
    must_include_counter: bool = True


class CreativityReflection(BaseModel):
    gap_threshold: float = 0.40


class CreativityComplexity(BaseModel):
    K0_default: float = 0.50
    sigma_default: float = 0.30


class CreativityConfig(BaseModel):
    weights: CreativityWeights = Field(default_factory=CreativityWeights)
    gates: CreativityGates = Field(default_factory=CreativityGates)
    selector: CreativitySelector = Field(default_factory=CreativitySelector)
    reflection: CreativityReflection = Field(default_factory=CreativityReflection)
    complexity: CreativityComplexity = Field(default_factory=CreativityComplexity)


class SearXNGConfig(BaseModel):
    url: str = "http://localhost:8080"
    format: str = "json"


class ResearchPrefs(BaseModel):
    language: str = "ja"
    output_language: str = Field("ja", alias="output-language")
    require_japanese_summary: bool = Field(True, alias="require-japanese-summary")

    default_strategy: str = Field("iterative", alias="default-strategy")
    citation_style: str = Field("inline", alias="citation-style")

    preferred_sources: list[str] = Field(
        default_factory=lambda: ["openalex.org", "arxiv.org", "semanticscholar.org"],
        alias="preferred-sources",
    )
    banned_domains: list[str] = Field(default_factory=list, alias="banned-domains")

    default_breadth: int = Field(4, alias="default-breadth")
    default_depth: int = Field(2, alias="default-depth")

    search_backend_order: list[str] = Field(
        default_factory=lambda: ["searxng", "stub"], alias="search-backend-order"
    )
    academic_sources: list[str] = Field(
        default_factory=lambda: ["arxiv", "openalex"], alias="academic-sources"
    )
    read_backend_order: list[str] = Field(
        default_factory=lambda: ["jina", "defuddle", "stub"], alias="read-backend-order"
    )
    # Update this to the latest stable Anthropic model as models evolve.
    llm_default: str = Field("claude-opus-4-5", alias="llm-default")
    llm_budget_cap_usd: float = Field(5.00, alias="llm-budget-cap-usd")

    searxng: SearXNGConfig = Field(default_factory=SearXNGConfig)
    creativity: CreativityConfig = Field(default_factory=CreativityConfig)

    model_config = {"populate_by_name": True, "extra": "ignore"}


DEFAULT_PREFS_PATH = Path.home() / ".agents" / "research-prefs.yaml"
EXAMPLE_PREFS_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "examples"
    / "research-prefs.example.yaml"
)


def load_prefs(path: Optional[Path] = None) -> ResearchPrefs:
    """Load prefs from YAML; fall back to the bundled example, then to in-code defaults."""
    candidates = []
    if path is not None:
        candidates.append(Path(path))
    candidates.extend([DEFAULT_PREFS_PATH, EXAMPLE_PREFS_PATH])

    for p in candidates:
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                raw = yaml.safe_load(f) or {}
            return ResearchPrefs.model_validate(raw)

    # No file anywhere — return defaults.
    return ResearchPrefs()


def resolve_anthropic_api_key() -> Optional[str]:
    """Resolve Claude API key from env → ~/.anthropic/api_key → ~/.claude/config.

    Returns None if nothing is found. Callers using stub backends can ignore None.
    """
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return key.strip()

    api_key_file = Path.home() / ".anthropic" / "api_key"
    if api_key_file.exists():
        try:
            return api_key_file.read_text().strip()
        except OSError:
            pass

    # ~/.claude/config or similar — best-effort, no guarantee on format.
    claude_config = Path.home() / ".claude" / "config.json"
    if claude_config.exists():
        try:
            import json

            data = json.loads(claude_config.read_text())
            return data.get("anthropic_api_key") or data.get("api_key")
        except (OSError, ValueError):
            pass

    return None


def resolve_env(name: str, *, strip: bool = True) -> Optional[str]:
    """Return an env var, treating empty string as None (post-.env-load)."""
    v = os.environ.get(name)
    if v is None:
        return None
    v = v.strip() if strip else v
    return v or None


def env_status() -> dict[str, Optional[str]]:
    """Summarize which optional API keys are set. Used by `kr config`.

    Returns redacted values — for keys we just say "set"/"not set"; for mailto
    we return the actual address (it's not a secret).
    """
    def redact(value: Optional[str]) -> Optional[str]:
        if not value:
            return None
        return f"set ({len(value)} chars)"

    return {
        "OPENALEX_MAILTO": resolve_env("OPENALEX_MAILTO"),  # not a secret
        "ANTHROPIC_API_KEY": redact(resolve_anthropic_api_key()),
        "SEMANTIC_SCHOLAR_API_KEY": redact(resolve_env("SEMANTIC_SCHOLAR_API_KEY")),
        "ASTA_API_KEY": redact(resolve_env("ASTA_API_KEY")),
        "CROSSREF_MAILTO": resolve_env("CROSSREF_MAILTO"),
        "OPENREVIEW_USERNAME": resolve_env("OPENREVIEW_USERNAME"),  # not a secret
        "OPENREVIEW_PASSWORD": redact(resolve_env("OPENREVIEW_PASSWORD")),
        "SEARXNG_URL": resolve_env("SEARXNG_URL"),
        "EXA_API_KEY": redact(resolve_env("EXA_API_KEY")),
        "TAVILY_API_KEY": redact(resolve_env("TAVILY_API_KEY")),
        "LINKUP_API_KEY": redact(resolve_env("LINKUP_API_KEY")),
        "FIRECRAWL_API_KEY": redact(resolve_env("FIRECRAWL_API_KEY")),
        "JINA_API_KEY": redact(resolve_env("JINA_API_KEY")),
    }


def resolve_prefs_path() -> Path:
    """Where the user's prefs file should live."""
    return DEFAULT_PREFS_PATH
