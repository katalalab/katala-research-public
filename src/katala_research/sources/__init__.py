"""Academic Sources — produce Candidates with peer-review-aware metadata.

Each Source implements `AcademicSource` (see base.py). The orchestrator can
plug any combination into the search stage to mix preprint and peer-reviewed
evidence.
"""
from .base import AcademicSource, SourceResult

__all__ = ["AcademicSource", "SourceResult"]
