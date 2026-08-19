"""Local God-proof research kernel.

This module does not claim to prove God. It converts major argument families
into auditable proof obligations so the next research step is explicit,
machine-readable, and logged.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from .session.ledger import new_session_dir


DEFAULT_GODPROOF_ROOT = Path.home() / "work" / "research" / "sessions"
RETRIEVED_AT = "2026-05-24"


@dataclass(frozen=True)
class Source:
    id: str
    title: str
    url: str
    source_type: str
    retrieved_at: str = RETRIEVED_AT

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "source_type": self.source_type,
            "retrieved_at": self.retrieved_at,
        }


@dataclass(frozen=True)
class Premise:
    id: str
    text: str
    status: str
    confidence: float
    source_ids: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "text": self.text,
            "status": self.status,
            "confidence": self.confidence,
            "source_ids": self.source_ids,
        }


@dataclass(frozen=True)
class ArgumentFamily:
    id: str
    name: str
    thesis: str
    formal_shape: str
    premise_ids: list[str]
    source_ids: list[str]
    machine_status: str
    blockers: list[str]

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "thesis": self.thesis,
            "formal_shape": self.formal_shape,
            "premise_ids": self.premise_ids,
            "source_ids": self.source_ids,
            "machine_status": self.machine_status,
            "blockers": self.blockers,
        }


@dataclass(frozen=True)
class CounterArgument:
    id: str
    name: str
    pressure: str
    target_argument_ids: list[str]
    source_ids: list[str]
    severity: float

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "pressure": self.pressure,
            "target_argument_ids": self.target_argument_ids,
            "source_ids": self.source_ids,
            "severity": self.severity,
        }


@dataclass(frozen=True)
class ProofObligation:
    id: str
    argument_id: str
    kind: str
    statement: str
    status: str
    machine_check: str
    required_inputs: list[str]
    source_ids: list[str] = field(default_factory=list)
    blocks_proof_claim: bool = True

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "argument_id": self.argument_id,
            "kind": self.kind,
            "statement": self.statement,
            "status": self.status,
            "machine_check": self.machine_check,
            "required_inputs": self.required_inputs,
            "source_ids": self.source_ids,
            "blocks_proof_claim": self.blocks_proof_claim,
        }


@dataclass(frozen=True)
class WisdomEntry:
    id: str
    domain: str
    stance: str
    summary: str
    source_ids: list[str]
    argument_ids: list[str] = field(default_factory=list)
    proof_role: str = "context"

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "domain": self.domain,
            "stance": self.stance,
            "summary": self.summary,
            "source_ids": self.source_ids,
            "argument_ids": self.argument_ids,
            "proof_role": self.proof_role,
        }


@dataclass(frozen=True)
class TargetConcept:
    id: str
    label: str
    category: str
    description: str
    attributes: dict[str, Any]
    source_ids: list[str]

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "category": self.category,
            "description": self.description,
            "attributes": self.attributes,
            "source_ids": self.source_ids,
        }



import importlib.resources as _ilr

def _load_frontier() -> dict:
    """Load the static research-artifact data from the bundled JSON file.

    The data previously lived as inline Python literals in this module (~5 k lines).
    Keeping it in JSON lets the file stay under 20 k lines of logic while remaining
    importable at runtime with zero filesystem assumptions.
    """
    data_pkg = _ilr.files("katala_research.data")
    return _json_load_text((data_pkg / "godproof_frontier.json").read_text(encoding="utf-8"))


def _json_load_text(text: str) -> dict:
    return json.loads(text)


_FRONTIER = _load_frontier()

# --- scalar / list constants from data bundle ---
RETRIEVED_AT: str = _FRONTIER["RETRIEVED_AT"]
TARGET_PROOF_CONCEPT_ID: str = _FRONTIER["TARGET_PROOF_CONCEPT_ID"]
REQUIRED_TARGET_CONCEPT_FIELDS: list[str] = _FRONTIER["REQUIRED_TARGET_CONCEPT_FIELDS"]
REQUIRED_WISDOM_DOMAINS: list[str] = _FRONTIER["REQUIRED_WISDOM_DOMAINS"]

# --- dataclass-backed lists reconstructed from JSON records ---
SOURCES: list[Source] = [Source(**r) for r in _FRONTIER["SOURCES"]]
TARGET_CONCEPTS: list[TargetConcept] = [TargetConcept(**r) for r in _FRONTIER["TARGET_CONCEPTS"]]
PREMISES: list[Premise] = [Premise(**r) for r in _FRONTIER["PREMISES"]]
ARGUMENTS: list[ArgumentFamily] = [ArgumentFamily(**r) for r in _FRONTIER["ARGUMENTS"]]
COUNTERARGUMENTS: list[CounterArgument] = [CounterArgument(**r) for r in _FRONTIER["COUNTERARGUMENTS"]]
PROOF_OBLIGATIONS: list[ProofObligation] = [ProofObligation(**r) for r in _FRONTIER["PROOF_OBLIGATIONS"]]
WISDOM_CORPUS: list[WisdomEntry] = [WisdomEntry(**r) for r in _FRONTIER["WISDOM_CORPUS"]]

# --- pure-dict / pure-list constants from data bundle ---
MODAL_DERIVATION: dict = _FRONTIER["MODAL_DERIVATION"]
MODAL_MODEL: dict = _FRONTIER["MODAL_MODEL"]
TELEOLOGICAL_BAYES_MODEL: dict = _FRONTIER["TELEOLOGICAL_BAYES_MODEL"]
COSMOLOGICAL_PSR_MODEL: dict = _FRONTIER["COSMOLOGICAL_PSR_MODEL"]
EVIL_HIDDENNESS_CONSTRAINT_MODEL: dict = _FRONTIER["EVIL_HIDDENNESS_CONSTRAINT_MODEL"]
ONTOLOGICAL_SOUNDNESS_DOSSIER: dict = _FRONTIER["ONTOLOGICAL_SOUNDNESS_DOSSIER"]
ATTRIBUTE_COHERENCE_LEDGER: dict = _FRONTIER["ATTRIBUTE_COHERENCE_LEDGER"]
COHERENT_CONCEIVABILITY_MODEL: dict = _FRONTIER["COHERENT_CONCEIVABILITY_MODEL"]
METAPHYSICAL_POSSIBILITY_BRIDGE: dict = _FRONTIER["METAPHYSICAL_POSSIBILITY_BRIDGE"]
POSSIBLE_NECESSARY_EXISTENCE_BRIDGE: dict = _FRONTIER["POSSIBLE_NECESSARY_EXISTENCE_BRIDGE"]
DEFINITION_SMUGGLING_AUDIT: dict = _FRONTIER["DEFINITION_SMUGGLING_AUDIT"]
RIVAL_NECESSARY_PARITY_AUDIT: dict = _FRONTIER["RIVAL_NECESSARY_PARITY_AUDIT"]
POSITIVE_PROPERTY_FILTER_AUDIT: dict = _FRONTIER["POSITIVE_PROPERTY_FILTER_AUDIT"]
POSITIVE_GROUNDING_AUDIT: dict = _FRONTIER["POSITIVE_GROUNDING_AUDIT"]
MORAL_PERFECTION_GROUNDING_AUDIT: dict = _FRONTIER["MORAL_PERFECTION_GROUNDING_AUDIT"]
EVIL_HIDDENNESS_MORAL_PRESSURE_AUDIT: dict = _FRONTIER["EVIL_HIDDENNESS_MORAL_PRESSURE_AUDIT"]
EVIDENTIAL_EVIL_PROBABILITY_AUDIT: dict = _FRONTIER["EVIDENTIAL_EVIL_PROBABILITY_AUDIT"]
EVIDENTIAL_EVIL_LIKELIHOOD_LEDGER: dict = _FRONTIER["EVIDENTIAL_EVIL_LIKELIHOOD_LEDGER"]
EVIDENTIAL_EVIL_DEPENDENCE_MODEL: dict = _FRONTIER["EVIDENTIAL_EVIL_DEPENDENCE_MODEL"]
EVIDENTIAL_EVIL_CALIBRATION_LEDGER: dict = _FRONTIER["EVIDENTIAL_EVIL_CALIBRATION_LEDGER"]
EVIDENTIAL_EVIL_CASE_CORPUS: dict = _FRONTIER["EVIDENTIAL_EVIL_CASE_CORPUS"]
EVIDENTIAL_EVIL_REVIEWED_CASE_RECORDS: dict = _FRONTIER["EVIDENTIAL_EVIL_REVIEWED_CASE_RECORDS"]
EVIDENTIAL_EVIL_EMPIRICAL_EXPANSION_LEDGER: dict = _FRONTIER["EVIDENTIAL_EVIL_EMPIRICAL_EXPANSION_LEDGER"]
EVIDENTIAL_EVIL_PRIMARY_DATASET_SELECTION: dict = _FRONTIER["EVIDENTIAL_EVIL_PRIMARY_DATASET_SELECTION"]
EVIDENTIAL_EVIL_DATASET_INGESTION_MANIFEST: dict = _FRONTIER["EVIDENTIAL_EVIL_DATASET_INGESTION_MANIFEST"]
EVIDENTIAL_EVIL_LICENSE_PRIVACY_REVIEW: dict = _FRONTIER["EVIDENTIAL_EVIL_LICENSE_PRIVACY_REVIEW"]
EVIDENTIAL_EVIL_MICRODATA_MINIMIZATION_POLICY: dict = _FRONTIER["EVIDENTIAL_EVIL_MICRODATA_MINIMIZATION_POLICY"]
EVIDENTIAL_EVIL_DERIVED_AGGREGATE_SCHEMA: dict = _FRONTIER["EVIDENTIAL_EVIL_DERIVED_AGGREGATE_SCHEMA"]
EVIDENTIAL_EVIL_SOURCE_VERSION_HASH_PREFLIGHT: dict = _FRONTIER["EVIDENTIAL_EVIL_SOURCE_VERSION_HASH_PREFLIGHT"]
EVIDENTIAL_EVIL_SOURCE_ACQUISITION_HASH_RUNBOOK: dict = _FRONTIER["EVIDENTIAL_EVIL_SOURCE_ACQUISITION_HASH_RUNBOOK"]
EVIDENTIAL_EVIL_SUPPRESSION_REPORT_TEMPLATE: dict = _FRONTIER["EVIDENTIAL_EVIL_SUPPRESSION_REPORT_TEMPLATE"]
EVIDENTIAL_EVIL_LICENSE_DECISION_PACKET: dict = _FRONTIER["EVIDENTIAL_EVIL_LICENSE_DECISION_PACKET"]
EVIDENTIAL_EVIL_ATTRIBUTION_SOURCE_TITLES: dict = _FRONTIER["EVIDENTIAL_EVIL_ATTRIBUTION_SOURCE_TITLES"]
EVIDENTIAL_EVIL_ATTRIBUTION_TEMPLATE_LEDGER: dict = _FRONTIER["EVIDENTIAL_EVIL_ATTRIBUTION_TEMPLATE_LEDGER"]
POSSIBILITY_PREMISE_LADDER: dict = _FRONTIER["POSSIBILITY_PREMISE_LADDER"]
HUMAN_WISDOM_PRIMARY_SOURCE_SEED_LEDGER: dict = _FRONTIER["HUMAN_WISDOM_PRIMARY_SOURCE_SEED_LEDGER"]
HUMAN_WISDOM_PRIMARY_SOURCE_EXTRACTION_QUEUE: dict = _FRONTIER["HUMAN_WISDOM_PRIMARY_SOURCE_EXTRACTION_QUEUE"]
HUMAN_WISDOM_PRIMARY_SOURCE_SUMMARY_CANDIDATES: dict = _FRONTIER["HUMAN_WISDOM_PRIMARY_SOURCE_SUMMARY_CANDIDATES"]
HUMAN_WISDOM_DOMAIN_ARGUMENT_TARGETS: dict = _FRONTIER["HUMAN_WISDOM_DOMAIN_ARGUMENT_TARGETS"]
HUMAN_WISDOM_COUNTERPRESSURE_EDGE_PROPOSALS: dict = _FRONTIER["HUMAN_WISDOM_COUNTERPRESSURE_EDGE_PROPOSALS"]
HUMAN_WISDOM_COUNTERPRESSURE_EDGE_REVIEW_QUEUE: dict = _FRONTIER["HUMAN_WISDOM_COUNTERPRESSURE_EDGE_REVIEW_QUEUE"]
HUMAN_WISDOM_COUNTERPRESSURE_EDGE_REVIEW_RUBRIC: dict = _FRONTIER["HUMAN_WISDOM_COUNTERPRESSURE_EDGE_REVIEW_RUBRIC"]
HUMAN_WISDOM_COUNTERPRESSURE_EDGE_REVIEW_DECISIONS: dict = _FRONTIER["HUMAN_WISDOM_COUNTERPRESSURE_EDGE_REVIEW_DECISIONS"]
HUMAN_WISDOM_COUNTERPRESSURE_EDGE_RESOLUTION_PACKET: dict = _FRONTIER["HUMAN_WISDOM_COUNTERPRESSURE_EDGE_RESOLUTION_PACKET"]
HUMAN_WISDOM_COUNTERPRESSURE_EDGE_EVIDENCE_REQUEST_QUEUE: dict = _FRONTIER["HUMAN_WISDOM_COUNTERPRESSURE_EDGE_EVIDENCE_REQUEST_QUEUE"]
HUMAN_WISDOM_COUNTERPRESSURE_EDGE_EVIDENCE_ACQUISITION_MANIFEST: dict = _FRONTIER["HUMAN_WISDOM_COUNTERPRESSURE_EDGE_EVIDENCE_ACQUISITION_MANIFEST"]
HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_SCHEMA: dict = _FRONTIER["HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_SCHEMA"]
HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_REVIEW_QUEUE: dict = _FRONTIER["HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_REVIEW_QUEUE"]
HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_REVIEW_RUBRIC: dict = _FRONTIER["HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_REVIEW_RUBRIC"]
HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_REVIEW_DECISIONS: dict = _FRONTIER["HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_REVIEW_DECISIONS"]
HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_RESOLUTION_PACKET: dict = _FRONTIER["HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_RESOLUTION_PACKET"]
HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_EVIDENCE_REQUEST_QUEUE: dict = _FRONTIER["HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_EVIDENCE_REQUEST_QUEUE"]
HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_ACQUISITION_MANIFEST: dict = _FRONTIER["HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_ACQUISITION_MANIFEST"]
HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_ACQUISITION_HASH_RUNBOOK: dict = _FRONTIER["HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_ACQUISITION_HASH_RUNBOOK"]
HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_AUTHORIZATION_PACKET: dict = _FRONTIER["HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_AUTHORIZATION_PACKET"]
HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_AUTHORIZATION_REVIEW_QUEUE: dict = _FRONTIER["HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_AUTHORIZATION_REVIEW_QUEUE"]
HUMAN_WISDOM_INTAKE_ROADMAP: dict = _FRONTIER["HUMAN_WISDOM_INTAKE_ROADMAP"]


def _append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _premise_index() -> dict[str, Premise]:
    return {p.id: p for p in PREMISES}


def _argument_score(argument: ArgumentFamily, counter_index: dict[str, list[CounterArgument]]) -> dict[str, Any]:
    premise_by_id = _premise_index()
    premises = [premise_by_id[p] for p in argument.premise_ids]
    premise_confidence = sum(p.confidence for p in premises) / max(1, len(premises))
    contested = [p.id for p in premises if p.status in {"contested", "missing"}]
    counters = counter_index.get(argument.id, [])
    counter_pressure = sum(c.severity for c in counters) / max(1, len(counters)) if counters else 0.0
    blocker_pressure = min(1.0, 0.11 * len(argument.blockers) + 0.18 * len(contested))
    proof_proximity = max(0.0, premise_confidence - 0.35 * counter_pressure - 0.25 * blocker_pressure)
    return {
        "argument_id": argument.id,
        "name": argument.name,
        "proof_proximity": round(proof_proximity, 3),
        "premise_confidence": round(premise_confidence, 3),
        "counter_pressure": round(counter_pressure, 3),
        "blocker_pressure": round(blocker_pressure, 3),
        "contested_premise_ids": contested,
        "blocking_questions": argument.blockers,
        "machine_next_step": _machine_next_step(argument),
    }


def _machine_next_step(argument: ArgumentFamily) -> str:
    if argument.id == "arg-ontological-modal":
        return "Encode the exact modal axioms and test validity, consistency, and modal-collapse risk in Isabelle/HOL or Coq."
    if argument.id == "arg-teleological-fine-tuning":
        return "Build an explicit Bayesian model with priors, likelihoods, anthropic conditioning, and multiverse alternatives."
    if argument.id == "arg-pragmatic":
        return "Enumerate competing deity hypotheses and compute sensitivity of expected utility to payoff assumptions."
    return "Turn each contested premise into an independent source-backed sub-proof or counter-model search."


def _counter_index() -> dict[str, list[CounterArgument]]:
    by_arg: dict[str, list[CounterArgument]] = {}
    for counter in COUNTERARGUMENTS:
        for argument_id in counter.target_argument_ids:
            by_arg.setdefault(argument_id, []).append(counter)
    return by_arg


def _build_wisdom_map() -> dict[str, Any]:
    return {
        "status": "research_map_not_proof",
        "retrieved_at": RETRIEVED_AT,
        "sources": [s.as_dict() for s in SOURCES],
        "target_concepts": [concept.as_dict() for concept in TARGET_CONCEPTS],
        "wisdom_corpus": [entry.as_dict() for entry in WISDOM_CORPUS],
        "premises": [p.as_dict() for p in PREMISES],
        "arguments": [a.as_dict() for a in ARGUMENTS],
        "counterarguments": [c.as_dict() for c in COUNTERARGUMENTS],
        "proof_obligations": [o.as_dict() for o in PROOF_OBLIGATIONS],
    }


def _build_proof_graph() -> dict[str, Any]:
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, str]] = []
    for premise in PREMISES:
        nodes.append({"id": premise.id, "kind": "premise", "label": premise.text, "status": premise.status})
        for source_id in premise.source_ids:
            edges.append({"from": source_id, "to": premise.id, "kind": "supports-premise"})
    for source in SOURCES:
        nodes.append({"id": source.id, "kind": "source", "label": source.title, "url": source.url})
    for argument in ARGUMENTS:
        nodes.append({"id": argument.id, "kind": "argument", "label": argument.name})
        for premise_id in argument.premise_ids:
            edges.append({"from": premise_id, "to": argument.id, "kind": "required-by"})
        for source_id in argument.source_ids:
            edges.append({"from": source_id, "to": argument.id, "kind": "documents"})
    for counter in COUNTERARGUMENTS:
        nodes.append({"id": counter.id, "kind": "counterargument", "label": counter.name})
        for argument_id in counter.target_argument_ids:
            edges.append({"from": counter.id, "to": argument_id, "kind": "pressures"})
    for obligation in PROOF_OBLIGATIONS:
        nodes.append({
            "id": obligation.id,
            "kind": "proof_obligation",
            "label": obligation.statement,
            "status": obligation.status,
        })
        edges.append({"from": obligation.argument_id, "to": obligation.id, "kind": "blocked-by"})
        for source_id in obligation.source_ids:
            edges.append({"from": source_id, "to": obligation.id, "kind": "informs-obligation"})
    nodes.append({"id": "claim-god-exists", "kind": "target", "label": "God exists"})
    for argument in ARGUMENTS:
        edges.append({"from": argument.id, "to": "claim-god-exists", "kind": "would-support"})
    return {
        "status": "graph_of_candidate_support_not_final_proof",
        "nodes": nodes,
        "edges": edges,
    }


def _build_target_concept_registry() -> dict[str, Any]:
    return {
        "status": "target_concepts_defined",
        "proof_target_id": TARGET_PROOF_CONCEPT_ID,
        "required_target_concept_fields": REQUIRED_TARGET_CONCEPT_FIELDS,
        "concepts": [concept.as_dict() for concept in TARGET_CONCEPTS],
    }


def _target_concept_index() -> dict[str, TargetConcept]:
    return {concept.id: concept for concept in TARGET_CONCEPTS}


def _build_definition_checks() -> dict[str, Any]:
    concepts = _target_concept_index()
    target = concepts[TARGET_PROOF_CONCEPT_ID]
    present_fields = sorted(target.attributes)
    missing_fields = [
        field for field in REQUIRED_TARGET_CONCEPT_FIELDS
        if field not in target.attributes or target.attributes[field] in {"", None}
    ]
    checks = [
        {
            "id": "check-target-field-completeness",
            "status": "complete" if not missing_fields else "open",
            "target_concept_id": target.id,
            "required_fields": REQUIRED_TARGET_CONCEPT_FIELDS,
            "present_fields": present_fields,
            "missing_fields": missing_fields,
        },
        {
            "id": "check-target-distinguishes-comparators",
            "status": "complete",
            "target_concept_id": target.id,
            "comparator_concept_ids": [
                concept.id for concept in TARGET_CONCEPTS
                if concept.id != target.id
            ],
            "result": "classical theism is separated from deism and impersonal ultimacy comparators",
        },
        {
            "id": "check-target-counterargument-exposure",
            "status": "complete",
            "target_concept_id": target.id,
            "exposed_counterargument_ids": ["counter-evil", "counter-hiddenness", "counter-diversity"],
            "result": "target attributes are explicitly exposed to evil, hiddenness, and diversity constraints",
        },
    ]
    status = "complete" if all(check["status"] == "complete" for check in checks) else "open"
    return {
        "status": status,
        "target_concept_id": target.id,
        "checks": checks,
        "rule": "The target God concept gate is complete only when the proof target is field-complete, distinguished from comparators, and linked to counterargument exposure.",
    }


def _build_modal_derivation() -> dict[str, Any]:
    return {
        "status": "encoded",
        "derivation": MODAL_DERIVATION,
        "warning": (
            "This encodes the conditional S5 bridge from possible necessary "
            "existence to actuality. It does not settle the possibility premise, "
            "axiom consistency, or modal-collapse concerns."
        ),
    }


def _build_modal_validity_checks() -> dict[str, Any]:
    derivation = MODAL_DERIVATION
    formulas_by_step = {step["id"]: step["formula"] for step in derivation["steps"]}
    rules_by_id = {rule["id"]: rule for rule in derivation["rules"]}
    assumption_ids = {assumption["id"] for assumption in derivation["assumptions"]}
    checks: list[dict[str, Any]] = []

    for step in derivation["steps"]:
        justification = step["justification"]
        if justification in assumption_ids:
            checks.append({
                "id": f"check-{step['id']}",
                "status": "complete",
                "step_id": step["id"],
                "result": "assumption accepted for conditional validity check",
            })
            continue

        rule = rules_by_id.get(justification)
        dependency_ids = step.get("depends_on", [])
        dependency_formulas = [formulas_by_step.get(dep_id) for dep_id in dependency_ids]
        valid = (
            rule is not None
            and dependency_formulas == [rule["input"]]
            and step["formula"] == rule["output"]
        )
        checks.append({
            "id": f"check-{step['id']}",
            "status": "complete" if valid else "open",
            "step_id": step["id"],
            "rule_id": justification,
            "dependency_formulas": dependency_formulas,
            "expected_input": rule["input"] if rule else None,
            "expected_output": rule["output"] if rule else None,
            "actual_output": step["formula"],
        })

    conclusion_step = derivation["steps"][-1]
    checks.append({
        "id": "check-conclusion",
        "status": "complete" if conclusion_step["formula"] == derivation["conclusion"] else "open",
        "expected_conclusion": derivation["conclusion"],
        "actual_conclusion": conclusion_step["formula"],
    })
    status = "complete" if all(check["status"] == "complete" for check in checks) else "open"
    return {
        "status": status,
        "argument_id": derivation["argument_id"],
        "scope": derivation["scope"],
        "checks": checks,
        "remaining_risks": [
            "the possibility premise remains a soundness obligation",
            "the selected modal axioms still require consistency and modal-collapse checks",
            "this is a minimal bridge, not the full Godel/Scott positive-property derivation",
        ],
    }


def _is_s5_accessibility(model: dict[str, Any]) -> bool:
    worlds = set(model["worlds"])
    access = {world: set(targets) for world, targets in model["accessibility"].items()}
    if set(access) != worlds or any(not targets <= worlds for targets in access.values()):
        return False
    reflexive = all(world in access[world] for world in worlds)
    symmetric = all(
        world in access[target]
        for world in worlds
        for target in access[world]
    )
    transitive = all(
        third in access[world]
        for world in worlds
        for target in access[world]
        for third in access[target]
    )
    return reflexive and symmetric and transitive


def _modal_box(model: dict[str, Any], proposition: str, world: str) -> bool:
    valuation = model["valuation"][proposition]
    return all(valuation[target] for target in model["accessibility"][world])


def _modal_diamond_box(model: dict[str, Any], proposition: str, world: str) -> bool:
    return any(
        _modal_box(model, proposition, target)
        for target in model["accessibility"][world]
    )


def _build_modal_consistency_checks() -> dict[str, Any]:
    model = MODAL_MODEL
    actual = model["actual_world"]
    s5_ok = _is_s5_accessibility(model)
    possible_necessary_g = _modal_diamond_box(model, "G", actual)
    necessary_g = _modal_box(model, "G", actual)
    actual_g = model["valuation"]["G"][actual]
    p_true_not_necessary = (
        model["valuation"]["P"][actual]
        and not _modal_box(model, "P", actual)
    )
    checks = [
        {
            "id": "check-s5-frame",
            "status": "complete" if s5_ok else "open",
            "result": "accessibility is reflexive, symmetric, and transitive" if s5_ok else "accessibility is not S5",
        },
        {
            "id": "check-assumption-satisfiable",
            "status": "complete" if possible_necessary_g else "open",
            "formula": "◇□G",
            "actual_world": actual,
            "result": possible_necessary_g,
        },
        {
            "id": "check-conclusion-satisfied",
            "status": "complete" if necessary_g and actual_g else "open",
            "formulas": ["□G", "G"],
            "actual_world": actual,
            "result": {"□G": necessary_g, "G": actual_g},
        },
        {
            "id": "check-minimal-modal-collapse-not-introduced",
            "status": "complete" if p_true_not_necessary else "open",
            "counterexample": {"formula": "P -> □P", "world": actual, "P": True, "□P": False},
            "result": "P is true at the actual world but not necessary",
        },
    ]
    status = "complete" if all(check["status"] == "complete" for check in checks) else "open"
    return {
        "status": status,
        "argument_id": MODAL_DERIVATION["argument_id"],
        "scope": model["scope"],
        "model": model,
        "checks": checks,
        "remaining_risks": [
            "this checks the selected minimal modal bridge, not every Godel/Scott axiom variant",
            "the contested possibility premise remains a soundness question",
            "full proof-assistant replay and broader model search remain useful next steps",
        ],
    }


def _normalize_distribution(values: dict[str, float]) -> dict[str, float]:
    total = sum(values.values())
    if total <= 0:
        return {key: 0.0 for key in values}
    return {key: round(value / total, 6) for key, value in values.items()}


def _posterior(priors: dict[str, float], likelihoods: dict[str, float]) -> dict[str, float]:
    weighted = {
        hypothesis: priors[hypothesis] * likelihoods[hypothesis]
        for hypothesis in priors
    }
    return _normalize_distribution(weighted)


def _build_teleological_bayes_model() -> dict[str, Any]:
    hypotheses = TELEOLOGICAL_BAYES_MODEL["hypotheses"]
    priors = {hypothesis["id"]: hypothesis["prior"] for hypothesis in hypotheses}
    likelihoods = {hypothesis["id"]: hypothesis["likelihood"] for hypothesis in hypotheses}
    posterior = _posterior(priors, likelihoods)
    return {
        "status": "encoded",
        "model": TELEOLOGICAL_BAYES_MODEL,
        "base_case": {
            "priors": priors,
            "likelihoods": likelihoods,
            "posterior": posterior,
            "top_hypothesis": max(posterior, key=posterior.get),
        },
        "warning": (
            "Numerical values are explicit sensitivity-test parameters. They are "
            "not measurements and do not by themselves prove the target concept."
        ),
    }


def _build_teleological_bayes_checks() -> dict[str, Any]:
    model = TELEOLOGICAL_BAYES_MODEL
    hypotheses = model["hypotheses"]
    hypothesis_ids = [hypothesis["id"] for hypothesis in hypotheses]
    priors = {hypothesis["id"]: hypothesis["prior"] for hypothesis in hypotheses}
    likelihoods = {hypothesis["id"]: hypothesis["likelihood"] for hypothesis in hypotheses}
    base_posterior = _posterior(priors, likelihoods)
    scenario_results = []
    for scenario in model["sensitivity_scenarios"]:
        posterior = _posterior(scenario["priors"], scenario["likelihoods"])
        scenario_results.append({
            "id": scenario["id"],
            "posterior": posterior,
            "top_hypothesis": max(posterior, key=posterior.get),
        })

    top_hypotheses = sorted({scenario["top_hypothesis"] for scenario in scenario_results})
    checks = [
        {
            "id": "check-hypothesis-set",
            "status": "complete" if len(hypothesis_ids) >= 3 else "open",
            "hypothesis_ids": hypothesis_ids,
        },
        {
            "id": "check-priors-normalized",
            "status": "complete" if abs(sum(priors.values()) - 1.0) < 1e-9 else "open",
            "prior_sum": round(sum(priors.values()), 6),
        },
        {
            "id": "check-likelihoods-bounded",
            "status": "complete" if all(0.0 <= value <= 1.0 for value in likelihoods.values()) else "open",
            "likelihoods": likelihoods,
        },
        {
            "id": "check-anthropic-conditioning-declared",
            "status": "complete" if model["anthropic_conditioning"]["observer_selection"] else "open",
            "anthropic_conditioning": model["anthropic_conditioning"],
        },
        {
            "id": "check-multiverse-alternative-present",
            "status": "complete" if "multiverse_selection" in hypothesis_ids else "open",
            "hypothesis_ids": hypothesis_ids,
        },
        {
            "id": "check-sensitivity-varies",
            "status": "complete" if len(top_hypotheses) >= 2 else "open",
            "top_hypotheses": top_hypotheses,
            "result": "posterior winner changes under declared sensitivity scenarios",
        },
    ]
    status = "complete" if all(check["status"] == "complete" for check in checks) else "open"
    return {
        "status": status,
        "argument_id": model["argument_id"],
        "scope": "explicit_bayesian_evidence_bookkeeping_not_proof",
        "base_posterior": base_posterior,
        "scenario_results": scenario_results,
        "checks": checks,
        "remaining_risks": [
            "priors and likelihoods remain philosophically and scientifically contestable",
            "the hypothesis set is coarse-grained and not exhaustive",
            "fine-tuning evidence remains insufficient for proof without independent premise support",
        ],
    }


def _build_cosmological_psr_model() -> dict[str, Any]:
    return {
        "status": "encoded",
        "model": COSMOLOGICAL_PSR_MODEL,
        "warning": (
            "This records PSR variants and bridge requirements. It does not prove "
            "that strong PSR is true or that a necessary ground has every target "
            "God attribute."
        ),
    }


def _build_cosmological_psr_checks() -> dict[str, Any]:
    model = COSMOLOGICAL_PSR_MODEL
    variants = {variant["id"]: variant for variant in model["psr_variants"]}
    candidates = {candidate["id"]: candidate for candidate in model["explanation_candidates"]}
    necessary_ground = candidates["necessary_ground"]
    bridge_requirements = set(model["bridge_requirements"])
    bridged = set(necessary_ground["target_bridge_attributes"])
    countermodel_ids = [
        candidate_id for candidate_id in candidates
        if candidate_id != "necessary_ground"
    ]
    checks = [
        {
            "id": "check-psr-variant-taxonomy",
            "status": "complete" if {"strong_psr", "contingent_psr", "weak_explanatory_principle"} <= set(variants) else "open",
            "variant_ids": sorted(variants),
        },
        {
            "id": "check-strong-psr-not-smuggled",
            "status": "complete" if variants["strong_psr"]["status"] == "too_strong_for_current_proof" else "open",
            "result": "strong PSR is recorded as contested, not silently assumed",
        },
        {
            "id": "check-countermodels-present",
            "status": "complete" if {"brute_fact", "infinite_regress", "closed_contingent_totality"} <= set(countermodel_ids) else "open",
            "countermodel_ids": sorted(countermodel_ids),
        },
        {
            "id": "check-necessary-ground-bridge-partial",
            "status": "complete" if bridged < bridge_requirements else "open",
            "bridged_attributes": sorted(bridged),
            "missing_attributes": sorted(bridge_requirements - bridged),
            "result": "necessary ground reaches only part of the target God concept",
        },
        {
            "id": "check-replacement-principle-available",
            "status": "complete" if variants["contingent_psr"]["status"] == "candidate" else "open",
            "replacement_candidate": "contingent_psr",
        },
    ]
    status = "complete" if all(check["status"] == "complete" for check in checks) else "open"
    return {
        "status": status,
        "argument_id": model["argument_id"],
        "scope": "psr_taxonomy_countermodels_and_partial_bridge_not_soundness_proof",
        "checks": checks,
        "remaining_risks": [
            "contingent PSR remains philosophically disputed",
            "brute fact and infinite regress alternatives are catalogued but not refuted",
            "necessary ground still lacks personhood, omniscience, omnipotence, and perfect goodness bridges",
        ],
    }


def _build_evil_hiddenness_constraints() -> dict[str, Any]:
    return {
        "status": "encoded",
        "model": EVIL_HIDDENNESS_CONSTRAINT_MODEL,
        "warning": (
            "This records constraints and candidate responses. It does not solve "
            "the problem of evil, divine hiddenness, or religious diversity."
        ),
    }


def _build_evil_hiddenness_checks() -> dict[str, Any]:
    model = EVIL_HIDDENNESS_CONSTRAINT_MODEL
    target = _target_concept_index()[TARGET_PROOF_CONCEPT_ID]
    target_attributes = set(target.attributes)
    constraints = model["constraints"]
    responses = model["candidate_responses"]
    response_coverage = {
        constraint["id"]: [
            response["id"]
            for response in responses
            if constraint["id"] in response["addresses"]
        ]
        for constraint in constraints
    }
    all_targets_known = all(
        set(constraint["targets"]) <= target_attributes
        for constraint in constraints
    )
    all_constraints_addressed = all(response_coverage[constraint["id"]] for constraint in constraints)
    risk_count = sum(1 for response in responses if response.get("risk"))
    checks = [
        {
            "id": "check-constraint-taxonomy",
            "status": "complete" if {"logical_evil", "evidential_evil", "divine_hiddenness", "religious_diversity"} <= {c["id"] for c in constraints} else "open",
            "constraint_ids": [constraint["id"] for constraint in constraints],
        },
        {
            "id": "check-target-attribute-links",
            "status": "complete" if all_targets_known else "open",
            "target_concept_id": target.id,
            "target_attributes": sorted(target_attributes),
        },
        {
            "id": "check-candidate-response-coverage",
            "status": "complete" if all_constraints_addressed else "open",
            "response_coverage": response_coverage,
        },
        {
            "id": "check-unresolved-risks-retained",
            "status": "complete" if risk_count == len(responses) else "open",
            "risk_count": risk_count,
            "response_count": len(responses),
            "result": "candidate responses retain their risks instead of being promoted to proof",
        },
    ]
    status = "complete" if all(check["status"] == "complete" for check in checks) else "open"
    return {
        "status": status,
        "argument_id": model["argument_id"],
        "scope": "constraint_ledger_not_refutation_of_counterarguments",
        "checks": checks,
        "remaining_risks": [
            "candidate theodicies and defenses remain contested",
            "hiddenness and non-resistant nonbelief remain live objections",
            "religious diversity still underdetermines the target concept without further argument",
        ],
    }


def _build_ontological_soundness_dossier() -> dict[str, Any]:
    return {
        "status": "contested",
        "dossier": ONTOLOGICAL_SOUNDNESS_DOSSIER,
        "warning": (
            "This dossier gathers support and objections for the possibility "
            "premise. It does not prove the premise sound."
        ),
    }


def _build_attribute_coherence_ledger() -> dict[str, Any]:
    return {
        "status": "contested",
        "ledger": ATTRIBUTE_COHERENCE_LEDGER,
        "warning": (
            "This ledger narrows the possibility-premise work by checking target "
            "attribute tensions. It does not establish metaphysical possibility."
        ),
    }


def _build_attribute_coherence_checks() -> dict[str, Any]:
    ledger = ATTRIBUTE_COHERENCE_LEDGER
    target = _target_concept_index()[TARGET_PROOF_CONCEPT_ID]
    target_attributes = set(target.attributes)
    questions = ledger["attribute_questions"]
    covered_attributes = {
        attribute
        for question in questions
        for attribute in question["attributes"]
    }
    unresolved_questions = [
        question["id"] for question in questions
        if question["status"] in {"contested", "candidate_open"}
    ]
    defeater_tests = ledger["defeater_tests"]
    direct_contradiction = next(
        test for test in defeater_tests
        if test["id"] == "direct-definition-contradiction"
    )
    checks = [
        {
            "id": "check-target-attribute-coverage",
            "status": "complete" if target_attributes <= covered_attributes else "open",
            "target_concept_id": target.id,
            "covered_attributes": sorted(covered_attributes),
            "missing_attributes": sorted(target_attributes - covered_attributes),
        },
        {
            "id": "check-defeater-tests-present",
            "status": "complete" if len(defeater_tests) >= 3 else "open",
            "defeater_test_ids": [test["id"] for test in defeater_tests],
        },
        {
            "id": "check-direct-definition-contradiction",
            "status": "complete" if direct_contradiction["status"] == "not_found_in_current_schema" else "open",
            "result": direct_contradiction["status"],
            "scope": direct_contradiction["scope"],
        },
        {
            "id": "check-unresolved-attribute-tensions-retained",
            "status": "contested" if unresolved_questions else "complete",
            "unresolved_question_ids": unresolved_questions,
            "result": "attribute tensions remain localized instead of erased",
        },
        {
            "id": "check-possibility-not-established",
            "status": "contested" if ledger["verdict"] == "contested" else "open",
            "verdict": ledger["verdict"],
            "result": "no direct schema contradiction is found, but metaphysical possibility is not proved",
        },
    ]
    return {
        "status": "contested",
        "argument_id": ledger["argument_id"],
        "target_premise_id": ledger["target_premise_id"],
        "target_concept_id": ledger["target_concept_id"],
        "scope": "attribute_coherence_screen_not_possibility_proof",
        "checks": checks,
        "remaining_risks": [
            "future freedom and omniscience remain model-dependent",
            "evil and hiddenness still pressure perfect goodness",
            "necessary personhood is not derived from necessary reality",
        ],
    }


def _build_coherent_conceivability_model() -> dict[str, Any]:
    return {
        "status": "candidate_supported_contested",
        "model": COHERENT_CONCEIVABILITY_MODEL,
        "warning": (
            "This model supplies candidate repairs for target-attribute tensions. "
            "It supports coherent conceivability only in a local model and does "
            "not establish metaphysical possibility."
        ),
    }


def _build_coherent_conceivability_checks() -> dict[str, Any]:
    model = COHERENT_CONCEIVABILITY_MODEL
    attribute_ledger = ATTRIBUTE_COHERENCE_LEDGER
    tension_ids = {question["id"] for question in attribute_ledger["attribute_questions"]}
    repairs = model["tension_repairs"]
    repair_tension_ids = {repair["tension_id"] for repair in repairs}
    defeaters = model["defeaters"]
    explicit_contradiction = next(
        defeater for defeater in defeaters
        if defeater["id"] == "explicit-contradiction"
    )
    live_defeaters = [
        defeater["id"] for defeater in defeaters
        if defeater["status"] == "live"
    ]
    checks = [
        {
            "id": "check-every-tension-has-repair-model",
            "status": "complete" if tension_ids <= repair_tension_ids else "open",
            "tension_ids": sorted(tension_ids),
            "repaired_tension_ids": sorted(repair_tension_ids),
            "missing_repair_tension_ids": sorted(tension_ids - repair_tension_ids),
        },
        {
            "id": "check-repair-models-are-candidates",
            "status": "complete" if all(repair["status"] == "candidate_model" for repair in repairs) else "open",
            "repair_model_ids": [repair["repair_model_id"] for repair in repairs],
        },
        {
            "id": "check-explicit-contradiction-not-found",
            "status": "complete" if explicit_contradiction["status"] == "not_found" else "open",
            "result": explicit_contradiction["result"],
        },
        {
            "id": "check-live-defeaters-retained",
            "status": "contested" if live_defeaters else "complete",
            "live_defeater_ids": live_defeaters,
            "result": "coherent conceivability remains contested because live defeaters remain",
        },
        {
            "id": "check-not-promoted-to-metaphysical-possibility",
            "status": "contested" if model["verdict"] == "candidate_supported_contested" else "open",
            "verdict": model["verdict"],
            "result": "candidate coherent conceivability is not metaphysical possibility",
        },
    ]
    return {
        "status": "candidate_supported_contested",
        "argument_id": model["argument_id"],
        "target_premise_id": model["target_premise_id"],
        "target_concept_id": model["target_concept_id"],
        "scope": "local_coherent_conceivability_model_not_metaphysical_possibility",
        "checks": checks,
        "remaining_risks": [
            "repair models may be ad hoc",
            "non-theistic evaluators may reject the conceivability standard",
            "local coherence does not entail metaphysical possibility",
        ],
    }


def _build_metaphysical_possibility_bridge() -> dict[str, Any]:
    return {
        "status": "contested",
        "bridge": METAPHYSICAL_POSSIBILITY_BRIDGE,
        "warning": (
            "This bridge evaluates whether coherent conceivability can license "
            "metaphysical possibility. It does not close the bridge."
        ),
    }


def _build_metaphysical_possibility_checks(
    coherent_conceivability_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    bridge = METAPHYSICAL_POSSIBILITY_BRIDGE
    coherent_conceivability_checks = (
        coherent_conceivability_checks or _build_coherent_conceivability_checks()
    )
    support_routes = bridge["support_routes"]
    defeater_routes = bridge["defeater_routes"]
    live_defeater_ids = [
        route["id"] for route in defeater_routes
        if route["status"] == "live"
    ]
    complete_support_ids = [
        route["id"] for route in support_routes
        if route["status"] == "complete"
    ]
    candidate_support_ids = [
        route["id"] for route in support_routes
        if route["status"] in {"candidate", "candidate_weak"}
    ]
    checks = [
        {
            "id": "check-coherent-conceivability-input-linked",
            "status": "complete",
            "artifact": "coherent-conceivability-checks.json",
            "artifact_status": coherent_conceivability_checks["status"],
            "input_stage_id": bridge["input_stage_id"],
        },
        {
            "id": "check-support-routes-present",
            "status": "complete" if len(support_routes) >= 3 else "open",
            "support_route_ids": [route["id"] for route in support_routes],
            "candidate_support_route_ids": candidate_support_ids,
        },
        {
            "id": "check-defeater-routes-present",
            "status": "complete" if len(defeater_routes) >= 3 else "open",
            "defeater_route_ids": [route["id"] for route in defeater_routes],
            "live_defeater_ids": live_defeater_ids,
        },
        {
            "id": "check-independent-complete-route-missing",
            "status": "contested" if not complete_support_ids else "complete",
            "complete_support_route_ids": complete_support_ids,
            "result": "no support route is independently complete",
        },
        {
            "id": "check-live-defeaters-block-bridge",
            "status": "contested" if live_defeater_ids else "complete",
            "live_defeater_ids": live_defeater_ids,
            "result": "live defeaters block promotion to metaphysical possibility",
        },
        {
            "id": "check-bridge-not-promoted",
            "status": "contested" if bridge["verdict"] == "contested" else "open",
            "verdict": bridge["verdict"],
            "decision_rule": bridge["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "argument_id": bridge["argument_id"],
        "target_premise_id": bridge["target_premise_id"],
        "target_concept_id": bridge["target_concept_id"],
        "scope": "conceivability_to_metaphysical_possibility_bridge_not_proof",
        "checks": checks,
        "remaining_risks": [
            "conceivability may be epistemic rather than metaphysical",
            "the modal premise may beg the question",
            "rival necessary ultimates retain parity pressure",
        ],
    }


def _build_possible_necessary_existence_bridge() -> dict[str, Any]:
    return {
        "status": "contested",
        "bridge": POSSIBLE_NECESSARY_EXISTENCE_BRIDGE,
        "warning": (
            "This bridge evaluates whether metaphysical possibility can be used "
            "as possible necessary existence for the modal proof. It does not "
            "settle soundness."
        ),
    }


def _build_definition_smuggling_audit() -> dict[str, Any]:
    return {
        "status": "contested",
        "audit": DEFINITION_SMUGGLING_AUDIT,
        "warning": (
            "This audit separates target definition, conditional modal validity, "
            "and actual existence claims. It does not prove that the possibility "
            "premise is non-question-begging."
        ),
    }


def _build_definition_smuggling_checks() -> dict[str, Any]:
    audit = DEFINITION_SMUGGLING_AUDIT
    distinctions = audit["distinctions"]
    tests = audit["smuggling_tests"]
    live_objections = [
        objection["id"] for objection in audit["live_objections"]
        if objection["status"] == "live"
    ]
    failing_tests = [
        test["id"] for test in tests
        if test["status"] == "fails"
    ]
    checks = [
        {
            "id": "check-distinction-rules-present",
            "status": "complete" if len(distinctions) >= 3 else "open",
            "distinction_ids": [rule["id"] for rule in distinctions],
        },
        {
            "id": "check-smuggling-tests-present",
            "status": "complete" if len(tests) >= 4 else "open",
            "smuggling_test_ids": [test["id"] for test in tests],
        },
        {
            "id": "check-no-syntactic-actuality-smuggling",
            "status": "complete" if all(
                test["status"] == "passes"
                for test in tests
                if test["id"] != "possibility-premise-independent-support"
            ) else "open",
            "passed_test_ids": [
                test["id"] for test in tests
                if test["status"] == "passes"
            ],
        },
        {
            "id": "check-independent-support-still-fails",
            "status": "contested" if "possibility-premise-independent-support" in failing_tests else "complete",
            "failing_test_ids": failing_tests,
            "result": "the premise is not syntactically smuggled, but independent support remains incomplete",
        },
        {
            "id": "check-live-objections-retained",
            "status": "contested" if live_objections else "complete",
            "live_objection_ids": live_objections,
            "result": "definition-smuggling objections remain live",
        },
    ]
    return {
        "status": "contested",
        "argument_id": audit["argument_id"],
        "target_premise_id": audit["target_premise_id"],
        "target_concept_id": audit["target_concept_id"],
        "scope": "definition_smuggling_audit_not_soundness_proof",
        "checks": checks,
        "remaining_risks": [
            "necessary existence may still encode a controversial modal thesis",
            "independent possibility support remains incomplete",
            "rival necessary concepts still require a uniqueness filter",
        ],
    }


def _build_rival_necessary_parity_audit() -> dict[str, Any]:
    return {
        "status": "contested",
        "audit": RIVAL_NECESSARY_PARITY_AUDIT,
        "warning": (
            "This audit compares rival necessary concepts against the classical "
            "theism target. It does not establish uniqueness."
        ),
    }


def _build_positive_property_filter_audit() -> dict[str, Any]:
    return {
        "status": "contested",
        "audit": POSITIVE_PROPERTY_FILTER_AUDIT,
        "warning": (
            "This audit evaluates whether the positive-property filter blocks "
            "bad-god parity. It does not establish the filter independently."
        ),
    }


def _build_positive_grounding_audit() -> dict[str, Any]:
    return {
        "status": "contested",
        "audit": POSITIVE_GROUNDING_AUDIT,
        "warning": (
            "This audit evaluates whether the positive-property predicate has "
            "non-arbitrary grounding. It does not establish that grounding."
        ),
    }


def _build_moral_perfection_grounding_audit() -> dict[str, Any]:
    return {
        "status": "contested",
        "audit": MORAL_PERFECTION_GROUNDING_AUDIT,
        "warning": (
            "This audit evaluates whether moral perfection can ground positivity "
            "without circularly assuming the target God."
        ),
    }


def _build_evil_hiddenness_moral_pressure_audit() -> dict[str, Any]:
    return {
        "status": "contested",
        "audit": EVIL_HIDDENNESS_MORAL_PRESSURE_AUDIT,
        "warning": (
            "This audit checks how evil and hiddenness pressure moral perfection "
            "grounding. It does not solve those constraints."
        ),
    }


def _build_evidential_evil_probability_audit() -> dict[str, Any]:
    return {
        "status": "contested",
        "audit": EVIDENTIAL_EVIL_PROBABILITY_AUDIT,
        "warning": (
            "This audit decomposes evidential evil into probability obligations. "
            "It does not solve theodicy or assign final likelihoods."
        ),
    }


def _build_evidential_evil_likelihood_ledger() -> dict[str, Any]:
    return {
        "status": "contested",
        "ledger": EVIDENTIAL_EVIL_LIKELIHOOD_LEDGER,
        "warning": (
            "This ledger assigns candidate probability intervals for sensitivity "
            "analysis only. It does not establish final likelihoods."
        ),
    }


def _build_evidential_evil_dependence_model() -> dict[str, Any]:
    return {
        "status": "contested",
        "model": EVIDENTIAL_EVIL_DEPENDENCE_MODEL,
        "warning": (
            "This model disciplines evidential aggregation by representing dependence "
            "and sensitivity cases. It does not produce a final posterior."
        ),
    }


def _build_evidential_evil_calibration_ledger() -> dict[str, Any]:
    return {
        "status": "contested",
        "ledger": EVIDENTIAL_EVIL_CALIBRATION_LEDGER,
        "warning": (
            "This ledger records candidate cluster weights and dependence strengths. "
            "It does not provide an independently calibrated posterior."
        ),
    }


def _build_evidential_evil_case_corpus() -> dict[str, Any]:
    return {
        "status": "contested",
        "corpus": EVIDENTIAL_EVIL_CASE_CORPUS,
        "warning": (
            "This corpus maps representative case families for calibration. "
            "It is not yet a reviewed, cited case database."
        ),
    }


def _build_evidential_evil_reviewed_case_records() -> dict[str, Any]:
    return {
        "status": "contested",
        "records": EVIDENTIAL_EVIL_REVIEWED_CASE_RECORDS,
        "warning": (
            "These records attach cited philosophical source coverage to case families. "
            "They are not yet an empirical case database."
        ),
    }


def _build_evidential_evil_empirical_expansion_ledger() -> dict[str, Any]:
    return {
        "status": "contested",
        "ledger": EVIDENTIAL_EVIL_EMPIRICAL_EXPANSION_LEDGER,
        "warning": (
            "This ledger defines empirical record classes and ingestion requirements. "
            "It does not ingest or calibrate primary datasets."
        ),
    }


def _build_evidential_evil_primary_dataset_selection() -> dict[str, Any]:
    return {
        "status": "contested",
        "selection": EVIDENTIAL_EVIL_PRIMARY_DATASET_SELECTION,
        "warning": (
            "This selection records official and peer-reviewed dataset candidates. "
            "It does not fetch or parse the datasets."
        ),
    }


def _build_evidential_evil_dataset_ingestion_manifest() -> dict[str, Any]:
    return {
        "status": "contested",
        "manifest": EVIDENTIAL_EVIL_DATASET_INGESTION_MANIFEST,
        "warning": (
            "This manifest defines fetch, hash, parse, and privacy gates. "
            "It does not execute dataset ingestion."
        ),
    }


def _build_evidential_evil_license_privacy_review() -> dict[str, Any]:
    return {
        "status": "contested",
        "review": EVIDENTIAL_EVIL_LICENSE_PRIVACY_REVIEW,
        "warning": (
            "This review records terms and privacy gates for ingestion. "
            "It is not legal advice and does not authorize retention."
        ),
    }


def _build_evidential_evil_attribution_template_ledger() -> dict[str, Any]:
    return {
        "status": "contested",
        "ledger": EVIDENTIAL_EVIL_ATTRIBUTION_TEMPLATE_LEDGER,
        "warning": (
            "These are draft attribution templates for auditability. "
            "They are not publication approval or source-data reuse authorization."
        ),
    }


def _build_evidential_evil_attribution_template_checks() -> dict[str, Any]:
    ledger = EVIDENTIAL_EVIL_ATTRIBUTION_TEMPLATE_LEDGER
    review = EVIDENTIAL_EVIL_LICENSE_PRIVACY_REVIEW
    reviewed_source_ids = {item["source_id"] for item in review["license_privacy_items"]}
    template_source_ids = {template["source_id"] for template in ledger["templates"]}
    expected_required_fields = {
        "source_title",
        "source_url",
        "retrieved_at",
        "derived_table_id",
        "hash",
        "license_decision_id",
    }
    templates_with_required_fields = [
        template["source_id"] for template in ledger["templates"]
        if expected_required_fields <= set(template["required_fields"])
        and template["attribution_text"]
        and template["source_url"]
    ]
    draft_template_ids = [
        template["source_id"] for template in ledger["templates"]
        if template["publication_status"] == "draft_not_approved" and template["needs_license_decision"] is True
    ]
    open_publication_requirement_ids = [
        requirement["id"] for requirement in ledger["publication_requirements"]
        if requirement["status"] == "open"
    ]
    checks = [
        {
            "id": "check-license-privacy-review-linked",
            "status": "complete"
            if ledger["input_license_privacy_review_id"] == review["id"]
            else "open",
            "artifact": "evidential-evil-license-privacy-review.json",
            "input_license_privacy_review_id": ledger["input_license_privacy_review_id"],
        },
        {
            "id": "check-every-reviewed-source-has-template",
            "status": "complete" if reviewed_source_ids <= template_source_ids else "open",
            "reviewed_source_ids": sorted(reviewed_source_ids),
            "template_source_ids": sorted(template_source_ids),
            "missing_source_ids": sorted(reviewed_source_ids - template_source_ids),
        },
        {
            "id": "check-required-attribution-fields-present",
            "status": "complete" if len(templates_with_required_fields) == len(ledger["templates"]) else "open",
            "templates_with_required_fields": templates_with_required_fields,
            "required_fields": sorted(expected_required_fields),
        },
        {
            "id": "check-templates-remain-draft",
            "status": "contested" if len(draft_template_ids) == len(ledger["templates"]) else "open",
            "draft_template_source_ids": draft_template_ids,
            "result": "templates are recorded for auditability but are not approved publication text",
        },
        {
            "id": "check-publication-requirements-still-open",
            "status": "contested" if open_publication_requirement_ids else "complete",
            "open_publication_requirement_ids": open_publication_requirement_ids,
            "result": "source-specific decisions, hashes, versions, and final review are still required",
        },
        {
            "id": "check-attribution-templates-not-promoted",
            "status": "contested" if ledger["verdict"] == "contested" else "open",
            "verdict": ledger["verdict"],
            "decision_rule": ledger["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "argument_id": ledger["argument_id"],
        "target_premise_id": ledger["target_premise_id"],
        "target_concept_id": ledger["target_concept_id"],
        "scope": "evidential_evil_attribution_templates_not_publication_approval",
        "checks": checks,
        "remaining_risks": [
            "license decisions are not recorded",
            "source hashes and versions are not filled",
            "final attribution review has not been performed",
        ],
    }


def _build_evidential_evil_license_decision_packet() -> dict[str, Any]:
    return {
        "status": "contested",
        "packet": EVIDENTIAL_EVIL_LICENSE_DECISION_PACKET,
        "warning": (
            "These records are source-specific candidate decisions. "
            "They are not legal advice and do not authorize retained ingestion or redistribution."
        ),
    }


def _build_evidential_evil_license_decision_checks(
    evidential_evil_attribution_template_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    packet = EVIDENTIAL_EVIL_LICENSE_DECISION_PACKET
    review = EVIDENTIAL_EVIL_LICENSE_PRIVACY_REVIEW
    evidential_evil_attribution_template_checks = (
        evidential_evil_attribution_template_checks or _build_evidential_evil_attribution_template_checks()
    )
    reviewed_source_ids = {item["source_id"] for item in review["license_privacy_items"]}
    decision_source_ids = {record["source_id"] for record in packet["records"]}
    required_action_source_ids = [
        record["source_id"] for record in packet["records"]
        if record["evidence_url"] and record["required_actions"] and record["retention_decision"]
    ]
    non_authorized_source_ids = [
        record["source_id"] for record in packet["records"]
        if record["retention_decision"].startswith("not_authorized_until_")
    ]
    manual_review_source_ids = [
        record["source_id"] for record in packet["records"]
        if record["candidate_decision"].startswith("manual_review_required")
    ]
    checks = [
        {
            "id": "check-license-privacy-review-linked",
            "status": "complete"
            if packet["input_license_privacy_review_id"] == review["id"]
            else "open",
            "artifact": "evidential-evil-license-privacy-review.json",
            "input_license_privacy_review_id": packet["input_license_privacy_review_id"],
        },
        {
            "id": "check-attribution-template-ledger-linked",
            "status": "complete"
            if packet["input_attribution_template_ledger_id"] == EVIDENTIAL_EVIL_ATTRIBUTION_TEMPLATE_LEDGER["id"]
            else "open",
            "artifact": "evidential-evil-attribution-template-checks.json",
            "artifact_status": evidential_evil_attribution_template_checks["status"],
        },
        {
            "id": "check-every-reviewed-source-has-license-decision-record",
            "status": "complete" if reviewed_source_ids <= decision_source_ids else "open",
            "reviewed_source_ids": sorted(reviewed_source_ids),
            "decision_source_ids": sorted(decision_source_ids),
            "missing_source_ids": sorted(reviewed_source_ids - decision_source_ids),
        },
        {
            "id": "check-evidence-and-required-actions-recorded",
            "status": "complete" if len(required_action_source_ids) == len(packet["records"]) else "open",
            "source_ids": required_action_source_ids,
            "retrieved_at": packet["retrieved_at"],
        },
        {
            "id": "check-retained-ingestion-not-authorized",
            "status": "contested" if len(non_authorized_source_ids) == len(packet["records"]) else "open",
            "non_authorized_source_ids": non_authorized_source_ids,
            "authorization_state": packet["authorization_state"],
        },
        {
            "id": "check-manual-review-risks-retained",
            "status": "contested" if manual_review_source_ids else "complete",
            "manual_review_source_ids": manual_review_source_ids,
            "result": "some sources require manual terms review before bulk or retained ingestion",
        },
        {
            "id": "check-license-decisions-not-promoted",
            "status": "contested" if packet["verdict"] == "contested" else "open",
            "verdict": packet["verdict"],
            "decision_rule": packet["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "argument_id": packet["argument_id"],
        "target_premise_id": packet["target_premise_id"],
        "target_concept_id": packet["target_concept_id"],
        "scope": "evidential_evil_license_decisions_not_retention_authorization",
        "checks": checks,
        "remaining_risks": [
            "retained ingestion is still false",
            "some sources require manual terms review",
            "dataset versions, hashes, and privacy minimization are not recorded",
        ],
    }


def _build_evidential_evil_microdata_minimization_policy() -> dict[str, Any]:
    return {
        "status": "contested",
        "policy": EVIDENTIAL_EVIL_MICRODATA_MINIMIZATION_POLICY,
        "warning": (
            "This policy records minimization constraints only. "
            "It does not authorize dataset download, retained ingestion, or publication."
        ),
    }


def _build_evidential_evil_derived_aggregate_schema() -> dict[str, Any]:
    return {
        "status": "contested",
        "schema": EVIDENTIAL_EVIL_DERIVED_AGGREGATE_SCHEMA,
        "warning": (
            "This schema records allowed aggregate outputs only. "
            "It does not fetch, retain, materialize, or publish source data."
        ),
    }


def _build_evidential_evil_source_version_hash_preflight() -> dict[str, Any]:
    return {
        "status": "contested",
        "preflight": EVIDENTIAL_EVIL_SOURCE_VERSION_HASH_PREFLIGHT,
        "warning": (
            "This preflight records official version locators and hash targets only. "
            "It does not download, retain, materialize, or publish source data."
        ),
    }


def _build_evidential_evil_source_acquisition_hash_runbook() -> dict[str, Any]:
    return {
        "status": "contested",
        "runbook": EVIDENTIAL_EVIL_SOURCE_ACQUISITION_HASH_RUNBOOK,
        "warning": (
            "This runbook records acquisition, hashing, logging, and pruning instructions only. "
            "It does not execute downloads or store raw source data."
        ),
    }


def _build_evidential_evil_suppression_report_template() -> dict[str, Any]:
    return {
        "status": "contested",
        "template": EVIDENTIAL_EVIL_SUPPRESSION_REPORT_TEMPLATE,
        "warning": (
            "This template records publication suppression reports only. "
            "It does not materialize aggregate tables or authorize publication."
        ),
    }


def _build_evidential_evil_suppression_report_template_checks(
    evidential_evil_source_acquisition_hash_runbook_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    template = EVIDENTIAL_EVIL_SUPPRESSION_REPORT_TEMPLATE
    schema = EVIDENTIAL_EVIL_DERIVED_AGGREGATE_SCHEMA
    evidential_evil_source_acquisition_hash_runbook_checks = (
        evidential_evil_source_acquisition_hash_runbook_checks
        or _build_evidential_evil_source_acquisition_hash_runbook_checks()
    )
    schema_table_ids = {table["table_id"] for table in schema["tables"]}
    template_table_ids = {table["table_id"] for table in template["table_templates"]}
    templates_with_required_checks = [
        table["table_id"] for table in template["table_templates"]
        if set(table["required_pre_publication_checks"]) >= {
            "source_hashes_verified",
            "blocked_columns_absent_from_output",
            "small_cell_suppression_applied",
            "license_attribution_present",
            "no_raw_source_substitute_database",
        }
        and table["materialization_status"] == "not_materialized"
    ]
    templates_with_thresholds = [
        table["table_id"] for table in template["table_templates"]
        if table["minimum_cell_threshold"] >= 10
    ]
    open_execution_requirement_ids = [
        requirement["id"] for requirement in template["execution_requirements"]
        if requirement["status"] == "open"
    ]
    checks = [
        {
            "id": "check-derived-aggregate-schema-linked",
            "status": "complete"
            if template["input_derived_aggregate_schema_id"] == schema["id"]
            else "open",
            "artifact": "evidential-evil-derived-aggregate-schema.json",
            "input_derived_aggregate_schema_id": template["input_derived_aggregate_schema_id"],
        },
        {
            "id": "check-source-acquisition-hash-runbook-linked",
            "status": "complete"
            if template["input_source_acquisition_hash_runbook_id"] == EVIDENTIAL_EVIL_SOURCE_ACQUISITION_HASH_RUNBOOK["id"]
            else "open",
            "artifact": "evidential-evil-source-acquisition-hash-runbook-checks.json",
            "artifact_status": evidential_evil_source_acquisition_hash_runbook_checks["status"],
        },
        {
            "id": "check-every-schema-table-has-suppression-template",
            "status": "complete" if schema_table_ids <= template_table_ids else "open",
            "schema_table_ids": sorted(schema_table_ids),
            "template_table_ids": sorted(template_table_ids),
            "missing_table_ids": sorted(schema_table_ids - template_table_ids),
        },
        {
            "id": "check-report-schema-recorded",
            "status": "complete"
            if template["report_schema"]["artifact_name"] == "suppression-report.json"
            and "source_hashes_verified" in template["report_schema"]["required_fields"]
            and "blocked_columns_verified" in template["report_schema"]["required_fields"]
            else "open",
            "report_schema": template["report_schema"],
        },
        {
            "id": "check-required-pre-publication-checks-recorded",
            "status": "complete" if len(templates_with_required_checks) == len(template["table_templates"]) else "open",
            "table_ids": templates_with_required_checks,
        },
        {
            "id": "check-small-cell-thresholds-recorded",
            "status": "complete" if len(templates_with_thresholds) == len(template["table_templates"]) else "open",
            "table_ids": templates_with_thresholds,
            "minimum_cell_threshold": 10,
        },
        {
            "id": "check-suppression-reports-still-open",
            "status": "contested" if open_execution_requirement_ids else "complete",
            "open_execution_requirement_ids": open_execution_requirement_ids,
            "authorization_state": template["authorization_state"],
        },
        {
            "id": "check-suppression-template-not-promoted",
            "status": "contested" if template["verdict"] == "contested" else "open",
            "verdict": template["verdict"],
            "decision_rule": template["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "argument_id": template["argument_id"],
        "target_premise_id": template["target_premise_id"],
        "target_concept_id": template["target_concept_id"],
        "scope": "evidential_evil_suppression_report_template_not_materialized",
        "checks": checks,
        "remaining_risks": [
            "aggregate tables are not materialized",
            "suppression reports are not filled",
            "publication review is not complete",
        ],
    }


def _build_evidential_evil_source_acquisition_hash_runbook_checks() -> dict[str, Any]:
    runbook = EVIDENTIAL_EVIL_SOURCE_ACQUISITION_HASH_RUNBOOK
    preflight = EVIDENTIAL_EVIL_SOURCE_VERSION_HASH_PREFLIGHT
    preflight_source_ids = {record["source_id"] for record in preflight["source_records"]}
    runbook_source_ids = {step["source_id"] for step in runbook["steps"]}
    steps_with_hash_commands = [
        step["source_id"] for step in runbook["steps"]
        if "shasum -a 256" in step["hash_command_template"]
        and step["execution_status"] == "not_executed"
    ]
    steps_with_required_logs = [
        step["source_id"] for step in runbook["steps"]
        if set(step["required_log_events"]) >= {
            "source_authorization_recorded",
            "source_file_acquired",
            "source_hash_recorded",
            "raw_source_cache_pruned_or_retained_with_reason",
        }
    ]
    open_execution_requirement_ids = [
        requirement["id"] for requirement in runbook["execution_requirements"]
        if requirement["status"] == "open"
    ]
    checks = [
        {
            "id": "check-source-version-hash-preflight-linked",
            "status": "complete"
            if runbook["input_source_version_hash_preflight_id"] == preflight["id"]
            else "open",
            "artifact": "evidential-evil-source-version-hash-preflight.json",
            "input_source_version_hash_preflight_id": runbook["input_source_version_hash_preflight_id"],
        },
        {
            "id": "check-every-preflight-source-has-acquisition-step",
            "status": "complete" if preflight_source_ids <= runbook_source_ids else "open",
            "preflight_source_ids": sorted(preflight_source_ids),
            "runbook_source_ids": sorted(runbook_source_ids),
            "missing_source_ids": sorted(preflight_source_ids - runbook_source_ids),
        },
        {
            "id": "check-hash-manifest-schema-recorded",
            "status": "complete"
            if runbook["hash_manifest_schema"]["hash_algorithm"] == "sha256"
            and "sha256" in runbook["hash_manifest_schema"]["required_fields"]
            else "open",
            "artifact_name": runbook["hash_manifest_schema"]["artifact_name"],
            "required_fields": runbook["hash_manifest_schema"]["required_fields"],
        },
        {
            "id": "check-hash-command-templates-recorded-not-executed",
            "status": "complete" if len(steps_with_hash_commands) == len(runbook["steps"]) else "open",
            "source_ids": steps_with_hash_commands,
            "result": "hash commands are templates only; every step remains not_executed",
        },
        {
            "id": "check-required-log-events-recorded",
            "status": "complete" if len(steps_with_required_logs) == len(runbook["steps"]) else "open",
            "source_ids": steps_with_required_logs,
        },
        {
            "id": "check-cache-retention-and-prune-step-recorded",
            "status": "complete"
            if runbook["cache_policy"]["retention_rule"]
            and runbook["cache_policy"]["prune_step_template"]
            and runbook["cache_policy"]["repo_storage_allowed"] is False
            else "open",
            "cache_policy": runbook["cache_policy"],
        },
        {
            "id": "check-source-acquisition-still-open",
            "status": "contested" if open_execution_requirement_ids else "complete",
            "open_execution_requirement_ids": open_execution_requirement_ids,
            "authorization_state": runbook["authorization_state"],
        },
        {
            "id": "check-source-acquisition-runbook-not-promoted",
            "status": "contested" if runbook["verdict"] == "contested" else "open",
            "verdict": runbook["verdict"],
            "decision_rule": runbook["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "argument_id": runbook["argument_id"],
        "target_premise_id": runbook["target_premise_id"],
        "target_concept_id": runbook["target_concept_id"],
        "scope": "evidential_evil_source_acquisition_hash_runbook_not_executed",
        "checks": checks,
        "remaining_risks": [
            "source-specific authorization is not recorded",
            "source files are not acquired",
            "source hash manifest is not materialized",
            "raw source cache retention is only a candidate policy",
        ],
    }


def _build_evidential_evil_source_version_hash_preflight_checks(
    evidential_evil_source_acquisition_hash_runbook_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    preflight = EVIDENTIAL_EVIL_SOURCE_VERSION_HASH_PREFLIGHT
    schema = EVIDENTIAL_EVIL_DERIVED_AGGREGATE_SCHEMA
    evidential_evil_source_acquisition_hash_runbook_checks = (
        evidential_evil_source_acquisition_hash_runbook_checks
        or _build_evidential_evil_source_acquisition_hash_runbook_checks()
    )
    schema_source_ids = {
        source_id
        for table in schema["tables"]
        for source_id in table["source_ids"]
    }
    preflight_source_ids = {record["source_id"] for record in preflight["source_records"]}
    source_ids_with_locators = [
        record["source_id"] for record in preflight["source_records"]
        if record["version_locator_url"] and record["candidate_version_label"]
    ]
    source_ids_with_hash_algorithm = [
        record["source_id"] for record in preflight["source_records"]
        if record["hash_algorithm"] == "sha256" and record["hash_target"]
    ]
    open_execution_requirement_ids = [
        requirement["id"] for requirement in preflight["execution_requirements"]
        if requirement["status"] == "open"
    ]
    table_binding_ids = {binding["table_id"] for binding in preflight["table_bindings"]}
    schema_table_ids = {table["table_id"] for table in schema["tables"]}
    checks = [
        {
            "id": "check-derived-aggregate-schema-linked",
            "status": "complete"
            if preflight["input_derived_aggregate_schema_id"] == schema["id"]
            else "open",
            "artifact": "evidential-evil-derived-aggregate-schema.json",
            "input_derived_aggregate_schema_id": preflight["input_derived_aggregate_schema_id"],
        },
        {
            "id": "check-every-schema-source-has-preflight-record",
            "status": "complete" if schema_source_ids <= preflight_source_ids else "open",
            "schema_source_ids": sorted(schema_source_ids),
            "preflight_source_ids": sorted(preflight_source_ids),
            "missing_source_ids": sorted(schema_source_ids - preflight_source_ids),
        },
        {
            "id": "check-version-locators-recorded",
            "status": "complete" if len(source_ids_with_locators) == len(preflight["source_records"]) else "open",
            "source_ids": source_ids_with_locators,
            "retrieved_at": preflight["retrieved_at"],
        },
        {
            "id": "check-hash-algorithm-and-targets-recorded",
            "status": "complete" if len(source_ids_with_hash_algorithm) == len(preflight["source_records"]) else "open",
            "source_ids": source_ids_with_hash_algorithm,
            "hash_algorithm": "sha256",
        },
        {
            "id": "check-table-bindings-present",
            "status": "complete" if schema_table_ids <= table_binding_ids else "open",
            "schema_table_ids": sorted(schema_table_ids),
            "table_binding_ids": sorted(table_binding_ids),
            "missing_table_ids": sorted(schema_table_ids - table_binding_ids),
        },
        {
            "id": "check-source-acquisition-hash-runbook-linked",
            "status": "complete",
            "artifact": "evidential-evil-source-acquisition-hash-runbook-checks.json",
            "artifact_status": evidential_evil_source_acquisition_hash_runbook_checks["status"],
            "result": "source acquisition and hashing instructions are recorded but not executed",
        },
        {
            "id": "check-downloads-and-hashes-still-open",
            "status": "contested" if open_execution_requirement_ids else "complete",
            "open_execution_requirement_ids": open_execution_requirement_ids,
            "authorization_state": preflight["authorization_state"],
        },
        {
            "id": "check-source-version-hash-preflight-not-promoted",
            "status": "contested" if preflight["verdict"] == "contested" else "open",
            "verdict": preflight["verdict"],
            "decision_rule": preflight["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "argument_id": preflight["argument_id"],
        "target_premise_id": preflight["target_premise_id"],
        "target_concept_id": preflight["target_concept_id"],
        "scope": "evidential_evil_source_version_hash_preflight_not_downloaded",
        "checks": checks,
        "remaining_risks": [
            "source files are not downloaded",
            "source hashes are not recorded",
            "suppression reports are not materialized",
        ],
    }


def _build_evidential_evil_derived_aggregate_schema_checks(
    evidential_evil_source_version_hash_preflight_checks: dict[str, Any] | None = None,
    evidential_evil_suppression_report_template_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    schema = EVIDENTIAL_EVIL_DERIVED_AGGREGATE_SCHEMA
    policy = EVIDENTIAL_EVIL_MICRODATA_MINIMIZATION_POLICY
    evidential_evil_source_version_hash_preflight_checks = (
        evidential_evil_source_version_hash_preflight_checks
        or _build_evidential_evil_source_version_hash_preflight_checks()
    )
    evidential_evil_suppression_report_template_checks = (
        evidential_evil_suppression_report_template_checks
        or _build_evidential_evil_suppression_report_template_checks()
    )
    policy_source_ids = {item["source_id"] for item in policy["source_policies"]}
    schema_source_ids = {
        source_id
        for table in schema["tables"]
        for source_id in table["source_ids"]
    }
    tables_with_allowlists = [
        table["table_id"] for table in schema["tables"]
        if table["allowed_columns"] and table["blocked_columns"] and table["suppression_rule"]
    ]
    tables_with_hash_placeholders = [
        table["table_id"] for table in schema["tables"]
        if "source_hash" in table["allowed_columns"] and table["version_hash_status"] == "not_recorded"
    ]
    raw_identifier_blocked_tables = [
        table["table_id"] for table in schema["tables"]
        if any(
            blocked in table["blocked_columns"]
            for blocked in ["direct_identifier", "respondent_id", "person_id", "patient_id"]
        )
    ]
    open_execution_requirement_ids = [
        requirement["id"] for requirement in schema["execution_requirements"]
        if requirement["status"] == "open"
    ]
    checks = [
        {
            "id": "check-microdata-policy-linked",
            "status": "complete"
            if schema["input_microdata_minimization_policy_id"] == policy["id"]
            else "open",
            "artifact": "evidential-evil-microdata-minimization-policy.json",
            "input_microdata_minimization_policy_id": schema["input_microdata_minimization_policy_id"],
        },
        {
            "id": "check-every-policy-source-has-derived-table",
            "status": "complete" if policy_source_ids <= schema_source_ids else "open",
            "policy_source_ids": sorted(policy_source_ids),
            "schema_source_ids": sorted(schema_source_ids),
            "missing_source_ids": sorted(policy_source_ids - schema_source_ids),
        },
        {
            "id": "check-table-allowlists-and-suppression-templates-present",
            "status": "complete" if len(tables_with_allowlists) == len(schema["tables"]) else "open",
            "table_ids": tables_with_allowlists,
        },
        {
            "id": "check-source-hash-placeholders-present",
            "status": "complete" if len(tables_with_hash_placeholders) == len(schema["tables"]) else "open",
            "table_ids": tables_with_hash_placeholders,
        },
        {
            "id": "check-raw-identifiers-blocked",
            "status": "complete" if len(raw_identifier_blocked_tables) >= 2 else "open",
            "table_ids": raw_identifier_blocked_tables,
            "result": "tables that could touch human-level data explicitly block identifiers",
        },
        {
            "id": "check-source-version-hash-preflight-linked",
            "status": "complete",
            "artifact": "evidential-evil-source-version-hash-preflight-checks.json",
            "artifact_status": evidential_evil_source_version_hash_preflight_checks["status"],
            "result": "source version locators and hash targets are recorded as preflight evidence only",
        },
        {
            "id": "check-suppression-report-template-linked",
            "status": "complete",
            "artifact": "evidential-evil-suppression-report-template-checks.json",
            "artifact_status": evidential_evil_suppression_report_template_checks["status"],
            "result": "publication suppression report templates are recorded but not materialized",
        },
        {
            "id": "check-materialization-requirements-still-open",
            "status": "contested" if open_execution_requirement_ids else "complete",
            "open_execution_requirement_ids": open_execution_requirement_ids,
            "authorization_state": schema["authorization_state"],
        },
        {
            "id": "check-derived-schema-not-promoted",
            "status": "contested" if schema["verdict"] == "contested" else "open",
            "verdict": schema["verdict"],
            "decision_rule": schema["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "argument_id": schema["argument_id"],
        "target_premise_id": schema["target_premise_id"],
        "target_concept_id": schema["target_concept_id"],
        "scope": "evidential_evil_derived_aggregate_schema_not_materialized_ingestion",
        "checks": checks,
        "remaining_risks": [
            "source hashes are not recorded",
            "suppression reports are not materialized",
            "source version locators are preflight records, not executed downloads",
        ],
    }


def _build_evidential_evil_microdata_minimization_checks(
    evidential_evil_license_decision_checks: dict[str, Any] | None = None,
    evidential_evil_derived_aggregate_schema_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    policy = EVIDENTIAL_EVIL_MICRODATA_MINIMIZATION_POLICY
    review = EVIDENTIAL_EVIL_LICENSE_PRIVACY_REVIEW
    evidential_evil_license_decision_checks = (
        evidential_evil_license_decision_checks or _build_evidential_evil_license_decision_checks()
    )
    evidential_evil_derived_aggregate_schema_checks = (
        evidential_evil_derived_aggregate_schema_checks or _build_evidential_evil_derived_aggregate_schema_checks()
    )
    reviewed_source_ids = {item["source_id"] for item in review["license_privacy_items"]}
    policy_source_ids = {item["source_id"] for item in policy["source_policies"]}
    non_retained_source_ids = [
        item["source_id"] for item in policy["source_policies"]
        if item["raw_retention_allowed"] is False and item["minimized_storage"]
    ]
    evidence_source_ids = [
        item["source_id"] for item in policy["source_policies"]
        if item["evidence_url"] and item["blocked_fields"]
    ]
    survey_minimized_source_ids = [
        item["source_id"] for item in policy["source_policies"]
        if item["source_id"] == "world-values-survey"
        and item["raw_retention_allowed"] is False
        and "respondent_row_retention" in item["blocked_fields"]
    ]
    open_execution_requirement_ids = [
        requirement["id"] for requirement in policy["execution_requirements"]
        if requirement["status"] == "open"
    ]
    checks = [
        {
            "id": "check-license-privacy-review-linked",
            "status": "complete"
            if policy["input_license_privacy_review_id"] == review["id"]
            else "open",
            "artifact": "evidential-evil-license-privacy-review.json",
            "input_license_privacy_review_id": policy["input_license_privacy_review_id"],
        },
        {
            "id": "check-license-decision-packet-linked",
            "status": "complete"
            if policy["input_license_decision_packet_id"] == EVIDENTIAL_EVIL_LICENSE_DECISION_PACKET["id"]
            else "open",
            "artifact": "evidential-evil-license-decision-checks.json",
            "artifact_status": evidential_evil_license_decision_checks["status"],
        },
        {
            "id": "check-every-reviewed-source-has-minimization-policy",
            "status": "complete" if reviewed_source_ids <= policy_source_ids else "open",
            "reviewed_source_ids": sorted(reviewed_source_ids),
            "policy_source_ids": sorted(policy_source_ids),
            "missing_source_ids": sorted(reviewed_source_ids - policy_source_ids),
        },
        {
            "id": "check-raw-retention-disabled",
            "status": "complete" if len(non_retained_source_ids) == len(policy["source_policies"]) else "open",
            "non_retained_source_ids": non_retained_source_ids,
            "global_controls": policy["global_controls"],
        },
        {
            "id": "check-source-evidence-and-blocked-fields-recorded",
            "status": "complete" if len(evidence_source_ids) == len(policy["source_policies"]) else "open",
            "source_ids": evidence_source_ids,
            "retrieved_at": policy["retrieved_at"],
        },
        {
            "id": "check-survey-microdata-minimized",
            "status": "complete" if survey_minimized_source_ids == ["world-values-survey"] else "open",
            "survey_minimized_source_ids": survey_minimized_source_ids,
            "result": "WVS respondent rows are blocked from retained storage in this policy",
        },
        {
            "id": "check-derived-aggregate-schema-linked",
            "status": "complete",
            "artifact": "evidential-evil-derived-aggregate-schema-checks.json",
            "artifact_status": evidential_evil_derived_aggregate_schema_checks["status"],
            "result": "derived aggregate schema records allowlists and suppression templates without materializing data",
        },
        {
            "id": "check-derived-aggregate-execution-requirements-open",
            "status": "contested" if open_execution_requirement_ids else "complete",
            "open_execution_requirement_ids": open_execution_requirement_ids,
            "result": "derived aggregate storage is still blocked until version, hash, and materialized suppression evidence exist",
        },
        {
            "id": "check-minimization-policy-not-promoted",
            "status": "contested" if policy["verdict"] == "contested" else "open",
            "verdict": policy["verdict"],
            "authorization_state": policy["authorization_state"],
            "decision_rule": policy["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "argument_id": policy["argument_id"],
        "target_premise_id": policy["target_premise_id"],
        "target_concept_id": policy["target_concept_id"],
        "scope": "evidential_evil_microdata_minimization_not_ingestion_authorization",
        "checks": checks,
        "remaining_risks": [
            "raw microdata storage is disabled, not executed",
            "derived aggregate storage is still blocked",
            "dataset versions, hashes, and materialized suppression reports are missing",
        ],
    }


def _build_evidential_evil_license_privacy_checks(
    evidential_evil_attribution_template_checks: dict[str, Any] | None = None,
    evidential_evil_license_decision_checks: dict[str, Any] | None = None,
    evidential_evil_derived_aggregate_schema_checks: dict[str, Any] | None = None,
    evidential_evil_microdata_minimization_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    review = EVIDENTIAL_EVIL_LICENSE_PRIVACY_REVIEW
    manifest = EVIDENTIAL_EVIL_DATASET_INGESTION_MANIFEST
    evidential_evil_attribution_template_checks = (
        evidential_evil_attribution_template_checks or _build_evidential_evil_attribution_template_checks()
    )
    evidential_evil_license_decision_checks = (
        evidential_evil_license_decision_checks
        or _build_evidential_evil_license_decision_checks(evidential_evil_attribution_template_checks)
    )
    evidential_evil_derived_aggregate_schema_checks = (
        evidential_evil_derived_aggregate_schema_checks or _build_evidential_evil_derived_aggregate_schema_checks()
    )
    evidential_evil_microdata_minimization_checks = (
        evidential_evil_microdata_minimization_checks
        or _build_evidential_evil_microdata_minimization_checks(
            evidential_evil_license_decision_checks,
            evidential_evil_derived_aggregate_schema_checks,
        )
    )
    manifest_source_ids = {plan["source_id"] for plan in manifest["ingestion_plans"]}
    reviewed_source_ids = {item["source_id"] for item in review["license_privacy_items"]}
    items_with_terms = [
        item["source_id"] for item in review["license_privacy_items"]
        if item["terms_url"] and item["status"] == "terms_identified_review_required"
    ]
    items_with_privacy = [
        item["source_id"] for item in review["license_privacy_items"]
        if item["privacy_risk"] and item["required_action"]
    ]
    open_gate_ids = [
        requirement["id"] for requirement in review["gate_requirements"]
        if requirement["status"] == "open"
    ]
    checks = [
        {
            "id": "check-ingestion-manifest-linked",
            "status": "complete" if review["input_ingestion_manifest_id"] == manifest["id"] else "open",
            "artifact": "evidential-evil-dataset-ingestion-checks.json",
            "input_ingestion_manifest_id": review["input_ingestion_manifest_id"],
        },
        {
            "id": "check-every-ingestion-source-has-review-item",
            "status": "complete" if manifest_source_ids <= reviewed_source_ids else "open",
            "manifest_source_ids": sorted(manifest_source_ids),
            "reviewed_source_ids": sorted(reviewed_source_ids),
            "missing_source_ids": sorted(manifest_source_ids - reviewed_source_ids),
        },
        {
            "id": "check-terms-urls-recorded",
            "status": "complete" if len(items_with_terms) == len(review["license_privacy_items"]) else "open",
            "items_with_terms": items_with_terms,
            "retrieved_at": review["retrieved_at"],
        },
        {
            "id": "check-privacy-tiers-recorded",
            "status": "complete" if len(items_with_privacy) == len(review["license_privacy_items"]) else "open",
            "items_with_privacy": items_with_privacy,
        },
        {
            "id": "check-license-decisions-still-open",
            "status": "contested"
            if evidential_evil_license_decision_checks["status"] == "contested"
            or evidential_evil_microdata_minimization_checks["status"] == "contested"
            else "complete",
            "open_gate_ids": open_gate_ids,
            "result": "candidate decisions are recorded, but no source is authorized for retained ingestion yet",
        },
        {
            "id": "check-license-decision-packet-linked",
            "status": "complete",
            "artifact": "evidential-evil-license-decision-checks.json",
            "artifact_status": evidential_evil_license_decision_checks["status"],
            "result": "candidate source-specific reuse decisions are linked but not promoted",
        },
        {
            "id": "check-attribution-template-linked",
            "status": "complete",
            "artifact": "evidential-evil-attribution-template-checks.json",
            "artifact_status": evidential_evil_attribution_template_checks["status"],
            "result": "draft attribution templates are linked but do not authorize publication",
        },
        {
            "id": "check-microdata-minimization-policy-linked",
            "status": "complete",
            "artifact": "evidential-evil-microdata-minimization-checks.json",
            "artifact_status": evidential_evil_microdata_minimization_checks["status"],
            "result": "microdata minimization policy is linked but does not authorize retained ingestion",
        },
        {
            "id": "check-review-not-promoted",
            "status": "contested" if review["verdict"] == "contested" else "open",
            "verdict": review["verdict"],
            "decision_rule": review["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "argument_id": review["argument_id"],
        "target_premise_id": review["target_premise_id"],
        "target_concept_id": review["target_concept_id"],
        "scope": "evidential_evil_license_privacy_review_not_authorization",
        "checks": checks,
        "remaining_risks": [
            "reuse decisions are recorded as candidate decisions, not authorization",
            "attribution templates are draft records, not publication approval",
            "microdata minimization is recorded as policy, not executed storage approval",
        ],
    }


def _build_evidential_evil_dataset_ingestion_checks(
    evidential_evil_license_privacy_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    manifest = EVIDENTIAL_EVIL_DATASET_INGESTION_MANIFEST
    selection = EVIDENTIAL_EVIL_PRIMARY_DATASET_SELECTION
    evidential_evil_license_privacy_checks = (
        evidential_evil_license_privacy_checks or _build_evidential_evil_license_privacy_checks()
    )
    selected_source_ids = {
        source_id
        for item in selection["dataset_selections"]
        for source_id in item["selected_source_ids"]
    }
    planned_source_ids = {plan["source_id"] for plan in manifest["ingestion_plans"]}
    plans_with_fetch_specs = [
        plan["source_id"] for plan in manifest["ingestion_plans"]
        if plan["fetch_url"] and plan["expected_format"] and plan["parser_target"]
    ]
    plans_with_privacy_review = [
        plan["source_id"] for plan in manifest["ingestion_plans"]
        if plan["privacy_tier"] and plan["license_review_status"] == "open"
    ]
    open_execution_ids = [
        requirement["id"] for requirement in manifest["execution_requirements"]
        if requirement["status"] == "open"
    ]
    planned_not_fetched_ids = [
        plan["source_id"] for plan in manifest["ingestion_plans"]
        if plan["status"] == "planned_not_fetched"
    ]
    checks = [
        {
            "id": "check-primary-selection-linked",
            "status": "complete" if manifest["input_selection_id"] == selection["id"] else "open",
            "artifact": "evidential-evil-primary-dataset-selection-checks.json",
            "input_selection_id": manifest["input_selection_id"],
        },
        {
            "id": "check-every-selected-source-has-ingestion-plan",
            "status": "complete" if selected_source_ids <= planned_source_ids else "open",
            "selected_source_ids": sorted(selected_source_ids),
            "planned_source_ids": sorted(planned_source_ids),
            "missing_source_ids": sorted(selected_source_ids - planned_source_ids),
        },
        {
            "id": "check-fetch-parse-specs-present",
            "status": "complete" if len(plans_with_fetch_specs) == len(manifest["ingestion_plans"]) else "open",
            "plans_with_fetch_specs": plans_with_fetch_specs,
        },
        {
            "id": "check-storage-policy-present",
            "status": "complete" if all(
                manifest["storage_policy"].get(key)
                for key in ["raw_dataset_root", "derived_table_root", "hash_algorithm", "personal_data_policy"]
            ) else "open",
            "storage_policy": manifest["storage_policy"],
        },
        {
            "id": "check-license-privacy-gates-present",
            "status": "complete" if len(plans_with_privacy_review) == len(manifest["ingestion_plans"]) else "open",
            "plans_with_privacy_review": plans_with_privacy_review,
        },
        {
            "id": "check-license-privacy-review-linked",
            "status": "complete",
            "artifact": "evidential-evil-license-privacy-checks.json",
            "artifact_status": evidential_evil_license_privacy_checks["status"],
            "result": "terms and privacy review is linked before ingestion is executed",
        },
        {
            "id": "check-ingestion-not-executed",
            "status": "contested" if planned_not_fetched_ids else "complete",
            "planned_not_fetched_source_ids": planned_not_fetched_ids,
            "open_execution_requirement_ids": open_execution_ids,
            "result": "ingestion is executable but has not been run",
        },
        {
            "id": "check-ingestion-manifest-not-promoted",
            "status": "contested" if manifest["verdict"] == "contested" else "open",
            "verdict": manifest["verdict"],
            "decision_rule": manifest["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "argument_id": manifest["argument_id"],
        "target_premise_id": manifest["target_premise_id"],
        "target_concept_id": manifest["target_concept_id"],
        "scope": "evidential_evil_dataset_ingestion_manifest_not_executed_ingestion",
        "checks": checks,
        "remaining_risks": [
            "datasets are not downloaded, hashed, or parsed",
            "license and privacy gates are defined but open",
            "derived evidence tables do not exist yet",
        ],
    }


def _build_evidential_evil_primary_dataset_selection_checks(
    evidential_evil_dataset_ingestion_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    selection = EVIDENTIAL_EVIL_PRIMARY_DATASET_SELECTION
    expansion = EVIDENTIAL_EVIL_EMPIRICAL_EXPANSION_LEDGER
    evidential_evil_dataset_ingestion_checks = (
        evidential_evil_dataset_ingestion_checks or _build_evidential_evil_dataset_ingestion_checks()
    )
    source_ids = {source.id for source in SOURCES}
    selected_source_ids = {
        source_id
        for item in selection["dataset_selections"]
        for source_id in item["selected_source_ids"]
    }
    unknown_source_ids = selected_source_ids - source_ids
    record_class_ids = {item["id"] for item in expansion["empirical_record_classes"]}
    selected_record_class_ids = {item["record_class_id"] for item in selection["dataset_selections"]}
    required_dataset_ids = {
        requirement
        for item in expansion["empirical_record_classes"]
        for requirement in item["dataset_requirements"]
    }
    covered_dataset_ids = {
        requirement
        for item in selection["dataset_selections"]
        for requirement in item["covers_dataset_requirements"]
    }
    selections_with_limits = [
        item["record_class_id"] for item in selection["dataset_selections"]
        if item["limits"]
    ]
    open_requirements = [
        requirement["id"] for requirement in selection["selection_requirements"]
        if requirement["status"] == "open"
    ]
    checks = [
        {
            "id": "check-empirical-expansion-linked",
            "status": "complete" if selection["input_empirical_expansion_id"] == expansion["id"] else "open",
            "artifact": "evidential-evil-empirical-expansion-checks.json",
            "input_empirical_expansion_id": selection["input_empirical_expansion_id"],
        },
        {
            "id": "check-selected-sources-known",
            "status": "complete" if not unknown_source_ids else "open",
            "selected_source_ids": sorted(selected_source_ids),
            "unknown_source_ids": sorted(unknown_source_ids),
            "retrieved_at": selection["retrieved_at"],
        },
        {
            "id": "check-every-record-class-has-source",
            "status": "complete" if record_class_ids <= selected_record_class_ids else "open",
            "record_class_ids": sorted(record_class_ids),
            "selected_record_class_ids": sorted(selected_record_class_ids),
            "missing_record_class_ids": sorted(record_class_ids - selected_record_class_ids),
        },
        {
            "id": "check-dataset-requirements-covered",
            "status": "complete" if required_dataset_ids <= covered_dataset_ids else "open",
            "required_dataset_ids": sorted(required_dataset_ids),
            "covered_dataset_ids": sorted(covered_dataset_ids),
            "missing_dataset_ids": sorted(required_dataset_ids - covered_dataset_ids),
        },
        {
            "id": "check-coverage-limits-recorded",
            "status": "complete" if len(selections_with_limits) == len(selection["dataset_selections"]) else "open",
            "selections_with_limits": selections_with_limits,
        },
        {
            "id": "check-ingestion-manifest-linked",
            "status": "complete",
            "artifact": "evidential-evil-dataset-ingestion-checks.json",
            "artifact_status": evidential_evil_dataset_ingestion_checks["status"],
            "result": "fetch, hash, parse, and privacy gates are manifest before ingestion is promoted",
        },
        {
            "id": "check-license-review-still-open",
            "status": "contested" if "license-and-privacy-review" in open_requirements else "complete",
            "open_requirement_ids": open_requirements,
            "result": "dataset sources are selected and manifest exists, but license and privacy review remain open",
        },
        {
            "id": "check-selection-not-promoted",
            "status": "contested" if selection["verdict"] == "contested" else "open",
            "verdict": selection["verdict"],
            "decision_rule": selection["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "argument_id": selection["argument_id"],
        "target_premise_id": selection["target_premise_id"],
        "target_concept_id": selection["target_concept_id"],
        "scope": "evidential_evil_primary_dataset_selection_not_ingestion",
        "checks": checks,
        "remaining_risks": [
            "selected datasets are not fetched or hashed",
            "licenses and privacy constraints are not reviewed",
            "some dataset requirements may need supplemental sources",
        ],
    }


def _build_evidential_evil_empirical_expansion_checks(
    evidential_evil_primary_dataset_selection_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ledger = EVIDENTIAL_EVIL_EMPIRICAL_EXPANSION_LEDGER
    records = EVIDENTIAL_EVIL_REVIEWED_CASE_RECORDS
    evidential_evil_primary_dataset_selection_checks = (
        evidential_evil_primary_dataset_selection_checks
        or _build_evidential_evil_primary_dataset_selection_checks()
    )
    case_family_ids = {
        record["case_family_id"] for record in records["records"]
    }
    expanded_case_family_ids = {
        case_family_id
        for record_class in ledger["empirical_record_classes"]
        for case_family_id in record_class["case_family_ids"]
    }
    dimension_ids = {
        dimension["id"] for dimension in EVIDENTIAL_EVIL_PROBABILITY_AUDIT["evidence_dimensions"]
    }
    expanded_dimension_ids = {
        dimension_id
        for record_class in ledger["empirical_record_classes"]
        for dimension_id in record_class["dimension_ids"]
    }
    dataset_requirement_ids = {
        requirement
        for record_class in ledger["empirical_record_classes"]
        for requirement in record_class["dataset_requirements"]
    }
    open_ingestion_ids = [
        requirement["id"] for requirement in ledger["ingestion_requirements"]
        if requirement["status"] == "open"
    ]
    not_ingested_ids = [
        record_class["id"] for record_class in ledger["empirical_record_classes"]
        if record_class["status"] == "needed_not_ingested"
    ]
    checks = [
        {
            "id": "check-reviewed-records-linked",
            "status": "complete" if ledger["input_reviewed_records_id"] == records["id"] else "open",
            "artifact": "evidential-evil-reviewed-case-records-checks.json",
            "input_reviewed_records_id": ledger["input_reviewed_records_id"],
        },
        {
            "id": "check-every-case-family-has-empirical-class",
            "status": "complete" if case_family_ids <= expanded_case_family_ids else "open",
            "case_family_ids": sorted(case_family_ids),
            "expanded_case_family_ids": sorted(expanded_case_family_ids),
            "missing_case_family_ids": sorted(case_family_ids - expanded_case_family_ids),
        },
        {
            "id": "check-every-dimension-has-empirical-class",
            "status": "complete" if dimension_ids <= expanded_dimension_ids else "open",
            "dimension_ids": sorted(dimension_ids),
            "expanded_dimension_ids": sorted(expanded_dimension_ids),
            "missing_dimension_ids": sorted(dimension_ids - expanded_dimension_ids),
        },
        {
            "id": "check-dataset-requirements-present",
            "status": "complete" if len(dataset_requirement_ids) >= 10 else "open",
            "dataset_requirement_ids": sorted(dataset_requirement_ids),
        },
        {
            "id": "check-ingestion-requirements-present",
            "status": "complete" if len(ledger["ingestion_requirements"]) >= 4 else "open",
            "ingestion_requirement_ids": [item["id"] for item in ledger["ingestion_requirements"]],
        },
        {
            "id": "check-primary-dataset-selection-linked",
            "status": "complete",
            "artifact": "evidential-evil-primary-dataset-selection-checks.json",
            "artifact_status": evidential_evil_primary_dataset_selection_checks["status"],
            "result": "official and peer-reviewed dataset candidates are selected before ingestion",
        },
        {
            "id": "check-primary-data-not-ingested",
            "status": "contested" if not_ingested_ids else "complete",
            "not_ingested_record_class_ids": not_ingested_ids,
            "open_ingestion_requirement_ids": open_ingestion_ids,
            "result": "empirical classes are defined but primary datasets are not ingested",
        },
        {
            "id": "check-empirical-expansion-not-promoted",
            "status": "contested" if ledger["verdict"] == "contested" else "open",
            "verdict": ledger["verdict"],
            "decision_rule": ledger["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "argument_id": ledger["argument_id"],
        "target_premise_id": ledger["target_premise_id"],
        "target_concept_id": ledger["target_concept_id"],
        "scope": "evidential_evil_empirical_expansion_scaffold_not_ingested_dataset",
        "checks": checks,
        "remaining_risks": [
            "primary datasets have not been selected or ingested",
            "severity bands and counts are still uncalibrated",
            "cross-cultural sampling remains a requirement rather than completed data",
        ],
    }


def _build_evidential_evil_reviewed_case_record_checks(
    evidential_evil_empirical_expansion_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    records = EVIDENTIAL_EVIL_REVIEWED_CASE_RECORDS
    corpus = EVIDENTIAL_EVIL_CASE_CORPUS
    evidential_evil_empirical_expansion_checks = (
        evidential_evil_empirical_expansion_checks
        or _build_evidential_evil_empirical_expansion_checks()
    )
    source_ids = {source.id for source in SOURCES}
    case_family_ids = {case["id"] for case in corpus["case_families"]}
    record_case_family_ids = {record["case_family_id"] for record in records["records"]}
    record_source_ids = {
        source_id
        for record in records["records"]
        for source_id in record["source_ids"]
    }
    unknown_source_ids = record_source_ids - source_ids
    sourced_record_ids = [
        record["id"] for record in records["records"]
        if record["source_ids"] and record["review_status"] == "source_backed"
    ]
    mapped_dimension_record_ids = [
        record["id"] for record in records["records"]
        if record["dimension_ids"] and record["cluster_ids"]
    ]
    open_requirements = [
        requirement["id"] for requirement in records["review_requirements"]
        if requirement["status"] == "open"
    ]
    checks = [
        {
            "id": "check-case-corpus-linked",
            "status": "complete" if records["input_case_corpus_id"] == corpus["id"] else "open",
            "artifact": "evidential-evil-case-corpus-checks.json",
            "input_case_corpus_id": records["input_case_corpus_id"],
        },
        {
            "id": "check-every-case-family-has-record",
            "status": "complete" if case_family_ids <= record_case_family_ids else "open",
            "case_family_ids": sorted(case_family_ids),
            "record_case_family_ids": sorted(record_case_family_ids),
            "missing_case_family_ids": sorted(case_family_ids - record_case_family_ids),
        },
        {
            "id": "check-record-sources-known",
            "status": "complete" if not unknown_source_ids else "open",
            "source_ids": sorted(record_source_ids),
            "unknown_source_ids": sorted(unknown_source_ids),
        },
        {
            "id": "check-records-source-backed",
            "status": "complete" if len(sourced_record_ids) == len(records["records"]) else "open",
            "source_backed_record_ids": sourced_record_ids,
        },
        {
            "id": "check-record-mapping-preserved",
            "status": "complete" if len(mapped_dimension_record_ids) == len(records["records"]) else "open",
            "mapped_record_ids": mapped_dimension_record_ids,
        },
        {
            "id": "check-empirical-expansion-linked",
            "status": "complete",
            "artifact": "evidential-evil-empirical-expansion-checks.json",
            "artifact_status": evidential_evil_empirical_expansion_checks["status"],
            "result": "empirical expansion requirements are represented before reviewed records are promoted",
        },
        {
            "id": "check-severity-calibration-open",
            "status": "contested" if "case-severity-calibration" in open_requirements else "complete",
            "open_requirement_ids": open_requirements,
            "result": "empirical expansion is scaffolded but severity calibration remains open",
        },
        {
            "id": "check-reviewed-records-not-promoted",
            "status": "contested" if records["verdict"] == "contested" else "open",
            "verdict": records["verdict"],
            "decision_rule": records["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "argument_id": records["argument_id"],
        "target_premise_id": records["target_premise_id"],
        "target_concept_id": records["target_concept_id"],
        "scope": "source_backed_evidential_evil_case_records_not_empirical_database",
        "checks": checks,
        "remaining_risks": [
            "records rely on philosophical source coverage rather than primary empirical datasets",
            "severity bands are not calibrated with counts",
            "cross-cultural and non-Western case expansion remains incomplete",
        ],
    }


def _build_evidential_evil_case_corpus_checks(
    evidential_evil_reviewed_case_record_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    corpus = EVIDENTIAL_EVIL_CASE_CORPUS
    calibration = EVIDENTIAL_EVIL_CALIBRATION_LEDGER
    evidential_evil_reviewed_case_record_checks = (
        evidential_evil_reviewed_case_record_checks or _build_evidential_evil_reviewed_case_record_checks()
    )
    expected_dimension_ids = {
        dimension["id"] for dimension in EVIDENTIAL_EVIL_PROBABILITY_AUDIT["evidence_dimensions"]
    }
    expected_cluster_ids = {
        cluster["id"] for cluster in EVIDENTIAL_EVIL_DEPENDENCE_MODEL["dependence_clusters"]
    }
    mapped_dimension_ids = {
        dimension_id
        for case in corpus["case_families"]
        for dimension_id in case["dimension_ids"]
    }
    mapped_cluster_ids = {
        cluster_id
        for case in corpus["case_families"]
        for cluster_id in case["cluster_ids"]
    }
    perspective_tags = {
        tag
        for case in corpus["case_families"]
        for tag in case["perspective_tags"]
    }
    open_expectations = [
        expectation["id"] for expectation in corpus["coverage_expectations"]
        if expectation["status"] == "open"
    ]
    checks = [
        {
            "id": "check-calibration-ledger-linked",
            "status": "complete" if corpus["input_calibration_id"] == calibration["id"] else "open",
            "artifact": "evidential-evil-calibration-checks.json",
            "input_calibration_id": corpus["input_calibration_id"],
        },
        {
            "id": "check-case-families-present",
            "status": "complete" if len(corpus["case_families"]) >= 6 else "open",
            "case_family_ids": [case["id"] for case in corpus["case_families"]],
        },
        {
            "id": "check-dimension-coverage",
            "status": "complete" if expected_dimension_ids <= mapped_dimension_ids else "open",
            "dimension_ids": sorted(expected_dimension_ids),
            "mapped_dimension_ids": sorted(mapped_dimension_ids),
            "missing_dimension_ids": sorted(expected_dimension_ids - mapped_dimension_ids),
        },
        {
            "id": "check-cluster-coverage",
            "status": "complete" if expected_cluster_ids <= mapped_cluster_ids else "open",
            "cluster_ids": sorted(expected_cluster_ids),
            "mapped_cluster_ids": sorted(mapped_cluster_ids),
            "missing_cluster_ids": sorted(expected_cluster_ids - mapped_cluster_ids),
        },
        {
            "id": "check-perspective-diversity",
            "status": "complete" if {
                "skeptical_theism_response",
                "non_theistic_indifference",
                "cross_tradition_pressure",
            } <= perspective_tags else "open",
            "perspective_tags": sorted(perspective_tags),
        },
        {
            "id": "check-reviewed-case-records-linked",
            "status": "complete",
            "artifact": "evidential-evil-reviewed-case-records-checks.json",
            "artifact_status": evidential_evil_reviewed_case_record_checks["status"],
            "result": "source-backed case records are linked before case corpus is treated as reviewed",
        },
        {
            "id": "check-exhaustive-case-database-open",
            "status": "contested" if "exhaustive-case-database" in open_expectations else "complete",
            "open_expectation_ids": open_expectations,
            "result": "case records exist but are not an exhaustive reviewed database",
        },
        {
            "id": "check-case-corpus-not-promoted",
            "status": "contested" if corpus["verdict"] == "contested" else "open",
            "verdict": corpus["verdict"],
            "decision_rule": corpus["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "argument_id": corpus["argument_id"],
        "target_premise_id": corpus["target_premise_id"],
        "target_concept_id": corpus["target_concept_id"],
        "scope": "evidential_evil_case_corpus_candidate_mapping_not_reviewed_database",
        "checks": checks,
        "remaining_risks": [
            "case families are representative rather than reviewed individual records",
            "case severity and mapping weights are not independently cited",
            "cross-tradition weighting remains incomplete",
        ],
    }


def _build_evidential_evil_calibration_checks(
    evidential_evil_case_corpus_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ledger = EVIDENTIAL_EVIL_CALIBRATION_LEDGER
    model = EVIDENTIAL_EVIL_DEPENDENCE_MODEL
    evidential_evil_case_corpus_checks = (
        evidential_evil_case_corpus_checks or _build_evidential_evil_case_corpus_checks()
    )
    cluster_ids = {cluster["id"] for cluster in model["dependence_clusters"]}
    weighted_cluster_ids = {item["cluster_id"] for item in ledger["cluster_weight_intervals"]}
    strength_cluster_ids = {item["cluster_id"] for item in ledger["dependence_strength_intervals"]}
    scenario_ids = {scenario["id"] for scenario in model["sensitivity_scenarios"]}
    profile_scenario_ids = {profile["scenario_id"] for profile in ledger["scenario_weight_profiles"]}
    interval_items = ledger["cluster_weight_intervals"] + ledger["dependence_strength_intervals"]
    invalid_intervals = [
        item for item in interval_items
        if not (0 <= item["lower"] <= item["upper"] <= 1)
    ]
    open_requirements = [
        requirement["id"] for requirement in ledger["calibration_requirements"]
        if requirement["status"] == "open"
    ]
    checks = [
        {
            "id": "check-dependence-model-linked",
            "status": "complete" if ledger["input_model_id"] == model["id"] else "open",
            "artifact": "evidential-evil-dependence-checks.json",
            "input_model_id": ledger["input_model_id"],
        },
        {
            "id": "check-cluster-weights-present",
            "status": "complete" if cluster_ids <= weighted_cluster_ids else "open",
            "cluster_ids": sorted(cluster_ids),
            "weighted_cluster_ids": sorted(weighted_cluster_ids),
            "missing_cluster_ids": sorted(cluster_ids - weighted_cluster_ids),
        },
        {
            "id": "check-dependence-strengths-present",
            "status": "complete" if cluster_ids <= strength_cluster_ids else "open",
            "cluster_ids": sorted(cluster_ids),
            "strength_cluster_ids": sorted(strength_cluster_ids),
            "missing_cluster_ids": sorted(cluster_ids - strength_cluster_ids),
        },
        {
            "id": "check-scenario-weight-profiles-present",
            "status": "complete" if scenario_ids <= profile_scenario_ids else "open",
            "scenario_ids": sorted(scenario_ids),
            "profile_scenario_ids": sorted(profile_scenario_ids),
            "missing_scenario_ids": sorted(scenario_ids - profile_scenario_ids),
        },
        {
            "id": "check-calibration-intervals-in-unit-range",
            "status": "complete" if not invalid_intervals else "open",
            "invalid_interval_count": len(invalid_intervals),
        },
        {
            "id": "check-calibration-requirements-present",
            "status": "complete" if len(ledger["calibration_requirements"]) >= 4 else "open",
            "requirement_ids": [requirement["id"] for requirement in ledger["calibration_requirements"]],
        },
        {
            "id": "check-case-corpus-linked",
            "status": "complete",
            "artifact": "evidential-evil-case-corpus-checks.json",
            "artifact_status": evidential_evil_case_corpus_checks["status"],
            "requirement_id": "case-corpus-calibration",
            "result": "case corpus mapping is linked before cluster weights are treated as calibrated",
        },
        {
            "id": "check-calibration-requirements-open",
            "status": "contested" if open_requirements else "complete",
            "open_requirement_ids": open_requirements,
            "result": "candidate weights are explicit but not independently calibrated",
        },
        {
            "id": "check-calibration-not-promoted",
            "status": "contested" if ledger["verdict"] == "contested" else "open",
            "verdict": ledger["verdict"],
            "decision_rule": ledger["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "argument_id": ledger["argument_id"],
        "target_premise_id": ledger["target_premise_id"],
        "target_concept_id": ledger["target_concept_id"],
        "scope": "candidate_evidential_evil_calibration_not_independent_posterior",
        "checks": checks,
        "remaining_risks": [
            "cluster weights are candidate ranges only",
            "dependence strengths lack a reviewed case corpus",
            "posterior sensitivity has not been executed from calibrated inputs",
        ],
    }


def _build_evidential_evil_dependence_checks(
    evidential_evil_calibration_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    model = EVIDENTIAL_EVIL_DEPENDENCE_MODEL
    ledger = EVIDENTIAL_EVIL_LIKELIHOOD_LEDGER
    evidential_evil_calibration_checks = (
        evidential_evil_calibration_checks or _build_evidential_evil_calibration_checks()
    )
    audit_dimension_ids = {
        dimension["id"] for dimension in EVIDENTIAL_EVIL_PROBABILITY_AUDIT["evidence_dimensions"]
    }
    clustered_dimension_ids = {
        dimension_id
        for cluster in model["dependence_clusters"]
        for dimension_id in cluster["dimension_ids"]
    }
    aggregation_profile_ids = {profile["id"] for profile in model["aggregation_profiles"]}
    active_guardrail_ids = {
        guardrail["id"] for guardrail in model["guardrails"]
        if guardrail["status"] == "active"
    }
    contested_scenario_ids = [
        scenario["id"] for scenario in model["sensitivity_scenarios"]
        if scenario["status"] == "contested"
    ]
    checks = [
        {
            "id": "check-likelihood-ledger-linked",
            "status": "complete" if model["input_ledger_id"] == ledger["id"] else "open",
            "artifact": "evidential-evil-likelihood-checks.json",
            "input_ledger_id": model["input_ledger_id"],
        },
        {
            "id": "check-all-dimensions-clustered",
            "status": "complete" if audit_dimension_ids <= clustered_dimension_ids else "open",
            "dimension_ids": sorted(audit_dimension_ids),
            "clustered_dimension_ids": sorted(clustered_dimension_ids),
            "missing_dimension_ids": sorted(audit_dimension_ids - clustered_dimension_ids),
        },
        {
            "id": "check-aggregation-profiles-present",
            "status": "complete" if {
                "naive_independent_product",
                "clustered_partial_pooling",
                "max_pressure_dimension",
                "skeptical_damped_profile",
            } <= aggregation_profile_ids else "open",
            "aggregation_profile_ids": sorted(aggregation_profile_ids),
        },
        {
            "id": "check-naive-independence-rejected",
            "status": "complete" if any(
                profile["id"] == "naive_independent_product"
                and profile["status"] == "rejected_for_now"
                for profile in model["aggregation_profiles"]
            ) else "open",
            "result": "known dependence blocks naive multiplication",
        },
        {
            "id": "check-sensitivity-scenarios-present",
            "status": "complete" if len(model["sensitivity_scenarios"]) >= 3 else "open",
            "scenario_ids": [scenario["id"] for scenario in model["sensitivity_scenarios"]],
        },
        {
            "id": "check-guardrails-active",
            "status": "complete" if {
                "no-naive-independent-multiplication",
                "no-skeptical-damping-without-cost",
                "no-proof-from-sensitivity-only",
            } <= active_guardrail_ids else "open",
            "active_guardrail_ids": sorted(active_guardrail_ids),
        },
        {
            "id": "check-calibration-ledger-linked",
            "status": "complete",
            "artifact": "evidential-evil-calibration-checks.json",
            "artifact_status": evidential_evil_calibration_checks["status"],
            "result": "cluster weights and dependence strengths are explicit before aggregation",
        },
        {
            "id": "check-scenarios-remain-contested",
            "status": "contested" if contested_scenario_ids else "complete",
            "contested_scenario_ids": contested_scenario_ids,
            "result": "sensitivity analysis maps the pressure but does not close it",
        },
        {
            "id": "check-dependence-model-not-promoted",
            "status": "contested" if model["verdict"] == "contested" else "open",
            "verdict": model["verdict"],
            "decision_rule": model["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "argument_id": model["argument_id"],
        "target_premise_id": model["target_premise_id"],
        "target_concept_id": model["target_concept_id"],
        "scope": "evidential_evil_dependence_and_sensitivity_model_not_final_aggregation",
        "checks": checks,
        "remaining_risks": [
            "cluster weights are explicit but not independently justified",
            "dependence strengths are interval-modeled but not calibrated by a reviewed corpus",
            "sensitivity scenarios remain contested and cannot prove the target premise",
        ],
    }


def _build_evidential_evil_likelihood_checks(
    evidential_evil_dependence_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ledger = EVIDENTIAL_EVIL_LIKELIHOOD_LEDGER
    audit = EVIDENTIAL_EVIL_PROBABILITY_AUDIT
    evidential_evil_dependence_checks = (
        evidential_evil_dependence_checks or _build_evidential_evil_dependence_checks()
    )
    hypothesis_ids = {hypothesis["id"] for hypothesis in audit["hypotheses"]}
    evidence_dimension_ids = {dimension["id"] for dimension in audit["evidence_dimensions"]}
    prior_hypothesis_ids = {item["hypothesis_id"] for item in ledger["prior_intervals"]}
    likelihood_pairs = {
        (item["evidence_dimension_id"], item["hypothesis_id"])
        for item in ledger["likelihood_intervals"]
    }
    expected_pairs = {
        (dimension_id, hypothesis_id)
        for dimension_id in evidence_dimension_ids
        for hypothesis_id in hypothesis_ids
    }
    invalid_intervals = [
        item for item in ledger["prior_intervals"] + ledger["likelihood_intervals"]
        if not (0 <= item["lower"] <= item["upper"] <= 1)
    ]
    wide_intervals = [
        item for item in ledger["likelihood_intervals"]
        if item["upper"] - item["lower"] >= 0.40
    ]
    rival_pairs = [
        item for item in ledger["likelihood_intervals"]
        if item["hypothesis_id"] == "non_theistic_indifference"
    ]
    checks = [
        {
            "id": "check-probability-audit-linked",
            "status": "complete" if ledger["input_audit_id"] == audit["id"] else "open",
            "artifact": "evidential-evil-probability-checks.json",
            "input_audit_id": ledger["input_audit_id"],
        },
        {
            "id": "check-prior-intervals-declared",
            "status": "complete" if hypothesis_ids <= prior_hypothesis_ids else "open",
            "hypothesis_ids": sorted(hypothesis_ids),
            "prior_hypothesis_ids": sorted(prior_hypothesis_ids),
            "missing_prior_hypothesis_ids": sorted(hypothesis_ids - prior_hypothesis_ids),
        },
        {
            "id": "check-likelihood-grid-complete",
            "status": "complete" if expected_pairs <= likelihood_pairs else "open",
            "expected_pair_count": len(expected_pairs),
            "actual_pair_count": len(likelihood_pairs),
            "missing_pairs": sorted([list(pair) for pair in expected_pairs - likelihood_pairs]),
        },
        {
            "id": "check-intervals-in-unit-range",
            "status": "complete" if not invalid_intervals else "open",
            "invalid_interval_count": len(invalid_intervals),
        },
        {
            "id": "check-rival-likelihoods-compared",
            "status": "complete" if len(rival_pairs) == len(evidence_dimension_ids) else "open",
            "rival_hypothesis_id": "non_theistic_indifference",
            "rival_pair_count": len(rival_pairs),
        },
        {
            "id": "check-response-costs-declared",
            "status": "complete" if len(ledger["response_costs"]) >= 3 else "open",
            "response_model_ids": [item["response_model_id"] for item in ledger["response_costs"]],
        },
        {
            "id": "check-dependence-model-linked",
            "status": "complete",
            "artifact": "evidential-evil-dependence-checks.json",
            "artifact_status": evidential_evil_dependence_checks["status"],
            "result": "dependence and sensitivity model is linked before likelihood intervals are aggregated",
        },
        {
            "id": "check-wide-intervals-retained",
            "status": "contested" if wide_intervals else "complete",
            "wide_interval_count": len(wide_intervals),
            "result": "candidate likelihoods are too wide to settle evidential evil",
        },
        {
            "id": "check-aggregation-not-final",
            "status": "contested" if ledger["aggregation_rule"]["status"] == "contested" else "open",
            "aggregation_rule_id": ledger["aggregation_rule"]["id"],
            "decision_rule": ledger["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "argument_id": ledger["argument_id"],
        "target_premise_id": ledger["target_premise_id"],
        "target_concept_id": ledger["target_concept_id"],
        "scope": "candidate_evidential_evil_likelihood_intervals_not_final_bayes_update",
        "checks": checks,
        "remaining_risks": [
            "intervals are stipulated for sensitivity rather than empirically calibrated",
            "evidence dimensions may be dependent and cannot be naively multiplied",
            "wide intervals and response costs keep the evidential pressure unresolved",
        ],
    }


def _build_evidential_evil_probability_checks(
    evidential_evil_likelihood_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    audit = EVIDENTIAL_EVIL_PROBABILITY_AUDIT
    evidential_evil_likelihood_checks = (
        evidential_evil_likelihood_checks or _build_evidential_evil_likelihood_checks()
    )
    hypotheses = audit["hypotheses"]
    evidence_dimensions = audit["evidence_dimensions"]
    response_models = audit["candidate_response_models"]
    probability_requirements = audit["probability_requirements"]
    live_objections = [
        objection["id"] for objection in audit["live_objections"]
        if objection["status"] == "live"
    ]
    open_probability_requirements = [
        requirement["id"] for requirement in probability_requirements
        if requirement["status"] == "open"
    ]
    evidence_dimension_ids = {dimension["id"] for dimension in evidence_dimensions}
    required_dimension_ids = {
        "intensity_of_suffering",
        "distribution_of_suffering",
        "apparently_gratuitous_suffering",
        "natural_evil",
        "animal_suffering",
    }
    checks = [
        {
            "id": "check-pressure-input-linked",
            "status": "complete" if audit["target_pressure_test_id"] == "evidential-probability-pressure" else "open",
            "artifact": "evil-hiddenness-moral-pressure-checks.json",
            "target_pressure_test_id": audit["target_pressure_test_id"],
            "result": "probability audit decomposes the open evidential-pressure test",
        },
        {
            "id": "check-hypotheses-present",
            "status": "complete" if len(hypotheses) >= 3 else "open",
            "hypothesis_ids": [hypothesis["id"] for hypothesis in hypotheses],
        },
        {
            "id": "check-evidence-dimensions-present",
            "status": "complete" if required_dimension_ids <= evidence_dimension_ids else "open",
            "evidence_dimension_ids": sorted(evidence_dimension_ids),
            "required_dimension_ids": sorted(required_dimension_ids),
            "missing_dimension_ids": sorted(required_dimension_ids - evidence_dimension_ids),
        },
        {
            "id": "check-response-models-present",
            "status": "complete" if len(response_models) >= 3 else "open",
            "response_model_ids": [model["id"] for model in response_models],
        },
        {
            "id": "check-likelihood-ledger-linked",
            "status": "complete",
            "artifact": "evidential-evil-likelihood-checks.json",
            "artifact_status": evidential_evil_likelihood_checks["status"],
            "result": "candidate interval likelihoods are linked before evidential evil is promoted",
        },
        {
            "id": "check-probability-requirements-candidate-addressed",
            "status": "complete" if not open_probability_requirements else "open",
            "open_probability_requirement_ids": open_probability_requirements,
            "result": "priors, likelihood intervals, response costs, and rival comparison are represented as candidate data",
        },
        {
            "id": "check-likelihoods-not-decisive",
            "status": "contested" if evidential_evil_likelihood_checks["status"] == "contested" else "complete",
            "artifact": "evidential-evil-likelihood-checks.json",
            "result": "candidate interval likelihoods are not strong enough for a proof claim",
        },
        {
            "id": "check-live-objections-retained",
            "status": "contested" if live_objections else "complete",
            "live_objection_ids": live_objections,
            "result": "evidential evil remains live after response models are listed",
        },
        {
            "id": "check-not-promoted-to-theodicy",
            "status": "contested" if audit["verdict"] == "contested" else "open",
            "verdict": audit["verdict"],
            "result": "probability decomposition is not promoted to a successful theodicy",
        },
    ]
    return {
        "status": "contested",
        "argument_id": audit["argument_id"],
        "target_premise_id": audit["target_premise_id"],
        "target_concept_id": audit["target_concept_id"],
        "scope": "evidential_evil_probability_audit_not_theodicy_solution",
        "checks": checks,
        "remaining_risks": [
            "likelihoods and priors are not quantified",
            "skeptical theism may reduce explanatory power",
            "natural evil, animal suffering, and hiddenness remain coupled pressure points",
        ],
    }


def _build_evil_hiddenness_moral_pressure_checks(
    evidential_evil_probability_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    audit = EVIL_HIDDENNESS_MORAL_PRESSURE_AUDIT
    evidential_evil_probability_checks = (
        evidential_evil_probability_checks or _build_evidential_evil_probability_checks()
    )
    pressure_links = audit["pressure_links"]
    tests = audit["response_sufficiency_tests"]
    constraint_ids = {constraint["id"] for constraint in EVIL_HIDDENNESS_CONSTRAINT_MODEL["constraints"]}
    linked_constraint_ids = {link["constraint_id"] for link in pressure_links}
    open_tests = [
        test["id"] for test in tests
        if test["status"] == "open"
    ]
    checks = [
        {
            "id": "check-all-evil-hiddenness-constraints-linked",
            "status": "complete" if constraint_ids <= linked_constraint_ids else "open",
            "constraint_ids": sorted(constraint_ids),
            "linked_constraint_ids": sorted(linked_constraint_ids),
            "missing_constraint_ids": sorted(constraint_ids - linked_constraint_ids),
        },
        {
            "id": "check-candidate-responses-present",
            "status": "complete" if all(link["candidate_response_ids"] for link in pressure_links) else "open",
            "pressure_link_ids": [link["constraint_id"] for link in pressure_links],
        },
        {
            "id": "check-response-sufficiency-tests-present",
            "status": "complete" if len(tests) >= 4 else "open",
            "response_sufficiency_test_ids": [test["id"] for test in tests],
        },
        {
            "id": "check-evidential-evil-probability-audit-linked",
            "status": "complete",
            "artifact": "evidential-evil-probability-checks.json",
            "artifact_status": evidential_evil_probability_checks["status"],
            "pressure_test_id": "evidential-probability-pressure",
            "result": "evidential evil probability pressure is decomposed before moral pressure is promoted",
        },
        {
            "id": "check-substantive-pressure-tests-open",
            "status": "contested" if open_tests else "complete",
            "open_test_ids": open_tests,
            "result": "candidate responses are present but do not establish perfect-goodness grounding",
        },
        {
            "id": "check-not-promoted-to-solution",
            "status": "contested" if audit["verdict"] == "contested" else "open",
            "verdict": audit["verdict"],
        },
    ]
    return {
        "status": "contested",
        "argument_id": audit["argument_id"],
        "target_premise_id": audit["target_premise_id"],
        "target_concept_id": audit["target_concept_id"],
        "scope": "evil_hiddenness_moral_pressure_audit_not_theodicy_solution",
        "checks": checks,
        "remaining_risks": [
            "evidential evil remains probabilistically unresolved",
            "divine hiddenness still pressures perfect personal goodness",
            "skeptical responses may weaken moral reasoning",
        ],
    }


def _build_moral_perfection_grounding_checks(
    evil_hiddenness_moral_pressure_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    audit = MORAL_PERFECTION_GROUNDING_AUDIT
    evil_hiddenness_moral_pressure_checks = (
        evil_hiddenness_moral_pressure_checks or _build_evil_hiddenness_moral_pressure_checks()
    )
    groundings = audit["candidate_groundings"]
    tests = audit["circularity_tests"]
    live_objections = [
        objection["id"] for objection in audit["live_objections"]
        if objection["status"] == "live"
    ]
    open_tests = [
        test["id"] for test in tests
        if test["status"] == "open"
    ]
    candidate_grounding_ids = [
        grounding["id"] for grounding in groundings
        if grounding["status"] == "candidate"
    ]
    checks = [
        {
            "id": "check-candidate-groundings-present",
            "status": "complete" if len(groundings) >= 3 else "open",
            "candidate_grounding_ids": candidate_grounding_ids,
        },
        {
            "id": "check-circularity-tests-present",
            "status": "complete" if len(tests) >= 4 else "open",
            "circularity_test_ids": [test["id"] for test in tests],
        },
        {
            "id": "check-explicit-godlike-definition-avoided",
            "status": "complete" if any(
                test["id"] == "does-not-define-good-as-godlike"
                and test["status"] == "candidate_pass"
                for test in tests
            ) else "open",
            "result": "goodness is not explicitly defined as whatever God has",
        },
        {
            "id": "check-evil-hiddenness-moral-pressure-linked",
            "status": "complete",
            "artifact": "evil-hiddenness-moral-pressure-checks.json",
            "artifact_status": evil_hiddenness_moral_pressure_checks["status"],
            "result": "evil and hiddenness pressure audit is linked before moral perfection grounding is promoted",
        },
        {
            "id": "check-circularity-tests-still-open",
            "status": "contested" if open_tests else "complete",
            "open_test_ids": open_tests,
            "result": "moral perfection grounding is not yet independent of the target proof",
        },
        {
            "id": "check-live-objections-retained",
            "status": "contested" if live_objections else "complete",
            "live_objection_ids": live_objections,
            "result": "moral perfection grounding remains contested",
        },
    ]
    return {
        "status": "contested",
        "argument_id": audit["argument_id"],
        "target_premise_id": audit["target_premise_id"],
        "target_concept_id": audit["target_concept_id"],
        "scope": "moral_perfection_grounding_audit_not_circularity_discharge",
        "checks": checks,
        "remaining_risks": [
            "moral realism may not select classical theism",
            "moral perfection may presuppose agency under proof",
            "evil and hiddenness still pressure perfect goodness",
        ],
    }


def _build_positive_grounding_checks(
    moral_perfection_grounding_checks: dict[str, Any] | None = None,
    evil_hiddenness_moral_pressure_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    audit = POSITIVE_GROUNDING_AUDIT
    evil_hiddenness_moral_pressure_checks = (
        evil_hiddenness_moral_pressure_checks or _build_evil_hiddenness_moral_pressure_checks()
    )
    moral_perfection_grounding_checks = (
        moral_perfection_grounding_checks
        or _build_moral_perfection_grounding_checks(evil_hiddenness_moral_pressure_checks)
    )
    routes = audit["grounding_routes"]
    tests = audit["anti_ad_hoc_tests"]
    live_objections = [
        objection["id"] for objection in audit["live_objections"]
        if objection["status"] == "live"
    ]
    complete_routes = [
        route["id"] for route in routes
        if route["status"] == "complete"
    ]
    open_tests = [
        test["id"] for test in tests
        if test["status"] == "open"
    ]
    checks = [
        {
            "id": "check-grounding-routes-present",
            "status": "complete" if len(routes) >= 3 else "open",
            "grounding_route_ids": [route["id"] for route in routes],
        },
        {
            "id": "check-anti-ad-hoc-tests-present",
            "status": "complete" if len(tests) >= 4 else "open",
            "anti_ad_hoc_test_ids": [test["id"] for test in tests],
        },
        {
            "id": "check-moral-perfection-grounding-audit-linked",
            "status": "complete",
            "artifact": "moral-perfection-grounding-checks.json",
            "artifact_status": moral_perfection_grounding_checks["status"],
            "route_id": "moral-perfection-route",
            "result": "moral perfection grounding audit is linked before promoting positive grounding",
        },
        {
            "id": "check-no-independent-complete-route",
            "status": "contested" if not complete_routes else "complete",
            "complete_route_ids": complete_routes,
            "result": "no positive-property grounding route is independently complete",
        },
        {
            "id": "check-open-anti-ad-hoc-tests-retained",
            "status": "contested" if open_tests else "complete",
            "open_test_ids": open_tests,
            "result": "anti-ad-hoc requirements are not all satisfied",
        },
        {
            "id": "check-live-objections-retained",
            "status": "contested" if live_objections else "complete",
            "live_objection_ids": live_objections,
            "result": "positive-property grounding remains contested",
        },
    ]
    return {
        "status": "contested",
        "argument_id": audit["argument_id"],
        "target_premise_id": audit["target_premise_id"],
        "target_concept_id": audit["target_concept_id"],
        "scope": "positive_property_grounding_audit_not_independent_grounding_proof",
        "checks": checks,
        "remaining_risks": [
            "objective excellence standard remains disputed",
            "moral perfection grounding may be circular",
            "anti-ad-hoc independence is not established",
        ],
    }


def _build_positive_property_filter_checks(
    positive_grounding_checks: dict[str, Any] | None = None,
    moral_perfection_grounding_checks: dict[str, Any] | None = None,
    evil_hiddenness_moral_pressure_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    audit = POSITIVE_PROPERTY_FILTER_AUDIT
    evil_hiddenness_moral_pressure_checks = (
        evil_hiddenness_moral_pressure_checks or _build_evil_hiddenness_moral_pressure_checks()
    )
    moral_perfection_grounding_checks = (
        moral_perfection_grounding_checks
        or _build_moral_perfection_grounding_checks(evil_hiddenness_moral_pressure_checks)
    )
    positive_grounding_checks = (
        positive_grounding_checks
        or _build_positive_grounding_checks(
            moral_perfection_grounding_checks,
            evil_hiddenness_moral_pressure_checks,
        )
    )
    criteria = audit["candidate_criteria"]
    tests = audit["bad_god_tests"]
    live_objections = [
        objection["id"] for objection in audit["live_objections"]
        if objection["status"] == "live"
    ]
    open_criteria = [
        criterion["id"] for criterion in criteria
        if criterion["status"] != "candidate"
    ]
    rejected_tests = [
        test["id"] for test in tests
        if test["status"] in {"candidate_rejected", "conditional_rejection"}
    ]
    checks = [
        {
            "id": "check-positive-criteria-present",
            "status": "complete" if len(criteria) >= 4 else "open",
            "criterion_ids": [criterion["id"] for criterion in criteria],
        },
        {
            "id": "check-bad-god-tests-present",
            "status": "complete" if len(tests) >= 3 else "open",
            "bad_god_test_ids": [test["id"] for test in tests],
        },
        {
            "id": "check-bad-god-candidates-screened",
            "status": "complete" if len(rejected_tests) == len(tests) else "open",
            "screened_test_ids": rejected_tests,
        },
        {
            "id": "check-positive-grounding-audit-linked",
            "status": "complete",
            "artifact": "positive-grounding-checks.json",
            "artifact_status": positive_grounding_checks["status"],
            "result": "positive-property grounding audit is linked before promoting the filter",
        },
        {
            "id": "check-non-arbitrary-grounding-open",
            "status": "contested" if "non-arbitrary-grounding" in open_criteria else "complete",
            "open_criterion_ids": open_criteria,
            "result": "the positive-property predicate lacks independent grounding",
        },
        {
            "id": "check-live-objections-retained",
            "status": "contested" if live_objections else "complete",
            "live_objection_ids": live_objections,
            "result": "bad-god parity is screened but not discharged",
        },
    ]
    return {
        "status": "contested",
        "argument_id": audit["argument_id"],
        "target_premise_id": audit["target_premise_id"],
        "target_concept_id": audit["target_concept_id"],
        "scope": "positive_property_filter_audit_not_uniqueness_proof",
        "checks": checks,
        "remaining_risks": [
            "positive-property grounding remains open",
            "perfect goodness remains pressured by evil and hiddenness",
            "bad-god parody is conditionally screened but not refuted",
        ],
    }


def _build_rival_necessary_parity_checks(
    positive_property_filter_checks: dict[str, Any] | None = None,
    positive_grounding_checks: dict[str, Any] | None = None,
    moral_perfection_grounding_checks: dict[str, Any] | None = None,
    evil_hiddenness_moral_pressure_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    audit = RIVAL_NECESSARY_PARITY_AUDIT
    evil_hiddenness_moral_pressure_checks = (
        evil_hiddenness_moral_pressure_checks or _build_evil_hiddenness_moral_pressure_checks()
    )
    moral_perfection_grounding_checks = (
        moral_perfection_grounding_checks
        or _build_moral_perfection_grounding_checks(evil_hiddenness_moral_pressure_checks)
    )
    positive_grounding_checks = (
        positive_grounding_checks
        or _build_positive_grounding_checks(
            moral_perfection_grounding_checks,
            evil_hiddenness_moral_pressure_checks,
        )
    )
    positive_property_filter_checks = (
        positive_property_filter_checks
        or _build_positive_property_filter_checks(
            positive_grounding_checks,
            moral_perfection_grounding_checks,
            evil_hiddenness_moral_pressure_checks,
        )
    )
    rivals = audit["rival_concepts"]
    filters = audit["uniqueness_filters"]
    live_rival_ids = [
        rival["id"] for rival in rivals
        if rival["status"] in {"live_competitor", "live_parody"}
    ]
    complete_filters = [
        item for item in filters
        if item["status"] == "complete"
    ]
    contested_filters = [
        item["id"] for item in filters
        if item["status"] == "contested"
    ]
    blocked_by_complete_filter = sorted({
        rival_id
        for item in complete_filters
        for rival_id in item["blocks_rival_ids"]
    })
    unresolved_rival_ids = sorted(set(live_rival_ids) - set(blocked_by_complete_filter))
    checks = [
        {
            "id": "check-rival-concepts-present",
            "status": "complete" if len(rivals) >= 3 else "open",
            "rival_concept_ids": [rival["id"] for rival in rivals],
        },
        {
            "id": "check-uniqueness-filters-present",
            "status": "complete" if len(filters) >= 4 else "open",
            "uniqueness_filter_ids": [item["id"] for item in filters],
        },
        {
            "id": "check-every-rival-has-some-filter",
            "status": "complete" if all(
                any(rival["id"] in item["blocks_rival_ids"] for item in filters)
                for rival in rivals
            ) else "open",
            "live_rival_ids": live_rival_ids,
        },
        {
            "id": "check-positive-property-filter-audit-linked",
            "status": "complete",
            "artifact": "positive-property-filter-checks.json",
            "artifact_status": positive_property_filter_checks["status"],
            "filter_id": "positive-property-filter",
            "result": "positive-property filter audit is linked to bad-god parity",
        },
        {
            "id": "check-filters-not-independent-complete",
            "status": "contested" if contested_filters else "complete",
            "contested_filter_ids": contested_filters,
            "result": "all current uniqueness filters remain contested",
        },
        {
            "id": "check-rival-parity-not-discharged",
            "status": "contested" if unresolved_rival_ids else "complete",
            "unresolved_rival_ids": unresolved_rival_ids,
            "decision_rule": audit["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "argument_id": audit["argument_id"],
        "target_premise_id": audit["target_premise_id"],
        "target_concept_id": audit["target_concept_id"],
        "scope": "rival_necessary_concepts_parity_audit_not_uniqueness_proof",
        "checks": checks,
        "remaining_risks": [
            "no uniqueness filter is independently complete",
            "impersonal ultimate and deistic designer competitors remain live",
            "necessary bad-god parody still pressures positive-property assumptions",
        ],
    }


def _build_possible_necessary_existence_checks(
    metaphysical_possibility_checks: dict[str, Any] | None = None,
    modal_validity_checks: dict[str, Any] | None = None,
    modal_consistency_checks: dict[str, Any] | None = None,
    definition_smuggling_checks: dict[str, Any] | None = None,
    rival_necessary_parity_checks: dict[str, Any] | None = None,
    positive_property_filter_checks: dict[str, Any] | None = None,
    positive_grounding_checks: dict[str, Any] | None = None,
    moral_perfection_grounding_checks: dict[str, Any] | None = None,
    evil_hiddenness_moral_pressure_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    bridge = POSSIBLE_NECESSARY_EXISTENCE_BRIDGE
    metaphysical_possibility_checks = (
        metaphysical_possibility_checks or _build_metaphysical_possibility_checks()
    )
    modal_validity_checks = modal_validity_checks or _build_modal_validity_checks()
    modal_consistency_checks = modal_consistency_checks or _build_modal_consistency_checks()
    definition_smuggling_checks = definition_smuggling_checks or _build_definition_smuggling_checks()
    evil_hiddenness_moral_pressure_checks = (
        evil_hiddenness_moral_pressure_checks or _build_evil_hiddenness_moral_pressure_checks()
    )
    moral_perfection_grounding_checks = (
        moral_perfection_grounding_checks
        or _build_moral_perfection_grounding_checks(evil_hiddenness_moral_pressure_checks)
    )
    positive_grounding_checks = (
        positive_grounding_checks
        or _build_positive_grounding_checks(moral_perfection_grounding_checks)
    )
    positive_property_filter_checks = (
        positive_property_filter_checks
        or _build_positive_property_filter_checks(
            positive_grounding_checks,
            moral_perfection_grounding_checks,
            evil_hiddenness_moral_pressure_checks,
        )
    )
    rival_necessary_parity_checks = (
        rival_necessary_parity_checks
        or _build_rival_necessary_parity_checks(
            positive_property_filter_checks,
            positive_grounding_checks,
            moral_perfection_grounding_checks,
        )
    )
    support_routes = bridge["support_routes"]
    defeater_routes = bridge["defeater_routes"]
    live_defeater_ids = [
        route["id"] for route in defeater_routes
        if route["status"] == "live"
    ]
    complete_support_ids = [
        route["id"] for route in support_routes
        if route["status"] == "complete"
    ]
    checks = [
        {
            "id": "check-metaphysical-possibility-input-linked",
            "status": "complete",
            "artifact": "metaphysical-possibility-checks.json",
            "artifact_status": metaphysical_possibility_checks["status"],
            "input_stage_id": bridge["input_stage_id"],
        },
        {
            "id": "check-modal-validity-linked",
            "status": "complete" if modal_validity_checks["status"] == "complete" else "open",
            "artifact": "modal-validity-checks.json",
            "artifact_status": modal_validity_checks["status"],
        },
        {
            "id": "check-modal-consistency-linked",
            "status": "complete" if modal_consistency_checks["status"] == "complete" else "open",
            "artifact": "modal-consistency-checks.json",
            "artifact_status": modal_consistency_checks["status"],
        },
        {
            "id": "check-support-routes-complete",
            "status": "complete" if len(complete_support_ids) == len(support_routes) else "open",
            "complete_support_route_ids": complete_support_ids,
            "support_route_ids": [route["id"] for route in support_routes],
        },
        {
            "id": "check-definition-smuggling-audit-linked",
            "status": "complete",
            "artifact": "definition-smuggling-checks.json",
            "artifact_status": definition_smuggling_checks["status"],
            "result": "definition-smuggling audit is linked before promoting possible necessary existence",
        },
        {
            "id": "check-rival-necessary-parity-audit-linked",
            "status": "complete",
            "artifact": "rival-necessary-parity-checks.json",
            "artifact_status": rival_necessary_parity_checks["status"],
            "result": "rival necessary-concept parity audit is linked before promotion",
        },
        {
            "id": "check-soundness-defeaters-retained",
            "status": "contested" if live_defeater_ids else "complete",
            "live_defeater_ids": live_defeater_ids,
            "result": "validity and consistency do not discharge soundness defeaters",
        },
        {
            "id": "check-bridge-not-promoted",
            "status": "contested" if bridge["verdict"] == "contested" else "open",
            "verdict": bridge["verdict"],
            "decision_rule": bridge["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "argument_id": bridge["argument_id"],
        "target_premise_id": bridge["target_premise_id"],
        "target_concept_id": bridge["target_concept_id"],
        "scope": "metaphysical_possibility_to_possible_necessary_existence_bridge_not_proof",
        "checks": checks,
        "remaining_risks": [
            "the metaphysical possibility input is contested",
            "necessary existence may be definition-smuggling",
            "rival necessary ultimates still create parity pressure",
        ],
    }


def _build_possibility_premise_ladder() -> dict[str, Any]:
    return {
        "status": "contested",
        "ladder": POSSIBILITY_PREMISE_LADDER,
        "warning": (
            "This ladder decomposes the possibility premise into smaller gates. "
            "It does not prove the jump from conceivability to metaphysical "
            "possibility or possible necessary existence."
        ),
    }


def _build_possibility_premise_checks(
    coherent_conceivability_checks: dict[str, Any] | None = None,
    metaphysical_possibility_checks: dict[str, Any] | None = None,
    possible_necessary_existence_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ladder = POSSIBILITY_PREMISE_LADDER
    coherent_conceivability_checks = (
        coherent_conceivability_checks or _build_coherent_conceivability_checks()
    )
    metaphysical_possibility_checks = (
        metaphysical_possibility_checks
        or _build_metaphysical_possibility_checks(coherent_conceivability_checks)
    )
    possible_necessary_existence_checks = (
        possible_necessary_existence_checks
        or _build_possible_necessary_existence_checks(metaphysical_possibility_checks)
    )
    stages = ladder["stages"]
    transitions = ladder["transitions"]
    stage_ids = [stage["id"] for stage in stages]
    transition_pairs = {(transition["from"], transition["to"]) for transition in transitions}
    expected_pairs = set(zip(stage_ids, stage_ids[1:]))
    blocked_stage_ids = [
        stage["id"] for stage in stages
        if stage["status"] != "complete"
    ]
    blocked_transition_ids = [
        transition["id"] for transition in transitions
        if transition["status"] != "complete"
    ]
    checks = [
        {
            "id": "check-ladder-stage-order",
            "status": "complete" if stage_ids == [
                "target-schema-defined",
                "no-direct-schema-contradiction",
                "coherent-conceivability",
                "metaphysical-possibility",
                "possible-necessary-existence",
            ] else "open",
            "stage_ids": stage_ids,
        },
        {
            "id": "check-transition-chain-complete",
            "status": "complete" if expected_pairs <= transition_pairs else "open",
            "expected_pairs": sorted([list(pair) for pair in expected_pairs]),
            "actual_pairs": sorted([list(pair) for pair in transition_pairs]),
        },
        {
            "id": "check-completed-foundation-stages",
            "status": "complete" if stage_ids[:2] == [
                "target-schema-defined",
                "no-direct-schema-contradiction",
            ] and all(stage["status"] == "complete" for stage in stages[:2]) else "open",
            "completed_stage_ids": [stage["id"] for stage in stages if stage["status"] == "complete"],
        },
        {
            "id": "check-coherent-conceivability-model-linked",
            "status": "complete",
            "artifact": "coherent-conceivability-checks.json",
            "artifact_status": coherent_conceivability_checks["status"],
            "stage_id": "coherent-conceivability",
            "result": "candidate repair model is linked to the coherent-conceivability stage",
        },
        {
            "id": "check-metaphysical-possibility-bridge-linked",
            "status": "complete",
            "artifact": "metaphysical-possibility-checks.json",
            "artifact_status": metaphysical_possibility_checks["status"],
            "stage_id": "metaphysical-possibility",
            "transition_id": "conceivability-to-metaphysical-possibility",
            "result": "contested bridge model is linked to the metaphysical-possibility stage",
        },
        {
            "id": "check-possible-necessary-existence-bridge-linked",
            "status": "complete",
            "artifact": "possible-necessary-existence-checks.json",
            "artifact_status": possible_necessary_existence_checks["status"],
            "stage_id": "possible-necessary-existence",
            "transition_id": "metaphysical-possibility-to-necessary-existence",
            "result": "contested bridge model is linked to the possible-necessary-existence stage",
        },
        {
            "id": "check-blocked-bridges-localized",
            "status": "contested" if blocked_stage_ids and blocked_transition_ids else "complete",
            "blocked_stage_ids": blocked_stage_ids,
            "blocked_transition_ids": blocked_transition_ids,
            "result": "the proof frontier is localized to conceivability and modal-possibility bridges",
        },
        {
            "id": "check-ladder-not-promoted-to-proof",
            "status": "contested" if ladder["verdict"] == "contested" else "open",
            "verdict": ladder["verdict"],
            "result": "the ladder records progress but still blocks the possibility premise",
        },
    ]
    return {
        "status": "contested",
        "argument_id": ladder["argument_id"],
        "target_premise_id": ladder["target_premise_id"],
        "target_concept_id": ladder["target_concept_id"],
        "scope": "possibility_premise_stage_decomposition_not_proof",
        "checks": checks,
        "remaining_risks": [
            "coherent conceivability has candidate support but remains contested",
            "the conceivability-to-possibility bridge remains contested",
            "possible necessary existence may still beg the question",
        ],
    }


def _build_ontological_soundness_checks(
    attribute_coherence_checks: dict[str, Any] | None = None,
    coherent_conceivability_checks: dict[str, Any] | None = None,
    metaphysical_possibility_checks: dict[str, Any] | None = None,
    definition_smuggling_checks: dict[str, Any] | None = None,
    evidential_evil_attribution_template_checks: dict[str, Any] | None = None,
    evidential_evil_license_decision_checks: dict[str, Any] | None = None,
    evidential_evil_source_acquisition_hash_runbook_checks: dict[str, Any] | None = None,
    evidential_evil_suppression_report_template_checks: dict[str, Any] | None = None,
    evidential_evil_source_version_hash_preflight_checks: dict[str, Any] | None = None,
    evidential_evil_derived_aggregate_schema_checks: dict[str, Any] | None = None,
    evidential_evil_microdata_minimization_checks: dict[str, Any] | None = None,
    evidential_evil_license_privacy_checks: dict[str, Any] | None = None,
    evidential_evil_dataset_ingestion_checks: dict[str, Any] | None = None,
    evidential_evil_primary_dataset_selection_checks: dict[str, Any] | None = None,
    evidential_evil_empirical_expansion_checks: dict[str, Any] | None = None,
    evidential_evil_reviewed_case_record_checks: dict[str, Any] | None = None,
    evidential_evil_case_corpus_checks: dict[str, Any] | None = None,
    evidential_evil_calibration_checks: dict[str, Any] | None = None,
    evidential_evil_dependence_checks: dict[str, Any] | None = None,
    evidential_evil_likelihood_checks: dict[str, Any] | None = None,
    evidential_evil_probability_checks: dict[str, Any] | None = None,
    evil_hiddenness_moral_pressure_checks: dict[str, Any] | None = None,
    moral_perfection_grounding_checks: dict[str, Any] | None = None,
    positive_grounding_checks: dict[str, Any] | None = None,
    positive_property_filter_checks: dict[str, Any] | None = None,
    rival_necessary_parity_checks: dict[str, Any] | None = None,
    possible_necessary_existence_checks: dict[str, Any] | None = None,
    possibility_premise_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    dossier = ONTOLOGICAL_SOUNDNESS_DOSSIER
    attribute_coherence_checks = attribute_coherence_checks or _build_attribute_coherence_checks()
    coherent_conceivability_checks = (
        coherent_conceivability_checks or _build_coherent_conceivability_checks()
    )
    metaphysical_possibility_checks = (
        metaphysical_possibility_checks
        or _build_metaphysical_possibility_checks(coherent_conceivability_checks)
    )
    definition_smuggling_checks = definition_smuggling_checks or _build_definition_smuggling_checks()
    evidential_evil_attribution_template_checks = (
        evidential_evil_attribution_template_checks or _build_evidential_evil_attribution_template_checks()
    )
    evidential_evil_license_decision_checks = (
        evidential_evil_license_decision_checks
        or _build_evidential_evil_license_decision_checks(evidential_evil_attribution_template_checks)
    )
    evidential_evil_source_acquisition_hash_runbook_checks = (
        evidential_evil_source_acquisition_hash_runbook_checks
        or _build_evidential_evil_source_acquisition_hash_runbook_checks()
    )
    evidential_evil_suppression_report_template_checks = (
        evidential_evil_suppression_report_template_checks
        or _build_evidential_evil_suppression_report_template_checks(
            evidential_evil_source_acquisition_hash_runbook_checks
        )
    )
    evidential_evil_source_version_hash_preflight_checks = (
        evidential_evil_source_version_hash_preflight_checks
        or _build_evidential_evil_source_version_hash_preflight_checks(
            evidential_evil_source_acquisition_hash_runbook_checks
        )
    )
    evidential_evil_derived_aggregate_schema_checks = (
        evidential_evil_derived_aggregate_schema_checks
        or _build_evidential_evil_derived_aggregate_schema_checks(
            evidential_evil_source_version_hash_preflight_checks,
            evidential_evil_suppression_report_template_checks,
        )
    )
    evidential_evil_microdata_minimization_checks = (
        evidential_evil_microdata_minimization_checks
        or _build_evidential_evil_microdata_minimization_checks(
            evidential_evil_license_decision_checks,
            evidential_evil_derived_aggregate_schema_checks,
        )
    )
    evidential_evil_license_privacy_checks = (
        evidential_evil_license_privacy_checks
        or _build_evidential_evil_license_privacy_checks(
            evidential_evil_attribution_template_checks,
            evidential_evil_license_decision_checks,
            evidential_evil_microdata_minimization_checks,
        )
    )
    evidential_evil_dataset_ingestion_checks = (
        evidential_evil_dataset_ingestion_checks
        or _build_evidential_evil_dataset_ingestion_checks(evidential_evil_license_privacy_checks)
    )
    evidential_evil_primary_dataset_selection_checks = (
        evidential_evil_primary_dataset_selection_checks
        or _build_evidential_evil_primary_dataset_selection_checks(evidential_evil_dataset_ingestion_checks)
    )
    evidential_evil_empirical_expansion_checks = (
        evidential_evil_empirical_expansion_checks
        or _build_evidential_evil_empirical_expansion_checks(evidential_evil_primary_dataset_selection_checks)
    )
    evidential_evil_reviewed_case_record_checks = (
        evidential_evil_reviewed_case_record_checks
        or _build_evidential_evil_reviewed_case_record_checks(evidential_evil_empirical_expansion_checks)
    )
    evidential_evil_case_corpus_checks = (
        evidential_evil_case_corpus_checks
        or _build_evidential_evil_case_corpus_checks(evidential_evil_reviewed_case_record_checks)
    )
    evidential_evil_calibration_checks = (
        evidential_evil_calibration_checks
        or _build_evidential_evil_calibration_checks(evidential_evil_case_corpus_checks)
    )
    evidential_evil_dependence_checks = (
        evidential_evil_dependence_checks
        or _build_evidential_evil_dependence_checks(evidential_evil_calibration_checks)
    )
    evidential_evil_likelihood_checks = (
        evidential_evil_likelihood_checks
        or _build_evidential_evil_likelihood_checks(evidential_evil_dependence_checks)
    )
    evidential_evil_probability_checks = (
        evidential_evil_probability_checks
        or _build_evidential_evil_probability_checks(evidential_evil_likelihood_checks)
    )
    evil_hiddenness_moral_pressure_checks = (
        evil_hiddenness_moral_pressure_checks
        or _build_evil_hiddenness_moral_pressure_checks(evidential_evil_probability_checks)
    )
    moral_perfection_grounding_checks = (
        moral_perfection_grounding_checks
        or _build_moral_perfection_grounding_checks(evil_hiddenness_moral_pressure_checks)
    )
    positive_grounding_checks = (
        positive_grounding_checks
        or _build_positive_grounding_checks(moral_perfection_grounding_checks)
    )
    positive_property_filter_checks = (
        positive_property_filter_checks
        or _build_positive_property_filter_checks(
            positive_grounding_checks,
            moral_perfection_grounding_checks,
        )
    )
    rival_necessary_parity_checks = (
        rival_necessary_parity_checks
        or _build_rival_necessary_parity_checks(
            positive_property_filter_checks,
            positive_grounding_checks,
            moral_perfection_grounding_checks,
            evil_hiddenness_moral_pressure_checks,
        )
    )
    possible_necessary_existence_checks = (
        possible_necessary_existence_checks
        or _build_possible_necessary_existence_checks(
            metaphysical_possibility_checks,
            definition_smuggling_checks=definition_smuggling_checks,
            rival_necessary_parity_checks=rival_necessary_parity_checks,
            positive_property_filter_checks=positive_property_filter_checks,
            positive_grounding_checks=positive_grounding_checks,
            moral_perfection_grounding_checks=moral_perfection_grounding_checks,
            evil_hiddenness_moral_pressure_checks=evil_hiddenness_moral_pressure_checks,
        )
    )
    possibility_premise_checks = (
        possibility_premise_checks
        or _build_possibility_premise_checks(
            coherent_conceivability_checks,
            metaphysical_possibility_checks,
            possible_necessary_existence_checks,
        )
    )
    support = dossier["supporting_considerations"]
    critical = dossier["critical_considerations"]
    parody_tests = dossier["parody_tests"]
    unresolved_parodies = [
        test["id"] for test in parody_tests
        if test["result"] == "not_resolved"
    ]
    checks = [
        {
            "id": "check-supporting-considerations-present",
            "status": "complete" if support else "open",
            "supporting_ids": [item["id"] for item in support],
        },
        {
            "id": "check-critical-considerations-present",
            "status": "complete" if len(critical) >= 3 else "open",
            "critical_ids": [item["id"] for item in critical],
        },
        {
            "id": "check-parody-tests-present",
            "status": "complete" if len(parody_tests) >= 3 else "open",
            "parody_test_ids": [item["id"] for item in parody_tests],
        },
        {
            "id": "check-unresolved-parodies-retained",
            "status": "contested" if unresolved_parodies else "complete",
            "unresolved_parody_ids": unresolved_parodies,
            "result": "unresolved parody pressure remains in the dossier",
        },
        {
            "id": "check-soundness-not-promoted",
            "status": "contested" if dossier["verdict"] == "contested" else "open",
            "verdict": dossier["verdict"],
            "result": "possibility premise remains contested and blocks proof claim",
        },
        {
            "id": "check-attribute-coherence-ledger-linked",
            "status": "complete",
            "artifact": "attribute-coherence-checks.json",
            "artifact_status": attribute_coherence_checks["status"],
            "result": "attribute-coherence screening is linked into the soundness gate",
        },
        {
            "id": "check-possibility-premise-ladder-linked",
            "status": "complete",
            "artifact": "possibility-premise-checks.json",
            "artifact_status": possibility_premise_checks["status"],
            "result": "possibility-premise stage decomposition is linked into the soundness gate",
        },
        {
            "id": "check-coherent-conceivability-model-linked",
            "status": "complete",
            "artifact": "coherent-conceivability-checks.json",
            "artifact_status": coherent_conceivability_checks["status"],
            "result": "candidate coherent-conceivability model is linked into the soundness gate",
        },
        {
            "id": "check-metaphysical-possibility-bridge-linked",
            "status": "complete",
            "artifact": "metaphysical-possibility-checks.json",
            "artifact_status": metaphysical_possibility_checks["status"],
            "result": "conceivability-to-metaphysical-possibility bridge is linked into the soundness gate",
        },
        {
            "id": "check-possible-necessary-existence-bridge-linked",
            "status": "complete",
            "artifact": "possible-necessary-existence-checks.json",
            "artifact_status": possible_necessary_existence_checks["status"],
            "result": "possible-necessary-existence bridge is linked into the soundness gate",
        },
        {
            "id": "check-definition-smuggling-audit-linked",
            "status": "complete",
            "artifact": "definition-smuggling-checks.json",
            "artifact_status": definition_smuggling_checks["status"],
            "result": "definition-smuggling audit is linked into the soundness gate",
        },
        {
            "id": "check-rival-necessary-parity-audit-linked",
            "status": "complete",
            "artifact": "rival-necessary-parity-checks.json",
            "artifact_status": rival_necessary_parity_checks["status"],
            "result": "rival necessary-concept parity audit is linked into the soundness gate",
        },
        {
            "id": "check-positive-property-filter-audit-linked",
            "status": "complete",
            "artifact": "positive-property-filter-checks.json",
            "artifact_status": positive_property_filter_checks["status"],
            "result": "positive-property filter audit is linked into the soundness gate",
        },
        {
            "id": "check-positive-grounding-audit-linked",
            "status": "complete",
            "artifact": "positive-grounding-checks.json",
            "artifact_status": positive_grounding_checks["status"],
            "result": "positive-property grounding audit is linked into the soundness gate",
        },
        {
            "id": "check-moral-perfection-grounding-audit-linked",
            "status": "complete",
            "artifact": "moral-perfection-grounding-checks.json",
            "artifact_status": moral_perfection_grounding_checks["status"],
            "result": "moral perfection grounding audit is linked into the soundness gate",
        },
        {
            "id": "check-evil-hiddenness-moral-pressure-audit-linked",
            "status": "complete",
            "artifact": "evil-hiddenness-moral-pressure-checks.json",
            "artifact_status": evil_hiddenness_moral_pressure_checks["status"],
            "result": "evil and hiddenness moral-pressure audit is linked into the soundness gate",
        },
        {
            "id": "check-evidential-evil-probability-audit-linked",
            "status": "complete",
            "artifact": "evidential-evil-probability-checks.json",
            "artifact_status": evidential_evil_probability_checks["status"],
            "result": "evidential evil probability audit is linked into the soundness gate",
        },
        {
            "id": "check-evidential-evil-likelihood-ledger-linked",
            "status": "complete",
            "artifact": "evidential-evil-likelihood-checks.json",
            "artifact_status": evidential_evil_likelihood_checks["status"],
            "result": "candidate evidential evil likelihood ledger is linked into the soundness gate",
        },
        {
            "id": "check-evidential-evil-dependence-model-linked",
            "status": "complete",
            "artifact": "evidential-evil-dependence-checks.json",
            "artifact_status": evidential_evil_dependence_checks["status"],
            "result": "evidential evil dependence and sensitivity model is linked into the soundness gate",
        },
        {
            "id": "check-evidential-evil-calibration-ledger-linked",
            "status": "complete",
            "artifact": "evidential-evil-calibration-checks.json",
            "artifact_status": evidential_evil_calibration_checks["status"],
            "result": "candidate evidential evil calibration ledger is linked into the soundness gate",
        },
        {
            "id": "check-evidential-evil-case-corpus-linked",
            "status": "complete",
            "artifact": "evidential-evil-case-corpus-checks.json",
            "artifact_status": evidential_evil_case_corpus_checks["status"],
            "result": "evidential evil case corpus is linked into the soundness gate",
        },
        {
            "id": "check-evidential-evil-reviewed-case-records-linked",
            "status": "complete",
            "artifact": "evidential-evil-reviewed-case-records-checks.json",
            "artifact_status": evidential_evil_reviewed_case_record_checks["status"],
            "result": "source-backed evidential evil case records are linked into the soundness gate",
        },
        {
            "id": "check-evidential-evil-empirical-expansion-linked",
            "status": "complete",
            "artifact": "evidential-evil-empirical-expansion-checks.json",
            "artifact_status": evidential_evil_empirical_expansion_checks["status"],
            "result": "empirical expansion scaffold is linked into the soundness gate",
        },
        {
            "id": "check-evidential-evil-primary-dataset-selection-linked",
            "status": "complete",
            "artifact": "evidential-evil-primary-dataset-selection-checks.json",
            "artifact_status": evidential_evil_primary_dataset_selection_checks["status"],
            "result": "primary dataset selection is linked into the soundness gate",
        },
        {
            "id": "check-evidential-evil-dataset-ingestion-manifest-linked",
            "status": "complete",
            "artifact": "evidential-evil-dataset-ingestion-checks.json",
            "artifact_status": evidential_evil_dataset_ingestion_checks["status"],
            "result": "dataset ingestion manifest is linked into the soundness gate",
        },
        {
            "id": "check-evidential-evil-attribution-template-linked",
            "status": "complete",
            "artifact": "evidential-evil-attribution-template-checks.json",
            "artifact_status": evidential_evil_attribution_template_checks["status"],
            "result": "dataset attribution template ledger is linked into the soundness gate",
        },
        {
            "id": "check-evidential-evil-license-decision-packet-linked",
            "status": "complete",
            "artifact": "evidential-evil-license-decision-checks.json",
            "artifact_status": evidential_evil_license_decision_checks["status"],
            "result": "candidate dataset license decision packet is linked into the soundness gate",
        },
        {
            "id": "check-evidential-evil-source-acquisition-hash-runbook-linked",
            "status": "complete",
            "artifact": "evidential-evil-source-acquisition-hash-runbook-checks.json",
            "artifact_status": evidential_evil_source_acquisition_hash_runbook_checks["status"],
            "result": "source acquisition and hashing runbook is linked into the soundness gate",
        },
        {
            "id": "check-evidential-evil-suppression-report-template-linked",
            "status": "complete",
            "artifact": "evidential-evil-suppression-report-template-checks.json",
            "artifact_status": evidential_evil_suppression_report_template_checks["status"],
            "result": "suppression report template is linked into the soundness gate",
        },
        {
            "id": "check-evidential-evil-source-version-hash-preflight-linked",
            "status": "complete",
            "artifact": "evidential-evil-source-version-hash-preflight-checks.json",
            "artifact_status": evidential_evil_source_version_hash_preflight_checks["status"],
            "result": "source version and hash preflight is linked into the soundness gate",
        },
        {
            "id": "check-evidential-evil-derived-aggregate-schema-linked",
            "status": "complete",
            "artifact": "evidential-evil-derived-aggregate-schema-checks.json",
            "artifact_status": evidential_evil_derived_aggregate_schema_checks["status"],
            "result": "derived aggregate schema is linked into the soundness gate",
        },
        {
            "id": "check-evidential-evil-microdata-minimization-linked",
            "status": "complete",
            "artifact": "evidential-evil-microdata-minimization-checks.json",
            "artifact_status": evidential_evil_microdata_minimization_checks["status"],
            "result": "microdata minimization policy is linked into the soundness gate",
        },
        {
            "id": "check-evidential-evil-license-privacy-review-linked",
            "status": "complete",
            "artifact": "evidential-evil-license-privacy-checks.json",
            "artifact_status": evidential_evil_license_privacy_checks["status"],
            "result": "license and privacy review gate is linked into the soundness gate",
        },
    ]
    return {
        "status": "contested",
        "argument_id": dossier["argument_id"],
        "target_premise_id": dossier["target_premise_id"],
        "scope": "possibility_premise_dossier_not_soundness_proof",
        "checks": checks,
        "related_artifacts": [
            "attribute-coherence-ledger.json",
            "attribute-coherence-checks.json",
            "coherent-conceivability-model.json",
            "coherent-conceivability-checks.json",
            "metaphysical-possibility-bridge.json",
            "metaphysical-possibility-checks.json",
            "definition-smuggling-audit.json",
            "definition-smuggling-checks.json",
            "evidential-evil-attribution-template-ledger.json",
            "evidential-evil-attribution-template-checks.json",
            "evidential-evil-license-decision-packet.json",
            "evidential-evil-license-decision-checks.json",
            "evidential-evil-source-acquisition-hash-runbook.json",
            "evidential-evil-source-acquisition-hash-runbook-checks.json",
            "evidential-evil-suppression-report-template.json",
            "evidential-evil-suppression-report-template-checks.json",
            "evidential-evil-source-version-hash-preflight.json",
            "evidential-evil-source-version-hash-preflight-checks.json",
            "evidential-evil-derived-aggregate-schema.json",
            "evidential-evil-derived-aggregate-schema-checks.json",
            "evidential-evil-microdata-minimization-policy.json",
            "evidential-evil-microdata-minimization-checks.json",
            "evidential-evil-license-privacy-review.json",
            "evidential-evil-license-privacy-checks.json",
            "evidential-evil-dataset-ingestion-manifest.json",
            "evidential-evil-dataset-ingestion-checks.json",
            "evidential-evil-primary-dataset-selection.json",
            "evidential-evil-primary-dataset-selection-checks.json",
            "evidential-evil-empirical-expansion-ledger.json",
            "evidential-evil-empirical-expansion-checks.json",
            "evidential-evil-reviewed-case-records.json",
            "evidential-evil-reviewed-case-records-checks.json",
            "evidential-evil-case-corpus.json",
            "evidential-evil-case-corpus-checks.json",
            "evidential-evil-calibration-ledger.json",
            "evidential-evil-calibration-checks.json",
            "evidential-evil-dependence-model.json",
            "evidential-evil-dependence-checks.json",
            "evidential-evil-likelihood-ledger.json",
            "evidential-evil-likelihood-checks.json",
            "evidential-evil-probability-audit.json",
            "evidential-evil-probability-checks.json",
            "evil-hiddenness-moral-pressure-audit.json",
            "evil-hiddenness-moral-pressure-checks.json",
            "moral-perfection-grounding-audit.json",
            "moral-perfection-grounding-checks.json",
            "positive-grounding-audit.json",
            "positive-grounding-checks.json",
            "positive-property-filter-audit.json",
            "positive-property-filter-checks.json",
            "rival-necessary-parity-audit.json",
            "rival-necessary-parity-checks.json",
            "possible-necessary-existence-bridge.json",
            "possible-necessary-existence-checks.json",
            "possibility-premise-ladder.json",
            "possibility-premise-checks.json",
        ],
        "remaining_risks": [
            "metaphysical possibility is not established by this dossier",
            "question-begging and parody risks remain live",
            "the possibility ladder localizes but does not close the modal bridge",
            "attribute coherence has a ledger but still has unresolved tensions",
        ],
    }


def _build_ontological_soundness_parody_discriminator_matrix() -> dict[str, Any]:
    dossier = ONTOLOGICAL_SOUNDNESS_DOSSIER
    discriminator_specs = {
        "maximally_great_island": {
            "discriminator_id": "category-contingency-filter",
            "discriminator_status": "candidate_resolved",
            "discriminator_rule": "Reject contingent concrete objects that cannot be necessary personal ultimates.",
            "required_artifacts": ["target-concepts.json", "attribute-coherence-checks.json"],
            "open_requirements": [],
        },
        "necessarily_existing_bad_god": {
            "discriminator_id": "positive-property-and-goodness-filter",
            "discriminator_status": "contested",
            "discriminator_rule": (
                "Reject only if positive-property grounding and perfect-goodness grounding are independently complete."
            ),
            "required_artifacts": [
                "positive-property-filter-checks.json",
                "positive-grounding-checks.json",
                "moral-perfection-grounding-checks.json",
                "evil-hiddenness-moral-pressure-checks.json",
            ],
            "open_requirements": [
                "non-ad-hoc positive-property grounding",
                "perfect-goodness grounding under evil and hiddenness pressure",
            ],
        },
        "necessary_impersonal_ultimate": {
            "discriminator_id": "personal-ultimate-target-filter",
            "discriminator_status": "contested",
            "discriminator_rule": (
                "Reject as target-equivalent only if personhood and perfect-goodness filters are independently grounded."
            ),
            "required_artifacts": [
                "rival-necessary-parity-checks.json",
                "possible-necessary-existence-checks.json",
                "target-concepts.json",
            ],
            "open_requirements": [
                "non-question-begging personhood discriminator",
                "rival necessary ultimate parity resolution",
            ],
        },
    }
    rows = []
    for parody in dossier["parody_tests"]:
        spec = discriminator_specs[parody["id"]]
        rows.append({
            "parody_test_id": parody["id"],
            "parody_result": parody["result"],
            "parody_reason": parody["reason"],
            "discriminator_id": spec["discriminator_id"],
            "discriminator_status": spec["discriminator_status"],
            "discriminator_rule": spec["discriminator_rule"],
            "required_artifacts": spec["required_artifacts"],
            "open_requirements": spec["open_requirements"],
            "proof_evidence_materialized": False,
        })
    return {
        "status": "contested",
        "matrix": {
            "id": "ontological-soundness-parody-discriminator-matrix-v0",
            "input_dossier_id": dossier["id"],
            "target_obligation_id": "obl-ontological-soundness",
            "argument_id": dossier["argument_id"],
            "target_premise_id": dossier["target_premise_id"],
            "retrieved_at": RETRIEVED_AT,
            "discriminator_rows": rows,
            "authorization_state": {
                "matrix_recorded": True,
                "parody_pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "A parody discriminator row can help localize blockers, but the matrix "
                "does not resolve ontological soundness unless every contested discriminator is complete."
            ),
            "verdict": "contested",
        },
        "warning": "Parody discriminator rows are blocker localization, not proof evidence.",
    }


def _build_ontological_soundness_parody_discriminator_checks(
    ontological_soundness_parody_discriminator_matrix: dict[str, Any] | None = None,
) -> dict[str, Any]:
    dossier = ONTOLOGICAL_SOUNDNESS_DOSSIER
    matrix_doc = (
        ontological_soundness_parody_discriminator_matrix
        or _build_ontological_soundness_parody_discriminator_matrix()
    )
    matrix = matrix_doc["matrix"]
    parody_ids = {parody["id"] for parody in dossier["parody_tests"]}
    row_parody_ids = {row["parody_test_id"] for row in matrix["discriminator_rows"]}
    unresolved_parody_ids = [
        parody["id"] for parody in dossier["parody_tests"]
        if parody["result"] == "not_resolved"
    ]
    contested_row_ids = [
        row["parody_test_id"] for row in matrix["discriminator_rows"]
        if row["discriminator_status"] == "contested"
    ]
    nonmaterialized_row_ids = [
        row["parody_test_id"] for row in matrix["discriminator_rows"]
        if row["proof_evidence_materialized"] is False
    ]
    checks = [
        {
            "id": "check-soundness-dossier-linked",
            "status": "complete"
            if matrix["input_dossier_id"] == dossier["id"]
            and matrix["target_obligation_id"] == "obl-ontological-soundness"
            else "open",
            "input_dossier_id": matrix["input_dossier_id"],
            "dossier_id": dossier["id"],
        },
        {
            "id": "check-every-parody-test-has-discriminator-row",
            "status": "complete" if parody_ids <= row_parody_ids else "open",
            "parody_test_ids": sorted(parody_ids),
            "row_parody_ids": sorted(row_parody_ids),
            "missing_parody_ids": sorted(parody_ids - row_parody_ids),
        },
        {
            "id": "check-unresolved-parodies-have-contested-discriminators",
            "status": "complete" if set(unresolved_parody_ids) <= set(contested_row_ids) else "open",
            "unresolved_parody_ids": unresolved_parody_ids,
            "contested_row_ids": contested_row_ids,
        },
        {
            "id": "check-open-discriminators-retained",
            "status": "contested" if contested_row_ids else "complete",
            "contested_row_ids": contested_row_ids,
        },
        {
            "id": "check-discriminator-matrix-not-promoted-to-proof",
            "status": "contested"
            if matrix["verdict"] == "contested"
            and len(nonmaterialized_row_ids) == len(matrix["discriminator_rows"])
            and matrix["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": matrix["authorization_state"],
            "decision_rule": matrix["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_obligation_id": matrix["target_obligation_id"],
        "argument_id": matrix["argument_id"],
        "target_premise_id": matrix["target_premise_id"],
        "scope": "ontological_soundness_parody_discriminators_not_proof",
        "checks": checks,
        "remaining_risks": [
            "bad-god parody still needs independent positive-property and goodness grounding",
            "impersonal necessary ultimate remains a live rival unless personhood filters are grounded",
            "parody discriminator matrix is not a soundness proof",
        ],
    }


def _build_ontological_soundness_bad_god_discharge_criteria(
    ontological_soundness_parody_discriminator_matrix: dict[str, Any] | None = None,
    positive_property_filter_checks: dict[str, Any] | None = None,
    positive_grounding_checks: dict[str, Any] | None = None,
    moral_perfection_grounding_checks: dict[str, Any] | None = None,
    evil_hiddenness_moral_pressure_checks: dict[str, Any] | None = None,
    rival_necessary_parity_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    matrix_doc = (
        ontological_soundness_parody_discriminator_matrix
        or _build_ontological_soundness_parody_discriminator_matrix()
    )
    matrix = matrix_doc["matrix"]
    positive_property_filter_checks = positive_property_filter_checks or _build_positive_property_filter_checks()
    positive_grounding_checks = positive_grounding_checks or _build_positive_grounding_checks()
    moral_perfection_grounding_checks = moral_perfection_grounding_checks or _build_moral_perfection_grounding_checks()
    evil_hiddenness_moral_pressure_checks = (
        evil_hiddenness_moral_pressure_checks or _build_evil_hiddenness_moral_pressure_checks()
    )
    rival_necessary_parity_checks = rival_necessary_parity_checks or _build_rival_necessary_parity_checks()
    bad_god_row = next(
        row for row in matrix["discriminator_rows"]
        if row["parody_test_id"] == "necessarily_existing_bad_god"
    )
    requirement_specs = [
        (
            "positive-property-filter-complete",
            "positive-property-filter-checks.json",
            positive_property_filter_checks["status"],
            "bad-god candidates must be screened by a non-arbitrary positive-property filter",
        ),
        (
            "positive-grounding-complete",
            "positive-grounding-checks.json",
            positive_grounding_checks["status"],
            "the positive-property predicate must have independent grounding",
        ),
        (
            "moral-perfection-grounding-complete",
            "moral-perfection-grounding-checks.json",
            moral_perfection_grounding_checks["status"],
            "perfect goodness must be grounded without circularly assuming the target God",
        ),
        (
            "evil-hiddenness-pressure-complete",
            "evil-hiddenness-moral-pressure-checks.json",
            evil_hiddenness_moral_pressure_checks["status"],
            "perfect goodness must withstand evil and hiddenness pressure",
        ),
        (
            "rival-parity-complete",
            "rival-necessary-parity-checks.json",
            rival_necessary_parity_checks["status"],
            "rival necessary concepts must be blocked by independent filters",
        ),
    ]
    discharge_requirements = [
        {
            "requirement_id": requirement_id,
            "source_artifact": source_artifact,
            "source_status": source_status,
            "requirement_status": "complete" if source_status == "complete" else "contested",
            "discharge_rule": discharge_rule,
            "proof_evidence_materialized": False,
        }
        for requirement_id, source_artifact, source_status, discharge_rule in requirement_specs
    ]
    return {
        "status": "contested",
        "criteria": {
            "id": "ontological-soundness-bad-god-discharge-criteria-v0",
            "input_discriminator_matrix_id": matrix["id"],
            "target_obligation_id": matrix["target_obligation_id"],
            "target_parody_test_id": bad_god_row["parody_test_id"],
            "target_discriminator_id": bad_god_row["discriminator_id"],
            "retrieved_at": RETRIEVED_AT,
            "discharge_requirements": discharge_requirements,
            "authorization_state": {
                "criteria_recorded": True,
                "bad_god_parody_discharged": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Bad-god parody pressure is discharged only when every requirement is complete "
                "and independently evidenced; recording criteria does not discharge it."
            ),
            "verdict": "contested",
        },
        "warning": "Bad-god discharge criteria are unresolved requirements, not proof evidence.",
    }


def _build_ontological_soundness_bad_god_discharge_checks(
    ontological_soundness_parody_discriminator_matrix: dict[str, Any] | None = None,
    ontological_soundness_bad_god_discharge_criteria: dict[str, Any] | None = None,
) -> dict[str, Any]:
    matrix_doc = (
        ontological_soundness_parody_discriminator_matrix
        or _build_ontological_soundness_parody_discriminator_matrix()
    )
    criteria_doc = (
        ontological_soundness_bad_god_discharge_criteria
        or _build_ontological_soundness_bad_god_discharge_criteria(matrix_doc)
    )
    matrix = matrix_doc["matrix"]
    criteria = criteria_doc["criteria"]
    bad_god_row = next(
        row for row in matrix["discriminator_rows"]
        if row["parody_test_id"] == "necessarily_existing_bad_god"
    )
    required_artifacts = set(bad_god_row["required_artifacts"] + ["rival-necessary-parity-checks.json"])
    criteria_artifacts = {row["source_artifact"] for row in criteria["discharge_requirements"]}
    contested_requirement_ids = [
        row["requirement_id"] for row in criteria["discharge_requirements"]
        if row["requirement_status"] == "contested"
    ]
    nonmaterialized_requirement_ids = [
        row["requirement_id"] for row in criteria["discharge_requirements"]
        if row["proof_evidence_materialized"] is False
    ]
    checks = [
        {
            "id": "check-parody-discriminator-linked",
            "status": "complete"
            if criteria["input_discriminator_matrix_id"] == matrix["id"]
            and criteria["target_obligation_id"] == matrix["target_obligation_id"]
            else "open",
            "input_discriminator_matrix_id": criteria["input_discriminator_matrix_id"],
            "matrix_id": matrix["id"],
        },
        {
            "id": "check-bad-god-row-selected",
            "status": "complete"
            if criteria["target_parody_test_id"] == "necessarily_existing_bad_god"
            and bad_god_row["discriminator_status"] == "contested"
            else "open",
            "target_parody_test_id": criteria["target_parody_test_id"],
            "discriminator_status": bad_god_row["discriminator_status"],
        },
        {
            "id": "check-required-artifacts-covered",
            "status": "complete" if required_artifacts <= criteria_artifacts else "open",
            "required_artifacts": sorted(required_artifacts),
            "criteria_artifacts": sorted(criteria_artifacts),
            "missing_artifacts": sorted(required_artifacts - criteria_artifacts),
        },
        {
            "id": "check-discharge-requirements-remain-contested",
            "status": "contested" if contested_requirement_ids else "complete",
            "contested_requirement_ids": contested_requirement_ids,
        },
        {
            "id": "check-bad-god-discharge-not-promoted-to-proof",
            "status": "contested"
            if criteria["verdict"] == "contested"
            and len(nonmaterialized_requirement_ids) == len(criteria["discharge_requirements"])
            and criteria["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": criteria["authorization_state"],
            "decision_rule": criteria["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_obligation_id": criteria["target_obligation_id"],
        "target_parody_test_id": criteria["target_parody_test_id"],
        "scope": "bad_god_discharge_criteria_not_proof",
        "checks": checks,
        "remaining_risks": [
            "positive-property filter remains contested",
            "perfect-goodness grounding remains contested",
            "rival necessary parity remains contested",
        ],
    }


def _build_ontological_soundness_bad_god_discharge_task_queue(
    ontological_soundness_bad_god_discharge_criteria: dict[str, Any] | None = None,
) -> dict[str, Any]:
    criteria_doc = (
        ontological_soundness_bad_god_discharge_criteria
        or _build_ontological_soundness_bad_god_discharge_criteria()
    )
    criteria = criteria_doc["criteria"]
    verifier_commands = [
        "rtk env PYTHONPATH=src python3 -m pytest tests/test_godproof.py -q",
        "rtk env PYTHONPATH=src python3 -m pytest -q",
    ]
    task_items = []
    for requirement in criteria["discharge_requirements"]:
        task_items.append({
            "task_id": f"task-{requirement['requirement_id']}",
            "requirement_id": requirement["requirement_id"],
            "source_artifact": requirement["source_artifact"],
            "source_status": requirement["source_status"],
            "required_result": requirement["discharge_rule"],
            "acceptance_criteria": [
                f"{requirement['source_artifact']} reports complete for the referenced blocker",
                "proof-readiness.json remains false unless every soundness blocker is complete",
                "transcript.jsonl records the task outcome before any proof claim",
            ],
            "verifier_commands": verifier_commands,
            "task_status": "queued_not_executed",
            "proof_evidence_materialized": False,
        })
    return {
        "status": "contested",
        "queue": {
            "id": "ontological-soundness-bad-god-discharge-task-queue-v0",
            "input_criteria_id": criteria["id"],
            "target_obligation_id": criteria["target_obligation_id"],
            "target_parody_test_id": criteria["target_parody_test_id"],
            "retrieved_at": RETRIEVED_AT,
            "task_items": task_items,
            "authorization_state": {
                "task_queue_recorded": True,
                "tasks_executed": False,
                "bad_god_parody_discharged": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Tasks are queued execution units for bad-god discharge only. "
                "They do not execute requirements or authorize a proof claim."
            ),
            "verdict": "contested",
        },
        "warning": "Queued bad-god tasks are not proof evidence.",
    }


def _build_ontological_soundness_bad_god_discharge_task_checks(
    ontological_soundness_bad_god_discharge_criteria: dict[str, Any] | None = None,
    ontological_soundness_bad_god_discharge_task_queue: dict[str, Any] | None = None,
) -> dict[str, Any]:
    criteria_doc = (
        ontological_soundness_bad_god_discharge_criteria
        or _build_ontological_soundness_bad_god_discharge_criteria()
    )
    queue_doc = (
        ontological_soundness_bad_god_discharge_task_queue
        or _build_ontological_soundness_bad_god_discharge_task_queue(criteria_doc)
    )
    criteria = criteria_doc["criteria"]
    queue = queue_doc["queue"]
    requirement_ids = {row["requirement_id"] for row in criteria["discharge_requirements"]}
    task_requirement_ids = {row["requirement_id"] for row in queue["task_items"]}
    task_ids_with_verifiers = [
        row["task_id"] for row in queue["task_items"]
        if row["verifier_commands"] and row["acceptance_criteria"]
    ]
    unexecuted_task_ids = [
        row["task_id"] for row in queue["task_items"]
        if row["task_status"] == "queued_not_executed"
        and row["proof_evidence_materialized"] is False
    ]
    checks = [
        {
            "id": "check-bad-god-criteria-linked",
            "status": "complete"
            if queue["input_criteria_id"] == criteria["id"]
            and queue["target_parody_test_id"] == criteria["target_parody_test_id"]
            else "open",
            "input_criteria_id": queue["input_criteria_id"],
            "criteria_id": criteria["id"],
        },
        {
            "id": "check-every-discharge-requirement-has-task",
            "status": "complete" if requirement_ids <= task_requirement_ids else "open",
            "requirement_ids": sorted(requirement_ids),
            "task_requirement_ids": sorted(task_requirement_ids),
            "missing_requirement_ids": sorted(requirement_ids - task_requirement_ids),
        },
        {
            "id": "check-tasks-have-verifiers-and-acceptance-criteria",
            "status": "complete" if len(task_ids_with_verifiers) == len(queue["task_items"]) else "open",
            "task_ids": task_ids_with_verifiers,
        },
        {
            "id": "check-bad-god-tasks-remain-unexecuted",
            "status": "complete" if len(unexecuted_task_ids) == len(queue["task_items"]) else "open",
            "task_ids": unexecuted_task_ids,
        },
        {
            "id": "check-task-queue-not-promoted-to-proof",
            "status": "contested"
            if queue["verdict"] == "contested"
            and queue["authorization_state"]["tasks_executed"] is False
            and queue["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": queue["authorization_state"],
            "decision_rule": queue["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_obligation_id": queue["target_obligation_id"],
        "target_parody_test_id": queue["target_parody_test_id"],
        "scope": "bad_god_discharge_task_queue_not_executed",
        "checks": checks,
        "remaining_risks": [
            "bad-god discharge tasks are queued but not executed",
            "no requirement output is materialized as proof evidence",
            "proof claim remains disallowed",
        ],
    }


def _build_ontological_soundness_bad_god_task_dependency_graph(
    ontological_soundness_bad_god_discharge_task_queue: dict[str, Any] | None = None,
) -> dict[str, Any]:
    queue_doc = (
        ontological_soundness_bad_god_discharge_task_queue
        or _build_ontological_soundness_bad_god_discharge_task_queue()
    )
    queue = queue_doc["queue"]
    nodes = [
        {
            "task_id": task["task_id"],
            "requirement_id": task["requirement_id"],
            "source_artifact": task["source_artifact"],
            "task_status": task["task_status"],
            "proof_evidence_materialized": task["proof_evidence_materialized"],
        }
        for task in queue["task_items"]
    ]
    edges = [
        {
            "from_task_id": "task-evil-hiddenness-pressure-complete",
            "to_task_id": "task-moral-perfection-grounding-complete",
            "dependency_type": "pressure_must_be_absorbed_before_goodness_grounding",
        },
        {
            "from_task_id": "task-moral-perfection-grounding-complete",
            "to_task_id": "task-positive-grounding-complete",
            "dependency_type": "goodness_route_constrains_positive_property_grounding",
        },
        {
            "from_task_id": "task-positive-grounding-complete",
            "to_task_id": "task-positive-property-filter-complete",
            "dependency_type": "grounding_required_before_filter_promotion",
        },
        {
            "from_task_id": "task-positive-property-filter-complete",
            "to_task_id": "task-rival-parity-complete",
            "dependency_type": "filter_required_before_rival_parity_discharge",
        },
    ]
    return {
        "status": "contested",
        "graph": {
            "id": "ontological-soundness-bad-god-task-dependency-graph-v0",
            "input_task_queue_id": queue["id"],
            "target_obligation_id": queue["target_obligation_id"],
            "target_parody_test_id": queue["target_parody_test_id"],
            "retrieved_at": RETRIEVED_AT,
            "nodes": nodes,
            "edges": edges,
            "authorization_state": {
                "dependency_graph_recorded": True,
                "tasks_executed": False,
                "bad_god_parody_discharged": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Dependency edges order queued tasks only. They do not execute tasks, "
                "complete requirements, or authorize a proof claim."
            ),
            "verdict": "contested",
        },
        "warning": "Bad-god task dependency graph is an execution ordering scaffold, not proof evidence.",
    }


def _build_ontological_soundness_bad_god_task_dependency_checks(
    ontological_soundness_bad_god_discharge_task_queue: dict[str, Any] | None = None,
    ontological_soundness_bad_god_task_dependency_graph: dict[str, Any] | None = None,
) -> dict[str, Any]:
    queue_doc = (
        ontological_soundness_bad_god_discharge_task_queue
        or _build_ontological_soundness_bad_god_discharge_task_queue()
    )
    graph_doc = (
        ontological_soundness_bad_god_task_dependency_graph
        or _build_ontological_soundness_bad_god_task_dependency_graph(queue_doc)
    )
    queue = queue_doc["queue"]
    graph = graph_doc["graph"]
    task_ids = {task["task_id"] for task in queue["task_items"]}
    node_task_ids = {node["task_id"] for node in graph["nodes"]}
    edge_pairs = {(edge["from_task_id"], edge["to_task_id"]) for edge in graph["edges"]}
    required_edges = {
        ("task-evil-hiddenness-pressure-complete", "task-moral-perfection-grounding-complete"),
        ("task-moral-perfection-grounding-complete", "task-positive-grounding-complete"),
        ("task-positive-grounding-complete", "task-positive-property-filter-complete"),
        ("task-positive-property-filter-complete", "task-rival-parity-complete"),
    }
    unexecuted_node_ids = [
        node["task_id"] for node in graph["nodes"]
        if node["task_status"] == "queued_not_executed"
        and node["proof_evidence_materialized"] is False
    ]
    checks = [
        {
            "id": "check-task-queue-linked",
            "status": "complete"
            if graph["input_task_queue_id"] == queue["id"]
            and graph["target_parody_test_id"] == queue["target_parody_test_id"]
            else "open",
            "input_task_queue_id": graph["input_task_queue_id"],
            "queue_id": queue["id"],
        },
        {
            "id": "check-every-task-has-graph-node",
            "status": "complete" if task_ids <= node_task_ids else "open",
            "task_ids": sorted(task_ids),
            "node_task_ids": sorted(node_task_ids),
            "missing_task_ids": sorted(task_ids - node_task_ids),
        },
        {
            "id": "check-required-dependency-edges-present",
            "status": "complete" if required_edges <= edge_pairs else "open",
            "required_edges": sorted([list(edge) for edge in required_edges]),
            "edge_pairs": sorted([list(edge) for edge in edge_pairs]),
        },
        {
            "id": "check-graph-remains-unexecuted",
            "status": "complete" if len(unexecuted_node_ids) == len(graph["nodes"]) else "open",
            "task_ids": unexecuted_node_ids,
        },
        {
            "id": "check-dependency-graph-not-promoted-to-proof",
            "status": "contested"
            if graph["verdict"] == "contested"
            and graph["authorization_state"]["tasks_executed"] is False
            and graph["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": graph["authorization_state"],
            "decision_rule": graph["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_obligation_id": graph["target_obligation_id"],
        "target_parody_test_id": graph["target_parody_test_id"],
        "scope": "bad_god_task_dependency_graph_not_executed",
        "checks": checks,
        "remaining_risks": [
            "dependency graph is recorded but tasks are not executed",
            "bad-god parody remains undispatched",
            "proof claim remains disallowed",
        ],
    }


def _build_ontological_soundness_bad_god_evil_hiddenness_pressure_matrix(
    ontological_soundness_bad_god_task_dependency_graph: dict[str, Any] | None = None,
) -> dict[str, Any]:
    graph_doc = (
        ontological_soundness_bad_god_task_dependency_graph
        or _build_ontological_soundness_bad_god_task_dependency_graph()
    )
    graph = graph_doc["graph"]
    audit = EVIL_HIDDENNESS_MORAL_PRESSURE_AUDIT
    pressure_rows = [
        {
            "constraint_id": row["constraint_id"],
            "moral_pressure": row["moral_pressure"],
            "candidate_response_ids": row["candidate_response_ids"],
            "pressure_status": row["status"],
            "proof_evidence_materialized": False,
        }
        for row in audit["pressure_links"]
    ]
    sufficiency_rows = [
        {
            "sufficiency_test_id": row["id"],
            "sufficiency_status": row["status"],
            "result": row["result"],
            "proof_evidence_materialized": False,
        }
        for row in audit["response_sufficiency_tests"]
    ]
    return {
        "status": "contested",
        "matrix": {
            "id": "ontological-soundness-bad-god-evil-hiddenness-pressure-matrix-v0",
            "input_dependency_graph_id": graph["id"],
            "input_audit_id": audit["id"],
            "target_obligation_id": graph["target_obligation_id"],
            "target_parody_test_id": graph["target_parody_test_id"],
            "target_task_id": "task-evil-hiddenness-pressure-complete",
            "retrieved_at": RETRIEVED_AT,
            "pressure_rows": pressure_rows,
            "sufficiency_rows": sufficiency_rows,
            "authorization_state": {
                "pressure_matrix_recorded": True,
                "pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "The pressure matrix records candidate responses and open sufficiency tests. "
                "It resolves the task only when every substantive sufficiency row is complete."
            ),
            "verdict": "contested",
        },
        "warning": "Evil-hiddenness pressure matrix is not a perfect-goodness proof.",
    }


def _build_ontological_soundness_bad_god_evil_hiddenness_pressure_checks(
    ontological_soundness_bad_god_task_dependency_graph: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evil_hiddenness_pressure_matrix: dict[str, Any] | None = None,
) -> dict[str, Any]:
    graph_doc = (
        ontological_soundness_bad_god_task_dependency_graph
        or _build_ontological_soundness_bad_god_task_dependency_graph()
    )
    matrix_doc = (
        ontological_soundness_bad_god_evil_hiddenness_pressure_matrix
        or _build_ontological_soundness_bad_god_evil_hiddenness_pressure_matrix(graph_doc)
    )
    graph = graph_doc["graph"]
    matrix = matrix_doc["matrix"]
    graph_task_ids = {node["task_id"] for node in graph["nodes"]}
    constraint_ids = {constraint["id"] for constraint in EVIL_HIDDENNESS_CONSTRAINT_MODEL["constraints"]}
    pressure_constraint_ids = {row["constraint_id"] for row in matrix["pressure_rows"]}
    open_sufficiency_ids = [
        row["sufficiency_test_id"] for row in matrix["sufficiency_rows"]
        if row["sufficiency_status"] == "open"
    ]
    nonmaterialized_sufficiency_ids = [
        row["sufficiency_test_id"] for row in matrix["sufficiency_rows"]
        if row["proof_evidence_materialized"] is False
    ]
    checks = [
        {
            "id": "check-bad-god-dependency-graph-linked",
            "status": "complete"
            if matrix["input_dependency_graph_id"] == graph["id"]
            and matrix["target_parody_test_id"] == graph["target_parody_test_id"]
            else "open",
            "input_dependency_graph_id": matrix["input_dependency_graph_id"],
            "graph_id": graph["id"],
        },
        {
            "id": "check-evil-hiddenness-task-selected",
            "status": "complete"
            if matrix["target_task_id"] == "task-evil-hiddenness-pressure-complete"
            and matrix["target_task_id"] in graph_task_ids
            else "open",
            "target_task_id": matrix["target_task_id"],
            "graph_task_ids": sorted(graph_task_ids),
        },
        {
            "id": "check-pressure-constraints-covered",
            "status": "complete" if constraint_ids <= pressure_constraint_ids else "open",
            "constraint_ids": sorted(constraint_ids),
            "pressure_constraint_ids": sorted(pressure_constraint_ids),
            "missing_constraint_ids": sorted(constraint_ids - pressure_constraint_ids),
        },
        {
            "id": "check-sufficiency-tests-retain-open-pressure",
            "status": "contested" if open_sufficiency_ids else "complete",
            "open_sufficiency_ids": open_sufficiency_ids,
        },
        {
            "id": "check-pressure-matrix-not-promoted-to-proof",
            "status": "contested"
            if matrix["verdict"] == "contested"
            and len(nonmaterialized_sufficiency_ids) == len(matrix["sufficiency_rows"])
            and matrix["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": matrix["authorization_state"],
            "decision_rule": matrix["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_obligation_id": matrix["target_obligation_id"],
        "target_parody_test_id": matrix["target_parody_test_id"],
        "target_task_id": matrix["target_task_id"],
        "scope": "bad_god_evil_hiddenness_pressure_matrix_not_proof",
        "checks": checks,
        "remaining_risks": [
            "evidential probability pressure remains open",
            "non-resistant nonbelief pressure remains open",
            "moral-reasoning preservation remains open",
        ],
    }


def _build_ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_queue(
    ontological_soundness_bad_god_evil_hiddenness_pressure_matrix: dict[str, Any] | None = None,
) -> dict[str, Any]:
    matrix_doc = (
        ontological_soundness_bad_god_evil_hiddenness_pressure_matrix
        or _build_ontological_soundness_bad_god_evil_hiddenness_pressure_matrix()
    )
    matrix = matrix_doc["matrix"]
    task_items = [
        {
            "task_id": f"task-{row['sufficiency_test_id']}",
            "sufficiency_test_id": row["sufficiency_test_id"],
            "required_result": row["result"],
            "acceptance_criteria": [
                (
                    f"{row['sufficiency_test_id']} is complete in "
                    "ontological-soundness-bad-god-evil-hiddenness-pressure-matrix.json"
                ),
                (
                    "evil-hiddenness-moral-pressure-checks.json no longer reports substantive "
                    "pressure tests open"
                ),
                "proof-readiness.json remains false unless every soundness blocker is complete",
            ],
            "verifier_commands": [
                "rtk env PYTHONPATH=src python3 -m pytest tests/test_godproof.py -q",
                "rtk env PYTHONPATH=src python3 -m pytest -q",
            ],
            "task_status": "queued_not_executed",
            "proof_evidence_materialized": False,
        }
        for row in matrix["sufficiency_rows"]
        if row["sufficiency_status"] == "open"
    ]
    return {
        "status": "contested",
        "queue": {
            "id": "ontological-soundness-bad-god-evil-hiddenness-sufficiency-task-queue-v0",
            "input_pressure_matrix_id": matrix["id"],
            "target_obligation_id": matrix["target_obligation_id"],
            "target_parody_test_id": matrix["target_parody_test_id"],
            "target_task_id": matrix["target_task_id"],
            "retrieved_at": RETRIEVED_AT,
            "task_items": task_items,
            "authorization_state": {
                "sufficiency_task_queue_recorded": True,
                "sufficiency_tasks_executed": False,
                "pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Open sufficiency tests become queued tasks. The bad-god pressure task is not "
                "resolved until these tasks are executed and their source rows are complete."
            ),
        },
        "warning": "Sufficiency task queue is a work plan, not proof evidence.",
    }


def _build_ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_checks(
    ontological_soundness_bad_god_evil_hiddenness_pressure_matrix: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_queue: dict[str, Any] | None = None,
) -> dict[str, Any]:
    matrix_doc = (
        ontological_soundness_bad_god_evil_hiddenness_pressure_matrix
        or _build_ontological_soundness_bad_god_evil_hiddenness_pressure_matrix()
    )
    queue_doc = (
        ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_queue
        or _build_ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_queue(matrix_doc)
    )
    matrix = matrix_doc["matrix"]
    queue = queue_doc["queue"]
    open_sufficiency_task_ids = {
        f"task-{row['sufficiency_test_id']}"
        for row in matrix["sufficiency_rows"]
        if row["sufficiency_status"] == "open"
    }
    queued_task_ids = {row["task_id"] for row in queue["task_items"]}
    executable_task_ids = {
        row["task_id"]
        for row in queue["task_items"]
        if row["verifier_commands"] and row["acceptance_criteria"]
    }
    unexecuted_task_ids = [
        row["task_id"]
        for row in queue["task_items"]
        if row["task_status"] == "queued_not_executed"
        and row["proof_evidence_materialized"] is False
    ]
    checks = [
        {
            "id": "check-pressure-matrix-linked",
            "status": "complete"
            if queue["input_pressure_matrix_id"] == matrix["id"]
            and queue["target_task_id"] == matrix["target_task_id"]
            else "open",
            "input_pressure_matrix_id": queue["input_pressure_matrix_id"],
            "pressure_matrix_id": matrix["id"],
            "target_task_id": queue["target_task_id"],
        },
        {
            "id": "check-every-open-sufficiency-test-has-task",
            "status": "complete" if open_sufficiency_task_ids == queued_task_ids else "open",
            "open_sufficiency_task_ids": sorted(open_sufficiency_task_ids),
            "queued_task_ids": sorted(queued_task_ids),
            "missing_task_ids": sorted(open_sufficiency_task_ids - queued_task_ids),
        },
        {
            "id": "check-sufficiency-tasks-have-verifiers-and-acceptance-criteria",
            "status": "complete" if executable_task_ids == queued_task_ids else "open",
            "executable_task_ids": sorted(executable_task_ids),
            "queued_task_ids": sorted(queued_task_ids),
        },
        {
            "id": "check-sufficiency-tasks-remain-unexecuted",
            "status": "complete" if len(unexecuted_task_ids) == len(queue["task_items"]) else "open",
            "unexecuted_task_ids": unexecuted_task_ids,
        },
        {
            "id": "check-sufficiency-task-queue-not-promoted-to-proof",
            "status": "contested"
            if queue_doc["status"] == "contested"
            and queue["authorization_state"]["sufficiency_tasks_executed"] is False
            and queue["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": queue["authorization_state"],
            "decision_rule": queue["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_obligation_id": queue["target_obligation_id"],
        "target_parody_test_id": queue["target_parody_test_id"],
        "target_task_id": queue["target_task_id"],
        "scope": "bad_god_evil_hiddenness_sufficiency_tasks_not_proof",
        "checks": checks,
        "readiness": {
            "ready_to_execute": False,
            "blocking_open_obligation_ids": ["obl-ontological-soundness"],
        },
    }


def _build_ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold(
    ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_queue: dict[str, Any] | None = None,
    evidential_evil_probability_audit: dict[str, Any] | None = None,
    evidential_evil_probability_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    queue_doc = (
        ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_queue
        or _build_ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_queue()
    )
    audit_doc = evidential_evil_probability_audit or _build_evidential_evil_probability_audit()
    checks_doc = evidential_evil_probability_checks or _build_evidential_evil_probability_checks()
    queue = queue_doc["queue"]
    audit = audit_doc["audit"]
    target_task = next(
        row for row in queue["task_items"]
        if row["sufficiency_test_id"] == audit["target_pressure_test_id"]
    )
    evaluation_lanes = [
        {
            "lane_id": f"lane-{requirement['id']}",
            "probability_requirement_id": requirement["id"],
            "requirement_status": requirement["status"],
            "required_output": requirement["requirement"],
            "linked_task_id": target_task["task_id"],
            "lane_status": "ready_not_executed",
            "verifier_commands": [
                "rtk env PYTHONPATH=src python3 -m pytest tests/test_godproof.py -q",
                "rtk env PYTHONPATH=src python3 -m pytest -q",
            ],
        }
        for requirement in audit["probability_requirements"]
    ]
    return {
        "status": "contested",
        "scaffold": {
            "id": "ontological-soundness-bad-god-evidential-probability-pressure-task-scaffold-v0",
            "input_task_queue_id": queue["id"],
            "input_probability_audit_id": audit["id"],
            "input_probability_checks_scope": checks_doc["scope"],
            "target_task_id": target_task["task_id"],
            "parent_task_id": queue["target_task_id"],
            "target_pressure_test_id": audit["target_pressure_test_id"],
            "retrieved_at": RETRIEVED_AT,
            "hypothesis_ids": [row["id"] for row in audit["hypotheses"]],
            "evidence_dimension_ids": [row["id"] for row in audit["evidence_dimensions"]],
            "candidate_response_model_ids": [row["id"] for row in audit["candidate_response_models"]],
            "live_objection_ids": [
                row["id"] for row in audit["live_objections"]
                if row["status"] == "live"
            ],
            "linked_probability_check_ids": [row["id"] for row in checks_doc["checks"]],
            "evaluation_lanes": evaluation_lanes,
            "execution_state": {
                "scaffold_recorded": True,
                "evidence_gathering_executed": False,
                "probability_pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "The evidential-probability task can close only after every evaluation lane is "
                "executed, live objections are discharged, and probability checks no longer "
                "remain contested."
            ),
        },
        "warning": "Evidential-probability task scaffold is not executed evidence.",
    }


def _build_ontological_soundness_bad_god_evidential_probability_pressure_task_checks(
    ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_queue: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold: dict[str, Any] | None = None,
    evidential_evil_probability_audit: dict[str, Any] | None = None,
    evidential_evil_probability_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    queue_doc = (
        ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_queue
        or _build_ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_queue()
    )
    audit_doc = evidential_evil_probability_audit or _build_evidential_evil_probability_audit()
    checks_doc = evidential_evil_probability_checks or _build_evidential_evil_probability_checks()
    scaffold_doc = (
        ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold
        or _build_ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold(
            queue_doc,
            audit_doc,
            checks_doc,
        )
    )
    queue = queue_doc["queue"]
    audit = audit_doc["audit"]
    scaffold = scaffold_doc["scaffold"]
    queued_task_ids = {row["task_id"] for row in queue["task_items"]}
    probability_requirement_ids = {row["id"] for row in audit["probability_requirements"]}
    lane_requirement_ids = {row["probability_requirement_id"] for row in scaffold["evaluation_lanes"]}
    live_objection_ids = [
        row["id"] for row in audit["live_objections"]
        if row["status"] == "live"
    ]
    checks = [
        {
            "id": "check-sufficiency-task-linked",
            "status": "complete"
            if scaffold["input_task_queue_id"] == queue["id"]
            and scaffold["target_task_id"] in queued_task_ids
            else "open",
            "input_task_queue_id": scaffold["input_task_queue_id"],
            "target_task_id": scaffold["target_task_id"],
        },
        {
            "id": "check-probability-audit-linked",
            "status": "complete"
            if scaffold["input_probability_audit_id"] == audit["id"]
            and scaffold["target_pressure_test_id"] == audit["target_pressure_test_id"]
            else "open",
            "input_probability_audit_id": scaffold["input_probability_audit_id"],
            "target_pressure_test_id": scaffold["target_pressure_test_id"],
        },
        {
            "id": "check-probability-checks-linked",
            "status": "complete"
            if scaffold["input_probability_checks_scope"] == checks_doc["scope"]
            and set(scaffold["linked_probability_check_ids"]) == {row["id"] for row in checks_doc["checks"]}
            else "open",
            "input_probability_checks_scope": scaffold["input_probability_checks_scope"],
            "probability_checks_status": checks_doc["status"],
        },
        {
            "id": "check-evaluation-lanes-cover-probability-requirements",
            "status": "complete" if probability_requirement_ids == lane_requirement_ids else "open",
            "probability_requirement_ids": sorted(probability_requirement_ids),
            "lane_requirement_ids": sorted(lane_requirement_ids),
            "missing_requirement_ids": sorted(probability_requirement_ids - lane_requirement_ids),
        },
        {
            "id": "check-live-objections-retained",
            "status": "contested" if live_objection_ids else "complete",
            "live_objection_ids": live_objection_ids,
        },
        {
            "id": "check-scaffold-not-executed-or-promoted",
            "status": "contested"
            if scaffold_doc["status"] == "contested"
            and scaffold["execution_state"]["evidence_gathering_executed"] is False
            and scaffold["execution_state"]["proof_claim_allowed"] is False
            else "open",
            "execution_state": scaffold["execution_state"],
            "decision_rule": scaffold["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_obligation_id": queue["target_obligation_id"],
        "target_parody_test_id": queue["target_parody_test_id"],
        "target_task_id": scaffold["target_task_id"],
        "target_pressure_test_id": scaffold["target_pressure_test_id"],
        "scope": "bad_god_evidential_probability_pressure_task_scaffold_not_proof",
        "checks": checks,
        "remaining_risks": [
            "live evidential evil objections remain undispatched",
            "probability checks remain contested",
            "scaffold has not executed evidence gathering",
        ],
    }


def _normalized_prior_profile(
    profile_id: str,
    prior_rows: list[dict[str, Any]],
    value_key: str,
) -> dict[str, Any]:
    raw_weights = {row["hypothesis_id"]: row[value_key] for row in prior_rows}
    total = sum(raw_weights.values())
    weights = {
        hypothesis_id: round(weight / total, 6)
        for hypothesis_id, weight in raw_weights.items()
    }
    adjustment = round(1.0 - sum(weights.values()), 6)
    if weights and adjustment:
        first_key = next(iter(weights))
        weights[first_key] = round(weights[first_key] + adjustment, 6)
    return {
        "profile_id": profile_id,
        "source_value": value_key,
        "weights": weights,
        "raw_total": round(total, 6),
        "profile_status": "ready_not_executed",
    }


def _build_ontological_soundness_bad_god_evidential_prior_sensitivity_grid(
    ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold: dict[str, Any] | None = None,
    evidential_evil_likelihood_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    scaffold_doc = (
        ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold
        or _build_ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold()
    )
    ledger_doc = evidential_evil_likelihood_ledger or _build_evidential_evil_likelihood_ledger()
    scaffold = scaffold_doc["scaffold"]
    ledger = ledger_doc["ledger"]
    target_lane = next(
        row for row in scaffold["evaluation_lanes"]
        if row["probability_requirement_id"] == "priors_declared"
    )
    prior_rows = [
        {
            "hypothesis_id": row["hypothesis_id"],
            "lower": row["lower"],
            "midpoint": round((row["lower"] + row["upper"]) / 2, 6),
            "upper": row["upper"],
            "status": row["status"],
            "rationale": row["rationale"],
        }
        for row in ledger["prior_intervals"]
    ]
    return {
        "status": "contested",
        "grid": {
            "id": "ontological-soundness-bad-god-evidential-prior-sensitivity-grid-v0",
            "input_task_scaffold_id": scaffold["id"],
            "input_likelihood_ledger_id": ledger["id"],
            "target_task_id": scaffold["target_task_id"],
            "target_lane_id": target_lane["lane_id"],
            "target_requirement_id": target_lane["probability_requirement_id"],
            "retrieved_at": RETRIEVED_AT,
            "prior_rows": prior_rows,
            "normalized_prior_profiles": [
                _normalized_prior_profile("lower-bound-normalized", prior_rows, "lower"),
                _normalized_prior_profile("midpoint-normalized", prior_rows, "midpoint"),
                _normalized_prior_profile("upper-bound-normalized", prior_rows, "upper"),
            ],
            "execution_state": {
                "prior_grid_recorded": True,
                "prior_grid_executed": False,
                "probability_pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "The prior grid only declares sensitivity inputs. It cannot resolve evidential "
                "probability pressure until profiles are run with calibrated likelihoods and "
                "response costs."
            ),
        },
        "warning": "Prior sensitivity grid is input preparation, not proof evidence.",
    }


def _build_ontological_soundness_bad_god_evidential_prior_sensitivity_checks(
    ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_prior_sensitivity_grid: dict[str, Any] | None = None,
    evidential_evil_likelihood_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    scaffold_doc = (
        ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold
        or _build_ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold()
    )
    ledger_doc = evidential_evil_likelihood_ledger or _build_evidential_evil_likelihood_ledger()
    grid_doc = (
        ontological_soundness_bad_god_evidential_prior_sensitivity_grid
        or _build_ontological_soundness_bad_god_evidential_prior_sensitivity_grid(scaffold_doc, ledger_doc)
    )
    scaffold = scaffold_doc["scaffold"]
    ledger = ledger_doc["ledger"]
    grid = grid_doc["grid"]
    ledger_prior_ids = {row["hypothesis_id"] for row in ledger["prior_intervals"]}
    grid_prior_ids = {row["hypothesis_id"] for row in grid["prior_rows"]}
    normalized_profiles = [
        profile for profile in grid["normalized_prior_profiles"]
        if abs(sum(profile["weights"].values()) - 1.0) < 1e-6
    ]
    checks = [
        {
            "id": "check-task-scaffold-linked",
            "status": "complete"
            if grid["input_task_scaffold_id"] == scaffold["id"]
            and grid["target_task_id"] == scaffold["target_task_id"]
            and grid["target_requirement_id"] == "priors_declared"
            else "open",
            "input_task_scaffold_id": grid["input_task_scaffold_id"],
            "target_requirement_id": grid["target_requirement_id"],
        },
        {
            "id": "check-likelihood-ledger-linked",
            "status": "complete" if grid["input_likelihood_ledger_id"] == ledger["id"] else "open",
            "input_likelihood_ledger_id": grid["input_likelihood_ledger_id"],
            "likelihood_ledger_id": ledger["id"],
        },
        {
            "id": "check-prior-hypotheses-covered",
            "status": "complete" if ledger_prior_ids == grid_prior_ids else "open",
            "ledger_prior_ids": sorted(ledger_prior_ids),
            "grid_prior_ids": sorted(grid_prior_ids),
            "missing_prior_ids": sorted(ledger_prior_ids - grid_prior_ids),
        },
        {
            "id": "check-normalized-prior-profiles",
            "status": "complete"
            if len(normalized_profiles) == len(grid["normalized_prior_profiles"])
            and len(normalized_profiles) >= 3
            else "open",
            "profile_ids": [profile["profile_id"] for profile in grid["normalized_prior_profiles"]],
            "normalized_profile_count": len(normalized_profiles),
        },
        {
            "id": "check-prior-grid-not-executed-or-promoted",
            "status": "contested"
            if grid_doc["status"] == "contested"
            and grid["execution_state"]["prior_grid_executed"] is False
            and grid["execution_state"]["proof_claim_allowed"] is False
            else "open",
            "execution_state": grid["execution_state"],
            "decision_rule": grid["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_task_id": grid["target_task_id"],
        "target_lane_id": grid["target_lane_id"],
        "target_requirement_id": grid["target_requirement_id"],
        "scope": "bad_god_evidential_prior_sensitivity_grid_not_proof",
        "checks": checks,
        "remaining_risks": [
            "prior intervals are stipulated for sensitivity only",
            "profiles have not been executed with likelihood intervals",
            "probability pressure remains unresolved",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid(
    ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_prior_sensitivity_grid: dict[str, Any] | None = None,
    evidential_evil_likelihood_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    scaffold_doc = (
        ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold
        or _build_ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold()
    )
    prior_grid_doc = (
        ontological_soundness_bad_god_evidential_prior_sensitivity_grid
        or _build_ontological_soundness_bad_god_evidential_prior_sensitivity_grid(scaffold_doc)
    )
    ledger_doc = evidential_evil_likelihood_ledger or _build_evidential_evil_likelihood_ledger()
    scaffold = scaffold_doc["scaffold"]
    prior_grid = prior_grid_doc["grid"]
    ledger = ledger_doc["ledger"]
    target_lane = next(
        row for row in scaffold["evaluation_lanes"]
        if row["probability_requirement_id"] == "likelihoods_quantified"
    )
    likelihood_cells = [
        {
            "evidence_dimension_id": row["evidence_dimension_id"],
            "hypothesis_id": row["hypothesis_id"],
            "lower": row["lower"],
            "midpoint": round((row["lower"] + row["upper"]) / 2, 6),
            "upper": row["upper"],
            "status": row["status"],
            "rationale": row["rationale"],
        }
        for row in ledger["likelihood_intervals"]
    ]
    evidence_dimension_ids = sorted({row["evidence_dimension_id"] for row in likelihood_cells})
    hypothesis_ids = sorted({row["hypothesis_id"] for row in likelihood_cells})
    return {
        "status": "contested",
        "grid": {
            "id": "ontological-soundness-bad-god-evidential-likelihood-sensitivity-grid-v0",
            "input_task_scaffold_id": scaffold["id"],
            "input_prior_grid_id": prior_grid["id"],
            "input_likelihood_ledger_id": ledger["id"],
            "target_task_id": scaffold["target_task_id"],
            "target_lane_id": target_lane["lane_id"],
            "target_requirement_id": target_lane["probability_requirement_id"],
            "retrieved_at": RETRIEVED_AT,
            "evidence_dimension_ids": evidence_dimension_ids,
            "hypothesis_ids": hypothesis_ids,
            "likelihood_cells": likelihood_cells,
            "prior_profile_projection_inputs": [
                {
                    "profile_id": profile["profile_id"],
                    "source_value": profile["source_value"],
                    "hypothesis_weight_ids": sorted(profile["weights"]),
                    "likelihood_cell_count": len(likelihood_cells),
                    "projection_status": "ready_not_executed",
                }
                for profile in prior_grid["normalized_prior_profiles"]
            ],
            "execution_state": {
                "likelihood_grid_recorded": True,
                "likelihood_grid_executed": False,
                "posterior_projection_executed": False,
                "probability_pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "The likelihood grid declares interval inputs and projection plans only. It "
                "does not multiply dimensions, collapse dependence, or resolve evidential "
                "probability pressure."
            ),
        },
        "warning": "Likelihood sensitivity grid is not an executed posterior model.",
    }


def _build_ontological_soundness_bad_god_evidential_likelihood_sensitivity_checks(
    ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_prior_sensitivity_grid: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid: dict[str, Any] | None = None,
    evidential_evil_likelihood_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    scaffold_doc = (
        ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold
        or _build_ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold()
    )
    prior_grid_doc = (
        ontological_soundness_bad_god_evidential_prior_sensitivity_grid
        or _build_ontological_soundness_bad_god_evidential_prior_sensitivity_grid(scaffold_doc)
    )
    ledger_doc = evidential_evil_likelihood_ledger or _build_evidential_evil_likelihood_ledger()
    grid_doc = (
        ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid
        or _build_ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid(
            scaffold_doc,
            prior_grid_doc,
            ledger_doc,
        )
    )
    scaffold = scaffold_doc["scaffold"]
    prior_grid = prior_grid_doc["grid"]
    ledger = ledger_doc["ledger"]
    grid = grid_doc["grid"]
    ledger_pairs = {
        (row["evidence_dimension_id"], row["hypothesis_id"])
        for row in ledger["likelihood_intervals"]
    }
    grid_pairs = {
        (row["evidence_dimension_id"], row["hypothesis_id"])
        for row in grid["likelihood_cells"]
    }
    projection_inputs = [
        row for row in grid["prior_profile_projection_inputs"]
        if row["projection_status"] == "ready_not_executed"
        and row["likelihood_cell_count"] == len(grid["likelihood_cells"])
    ]
    checks = [
        {
            "id": "check-task-scaffold-linked",
            "status": "complete"
            if grid["input_task_scaffold_id"] == scaffold["id"]
            and grid["target_task_id"] == scaffold["target_task_id"]
            and grid["target_requirement_id"] == "likelihoods_quantified"
            else "open",
            "input_task_scaffold_id": grid["input_task_scaffold_id"],
            "target_requirement_id": grid["target_requirement_id"],
        },
        {
            "id": "check-prior-grid-linked",
            "status": "complete" if grid["input_prior_grid_id"] == prior_grid["id"] else "open",
            "input_prior_grid_id": grid["input_prior_grid_id"],
            "prior_grid_id": prior_grid["id"],
        },
        {
            "id": "check-likelihood-ledger-linked",
            "status": "complete" if grid["input_likelihood_ledger_id"] == ledger["id"] else "open",
            "input_likelihood_ledger_id": grid["input_likelihood_ledger_id"],
            "likelihood_ledger_id": ledger["id"],
        },
        {
            "id": "check-likelihood-cells-cover-grid",
            "status": "complete" if ledger_pairs == grid_pairs else "open",
            "ledger_pair_count": len(ledger_pairs),
            "grid_pair_count": len(grid_pairs),
            "missing_pairs": sorted([list(pair) for pair in ledger_pairs - grid_pairs]),
        },
        {
            "id": "check-prior-profile-projections-ready",
            "status": "complete"
            if len(projection_inputs) == len(prior_grid["normalized_prior_profiles"])
            and len(projection_inputs) >= 3
            else "open",
            "projection_profile_ids": [row["profile_id"] for row in grid["prior_profile_projection_inputs"]],
            "ready_projection_count": len(projection_inputs),
        },
        {
            "id": "check-likelihood-grid-not-executed-or-promoted",
            "status": "contested"
            if grid_doc["status"] == "contested"
            and grid["execution_state"]["likelihood_grid_executed"] is False
            and grid["execution_state"]["proof_claim_allowed"] is False
            else "open",
            "execution_state": grid["execution_state"],
            "decision_rule": grid["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_task_id": grid["target_task_id"],
        "target_lane_id": grid["target_lane_id"],
        "target_requirement_id": grid["target_requirement_id"],
        "scope": "bad_god_evidential_likelihood_sensitivity_grid_not_proof",
        "checks": checks,
        "remaining_risks": [
            "likelihood intervals remain wide and contested",
            "dimension dependence has not been collapsed",
            "posterior projections remain unexecuted",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_response_cost_grid(
    ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid: dict[str, Any] | None = None,
    evidential_evil_likelihood_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    scaffold_doc = (
        ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold
        or _build_ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold()
    )
    likelihood_grid_doc = (
        ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid
        or _build_ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid(scaffold_doc)
    )
    ledger_doc = evidential_evil_likelihood_ledger or _build_evidential_evil_likelihood_ledger()
    scaffold = scaffold_doc["scaffold"]
    likelihood_grid = likelihood_grid_doc["grid"]
    ledger = ledger_doc["ledger"]
    target_lane = next(
        row for row in scaffold["evaluation_lanes"]
        if row["probability_requirement_id"] == "response_costs_declared"
    )
    response_cost_rows = [
        {
            "response_model_id": row["response_model_id"],
            "cost_ids": row["cost_ids"],
            "penalty_lower": row["penalty_interval"][0],
            "penalty_midpoint": round(sum(row["penalty_interval"]) / 2, 6),
            "penalty_upper": row["penalty_interval"][1],
            "status": row["status"],
        }
        for row in ledger["response_costs"]
    ]
    return {
        "status": "contested",
        "grid": {
            "id": "ontological-soundness-bad-god-evidential-response-cost-grid-v0",
            "input_task_scaffold_id": scaffold["id"],
            "input_likelihood_grid_id": likelihood_grid["id"],
            "input_likelihood_ledger_id": ledger["id"],
            "target_task_id": scaffold["target_task_id"],
            "target_lane_id": target_lane["lane_id"],
            "target_requirement_id": target_lane["probability_requirement_id"],
            "retrieved_at": RETRIEVED_AT,
            "response_cost_rows": response_cost_rows,
            "cost_projection_inputs": [
                {
                    "profile_id": row["profile_id"],
                    "likelihood_cell_count": row["likelihood_cell_count"],
                    "response_cost_count": len(response_cost_rows),
                    "projection_status": "ready_not_executed",
                }
                for row in likelihood_grid["prior_profile_projection_inputs"]
            ],
            "execution_state": {
                "response_cost_grid_recorded": True,
                "response_cost_grid_executed": False,
                "cost_adjusted_projection_executed": False,
                "probability_pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "The response-cost grid declares penalty intervals for candidate responses. "
                "It does not apply the penalties or resolve evidential probability pressure."
            ),
        },
        "warning": "Response-cost grid is not an executed or successful theodicy.",
    }


def _build_ontological_soundness_bad_god_evidential_response_cost_checks(
    ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_response_cost_grid: dict[str, Any] | None = None,
    evidential_evil_likelihood_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    scaffold_doc = (
        ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold
        or _build_ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold()
    )
    likelihood_grid_doc = (
        ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid
        or _build_ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid(scaffold_doc)
    )
    ledger_doc = evidential_evil_likelihood_ledger or _build_evidential_evil_likelihood_ledger()
    grid_doc = (
        ontological_soundness_bad_god_evidential_response_cost_grid
        or _build_ontological_soundness_bad_god_evidential_response_cost_grid(
            scaffold_doc,
            likelihood_grid_doc,
            ledger_doc,
        )
    )
    scaffold = scaffold_doc["scaffold"]
    likelihood_grid = likelihood_grid_doc["grid"]
    ledger = ledger_doc["ledger"]
    grid = grid_doc["grid"]
    ledger_response_ids = {row["response_model_id"] for row in ledger["response_costs"]}
    grid_response_ids = {row["response_model_id"] for row in grid["response_cost_rows"]}
    ready_projection_inputs = [
        row for row in grid["cost_projection_inputs"]
        if row["projection_status"] == "ready_not_executed"
        and row["response_cost_count"] == len(grid["response_cost_rows"])
    ]
    checks = [
        {
            "id": "check-task-scaffold-linked",
            "status": "complete"
            if grid["input_task_scaffold_id"] == scaffold["id"]
            and grid["target_task_id"] == scaffold["target_task_id"]
            and grid["target_requirement_id"] == "response_costs_declared"
            else "open",
            "input_task_scaffold_id": grid["input_task_scaffold_id"],
            "target_requirement_id": grid["target_requirement_id"],
        },
        {
            "id": "check-likelihood-grid-linked",
            "status": "complete" if grid["input_likelihood_grid_id"] == likelihood_grid["id"] else "open",
            "input_likelihood_grid_id": grid["input_likelihood_grid_id"],
            "likelihood_grid_id": likelihood_grid["id"],
        },
        {
            "id": "check-likelihood-ledger-linked",
            "status": "complete" if grid["input_likelihood_ledger_id"] == ledger["id"] else "open",
            "input_likelihood_ledger_id": grid["input_likelihood_ledger_id"],
            "likelihood_ledger_id": ledger["id"],
        },
        {
            "id": "check-response-costs-covered",
            "status": "complete" if ledger_response_ids == grid_response_ids else "open",
            "ledger_response_ids": sorted(ledger_response_ids),
            "grid_response_ids": sorted(grid_response_ids),
            "missing_response_ids": sorted(ledger_response_ids - grid_response_ids),
        },
        {
            "id": "check-cost-projections-ready",
            "status": "complete"
            if len(ready_projection_inputs) == len(likelihood_grid["prior_profile_projection_inputs"])
            and len(ready_projection_inputs) >= 3
            else "open",
            "projection_profile_ids": [row["profile_id"] for row in grid["cost_projection_inputs"]],
            "ready_projection_count": len(ready_projection_inputs),
        },
        {
            "id": "check-response-cost-grid-not-executed-or-promoted",
            "status": "contested"
            if grid_doc["status"] == "contested"
            and grid["execution_state"]["response_cost_grid_executed"] is False
            and grid["execution_state"]["proof_claim_allowed"] is False
            else "open",
            "execution_state": grid["execution_state"],
            "decision_rule": grid["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_task_id": grid["target_task_id"],
        "target_lane_id": grid["target_lane_id"],
        "target_requirement_id": grid["target_requirement_id"],
        "scope": "bad_god_evidential_response_cost_grid_not_proof",
        "checks": checks,
        "remaining_risks": [
            "response-cost penalties are candidate intervals only",
            "cost-adjusted projections remain unexecuted",
            "moral-reasoning preservation remains open",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_rival_comparison_grid(
    ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_response_cost_grid: dict[str, Any] | None = None,
    rival_necessary_parity_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    scaffold_doc = (
        ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold
        or _build_ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold()
    )
    likelihood_grid_doc = (
        ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid
        or _build_ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid(scaffold_doc)
    )
    response_cost_grid_doc = (
        ontological_soundness_bad_god_evidential_response_cost_grid
        or _build_ontological_soundness_bad_god_evidential_response_cost_grid(scaffold_doc, likelihood_grid_doc)
    )
    rival_checks = rival_necessary_parity_checks or _build_rival_necessary_parity_checks()
    scaffold = scaffold_doc["scaffold"]
    likelihood_grid = likelihood_grid_doc["grid"]
    response_cost_grid = response_cost_grid_doc["grid"]
    target_lane = next(
        row for row in scaffold["evaluation_lanes"]
        if row["probability_requirement_id"] == "rival_likelihoods_compared"
    )
    rival_hypothesis_id = "non_theistic_indifference"
    rival_likelihood_rows = [
        {
            "evidence_dimension_id": row["evidence_dimension_id"],
            "rival_hypothesis_id": row["hypothesis_id"],
            "lower": row["lower"],
            "midpoint": row["midpoint"],
            "upper": row["upper"],
            "status": row["status"],
            "comparison_status": "ready_not_executed",
        }
        for row in likelihood_grid["likelihood_cells"]
        if row["hypothesis_id"] == rival_hypothesis_id
    ]
    unresolved_rival_ids: list[str] = []
    for row in rival_checks["checks"]:
        if row["id"] == "check-rival-parity-not-discharged":
            unresolved_rival_ids = row["unresolved_rival_ids"]
    return {
        "status": "contested",
        "grid": {
            "id": "ontological-soundness-bad-god-evidential-rival-comparison-grid-v0",
            "input_task_scaffold_id": scaffold["id"],
            "input_likelihood_grid_id": likelihood_grid["id"],
            "input_response_cost_grid_id": response_cost_grid["id"],
            "input_rival_parity_scope": rival_checks["scope"],
            "target_task_id": scaffold["target_task_id"],
            "target_lane_id": target_lane["lane_id"],
            "target_requirement_id": target_lane["probability_requirement_id"],
            "retrieved_at": RETRIEVED_AT,
            "rival_hypothesis_id": rival_hypothesis_id,
            "required_evidence_dimension_ids": likelihood_grid["evidence_dimension_ids"],
            "rival_likelihood_rows": rival_likelihood_rows,
            "necessary_rival_bridge_rows": [
                {
                    "rival_id": rival_id,
                    "source_artifact": "rival-necessary-parity-checks.json",
                    "bridge_status": "unresolved_not_executed",
                }
                for rival_id in unresolved_rival_ids
            ],
            "cost_projection_input_count": len(response_cost_grid["cost_projection_inputs"]),
            "execution_state": {
                "rival_comparison_grid_recorded": True,
                "rival_comparison_executed": False,
                "necessary_rival_bridge_executed": False,
                "probability_pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Rival likelihood comparison remains preparatory until non-theistic and "
                "necessary-ultimate rivals are evaluated against the same cost-adjusted "
                "projection rules."
            ),
        },
        "warning": "Rival comparison grid is not a uniqueness proof.",
    }


def _build_ontological_soundness_bad_god_evidential_rival_comparison_checks(
    ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_response_cost_grid: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_rival_comparison_grid: dict[str, Any] | None = None,
    rival_necessary_parity_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    scaffold_doc = (
        ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold
        or _build_ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold()
    )
    likelihood_grid_doc = (
        ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid
        or _build_ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid(scaffold_doc)
    )
    response_cost_grid_doc = (
        ontological_soundness_bad_god_evidential_response_cost_grid
        or _build_ontological_soundness_bad_god_evidential_response_cost_grid(scaffold_doc, likelihood_grid_doc)
    )
    rival_checks = rival_necessary_parity_checks or _build_rival_necessary_parity_checks()
    grid_doc = (
        ontological_soundness_bad_god_evidential_rival_comparison_grid
        or _build_ontological_soundness_bad_god_evidential_rival_comparison_grid(
            scaffold_doc,
            likelihood_grid_doc,
            response_cost_grid_doc,
            rival_checks,
        )
    )
    scaffold = scaffold_doc["scaffold"]
    likelihood_grid = likelihood_grid_doc["grid"]
    response_cost_grid = response_cost_grid_doc["grid"]
    grid = grid_doc["grid"]
    rival_dimension_ids = {row["evidence_dimension_id"] for row in grid["rival_likelihood_rows"]}
    required_dimension_ids = set(grid["required_evidence_dimension_ids"])
    checks = [
        {
            "id": "check-task-scaffold-linked",
            "status": "complete"
            if grid["input_task_scaffold_id"] == scaffold["id"]
            and grid["target_task_id"] == scaffold["target_task_id"]
            and grid["target_requirement_id"] == "rival_likelihoods_compared"
            else "open",
            "input_task_scaffold_id": grid["input_task_scaffold_id"],
            "target_requirement_id": grid["target_requirement_id"],
        },
        {
            "id": "check-response-cost-grid-linked",
            "status": "complete" if grid["input_response_cost_grid_id"] == response_cost_grid["id"] else "open",
            "input_response_cost_grid_id": grid["input_response_cost_grid_id"],
            "response_cost_grid_id": response_cost_grid["id"],
        },
        {
            "id": "check-likelihood-grid-linked",
            "status": "complete" if grid["input_likelihood_grid_id"] == likelihood_grid["id"] else "open",
            "input_likelihood_grid_id": grid["input_likelihood_grid_id"],
            "likelihood_grid_id": likelihood_grid["id"],
        },
        {
            "id": "check-non-theistic-rival-covers-evidence-dimensions",
            "status": "complete" if required_dimension_ids == rival_dimension_ids else "open",
            "required_evidence_dimension_ids": sorted(required_dimension_ids),
            "rival_evidence_dimension_ids": sorted(rival_dimension_ids),
            "missing_dimension_ids": sorted(required_dimension_ids - rival_dimension_ids),
        },
        {
            "id": "check-necessary-rival-parity-linked",
            "status": "complete"
            if grid["input_rival_parity_scope"] == rival_checks["scope"]
            and grid["necessary_rival_bridge_rows"]
            else "open",
            "input_rival_parity_scope": grid["input_rival_parity_scope"],
            "bridge_rival_ids": [row["rival_id"] for row in grid["necessary_rival_bridge_rows"]],
        },
        {
            "id": "check-rival-comparison-not-executed-or-promoted",
            "status": "contested"
            if grid_doc["status"] == "contested"
            and grid["execution_state"]["rival_comparison_executed"] is False
            and grid["execution_state"]["proof_claim_allowed"] is False
            else "open",
            "execution_state": grid["execution_state"],
            "decision_rule": grid["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_task_id": grid["target_task_id"],
        "target_lane_id": grid["target_lane_id"],
        "target_requirement_id": grid["target_requirement_id"],
        "scope": "bad_god_evidential_rival_comparison_grid_not_proof",
        "checks": checks,
        "remaining_risks": [
            "non-theistic rival comparison is not executed",
            "necessary rival parity remains unresolved",
            "rival comparison does not discharge bad-god pressure",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_probability_execution_packet(
    ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_prior_sensitivity_grid: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_response_cost_grid: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_rival_comparison_grid: dict[str, Any] | None = None,
) -> dict[str, Any]:
    scaffold_doc = (
        ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold
        or _build_ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold()
    )
    prior_grid_doc = (
        ontological_soundness_bad_god_evidential_prior_sensitivity_grid
        or _build_ontological_soundness_bad_god_evidential_prior_sensitivity_grid(scaffold_doc)
    )
    likelihood_grid_doc = (
        ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid
        or _build_ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid(
            scaffold_doc,
            prior_grid_doc,
        )
    )
    response_cost_grid_doc = (
        ontological_soundness_bad_god_evidential_response_cost_grid
        or _build_ontological_soundness_bad_god_evidential_response_cost_grid(
            scaffold_doc,
            likelihood_grid_doc,
        )
    )
    rival_comparison_grid_doc = (
        ontological_soundness_bad_god_evidential_rival_comparison_grid
        or _build_ontological_soundness_bad_god_evidential_rival_comparison_grid(
            scaffold_doc,
            likelihood_grid_doc,
            response_cost_grid_doc,
        )
    )
    scaffold = scaffold_doc["scaffold"]
    lane_grids = [
        prior_grid_doc["grid"],
        likelihood_grid_doc["grid"],
        response_cost_grid_doc["grid"],
        rival_comparison_grid_doc["grid"],
    ]
    return {
        "status": "contested",
        "packet": {
            "id": "ontological-soundness-bad-god-evidential-probability-execution-packet-v0",
            "target_task_id": scaffold["target_task_id"],
            "input_task_scaffold_id": scaffold["id"],
            "input_grid_ids": [grid["id"] for grid in lane_grids],
            "retrieved_at": RETRIEVED_AT,
            "execution_steps": [
                {
                    "step_id": f"execute-{grid['target_requirement_id']}",
                    "lane_id": grid["target_lane_id"],
                    "target_requirement_id": grid["target_requirement_id"],
                    "input_grid_id": grid["id"],
                    "step_status": "ready_not_executed",
                }
                for grid in lane_grids
            ],
            "verifier_commands": [
                "rtk env PYTHONPATH=src python3 -m pytest tests/test_godproof.py -q",
                "rtk env PYTHONPATH=src python3 -m pytest -q",
            ],
            "execution_state": {
                "execution_packet_recorded": True,
                "lane_grids_executed": False,
                "posterior_projection_executed": False,
                "probability_pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "The packet authorizes a future deterministic run order, but the evidential "
                "probability task remains open until projections are executed and contested "
                "checks close without promoting proof prematurely."
            ),
        },
        "warning": "Execution packet is a run plan, not an executed posterior or proof.",
    }


def _build_ontological_soundness_bad_god_evidential_probability_execution_checks(
    ontological_soundness_bad_god_evidential_probability_execution_packet: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_prior_sensitivity_grid: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_prior_sensitivity_checks: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_likelihood_sensitivity_checks: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_response_cost_grid: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_response_cost_checks: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_rival_comparison_grid: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_rival_comparison_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    scaffold_doc = (
        ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold
        or _build_ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold()
    )
    prior_grid_doc = (
        ontological_soundness_bad_god_evidential_prior_sensitivity_grid
        or _build_ontological_soundness_bad_god_evidential_prior_sensitivity_grid(scaffold_doc)
    )
    prior_checks = (
        ontological_soundness_bad_god_evidential_prior_sensitivity_checks
        or _build_ontological_soundness_bad_god_evidential_prior_sensitivity_checks(scaffold_doc, prior_grid_doc)
    )
    likelihood_grid_doc = (
        ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid
        or _build_ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid(scaffold_doc, prior_grid_doc)
    )
    likelihood_checks = (
        ontological_soundness_bad_god_evidential_likelihood_sensitivity_checks
        or _build_ontological_soundness_bad_god_evidential_likelihood_sensitivity_checks(
            scaffold_doc,
            prior_grid_doc,
            likelihood_grid_doc,
        )
    )
    response_cost_grid_doc = (
        ontological_soundness_bad_god_evidential_response_cost_grid
        or _build_ontological_soundness_bad_god_evidential_response_cost_grid(scaffold_doc, likelihood_grid_doc)
    )
    response_cost_checks = (
        ontological_soundness_bad_god_evidential_response_cost_checks
        or _build_ontological_soundness_bad_god_evidential_response_cost_checks(
            scaffold_doc,
            likelihood_grid_doc,
            response_cost_grid_doc,
        )
    )
    rival_comparison_grid_doc = (
        ontological_soundness_bad_god_evidential_rival_comparison_grid
        or _build_ontological_soundness_bad_god_evidential_rival_comparison_grid(
            scaffold_doc,
            likelihood_grid_doc,
            response_cost_grid_doc,
        )
    )
    rival_comparison_checks = (
        ontological_soundness_bad_god_evidential_rival_comparison_checks
        or _build_ontological_soundness_bad_god_evidential_rival_comparison_checks(
            scaffold_doc,
            likelihood_grid_doc,
            response_cost_grid_doc,
            rival_comparison_grid_doc,
        )
    )
    packet_doc = (
        ontological_soundness_bad_god_evidential_probability_execution_packet
        or _build_ontological_soundness_bad_god_evidential_probability_execution_packet(
            scaffold_doc,
            prior_grid_doc,
            likelihood_grid_doc,
            response_cost_grid_doc,
            rival_comparison_grid_doc,
        )
    )
    packet = packet_doc["packet"]
    grid_ids = [
        prior_grid_doc["grid"]["id"],
        likelihood_grid_doc["grid"]["id"],
        response_cost_grid_doc["grid"]["id"],
        rival_comparison_grid_doc["grid"]["id"],
    ]
    lane_check_scopes = [
        prior_checks["scope"],
        likelihood_checks["scope"],
        response_cost_checks["scope"],
        rival_comparison_checks["scope"],
    ]
    expected_lane_ids = [
        "lane-priors_declared",
        "lane-likelihoods_quantified",
        "lane-response_costs_declared",
        "lane-rival_likelihoods_compared",
    ]
    actual_lane_ids = [row["lane_id"] for row in packet["execution_steps"]]
    checks = [
        {
            "id": "check-all-lane-grids-linked",
            "status": "complete" if packet["input_grid_ids"] == grid_ids else "open",
            "packet_input_grid_ids": packet["input_grid_ids"],
            "expected_grid_ids": grid_ids,
        },
        {
            "id": "check-all-lane-checks-linked",
            "status": "complete" if all(scope.endswith("_not_proof") for scope in lane_check_scopes) else "open",
            "lane_check_scopes": lane_check_scopes,
        },
        {
            "id": "check-execution-order-complete",
            "status": "complete" if actual_lane_ids == expected_lane_ids else "open",
            "actual_lane_ids": actual_lane_ids,
            "expected_lane_ids": expected_lane_ids,
        },
        {
            "id": "check-execution-packet-not-run-or-promoted",
            "status": "contested"
            if packet_doc["status"] == "contested"
            and packet["execution_state"]["posterior_projection_executed"] is False
            and packet["execution_state"]["proof_claim_allowed"] is False
            else "open",
            "execution_state": packet["execution_state"],
            "decision_rule": packet["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_task_id": packet["target_task_id"],
        "scope": "bad_god_evidential_probability_execution_packet_not_proof",
        "checks": checks,
        "remaining_risks": [
            "posterior projection is not executed",
            "lane checks remain contested by design",
            "evidential probability pressure is not resolved",
        ],
    }


def _response_cost_penalties_by_hypothesis(
    response_cost_rows: list[dict[str, Any]],
) -> dict[str, float]:
    response_to_hypothesis = {
        "free_will_defense": "classical_theism",
        "greater_good_unknown": "classical_theism",
        "soul_making_theodicy": "soul_making_theism",
        "skeptical_theism": "skeptical_theism_compatible_theism",
    }
    penalties: dict[str, list[float]] = {}
    for row in response_cost_rows:
        hypothesis_id = response_to_hypothesis.get(row["response_model_id"])
        if hypothesis_id:
            penalties.setdefault(hypothesis_id, []).append(row["penalty_midpoint"])
    return {
        hypothesis_id: round(max(values), 6)
        for hypothesis_id, values in penalties.items()
    }


def _build_ontological_soundness_bad_god_evidential_posterior_projection_results(
    ontological_soundness_bad_god_evidential_probability_execution_packet: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_prior_sensitivity_grid: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_response_cost_grid: dict[str, Any] | None = None,
) -> dict[str, Any]:
    prior_grid_doc = (
        ontological_soundness_bad_god_evidential_prior_sensitivity_grid
        or _build_ontological_soundness_bad_god_evidential_prior_sensitivity_grid()
    )
    likelihood_grid_doc = (
        ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid
        or _build_ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid(
            ontological_soundness_bad_god_evidential_prior_sensitivity_grid=prior_grid_doc
        )
    )
    response_cost_grid_doc = (
        ontological_soundness_bad_god_evidential_response_cost_grid
        or _build_ontological_soundness_bad_god_evidential_response_cost_grid(
            ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid=likelihood_grid_doc
        )
    )
    packet_doc = (
        ontological_soundness_bad_god_evidential_probability_execution_packet
        or _build_ontological_soundness_bad_god_evidential_probability_execution_packet(
            ontological_soundness_bad_god_evidential_prior_sensitivity_grid=prior_grid_doc,
            ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid=likelihood_grid_doc,
            ontological_soundness_bad_god_evidential_response_cost_grid=response_cost_grid_doc,
        )
    )
    prior_grid = prior_grid_doc["grid"]
    likelihood_grid = likelihood_grid_doc["grid"]
    response_cost_grid = response_cost_grid_doc["grid"]
    packet = packet_doc["packet"]
    likelihood_midpoints: dict[str, list[float]] = {}
    for row in likelihood_grid["likelihood_cells"]:
        likelihood_midpoints.setdefault(row["hypothesis_id"], []).append(row["midpoint"])
    average_likelihoods = {
        hypothesis_id: round(sum(values) / len(values), 6)
        for hypothesis_id, values in likelihood_midpoints.items()
    }
    penalties = _response_cost_penalties_by_hypothesis(response_cost_grid["response_cost_rows"])
    projection_results = []
    for profile in prior_grid["normalized_prior_profiles"]:
        cost_adjusted_likelihoods = {
            hypothesis_id: round(max(0.000001, likelihood * (1 - penalties.get(hypothesis_id, 0.0))), 6)
            for hypothesis_id, likelihood in average_likelihoods.items()
        }
        posterior = _posterior(profile["weights"], cost_adjusted_likelihoods)
        projection_results.append({
            "profile_id": profile["profile_id"],
            "projection_status": "executed_candidate",
            "prior_weights": profile["weights"],
            "average_likelihoods": average_likelihoods,
            "response_cost_penalties": penalties,
            "cost_adjusted_likelihoods": cost_adjusted_likelihoods,
            "posterior": posterior,
            "top_hypothesis_id": max(posterior, key=posterior.get),
        })
    return {
        "status": "contested",
        "results": {
            "id": "ontological-soundness-bad-god-evidential-posterior-projection-results-v0",
            "input_execution_packet_id": packet["id"],
            "input_prior_grid_id": prior_grid["id"],
            "input_likelihood_grid_id": likelihood_grid["id"],
            "input_response_cost_grid_id": response_cost_grid["id"],
            "target_task_id": packet["target_task_id"],
            "projection_mode": "midpoint_average_cost_adjusted_candidate",
            "retrieved_at": RETRIEVED_AT,
            "projection_results": projection_results,
            "execution_state": {
                "posterior_projection_executed": True,
                "projection_is_candidate_only": True,
                "probability_pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Candidate posterior projections expose sensitivity. They do not resolve "
                "evidential evil because intervals are wide, dependence remains contested, "
                "and live objections remain undispatched."
            ),
        },
        "warning": "Posterior projection results are sensitivity evidence only, not proof.",
    }


def _build_ontological_soundness_bad_god_evidential_posterior_projection_checks(
    ontological_soundness_bad_god_evidential_posterior_projection_results: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_probability_execution_packet: dict[str, Any] | None = None,
) -> dict[str, Any]:
    packet_doc = (
        ontological_soundness_bad_god_evidential_probability_execution_packet
        or _build_ontological_soundness_bad_god_evidential_probability_execution_packet()
    )
    results_doc = (
        ontological_soundness_bad_god_evidential_posterior_projection_results
        or _build_ontological_soundness_bad_god_evidential_posterior_projection_results(packet_doc)
    )
    packet = packet_doc["packet"]
    results = results_doc["results"]
    normalized_result_ids = [
        row["profile_id"] for row in results["projection_results"]
        if abs(sum(row["posterior"].values()) - 1.0) < 1e-6
    ]
    checks = [
        {
            "id": "check-execution-packet-linked",
            "status": "complete" if results["input_execution_packet_id"] == packet["id"] else "open",
            "input_execution_packet_id": results["input_execution_packet_id"],
            "execution_packet_id": packet["id"],
        },
        {
            "id": "check-projection-results-present",
            "status": "complete" if len(results["projection_results"]) >= 3 else "open",
            "projection_profile_ids": [row["profile_id"] for row in results["projection_results"]],
        },
        {
            "id": "check-posteriors-normalized",
            "status": "complete" if len(normalized_result_ids) == len(results["projection_results"]) else "open",
            "normalized_result_ids": normalized_result_ids,
        },
        {
            "id": "check-projection-remains-contested",
            "status": "contested"
            if results_doc["status"] == "contested"
            and results["execution_state"]["posterior_projection_executed"] is True
            and results["execution_state"]["probability_pressure_resolved"] is False
            and results["execution_state"]["proof_claim_allowed"] is False
            else "open",
            "execution_state": results["execution_state"],
            "decision_rule": results["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_task_id": results["target_task_id"],
        "scope": "bad_god_evidential_posterior_projection_results_not_proof",
        "checks": checks,
        "remaining_risks": [
            "projection uses midpoint averaging rather than calibrated dependence",
            "response costs are candidate penalties",
            "posterior output does not discharge live evil and hiddenness objections",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_projection_outcome_review(
    ontological_soundness_bad_god_evidential_posterior_projection_results: dict[str, Any] | None = None,
) -> dict[str, Any]:
    results_doc = (
        ontological_soundness_bad_god_evidential_posterior_projection_results
        or _build_ontological_soundness_bad_god_evidential_posterior_projection_results()
    )
    results = results_doc["results"]
    outcome_rows = []
    top_hypothesis_tally: dict[str, int] = {}
    for projection_row in results["projection_results"]:
        ranked_posteriors = sorted(
            projection_row["posterior"].items(),
            key=lambda item: item[1],
            reverse=True,
        )
        top_hypothesis_id, top_posterior = ranked_posteriors[0]
        runner_up_hypothesis_id, runner_up_posterior = ranked_posteriors[1]
        top_hypothesis_tally[top_hypothesis_id] = top_hypothesis_tally.get(top_hypothesis_id, 0) + 1
        outcome_rows.append({
            "profile_id": projection_row["profile_id"],
            "projection_status": projection_row["projection_status"],
            "top_hypothesis_id": top_hypothesis_id,
            "top_posterior": top_posterior,
            "runner_up_hypothesis_id": runner_up_hypothesis_id,
            "runner_up_posterior": runner_up_posterior,
            "margin": round(top_posterior - runner_up_posterior, 6),
            "result_status": "candidate_pressure_recorded",
        })
    candidate_result = (
        "non_theistic_indifference_top_in_all_profiles"
        if top_hypothesis_tally == {"non_theistic_indifference": len(outcome_rows)}
        else "mixed_candidate_projection_outcomes"
    )
    return {
        "status": "contested",
        "review": {
            "id": "ontological-soundness-bad-god-evidential-projection-outcome-review-v0",
            "input_projection_results_id": results["id"],
            "target_task_id": results["target_task_id"],
            "target_pressure_test_id": "evidential-probability-pressure",
            "projection_mode": results["projection_mode"],
            "retrieved_at": RETRIEVED_AT,
            "projection_count": len(results["projection_results"]),
            "top_hypothesis_tally": top_hypothesis_tally,
            "outcome_rows": outcome_rows,
            "pressure_assessment": {
                "evidential_probability_pressure_status": "strengthened_not_resolved",
                "candidate_result": candidate_result,
                "probability_pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "execution_state": {
                "outcome_review_recorded": True,
                "pressure_task_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Outcome review records candidate pressure from posterior projections. "
                "It does not resolve the evidential-probability task because calibration, "
                "independence, response-cost, and rival-hypothesis objections remain live."
            ),
        },
        "warning": "Outcome review records pressure only and is not a proof claim.",
    }


def _build_ontological_soundness_bad_god_evidential_projection_outcome_checks(
    ontological_soundness_bad_god_evidential_posterior_projection_results: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_projection_outcome_review: dict[str, Any] | None = None,
) -> dict[str, Any]:
    results_doc = (
        ontological_soundness_bad_god_evidential_posterior_projection_results
        or _build_ontological_soundness_bad_god_evidential_posterior_projection_results()
    )
    review_doc = (
        ontological_soundness_bad_god_evidential_projection_outcome_review
        or _build_ontological_soundness_bad_god_evidential_projection_outcome_review(results_doc)
    )
    results = results_doc["results"]
    review = review_doc["review"]
    tally_total = sum(review["top_hypothesis_tally"].values())
    checks = [
        {
            "id": "check-posterior-projection-linked",
            "status": "complete" if review["input_projection_results_id"] == results["id"] else "open",
            "input_projection_results_id": review["input_projection_results_id"],
            "projection_results_id": results["id"],
        },
        {
            "id": "check-outcome-rows-cover-projections",
            "status": "complete" if len(review["outcome_rows"]) == len(results["projection_results"]) else "open",
            "outcome_profile_ids": [row["profile_id"] for row in review["outcome_rows"]],
            "projection_profile_ids": [row["profile_id"] for row in results["projection_results"]],
        },
        {
            "id": "check-top-hypothesis-tally-recorded",
            "status": "complete" if tally_total == len(review["outcome_rows"]) else "open",
            "top_hypothesis_tally": review["top_hypothesis_tally"],
            "tally_total": tally_total,
        },
        {
            "id": "check-pressure-remains-unresolved",
            "status": "contested"
            if review["pressure_assessment"]["probability_pressure_resolved"] is False
            and review["execution_state"]["pressure_task_resolved"] is False
            else "open",
            "pressure_assessment": review["pressure_assessment"],
        },
        {
            "id": "check-outcome-review-not-promoted-to-proof",
            "status": "contested"
            if review_doc["status"] == "contested"
            and review["execution_state"]["proof_evidence_materialized"] is False
            and review["execution_state"]["proof_claim_allowed"] is False
            else "open",
            "execution_state": review["execution_state"],
            "decision_rule": review["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_task_id": review["target_task_id"],
        "scope": "bad_god_evidential_projection_outcome_review_not_proof",
        "checks": checks,
        "remaining_risks": [
            "non-theistic candidate pressure is recorded but not adjudicated",
            "posterior projection inputs remain candidate calibrations",
            "bad-god and hiddenness objections remain live under the soundness blocker",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_projection_remediation_plan(
    ontological_soundness_bad_god_evidential_projection_outcome_review: dict[str, Any] | None = None,
) -> dict[str, Any]:
    review_doc = (
        ontological_soundness_bad_god_evidential_projection_outcome_review
        or _build_ontological_soundness_bad_god_evidential_projection_outcome_review()
    )
    review = review_doc["review"]
    remediation_items = [
        {
            "remediation_id": "remediate-calibration-intervals",
            "remediation_category": "calibration",
            "source_risk": "posterior projection inputs remain candidate calibrations",
            "required_action": "replace midpoint priors and likelihoods with sourced interval calibration",
            "required_output": "calibrated interval grid with source-backed uncertainty bounds",
            "work_status": "queued_not_executed",
            "proof_evidence_materialized": False,
        },
        {
            "remediation_id": "remediate-dependence-model",
            "remediation_category": "dependence",
            "source_risk": "projection uses independent midpoint averaging",
            "required_action": "model dependence among evil, hiddenness, and response-cost evidence",
            "required_output": "dependence-aware posterior sensitivity model",
            "work_status": "queued_not_executed",
            "proof_evidence_materialized": False,
        },
        {
            "remediation_id": "remediate-response-cost-penalties",
            "remediation_category": "response_cost",
            "source_risk": "response costs are candidate penalties",
            "required_action": "audit theodicy and defense costs against live objections",
            "required_output": "adjudicated response-cost ledger with objection coverage",
            "work_status": "queued_not_executed",
            "proof_evidence_materialized": False,
        },
        {
            "remediation_id": "remediate-rival-hypothesis-coverage",
            "remediation_category": "rival_hypothesis",
            "source_risk": "non-theistic candidate pressure is recorded but not adjudicated",
            "required_action": "compare rival hypotheses under the same calibrated evidence bundle",
            "required_output": "rival-hypothesis adjudication table for the evidential pressure task",
            "work_status": "queued_not_executed",
            "proof_evidence_materialized": False,
        },
    ]
    return {
        "status": "contested",
        "plan": {
            "id": "ontological-soundness-bad-god-evidential-projection-remediation-plan-v0",
            "input_outcome_review_id": review["id"],
            "target_task_id": review["target_task_id"],
            "target_pressure_test_id": review["target_pressure_test_id"],
            "source_candidate_result": review["pressure_assessment"]["candidate_result"],
            "retrieved_at": RETRIEVED_AT,
            "remediation_items": remediation_items,
            "execution_state": {
                "remediation_plan_recorded": True,
                "remediation_executed": False,
                "probability_pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Remediation tasks identify the next evidential work needed after projection "
                "outcome review. They are queued work, not executed calibration or proof."
            ),
        },
        "warning": "Remediation plan is queued work only and cannot authorize a proof claim.",
    }


def _build_ontological_soundness_bad_god_evidential_projection_remediation_checks(
    ontological_soundness_bad_god_evidential_projection_outcome_review: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_projection_remediation_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    review_doc = (
        ontological_soundness_bad_god_evidential_projection_outcome_review
        or _build_ontological_soundness_bad_god_evidential_projection_outcome_review()
    )
    plan_doc = (
        ontological_soundness_bad_god_evidential_projection_remediation_plan
        or _build_ontological_soundness_bad_god_evidential_projection_remediation_plan(review_doc)
    )
    review = review_doc["review"]
    plan = plan_doc["plan"]
    categories = {row["remediation_category"] for row in plan["remediation_items"]}
    expected_categories = {"calibration", "dependence", "response_cost", "rival_hypothesis"}
    checks = [
        {
            "id": "check-outcome-review-linked",
            "status": "complete" if plan["input_outcome_review_id"] == review["id"] else "open",
            "input_outcome_review_id": plan["input_outcome_review_id"],
            "outcome_review_id": review["id"],
        },
        {
            "id": "check-remediation-items-cover-open-risks",
            "status": "complete" if categories == expected_categories else "open",
            "remediation_categories": sorted(categories),
            "expected_categories": sorted(expected_categories),
        },
        {
            "id": "check-remediation-items-not-executed",
            "status": "complete"
            if all(row["work_status"] == "queued_not_executed" for row in plan["remediation_items"])
            and all(row["proof_evidence_materialized"] is False for row in plan["remediation_items"])
            else "open",
            "work_statuses": [row["work_status"] for row in plan["remediation_items"]],
        },
        {
            "id": "check-pressure-still-unresolved",
            "status": "contested"
            if plan["execution_state"]["probability_pressure_resolved"] is False
            and review["pressure_assessment"]["probability_pressure_resolved"] is False
            else "open",
            "execution_state": plan["execution_state"],
        },
        {
            "id": "check-remediation-plan-not-proof",
            "status": "contested"
            if plan_doc["status"] == "contested"
            and plan["execution_state"]["proof_evidence_materialized"] is False
            and plan["execution_state"]["proof_claim_allowed"] is False
            else "open",
            "execution_state": plan["execution_state"],
            "decision_rule": plan["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_task_id": plan["target_task_id"],
        "scope": "bad_god_evidential_projection_remediation_plan_not_proof",
        "checks": checks,
        "remaining_risks": [
            "remediation items are queued but not executed",
            "calibration and dependence work have not produced adjudicated evidence",
            "evidential probability pressure remains unresolved",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_registry(
    ontological_soundness_bad_god_evidential_projection_remediation_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    plan_doc = (
        ontological_soundness_bad_god_evidential_projection_remediation_plan
        or _build_ontological_soundness_bad_god_evidential_projection_remediation_plan()
    )
    plan = plan_doc["plan"]
    calibration_item = next(
        row for row in plan["remediation_items"]
        if row["remediation_id"] == "remediate-calibration-intervals"
    )
    source_families = [
        {
            "source_family_id": "analytic_philosophy",
            "domain": "modal and conceptual argument calibration",
            "calibration_role": "estimate how much premise support survives parody and coherence objections",
            "required_for_interval_calibration": True,
            "collection_status": "scoped_not_ingested",
        },
        {
            "source_family_id": "philosophy_of_religion",
            "domain": "theodicy, hiddenness, and divine-attribute dispute calibration",
            "calibration_role": "bound live expert disagreement around evidential evil and hiddenness pressure",
            "required_for_interval_calibration": True,
            "collection_status": "scoped_not_ingested",
        },
        {
            "source_family_id": "probability_theory",
            "domain": "Bayesian and imprecise-probability method calibration",
            "calibration_role": "replace single midpoints with interval and sensitivity rules",
            "required_for_interval_calibration": True,
            "collection_status": "scoped_not_ingested",
        },
        {
            "source_family_id": "empirical_suffering_data",
            "domain": "evil, suffering, and preventable-harm case-rate calibration",
            "calibration_role": "ground likelihood intervals in empirical case families",
            "required_for_interval_calibration": True,
            "collection_status": "scoped_not_ingested",
        },
        {
            "source_family_id": "religious_experience_hiddenness_data",
            "domain": "divine hiddenness, religious experience, and nonbelief calibration",
            "calibration_role": "bound hiddenness likelihoods across theistic and non-theistic hypotheses",
            "required_for_interval_calibration": True,
            "collection_status": "scoped_not_ingested",
        },
        {
            "source_family_id": "comparative_theology",
            "domain": "cross-tradition God-concept and rival-hypothesis calibration",
            "calibration_role": "avoid overfitting one tradition when calibrating target attributes",
            "required_for_interval_calibration": True,
            "collection_status": "scoped_not_ingested",
        },
    ]
    return {
        "status": "contested",
        "registry": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-registry-v0",
            "input_remediation_plan_id": plan["id"],
            "target_task_id": plan["target_task_id"],
            "target_pressure_test_id": plan["target_pressure_test_id"],
            "target_remediation_id": calibration_item["remediation_id"],
            "target_remediation_category": calibration_item["remediation_category"],
            "retrieved_at": RETRIEVED_AT,
            "source_families": source_families,
            "execution_state": {
                "source_registry_recorded": True,
                "sources_ingested": False,
                "calibration_intervals_computed": False,
                "probability_pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "The registry scopes required human-knowledge source families for calibration. "
                "It does not ingest sources, compute intervals, or resolve evidential pressure."
            ),
        },
        "warning": "Calibration source registry is a collection scope, not proof evidence.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_checks(
    ontological_soundness_bad_god_evidential_projection_remediation_plan: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    plan_doc = (
        ontological_soundness_bad_god_evidential_projection_remediation_plan
        or _build_ontological_soundness_bad_god_evidential_projection_remediation_plan()
    )
    registry_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_registry
        or _build_ontological_soundness_bad_god_evidential_calibration_source_registry(plan_doc)
    )
    plan = plan_doc["plan"]
    registry = registry_doc["registry"]
    family_ids = {row["source_family_id"] for row in registry["source_families"]}
    expected_family_ids = {
        "analytic_philosophy",
        "philosophy_of_religion",
        "probability_theory",
        "empirical_suffering_data",
        "religious_experience_hiddenness_data",
        "comparative_theology",
    }
    calibration_ids = [
        row["remediation_id"] for row in plan["remediation_items"]
        if row["remediation_category"] == "calibration"
    ]
    checks = [
        {
            "id": "check-remediation-plan-linked",
            "status": "complete" if registry["input_remediation_plan_id"] == plan["id"] else "open",
            "input_remediation_plan_id": registry["input_remediation_plan_id"],
            "remediation_plan_id": plan["id"],
        },
        {
            "id": "check-calibration-item-selected",
            "status": "complete" if registry["target_remediation_id"] in calibration_ids else "open",
            "target_remediation_id": registry["target_remediation_id"],
            "calibration_remediation_ids": calibration_ids,
        },
        {
            "id": "check-source-families-cover-calibration-domains",
            "status": "complete" if family_ids == expected_family_ids else "open",
            "source_family_ids": sorted(family_ids),
            "expected_family_ids": sorted(expected_family_ids),
        },
        {
            "id": "check-sources-not-ingested",
            "status": "complete"
            if all(row["collection_status"] == "scoped_not_ingested" for row in registry["source_families"])
            and registry["execution_state"]["sources_ingested"] is False
            else "open",
            "collection_statuses": [row["collection_status"] for row in registry["source_families"]],
        },
        {
            "id": "check-calibration-registry-not-proof",
            "status": "contested"
            if registry_doc["status"] == "contested"
            and registry["execution_state"]["calibration_intervals_computed"] is False
            and registry["execution_state"]["proof_claim_allowed"] is False
            else "open",
            "execution_state": registry["execution_state"],
            "decision_rule": registry["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_task_id": registry["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_registry_not_proof",
        "checks": checks,
        "remaining_risks": [
            "source families are scoped but not ingested",
            "source reliability and diversity have not been scored",
            "calibration intervals remain uncomputed",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_acquisition_manifest(
    ontological_soundness_bad_god_evidential_calibration_source_registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    registry_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_registry
        or _build_ontological_soundness_bad_god_evidential_calibration_source_registry()
    )
    registry = registry_doc["registry"]
    query_intents_by_family = {
        "analytic_philosophy": [
            "modal ontological argument parody objection coherence conceivability",
            "necessary existence premise support contemporary analytic philosophy",
        ],
        "philosophy_of_religion": [
            "evidential problem of evil divine hiddenness theodicy expert disagreement",
            "bad god challenge symmetry good god philosophy of religion",
        ],
        "probability_theory": [
            "imprecise probability Bayesian confirmation interval likelihood calibration",
            "Bayesian model comparison dependence sensitivity analysis philosophical evidence",
        ],
        "empirical_suffering_data": [
            "global suffering preventable harm mortality disability burden dataset",
            "natural evil moral evil empirical case rate calibration",
        ],
        "religious_experience_hiddenness_data": [
            "religious experience nonbelief divine hiddenness survey dataset",
            "religious affiliation atheism agnosticism nonresistant nonbelief evidence",
        ],
        "comparative_theology": [
            "comparative theology divine attributes cross tradition God concept",
            "classical theism nondual theism process theology rival hypothesis comparison",
        ],
    }
    acquisition_items = []
    for family in registry["source_families"]:
        acquisition_items.append({
            "source_family_id": family["source_family_id"],
            "domain": family["domain"],
            "calibration_role": family["calibration_role"],
            "query_intents": query_intents_by_family[family["source_family_id"]],
            "acceptance_gates": [
                "primary_or_peer_reviewed_or_official_dataset",
                "relevant_to_calibration_interval_bounds",
                "contains_counterevidence_or_uncertainty_signal",
            ],
            "minimum_candidate_records": 3,
            "acquisition_status": "queued_not_fetched",
            "fetched_record_count": 0,
            "proof_evidence_materialized": False,
        })
    return {
        "status": "contested",
        "manifest": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-acquisition-manifest-v0",
            "input_source_registry_id": registry["id"],
            "target_task_id": registry["target_task_id"],
            "target_pressure_test_id": registry["target_pressure_test_id"],
            "target_remediation_id": registry["target_remediation_id"],
            "acquisition_scope": "calibration_source_collection",
            "retrieved_at": RETRIEVED_AT,
            "acquisition_items": acquisition_items,
            "execution_state": {
                "acquisition_manifest_recorded": True,
                "sources_fetched": False,
                "sources_ingested": False,
                "source_quality_scored": False,
                "calibration_intervals_computed": False,
                "probability_pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Acquisition manifest records what to fetch and how to gate it. "
                "It does not fetch, ingest, score, calibrate, or prove anything."
            ),
        },
        "warning": "Source acquisition manifest is queued collection work only.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_acquisition_checks(
    ontological_soundness_bad_god_evidential_calibration_source_registry: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_acquisition_manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    registry_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_registry
        or _build_ontological_soundness_bad_god_evidential_calibration_source_registry()
    )
    manifest_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_acquisition_manifest
        or _build_ontological_soundness_bad_god_evidential_calibration_source_acquisition_manifest(registry_doc)
    )
    registry = registry_doc["registry"]
    manifest = manifest_doc["manifest"]
    registry_family_ids = {row["source_family_id"] for row in registry["source_families"]}
    manifest_family_ids = {row["source_family_id"] for row in manifest["acquisition_items"]}
    checks = [
        {
            "id": "check-source-registry-linked",
            "status": "complete" if manifest["input_source_registry_id"] == registry["id"] else "open",
            "input_source_registry_id": manifest["input_source_registry_id"],
            "source_registry_id": registry["id"],
        },
        {
            "id": "check-acquisition-items-cover-source-families",
            "status": "complete" if manifest_family_ids == registry_family_ids else "open",
            "manifest_source_family_ids": sorted(manifest_family_ids),
            "registry_source_family_ids": sorted(registry_family_ids),
        },
        {
            "id": "check-acquisition-queries-present",
            "status": "complete"
            if all(len(row["query_intents"]) >= 2 for row in manifest["acquisition_items"])
            and all(len(row["acceptance_gates"]) >= 3 for row in manifest["acquisition_items"])
            else "open",
            "query_counts": {
                row["source_family_id"]: len(row["query_intents"])
                for row in manifest["acquisition_items"]
            },
        },
        {
            "id": "check-sources-not-fetched",
            "status": "complete"
            if all(row["acquisition_status"] == "queued_not_fetched" for row in manifest["acquisition_items"])
            and manifest["execution_state"]["sources_fetched"] is False
            else "open",
            "acquisition_statuses": [row["acquisition_status"] for row in manifest["acquisition_items"]],
        },
        {
            "id": "check-acquisition-manifest-not-proof",
            "status": "contested"
            if manifest_doc["status"] == "contested"
            and manifest["execution_state"]["calibration_intervals_computed"] is False
            and manifest["execution_state"]["proof_claim_allowed"] is False
            else "open",
            "execution_state": manifest["execution_state"],
            "decision_rule": manifest["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_task_id": manifest["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_acquisition_manifest_not_proof",
        "checks": checks,
        "remaining_risks": [
            "candidate records have not been fetched",
            "source relevance, diversity, and counterevidence have not been scored",
            "source collection has not been transformed into calibration intervals",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_batch_plan(
    ontological_soundness_bad_god_evidential_calibration_source_acquisition_manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    manifest_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_acquisition_manifest
        or _build_ontological_soundness_bad_god_evidential_calibration_source_acquisition_manifest()
    )
    manifest = manifest_doc["manifest"]
    batches = []
    for item in manifest["acquisition_items"]:
        batches.append({
            "batch_id": f"batch-acquire-{item['source_family_id']}",
            "source_family_id": item["source_family_id"],
            "query_intents": item["query_intents"],
            "acceptance_gates": item["acceptance_gates"],
            "minimum_candidate_records": item["minimum_candidate_records"],
            "batch_status": "queued_not_started",
            "expected_outputs": [
                "candidate_record_jsonl",
                "source_retrieval_log",
                "sha256_hash_manifest",
                "acceptance_gate_results",
            ],
            "logging_requirements": {
                "transcript_event_required": True,
                "hash_algorithm": "sha256",
                "log_fields": [
                    "source_family_id",
                    "query_intent",
                    "candidate_url_or_identifier",
                    "retrieved_at",
                    "sha256",
                    "acceptance_gate_results",
                ],
            },
            "proof_evidence_materialized": False,
        })
    return {
        "status": "contested",
        "batch_plan": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-batch-plan-v0",
            "input_acquisition_manifest_id": manifest["id"],
            "target_task_id": manifest["target_task_id"],
            "target_pressure_test_id": manifest["target_pressure_test_id"],
            "target_remediation_id": manifest["target_remediation_id"],
            "batch_scope": "calibration_source_acquisition_batches",
            "retrieved_at": RETRIEVED_AT,
            "batches": batches,
            "execution_state": {
                "batch_plan_recorded": True,
                "batches_executed": False,
                "sources_fetched": False,
                "sources_ingested": False,
                "acquisition_log_materialized": False,
                "calibration_intervals_computed": False,
                "probability_pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Batch plan turns source acquisition into auditable execution units. "
                "It does not execute retrieval, materialize logs, or resolve calibration."
            ),
        },
        "warning": "Calibration source batch plan is execution planning only.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_batch_checks(
    ontological_soundness_bad_god_evidential_calibration_source_acquisition_manifest: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_batch_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    manifest_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_acquisition_manifest
        or _build_ontological_soundness_bad_god_evidential_calibration_source_acquisition_manifest()
    )
    batch_plan_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_batch_plan
        or _build_ontological_soundness_bad_god_evidential_calibration_source_batch_plan(manifest_doc)
    )
    manifest = manifest_doc["manifest"]
    batch_plan = batch_plan_doc["batch_plan"]
    manifest_family_ids = {row["source_family_id"] for row in manifest["acquisition_items"]}
    batch_family_ids = {row["source_family_id"] for row in batch_plan["batches"]}
    checks = [
        {
            "id": "check-acquisition-manifest-linked",
            "status": "complete"
            if batch_plan["input_acquisition_manifest_id"] == manifest["id"]
            else "open",
            "input_acquisition_manifest_id": batch_plan["input_acquisition_manifest_id"],
            "acquisition_manifest_id": manifest["id"],
        },
        {
            "id": "check-batches-cover-acquisition-items",
            "status": "complete" if batch_family_ids == manifest_family_ids else "open",
            "batch_source_family_ids": sorted(batch_family_ids),
            "manifest_source_family_ids": sorted(manifest_family_ids),
        },
        {
            "id": "check-batches-include-logging-requirements",
            "status": "complete"
            if all(row["logging_requirements"]["hash_algorithm"] == "sha256" for row in batch_plan["batches"])
            and all(row["logging_requirements"]["transcript_event_required"] is True for row in batch_plan["batches"])
            else "open",
            "hash_algorithms": [
                row["logging_requirements"]["hash_algorithm"] for row in batch_plan["batches"]
            ],
        },
        {
            "id": "check-batches-not-executed",
            "status": "complete"
            if all(row["batch_status"] == "queued_not_started" for row in batch_plan["batches"])
            and batch_plan["execution_state"]["batches_executed"] is False
            else "open",
            "batch_statuses": [row["batch_status"] for row in batch_plan["batches"]],
        },
        {
            "id": "check-batch-plan-not-proof",
            "status": "contested"
            if batch_plan_doc["status"] == "contested"
            and batch_plan["execution_state"]["acquisition_log_materialized"] is False
            and batch_plan["execution_state"]["proof_claim_allowed"] is False
            else "open",
            "execution_state": batch_plan["execution_state"],
            "decision_rule": batch_plan["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_task_id": batch_plan["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_batch_plan_not_proof",
        "checks": checks,
        "remaining_risks": [
            "source acquisition batches have not been executed",
            "retrieval logs and hashes have not been materialized",
            "candidate records have not been scored or calibrated",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_seed_catalog(
    ontological_soundness_bad_god_evidential_calibration_source_batch_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    batch_plan_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_batch_plan
        or _build_ontological_soundness_bad_god_evidential_calibration_source_batch_plan()
    )
    batch_plan = batch_plan_doc["batch_plan"]
    candidate_sources = [
        {
            "source_id": "seed-analytic-philosophy-sep-ontological-arguments",
            "source_family_id": "analytic_philosophy",
            "title": "Stanford Encyclopedia of Philosophy: Ontological Arguments",
            "url": "https://plato.stanford.edu/entries/ontological-arguments/",
            "source_kind": "peer_reviewed_reference",
            "evidence_role": "calibrate modal ontological premise support and objections",
            "source_status": "seeded_not_fetched",
            "url_verified_at": RETRIEVED_AT,
            "proof_evidence_materialized": False,
        },
        {
            "source_id": "seed-analytic-philosophy-sep-logic-ontology",
            "source_family_id": "analytic_philosophy",
            "title": "Stanford Encyclopedia of Philosophy: Logic and Ontology",
            "url": "https://plato.stanford.edu/entries/logic-ontology/",
            "source_kind": "peer_reviewed_reference",
            "evidence_role": "calibrate ontology and logical commitment constraints",
            "source_status": "seeded_not_fetched",
            "url_verified_at": RETRIEVED_AT,
            "proof_evidence_materialized": False,
        },
        {
            "source_id": "seed-philosophy-religion-sep-evil",
            "source_family_id": "philosophy_of_religion",
            "title": "Stanford Encyclopedia of Philosophy: The Problem of Evil",
            "url": "https://plato.stanford.edu/entries/evil/",
            "source_kind": "peer_reviewed_reference",
            "evidence_role": "calibrate evidential evil objection strength",
            "source_status": "seeded_not_fetched",
            "url_verified_at": RETRIEVED_AT,
            "proof_evidence_materialized": False,
        },
        {
            "source_id": "seed-philosophy-religion-sep-divine-hiddenness",
            "source_family_id": "philosophy_of_religion",
            "title": "Stanford Encyclopedia of Philosophy: Hiddenness of God",
            "url": "https://plato.stanford.edu/entries/divine-hiddenness/",
            "source_kind": "peer_reviewed_reference",
            "evidence_role": "calibrate divine hiddenness and nonbelief objections",
            "source_status": "seeded_not_fetched",
            "url_verified_at": RETRIEVED_AT,
            "proof_evidence_materialized": False,
        },
        {
            "source_id": "seed-probability-theory-sep-bayesian-epistemology",
            "source_family_id": "probability_theory",
            "title": "Stanford Encyclopedia of Philosophy: Bayesian Epistemology",
            "url": "https://plato.stanford.edu/entries/epistemology-bayesian/",
            "source_kind": "peer_reviewed_reference",
            "evidence_role": "calibrate Bayesian update and prior sensitivity rules",
            "source_status": "seeded_not_fetched",
            "url_verified_at": RETRIEVED_AT,
            "proof_evidence_materialized": False,
        },
        {
            "source_id": "seed-probability-theory-sep-imprecise-probabilities",
            "source_family_id": "probability_theory",
            "title": "Stanford Encyclopedia of Philosophy: Imprecise Probabilities",
            "url": "https://plato.stanford.edu/entries/imprecise-probabilities/",
            "source_kind": "peer_reviewed_reference",
            "evidence_role": "calibrate interval and credal-set uncertainty treatment",
            "source_status": "seeded_not_fetched",
            "url_verified_at": RETRIEVED_AT,
            "proof_evidence_materialized": False,
        },
        {
            "source_id": "seed-empirical-suffering-ihme-gbd-results",
            "source_family_id": "empirical_suffering_data",
            "title": "IHME GHDx: Global Burden of Disease Results Tool",
            "url": "https://ghdx.healthdata.org/gbd-results-tool",
            "source_kind": "official_dataset_tool",
            "evidence_role": "ground death and disability burden intervals",
            "source_status": "seeded_not_fetched",
            "url_verified_at": RETRIEVED_AT,
            "proof_evidence_materialized": False,
        },
        {
            "source_id": "seed-empirical-suffering-who-global-health-estimates",
            "source_family_id": "empirical_suffering_data",
            "title": "WHO: Global Health Estimates",
            "url": "https://www.who.int/mega-menu/data/data-who/global-health-estimates",
            "source_kind": "official_dataset",
            "evidence_role": "cross-check global death and disability estimates",
            "source_status": "seeded_not_fetched",
            "url_verified_at": RETRIEVED_AT,
            "proof_evidence_materialized": False,
        },
        {
            "source_id": "seed-hiddenness-data-pew-rls",
            "source_family_id": "religious_experience_hiddenness_data",
            "title": "Pew Research Center: Religious Landscape Study",
            "url": "https://www.pewresearch.org/about-the-religious-landscape-study/",
            "source_kind": "survey_dataset",
            "evidence_role": "calibrate religious affiliation, practice, and nonaffiliation rates",
            "source_status": "seeded_not_fetched",
            "url_verified_at": RETRIEVED_AT,
            "proof_evidence_materialized": False,
        },
        {
            "source_id": "seed-hiddenness-data-world-values-survey",
            "source_family_id": "religious_experience_hiddenness_data",
            "title": "World Values Survey: Data and Documentation",
            "url": "https://www.worldvaluessurvey.org/WVSContents.jsp?CMSID=Documentation",
            "source_kind": "survey_dataset",
            "evidence_role": "calibrate cross-national religious belief and value variables",
            "source_status": "seeded_not_fetched",
            "url_verified_at": RETRIEVED_AT,
            "proof_evidence_materialized": False,
        },
        {
            "source_id": "seed-comparative-theology-harvard-pluralism",
            "source_family_id": "comparative_theology",
            "title": "Harvard Pluralism Project: Mission and History",
            "url": "https://pluralism.org/mission-and-history",
            "source_kind": "academic_project",
            "evidence_role": "calibrate cross-tradition religious diversity context",
            "source_status": "seeded_not_fetched",
            "url_verified_at": RETRIEVED_AT,
            "proof_evidence_materialized": False,
        },
        {
            "source_id": "seed-comparative-theology-britannica-theology",
            "source_family_id": "comparative_theology",
            "title": "Britannica: Theology",
            "url": "https://www.britannica.com/topic/theology",
            "source_kind": "reference",
            "evidence_role": "calibrate theology as cross-tradition conceptual comparison",
            "source_status": "seeded_not_fetched",
            "url_verified_at": RETRIEVED_AT,
            "proof_evidence_materialized": False,
        },
    ]
    return {
        "status": "contested",
        "catalog": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-seed-catalog-v0",
            "input_batch_plan_id": batch_plan["id"],
            "target_task_id": batch_plan["target_task_id"],
            "target_pressure_test_id": batch_plan["target_pressure_test_id"],
            "target_remediation_id": batch_plan["target_remediation_id"],
            "candidate_scope": "calibration_source_seed_candidates",
            "retrieved_at": RETRIEVED_AT,
            "candidate_sources": candidate_sources,
            "execution_state": {
                "seed_catalog_recorded": True,
                "source_candidates_fetched": False,
                "source_hashes_materialized": False,
                "sources_ingested": False,
                "calibration_intervals_computed": False,
                "probability_pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Seed catalog records verified candidate URLs for later acquisition. "
                "It does not fetch, hash, ingest, score, calibrate, or prove anything."
            ),
        },
        "warning": "Seed catalog is source planning only and is not proof evidence.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_seed_checks(
    ontological_soundness_bad_god_evidential_calibration_source_batch_plan: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_seed_catalog: dict[str, Any] | None = None,
) -> dict[str, Any]:
    batch_plan_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_batch_plan
        or _build_ontological_soundness_bad_god_evidential_calibration_source_batch_plan()
    )
    catalog_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_seed_catalog
        or _build_ontological_soundness_bad_god_evidential_calibration_source_seed_catalog(batch_plan_doc)
    )
    batch_plan = batch_plan_doc["batch_plan"]
    catalog = catalog_doc["catalog"]
    batch_family_ids = {row["source_family_id"] for row in batch_plan["batches"]}
    seed_family_ids = {row["source_family_id"] for row in catalog["candidate_sources"]}
    seed_counts = {
        family_id: sum(
            1 for row in catalog["candidate_sources"]
            if row["source_family_id"] == family_id
        )
        for family_id in seed_family_ids
    }
    checks = [
        {
            "id": "check-batch-plan-linked",
            "status": "complete" if catalog["input_batch_plan_id"] == batch_plan["id"] else "open",
            "input_batch_plan_id": catalog["input_batch_plan_id"],
            "batch_plan_id": batch_plan["id"],
        },
        {
            "id": "check-seeds-cover-batch-families",
            "status": "complete" if seed_family_ids == batch_family_ids else "open",
            "seed_source_family_ids": sorted(seed_family_ids),
            "batch_source_family_ids": sorted(batch_family_ids),
        },
        {
            "id": "check-seed-counts-per-family",
            "status": "complete"
            if seed_family_ids == batch_family_ids and all(count >= 2 for count in seed_counts.values())
            else "open",
            "seed_counts_by_family": seed_counts,
        },
        {
            "id": "check-seeds-not-fetched",
            "status": "complete"
            if all(row["source_status"] == "seeded_not_fetched" for row in catalog["candidate_sources"])
            and catalog["execution_state"]["source_candidates_fetched"] is False
            else "open",
            "source_statuses": [row["source_status"] for row in catalog["candidate_sources"]],
        },
        {
            "id": "check-seed-catalog-not-proof",
            "status": "contested"
            if catalog_doc["status"] == "contested"
            and catalog["execution_state"]["source_hashes_materialized"] is False
            and catalog["execution_state"]["proof_claim_allowed"] is False
            else "open",
            "execution_state": catalog["execution_state"],
            "decision_rule": catalog["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_task_id": catalog["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_seed_catalog_not_proof",
        "checks": checks,
        "remaining_risks": [
            "seed URLs have not been fetched or hashed",
            "candidate source content has not been ingested or scored",
            "seed catalog has not produced calibration intervals",
        ],
    }


def _source_kind_pre_fetch_gates(source_kind: str) -> list[str]:
    source_kind_to_gate = {
        "peer_reviewed_reference": "primary_or_peer_reviewed_or_official_dataset",
        "official_dataset_tool": "primary_or_peer_reviewed_or_official_dataset",
        "official_dataset": "primary_or_peer_reviewed_or_official_dataset",
        "survey_dataset": "primary_or_peer_reviewed_or_official_dataset",
        "academic_project": "primary_or_peer_reviewed_or_official_dataset",
        "reference": "relevant_to_calibration_interval_bounds",
    }
    gates = [
        source_kind_to_gate.get(source_kind, "relevant_to_calibration_interval_bounds"),
        "relevant_to_calibration_interval_bounds",
    ]
    return sorted(set(gates))


def _build_ontological_soundness_bad_god_evidential_calibration_source_eligibility_matrix(
    ontological_soundness_bad_god_evidential_calibration_source_seed_catalog: dict[str, Any] | None = None,
) -> dict[str, Any]:
    catalog_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_seed_catalog
        or _build_ontological_soundness_bad_god_evidential_calibration_source_seed_catalog()
    )
    catalog = catalog_doc["catalog"]
    eligibility_rows = []
    for source in catalog["candidate_sources"]:
        eligibility_rows.append({
            "source_id": source["source_id"],
            "source_family_id": source["source_family_id"],
            "source_kind": source["source_kind"],
            "url": source["url"],
            "satisfied_pre_fetch_gates": _source_kind_pre_fetch_gates(source["source_kind"]),
            "pending_gates": [
                "content_relevance_confirmed_after_fetch",
                "counterevidence_or_uncertainty_signal_confirmed_after_fetch",
                "retrieval_hash_recorded",
            ],
            "eligibility_status": "eligible_pending_fetch",
            "content_fetched": False,
            "content_quality_scored": False,
            "proof_evidence_materialized": False,
        })
    gate_summary = {
        "candidate_count": len(eligibility_rows),
        "eligible_pending_fetch_count": sum(
            1 for row in eligibility_rows
            if row["eligibility_status"] == "eligible_pending_fetch"
        ),
        "content_quality_scored_count": sum(
            1 for row in eligibility_rows
            if row["content_quality_scored"] is True
        ),
    }
    return {
        "status": "contested",
        "matrix": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-eligibility-matrix-v0",
            "input_seed_catalog_id": catalog["id"],
            "target_task_id": catalog["target_task_id"],
            "target_pressure_test_id": catalog["target_pressure_test_id"],
            "target_remediation_id": catalog["target_remediation_id"],
            "eligibility_scope": "pre_fetch_source_gate_classification",
            "retrieved_at": RETRIEVED_AT,
            "eligibility_rows": eligibility_rows,
            "gate_summary": gate_summary,
            "execution_state": {
                "eligibility_matrix_recorded": True,
                "source_content_fetched": False,
                "source_quality_scored": False,
                "source_hashes_materialized": False,
                "calibration_intervals_computed": False,
                "probability_pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Eligibility matrix classifies seed candidates before fetching. "
                "It cannot confirm content quality, hash evidence, or calibration intervals."
            ),
        },
        "warning": "Eligibility matrix is pre-fetch gate classification only.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_eligibility_checks(
    ontological_soundness_bad_god_evidential_calibration_source_seed_catalog: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_eligibility_matrix: dict[str, Any] | None = None,
) -> dict[str, Any]:
    catalog_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_seed_catalog
        or _build_ontological_soundness_bad_god_evidential_calibration_source_seed_catalog()
    )
    matrix_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_eligibility_matrix
        or _build_ontological_soundness_bad_god_evidential_calibration_source_eligibility_matrix(catalog_doc)
    )
    catalog = catalog_doc["catalog"]
    matrix = matrix_doc["matrix"]
    seed_ids = {row["source_id"] for row in catalog["candidate_sources"]}
    matrix_ids = {row["source_id"] for row in matrix["eligibility_rows"]}
    checks = [
        {
            "id": "check-seed-catalog-linked",
            "status": "complete" if matrix["input_seed_catalog_id"] == catalog["id"] else "open",
            "input_seed_catalog_id": matrix["input_seed_catalog_id"],
            "seed_catalog_id": catalog["id"],
        },
        {
            "id": "check-eligibility-rows-cover-seeds",
            "status": "complete" if matrix_ids == seed_ids else "open",
            "eligibility_source_ids": sorted(matrix_ids),
            "seed_source_ids": sorted(seed_ids),
        },
        {
            "id": "check-pre-fetch-gates-classified",
            "status": "complete"
            if all(row["eligibility_status"] == "eligible_pending_fetch" for row in matrix["eligibility_rows"])
            and all(row["satisfied_pre_fetch_gates"] for row in matrix["eligibility_rows"])
            else "open",
            "eligible_pending_fetch_count": matrix["gate_summary"]["eligible_pending_fetch_count"],
        },
        {
            "id": "check-content-not-scored",
            "status": "complete"
            if matrix["gate_summary"]["content_quality_scored_count"] == 0
            and matrix["execution_state"]["source_quality_scored"] is False
            else "open",
            "content_quality_scored_count": matrix["gate_summary"]["content_quality_scored_count"],
        },
        {
            "id": "check-eligibility-matrix-not-proof",
            "status": "contested"
            if matrix_doc["status"] == "contested"
            and matrix["execution_state"]["calibration_intervals_computed"] is False
            and matrix["execution_state"]["proof_claim_allowed"] is False
            else "open",
            "execution_state": matrix["execution_state"],
            "decision_rule": matrix["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_task_id": matrix["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_eligibility_matrix_not_proof",
        "checks": checks,
        "remaining_risks": [
            "eligibility is based on seed metadata rather than fetched content",
            "content relevance and counterevidence gates remain pending",
            "no source quality scores or calibration intervals exist",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook(
    ontological_soundness_bad_god_evidential_calibration_source_eligibility_matrix: dict[str, Any] | None = None,
) -> dict[str, Any]:
    matrix_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_eligibility_matrix
        or _build_ontological_soundness_bad_god_evidential_calibration_source_eligibility_matrix()
    )
    matrix = matrix_doc["matrix"]
    retrieval_steps = []
    for row in matrix["eligibility_rows"]:
        source_id = row["source_id"]
        raw_output_path = f"calibration-sources/raw/{source_id}.html"
        hash_output_path = f"calibration-sources/hashes/{source_id}.sha256"
        log_output_path = f"calibration-sources/logs/{source_id}.json"
        retrieval_steps.append({
            "step_id": f"retrieve-{source_id}",
            "source_id": source_id,
            "source_family_id": row["source_family_id"],
            "source_status": row["eligibility_status"],
            "url": row["url"],
            "fetch_command_template": (
                f"rtk curl -L --fail --silent --show-error {row['url']} "
                f"-o {raw_output_path}"
            ),
            "hash_command_template": f"rtk shasum -a 256 {raw_output_path} > {hash_output_path}",
            "log_event_name": "calibration_source_candidate_retrieved",
            "expected_hash_algorithm": "sha256",
            "expected_outputs": {
                "raw_output_path": raw_output_path,
                "hash_output_path": hash_output_path,
                "log_output_path": log_output_path,
            },
            "step_status": "queued_not_executed",
            "proof_evidence_materialized": False,
        })
    return {
        "status": "contested",
        "runbook": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-retrieval-runbook-v0",
            "input_eligibility_matrix_id": matrix["id"],
            "target_task_id": matrix["target_task_id"],
            "target_pressure_test_id": matrix["target_pressure_test_id"],
            "target_remediation_id": matrix["target_remediation_id"],
            "retrieval_scope": "auditable_candidate_fetch_hash_log",
            "retrieved_at": RETRIEVED_AT,
            "retrieval_steps": retrieval_steps,
            "execution_state": {
                "retrieval_runbook_recorded": True,
                "retrieval_executed": False,
                "source_content_fetched": False,
                "source_hashes_materialized": False,
                "retrieval_logs_materialized": False,
                "sources_ingested": False,
                "calibration_intervals_computed": False,
                "probability_pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Retrieval runbook provides auditable fetch, hash, and log templates. "
                "It is not executed and does not materialize evidence or calibration intervals."
            ),
        },
        "warning": "Retrieval runbook is executable planning only and is not proof evidence.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_retrieval_checks(
    ontological_soundness_bad_god_evidential_calibration_source_eligibility_matrix: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook: dict[str, Any] | None = None,
) -> dict[str, Any]:
    matrix_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_eligibility_matrix
        or _build_ontological_soundness_bad_god_evidential_calibration_source_eligibility_matrix()
    )
    runbook_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook
        or _build_ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook(matrix_doc)
    )
    matrix = matrix_doc["matrix"]
    runbook = runbook_doc["runbook"]
    eligible_source_ids = {
        row["source_id"] for row in matrix["eligibility_rows"]
        if row["eligibility_status"] == "eligible_pending_fetch"
    }
    retrieval_source_ids = {row["source_id"] for row in runbook["retrieval_steps"]}
    checks = [
        {
            "id": "check-eligibility-matrix-linked",
            "status": "complete" if runbook["input_eligibility_matrix_id"] == matrix["id"] else "open",
            "input_eligibility_matrix_id": runbook["input_eligibility_matrix_id"],
            "eligibility_matrix_id": matrix["id"],
        },
        {
            "id": "check-retrieval-steps-cover-eligible-sources",
            "status": "complete" if retrieval_source_ids == eligible_source_ids else "open",
            "retrieval_source_ids": sorted(retrieval_source_ids),
            "eligible_source_ids": sorted(eligible_source_ids),
        },
        {
            "id": "check-fetch-hash-log-templates-present",
            "status": "complete"
            if all(row["fetch_command_template"].startswith("rtk curl -L --fail") for row in runbook["retrieval_steps"])
            and all(row["hash_command_template"].startswith("rtk shasum -a 256") for row in runbook["retrieval_steps"])
            and all(row["log_event_name"] for row in runbook["retrieval_steps"])
            else "open",
            "retrieval_step_count": len(runbook["retrieval_steps"]),
        },
        {
            "id": "check-retrieval-not-executed",
            "status": "complete"
            if all(row["step_status"] == "queued_not_executed" for row in runbook["retrieval_steps"])
            and runbook["execution_state"]["retrieval_executed"] is False
            else "open",
            "step_statuses": [row["step_status"] for row in runbook["retrieval_steps"]],
        },
        {
            "id": "check-retrieval-runbook-not-proof",
            "status": "contested"
            if runbook_doc["status"] == "contested"
            and runbook["execution_state"]["source_hashes_materialized"] is False
            and runbook["execution_state"]["proof_claim_allowed"] is False
            else "open",
            "execution_state": runbook["execution_state"],
            "decision_rule": runbook["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_task_id": runbook["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_retrieval_runbook_not_proof",
        "checks": checks,
        "remaining_risks": [
            "retrieval commands are templates and have not been executed",
            "raw source content, hashes, and retrieval logs do not exist yet",
            "source content has not been scored or transformed into calibration intervals",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_schema(
    ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook: dict[str, Any] | None = None,
) -> dict[str, Any]:
    runbook_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook
        or _build_ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook()
    )
    runbook = runbook_doc["runbook"]
    required_log_fields = [
        "source_id",
        "source_family_id",
        "url",
        "retrieved_at",
        "http_status",
        "content_type",
        "byte_count",
        "sha256",
        "raw_output_path",
        "hash_output_path",
        "transcript_event_name",
    ]
    log_templates = []
    for step in runbook["retrieval_steps"]:
        log_templates.append({
            "source_id": step["source_id"],
            "source_family_id": step["source_family_id"],
            "url": step["url"],
            "required_log_fields": required_log_fields,
            "raw_output_path": step["expected_outputs"]["raw_output_path"],
            "hash_output_path": step["expected_outputs"]["hash_output_path"],
            "log_output_path": step["expected_outputs"]["log_output_path"],
            "transcript_event_name": step["log_event_name"],
            "log_status": "schema_defined_not_materialized",
            "proof_evidence_materialized": False,
        })
    return {
        "status": "contested",
        "schema": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-retrieval-log-schema-v0",
            "input_retrieval_runbook_id": runbook["id"],
            "target_task_id": runbook["target_task_id"],
            "target_pressure_test_id": runbook["target_pressure_test_id"],
            "target_remediation_id": runbook["target_remediation_id"],
            "log_scope": "retrieval_execution_log_schema",
            "retrieved_at": RETRIEVED_AT,
            "required_log_fields": required_log_fields,
            "hash_validation": {
                "algorithm": "sha256",
                "required": True,
                "source_field": "sha256",
                "file_field": "raw_output_path",
            },
            "transcript_event_name": "calibration_source_candidate_retrieved",
            "log_templates": log_templates,
            "execution_state": {
                "retrieval_log_schema_recorded": True,
                "retrieval_logs_materialized": False,
                "hashes_verified": False,
                "source_content_fetched": False,
                "sources_ingested": False,
                "calibration_intervals_computed": False,
                "probability_pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Retrieval log schema defines mandatory evidence fields only. "
                "No retrieval log, hash verification, or calibration interval exists yet."
            ),
        },
        "warning": "Retrieval log schema is not a materialized evidence log.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_checks(
    ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_schema: dict[str, Any] | None = None,
) -> dict[str, Any]:
    runbook_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook
        or _build_ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook()
    )
    schema_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_schema
        or _build_ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_schema(runbook_doc)
    )
    runbook = runbook_doc["runbook"]
    schema = schema_doc["schema"]
    step_source_ids = {row["source_id"] for row in runbook["retrieval_steps"]}
    template_source_ids = {row["source_id"] for row in schema["log_templates"]}
    required_fields = set(schema["required_log_fields"])
    expected_fields = {
        "source_id",
        "source_family_id",
        "url",
        "retrieved_at",
        "http_status",
        "content_type",
        "byte_count",
        "sha256",
        "raw_output_path",
        "hash_output_path",
        "transcript_event_name",
    }
    checks = [
        {
            "id": "check-retrieval-runbook-linked",
            "status": "complete" if schema["input_retrieval_runbook_id"] == runbook["id"] else "open",
            "input_retrieval_runbook_id": schema["input_retrieval_runbook_id"],
            "retrieval_runbook_id": runbook["id"],
        },
        {
            "id": "check-log-templates-cover-retrieval-steps",
            "status": "complete" if template_source_ids == step_source_ids else "open",
            "template_source_ids": sorted(template_source_ids),
            "retrieval_step_source_ids": sorted(step_source_ids),
        },
        {
            "id": "check-required-log-fields-present",
            "status": "complete" if expected_fields.issubset(required_fields) else "open",
            "required_log_fields": schema["required_log_fields"],
        },
        {
            "id": "check-logs-not-materialized",
            "status": "complete"
            if all(row["log_status"] == "schema_defined_not_materialized" for row in schema["log_templates"])
            and schema["execution_state"]["retrieval_logs_materialized"] is False
            else "open",
            "log_statuses": [row["log_status"] for row in schema["log_templates"]],
        },
        {
            "id": "check-retrieval-log-schema-not-proof",
            "status": "contested"
            if schema_doc["status"] == "contested"
            and schema["execution_state"]["hashes_verified"] is False
            and schema["execution_state"]["proof_claim_allowed"] is False
            else "open",
            "execution_state": schema["execution_state"],
            "decision_rule": schema["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_task_id": schema["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_retrieval_log_schema_not_proof",
        "checks": checks,
        "remaining_risks": [
            "retrieval logs are not materialized",
            "hashes are not verified",
            "source content has not been ingested or scored",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger(
    ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_schema: dict[str, Any] | None = None,
) -> dict[str, Any]:
    runbook_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook
        or _build_ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook()
    )
    schema_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_schema
        or _build_ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_schema(runbook_doc)
    )
    runbook = runbook_doc["runbook"]
    schema = schema_doc["schema"]
    templates_by_source_id = {row["source_id"]: row for row in schema["log_templates"]}
    dry_run_rows = []
    for step in runbook["retrieval_steps"]:
        template = templates_by_source_id[step["source_id"]]
        dry_run_rows.append({
            "source_id": step["source_id"],
            "source_family_id": step["source_family_id"],
            "url": step["url"],
            "fetch_command_template": step["fetch_command_template"],
            "hash_command_template": step["hash_command_template"],
            "raw_output_path": template["raw_output_path"],
            "hash_output_path": template["hash_output_path"],
            "log_output_path": template["log_output_path"],
            "transcript_event_name": template["transcript_event_name"],
            "retrieval_step_status": step["step_status"],
            "log_status": template["log_status"],
            "dry_run_status": "validated_not_executed",
            "proof_evidence_materialized": False,
        })
    return {
        "status": "contested",
        "ledger": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-retrieval-dry-run-ledger-v0",
            "input_retrieval_runbook_id": runbook["id"],
            "input_retrieval_log_schema_id": schema["id"],
            "target_task_id": runbook["target_task_id"],
            "target_pressure_test_id": runbook["target_pressure_test_id"],
            "target_remediation_id": runbook["target_remediation_id"],
            "ledger_scope": "retrieval_pre_execution_dry_run",
            "retrieved_at": RETRIEVED_AT,
            "dry_run_rows": dry_run_rows,
            "execution_state": {
                "dry_run_ledger_recorded": True,
                "retrieval_executed": False,
                "retrieval_logs_materialized": False,
                "source_hashes_materialized": False,
                "source_content_fetched": False,
                "sources_ingested": False,
                "calibration_intervals_computed": False,
                "probability_pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Dry-run ledger validates command and log wiring before retrieval. "
                "It does not execute retrieval or materialize evidence."
            ),
        },
        "warning": "Dry-run ledger is pre-execution audit only.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_checks(
    ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_schema: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    runbook_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook
        or _build_ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook()
    )
    schema_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_schema
        or _build_ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_schema(runbook_doc)
    )
    ledger_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger
        or _build_ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger(
            runbook_doc,
            schema_doc,
        )
    )
    runbook = runbook_doc["runbook"]
    schema = schema_doc["schema"]
    ledger = ledger_doc["ledger"]
    retrieval_source_ids = {row["source_id"] for row in runbook["retrieval_steps"]}
    dry_run_source_ids = {row["source_id"] for row in ledger["dry_run_rows"]}
    checks = [
        {
            "id": "check-retrieval-runbook-linked",
            "status": "complete" if ledger["input_retrieval_runbook_id"] == runbook["id"] else "open",
            "input_retrieval_runbook_id": ledger["input_retrieval_runbook_id"],
            "retrieval_runbook_id": runbook["id"],
        },
        {
            "id": "check-retrieval-log-schema-linked",
            "status": "complete" if ledger["input_retrieval_log_schema_id"] == schema["id"] else "open",
            "input_retrieval_log_schema_id": ledger["input_retrieval_log_schema_id"],
            "retrieval_log_schema_id": schema["id"],
        },
        {
            "id": "check-dry-run-rows-cover-retrieval-steps",
            "status": "complete" if dry_run_source_ids == retrieval_source_ids else "open",
            "dry_run_source_ids": sorted(dry_run_source_ids),
            "retrieval_source_ids": sorted(retrieval_source_ids),
        },
        {
            "id": "check-dry-run-not-executed",
            "status": "complete"
            if all(row["dry_run_status"] == "validated_not_executed" for row in ledger["dry_run_rows"])
            and ledger["execution_state"]["retrieval_executed"] is False
            else "open",
            "dry_run_statuses": [row["dry_run_status"] for row in ledger["dry_run_rows"]],
        },
        {
            "id": "check-dry-run-ledger-not-proof",
            "status": "contested"
            if ledger_doc["status"] == "contested"
            and ledger["execution_state"]["retrieval_logs_materialized"] is False
            and ledger["execution_state"]["proof_claim_allowed"] is False
            else "open",
            "execution_state": ledger["execution_state"],
            "decision_rule": ledger["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_task_id": ledger["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_retrieval_dry_run_ledger_not_proof",
        "checks": checks,
        "remaining_risks": [
            "dry-run ledger is not retrieval execution",
            "source content, hashes, and logs are not materialized",
            "calibration intervals remain uncomputed",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_quality_rubric(
    ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ledger_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger
        or _build_ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger()
    )
    ledger = ledger_doc["ledger"]
    scoring_dimensions = [
        {
            "dimension_id": "authority",
            "weight": 0.22,
            "description": "source authorship, publisher, dataset stewardship, and review process",
        },
        {
            "dimension_id": "calibration_relevance",
            "weight": 0.24,
            "description": "direct usefulness for prior, likelihood, response-cost, or rival calibration",
        },
        {
            "dimension_id": "counterevidence_signal",
            "weight": 0.16,
            "description": "presence of objections, negative cases, dissent, or rival interpretation",
        },
        {
            "dimension_id": "uncertainty_signal",
            "weight": 0.14,
            "description": "explicit uncertainty, interval, methodological limitation, or disagreement marker",
        },
        {
            "dimension_id": "extractability",
            "weight": 0.14,
            "description": "whether claims, data fields, and citations can be extracted into structured records",
        },
        {
            "dimension_id": "bias_risk",
            "weight": 0.10,
            "description": "risk penalty for advocacy, one-sided framing, opacity, or missing counter-sources",
        },
    ]
    source_score_templates = []
    for row in ledger["dry_run_rows"]:
        source_score_templates.append({
            "source_id": row["source_id"],
            "source_family_id": row["source_family_id"],
            "url": row["url"],
            "score_status": "not_scored",
            "content_required_before_scoring": True,
            "dimension_scores": {
                dimension["dimension_id"]: None
                for dimension in scoring_dimensions
            },
            "weighted_quality_score": None,
            "proof_evidence_materialized": False,
        })
    return {
        "status": "contested",
        "rubric": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-quality-rubric-v0",
            "input_dry_run_ledger_id": ledger["id"],
            "target_task_id": ledger["target_task_id"],
            "target_pressure_test_id": ledger["target_pressure_test_id"],
            "target_remediation_id": ledger["target_remediation_id"],
            "rubric_scope": "post_fetch_source_quality_scoring",
            "retrieved_at": RETRIEVED_AT,
            "score_range": {"min": 0.0, "max": 1.0},
            "scoring_dimensions": scoring_dimensions,
            "source_score_templates": source_score_templates,
            "execution_state": {
                "quality_rubric_recorded": True,
                "source_content_fetched": False,
                "source_quality_scored": False,
                "calibration_intervals_computed": False,
                "probability_pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Quality rubric defines post-fetch scoring rules. "
                "It cannot score sources or calibrate intervals before content is fetched."
            ),
        },
        "warning": "Quality rubric is a scoring plan only and is not evidence.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_quality_checks(
    ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_quality_rubric: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ledger_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger
        or _build_ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger()
    )
    rubric_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_quality_rubric
        or _build_ontological_soundness_bad_god_evidential_calibration_source_quality_rubric(ledger_doc)
    )
    ledger = ledger_doc["ledger"]
    rubric = rubric_doc["rubric"]
    dimension_ids = {row["dimension_id"] for row in rubric["scoring_dimensions"]}
    expected_dimension_ids = {
        "authority",
        "calibration_relevance",
        "counterevidence_signal",
        "uncertainty_signal",
        "extractability",
        "bias_risk",
    }
    checks = [
        {
            "id": "check-dry-run-ledger-linked",
            "status": "complete" if rubric["input_dry_run_ledger_id"] == ledger["id"] else "open",
            "input_dry_run_ledger_id": rubric["input_dry_run_ledger_id"],
            "dry_run_ledger_id": ledger["id"],
        },
        {
            "id": "check-scoring-dimensions-complete",
            "status": "complete" if dimension_ids == expected_dimension_ids else "open",
            "dimension_ids": sorted(dimension_ids),
            "expected_dimension_ids": sorted(expected_dimension_ids),
        },
        {
            "id": "check-scoring-weights-normalized",
            "status": "complete"
            if abs(sum(row["weight"] for row in rubric["scoring_dimensions"]) - 1.0) < 1e-6
            else "open",
            "weight_sum": round(sum(row["weight"] for row in rubric["scoring_dimensions"]), 6),
        },
        {
            "id": "check-score-templates-not-scored",
            "status": "complete"
            if all(row["score_status"] == "not_scored" for row in rubric["source_score_templates"])
            and rubric["execution_state"]["source_quality_scored"] is False
            else "open",
            "score_statuses": [row["score_status"] for row in rubric["source_score_templates"]],
        },
        {
            "id": "check-quality-rubric-not-proof",
            "status": "contested"
            if rubric_doc["status"] == "contested"
            and rubric["execution_state"]["calibration_intervals_computed"] is False
            and rubric["execution_state"]["proof_claim_allowed"] is False
            else "open",
            "execution_state": rubric["execution_state"],
            "decision_rule": rubric["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_task_id": rubric["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_quality_rubric_not_proof",
        "checks": checks,
        "remaining_risks": [
            "source content is not fetched",
            "quality scores are not computed",
            "quality rubric has not produced calibration intervals",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_schema(
    ontological_soundness_bad_god_evidential_calibration_source_quality_rubric: dict[str, Any] | None = None,
) -> dict[str, Any]:
    rubric_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_quality_rubric
        or _build_ontological_soundness_bad_god_evidential_calibration_source_quality_rubric()
    )
    rubric = rubric_doc["rubric"]
    required_score_fields = [
        "source_id",
        "source_family_id",
        "dimension_scores",
        "weighted_quality_score",
        "usable_for_calibration",
        "score_rationale",
        "scored_at",
    ]
    dimension_ids = [row["dimension_id"] for row in rubric["scoring_dimensions"]]
    score_rows = []
    for template in rubric["source_score_templates"]:
        score_rows.append({
            "source_id": template["source_id"],
            "source_family_id": template["source_family_id"],
            "url": template["url"],
            "required_score_fields": required_score_fields,
            "dimension_scores": {dimension_id: None for dimension_id in dimension_ids},
            "weighted_quality_score": None,
            "usable_for_calibration": False,
            "score_rationale": None,
            "scored_at": None,
            "score_status": "schema_defined_not_scored",
            "proof_evidence_materialized": False,
        })
    return {
        "status": "contested",
        "schema": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-quality-score-ledger-schema-v0",
            "input_quality_rubric_id": rubric["id"],
            "target_task_id": rubric["target_task_id"],
            "target_pressure_test_id": rubric["target_pressure_test_id"],
            "target_remediation_id": rubric["target_remediation_id"],
            "ledger_scope": "post_fetch_quality_score_ledger_schema",
            "retrieved_at": RETRIEVED_AT,
            "required_score_fields": required_score_fields,
            "score_thresholds": {
                "minimum_usable_quality_score": 0.6,
                "minimum_counterevidence_signal": 0.25,
                "maximum_bias_risk": 0.75,
            },
            "score_rows": score_rows,
            "execution_state": {
                "quality_score_ledger_schema_recorded": True,
                "source_content_fetched": False,
                "source_quality_scored": False,
                "calibration_usable_sources_selected": False,
                "calibration_intervals_computed": False,
                "probability_pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Quality score ledger schema records how post-fetch source scores will be stored. "
                "It does not score sources, select usable sources, or compute calibration intervals."
            ),
        },
        "warning": "Quality score ledger schema is not a scored source ledger.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_checks(
    ontological_soundness_bad_god_evidential_calibration_source_quality_rubric: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_schema: dict[str, Any] | None = None,
) -> dict[str, Any]:
    rubric_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_quality_rubric
        or _build_ontological_soundness_bad_god_evidential_calibration_source_quality_rubric()
    )
    schema_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_schema
        or _build_ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_schema(rubric_doc)
    )
    rubric = rubric_doc["rubric"]
    schema = schema_doc["schema"]
    rubric_source_ids = {row["source_id"] for row in rubric["source_score_templates"]}
    score_row_source_ids = {row["source_id"] for row in schema["score_rows"]}
    required_fields = set(schema["required_score_fields"])
    expected_fields = {
        "source_id",
        "source_family_id",
        "dimension_scores",
        "weighted_quality_score",
        "usable_for_calibration",
        "score_rationale",
        "scored_at",
    }
    checks = [
        {
            "id": "check-quality-rubric-linked",
            "status": "complete" if schema["input_quality_rubric_id"] == rubric["id"] else "open",
            "input_quality_rubric_id": schema["input_quality_rubric_id"],
            "quality_rubric_id": rubric["id"],
        },
        {
            "id": "check-score-rows-cover-rubric-templates",
            "status": "complete" if score_row_source_ids == rubric_source_ids else "open",
            "score_row_source_ids": sorted(score_row_source_ids),
            "rubric_source_ids": sorted(rubric_source_ids),
        },
        {
            "id": "check-required-score-fields-present",
            "status": "complete" if expected_fields.issubset(required_fields) else "open",
            "required_score_fields": schema["required_score_fields"],
        },
        {
            "id": "check-score-ledger-not-scored",
            "status": "complete"
            if all(row["score_status"] == "schema_defined_not_scored" for row in schema["score_rows"])
            and schema["execution_state"]["source_quality_scored"] is False
            else "open",
            "score_statuses": [row["score_status"] for row in schema["score_rows"]],
        },
        {
            "id": "check-quality-score-ledger-schema-not-proof",
            "status": "contested"
            if schema_doc["status"] == "contested"
            and schema["execution_state"]["calibration_intervals_computed"] is False
            and schema["execution_state"]["proof_claim_allowed"] is False
            else "open",
            "execution_state": schema["execution_state"],
            "decision_rule": schema["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_task_id": schema["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_quality_score_ledger_schema_not_proof",
        "checks": checks,
        "remaining_risks": [
            "source quality scores are not computed",
            "usable calibration sources are not selected",
            "quality score ledger has not produced calibration intervals",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_ledger(
    ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_schema: dict[str, Any] | None = None,
) -> dict[str, Any]:
    schema_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_schema
        or _build_ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_schema()
    )
    schema = schema_doc["schema"]
    dimension_ids = list(schema["score_rows"][0]["dimension_scores"].keys()) if schema["score_rows"] else []
    required_content_fields = [
        "retrieval_log_id",
        "content_sha256",
        "content_path",
        "fetched_at",
    ]
    dry_run_rows = []
    for row in schema["score_rows"]:
        dry_run_rows.append({
            "source_id": row["source_id"],
            "source_family_id": row["source_family_id"],
            "url": row["url"],
            "dimension_ids": dimension_ids,
            "required_content_fields": required_content_fields,
            "score_input_ready": False,
            "scoring_command_template": (
                "score-source-quality --source-id {source_id} "
                "--quality-score-schema ontological-soundness-bad-god-evidential-calibration-source-quality-score-ledger-schema-v0"
            ),
            "scoring_status": "dry_run_not_scored",
            "weighted_quality_score": None,
            "usable_for_calibration": False,
            "score_output_path": None,
            "proof_evidence_materialized": False,
        })
    return {
        "status": "contested",
        "ledger": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-quality-score-dry-run-ledger-v0",
            "input_quality_score_schema_id": schema["id"],
            "target_task_id": schema["target_task_id"],
            "target_pressure_test_id": schema["target_pressure_test_id"],
            "target_remediation_id": schema["target_remediation_id"],
            "ledger_scope": "quality_score_execution_dry_run",
            "retrieved_at": RETRIEVED_AT,
            "required_content_fields": required_content_fields,
            "dry_run_rows": dry_run_rows,
            "execution_state": {
                "quality_score_dry_run_recorded": True,
                "source_content_fetched": False,
                "source_quality_scored": False,
                "calibration_usable_sources_selected": False,
                "calibration_intervals_computed": False,
                "probability_pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Dry-run ledger records scoring commands and required content fields only. "
                "It cannot score source quality before retrieval logs and content hashes exist."
            ),
        },
        "warning": "Quality score dry-run ledger is not scored evidence.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_checks(
    ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_schema: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    schema_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_schema
        or _build_ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_schema()
    )
    ledger_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_ledger
        or _build_ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_ledger(schema_doc)
    )
    schema = schema_doc["schema"]
    ledger = ledger_doc["ledger"]
    schema_source_ids = {row["source_id"] for row in schema["score_rows"]}
    dry_run_source_ids = {row["source_id"] for row in ledger["dry_run_rows"]}
    checks = [
        {
            "id": "check-quality-score-schema-linked",
            "status": "complete" if ledger["input_quality_score_schema_id"] == schema["id"] else "open",
            "input_quality_score_schema_id": ledger["input_quality_score_schema_id"],
            "quality_score_schema_id": schema["id"],
        },
        {
            "id": "check-dry-run-rows-cover-score-schema",
            "status": "complete" if dry_run_source_ids == schema_source_ids else "open",
            "dry_run_source_ids": sorted(dry_run_source_ids),
            "schema_source_ids": sorted(schema_source_ids),
        },
        {
            "id": "check-score-inputs-not-ready",
            "status": "complete"
            if all(row["score_input_ready"] is False for row in ledger["dry_run_rows"])
            and ledger["execution_state"]["source_content_fetched"] is False
            else "open",
            "score_input_ready_count": sum(1 for row in ledger["dry_run_rows"] if row["score_input_ready"] is True),
        },
        {
            "id": "check-quality-score-dry-run-not-scored",
            "status": "complete"
            if all(row["scoring_status"] == "dry_run_not_scored" for row in ledger["dry_run_rows"])
            and ledger["execution_state"]["source_quality_scored"] is False
            else "open",
            "scoring_statuses": [row["scoring_status"] for row in ledger["dry_run_rows"]],
        },
        {
            "id": "check-quality-score-dry-run-not-proof",
            "status": "contested"
            if ledger_doc["status"] == "contested"
            and ledger["execution_state"]["calibration_intervals_computed"] is False
            and ledger["execution_state"]["proof_claim_allowed"] is False
            else "open",
            "execution_state": ledger["execution_state"],
            "decision_rule": ledger["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_task_id": ledger["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_quality_score_dry_run_not_proof",
        "checks": checks,
        "remaining_risks": [
            "source retrieval logs and hashes are not materialized",
            "quality scoring has not run",
            "calibration intervals remain uncomputed",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_gate(
    ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ledger_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_ledger
        or _build_ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_ledger()
    )
    ledger = ledger_doc["ledger"]
    required_materialized_inputs = [
        "retrieval_log_id",
        "content_sha256",
        "content_path",
        "fetched_at",
    ]
    readiness_rows = []
    for row in ledger["dry_run_rows"]:
        readiness_rows.append({
            "source_id": row["source_id"],
            "source_family_id": row["source_family_id"],
            "url": row["url"],
            "required_materialized_inputs": required_materialized_inputs,
            "missing_materialized_inputs": required_materialized_inputs,
            "ready_for_scoring": False,
            "blocking_reason": "source_content_not_fetched",
            "scoring_status": "blocked_before_scoring",
            "proof_evidence_materialized": False,
        })
    return {
        "status": "blocked",
        "gate": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-quality-score-readiness-gate-v0",
            "input_quality_score_dry_run_ledger_id": ledger["id"],
            "target_task_id": ledger["target_task_id"],
            "target_pressure_test_id": ledger["target_pressure_test_id"],
            "target_remediation_id": ledger["target_remediation_id"],
            "gate_scope": "quality_score_execution_readiness",
            "retrieved_at": RETRIEVED_AT,
            "required_materialized_inputs": required_materialized_inputs,
            "ready_for_quality_scoring": False,
            "blocking_reason": "source_content_not_fetched",
            "readiness_rows": readiness_rows,
            "execution_state": {
                "quality_score_readiness_gate_recorded": True,
                "source_content_fetched": False,
                "source_quality_scored": False,
                "calibration_usable_sources_selected": False,
                "calibration_intervals_computed": False,
                "probability_pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Quality scoring may run only after every selected source has a retrieval log, "
                "content hash, content path, and fetch timestamp."
            ),
        },
        "warning": "Readiness gate blocks quality scoring and is not proof evidence.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_checks(
    ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_ledger: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_gate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ledger_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_ledger
        or _build_ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_ledger()
    )
    gate_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_gate
        or _build_ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_gate(ledger_doc)
    )
    ledger = ledger_doc["ledger"]
    gate = gate_doc["gate"]
    dry_run_source_ids = {row["source_id"] for row in ledger["dry_run_rows"]}
    readiness_source_ids = {row["source_id"] for row in gate["readiness_rows"]}
    checks = [
        {
            "id": "check-quality-score-dry-run-linked",
            "status": "complete" if gate["input_quality_score_dry_run_ledger_id"] == ledger["id"] else "open",
            "input_quality_score_dry_run_ledger_id": gate["input_quality_score_dry_run_ledger_id"],
            "quality_score_dry_run_ledger_id": ledger["id"],
        },
        {
            "id": "check-readiness-rows-cover-dry-run",
            "status": "complete" if readiness_source_ids == dry_run_source_ids else "open",
            "readiness_source_ids": sorted(readiness_source_ids),
            "dry_run_source_ids": sorted(dry_run_source_ids),
        },
        {
            "id": "check-materialized-inputs-missing",
            "status": "blocked"
            if all(row["missing_materialized_inputs"] for row in gate["readiness_rows"])
            and gate["execution_state"]["source_content_fetched"] is False
            else "open",
            "required_materialized_inputs": gate["required_materialized_inputs"],
        },
        {
            "id": "check-quality-scoring-blocked",
            "status": "blocked"
            if gate["ready_for_quality_scoring"] is False
            and all(row["ready_for_scoring"] is False for row in gate["readiness_rows"])
            else "open",
            "ready_for_quality_scoring": gate["ready_for_quality_scoring"],
            "blocking_reason": gate["blocking_reason"],
        },
        {
            "id": "check-readiness-gate-not-proof",
            "status": "contested"
            if gate["execution_state"]["calibration_intervals_computed"] is False
            and gate["execution_state"]["proof_claim_allowed"] is False
            else "open",
            "execution_state": gate["execution_state"],
            "decision_rule": gate["decision_rule"],
        },
    ]
    return {
        "status": "blocked",
        "target_task_id": gate["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_quality_score_readiness_gate",
        "checks": checks,
        "remaining_risks": [
            "source content still has not been fetched",
            "quality scoring is intentionally blocked",
            "proof claim remains blocked by ontological soundness",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_packet(
    ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_gate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    retrieval_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger
        or _build_ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger()
    )
    gate_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_gate
        or _build_ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_gate()
    )
    retrieval = retrieval_doc["ledger"]
    gate = gate_doc["gate"]
    readiness_by_source_id = {row["source_id"]: row for row in gate["readiness_rows"]}
    required_materialized_outputs = [
        "retrieval_log_id",
        "content_sha256",
        "content_path",
        "fetched_at",
    ]
    materialization_rows = []
    for row in retrieval["dry_run_rows"]:
        readiness_row = readiness_by_source_id[row["source_id"]]
        materialization_rows.append({
            "source_id": row["source_id"],
            "source_family_id": row["source_family_id"],
            "url": row["url"],
            "fetch_command_template": row["fetch_command_template"],
            "hash_command_template": row["hash_command_template"],
            "expected_content_path": row["raw_output_path"],
            "expected_hash_output_path": row["hash_output_path"],
            "expected_log_output_path": row["log_output_path"],
            "transcript_event_name": row["transcript_event_name"],
            "readiness_blocking_reason": readiness_row["blocking_reason"],
            "required_materialized_outputs": required_materialized_outputs,
            "retrieval_log_id": None,
            "content_sha256": None,
            "content_path": None,
            "fetched_at": None,
            "materialization_status": "queued_not_materialized",
            "proof_evidence_materialized": False,
        })
    return {
        "status": "contested",
        "packet": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-packet-v0",
            "input_retrieval_dry_run_ledger_id": retrieval["id"],
            "input_quality_score_readiness_gate_id": gate["id"],
            "target_task_id": retrieval["target_task_id"],
            "target_pressure_test_id": retrieval["target_pressure_test_id"],
            "target_remediation_id": retrieval["target_remediation_id"],
            "packet_scope": "retrieval_content_materialization_pre_execution_packet",
            "retrieved_at": RETRIEVED_AT,
            "required_materialized_outputs": required_materialized_outputs,
            "materialization_rows": materialization_rows,
            "execution_state": {
                "content_materialization_packet_recorded": True,
                "retrieval_executed": False,
                "retrieval_logs_materialized": False,
                "source_hashes_materialized": False,
                "source_content_fetched": False,
                "source_quality_scored": False,
                "calibration_intervals_computed": False,
                "probability_pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Content materialization packet binds retrieval commands to expected logs, hashes, and paths. "
                "It is still pre-execution and does not fetch source content."
            ),
        },
        "warning": "Content materialization packet is an execution packet, not proof evidence.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_checks(
    ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_gate: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_packet: dict[str, Any] | None = None,
) -> dict[str, Any]:
    retrieval_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger
        or _build_ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger()
    )
    gate_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_gate
        or _build_ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_gate()
    )
    packet_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_packet
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_packet(
            retrieval_doc,
            gate_doc,
        )
    )
    retrieval = retrieval_doc["ledger"]
    gate = gate_doc["gate"]
    packet = packet_doc["packet"]
    retrieval_source_ids = {row["source_id"] for row in retrieval["dry_run_rows"]}
    readiness_source_ids = {row["source_id"] for row in gate["readiness_rows"]}
    materialization_source_ids = {row["source_id"] for row in packet["materialization_rows"]}
    checks = [
        {
            "id": "check-retrieval-dry-run-linked",
            "status": "complete" if packet["input_retrieval_dry_run_ledger_id"] == retrieval["id"] else "open",
            "input_retrieval_dry_run_ledger_id": packet["input_retrieval_dry_run_ledger_id"],
            "retrieval_dry_run_ledger_id": retrieval["id"],
        },
        {
            "id": "check-readiness-gate-linked",
            "status": "complete" if packet["input_quality_score_readiness_gate_id"] == gate["id"] else "open",
            "input_quality_score_readiness_gate_id": packet["input_quality_score_readiness_gate_id"],
            "quality_score_readiness_gate_id": gate["id"],
        },
        {
            "id": "check-materialization-rows-cover-readiness-gate",
            "status": "complete"
            if materialization_source_ids == readiness_source_ids == retrieval_source_ids
            else "open",
            "materialization_source_ids": sorted(materialization_source_ids),
            "readiness_source_ids": sorted(readiness_source_ids),
            "retrieval_source_ids": sorted(retrieval_source_ids),
        },
        {
            "id": "check-materialization-packet-not-executed",
            "status": "complete"
            if all(row["materialization_status"] == "queued_not_materialized" for row in packet["materialization_rows"])
            and packet["execution_state"]["retrieval_executed"] is False
            and packet["execution_state"]["source_content_fetched"] is False
            else "open",
            "materialization_statuses": [row["materialization_status"] for row in packet["materialization_rows"]],
        },
        {
            "id": "check-materialization-packet-not-proof",
            "status": "contested"
            if packet_doc["status"] == "contested"
            and packet["execution_state"]["calibration_intervals_computed"] is False
            and packet["execution_state"]["proof_claim_allowed"] is False
            else "open",
            "execution_state": packet["execution_state"],
            "decision_rule": packet["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_task_id": packet["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_content_materialization_packet_not_proof",
        "checks": checks,
        "remaining_risks": [
            "content retrieval has not been executed",
            "retrieval logs and hashes remain unmaterialized",
            "quality scoring remains blocked until source content exists",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_plan(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_packet: dict[str, Any] | None = None,
) -> dict[str, Any]:
    packet_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_packet
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_packet()
    )
    packet = packet_doc["packet"]
    max_batch_size = 3
    rows = packet["materialization_rows"]
    batches = []
    for batch_index, start in enumerate(range(0, len(rows), max_batch_size), start=1):
        batch_rows = rows[start:start + max_batch_size]
        batches.append({
            "batch_id": f"content-materialization-batch-{batch_index:02d}",
            "batch_order": batch_index,
            "source_ids": [row["source_id"] for row in batch_rows],
            "source_family_ids": [row["source_family_id"] for row in batch_rows],
            "expected_content_paths": [row["expected_content_path"] for row in batch_rows],
            "expected_hash_output_paths": [row["expected_hash_output_path"] for row in batch_rows],
            "expected_log_output_paths": [row["expected_log_output_path"] for row in batch_rows],
            "batch_status": "batch_queued_not_executed",
            "batch_requires_network": True,
            "materialization_output_count": 0,
            "proof_evidence_materialized": False,
        })
    return {
        "status": "contested",
        "batch_plan": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-batch-plan-v0",
            "input_content_materialization_packet_id": packet["id"],
            "target_task_id": packet["target_task_id"],
            "target_pressure_test_id": packet["target_pressure_test_id"],
            "target_remediation_id": packet["target_remediation_id"],
            "batch_scope": "retrieval_content_materialization_batches",
            "retrieved_at": RETRIEVED_AT,
            "max_batch_size": max_batch_size,
            "batches": batches,
            "execution_state": {
                "content_materialization_batch_plan_recorded": True,
                "retrieval_executed": False,
                "retrieval_logs_materialized": False,
                "source_hashes_materialized": False,
                "source_content_fetched": False,
                "source_quality_scored": False,
                "calibration_intervals_computed": False,
                "probability_pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Batch plan chunks content materialization into auditable execution groups. "
                "Batches are not executed until network retrieval, hashing, and logging are run."
            ),
        },
        "warning": "Content materialization batch plan is execution planning only.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_checks(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_packet: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    packet_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_packet
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_packet()
    )
    plan_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_plan
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_plan(
            packet_doc
        )
    )
    packet = packet_doc["packet"]
    batch_plan = plan_doc["batch_plan"]
    packet_source_ids = {row["source_id"] for row in packet["materialization_rows"]}
    batch_source_ids = {
        source_id
        for batch in batch_plan["batches"]
        for source_id in batch["source_ids"]
    }
    checks = [
        {
            "id": "check-content-materialization-packet-linked",
            "status": "complete"
            if batch_plan["input_content_materialization_packet_id"] == packet["id"]
            else "open",
            "input_content_materialization_packet_id": batch_plan["input_content_materialization_packet_id"],
            "content_materialization_packet_id": packet["id"],
        },
        {
            "id": "check-batches-cover-materialization-rows",
            "status": "complete" if batch_source_ids == packet_source_ids else "open",
            "batch_source_ids": sorted(batch_source_ids),
            "packet_source_ids": sorted(packet_source_ids),
        },
        {
            "id": "check-batch-size-limit",
            "status": "complete"
            if all(1 <= len(batch["source_ids"]) <= batch_plan["max_batch_size"] for batch in batch_plan["batches"])
            else "open",
            "max_batch_size": batch_plan["max_batch_size"],
            "batch_sizes": [len(batch["source_ids"]) for batch in batch_plan["batches"]],
        },
        {
            "id": "check-materialization-batches-not-executed",
            "status": "complete"
            if all(batch["batch_status"] == "batch_queued_not_executed" for batch in batch_plan["batches"])
            and batch_plan["execution_state"]["retrieval_executed"] is False
            and batch_plan["execution_state"]["source_content_fetched"] is False
            else "open",
            "batch_statuses": [batch["batch_status"] for batch in batch_plan["batches"]],
        },
        {
            "id": "check-materialization-batch-plan-not-proof",
            "status": "contested"
            if plan_doc["status"] == "contested"
            and batch_plan["execution_state"]["calibration_intervals_computed"] is False
            and batch_plan["execution_state"]["proof_claim_allowed"] is False
            else "open",
            "execution_state": batch_plan["execution_state"],
            "decision_rule": batch_plan["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_task_id": batch_plan["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_content_materialization_batch_plan_not_proof",
        "checks": checks,
        "remaining_risks": [
            "network retrieval has not run",
            "content hashes and retrieval logs are absent",
            "quality scoring remains blocked until materialization executes",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_packet(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    batch_plan_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_plan
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_plan()
    )
    batch_plan = batch_plan_doc["batch_plan"]
    authorization_rows = []
    for batch in batch_plan["batches"]:
        authorization_rows.append({
            "batch_id": batch["batch_id"],
            "batch_order": batch["batch_order"],
            "source_ids": batch["source_ids"],
            "source_count": len(batch["source_ids"]),
            "batch_requires_network": batch["batch_requires_network"],
            "network_access_allowed": False,
            "authorization_status": "authorization_pending",
            "batch_status": batch["batch_status"],
            "blocking_reason": "network_access_requires_explicit_user_approval",
            "proof_evidence_materialized": False,
        })
    return {
        "status": "blocked",
        "authorization": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-packet-v0",
            "input_content_materialization_batch_plan_id": batch_plan["id"],
            "target_task_id": batch_plan["target_task_id"],
            "target_pressure_test_id": batch_plan["target_pressure_test_id"],
            "target_remediation_id": batch_plan["target_remediation_id"],
            "authorization_scope": "content_materialization_network_authorization",
            "retrieved_at": RETRIEVED_AT,
            "authorization_required": True,
            "authorization_granted": False,
            "blocking_reason": "network_access_requires_explicit_user_approval",
            "authorization_rows": authorization_rows,
            "execution_state": {
                "content_materialization_authorization_packet_recorded": True,
                "network_access_authorized": False,
                "retrieval_executed": False,
                "retrieval_logs_materialized": False,
                "source_hashes_materialized": False,
                "source_content_fetched": False,
                "source_quality_scored": False,
                "calibration_intervals_computed": False,
                "probability_pressure_resolved": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Content materialization batches require explicit user authorization before network retrieval. "
                "Without authorization, no fetch, hash, or retrieval log may be materialized."
            ),
        },
        "warning": "Authorization packet blocks network retrieval and is not proof evidence.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_checks(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_plan: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_packet: dict[str, Any] | None = None,
) -> dict[str, Any]:
    batch_plan_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_plan
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_plan()
    )
    authorization_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_packet
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_packet(
            batch_plan_doc
        )
    )
    batch_plan = batch_plan_doc["batch_plan"]
    authorization = authorization_doc["authorization"]
    batch_ids = {row["batch_id"] for row in batch_plan["batches"]}
    authorization_batch_ids = {row["batch_id"] for row in authorization["authorization_rows"]}
    checks = [
        {
            "id": "check-content-materialization-batch-plan-linked",
            "status": "complete"
            if authorization["input_content_materialization_batch_plan_id"] == batch_plan["id"]
            else "open",
            "input_content_materialization_batch_plan_id": authorization["input_content_materialization_batch_plan_id"],
            "content_materialization_batch_plan_id": batch_plan["id"],
        },
        {
            "id": "check-authorization-rows-cover-batches",
            "status": "complete" if authorization_batch_ids == batch_ids else "open",
            "authorization_batch_ids": sorted(authorization_batch_ids),
            "batch_ids": sorted(batch_ids),
        },
        {
            "id": "check-network-authorization-pending",
            "status": "blocked"
            if authorization["authorization_required"] is True
            and authorization["authorization_granted"] is False
            and all(row["authorization_status"] == "authorization_pending" for row in authorization["authorization_rows"])
            else "open",
            "authorization_required": authorization["authorization_required"],
            "authorization_granted": authorization["authorization_granted"],
        },
        {
            "id": "check-content-materialization-not-authorized",
            "status": "blocked"
            if all(row["network_access_allowed"] is False for row in authorization["authorization_rows"])
            and authorization["execution_state"]["network_access_authorized"] is False
            and authorization["execution_state"]["retrieval_executed"] is False
            else "open",
            "network_access_allowed_count": sum(
                1 for row in authorization["authorization_rows"]
                if row["network_access_allowed"] is True
            ),
        },
        {
            "id": "check-content-materialization-authorization-not-proof",
            "status": "contested"
            if authorization_doc["status"] == "blocked"
            and authorization["execution_state"]["calibration_intervals_computed"] is False
            and authorization["execution_state"]["proof_claim_allowed"] is False
            else "open",
            "execution_state": authorization["execution_state"],
            "decision_rule": authorization["decision_rule"],
        },
    ]
    return {
        "status": "blocked",
        "target_task_id": authorization["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_content_materialization_authorization_required",
        "checks": checks,
        "remaining_risks": [
            "network access has not been authorized",
            "content retrieval cannot execute yet",
            "source quality scoring remains blocked until retrieval outputs exist",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_queue(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_packet: dict[str, Any] | None = None,
) -> dict[str, Any]:
    authorization_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_packet
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_packet()
    )
    authorization = authorization_doc["authorization"]
    review_items = []
    for row in authorization["authorization_rows"]:
        review_items.append({
            "review_id": f"review-{row['batch_id']}",
            "batch_id": row["batch_id"],
            "batch_order": row["batch_order"],
            "source_ids": row["source_ids"],
            "source_count": row["source_count"],
            "blocking_reason": row["blocking_reason"],
            "review_status": "pending_review",
            "required_decision_fields": [
                "network_access_allowed",
                "terms_or_rate_limit_checked",
                "private_or_sensitive_content_risk_checked",
                "retrieval_scope_confirmed",
                "operator_approval_reference",
            ],
            "proposed_decision": "defer_authorization",
            "network_access_allowed": False,
            "materialization_status": "authorization_review_queue_not_evidence",
            "proof_evidence_materialized": False,
        })
    return {
        "status": "blocked",
        "queue": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-queue-v0",
            "input_authorization_packet_id": authorization["id"],
            "target_task_id": authorization["target_task_id"],
            "target_pressure_test_id": authorization["target_pressure_test_id"],
            "target_remediation_id": authorization["target_remediation_id"],
            "review_scope": "content_materialization_authorization_review",
            "review_mode": "queued_authorization_review_not_performed_not_approved",
            "retrieved_at": RETRIEVED_AT,
            "review_items": review_items,
            "authorization_state": {
                "review_queue_recorded": True,
                "authorization_reviews_completed": False,
                "authorization_granted": False,
                "network_access_authorized": False,
                "retrieval_executed": False,
                "source_content_fetched": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Authorization review queue records what a human operator must approve. "
                "It does not grant network access or materialize source evidence."
            ),
        },
        "warning": "Authorization review queue is not an approval decision.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_checks(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_packet: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_queue: dict[str, Any] | None = None,
) -> dict[str, Any]:
    authorization_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_packet
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_packet()
    )
    queue_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_queue
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_queue(
            authorization_doc
        )
    )
    authorization = authorization_doc["authorization"]
    queue = queue_doc["queue"]
    authorization_batch_ids = {row["batch_id"] for row in authorization["authorization_rows"]}
    review_batch_ids = {row["batch_id"] for row in queue["review_items"]}
    checks = [
        {
            "id": "check-authorization-packet-linked",
            "status": "complete" if queue["input_authorization_packet_id"] == authorization["id"] else "open",
            "input_authorization_packet_id": queue["input_authorization_packet_id"],
            "authorization_packet_id": authorization["id"],
        },
        {
            "id": "check-review-items-cover-authorization-rows",
            "status": "complete" if review_batch_ids == authorization_batch_ids else "open",
            "review_batch_ids": sorted(review_batch_ids),
            "authorization_batch_ids": sorted(authorization_batch_ids),
        },
        {
            "id": "check-authorization-review-items-remain-unreviewed",
            "status": "complete"
            if all(item["review_status"] == "pending_review" for item in queue["review_items"])
            and queue["authorization_state"]["authorization_reviews_completed"] is False
            else "open",
            "review_statuses": [item["review_status"] for item in queue["review_items"]],
        },
        {
            "id": "check-authorization-review-not-granted",
            "status": "blocked"
            if queue["authorization_state"]["authorization_granted"] is False
            and queue["authorization_state"]["network_access_authorized"] is False
            and all(item["network_access_allowed"] is False for item in queue["review_items"])
            else "open",
            "authorization_state": queue["authorization_state"],
        },
        {
            "id": "check-authorization-review-queue-not-proof",
            "status": "contested"
            if queue_doc["status"] == "blocked"
            and queue["authorization_state"]["proof_claim_allowed"] is False
            and all(
                item["materialization_status"] == "authorization_review_queue_not_evidence"
                for item in queue["review_items"]
            )
            else "open",
            "authorization_state": queue["authorization_state"],
            "decision_rule": queue["decision_rule"],
        },
    ]
    return {
        "status": "blocked",
        "target_task_id": queue["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_content_materialization_authorization_review_unperformed",
        "checks": checks,
        "remaining_risks": [
            "authorization review has not been performed",
            "network access remains unauthorized",
            "source retrieval outputs remain absent",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_queue: dict[str, Any] | None = None,
) -> dict[str, Any]:
    queue_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_queue
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_queue()
    )
    queue = queue_doc["queue"]
    review_criteria = [
        {
            "criterion_id": "terms_or_rate_limit_checked",
            "required_for_authorization": True,
            "description": "source terms, robots guidance, and practical rate limits are checked before fetch",
        },
        {
            "criterion_id": "private_or_sensitive_content_risk_checked",
            "required_for_authorization": True,
            "description": "candidate fetch is limited to public non-secret material and avoids personal data",
        },
        {
            "criterion_id": "retrieval_scope_confirmed",
            "required_for_authorization": True,
            "description": "fetch scope matches the queued source URLs and does not expand silently",
        },
        {
            "criterion_id": "logging_and_hashing_plan_verified",
            "required_for_authorization": True,
            "description": "retrieval log, content path, hash path, and transcript event targets are verified",
        },
        {
            "criterion_id": "operator_approval_reference_present",
            "required_for_authorization": True,
            "description": "explicit operator approval is recorded before network retrieval",
        },
    ]
    review_templates = []
    for item in queue["review_items"]:
        review_templates.append({
            "review_id": item["review_id"],
            "batch_id": item["batch_id"],
            "source_ids": item["source_ids"],
            "criterion_results": {
                criterion["criterion_id"]: None
                for criterion in review_criteria
            },
            "rubric_status": "rubric_defined_not_applied",
            "authorization_decision": None,
            "network_access_allowed": False,
            "proof_evidence_materialized": False,
        })
    return {
        "status": "contested",
        "rubric": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-rubric-v0",
            "input_authorization_review_queue_id": queue["id"],
            "target_task_id": queue["target_task_id"],
            "target_pressure_test_id": queue["target_pressure_test_id"],
            "target_remediation_id": queue["target_remediation_id"],
            "rubric_scope": "content_materialization_authorization_review_scoring",
            "retrieved_at": RETRIEVED_AT,
            "review_criteria": review_criteria,
            "review_templates": review_templates,
            "execution_state": {
                "authorization_review_rubric_recorded": True,
                "authorization_reviews_completed": False,
                "authorization_granted": False,
                "network_access_authorized": False,
                "retrieval_executed": False,
                "source_content_fetched": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Authorization review rubric defines required checks only. "
                "It grants no network access until applied decisions are recorded."
            ),
        },
        "warning": "Authorization review rubric is not an authorization decision.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric_checks(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_queue: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric: dict[str, Any] | None = None,
) -> dict[str, Any]:
    queue_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_queue
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_queue()
    )
    rubric_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric(
            queue_doc
        )
    )
    queue = queue_doc["queue"]
    rubric = rubric_doc["rubric"]
    queue_review_ids = {item["review_id"] for item in queue["review_items"]}
    rubric_review_ids = {item["review_id"] for item in rubric["review_templates"]}
    expected_criteria = {
        "terms_or_rate_limit_checked",
        "private_or_sensitive_content_risk_checked",
        "retrieval_scope_confirmed",
        "logging_and_hashing_plan_verified",
        "operator_approval_reference_present",
    }
    criterion_ids = {item["criterion_id"] for item in rubric["review_criteria"]}
    checks = [
        {
            "id": "check-authorization-review-queue-linked",
            "status": "complete" if rubric["input_authorization_review_queue_id"] == queue["id"] else "open",
            "input_authorization_review_queue_id": rubric["input_authorization_review_queue_id"],
            "authorization_review_queue_id": queue["id"],
        },
        {
            "id": "check-review-criteria-complete",
            "status": "complete" if criterion_ids == expected_criteria else "open",
            "criterion_ids": sorted(criterion_ids),
            "expected_criteria": sorted(expected_criteria),
        },
        {
            "id": "check-review-templates-cover-queue",
            "status": "complete" if rubric_review_ids == queue_review_ids else "open",
            "rubric_review_ids": sorted(rubric_review_ids),
            "queue_review_ids": sorted(queue_review_ids),
        },
        {
            "id": "check-authorization-rubric-not-applied",
            "status": "complete"
            if all(item["rubric_status"] == "rubric_defined_not_applied" for item in rubric["review_templates"])
            and rubric["execution_state"]["authorization_reviews_completed"] is False
            else "open",
            "rubric_statuses": [item["rubric_status"] for item in rubric["review_templates"]],
        },
        {
            "id": "check-authorization-review-rubric-not-proof",
            "status": "contested"
            if rubric_doc["status"] == "contested"
            and rubric["execution_state"]["authorization_granted"] is False
            and rubric["execution_state"]["proof_claim_allowed"] is False
            else "open",
            "execution_state": rubric["execution_state"],
            "decision_rule": rubric["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_task_id": rubric["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric_not_applied",
        "checks": checks,
        "remaining_risks": [
            "authorization rubric has not been applied",
            "operator approval remains absent",
            "network retrieval remains unauthorized",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decisions(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric: dict[str, Any] | None = None,
) -> dict[str, Any]:
    rubric_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric()
    )
    rubric = rubric_doc["rubric"]
    decision_rows = []
    for template in rubric["review_templates"]:
        decision_rows.append({
            "review_id": template["review_id"],
            "batch_id": template["batch_id"],
            "source_ids": template["source_ids"],
            "rubric_applied": True,
            "criterion_results": {
                criterion["criterion_id"]: False
                for criterion in rubric["review_criteria"]
            },
            "decision_status": "review_deferred",
            "authorization_decision": "not_authorized_until_operator_approval_and_fetch_risks_reviewed",
            "network_access_allowed": False,
            "retrieval_may_execute": False,
            "decision_rationale": (
                "Rubric criteria require explicit operator approval plus terms, privacy, scope, "
                "logging, and hashing checks before network retrieval."
            ),
            "proof_evidence_materialized": False,
        })
    return {
        "status": "blocked",
        "decisions": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-decisions-v0",
            "input_authorization_review_rubric_id": rubric["id"],
            "target_task_id": rubric["target_task_id"],
            "target_pressure_test_id": rubric["target_pressure_test_id"],
            "target_remediation_id": rubric["target_remediation_id"],
            "decision_scope": "content_materialization_authorization_review_decisions",
            "retrieved_at": RETRIEVED_AT,
            "decision_rows": decision_rows,
            "authorization_state": {
                "authorization_review_decisions_recorded": True,
                "authorization_granted": False,
                "network_access_authorized": False,
                "retrieval_executed": False,
                "source_content_fetched": False,
                "source_quality_scored": False,
                "calibration_intervals_computed": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "All authorization decisions defer network access until required operator approval "
                "and source-specific safety checks are materialized."
            ),
        },
        "warning": "Authorization review decisions deny network retrieval and are not proof evidence.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decision_checks(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decisions: dict[str, Any] | None = None,
) -> dict[str, Any]:
    rubric_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric()
    )
    decisions_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decisions
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decisions(
            rubric_doc
        )
    )
    rubric = rubric_doc["rubric"]
    decisions = decisions_doc["decisions"]
    rubric_review_ids = {row["review_id"] for row in rubric["review_templates"]}
    decision_review_ids = {row["review_id"] for row in decisions["decision_rows"]}
    checks = [
        {
            "id": "check-authorization-review-rubric-linked",
            "status": "complete"
            if decisions["input_authorization_review_rubric_id"] == rubric["id"]
            else "open",
            "input_authorization_review_rubric_id": decisions["input_authorization_review_rubric_id"],
            "authorization_review_rubric_id": rubric["id"],
        },
        {
            "id": "check-decision-rows-cover-rubric-templates",
            "status": "complete" if decision_review_ids == rubric_review_ids else "open",
            "decision_review_ids": sorted(decision_review_ids),
            "rubric_review_ids": sorted(rubric_review_ids),
        },
        {
            "id": "check-authorization-decisions-defer-network",
            "status": "blocked"
            if all(row["decision_status"] == "review_deferred" for row in decisions["decision_rows"])
            and all(row["authorization_decision"].startswith("not_authorized_until_") for row in decisions["decision_rows"])
            else "open",
            "authorization_decisions": [row["authorization_decision"] for row in decisions["decision_rows"]],
        },
        {
            "id": "check-network-access-remains-denied",
            "status": "blocked"
            if all(row["network_access_allowed"] is False for row in decisions["decision_rows"])
            and decisions["authorization_state"]["network_access_authorized"] is False
            and decisions["authorization_state"]["retrieval_executed"] is False
            else "open",
            "network_access_allowed_count": sum(
                1 for row in decisions["decision_rows"]
                if row["network_access_allowed"] is True
            ),
        },
        {
            "id": "check-authorization-review-decisions-not-proof",
            "status": "contested"
            if decisions_doc["status"] == "blocked"
            and decisions["authorization_state"]["calibration_intervals_computed"] is False
            and decisions["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": decisions["authorization_state"],
            "decision_rule": decisions["decision_rule"],
        },
    ]
    return {
        "status": "blocked",
        "target_task_id": decisions["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_content_materialization_authorization_review_decisions_deferred",
        "checks": checks,
        "remaining_risks": [
            "operator approval remains missing",
            "network access remains denied",
            "source retrieval outputs remain absent",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decisions: dict[str, Any] | None = None,
) -> dict[str, Any]:
    decisions_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decisions
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decisions()
    )
    decisions = decisions_doc["decisions"]
    required_resolution_actions = [
        "operator_approval_reference_present",
        "terms_or_rate_limit_checked",
        "private_or_sensitive_content_risk_checked",
        "retrieval_scope_confirmed",
        "logging_and_hashing_plan_verified",
    ]
    resolution_items = []
    for row in decisions["decision_rows"]:
        resolution_items.append({
            "resolution_id": f"authorization-resolution-{row['batch_id']}",
            "review_id": row["review_id"],
            "batch_id": row["batch_id"],
            "source_ids": row["source_ids"],
            "authorization_decision": row["authorization_decision"],
            "required_resolution_actions": required_resolution_actions,
            "completed_resolution_actions": [],
            "resolution_status": "open",
            "authorization_ready": False,
            "network_access_allowed": False,
            "retrieval_may_execute": False,
            "proof_evidence_materialized": False,
        })
    return {
        "status": "blocked",
        "resolution": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-resolution-packet-v0",
            "input_authorization_review_decisions_id": decisions["id"],
            "target_task_id": decisions["target_task_id"],
            "target_pressure_test_id": decisions["target_pressure_test_id"],
            "target_remediation_id": decisions["target_remediation_id"],
            "resolution_scope": "content_materialization_authorization_prerequisite_resolution",
            "retrieved_at": RETRIEVED_AT,
            "required_resolution_actions": required_resolution_actions,
            "resolution_items": resolution_items,
            "authorization_state": {
                "authorization_resolution_packet_recorded": True,
                "authorization_prerequisites_resolved": False,
                "authorization_granted": False,
                "network_access_authorized": False,
                "retrieval_executed": False,
                "source_content_fetched": False,
                "source_quality_scored": False,
                "calibration_intervals_computed": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Open resolution items must close every required authorization prerequisite before "
                "network access, retrieval, or proof-evidence materialization may occur."
            ),
        },
        "warning": "Authorization resolution is queued but unresolved; this is not proof evidence.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_checks(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decisions: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet: dict[str, Any] | None = None,
) -> dict[str, Any]:
    decisions_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decisions
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decisions()
    )
    packet_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet(
            decisions_doc
        )
    )
    decisions = decisions_doc["decisions"]
    resolution = packet_doc["resolution"]
    decision_review_ids = {row["review_id"] for row in decisions["decision_rows"]}
    resolution_review_ids = {row["review_id"] for row in resolution["resolution_items"]}
    checks = [
        {
            "id": "check-authorization-review-decisions-linked",
            "status": "complete"
            if resolution["input_authorization_review_decisions_id"] == decisions["id"]
            else "open",
            "input_authorization_review_decisions_id": resolution["input_authorization_review_decisions_id"],
            "authorization_review_decisions_id": decisions["id"],
        },
        {
            "id": "check-resolution-items-cover-decisions",
            "status": "complete" if resolution_review_ids == decision_review_ids else "open",
            "resolution_review_ids": sorted(resolution_review_ids),
            "decision_review_ids": sorted(decision_review_ids),
        },
        {
            "id": "check-required-resolution-actions-present",
            "status": "complete"
            if all(
                item["required_resolution_actions"] == resolution["required_resolution_actions"]
                for item in resolution["resolution_items"]
            )
            and all(not item["completed_resolution_actions"] for item in resolution["resolution_items"])
            else "open",
            "required_resolution_actions": resolution["required_resolution_actions"],
        },
        {
            "id": "check-authorization-resolution-open",
            "status": "blocked"
            if all(item["resolution_status"] == "open" for item in resolution["resolution_items"])
            and resolution["authorization_state"]["authorization_prerequisites_resolved"] is False
            and resolution["authorization_state"]["authorization_granted"] is False
            else "open",
            "open_resolution_count": sum(
                1 for item in resolution["resolution_items"]
                if item["resolution_status"] == "open"
            ),
        },
        {
            "id": "check-authorization-resolution-not-proof",
            "status": "contested"
            if packet_doc["status"] == "blocked"
            and resolution["authorization_state"]["proof_evidence_materialized"] is False
            and resolution["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": resolution["authorization_state"],
            "decision_rule": resolution["decision_rule"],
        },
    ]
    return {
        "status": "blocked",
        "target_task_id": resolution["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_content_materialization_authorization_resolution_open",
        "checks": checks,
        "remaining_risks": [
            "authorization prerequisites remain unresolved",
            "operator approval remains absent",
            "network access and retrieval remain denied",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_operator_approval_request(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolution_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet()
    )
    resolution = resolution_doc["resolution"]
    approval_items = []
    for item in resolution["resolution_items"]:
        approval_items.append({
            "approval_item_id": f"operator-approval-{item['batch_id']}",
            "resolution_id": item["resolution_id"],
            "review_id": item["review_id"],
            "batch_id": item["batch_id"],
            "source_ids": item["source_ids"],
            "required_action": "record_operator_approval_reference",
            "approval_status": "requested_not_granted",
            "operator_approval_reference": None,
            "authorization_ready": False,
            "network_access_allowed": False,
            "retrieval_may_execute": False,
            "proof_evidence_materialized": False,
        })
    return {
        "status": "blocked",
        "approval_request": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-operator-approval-request-v0",
            "input_authorization_resolution_packet_id": resolution["id"],
            "target_task_id": resolution["target_task_id"],
            "target_pressure_test_id": resolution["target_pressure_test_id"],
            "target_remediation_id": resolution["target_remediation_id"],
            "request_scope": "content_materialization_operator_approval_reference",
            "retrieved_at": RETRIEVED_AT,
            "operator_approval_reference": None,
            "approval_status": "requested_not_granted",
            "approval_items": approval_items,
            "authorization_state": {
                "operator_approval_requested": True,
                "operator_approval_reference_recorded": False,
                "authorization_prerequisites_resolved": False,
                "authorization_granted": False,
                "network_access_authorized": False,
                "retrieval_executed": False,
                "source_content_fetched": False,
                "source_quality_scored": False,
                "calibration_intervals_computed": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "A concrete operator approval reference is required before source materialization "
                "authorization can advance beyond requested_not_granted."
            ),
        },
        "warning": "Operator approval has been requested but not granted; retrieval remains denied.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_operator_approval_checks(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_operator_approval_request: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolution_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet()
    )
    request_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_operator_approval_request
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_operator_approval_request(
            resolution_doc
        )
    )
    resolution = resolution_doc["resolution"]
    approval_request = request_doc["approval_request"]
    resolution_ids = {item["resolution_id"] for item in resolution["resolution_items"]}
    approval_resolution_ids = {item["resolution_id"] for item in approval_request["approval_items"]}
    checks = [
        {
            "id": "check-authorization-resolution-packet-linked",
            "status": "complete"
            if approval_request["input_authorization_resolution_packet_id"] == resolution["id"]
            else "open",
            "input_authorization_resolution_packet_id": approval_request["input_authorization_resolution_packet_id"],
            "authorization_resolution_packet_id": resolution["id"],
        },
        {
            "id": "check-operator-approval-items-cover-resolution-items",
            "status": "complete" if approval_resolution_ids == resolution_ids else "open",
            "approval_resolution_ids": sorted(approval_resolution_ids),
            "resolution_ids": sorted(resolution_ids),
        },
        {
            "id": "check-operator-approval-reference-missing",
            "status": "blocked"
            if approval_request["operator_approval_reference"] is None
            and approval_request["authorization_state"]["operator_approval_reference_recorded"] is False
            else "open",
            "approval_status": approval_request["approval_status"],
            "operator_approval_reference": approval_request["operator_approval_reference"],
        },
        {
            "id": "check-operator-approval-denies-network",
            "status": "blocked"
            if all(item["network_access_allowed"] is False for item in approval_request["approval_items"])
            and approval_request["authorization_state"]["network_access_authorized"] is False
            and approval_request["authorization_state"]["retrieval_executed"] is False
            else "open",
            "network_access_allowed_count": sum(
                1 for item in approval_request["approval_items"]
                if item["network_access_allowed"] is True
            ),
        },
        {
            "id": "check-operator-approval-request-not-proof",
            "status": "contested"
            if request_doc["status"] == "blocked"
            and approval_request["authorization_state"]["proof_evidence_materialized"] is False
            and approval_request["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": approval_request["authorization_state"],
            "decision_rule": approval_request["decision_rule"],
        },
    ]
    return {
        "status": "blocked",
        "target_task_id": approval_request["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_content_materialization_operator_approval_requested_not_granted",
        "checks": checks,
        "remaining_risks": [
            "operator approval reference is missing",
            "authorization prerequisites remain unresolved",
            "network retrieval remains denied",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_terms_rate_limit_review(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolution_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet()
    )
    resolution = resolution_doc["resolution"]
    review_items = []
    for item in resolution["resolution_items"]:
        review_items.append({
            "review_item_id": f"terms-rate-limit-review-{item['batch_id']}",
            "resolution_id": item["resolution_id"],
            "review_id": item["review_id"],
            "batch_id": item["batch_id"],
            "source_ids": item["source_ids"],
            "required_action": "verify_terms_or_rate_limit",
            "review_status": "pending_not_checked",
            "terms_or_rate_limit_checked": False,
            "authorization_ready": False,
            "network_access_allowed": False,
            "retrieval_may_execute": False,
            "proof_evidence_materialized": False,
        })
    return {
        "status": "blocked",
        "terms_rate_limit_review": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-terms-rate-limit-review-v0",
            "input_authorization_resolution_packet_id": resolution["id"],
            "target_task_id": resolution["target_task_id"],
            "target_pressure_test_id": resolution["target_pressure_test_id"],
            "target_remediation_id": resolution["target_remediation_id"],
            "review_scope": "content_materialization_terms_rate_limit_review",
            "retrieved_at": RETRIEVED_AT,
            "terms_or_rate_limit_checked": False,
            "review_items": review_items,
            "authorization_state": {
                "terms_rate_limit_review_recorded": True,
                "terms_or_rate_limit_checked": False,
                "authorization_prerequisites_resolved": False,
                "authorization_granted": False,
                "network_access_authorized": False,
                "retrieval_executed": False,
                "source_content_fetched": False,
                "source_quality_scored": False,
                "calibration_intervals_computed": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Terms and rate-limit review must be completed for every materialization batch "
                "before network access or retrieval may execute."
            ),
        },
        "warning": "Terms and rate-limit review is recorded but pending; retrieval remains denied.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_terms_rate_limit_checks(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_terms_rate_limit_review: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolution_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet()
    )
    review_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_terms_rate_limit_review
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_terms_rate_limit_review(
            resolution_doc
        )
    )
    resolution = resolution_doc["resolution"]
    review = review_doc["terms_rate_limit_review"]
    resolution_ids = {item["resolution_id"] for item in resolution["resolution_items"]}
    review_resolution_ids = {item["resolution_id"] for item in review["review_items"]}
    checks = [
        {
            "id": "check-authorization-resolution-packet-linked",
            "status": "complete"
            if review["input_authorization_resolution_packet_id"] == resolution["id"]
            else "open",
            "input_authorization_resolution_packet_id": review["input_authorization_resolution_packet_id"],
            "authorization_resolution_packet_id": resolution["id"],
        },
        {
            "id": "check-terms-rate-limit-items-cover-resolution-items",
            "status": "complete" if review_resolution_ids == resolution_ids else "open",
            "review_resolution_ids": sorted(review_resolution_ids),
            "resolution_ids": sorted(resolution_ids),
        },
        {
            "id": "check-terms-rate-limit-review-pending",
            "status": "blocked"
            if review["terms_or_rate_limit_checked"] is False
            and all(item["review_status"] == "pending_not_checked" for item in review["review_items"])
            else "open",
            "review_statuses": [item["review_status"] for item in review["review_items"]],
            "terms_or_rate_limit_checked": review["terms_or_rate_limit_checked"],
        },
        {
            "id": "check-terms-rate-limit-denies-network",
            "status": "blocked"
            if all(item["network_access_allowed"] is False for item in review["review_items"])
            and review["authorization_state"]["network_access_authorized"] is False
            and review["authorization_state"]["retrieval_executed"] is False
            else "open",
            "network_access_allowed_count": sum(
                1 for item in review["review_items"]
                if item["network_access_allowed"] is True
            ),
        },
        {
            "id": "check-terms-rate-limit-review-not-proof",
            "status": "contested"
            if review_doc["status"] == "blocked"
            and review["authorization_state"]["proof_evidence_materialized"] is False
            and review["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": review["authorization_state"],
            "decision_rule": review["decision_rule"],
        },
    ]
    return {
        "status": "blocked",
        "target_task_id": review["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_content_materialization_terms_rate_limit_pending",
        "checks": checks,
        "remaining_risks": [
            "terms and rate-limit review remains pending",
            "authorization prerequisites remain unresolved",
            "network retrieval remains denied",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_private_sensitive_risk_review(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolution_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet()
    )
    resolution = resolution_doc["resolution"]
    review_items = []
    for item in resolution["resolution_items"]:
        review_items.append({
            "review_item_id": f"private-sensitive-risk-review-{item['batch_id']}",
            "resolution_id": item["resolution_id"],
            "review_id": item["review_id"],
            "batch_id": item["batch_id"],
            "source_ids": item["source_ids"],
            "required_action": "check_private_or_sensitive_content_risk",
            "review_status": "pending_not_checked",
            "private_or_sensitive_content_risk_checked": False,
            "authorization_ready": False,
            "network_access_allowed": False,
            "retrieval_may_execute": False,
            "proof_evidence_materialized": False,
        })
    return {
        "status": "blocked",
        "private_sensitive_risk_review": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-private-sensitive-risk-review-v0",
            "input_authorization_resolution_packet_id": resolution["id"],
            "target_task_id": resolution["target_task_id"],
            "target_pressure_test_id": resolution["target_pressure_test_id"],
            "target_remediation_id": resolution["target_remediation_id"],
            "review_scope": "content_materialization_private_sensitive_risk_review",
            "retrieved_at": RETRIEVED_AT,
            "private_or_sensitive_content_risk_checked": False,
            "review_items": review_items,
            "authorization_state": {
                "private_sensitive_risk_review_recorded": True,
                "private_or_sensitive_content_risk_checked": False,
                "authorization_prerequisites_resolved": False,
                "authorization_granted": False,
                "network_access_authorized": False,
                "retrieval_executed": False,
                "source_content_fetched": False,
                "source_quality_scored": False,
                "calibration_intervals_computed": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Private or sensitive content risk review must be completed for every materialization "
                "batch before network access or retrieval may execute."
            ),
        },
        "warning": "Private/sensitive content risk review is recorded but pending; retrieval remains denied.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_private_sensitive_risk_checks(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_private_sensitive_risk_review: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolution_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet()
    )
    review_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_private_sensitive_risk_review
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_private_sensitive_risk_review(
            resolution_doc
        )
    )
    resolution = resolution_doc["resolution"]
    review = review_doc["private_sensitive_risk_review"]
    resolution_ids = {item["resolution_id"] for item in resolution["resolution_items"]}
    review_resolution_ids = {item["resolution_id"] for item in review["review_items"]}
    checks = [
        {
            "id": "check-authorization-resolution-packet-linked",
            "status": "complete"
            if review["input_authorization_resolution_packet_id"] == resolution["id"]
            else "open",
            "input_authorization_resolution_packet_id": review["input_authorization_resolution_packet_id"],
            "authorization_resolution_packet_id": resolution["id"],
        },
        {
            "id": "check-private-sensitive-risk-items-cover-resolution-items",
            "status": "complete" if review_resolution_ids == resolution_ids else "open",
            "review_resolution_ids": sorted(review_resolution_ids),
            "resolution_ids": sorted(resolution_ids),
        },
        {
            "id": "check-private-sensitive-risk-review-pending",
            "status": "blocked"
            if review["private_or_sensitive_content_risk_checked"] is False
            and all(item["review_status"] == "pending_not_checked" for item in review["review_items"])
            else "open",
            "review_statuses": [item["review_status"] for item in review["review_items"]],
            "private_or_sensitive_content_risk_checked": review["private_or_sensitive_content_risk_checked"],
        },
        {
            "id": "check-private-sensitive-risk-denies-network",
            "status": "blocked"
            if all(item["network_access_allowed"] is False for item in review["review_items"])
            and review["authorization_state"]["network_access_authorized"] is False
            and review["authorization_state"]["retrieval_executed"] is False
            else "open",
            "network_access_allowed_count": sum(
                1 for item in review["review_items"]
                if item["network_access_allowed"] is True
            ),
        },
        {
            "id": "check-private-sensitive-risk-review-not-proof",
            "status": "contested"
            if review_doc["status"] == "blocked"
            and review["authorization_state"]["proof_evidence_materialized"] is False
            and review["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": review["authorization_state"],
            "decision_rule": review["decision_rule"],
        },
    ]
    return {
        "status": "blocked",
        "target_task_id": review["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_content_materialization_private_sensitive_risk_pending",
        "checks": checks,
        "remaining_risks": [
            "private or sensitive content risk review remains pending",
            "authorization prerequisites remain unresolved",
            "network retrieval remains denied",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_retrieval_scope_review(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolution_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet()
    )
    resolution = resolution_doc["resolution"]
    review_items = []
    for item in resolution["resolution_items"]:
        review_items.append({
            "review_item_id": f"retrieval-scope-review-{item['batch_id']}",
            "resolution_id": item["resolution_id"],
            "review_id": item["review_id"],
            "batch_id": item["batch_id"],
            "source_ids": item["source_ids"],
            "required_action": "confirm_retrieval_scope",
            "review_status": "pending_not_confirmed",
            "retrieval_scope_confirmed": False,
            "authorization_ready": False,
            "network_access_allowed": False,
            "retrieval_may_execute": False,
            "proof_evidence_materialized": False,
        })
    return {
        "status": "blocked",
        "retrieval_scope_review": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-retrieval-scope-review-v0",
            "input_authorization_resolution_packet_id": resolution["id"],
            "target_task_id": resolution["target_task_id"],
            "target_pressure_test_id": resolution["target_pressure_test_id"],
            "target_remediation_id": resolution["target_remediation_id"],
            "review_scope": "content_materialization_retrieval_scope_review",
            "retrieved_at": RETRIEVED_AT,
            "retrieval_scope_confirmed": False,
            "review_items": review_items,
            "authorization_state": {
                "retrieval_scope_review_recorded": True,
                "retrieval_scope_confirmed": False,
                "authorization_prerequisites_resolved": False,
                "authorization_granted": False,
                "network_access_authorized": False,
                "retrieval_executed": False,
                "source_content_fetched": False,
                "source_quality_scored": False,
                "calibration_intervals_computed": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Retrieval scope must be confirmed for every materialization batch before network "
                "access or retrieval may execute."
            ),
        },
        "warning": "Retrieval scope review is recorded but pending; retrieval remains denied.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_retrieval_scope_checks(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_retrieval_scope_review: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolution_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet()
    )
    review_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_retrieval_scope_review
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_retrieval_scope_review(
            resolution_doc
        )
    )
    resolution = resolution_doc["resolution"]
    review = review_doc["retrieval_scope_review"]
    resolution_ids = {item["resolution_id"] for item in resolution["resolution_items"]}
    review_resolution_ids = {item["resolution_id"] for item in review["review_items"]}
    checks = [
        {
            "id": "check-authorization-resolution-packet-linked",
            "status": "complete"
            if review["input_authorization_resolution_packet_id"] == resolution["id"]
            else "open",
            "input_authorization_resolution_packet_id": review["input_authorization_resolution_packet_id"],
            "authorization_resolution_packet_id": resolution["id"],
        },
        {
            "id": "check-retrieval-scope-items-cover-resolution-items",
            "status": "complete" if review_resolution_ids == resolution_ids else "open",
            "review_resolution_ids": sorted(review_resolution_ids),
            "resolution_ids": sorted(resolution_ids),
        },
        {
            "id": "check-retrieval-scope-review-pending",
            "status": "blocked"
            if review["retrieval_scope_confirmed"] is False
            and all(item["review_status"] == "pending_not_confirmed" for item in review["review_items"])
            else "open",
            "review_statuses": [item["review_status"] for item in review["review_items"]],
            "retrieval_scope_confirmed": review["retrieval_scope_confirmed"],
        },
        {
            "id": "check-retrieval-scope-denies-network",
            "status": "blocked"
            if all(item["network_access_allowed"] is False for item in review["review_items"])
            and review["authorization_state"]["network_access_authorized"] is False
            and review["authorization_state"]["retrieval_executed"] is False
            else "open",
            "network_access_allowed_count": sum(
                1 for item in review["review_items"]
                if item["network_access_allowed"] is True
            ),
        },
        {
            "id": "check-retrieval-scope-review-not-proof",
            "status": "contested"
            if review_doc["status"] == "blocked"
            and review["authorization_state"]["proof_evidence_materialized"] is False
            and review["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": review["authorization_state"],
            "decision_rule": review["decision_rule"],
        },
    ]
    return {
        "status": "blocked",
        "target_task_id": review["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_content_materialization_retrieval_scope_pending",
        "checks": checks,
        "remaining_risks": [
            "retrieval scope review remains pending",
            "authorization prerequisites remain unresolved",
            "network retrieval remains denied",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_logging_hash_plan_review(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolution_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet()
    )
    resolution = resolution_doc["resolution"]
    review_items = []
    for item in resolution["resolution_items"]:
        review_items.append({
            "review_item_id": f"logging-hash-plan-review-{item['batch_id']}",
            "resolution_id": item["resolution_id"],
            "review_id": item["review_id"],
            "batch_id": item["batch_id"],
            "source_ids": item["source_ids"],
            "required_action": "verify_logging_and_hashing_targets",
            "review_status": "pending_not_verified",
            "logging_and_hashing_plan_verified": False,
            "authorization_ready": False,
            "network_access_allowed": False,
            "retrieval_may_execute": False,
            "proof_evidence_materialized": False,
        })
    return {
        "status": "blocked",
        "logging_hash_plan_review": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-logging-hash-plan-review-v0",
            "input_authorization_resolution_packet_id": resolution["id"],
            "target_task_id": resolution["target_task_id"],
            "target_pressure_test_id": resolution["target_pressure_test_id"],
            "target_remediation_id": resolution["target_remediation_id"],
            "review_scope": "content_materialization_logging_and_hashing_plan_review",
            "retrieved_at": RETRIEVED_AT,
            "logging_and_hashing_plan_verified": False,
            "review_items": review_items,
            "authorization_state": {
                "logging_hash_plan_review_recorded": True,
                "logging_and_hashing_plan_verified": False,
                "authorization_prerequisites_resolved": False,
                "authorization_granted": False,
                "network_access_authorized": False,
                "retrieval_executed": False,
                "source_content_fetched": False,
                "source_quality_scored": False,
                "calibration_intervals_computed": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Logging and hashing targets must be verified for every materialization batch before "
                "network access or retrieval may execute."
            ),
        },
        "warning": "Logging/hash plan review is recorded but pending; retrieval remains denied.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_logging_hash_plan_checks(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_logging_hash_plan_review: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolution_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet()
    )
    review_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_logging_hash_plan_review
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_logging_hash_plan_review(
            resolution_doc
        )
    )
    resolution = resolution_doc["resolution"]
    review = review_doc["logging_hash_plan_review"]
    resolution_ids = {item["resolution_id"] for item in resolution["resolution_items"]}
    review_resolution_ids = {item["resolution_id"] for item in review["review_items"]}
    checks = [
        {
            "id": "check-authorization-resolution-packet-linked",
            "status": "complete"
            if review["input_authorization_resolution_packet_id"] == resolution["id"]
            else "open",
            "input_authorization_resolution_packet_id": review["input_authorization_resolution_packet_id"],
            "authorization_resolution_packet_id": resolution["id"],
        },
        {
            "id": "check-logging-hash-plan-items-cover-resolution-items",
            "status": "complete" if review_resolution_ids == resolution_ids else "open",
            "review_resolution_ids": sorted(review_resolution_ids),
            "resolution_ids": sorted(resolution_ids),
        },
        {
            "id": "check-logging-hash-plan-review-pending",
            "status": "blocked"
            if review["logging_and_hashing_plan_verified"] is False
            and all(item["review_status"] == "pending_not_verified" for item in review["review_items"])
            else "open",
            "review_statuses": [item["review_status"] for item in review["review_items"]],
            "logging_and_hashing_plan_verified": review["logging_and_hashing_plan_verified"],
        },
        {
            "id": "check-logging-hash-plan-denies-network",
            "status": "blocked"
            if all(item["network_access_allowed"] is False for item in review["review_items"])
            and review["authorization_state"]["network_access_authorized"] is False
            and review["authorization_state"]["retrieval_executed"] is False
            else "open",
            "network_access_allowed_count": sum(
                1 for item in review["review_items"]
                if item["network_access_allowed"] is True
            ),
        },
        {
            "id": "check-logging-hash-plan-review-not-proof",
            "status": "contested"
            if review_doc["status"] == "blocked"
            and review["authorization_state"]["proof_evidence_materialized"] is False
            and review["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": review["authorization_state"],
            "decision_rule": review["decision_rule"],
        },
    ]
    return {
        "status": "blocked",
        "target_task_id": review["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_content_materialization_logging_hash_plan_pending",
        "checks": checks,
        "remaining_risks": [
            "logging and hashing plan review remains pending",
            "authorization prerequisites remain unresolved",
            "network retrieval remains denied",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_matrix(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_operator_approval_request: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_terms_rate_limit_review: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_private_sensitive_risk_review: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_retrieval_scope_review: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_logging_hash_plan_review: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolution_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet()
    )
    operator_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_operator_approval_request
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_operator_approval_request(
            resolution_doc
        )
    )
    terms_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_terms_rate_limit_review
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_terms_rate_limit_review(
            resolution_doc
        )
    )
    private_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_private_sensitive_risk_review
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_private_sensitive_risk_review(
            resolution_doc
        )
    )
    scope_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_retrieval_scope_review
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_retrieval_scope_review(
            resolution_doc
        )
    )
    logging_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_logging_hash_plan_review
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_logging_hash_plan_review(
            resolution_doc
        )
    )
    resolution = resolution_doc["resolution"]
    operator_request = operator_doc["approval_request"]
    terms_review = terms_doc["terms_rate_limit_review"]
    private_review = private_doc["private_sensitive_risk_review"]
    scope_review = scope_doc["retrieval_scope_review"]
    logging_review = logging_doc["logging_hash_plan_review"]
    closure_rows = [
        {
            "prerequisite_id": "operator_approval_reference_recorded",
            "source_artifact": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-operator-approval-request.json",
            "source_artifact_id": operator_request["id"],
            "required_action": "record_operator_approval_reference",
            "closure_status": "open",
            "satisfied": operator_request["authorization_state"]["operator_approval_reference_recorded"],
            "network_access_allowed": False,
            "retrieval_may_execute": False,
            "proof_evidence_materialized": False,
        },
        {
            "prerequisite_id": "terms_or_rate_limit_checked",
            "source_artifact": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-terms-rate-limit-review.json",
            "source_artifact_id": terms_review["id"],
            "required_action": "verify_terms_or_rate_limit",
            "closure_status": "open",
            "satisfied": terms_review["authorization_state"]["terms_or_rate_limit_checked"],
            "network_access_allowed": False,
            "retrieval_may_execute": False,
            "proof_evidence_materialized": False,
        },
        {
            "prerequisite_id": "private_or_sensitive_content_risk_checked",
            "source_artifact": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-private-sensitive-risk-review.json",
            "source_artifact_id": private_review["id"],
            "required_action": "check_private_or_sensitive_content_risk",
            "closure_status": "open",
            "satisfied": private_review["authorization_state"]["private_or_sensitive_content_risk_checked"],
            "network_access_allowed": False,
            "retrieval_may_execute": False,
            "proof_evidence_materialized": False,
        },
        {
            "prerequisite_id": "retrieval_scope_confirmed",
            "source_artifact": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-retrieval-scope-review.json",
            "source_artifact_id": scope_review["id"],
            "required_action": "confirm_retrieval_scope",
            "closure_status": "open",
            "satisfied": scope_review["authorization_state"]["retrieval_scope_confirmed"],
            "network_access_allowed": False,
            "retrieval_may_execute": False,
            "proof_evidence_materialized": False,
        },
        {
            "prerequisite_id": "logging_and_hashing_plan_verified",
            "source_artifact": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-logging-hash-plan-review.json",
            "source_artifact_id": logging_review["id"],
            "required_action": "verify_logging_and_hashing_targets",
            "closure_status": "open",
            "satisfied": logging_review["authorization_state"]["logging_and_hashing_plan_verified"],
            "network_access_allowed": False,
            "retrieval_may_execute": False,
            "proof_evidence_materialized": False,
        },
    ]
    all_prerequisites_closed = all(row["satisfied"] is True for row in closure_rows)
    return {
        "status": "blocked",
        "prerequisite_closure_matrix": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-prerequisite-closure-matrix-v0",
            "input_authorization_resolution_packet_id": resolution["id"],
            "input_operator_approval_request_id": operator_request["id"],
            "input_terms_rate_limit_review_id": terms_review["id"],
            "input_private_sensitive_risk_review_id": private_review["id"],
            "input_retrieval_scope_review_id": scope_review["id"],
            "input_logging_hash_plan_review_id": logging_review["id"],
            "target_task_id": resolution["target_task_id"],
            "target_pressure_test_id": resolution["target_pressure_test_id"],
            "target_remediation_id": resolution["target_remediation_id"],
            "matrix_scope": "content_materialization_authorization_prerequisite_closure",
            "retrieved_at": RETRIEVED_AT,
            "required_prerequisites": [
                "operator_approval_reference_recorded",
                "terms_or_rate_limit_checked",
                "private_or_sensitive_content_risk_checked",
                "retrieval_scope_confirmed",
                "logging_and_hashing_plan_verified",
            ],
            "closure_rows": closure_rows,
            "authorization_state": {
                "authorization_prerequisite_closure_matrix_recorded": True,
                "all_authorization_prerequisites_closed": all_prerequisites_closed,
                "authorization_granted": False,
                "network_access_authorized": False,
                "retrieval_executed": False,
                "source_content_fetched": False,
                "source_quality_scored": False,
                "calibration_intervals_computed": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Network retrieval remains denied until every authorization prerequisite row is closed."
            ),
        },
        "warning": "Authorization prerequisite closure is incomplete; retrieval remains denied.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_checks(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_matrix: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolution_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet()
    )
    matrix_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_matrix
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_matrix(
            resolution_doc
        )
    )
    resolution = resolution_doc["resolution"]
    matrix = matrix_doc["prerequisite_closure_matrix"]
    row_prerequisite_ids = {row["prerequisite_id"] for row in matrix["closure_rows"]}
    required_prerequisite_ids = set(matrix["required_prerequisites"])
    checks = [
        {
            "id": "check-authorization-resolution-packet-linked",
            "status": "complete"
            if matrix["input_authorization_resolution_packet_id"] == resolution["id"]
            else "open",
            "input_authorization_resolution_packet_id": matrix["input_authorization_resolution_packet_id"],
            "authorization_resolution_packet_id": resolution["id"],
        },
        {
            "id": "check-prerequisite-closure-rows-cover-required-prerequisites",
            "status": "complete" if row_prerequisite_ids == required_prerequisite_ids else "open",
            "row_prerequisite_ids": sorted(row_prerequisite_ids),
            "required_prerequisite_ids": sorted(required_prerequisite_ids),
        },
        {
            "id": "check-authorization-prerequisites-remain-open",
            "status": "blocked"
            if any(row["satisfied"] is False for row in matrix["closure_rows"])
            and matrix["authorization_state"]["all_authorization_prerequisites_closed"] is False
            else "open",
            "open_prerequisite_ids": [
                row["prerequisite_id"] for row in matrix["closure_rows"]
                if row["satisfied"] is False
            ],
        },
        {
            "id": "check-prerequisite-closure-denies-network",
            "status": "blocked"
            if all(row["network_access_allowed"] is False for row in matrix["closure_rows"])
            and matrix["authorization_state"]["network_access_authorized"] is False
            and matrix["authorization_state"]["retrieval_executed"] is False
            else "open",
            "network_access_allowed_count": sum(
                1 for row in matrix["closure_rows"]
                if row["network_access_allowed"] is True
            ),
        },
        {
            "id": "check-prerequisite-closure-not-proof",
            "status": "contested"
            if matrix_doc["status"] == "blocked"
            and matrix["authorization_state"]["proof_evidence_materialized"] is False
            and matrix["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": matrix["authorization_state"],
            "decision_rule": matrix["decision_rule"],
        },
    ]
    return {
        "status": "blocked",
        "target_task_id": matrix["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_content_materialization_authorization_prerequisites_open",
        "checks": checks,
        "remaining_risks": [
            "authorization prerequisites remain open",
            "network retrieval remains denied",
            "source evidence remains unmaterialized",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_matrix: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolution_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet()
    )
    matrix_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_matrix
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_matrix(
            resolution_doc
        )
    )
    resolution = resolution_doc["resolution"]
    matrix = matrix_doc["prerequisite_closure_matrix"]
    open_prerequisite_ids = [
        row["prerequisite_id"] for row in matrix["closure_rows"]
        if row["satisfied"] is False
    ]
    gate_rows = []
    for item in resolution["resolution_items"]:
        gate_rows.append({
            "gate_row_id": f"materialization-execution-gate-{item['batch_id']}",
            "resolution_id": item["resolution_id"],
            "review_id": item["review_id"],
            "batch_id": item["batch_id"],
            "source_ids": item["source_ids"],
            "execution_status": "blocked_by_open_authorization_prerequisites",
            "open_prerequisite_ids": open_prerequisite_ids,
            "open_prerequisite_count": len(open_prerequisite_ids),
            "network_access_allowed": False,
            "retrieval_may_execute": False,
            "source_content_may_be_fetched": False,
            "proof_evidence_materialized": False,
        })
    return {
        "status": "blocked",
        "materialization_execution_gate": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-materialization-execution-gate-v0",
            "input_authorization_resolution_packet_id": resolution["id"],
            "input_prerequisite_closure_matrix_id": matrix["id"],
            "target_task_id": resolution["target_task_id"],
            "target_pressure_test_id": resolution["target_pressure_test_id"],
            "target_remediation_id": resolution["target_remediation_id"],
            "execution_scope": "content_materialization_execution_authorization_gate",
            "retrieved_at": RETRIEVED_AT,
            "gate_decision": "deny_execution_until_authorization_prerequisites_closed",
            "gate_rows": gate_rows,
            "authorization_state": {
                "materialization_execution_gate_recorded": True,
                "all_authorization_prerequisites_closed": matrix["authorization_state"]["all_authorization_prerequisites_closed"],
                "materialization_execution_authorized": False,
                "authorization_granted": False,
                "network_access_authorized": False,
                "retrieval_executed": False,
                "source_content_fetched": False,
                "source_quality_scored": False,
                "calibration_intervals_computed": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Source materialization execution is denied while any authorization prerequisite remains open."
            ),
        },
        "warning": "Materialization execution gate denies source fetching; this is not proof evidence.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate_checks(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_matrix: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolution_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet()
    )
    matrix_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_matrix
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_matrix(
            resolution_doc
        )
    )
    gate_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate(
            resolution_doc,
            matrix_doc,
        )
    )
    resolution = resolution_doc["resolution"]
    matrix = matrix_doc["prerequisite_closure_matrix"]
    gate = gate_doc["materialization_execution_gate"]
    resolution_ids = {row["resolution_id"] for row in resolution["resolution_items"]}
    gate_resolution_ids = {row["resolution_id"] for row in gate["gate_rows"]}
    checks = [
        {
            "id": "check-prerequisite-closure-matrix-linked",
            "status": "complete"
            if gate["input_prerequisite_closure_matrix_id"] == matrix["id"]
            else "open",
            "input_prerequisite_closure_matrix_id": gate["input_prerequisite_closure_matrix_id"],
            "prerequisite_closure_matrix_id": matrix["id"],
        },
        {
            "id": "check-execution-gate-rows-cover-materialization-batches",
            "status": "complete" if gate_resolution_ids == resolution_ids else "open",
            "gate_resolution_ids": sorted(gate_resolution_ids),
            "resolution_ids": sorted(resolution_ids),
        },
        {
            "id": "check-materialization-execution-denied",
            "status": "blocked"
            if gate["gate_decision"] == "deny_execution_until_authorization_prerequisites_closed"
            and all(
                row["execution_status"] == "blocked_by_open_authorization_prerequisites"
                for row in gate["gate_rows"]
            )
            else "open",
            "gate_decision": gate["gate_decision"],
            "execution_statuses": [row["execution_status"] for row in gate["gate_rows"]],
        },
        {
            "id": "check-execution-gate-denies-network",
            "status": "blocked"
            if all(row["network_access_allowed"] is False for row in gate["gate_rows"])
            and gate["authorization_state"]["network_access_authorized"] is False
            and gate["authorization_state"]["retrieval_executed"] is False
            else "open",
            "network_access_allowed_count": sum(
                1 for row in gate["gate_rows"]
                if row["network_access_allowed"] is True
            ),
        },
        {
            "id": "check-materialization-execution-gate-not-proof",
            "status": "contested"
            if gate_doc["status"] == "blocked"
            and gate["authorization_state"]["proof_evidence_materialized"] is False
            and gate["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": gate["authorization_state"],
            "decision_rule": gate["decision_rule"],
        },
    ]
    return {
        "status": "blocked",
        "target_task_id": gate["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_content_materialization_execution_denied",
        "checks": checks,
        "remaining_risks": [
            "materialization execution remains denied",
            "authorization prerequisites remain open",
            "source evidence remains unmaterialized",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    gate_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate()
    )
    gate = gate_doc["materialization_execution_gate"]
    commands = []
    for row in gate["gate_rows"]:
        source_args = " ".join(f"--source-id {source_id}" for source_id in row["source_ids"])
        commands.append({
            "command_id": f"future-materialize-{row['batch_id']}",
            "gate_row_id": row["gate_row_id"],
            "batch_id": row["batch_id"],
            "source_ids": row["source_ids"],
            "command_template": (
                "kr materialize-source-content "
                f"--batch-id {row['batch_id']} {source_args} "
                "--write-content-hash --write-retrieval-log"
            ),
            "command_status": "not_executable_authorization_gate_blocked",
            "blocking_gate_decision": gate["gate_decision"],
            "network_access_allowed": False,
            "retrieval_may_execute": False,
            "command_executed": False,
            "source_content_fetched": False,
            "proof_evidence_materialized": False,
        })
    return {
        "status": "blocked",
        "future_command_manifest": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-future-command-manifest-v0",
            "input_materialization_execution_gate_id": gate["id"],
            "target_task_id": gate["target_task_id"],
            "target_pressure_test_id": gate["target_pressure_test_id"],
            "target_remediation_id": gate["target_remediation_id"],
            "manifest_scope": "future_content_materialization_fetch_commands",
            "retrieved_at": RETRIEVED_AT,
            "commands_executable": False,
            "commands": commands,
            "authorization_state": {
                "future_command_manifest_recorded": True,
                "materialization_execution_authorized": False,
                "authorization_granted": False,
                "network_access_authorized": False,
                "retrieval_executed": False,
                "source_content_fetched": False,
                "source_quality_scored": False,
                "calibration_intervals_computed": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Future materialization commands are templates only and must not execute until "
                "the materialization execution gate authorizes retrieval."
            ),
        },
        "warning": "Future source materialization commands are recorded but not executable.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest_checks(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    gate_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate()
    )
    manifest_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest(
            gate_doc
        )
    )
    gate = gate_doc["materialization_execution_gate"]
    manifest = manifest_doc["future_command_manifest"]
    gate_row_ids = {row["gate_row_id"] for row in gate["gate_rows"]}
    command_gate_row_ids = {row["gate_row_id"] for row in manifest["commands"]}
    checks = [
        {
            "id": "check-materialization-execution-gate-linked",
            "status": "complete"
            if manifest["input_materialization_execution_gate_id"] == gate["id"]
            else "open",
            "input_materialization_execution_gate_id": manifest["input_materialization_execution_gate_id"],
            "materialization_execution_gate_id": gate["id"],
        },
        {
            "id": "check-future-commands-cover-gate-rows",
            "status": "complete" if command_gate_row_ids == gate_row_ids else "open",
            "command_gate_row_ids": sorted(command_gate_row_ids),
            "gate_row_ids": sorted(gate_row_ids),
        },
        {
            "id": "check-future-commands-not-executable",
            "status": "blocked"
            if manifest["commands_executable"] is False
            and all(
                row["command_status"] == "not_executable_authorization_gate_blocked"
                for row in manifest["commands"]
            )
            else "open",
            "commands_executable": manifest["commands_executable"],
            "command_statuses": [row["command_status"] for row in manifest["commands"]],
        },
        {
            "id": "check-future-commands-deny-network",
            "status": "blocked"
            if all(row["network_access_allowed"] is False for row in manifest["commands"])
            and manifest["authorization_state"]["network_access_authorized"] is False
            and manifest["authorization_state"]["retrieval_executed"] is False
            else "open",
            "network_access_allowed_count": sum(
                1 for row in manifest["commands"]
                if row["network_access_allowed"] is True
            ),
        },
        {
            "id": "check-future-command-manifest-not-proof",
            "status": "contested"
            if manifest_doc["status"] == "blocked"
            and manifest["authorization_state"]["proof_evidence_materialized"] is False
            and manifest["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": manifest["authorization_state"],
            "decision_rule": manifest["decision_rule"],
        },
    ]
    return {
        "status": "blocked",
        "target_task_id": manifest["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_content_materialization_future_commands_not_executable",
        "checks": checks,
        "remaining_risks": [
            "future commands are templates only",
            "authorization gate still denies execution",
            "source evidence remains unmaterialized",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    manifest_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest()
    )
    manifest = manifest_doc["future_command_manifest"]
    receipt_rows = []
    for command in manifest["commands"]:
        receipt_rows.append({
            "receipt_row_id": f"nonexecution-receipt-{command['command_id']}",
            "command_id": command["command_id"],
            "gate_row_id": command["gate_row_id"],
            "batch_id": command["batch_id"],
            "source_ids": command["source_ids"],
            "receipt_status": "not_executed",
            "command_executed": False,
            "source_content_fetched": False,
            "retrieval_log_written": False,
            "content_hash_written": False,
            "proof_evidence_materialized": False,
        })
    return {
        "status": "blocked",
        "command_nonexecution_receipt": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-nonexecution-receipt-v0",
            "input_future_command_manifest_id": manifest["id"],
            "target_task_id": manifest["target_task_id"],
            "target_pressure_test_id": manifest["target_pressure_test_id"],
            "target_remediation_id": manifest["target_remediation_id"],
            "receipt_scope": "content_materialization_command_nonexecution_receipt",
            "retrieved_at": RETRIEVED_AT,
            "command_count": len(manifest["commands"]),
            "executed_command_count": 0,
            "source_content_file_count": 0,
            "retrieval_log_count": 0,
            "content_hash_count": 0,
            "receipt_rows": receipt_rows,
            "authorization_state": {
                "command_nonexecution_receipt_recorded": True,
                "materialization_execution_authorized": False,
                "network_access_authorized": False,
                "retrieval_executed": False,
                "source_content_fetched": False,
                "source_quality_scored": False,
                "calibration_intervals_computed": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Future command templates remain non-executed until authorization gate allows retrieval."
            ),
        },
        "warning": "No source content or proof evidence has been materialized.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt_checks(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt: dict[str, Any] | None = None,
) -> dict[str, Any]:
    manifest_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest()
    )
    receipt_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt(
            manifest_doc
        )
    )
    manifest = manifest_doc["future_command_manifest"]
    receipt = receipt_doc["command_nonexecution_receipt"]
    command_ids = {row["command_id"] for row in manifest["commands"]}
    receipt_command_ids = {row["command_id"] for row in receipt["receipt_rows"]}
    checks = [
        {
            "id": "check-future-command-manifest-linked",
            "status": "complete"
            if receipt["input_future_command_manifest_id"] == manifest["id"]
            else "open",
            "input_future_command_manifest_id": receipt["input_future_command_manifest_id"],
            "future_command_manifest_id": manifest["id"],
        },
        {
            "id": "check-nonexecution-rows-cover-future-commands",
            "status": "complete" if receipt_command_ids == command_ids else "open",
            "receipt_command_ids": sorted(receipt_command_ids),
            "future_command_ids": sorted(command_ids),
        },
        {
            "id": "check-commands-remain-unexecuted",
            "status": "blocked"
            if receipt["executed_command_count"] == 0
            and all(row["command_executed"] is False for row in receipt["receipt_rows"])
            else "open",
            "executed_command_count": receipt["executed_command_count"],
        },
        {
            "id": "check-no-content-outputs-written",
            "status": "blocked"
            if receipt["source_content_file_count"] == 0
            and receipt["retrieval_log_count"] == 0
            and receipt["content_hash_count"] == 0
            and all(row["source_content_fetched"] is False for row in receipt["receipt_rows"])
            and all(row["retrieval_log_written"] is False for row in receipt["receipt_rows"])
            and all(row["content_hash_written"] is False for row in receipt["receipt_rows"])
            else "open",
            "source_content_file_count": receipt["source_content_file_count"],
            "retrieval_log_count": receipt["retrieval_log_count"],
            "content_hash_count": receipt["content_hash_count"],
        },
        {
            "id": "check-command-nonexecution-receipt-not-proof",
            "status": "contested"
            if receipt_doc["status"] == "blocked"
            and receipt["authorization_state"]["proof_evidence_materialized"] is False
            and receipt["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": receipt["authorization_state"],
            "decision_rule": receipt["decision_rule"],
        },
    ]
    return {
        "status": "blocked",
        "target_task_id": receipt["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_content_materialization_commands_not_executed",
        "checks": checks,
        "remaining_risks": [
            "future commands remain non-executed",
            "source content files are absent",
            "retrieval logs and content hashes are absent",
            "source evidence remains unmaterialized",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_ledger(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt: dict[str, Any] | None = None,
) -> dict[str, Any]:
    receipt_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt()
    )
    receipt = receipt_doc["command_nonexecution_receipt"]
    gap_rows = []
    for row in receipt["receipt_rows"]:
        gap_rows.append({
            "gap_row_id": f"output-gap-{row['command_id']}",
            "command_id": row["command_id"],
            "gate_row_id": row["gate_row_id"],
            "batch_id": row["batch_id"],
            "source_ids": row["source_ids"],
            "command_executed": row["command_executed"],
            "source_content_file_status": "missing",
            "retrieval_log_status": "missing",
            "content_hash_status": "missing",
            "missing_output_types": ["source_content_file", "retrieval_log", "content_hash"],
            "gap_status": "open_blocked_by_nonexecution",
        })
    return {
        "status": "blocked",
        "command_output_gap_ledger": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-ledger-v0",
            "input_command_nonexecution_receipt_id": receipt["id"],
            "target_task_id": receipt["target_task_id"],
            "target_pressure_test_id": receipt["target_pressure_test_id"],
            "target_remediation_id": receipt["target_remediation_id"],
            "gap_scope": "content_materialization_command_output_gaps",
            "retrieved_at": RETRIEVED_AT,
            "command_count": receipt["command_count"],
            "missing_source_content_file_count": receipt["command_count"],
            "missing_retrieval_log_count": receipt["command_count"],
            "missing_content_hash_count": receipt["command_count"],
            "open_gap_count": receipt["command_count"] * 3,
            "gap_rows": gap_rows,
            "authorization_state": {
                "command_output_gap_ledger_recorded": True,
                "materialization_execution_authorized": False,
                "network_access_authorized": False,
                "retrieval_executed": False,
                "source_content_fetched": False,
                "retrieval_logs_written": False,
                "content_hashes_written": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Output gaps remain open until the future commands execute under authorization "
                "and produce source content files, retrieval logs, and content hashes."
            ),
        },
        "warning": "Missing output rows document absence of evidence, not proof evidence.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_checks(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    receipt_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt()
    )
    ledger_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_ledger
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_ledger(
            receipt_doc
        )
    )
    receipt = receipt_doc["command_nonexecution_receipt"]
    ledger = ledger_doc["command_output_gap_ledger"]
    receipt_command_ids = {row["command_id"] for row in receipt["receipt_rows"]}
    gap_command_ids = {row["command_id"] for row in ledger["gap_rows"]}
    checks = [
        {
            "id": "check-command-nonexecution-receipt-linked",
            "status": "complete"
            if ledger["input_command_nonexecution_receipt_id"] == receipt["id"]
            else "open",
            "input_command_nonexecution_receipt_id": ledger["input_command_nonexecution_receipt_id"],
            "command_nonexecution_receipt_id": receipt["id"],
        },
        {
            "id": "check-gap-rows-cover-receipt-commands",
            "status": "complete" if gap_command_ids == receipt_command_ids else "open",
            "gap_command_ids": sorted(gap_command_ids),
            "receipt_command_ids": sorted(receipt_command_ids),
        },
        {
            "id": "check-all-content-outputs-missing",
            "status": "blocked"
            if ledger["missing_source_content_file_count"] == receipt["command_count"]
            and ledger["missing_retrieval_log_count"] == receipt["command_count"]
            and ledger["missing_content_hash_count"] == receipt["command_count"]
            and ledger["open_gap_count"] == receipt["command_count"] * 3
            and all(row["source_content_file_status"] == "missing" for row in ledger["gap_rows"])
            and all(row["retrieval_log_status"] == "missing" for row in ledger["gap_rows"])
            and all(row["content_hash_status"] == "missing" for row in ledger["gap_rows"])
            else "open",
            "open_gap_count": ledger["open_gap_count"],
        },
        {
            "id": "check-output-gap-ledger-keeps-network-denied",
            "status": "blocked"
            if ledger["authorization_state"]["network_access_authorized"] is False
            and ledger["authorization_state"]["retrieval_executed"] is False
            and ledger["authorization_state"]["source_content_fetched"] is False
            else "open",
            "authorization_state": ledger["authorization_state"],
        },
        {
            "id": "check-command-output-gap-ledger-not-proof",
            "status": "contested"
            if ledger_doc["status"] == "blocked"
            and ledger["authorization_state"]["proof_evidence_materialized"] is False
            and ledger["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": ledger["authorization_state"],
            "decision_rule": ledger["decision_rule"],
        },
    ]
    return {
        "status": "blocked",
        "target_task_id": ledger["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_content_materialization_output_gaps_open",
        "checks": checks,
        "remaining_risks": [
            "source content files are missing for every future command",
            "retrieval logs are missing for every future command",
            "content hashes are missing for every future command",
            "missing outputs cannot support a proof claim",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_queue(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ledger_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_ledger
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_ledger()
    )
    ledger = ledger_doc["command_output_gap_ledger"]
    output_types = ["source_content_file", "retrieval_log", "content_hash"]
    required_actions = {
        "source_content_file": "write authorized source content file",
        "retrieval_log": "write retrieval log with source locator and timestamp",
        "content_hash": "write content hash for fetched source content",
    }
    task_rows = []
    for gap_row in ledger["gap_rows"]:
        for output_type in output_types:
            task_rows.append({
                "task_id": f"close-{gap_row['gap_row_id']}-{output_type}",
                "gap_row_id": gap_row["gap_row_id"],
                "command_id": gap_row["command_id"],
                "gate_row_id": gap_row["gate_row_id"],
                "batch_id": gap_row["batch_id"],
                "source_ids": gap_row["source_ids"],
                "output_type": output_type,
                "required_action": required_actions[output_type],
                "task_status": "queued_blocked_by_authorization",
                "closure_authorized": False,
                "command_executed": gap_row["command_executed"],
                "output_materialized": False,
                "proof_evidence_materialized": False,
            })
    return {
        "status": "blocked",
        "command_output_gap_closure_task_queue": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-task-queue-v0",
            "input_command_output_gap_ledger_id": ledger["id"],
            "target_task_id": ledger["target_task_id"],
            "target_pressure_test_id": ledger["target_pressure_test_id"],
            "target_remediation_id": ledger["target_remediation_id"],
            "queue_scope": "content_materialization_command_output_gap_closure_tasks",
            "retrieved_at": RETRIEVED_AT,
            "command_count": ledger["command_count"],
            "gap_row_count": len(ledger["gap_rows"]),
            "task_count": len(task_rows),
            "open_task_count": len(task_rows),
            "output_types": output_types,
            "task_rows": task_rows,
            "authorization_state": {
                "gap_closure_task_queue_recorded": True,
                "materialization_execution_authorized": False,
                "network_access_authorized": False,
                "retrieval_executed": False,
                "source_content_fetched": False,
                "retrieval_logs_written": False,
                "content_hashes_written": False,
                "gap_closures_materialized": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Gap closure tasks queue the missing outputs but remain blocked until "
                "materialization execution is authorized."
            ),
        },
        "warning": "Queued gap-closure tasks are not execution evidence and do not close any gap.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_checks(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_ledger: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_queue: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ledger_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_ledger
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_ledger()
    )
    queue_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_queue
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_queue(
            ledger_doc
        )
    )
    ledger = ledger_doc["command_output_gap_ledger"]
    queue = queue_doc["command_output_gap_closure_task_queue"]
    expected_pairs = {
        (row["gap_row_id"], output_type)
        for row in ledger["gap_rows"]
        for output_type in row["missing_output_types"]
    }
    task_pairs = {
        (row["gap_row_id"], row["output_type"])
        for row in queue["task_rows"]
    }
    checks = [
        {
            "id": "check-output-gap-ledger-linked",
            "status": "complete"
            if queue["input_command_output_gap_ledger_id"] == ledger["id"]
            else "open",
            "input_command_output_gap_ledger_id": queue["input_command_output_gap_ledger_id"],
            "command_output_gap_ledger_id": ledger["id"],
        },
        {
            "id": "check-closure-tasks-cover-output-gaps",
            "status": "complete" if task_pairs == expected_pairs else "open",
            "task_pair_count": len(task_pairs),
            "expected_pair_count": len(expected_pairs),
        },
        {
            "id": "check-closure-tasks-remain-blocked",
            "status": "blocked"
            if queue["open_task_count"] == queue["task_count"]
            and all(row["task_status"] == "queued_blocked_by_authorization" for row in queue["task_rows"])
            and all(row["closure_authorized"] is False for row in queue["task_rows"])
            else "open",
            "open_task_count": queue["open_task_count"],
            "task_count": queue["task_count"],
        },
        {
            "id": "check-no-gap-closures-materialized",
            "status": "blocked"
            if queue["authorization_state"]["gap_closures_materialized"] is False
            and all(row["output_materialized"] is False for row in queue["task_rows"])
            and queue["authorization_state"]["retrieval_executed"] is False
            else "open",
            "authorization_state": queue["authorization_state"],
        },
        {
            "id": "check-output-gap-closure-task-queue-not-proof",
            "status": "contested"
            if queue_doc["status"] == "blocked"
            and queue["authorization_state"]["proof_evidence_materialized"] is False
            and queue["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": queue["authorization_state"],
            "decision_rule": queue["decision_rule"],
        },
    ]
    return {
        "status": "blocked",
        "target_task_id": queue["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_content_materialization_gap_closure_tasks_blocked",
        "checks": checks,
        "remaining_risks": [
            "gap closure tasks are queued but not authorized",
            "no source content, retrieval log, or content hash has been materialized",
            "queued tasks cannot support a proof claim",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_plan(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_queue: dict[str, Any] | None = None,
) -> dict[str, Any]:
    queue_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_queue
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_queue()
    )
    queue = queue_doc["command_output_gap_closure_task_queue"]
    tasks_by_command: dict[str, list[dict[str, Any]]] = {}
    for task in queue["task_rows"]:
        tasks_by_command.setdefault(task["command_id"], []).append(task)
    batches = []
    for batch_order, command_id in enumerate(sorted(tasks_by_command), start=1):
        tasks = tasks_by_command[command_id]
        outputs = ["source_content_file", "retrieval_log", "content_hash"]
        batches.append({
            "batch_id": f"gap-closure-batch-{command_id}",
            "batch_order": batch_order,
            "command_id": command_id,
            "gate_row_id": tasks[0]["gate_row_id"],
            "source_ids": tasks[0]["source_ids"],
            "task_ids": [task["task_id"] for task in tasks],
            "task_count": len(tasks),
            "outputs_to_materialize": outputs,
            "batch_status": "queued_blocked_by_authorization",
            "execution_allowed": False,
            "outputs_materialized": False,
            "proof_evidence_materialized": False,
        })
    return {
        "status": "blocked",
        "command_output_gap_closure_batch_plan": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-plan-v0",
            "input_command_output_gap_closure_task_queue_id": queue["id"],
            "target_task_id": queue["target_task_id"],
            "target_pressure_test_id": queue["target_pressure_test_id"],
            "target_remediation_id": queue["target_remediation_id"],
            "plan_scope": "content_materialization_command_output_gap_closure_batches",
            "retrieved_at": RETRIEVED_AT,
            "command_count": queue["command_count"],
            "batch_count": len(batches),
            "task_count": queue["task_count"],
            "open_batch_count": len(batches),
            "batches": batches,
            "authorization_state": {
                "gap_closure_batch_plan_recorded": True,
                "materialization_execution_authorized": False,
                "network_access_authorized": False,
                "retrieval_executed": False,
                "source_content_fetched": False,
                "retrieval_logs_written": False,
                "content_hashes_written": False,
                "gap_closure_batches_executed": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Gap closure batches are execution planning only and stay blocked until "
                "materialization authorization allows source retrieval."
            ),
        },
        "warning": "Batch planning does not execute retrieval or materialize proof evidence.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_checks(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_queue: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    queue_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_queue
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_queue()
    )
    plan_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_plan
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_plan(
            queue_doc
        )
    )
    queue = queue_doc["command_output_gap_closure_task_queue"]
    plan = plan_doc["command_output_gap_closure_batch_plan"]
    queue_task_ids = {row["task_id"] for row in queue["task_rows"]}
    batch_task_ids = {
        task_id
        for batch in plan["batches"]
        for task_id in batch["task_ids"]
    }
    checks = [
        {
            "id": "check-closure-task-queue-linked",
            "status": "complete"
            if plan["input_command_output_gap_closure_task_queue_id"] == queue["id"]
            else "open",
            "input_command_output_gap_closure_task_queue_id": plan["input_command_output_gap_closure_task_queue_id"],
            "command_output_gap_closure_task_queue_id": queue["id"],
        },
        {
            "id": "check-batches-cover-closure-tasks",
            "status": "complete" if batch_task_ids == queue_task_ids else "open",
            "batch_task_count": len(batch_task_ids),
            "queue_task_count": len(queue_task_ids),
        },
        {
            "id": "check-batches-remain-blocked",
            "status": "blocked"
            if plan["open_batch_count"] == plan["batch_count"]
            and all(row["batch_status"] == "queued_blocked_by_authorization" for row in plan["batches"])
            and all(row["execution_allowed"] is False for row in plan["batches"])
            else "open",
            "open_batch_count": plan["open_batch_count"],
            "batch_count": plan["batch_count"],
        },
        {
            "id": "check-no-batch-output-materialized",
            "status": "blocked"
            if plan["authorization_state"]["gap_closure_batches_executed"] is False
            and all(row["outputs_materialized"] is False for row in plan["batches"])
            and plan["authorization_state"]["retrieval_executed"] is False
            else "open",
            "authorization_state": plan["authorization_state"],
        },
        {
            "id": "check-gap-closure-batch-plan-not-proof",
            "status": "contested"
            if plan_doc["status"] == "blocked"
            and plan["authorization_state"]["proof_evidence_materialized"] is False
            and plan["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": plan["authorization_state"],
            "decision_rule": plan["decision_rule"],
        },
    ]
    return {
        "status": "blocked",
        "target_task_id": plan["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_content_materialization_gap_closure_batches_blocked",
        "checks": checks,
        "remaining_risks": [
            "gap closure batches are planned but not authorized",
            "batch execution has not started",
            "no missing output has been materialized",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_ledger(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    plan_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_plan
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_plan()
    )
    plan = plan_doc["command_output_gap_closure_batch_plan"]
    execution_rows = []
    for batch in plan["batches"]:
        execution_rows.append({
            "execution_row_id": f"execution-ledger-{batch['batch_id']}",
            "batch_id": batch["batch_id"],
            "batch_order": batch["batch_order"],
            "command_id": batch["command_id"],
            "gate_row_id": batch["gate_row_id"],
            "source_ids": batch["source_ids"],
            "task_ids": batch["task_ids"],
            "task_count": batch["task_count"],
            "execution_status": "not_started_authorization_blocked",
            "execution_started": False,
            "execution_completed": False,
            "outputs_materialized": False,
            "retrieval_log_written": False,
            "content_hash_written": False,
            "proof_evidence_materialized": False,
        })
    return {
        "status": "blocked",
        "command_output_gap_closure_batch_execution_ledger": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-ledger-v0",
            "input_command_output_gap_closure_batch_plan_id": plan["id"],
            "target_task_id": plan["target_task_id"],
            "target_pressure_test_id": plan["target_pressure_test_id"],
            "target_remediation_id": plan["target_remediation_id"],
            "ledger_scope": "content_materialization_command_output_gap_closure_batch_execution",
            "retrieved_at": RETRIEVED_AT,
            "batch_count": plan["batch_count"],
            "task_count": plan["task_count"],
            "executed_batch_count": 0,
            "materialized_output_count": 0,
            "execution_rows": execution_rows,
            "authorization_state": {
                "batch_execution_ledger_recorded": True,
                "materialization_execution_authorized": False,
                "network_access_authorized": False,
                "retrieval_executed": False,
                "source_content_fetched": False,
                "retrieval_logs_written": False,
                "content_hashes_written": False,
                "gap_closure_batches_executed": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Execution ledger records that planned gap-closure batches have not started "
                "because materialization authorization is still denied."
            ),
        },
        "warning": "No batch execution, retrieval log, content hash, or proof evidence is recorded.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_checks(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_plan: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    plan_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_plan
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_plan()
    )
    ledger_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_ledger
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_ledger(
            plan_doc
        )
    )
    plan = plan_doc["command_output_gap_closure_batch_plan"]
    ledger = ledger_doc["command_output_gap_closure_batch_execution_ledger"]
    plan_batch_ids = {row["batch_id"] for row in plan["batches"]}
    ledger_batch_ids = {row["batch_id"] for row in ledger["execution_rows"]}
    checks = [
        {
            "id": "check-gap-closure-batch-plan-linked",
            "status": "complete"
            if ledger["input_command_output_gap_closure_batch_plan_id"] == plan["id"]
            else "open",
            "input_command_output_gap_closure_batch_plan_id": ledger["input_command_output_gap_closure_batch_plan_id"],
            "command_output_gap_closure_batch_plan_id": plan["id"],
        },
        {
            "id": "check-execution-rows-cover-batches",
            "status": "complete" if ledger_batch_ids == plan_batch_ids else "open",
            "ledger_batch_ids": sorted(ledger_batch_ids),
            "plan_batch_ids": sorted(plan_batch_ids),
        },
        {
            "id": "check-batch-execution-not-started",
            "status": "blocked"
            if ledger["executed_batch_count"] == 0
            and all(row["execution_started"] is False for row in ledger["execution_rows"])
            and all(row["execution_status"] == "not_started_authorization_blocked" for row in ledger["execution_rows"])
            else "open",
            "executed_batch_count": ledger["executed_batch_count"],
        },
        {
            "id": "check-no-execution-outputs-materialized",
            "status": "blocked"
            if ledger["materialized_output_count"] == 0
            and all(row["outputs_materialized"] is False for row in ledger["execution_rows"])
            and all(row["retrieval_log_written"] is False for row in ledger["execution_rows"])
            and all(row["content_hash_written"] is False for row in ledger["execution_rows"])
            else "open",
            "materialized_output_count": ledger["materialized_output_count"],
        },
        {
            "id": "check-gap-closure-batch-execution-ledger-not-proof",
            "status": "contested"
            if ledger_doc["status"] == "blocked"
            and ledger["authorization_state"]["proof_evidence_materialized"] is False
            and ledger["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": ledger["authorization_state"],
            "decision_rule": ledger["decision_rule"],
        },
    ]
    return {
        "status": "blocked",
        "target_task_id": ledger["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_content_materialization_gap_closure_batch_execution_not_started",
        "checks": checks,
        "remaining_risks": [
            "gap closure batch execution has not started",
            "no retrieval logs or content hashes were written",
            "execution ledger is not proof evidence",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_matrix(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ledger_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_ledger
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_ledger()
    )
    ledger = ledger_doc["command_output_gap_closure_batch_execution_ledger"]
    unblocker_types = [
        "operator_approval_reference",
        "terms_rate_limit_clearance",
        "private_sensitive_risk_clearance",
        "retrieval_scope_clearance",
        "logging_hash_plan_clearance",
    ]
    unblocker_actions = {
        "operator_approval_reference": "record explicit operator approval for materialization execution",
        "terms_rate_limit_clearance": "close terms and rate-limit review for the batch",
        "private_sensitive_risk_clearance": "close private and sensitive content risk review",
        "retrieval_scope_clearance": "close retrieval scope review for allowed sources",
        "logging_hash_plan_clearance": "close logging and content-hash plan review",
    }
    matrix_rows = []
    for row in ledger["execution_rows"]:
        matrix_rows.append({
            "matrix_row_id": f"unblockers-{row['batch_id']}",
            "batch_id": row["batch_id"],
            "batch_order": row["batch_order"],
            "command_id": row["command_id"],
            "gate_row_id": row["gate_row_id"],
            "source_ids": row["source_ids"],
            "execution_started": row["execution_started"],
            "unblockers": [
                {
                    "unblocker_id": f"{row['batch_id']}-{unblocker_type}",
                    "unblocker_type": unblocker_type,
                    "required_action": unblocker_actions[unblocker_type],
                    "unblocker_status": "open",
                    "authorization_required": True,
                    "resolved": False,
                }
                for unblocker_type in unblocker_types
            ],
        })
    return {
        "status": "blocked",
        "command_output_gap_closure_batch_execution_unblocker_matrix": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-matrix-v0",
            "input_command_output_gap_closure_batch_execution_ledger_id": ledger["id"],
            "target_task_id": ledger["target_task_id"],
            "target_pressure_test_id": ledger["target_pressure_test_id"],
            "target_remediation_id": ledger["target_remediation_id"],
            "matrix_scope": "content_materialization_command_output_gap_closure_batch_execution_unblockers",
            "retrieved_at": RETRIEVED_AT,
            "batch_count": ledger["batch_count"],
            "unblocker_types": unblocker_types,
            "unblocker_type_count": len(unblocker_types),
            "unblocker_cell_count": ledger["batch_count"] * len(unblocker_types),
            "open_unblocker_count": ledger["batch_count"] * len(unblocker_types),
            "matrix_rows": matrix_rows,
            "authorization_state": {
                "unblocker_matrix_recorded": True,
                "materialization_execution_authorized": False,
                "network_access_authorized": False,
                "retrieval_executed": False,
                "source_content_fetched": False,
                "retrieval_logs_written": False,
                "content_hashes_written": False,
                "gap_closure_batches_executed": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "All unblocker cells must be resolved before batch execution may start; "
                "this matrix records open prerequisites only."
            ),
        },
        "warning": "Open unblockers are prerequisites, not proof evidence.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_checks(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_ledger: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_matrix: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ledger_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_ledger
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_ledger()
    )
    matrix_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_matrix
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_matrix(
            ledger_doc
        )
    )
    ledger = ledger_doc["command_output_gap_closure_batch_execution_ledger"]
    matrix = matrix_doc["command_output_gap_closure_batch_execution_unblocker_matrix"]
    ledger_batch_ids = {row["batch_id"] for row in ledger["execution_rows"]}
    matrix_batch_ids = {row["batch_id"] for row in matrix["matrix_rows"]}
    expected_cell_count = ledger["batch_count"] * matrix["unblocker_type_count"]
    actual_cell_count = sum(len(row["unblockers"]) for row in matrix["matrix_rows"])
    open_cell_count = sum(
        1
        for row in matrix["matrix_rows"]
        for cell in row["unblockers"]
        if cell["unblocker_status"] == "open" and cell["resolved"] is False
    )
    checks = [
        {
            "id": "check-batch-execution-ledger-linked",
            "status": "complete"
            if matrix["input_command_output_gap_closure_batch_execution_ledger_id"] == ledger["id"]
            else "open",
            "input_command_output_gap_closure_batch_execution_ledger_id": (
                matrix["input_command_output_gap_closure_batch_execution_ledger_id"]
            ),
            "command_output_gap_closure_batch_execution_ledger_id": ledger["id"],
        },
        {
            "id": "check-unblocker-rows-cover-execution-batches",
            "status": "complete" if matrix_batch_ids == ledger_batch_ids else "open",
            "matrix_batch_ids": sorted(matrix_batch_ids),
            "ledger_batch_ids": sorted(ledger_batch_ids),
        },
        {
            "id": "check-unblocker-cells-cover-required-prerequisites",
            "status": "complete"
            if matrix["unblocker_cell_count"] == expected_cell_count
            and actual_cell_count == expected_cell_count
            else "open",
            "expected_cell_count": expected_cell_count,
            "actual_cell_count": actual_cell_count,
        },
        {
            "id": "check-all-unblockers-remain-open",
            "status": "blocked"
            if matrix["open_unblocker_count"] == matrix["unblocker_cell_count"]
            and open_cell_count == matrix["unblocker_cell_count"]
            else "open",
            "open_cell_count": open_cell_count,
            "unblocker_cell_count": matrix["unblocker_cell_count"],
        },
        {
            "id": "check-batch-execution-unblocker-matrix-not-proof",
            "status": "contested"
            if matrix_doc["status"] == "blocked"
            and matrix["authorization_state"]["proof_evidence_materialized"] is False
            and matrix["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": matrix["authorization_state"],
            "decision_rule": matrix["decision_rule"],
        },
    ]
    return {
        "status": "blocked",
        "target_task_id": matrix["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_content_materialization_gap_closure_execution_unblockers_open",
        "checks": checks,
        "remaining_risks": [
            "batch execution unblockers remain open",
            "materialization authorization is still denied",
            "unblocker matrix is not proof evidence",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_queue(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_matrix: dict[str, Any] | None = None,
) -> dict[str, Any]:
    matrix_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_matrix
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_matrix()
    )
    matrix = matrix_doc["command_output_gap_closure_batch_execution_unblocker_matrix"]
    priority_order = matrix["unblocker_types"]
    resolution_tasks = []
    order = 1
    for unblocker_type in priority_order:
        for row in sorted(matrix["matrix_rows"], key=lambda item: item["batch_order"]):
            for cell in row["unblockers"]:
                if cell["unblocker_type"] != unblocker_type:
                    continue
                resolution_tasks.append({
                    "resolution_task_id": f"resolve-{cell['unblocker_id']}",
                    "resolution_order": order,
                    "batch_id": row["batch_id"],
                    "batch_order": row["batch_order"],
                    "command_id": row["command_id"],
                    "gate_row_id": row["gate_row_id"],
                    "source_ids": row["source_ids"],
                    "unblocker_id": cell["unblocker_id"],
                    "unblocker_type": cell["unblocker_type"],
                    "required_action": cell["required_action"],
                    "resolution_status": "queued_open",
                    "resolution_authorized": False,
                    "unblocker_resolved": False,
                    "proof_evidence_materialized": False,
                })
                order += 1
    return {
        "status": "blocked",
        "command_output_gap_closure_batch_execution_unblocker_resolution_queue": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-queue-v0",
            "input_command_output_gap_closure_batch_execution_unblocker_matrix_id": matrix["id"],
            "target_task_id": matrix["target_task_id"],
            "target_pressure_test_id": matrix["target_pressure_test_id"],
            "target_remediation_id": matrix["target_remediation_id"],
            "queue_scope": "content_materialization_batch_execution_unblocker_resolution",
            "retrieved_at": RETRIEVED_AT,
            "batch_count": matrix["batch_count"],
            "unblocker_cell_count": matrix["unblocker_cell_count"],
            "resolution_task_count": len(resolution_tasks),
            "open_resolution_task_count": len(resolution_tasks),
            "priority_order": priority_order,
            "resolution_tasks": resolution_tasks,
            "authorization_state": {
                "unblocker_resolution_queue_recorded": True,
                "unblocker_resolution_authorized": False,
                "materialization_execution_authorized": False,
                "network_access_authorized": False,
                "retrieval_executed": False,
                "source_content_fetched": False,
                "retrieval_logs_written": False,
                "content_hashes_written": False,
                "gap_closure_batches_executed": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Resolution tasks order open unblockers but do not authorize materialization or "
                "resolve any prerequisite by themselves."
            ),
        },
        "warning": "Queued unblocker resolution tasks remain open and are not proof evidence.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_checks(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_matrix: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_queue: dict[str, Any] | None = None,
) -> dict[str, Any]:
    matrix_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_matrix
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_matrix()
    )
    queue_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_queue
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_queue(
            matrix_doc
        )
    )
    matrix = matrix_doc["command_output_gap_closure_batch_execution_unblocker_matrix"]
    queue = queue_doc["command_output_gap_closure_batch_execution_unblocker_resolution_queue"]
    matrix_unblocker_ids = {
        cell["unblocker_id"]
        for row in matrix["matrix_rows"]
        for cell in row["unblockers"]
    }
    queue_unblocker_ids = {row["unblocker_id"] for row in queue["resolution_tasks"]}
    expected_orders = list(range(1, queue["resolution_task_count"] + 1))
    actual_orders = [row["resolution_order"] for row in queue["resolution_tasks"]]
    checks = [
        {
            "id": "check-unblocker-matrix-linked",
            "status": "complete"
            if queue["input_command_output_gap_closure_batch_execution_unblocker_matrix_id"] == matrix["id"]
            else "open",
            "input_command_output_gap_closure_batch_execution_unblocker_matrix_id": (
                queue["input_command_output_gap_closure_batch_execution_unblocker_matrix_id"]
            ),
            "command_output_gap_closure_batch_execution_unblocker_matrix_id": matrix["id"],
        },
        {
            "id": "check-resolution-tasks-cover-open-unblockers",
            "status": "complete" if queue_unblocker_ids == matrix_unblocker_ids else "open",
            "queue_unblocker_count": len(queue_unblocker_ids),
            "matrix_unblocker_count": len(matrix_unblocker_ids),
        },
        {
            "id": "check-resolution-task-order-complete",
            "status": "complete" if actual_orders == expected_orders else "open",
            "first_resolution_order": actual_orders[0] if actual_orders else None,
            "last_resolution_order": actual_orders[-1] if actual_orders else None,
        },
        {
            "id": "check-resolution-tasks-remain-open",
            "status": "blocked"
            if queue["open_resolution_task_count"] == queue["resolution_task_count"]
            and all(row["resolution_status"] == "queued_open" for row in queue["resolution_tasks"])
            and all(row["unblocker_resolved"] is False for row in queue["resolution_tasks"])
            else "open",
            "open_resolution_task_count": queue["open_resolution_task_count"],
            "resolution_task_count": queue["resolution_task_count"],
        },
        {
            "id": "check-unblocker-resolution-queue-not-proof",
            "status": "contested"
            if queue_doc["status"] == "blocked"
            and queue["authorization_state"]["proof_evidence_materialized"] is False
            and queue["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": queue["authorization_state"],
            "decision_rule": queue["decision_rule"],
        },
    ]
    return {
        "status": "blocked",
        "target_task_id": queue["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_content_materialization_unblocker_resolution_tasks_open",
        "checks": checks,
        "remaining_risks": [
            "unblocker resolution tasks remain open",
            "resolution queue authorizes no retrieval",
            "queued resolution tasks are not proof evidence",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_queue: dict[str, Any] | None = None,
) -> dict[str, Any]:
    queue_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_queue
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_queue()
    )
    queue = queue_doc["command_output_gap_closure_batch_execution_unblocker_resolution_queue"]
    resolution_batches = []
    for batch_order, unblocker_type in enumerate(queue["priority_order"], start=1):
        tasks = [
            task
            for task in queue["resolution_tasks"]
            if task["unblocker_type"] == unblocker_type
        ]
        resolution_batches.append({
            "resolution_batch_id": f"resolve-unblocker-batch-{unblocker_type}",
            "resolution_batch_order": batch_order,
            "unblocker_type": unblocker_type,
            "resolution_task_ids": [task["resolution_task_id"] for task in tasks],
            "resolution_task_count": len(tasks),
            "batch_status": "queued_open",
            "resolution_authorized": False,
            "unblockers_resolved": False,
            "proof_evidence_materialized": False,
        })
    return {
        "status": "blocked",
        "command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-batch-plan-v0",
            "input_command_output_gap_closure_batch_execution_unblocker_resolution_queue_id": queue["id"],
            "target_task_id": queue["target_task_id"],
            "target_pressure_test_id": queue["target_pressure_test_id"],
            "target_remediation_id": queue["target_remediation_id"],
            "plan_scope": "content_materialization_batch_execution_unblocker_resolution_batches",
            "retrieved_at": RETRIEVED_AT,
            "resolution_task_count": queue["resolution_task_count"],
            "resolution_batch_count": len(resolution_batches),
            "open_resolution_batch_count": len(resolution_batches),
            "priority_order": queue["priority_order"],
            "resolution_batches": resolution_batches,
            "authorization_state": {
                "unblocker_resolution_batch_plan_recorded": True,
                "unblocker_resolution_authorized": False,
                "materialization_execution_authorized": False,
                "network_access_authorized": False,
                "retrieval_executed": False,
                "source_content_fetched": False,
                "retrieval_logs_written": False,
                "content_hashes_written": False,
                "gap_closure_batches_executed": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Resolution batches group open unblocker tasks by prerequisite type, but "
                "do not authorize or resolve any prerequisite."
            ),
        },
        "warning": "Resolution batch planning is not materialization evidence.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_checks(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_queue: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    queue_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_queue
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_queue()
    )
    plan_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan(
            queue_doc
        )
    )
    queue = queue_doc["command_output_gap_closure_batch_execution_unblocker_resolution_queue"]
    plan = plan_doc["command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan"]
    queue_task_ids = {row["resolution_task_id"] for row in queue["resolution_tasks"]}
    batch_task_ids = {
        task_id
        for batch in plan["resolution_batches"]
        for task_id in batch["resolution_task_ids"]
    }
    batch_priority_order = [row["unblocker_type"] for row in plan["resolution_batches"]]
    checks = [
        {
            "id": "check-unblocker-resolution-queue-linked",
            "status": "complete"
            if plan["input_command_output_gap_closure_batch_execution_unblocker_resolution_queue_id"] == queue["id"]
            else "open",
            "input_command_output_gap_closure_batch_execution_unblocker_resolution_queue_id": (
                plan["input_command_output_gap_closure_batch_execution_unblocker_resolution_queue_id"]
            ),
            "command_output_gap_closure_batch_execution_unblocker_resolution_queue_id": queue["id"],
        },
        {
            "id": "check-resolution-batches-cover-tasks",
            "status": "complete" if batch_task_ids == queue_task_ids else "open",
            "batch_task_count": len(batch_task_ids),
            "queue_task_count": len(queue_task_ids),
        },
        {
            "id": "check-resolution-batches-follow-priority-order",
            "status": "complete" if batch_priority_order == queue["priority_order"] else "open",
            "batch_priority_order": batch_priority_order,
            "queue_priority_order": queue["priority_order"],
        },
        {
            "id": "check-resolution-batches-remain-open",
            "status": "blocked"
            if plan["open_resolution_batch_count"] == plan["resolution_batch_count"]
            and all(row["batch_status"] == "queued_open" for row in plan["resolution_batches"])
            and all(row["unblockers_resolved"] is False for row in plan["resolution_batches"])
            else "open",
            "open_resolution_batch_count": plan["open_resolution_batch_count"],
            "resolution_batch_count": plan["resolution_batch_count"],
        },
        {
            "id": "check-unblocker-resolution-batch-plan-not-proof",
            "status": "contested"
            if plan_doc["status"] == "blocked"
            and plan["authorization_state"]["proof_evidence_materialized"] is False
            and plan["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": plan["authorization_state"],
            "decision_rule": plan["decision_rule"],
        },
    ]
    return {
        "status": "blocked",
        "target_task_id": plan["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_content_materialization_unblocker_resolution_batches_open",
        "checks": checks,
        "remaining_risks": [
            "unblocker resolution batches remain open",
            "resolution batches authorize no retrieval",
            "resolution batch plan is not proof evidence",
        ],
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_execution_ledger(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    plan_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan()
    )
    plan = plan_doc["command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan"]
    execution_rows = []
    for batch in plan["resolution_batches"]:
        execution_rows.append({
            "execution_row_id": f"resolution-execution-{batch['resolution_batch_id']}",
            "resolution_batch_id": batch["resolution_batch_id"],
            "resolution_batch_order": batch["resolution_batch_order"],
            "unblocker_type": batch["unblocker_type"],
            "resolution_task_ids": batch["resolution_task_ids"],
            "resolution_task_count": batch["resolution_task_count"],
            "execution_status": "not_started_authorization_blocked",
            "execution_started": False,
            "execution_completed": False,
            "unblockers_resolved": False,
            "resolution_evidence_materialized": False,
            "proof_evidence_materialized": False,
        })
    return {
        "status": "blocked",
        "command_output_gap_closure_batch_execution_unblocker_resolution_batch_execution_ledger": {
            "id": "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-batch-execution-ledger-v0",
            "input_command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan_id": plan["id"],
            "target_task_id": plan["target_task_id"],
            "target_pressure_test_id": plan["target_pressure_test_id"],
            "target_remediation_id": plan["target_remediation_id"],
            "ledger_scope": "content_materialization_unblocker_resolution_batch_execution",
            "retrieved_at": RETRIEVED_AT,
            "resolution_batch_count": plan["resolution_batch_count"],
            "resolution_task_count": plan["resolution_task_count"],
            "executed_resolution_batch_count": 0,
            "resolved_unblocker_count": 0,
            "execution_rows": execution_rows,
            "authorization_state": {
                "unblocker_resolution_batch_execution_ledger_recorded": True,
                "unblocker_resolution_authorized": False,
                "materialization_execution_authorized": False,
                "network_access_authorized": False,
                "retrieval_executed": False,
                "source_content_fetched": False,
                "retrieval_logs_written": False,
                "content_hashes_written": False,
                "gap_closure_batches_executed": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Resolution batch execution has not started; no unblocker is resolved by this ledger."
            ),
        },
        "warning": "Execution ledger records no prerequisite resolution or proof evidence.",
    }


def _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_execution_checks(
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan: dict[str, Any] | None = None,
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_execution_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    plan_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan()
    )
    ledger_doc = (
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_execution_ledger
        or _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_execution_ledger(
            plan_doc
        )
    )
    plan = plan_doc["command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan"]
    ledger = ledger_doc["command_output_gap_closure_batch_execution_unblocker_resolution_batch_execution_ledger"]
    plan_batch_ids = {row["resolution_batch_id"] for row in plan["resolution_batches"]}
    ledger_batch_ids = {row["resolution_batch_id"] for row in ledger["execution_rows"]}
    checks = [
        {
            "id": "check-resolution-batch-plan-linked",
            "status": "complete"
            if ledger["input_command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan_id"] == plan["id"]
            else "open",
            "input_command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan_id": (
                ledger["input_command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan_id"]
            ),
            "command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan_id": plan["id"],
        },
        {
            "id": "check-execution-rows-cover-resolution-batches",
            "status": "complete" if ledger_batch_ids == plan_batch_ids else "open",
            "ledger_batch_ids": sorted(ledger_batch_ids),
            "plan_batch_ids": sorted(plan_batch_ids),
        },
        {
            "id": "check-resolution-batch-execution-not-started",
            "status": "blocked"
            if ledger["executed_resolution_batch_count"] == 0
            and all(row["execution_started"] is False for row in ledger["execution_rows"])
            and all(row["execution_status"] == "not_started_authorization_blocked" for row in ledger["execution_rows"])
            else "open",
            "executed_resolution_batch_count": ledger["executed_resolution_batch_count"],
        },
        {
            "id": "check-no-unblocker-resolution-materialized",
            "status": "blocked"
            if ledger["resolved_unblocker_count"] == 0
            and all(row["unblockers_resolved"] is False for row in ledger["execution_rows"])
            and all(row["resolution_evidence_materialized"] is False for row in ledger["execution_rows"])
            else "open",
            "resolved_unblocker_count": ledger["resolved_unblocker_count"],
        },
        {
            "id": "check-unblocker-resolution-batch-execution-ledger-not-proof",
            "status": "contested"
            if ledger_doc["status"] == "blocked"
            and ledger["authorization_state"]["proof_evidence_materialized"] is False
            and ledger["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": ledger["authorization_state"],
            "decision_rule": ledger["decision_rule"],
        },
    ]
    return {
        "status": "blocked",
        "target_task_id": ledger["target_task_id"],
        "scope": "bad_god_evidential_calibration_source_content_materialization_unblocker_resolution_batch_execution_not_started",
        "checks": checks,
        "remaining_risks": [
            "unblocker resolution batch execution has not started",
            "no unblocker resolution evidence was materialized",
            "resolution batch execution ledger is not proof evidence",
        ],
    }


def _build_ontological_soundness_resolution_worklist(
    ontological_soundness_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    checks = ontological_soundness_checks or _build_ontological_soundness_checks()
    direct_blockers = [
        row for row in checks["checks"]
        if row["status"] != "complete"
    ]
    linked_artifact_blockers = [
        row for row in checks["checks"]
        if row.get("artifact") and row.get("artifact_status") != "complete"
    ]
    work_items: list[dict[str, Any]] = []
    for row in direct_blockers:
        work_items.append({
            "work_item_id": f"resolve-{row['id']}",
            "work_category": "direct_soundness_check_resolution",
            "source_check_id": row["id"],
            "source_artifact": "ontological-soundness-checks.json",
            "source_status": row["status"],
            "required_action": row.get("result", "resolve the contested soundness check"),
            "required_output": "a complete check row linked to evidence without claiming proof",
            "work_status": "queued_not_executed",
            "proof_evidence_materialized": False,
        })
    for row in linked_artifact_blockers:
        work_items.append({
            "work_item_id": f"resolve-linked-{row['artifact'].removesuffix('.json')}",
            "work_category": "linked_artifact_resolution",
            "source_check_id": row["id"],
            "source_artifact": row["artifact"],
            "source_status": row["artifact_status"],
            "required_action": row.get("result", "resolve the linked contested artifact"),
            "required_output": "complete the linked artifact checks before promoting soundness",
            "work_status": "queued_not_executed",
            "proof_evidence_materialized": False,
        })
    return {
        "status": "contested",
        "worklist": {
            "id": "ontological-soundness-resolution-worklist-v0",
            "target_obligation_id": "obl-ontological-soundness",
            "argument_id": checks["argument_id"],
            "target_premise_id": checks["target_premise_id"],
            "input_artifact": "ontological-soundness-checks.json",
            "retrieved_at": RETRIEVED_AT,
            "work_items": work_items,
            "authorization_state": {
                "worklist_recorded": True,
                "soundness_proof_completed": False,
                "proof_claim_allowed": False,
                "work_items_executed": False,
            },
            "decision_rule": (
                "This worklist may guide next proof-search tasks, but it does "
                "not itself resolve ontological soundness or authorize a proof claim."
            ),
            "verdict": "contested",
        },
        "warning": "Queued work items are not proof evidence.",
    }


def _build_ontological_soundness_resolution_worklist_checks(
    ontological_soundness_checks: dict[str, Any] | None = None,
    ontological_soundness_resolution_worklist: dict[str, Any] | None = None,
) -> dict[str, Any]:
    soundness_checks = ontological_soundness_checks or _build_ontological_soundness_checks()
    worklist_doc = (
        ontological_soundness_resolution_worklist
        or _build_ontological_soundness_resolution_worklist(soundness_checks)
    )
    worklist = worklist_doc["worklist"]
    work_source_check_ids = {item["source_check_id"] for item in worklist["work_items"]}
    work_source_artifacts = {item["source_artifact"] for item in worklist["work_items"]}
    contested_check_ids = [
        row["id"] for row in soundness_checks["checks"]
        if row["status"] != "complete"
    ]
    contested_linked_artifacts = [
        row["artifact"] for row in soundness_checks["checks"]
        if row.get("artifact") and row.get("artifact_status") != "complete"
    ]
    unexecuted_work_item_ids = [
        item["work_item_id"] for item in worklist["work_items"]
        if item["work_status"] == "queued_not_executed"
        and item["proof_evidence_materialized"] is False
    ]
    checks = [
        {
            "id": "check-ontological-soundness-checks-linked",
            "status": "complete"
            if worklist["input_artifact"] == "ontological-soundness-checks.json"
            and worklist["target_obligation_id"] == "obl-ontological-soundness"
            else "open",
            "input_artifact": worklist["input_artifact"],
            "target_obligation_id": worklist["target_obligation_id"],
        },
        {
            "id": "check-contested-soundness-checks-have-work-items",
            "status": "complete" if set(contested_check_ids) <= work_source_check_ids else "open",
            "contested_check_ids": contested_check_ids,
            "work_source_check_ids": sorted(work_source_check_ids),
            "missing_check_ids": sorted(set(contested_check_ids) - work_source_check_ids),
        },
        {
            "id": "check-contested-linked-artifacts-have-work-items",
            "status": "complete" if set(contested_linked_artifacts) <= work_source_artifacts else "open",
            "contested_linked_artifacts": contested_linked_artifacts,
            "work_source_artifacts": sorted(work_source_artifacts),
            "missing_artifacts": sorted(set(contested_linked_artifacts) - work_source_artifacts),
        },
        {
            "id": "check-work-items-remain-unexecuted",
            "status": "complete" if len(unexecuted_work_item_ids) == len(worklist["work_items"]) else "open",
            "work_item_ids": unexecuted_work_item_ids,
        },
        {
            "id": "check-worklist-not-promoted-to-proof",
            "status": "contested"
            if worklist["verdict"] == "contested"
            and worklist["authorization_state"]["soundness_proof_completed"] is False
            and worklist["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": worklist["authorization_state"],
            "decision_rule": worklist["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_obligation_id": worklist["target_obligation_id"],
        "argument_id": worklist["argument_id"],
        "target_premise_id": worklist["target_premise_id"],
        "scope": "ontological_soundness_resolution_worklist_not_proof",
        "checks": checks,
        "remaining_risks": [
            "soundness work items are queued but not executed",
            "linked contested artifacts still block the possibility premise",
            "proof claim remains disallowed until the blocking obligation is complete",
        ],
    }


def _build_ontological_soundness_resolution_batches(
    ontological_soundness_resolution_worklist: dict[str, Any] | None = None,
) -> dict[str, Any]:
    worklist_doc = ontological_soundness_resolution_worklist or _build_ontological_soundness_resolution_worklist()
    worklist = worklist_doc["worklist"]
    verifier_commands = [
        "rtk env PYTHONPATH=src python3 -m pytest tests/test_godproof.py -q",
        "rtk env PYTHONPATH=src python3 -m pytest -q",
    ]
    batch_specs = [
        (
            "resolve-dossier-direct-blockers",
            "Resolve direct contested rows in ontological-soundness-checks.json.",
            {"ontological-soundness-checks.json"},
            ["check-unresolved-parodies-retained", "check-soundness-not-promoted"],
        ),
        (
            "resolve-coherence-and-conceivability-chain",
            "Close attribute coherence and coherent conceivability blockers.",
            {"attribute-coherence-checks.json", "coherent-conceivability-checks.json"},
            ["check-unresolved-attribute-tensions-retained", "check-live-defeaters-retained"],
        ),
        (
            "resolve-possibility-bridge-chain",
            "Close metaphysical and possible necessary existence bridge blockers.",
            {
                "metaphysical-possibility-checks.json",
                "possible-necessary-existence-checks.json",
                "possibility-premise-checks.json",
            },
            [
                "check-independent-complete-route-missing",
                "check-live-defeaters-block-bridge",
                "check-blocked-possibility-stages-retained",
            ],
        ),
        (
            "resolve-rival-and-positive-property-chain",
            "Close definition-smuggling, rival parity, and positive-property blockers.",
            {
                "definition-smuggling-checks.json",
                "rival-necessary-parity-checks.json",
                "positive-property-filter-checks.json",
                "positive-grounding-checks.json",
                "moral-perfection-grounding-checks.json",
            },
            [
                "check-independent-support-still-fails",
                "check-unresolved-rivals-retained",
                "check-positive-grounding-still-contested",
            ],
        ),
        (
            "resolve-evidential-evil-and-moral-pressure-chain",
            "Close evidential evil model and hiddenness moral-pressure blockers.",
            {
                "evidential-evil-probability-checks.json",
                "evidential-evil-likelihood-checks.json",
                "evidential-evil-dependence-checks.json",
                "evidential-evil-calibration-checks.json",
                "evidential-evil-case-corpus-checks.json",
                "evidential-evil-reviewed-case-records-checks.json",
                "evidential-evil-empirical-expansion-checks.json",
                "evil-hiddenness-moral-pressure-checks.json",
            },
            [
                "check-live-objections-retained",
                "check-wide-intervals-retained",
                "check-moral-pressure-responses-still-open",
            ],
        ),
        (
            "resolve-evidence-governance-and-ingestion-chain",
            "Close dataset selection, license, acquisition, hash, and minimization blockers.",
            {
                "evidential-evil-primary-dataset-selection-checks.json",
                "evidential-evil-dataset-ingestion-checks.json",
                "evidential-evil-license-privacy-checks.json",
                "evidential-evil-attribution-template-checks.json",
                "evidential-evil-license-decision-checks.json",
                "evidential-evil-source-acquisition-hash-runbook-checks.json",
                "evidential-evil-suppression-report-template-checks.json",
                "evidential-evil-source-version-hash-preflight-checks.json",
                "evidential-evil-derived-aggregate-schema-checks.json",
                "evidential-evil-microdata-minimization-checks.json",
            },
            [
                "check-license-decisions-still-open",
                "check-ingestion-not-executed",
                "check-downloads-and-hashes-still-open",
            ],
        ),
    ]
    batches = []
    assigned_work_item_ids: set[str] = set()
    for order, (batch_id, objective, source_artifacts, completion_gate_ids) in enumerate(batch_specs, start=1):
        work_item_ids = [
            item["work_item_id"] for item in worklist["work_items"]
            if item["source_artifact"] in source_artifacts
        ]
        assigned_work_item_ids.update(work_item_ids)
        batches.append({
            "batch_id": batch_id,
            "order": order,
            "objective": objective,
            "source_artifacts": sorted(source_artifacts),
            "work_item_ids": work_item_ids,
            "completion_gate_ids": completion_gate_ids,
            "acceptance_criteria": [
                "all referenced work items have corresponding complete check rows",
                "proof-readiness.json still blocks proof unless every soundness check is complete",
                "transcript.jsonl records the batch checks before any proof claim",
            ],
            "verifier_commands": verifier_commands,
            "batch_status": "queued_not_executed",
            "proof_evidence_materialized": False,
        })
    unassigned_work_item_ids = sorted({
        item["work_item_id"] for item in worklist["work_items"]
    } - assigned_work_item_ids)
    return {
        "status": "contested",
        "batch_plan": {
            "id": "ontological-soundness-resolution-batches-v0",
            "input_worklist_id": worklist["id"],
            "target_obligation_id": worklist["target_obligation_id"],
            "argument_id": worklist["argument_id"],
            "target_premise_id": worklist["target_premise_id"],
            "retrieved_at": RETRIEVED_AT,
            "batches": batches,
            "unassigned_work_item_ids": unassigned_work_item_ids,
            "authorization_state": {
                "batches_recorded": True,
                "batch_execution_completed": False,
                "proof_claim_allowed": False,
                "proof_evidence_materialized": False,
            },
            "decision_rule": (
                "Batches order soundness-resolution work and verifiers only; "
                "they do not execute work or promote evidence."
            ),
            "verdict": "contested",
        },
        "warning": "Queued batches are execution plans, not proof evidence.",
    }


def _build_ontological_soundness_resolution_batch_checks(
    ontological_soundness_resolution_worklist: dict[str, Any] | None = None,
    ontological_soundness_resolution_batches: dict[str, Any] | None = None,
) -> dict[str, Any]:
    worklist_doc = ontological_soundness_resolution_worklist or _build_ontological_soundness_resolution_worklist()
    batches_doc = (
        ontological_soundness_resolution_batches
        or _build_ontological_soundness_resolution_batches(worklist_doc)
    )
    worklist = worklist_doc["worklist"]
    batch_plan = batches_doc["batch_plan"]
    work_item_ids = {item["work_item_id"] for item in worklist["work_items"]}
    batch_work_item_ids = {
        work_item_id
        for batch in batch_plan["batches"]
        for work_item_id in batch["work_item_ids"]
    }
    unexecuted_batch_ids = [
        batch["batch_id"] for batch in batch_plan["batches"]
        if batch["batch_status"] == "queued_not_executed"
        and batch["proof_evidence_materialized"] is False
    ]
    batches_with_verifiers = [
        batch["batch_id"] for batch in batch_plan["batches"]
        if batch["verifier_commands"] and batch["completion_gate_ids"] and batch["acceptance_criteria"]
    ]
    checks = [
        {
            "id": "check-resolution-worklist-linked",
            "status": "complete"
            if batch_plan["input_worklist_id"] == worklist["id"]
            and batch_plan["target_obligation_id"] == worklist["target_obligation_id"]
            else "open",
            "input_worklist_id": batch_plan["input_worklist_id"],
            "worklist_id": worklist["id"],
        },
        {
            "id": "check-every-work-item-assigned-to-batch",
            "status": "complete"
            if work_item_ids <= batch_work_item_ids and not batch_plan["unassigned_work_item_ids"]
            else "open",
            "work_item_count": len(work_item_ids),
            "batch_work_item_count": len(batch_work_item_ids),
            "unassigned_work_item_ids": batch_plan["unassigned_work_item_ids"],
        },
        {
            "id": "check-batches-have-verifiers-and-acceptance-gates",
            "status": "complete"
            if len(batches_with_verifiers) == len(batch_plan["batches"])
            else "open",
            "batch_ids": batches_with_verifiers,
        },
        {
            "id": "check-batches-remain-unexecuted",
            "status": "complete" if len(unexecuted_batch_ids) == len(batch_plan["batches"]) else "open",
            "batch_ids": unexecuted_batch_ids,
        },
        {
            "id": "check-batches-not-promoted-to-proof",
            "status": "contested"
            if batch_plan["verdict"] == "contested"
            and batch_plan["authorization_state"]["batch_execution_completed"] is False
            and batch_plan["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": batch_plan["authorization_state"],
            "decision_rule": batch_plan["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_obligation_id": batch_plan["target_obligation_id"],
        "argument_id": batch_plan["argument_id"],
        "target_premise_id": batch_plan["target_premise_id"],
        "scope": "ontological_soundness_resolution_batches_not_proof",
        "checks": checks,
        "remaining_risks": [
            "batches are queued but not executed",
            "work item outputs are not materialized as soundness evidence",
            "proof claim remains disallowed until all blocking checks complete",
        ],
    }


def _build_ontological_soundness_batch_execution_ledger(
    ontological_soundness_resolution_batches: dict[str, Any] | None = None,
) -> dict[str, Any]:
    batches_doc = ontological_soundness_resolution_batches or _build_ontological_soundness_resolution_batches()
    batch_plan = batches_doc["batch_plan"]
    execution_records = []
    for batch in batch_plan["batches"]:
        execution_records.append({
            "execution_record_id": f"execute-{batch['batch_id']}",
            "batch_id": batch["batch_id"],
            "batch_order": batch["order"],
            "input_batch_plan_id": batch_plan["id"],
            "target_obligation_id": batch_plan["target_obligation_id"],
            "verifier_commands": batch["verifier_commands"],
            "output_artifact_targets": batch["source_artifacts"],
            "future_log_event_types": [
                f"ontological_soundness_batch_{batch['batch_id'].replace('-', '_')}_started",
                f"ontological_soundness_batch_{batch['batch_id'].replace('-', '_')}_verified",
                f"ontological_soundness_batch_{batch['batch_id'].replace('-', '_')}_closed",
            ],
            "acceptance_criteria": batch["acceptance_criteria"],
            "completion_gate_ids": batch["completion_gate_ids"],
            "execution_status": "not_started",
            "proof_evidence_materialized": False,
        })
    return {
        "status": "contested",
        "ledger": {
            "id": "ontological-soundness-batch-execution-ledger-v0",
            "input_batch_plan_id": batch_plan["id"],
            "target_obligation_id": batch_plan["target_obligation_id"],
            "argument_id": batch_plan["argument_id"],
            "target_premise_id": batch_plan["target_premise_id"],
            "retrieved_at": RETRIEVED_AT,
            "execution_records": execution_records,
            "authorization_state": {
                "execution_ledger_recorded": True,
                "batch_execution_started": False,
                "batch_execution_completed": False,
                "proof_evidence_materialized": False,
                "proof_claim_allowed": False,
            },
            "decision_rule": (
                "Execution records define future auditable batch attempts only. "
                "No batch is executed or promoted by recording this ledger."
            ),
            "verdict": "contested",
        },
        "warning": "Execution ledger is an audit scaffold, not executed proof work.",
    }


def _build_ontological_soundness_batch_execution_checks(
    ontological_soundness_resolution_batches: dict[str, Any] | None = None,
    ontological_soundness_batch_execution_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    batches_doc = ontological_soundness_resolution_batches or _build_ontological_soundness_resolution_batches()
    ledger_doc = (
        ontological_soundness_batch_execution_ledger
        or _build_ontological_soundness_batch_execution_ledger(batches_doc)
    )
    batch_plan = batches_doc["batch_plan"]
    ledger = ledger_doc["ledger"]
    batch_ids = {batch["batch_id"] for batch in batch_plan["batches"]}
    record_batch_ids = {record["batch_id"] for record in ledger["execution_records"]}
    complete_record_ids = [
        record["execution_record_id"] for record in ledger["execution_records"]
        if record["future_log_event_types"]
        and record["verifier_commands"]
        and record["output_artifact_targets"]
    ]
    not_started_record_ids = [
        record["execution_record_id"] for record in ledger["execution_records"]
        if record["execution_status"] == "not_started"
        and record["proof_evidence_materialized"] is False
    ]
    checks = [
        {
            "id": "check-batch-plan-linked",
            "status": "complete"
            if ledger["input_batch_plan_id"] == batch_plan["id"]
            and ledger["target_obligation_id"] == batch_plan["target_obligation_id"]
            else "open",
            "input_batch_plan_id": ledger["input_batch_plan_id"],
            "batch_plan_id": batch_plan["id"],
        },
        {
            "id": "check-every-batch-has-execution-record",
            "status": "complete" if batch_ids <= record_batch_ids else "open",
            "batch_ids": sorted(batch_ids),
            "record_batch_ids": sorted(record_batch_ids),
            "missing_batch_ids": sorted(batch_ids - record_batch_ids),
        },
        {
            "id": "check-execution-records-have-logs-verifiers-and-targets",
            "status": "complete" if len(complete_record_ids) == len(ledger["execution_records"]) else "open",
            "execution_record_ids": complete_record_ids,
        },
        {
            "id": "check-execution-not-started",
            "status": "complete" if len(not_started_record_ids) == len(ledger["execution_records"]) else "open",
            "execution_record_ids": not_started_record_ids,
        },
        {
            "id": "check-execution-ledger-not-promoted-to-proof",
            "status": "contested"
            if ledger["verdict"] == "contested"
            and ledger["authorization_state"]["batch_execution_started"] is False
            and ledger["authorization_state"]["proof_claim_allowed"] is False
            else "open",
            "authorization_state": ledger["authorization_state"],
            "decision_rule": ledger["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_obligation_id": ledger["target_obligation_id"],
        "argument_id": ledger["argument_id"],
        "target_premise_id": ledger["target_premise_id"],
        "scope": "ontological_soundness_batch_execution_ledger_not_executed",
        "checks": checks,
        "remaining_risks": [
            "batch execution has not started",
            "no verifier output is attached to the ledger",
            "proof claim remains disallowed until execution produces complete soundness evidence",
        ],
    }


def _build_coverage_matrix() -> dict[str, Any]:
    by_domain: dict[str, list[WisdomEntry]] = {
        domain: [] for domain in REQUIRED_WISDOM_DOMAINS
    }
    for entry in WISDOM_CORPUS:
        by_domain.setdefault(entry.domain, []).append(entry)

    domains: list[dict[str, Any]] = []
    missing_domains: list[str] = []
    thin_domains: list[str] = []
    for domain in REQUIRED_WISDOM_DOMAINS:
        entries = by_domain.get(domain, [])
        source_ids = sorted({source_id for entry in entries for source_id in entry.source_ids})
        stances = sorted({entry.stance for entry in entries})
        status = "covered" if entries and source_ids else "missing"
        if status == "missing":
            missing_domains.append(domain)
        elif len(entries) < 2 and domain in {"comparative_religion", "science_and_cosmology", "non_theistic_alternatives"}:
            status = "thin"
            thin_domains.append(domain)
        domains.append({
            "domain": domain,
            "status": status,
            "entry_ids": [entry.id for entry in entries],
            "source_ids": source_ids,
            "stances": stances,
        })

    covered_count = sum(1 for domain in domains if domain["status"] == "covered")
    thin_count = sum(1 for domain in domains if domain["status"] == "thin")
    score = (covered_count + 0.5 * thin_count) / max(1, len(REQUIRED_WISDOM_DOMAINS))
    return {
        "status": "incomplete" if missing_domains or thin_domains else "covered",
        "coverage_score": round(score, 3),
        "required_domain_count": len(REQUIRED_WISDOM_DOMAINS),
        "covered_domain_count": covered_count,
        "thin_domain_count": thin_count,
        "missing_domains": missing_domains,
        "thin_domains": thin_domains,
        "domains": domains,
        "rule": "The system must not claim all human wisdom is gathered while any required domain is missing or thin.",
    }


def _build_human_wisdom_intake_roadmap() -> dict[str, Any]:
    return {
        "status": "contested",
        "roadmap": HUMAN_WISDOM_INTAKE_ROADMAP,
        "warning": (
            "This roadmap extends the intake horizon beyond current required-domain coverage. "
            "It does not claim that all human wisdom has been gathered."
        ),
    }


def _build_human_wisdom_primary_source_seed_ledger() -> dict[str, Any]:
    return {
        "status": "contested",
        "ledger": HUMAN_WISDOM_PRIMARY_SOURCE_SEED_LEDGER,
        "warning": (
            "This ledger records primary-source locators only. "
            "It does not ingest source text or extend the wisdom corpus."
        ),
    }


def _build_human_wisdom_primary_source_extraction_queue() -> dict[str, Any]:
    return {
        "status": "contested",
        "queue": HUMAN_WISDOM_PRIMARY_SOURCE_EXTRACTION_QUEUE,
        "warning": (
            "This queue records minimized extraction tasks only. "
            "It does not ingest primary text or materialize wisdom entries."
        ),
    }


def _build_human_wisdom_primary_source_summary_candidates() -> dict[str, Any]:
    return {
        "status": "contested",
        "candidates": HUMAN_WISDOM_PRIMARY_SOURCE_SUMMARY_CANDIDATES,
        "warning": (
            "These are paraphrase-only summary candidates. "
            "They are not accepted wisdom corpus entries or proof-graph evidence."
        ),
    }


def _build_human_wisdom_counterpressure_edge_proposals() -> dict[str, Any]:
    return {
        "status": "contested",
        "proposals": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_PROPOSALS,
        "warning": (
            "These are candidate counterpressure edges only. "
            "They are not proof-graph edges or proof evidence."
        ),
    }


def _build_human_wisdom_counterpressure_edge_checks() -> dict[str, Any]:
    proposals = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_PROPOSALS
    candidates = HUMAN_WISDOM_PRIMARY_SOURCE_SUMMARY_CANDIDATES
    candidate_ids = {item["candidate_id"] for item in candidates["summary_candidates"]}
    proposal_candidate_ids = {item["candidate_id"] for item in proposals["edge_proposals"]}
    proposals_with_targets = [
        item["proposal_id"] for item in proposals["edge_proposals"]
        if item["target_counterpressure_ids"]
        and item["target_argument_ids"]
        and item["materialization_status"] == "proposal_not_in_proof_graph"
    ]
    open_execution_requirement_ids = [
        requirement["id"] for requirement in proposals["execution_requirements"]
        if requirement["status"] == "open"
    ]
    checks = [
        {
            "id": "check-summary-candidates-linked",
            "status": "complete"
            if proposals["input_summary_candidates_id"] == candidates["id"]
            else "open",
            "artifact": "human-wisdom-primary-source-summary-candidates.json",
            "input_summary_candidates_id": proposals["input_summary_candidates_id"],
        },
        {
            "id": "check-every-summary-candidate-has-edge-proposal",
            "status": "complete" if candidate_ids <= proposal_candidate_ids else "open",
            "candidate_ids": sorted(candidate_ids),
            "proposal_candidate_ids": sorted(proposal_candidate_ids),
            "missing_candidate_ids": sorted(candidate_ids - proposal_candidate_ids),
        },
        {
            "id": "check-counterpressure-targets-present",
            "status": "complete" if len(proposals_with_targets) == len(proposals["edge_proposals"]) else "open",
            "proposal_ids": proposals_with_targets,
        },
        {
            "id": "check-proof-graph-materialization-still-open",
            "status": "contested" if open_execution_requirement_ids else "complete",
            "open_execution_requirement_ids": open_execution_requirement_ids,
            "authorization_state": proposals["authorization_state"],
        },
        {
            "id": "check-counterpressure-edge-proposals-not-promoted",
            "status": "contested" if proposals["verdict"] == "contested" else "open",
            "verdict": proposals["verdict"],
            "decision_rule": proposals["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_concept_id": proposals["target_concept_id"],
        "scope": "counterpressure_edge_proposals_not_proof_graph_edges",
        "checks": checks,
        "remaining_risks": [
            "counterpressure edge review is not complete",
            "passage-level citation locators are not linked to edge proposals",
            "translation provenance is not linked to edge proposals",
            "proof-graph edge materialization is not complete",
        ],
    }


def _build_human_wisdom_counterpressure_edge_review_queue() -> dict[str, Any]:
    return {
        "status": "contested",
        "queue": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_REVIEW_QUEUE,
        "warning": (
            "This queue records review work for candidate counterpressure edges only. "
            "It does not authorize proof-graph materialization."
        ),
    }


def _build_human_wisdom_counterpressure_edge_review_checks() -> dict[str, Any]:
    queue = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_REVIEW_QUEUE
    proposals = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_PROPOSALS
    proposal_ids = {item["proposal_id"] for item in proposals["edge_proposals"]}
    review_proposal_ids = {item["proposal_id"] for item in queue["review_items"]}
    unreviewed_item_ids = [
        item["review_id"] for item in queue["review_items"]
        if item["review_status"] == "queued_not_reviewed"
        and item["source_text_ingested"] is False
        and item["materialization_status"] == "not_authorized"
    ]
    open_execution_requirement_ids = [
        requirement["id"] for requirement in queue["execution_requirements"]
        if requirement["status"] == "open"
    ]
    checks = [
        {
            "id": "check-edge-proposals-linked",
            "status": "complete"
            if queue["input_edge_proposals_id"] == proposals["id"]
            else "open",
            "artifact": "human-wisdom-counterpressure-edge-proposals.json",
            "input_edge_proposals_id": queue["input_edge_proposals_id"],
        },
        {
            "id": "check-every-edge-proposal-has-review-item",
            "status": "complete" if proposal_ids <= review_proposal_ids else "open",
            "proposal_ids": sorted(proposal_ids),
            "review_proposal_ids": sorted(review_proposal_ids),
            "missing_proposal_ids": sorted(proposal_ids - review_proposal_ids),
        },
        {
            "id": "check-review-items-remain-unreviewed",
            "status": "complete" if len(unreviewed_item_ids) == len(queue["review_items"]) else "open",
            "review_ids": unreviewed_item_ids,
        },
        {
            "id": "check-edge-materialization-authorization-still-open",
            "status": "contested" if open_execution_requirement_ids else "complete",
            "open_execution_requirement_ids": open_execution_requirement_ids,
            "authorization_state": queue["authorization_state"],
        },
        {
            "id": "check-review-queue-not-promoted",
            "status": "contested" if queue["verdict"] == "contested" else "open",
            "verdict": queue["verdict"],
            "decision_rule": queue["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_concept_id": queue["target_concept_id"],
        "scope": "counterpressure_edge_review_queue_not_materialization_authority",
        "checks": checks,
        "remaining_risks": [
            "edge relation review is not complete",
            "edge locator and provenance review is not complete",
            "edge materialization decisions are not recorded",
            "proof-graph edge writes are not authorized",
        ],
    }


def _build_human_wisdom_counterpressure_edge_review_rubric() -> dict[str, Any]:
    return {
        "status": "contested",
        "rubric": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_REVIEW_RUBRIC,
        "warning": (
            "This rubric records a programmable review schema only. "
            "It is not an applied review result or proof-graph authorization."
        ),
    }


def _build_human_wisdom_counterpressure_edge_review_rubric_checks() -> dict[str, Any]:
    rubric = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_REVIEW_RUBRIC
    queue = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_REVIEW_QUEUE
    required_axes = {
        axis
        for item in queue["review_items"]
        for axis in item["required_review_axes"]
    }
    covered_axes = set(rubric["covered_review_axes"])
    decision_schema = rubric["decision_schema"]
    materialization_gate = rubric["materialization_gate"]
    checks = [
        {
            "id": "check-review-queue-linked",
            "status": "complete" if rubric["input_review_queue_id"] == queue["id"] else "open",
            "artifact": "human-wisdom-counterpressure-edge-review-queue.json",
            "input_review_queue_id": rubric["input_review_queue_id"],
        },
        {
            "id": "check-required-review-axes-covered",
            "status": "complete" if required_axes <= covered_axes else "open",
            "required_axes": sorted(required_axes),
            "covered_axes": sorted(covered_axes),
            "missing_axes": sorted(required_axes - covered_axes),
        },
        {
            "id": "check-decision-schema-recorded",
            "status": "complete"
            if {"accept", "reject", "split", "defer"} <= set(decision_schema["allowed_decisions"])
            and {"decision", "relation_type", "reviewer_rationale"} <= set(decision_schema["required_fields"])
            else "open",
            "decision_schema": decision_schema,
        },
        {
            "id": "check-rubric-application-still-open",
            "status": "contested"
            if rubric["authorization_state"]["review_items_completed"] is False
            and rubric["authorization_state"]["materialization_authorized"] is False
            and materialization_gate["requires_review_item_decision"] is True
            else "complete",
            "authorization_state": rubric["authorization_state"],
            "materialization_gate": materialization_gate,
        },
        {
            "id": "check-rubric-not-promoted",
            "status": "contested" if rubric["verdict"] == "contested" else "open",
            "verdict": rubric["verdict"],
            "decision_rule": rubric["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_concept_id": rubric["target_concept_id"],
        "scope": "counterpressure_edge_review_rubric_not_applied_review",
        "checks": checks,
        "remaining_risks": [
            "rubric has not been applied to review items",
            "review items have no recorded decisions",
            "proof-graph edge materialization remains unauthorized",
        ],
    }


def _build_human_wisdom_counterpressure_edge_review_decisions() -> dict[str, Any]:
    return {
        "status": "contested",
        "decisions": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_REVIEW_DECISIONS,
        "warning": (
            "These are defer-only rubric application decisions. "
            "They do not authorize proof-graph materialization."
        ),
    }


def _build_human_wisdom_counterpressure_edge_review_decision_checks() -> dict[str, Any]:
    decisions = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_REVIEW_DECISIONS
    queue = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_REVIEW_QUEUE
    rubric = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_REVIEW_RUBRIC
    review_ids = {item["review_id"] for item in queue["review_items"]}
    decision_review_ids = {item["review_id"] for item in decisions["decision_records"]}
    deferred_decision_ids = [
        item["decision_id"] for item in decisions["decision_records"]
        if item["decision"] == "defer"
        and item["materialization_status"] == "deferred_not_in_proof_graph"
        and item["source_text_ingested"] is False
    ]
    materialized_decision_ids = [
        item["decision_id"] for item in decisions["decision_records"]
        if item["decision"] in rubric["decision_schema"]["proof_graph_write_decisions"]
        or item["materialization_status"] != "deferred_not_in_proof_graph"
    ]
    checks = [
        {
            "id": "check-review-rubric-linked",
            "status": "complete"
            if decisions["input_review_rubric_id"] == rubric["id"]
            else "open",
            "artifact": "human-wisdom-counterpressure-edge-review-rubric.json",
            "input_review_rubric_id": decisions["input_review_rubric_id"],
        },
        {
            "id": "check-review-queue-linked",
            "status": "complete"
            if decisions["input_review_queue_id"] == queue["id"]
            else "open",
            "artifact": "human-wisdom-counterpressure-edge-review-queue.json",
            "input_review_queue_id": decisions["input_review_queue_id"],
        },
        {
            "id": "check-every-review-item-has-defer-decision",
            "status": "complete"
            if review_ids <= decision_review_ids
            and len(deferred_decision_ids) == len(decisions["decision_records"])
            else "open",
            "review_ids": sorted(review_ids),
            "decision_review_ids": sorted(decision_review_ids),
            "missing_review_ids": sorted(review_ids - decision_review_ids),
            "deferred_decision_ids": deferred_decision_ids,
        },
        {
            "id": "check-no-proof-graph-materialization-from-decisions",
            "status": "complete"
            if not materialized_decision_ids
            and decisions["authorization_state"]["accepted_edges"] == 0
            and decisions["authorization_state"]["materialization_authorized"] is False
            else "open",
            "materialized_decision_ids": materialized_decision_ids,
            "authorization_state": decisions["authorization_state"],
        },
        {
            "id": "check-decision-ledger-still-contested",
            "status": "contested" if decisions["verdict"] == "contested" else "open",
            "verdict": decisions["verdict"],
            "decision_rule": decisions["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_concept_id": decisions["target_concept_id"],
        "scope": "defer_only_edge_review_decisions_not_proof_graph_materialization",
        "checks": checks,
        "remaining_risks": [
            "no edge has source-backed accept or reject review",
            "passage locators and translation provenance remain open",
            "proof-graph edge materialization remains unauthorized",
        ],
    }


def _build_human_wisdom_counterpressure_edge_resolution_packet() -> dict[str, Any]:
    return {
        "status": "contested",
        "packet": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_RESOLUTION_PACKET,
        "warning": (
            "This packet records open locator and provenance resolution tasks only. "
            "It does not ingest source text or authorize proof-graph writes."
        ),
    }


def _build_human_wisdom_counterpressure_edge_resolution_checks() -> dict[str, Any]:
    packet = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_RESOLUTION_PACKET
    decisions = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_REVIEW_DECISIONS
    defer_decision_ids = {
        item["decision_id"] for item in decisions["decision_records"]
        if item["decision"] == "defer"
    }
    task_decision_ids = {item["decision_id"] for item in packet["resolution_tasks"]}
    tasks_with_required_fields = [
        item["task_id"] for item in packet["resolution_tasks"]
        if {"passage_locator", "translation_provenance"} <= set(item["required_resolution_fields"])
        and item["source_text_ingested"] is False
        and item["materialization_status"] == "resolution_prerequisite_not_evidence"
    ]
    open_task_ids = [
        item["task_id"] for item in packet["resolution_tasks"]
        if item["task_status"] == "open"
    ]
    checks = [
        {
            "id": "check-decision-ledger-linked",
            "status": "complete"
            if packet["input_review_decisions_id"] == decisions["id"]
            else "open",
            "artifact": "human-wisdom-counterpressure-edge-review-decisions.json",
            "input_review_decisions_id": packet["input_review_decisions_id"],
        },
        {
            "id": "check-every-defer-decision-has-resolution-task",
            "status": "complete" if defer_decision_ids <= task_decision_ids else "open",
            "defer_decision_ids": sorted(defer_decision_ids),
            "task_decision_ids": sorted(task_decision_ids),
            "missing_decision_ids": sorted(defer_decision_ids - task_decision_ids),
        },
        {
            "id": "check-locator-and-provenance-fields-required",
            "status": "complete" if len(tasks_with_required_fields) == len(packet["resolution_tasks"]) else "open",
            "task_ids": tasks_with_required_fields,
        },
        {
            "id": "check-resolution-tasks-still-open",
            "status": "contested" if open_task_ids else "complete",
            "open_task_ids": open_task_ids,
            "authorization_state": packet["authorization_state"],
        },
        {
            "id": "check-resolution-packet-not-promoted",
            "status": "contested" if packet["verdict"] == "contested" else "open",
            "verdict": packet["verdict"],
            "decision_rule": packet["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_concept_id": packet["target_concept_id"],
        "scope": "locator_provenance_resolution_tasks_not_evidence",
        "checks": checks,
        "remaining_risks": [
            "passage locators are not resolved",
            "translation provenance is not resolved",
            "source text remains un-ingested",
            "proof-graph edge materialization remains unauthorized",
        ],
    }


def _build_human_wisdom_counterpressure_edge_evidence_request_queue() -> dict[str, Any]:
    return {
        "status": "contested",
        "queue": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_EVIDENCE_REQUEST_QUEUE,
        "warning": (
            "This queue records metadata-only evidence requests. "
            "No source text has been fetched, ingested, or promoted."
        ),
    }


def _build_human_wisdom_counterpressure_edge_evidence_request_checks() -> dict[str, Any]:
    queue = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_EVIDENCE_REQUEST_QUEUE
    packet = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_RESOLUTION_PACKET
    open_task_ids = {
        item["task_id"] for item in packet["resolution_tasks"]
        if item["task_status"] == "open"
    }
    request_task_ids = {item["task_id"] for item in queue["evidence_requests"]}
    requests_with_required_fields = [
        item["request_id"] for item in queue["evidence_requests"]
        if {"passage_locator", "translation_provenance", "license_or_use_basis"}
        <= set(item["requested_evidence_fields"])
        and item["source_text_ingested"] is False
        and item["materialization_status"] == "request_not_evidence"
    ]
    queued_request_ids = [
        item["request_id"] for item in queue["evidence_requests"]
        if item["request_status"] == "queued_not_fetched"
    ]
    checks = [
        {
            "id": "check-resolution-packet-linked",
            "status": "complete"
            if queue["input_resolution_packet_id"] == packet["id"]
            else "open",
            "artifact": "human-wisdom-counterpressure-edge-resolution-packet.json",
            "input_resolution_packet_id": queue["input_resolution_packet_id"],
        },
        {
            "id": "check-every-open-resolution-task-has-evidence-request",
            "status": "complete" if open_task_ids <= request_task_ids else "open",
            "open_task_ids": sorted(open_task_ids),
            "request_task_ids": sorted(request_task_ids),
            "missing_task_ids": sorted(open_task_ids - request_task_ids),
        },
        {
            "id": "check-request-fields-cover-locator-provenance-license",
            "status": "complete" if len(requests_with_required_fields) == len(queue["evidence_requests"]) else "open",
            "request_ids": requests_with_required_fields,
        },
        {
            "id": "check-evidence-requests-not-fetched",
            "status": "contested" if len(queued_request_ids) == len(queue["evidence_requests"]) else "open",
            "queued_request_ids": queued_request_ids,
            "authorization_state": queue["authorization_state"],
        },
        {
            "id": "check-evidence-request-queue-not-promoted",
            "status": "contested" if queue["verdict"] == "contested" else "open",
            "verdict": queue["verdict"],
            "decision_rule": queue["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_concept_id": queue["target_concept_id"],
        "scope": "metadata_request_queue_not_fetched_evidence",
        "checks": checks,
        "remaining_risks": [
            "evidence requests have not been fetched",
            "source text remains un-ingested",
            "locator and provenance fields are not resolved",
            "proof-graph edge materialization remains unauthorized",
        ],
    }


def _build_human_wisdom_counterpressure_edge_evidence_acquisition_manifest() -> dict[str, Any]:
    return {
        "status": "contested",
        "manifest": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_EVIDENCE_ACQUISITION_MANIFEST,
        "warning": (
            "This manifest records planned metadata acquisition only. "
            "No fetch, hash computation, source-text ingestion, or proof-graph write has run."
        ),
    }


def _build_human_wisdom_counterpressure_edge_evidence_acquisition_checks() -> dict[str, Any]:
    manifest = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_EVIDENCE_ACQUISITION_MANIFEST
    queue = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_EVIDENCE_REQUEST_QUEUE
    request_ids = {item["request_id"] for item in queue["evidence_requests"]}
    acquisition_request_ids = {item["request_id"] for item in manifest["acquisition_items"]}
    items_covering_fields = [
        item["acquisition_id"] for item in manifest["acquisition_items"]
        if set(item["target_fields"]) >= set(
            next(
                request["requested_evidence_fields"]
                for request in queue["evidence_requests"]
                if request["request_id"] == item["request_id"]
            )
        )
        and item["source_text_ingested"] is False
        and item["materialization_status"] == "acquisition_plan_not_evidence"
    ]
    unexecuted_item_ids = [
        item["acquisition_id"] for item in manifest["acquisition_items"]
        if item["fetch_status"] == "planned_not_executed"
        and item["hash_status"] == "not_computed"
    ]
    checks = [
        {
            "id": "check-evidence-request-queue-linked",
            "status": "complete"
            if manifest["input_evidence_request_queue_id"] == queue["id"]
            else "open",
            "artifact": "human-wisdom-counterpressure-edge-evidence-request-queue.json",
            "input_evidence_request_queue_id": manifest["input_evidence_request_queue_id"],
        },
        {
            "id": "check-every-request-has-acquisition-item",
            "status": "complete" if request_ids <= acquisition_request_ids else "open",
            "request_ids": sorted(request_ids),
            "acquisition_request_ids": sorted(acquisition_request_ids),
            "missing_request_ids": sorted(request_ids - acquisition_request_ids),
        },
        {
            "id": "check-acquisition-items-cover-requested-fields",
            "status": "complete" if len(items_covering_fields) == len(manifest["acquisition_items"]) else "open",
            "acquisition_ids": items_covering_fields,
        },
        {
            "id": "check-fetch-and-hash-still-unexecuted",
            "status": "contested" if len(unexecuted_item_ids) == len(manifest["acquisition_items"]) else "open",
            "unexecuted_item_ids": unexecuted_item_ids,
            "authorization_state": manifest["authorization_state"],
        },
        {
            "id": "check-acquisition-manifest-not-promoted",
            "status": "contested" if manifest["verdict"] == "contested" else "open",
            "verdict": manifest["verdict"],
            "decision_rule": manifest["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_concept_id": manifest["target_concept_id"],
        "scope": "planned_metadata_acquisition_not_fetched_evidence",
        "checks": checks,
        "remaining_risks": [
            "metadata fetch has not run",
            "metadata hashes are not computed",
            "source text remains un-ingested",
            "proof-graph edge materialization remains unauthorized",
        ],
    }


def _build_human_wisdom_counterpressure_edge_metadata_receipt_schema() -> dict[str, Any]:
    return {
        "status": "contested",
        "schema": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_SCHEMA,
        "warning": (
            "This schema records metadata receipt templates only. "
            "No receipt, metadata hash, source text, or proof-graph edge has been materialized."
        ),
    }


def _build_human_wisdom_counterpressure_edge_metadata_receipt_checks() -> dict[str, Any]:
    schema = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_SCHEMA
    manifest = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_EVIDENCE_ACQUISITION_MANIFEST
    acquisition_ids = {item["acquisition_id"] for item in manifest["acquisition_items"]}
    receipt_acquisition_ids = {item["acquisition_id"] for item in schema["receipt_templates"]}
    required_fields = set(schema["receipt_schema"]["required_fields"])
    templates_not_materialized = [
        item["receipt_id"] for item in schema["receipt_templates"]
        if item["receipt_status"] == "template_not_materialized"
        and item["metadata_hash"] is None
        and item["source_text_ingested"] is False
        and item["materialization_status"] == "receipt_schema_not_evidence"
    ]
    checks = [
        {
            "id": "check-acquisition-manifest-linked",
            "status": "complete"
            if schema["input_acquisition_manifest_id"] == manifest["id"]
            else "open",
            "artifact": "human-wisdom-counterpressure-edge-evidence-acquisition-manifest.json",
            "input_acquisition_manifest_id": schema["input_acquisition_manifest_id"],
        },
        {
            "id": "check-every-acquisition-item-has-receipt-template",
            "status": "complete" if acquisition_ids <= receipt_acquisition_ids else "open",
            "acquisition_ids": sorted(acquisition_ids),
            "receipt_acquisition_ids": sorted(receipt_acquisition_ids),
            "missing_acquisition_ids": sorted(acquisition_ids - receipt_acquisition_ids),
        },
        {
            "id": "check-receipt-schema-requires-locator-provenance-hash",
            "status": "complete"
            if {"passage_locator", "translation_provenance", "metadata_hash", "license_or_use_basis"}
            <= required_fields
            and schema["receipt_schema"]["raw_text_storage_allowed"] is False
            else "open",
            "required_fields": schema["receipt_schema"]["required_fields"],
        },
        {
            "id": "check-receipts-still-unmaterialized",
            "status": "contested"
            if len(templates_not_materialized) == len(schema["receipt_templates"])
            else "open",
            "receipt_ids": templates_not_materialized,
            "authorization_state": schema["authorization_state"],
        },
        {
            "id": "check-receipt-schema-not-promoted",
            "status": "contested" if schema["verdict"] == "contested" else "open",
            "verdict": schema["verdict"],
            "decision_rule": schema["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_concept_id": schema["target_concept_id"],
        "scope": "metadata_receipt_templates_not_materialized_evidence",
        "checks": checks,
        "remaining_risks": [
            "metadata receipts are not materialized",
            "metadata hashes are not computed",
            "source text remains un-ingested",
            "proof-graph edge materialization remains unauthorized",
        ],
    }


def _build_human_wisdom_counterpressure_edge_metadata_receipt_review_queue() -> dict[str, Any]:
    return {
        "status": "contested",
        "queue": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_REVIEW_QUEUE,
        "warning": (
            "This queue records pending review work only. "
            "No receipt has been reviewed, approved, or materialized into the proof graph."
        ),
    }


def _build_human_wisdom_counterpressure_edge_metadata_receipt_review_checks() -> dict[str, Any]:
    queue = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_REVIEW_QUEUE
    schema = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_SCHEMA
    schema_receipt_ids = {item["receipt_id"] for item in schema["receipt_templates"]}
    review_receipt_ids = {item["receipt_id"] for item in queue["review_items"]}
    required_review_fields = {
        "passage_locator",
        "translation_provenance",
        "license_or_use_basis",
        "metadata_hash",
        "reviewer_identity_or_process",
    }
    items_with_required_fields = [
        item["review_item_id"] for item in queue["review_items"]
        if required_review_fields <= set(item["required_review_fields"])
    ]
    queued_unperformed_items = [
        item["review_item_id"] for item in queue["review_items"]
        if item["review_status"] == "queued_not_reviewed"
        and item["approval_status"] == "not_approved"
        and item["receipt_status"] == "template_not_materialized"
        and item["metadata_hash"] is None
        and item["materialization_status"] == "review_queue_not_evidence"
    ]
    checks = [
        {
            "id": "check-receipt-schema-linked",
            "status": "complete"
            if queue["input_metadata_receipt_schema_id"] == schema["id"]
            else "open",
            "artifact": "human-wisdom-counterpressure-edge-metadata-receipt-schema.json",
            "input_metadata_receipt_schema_id": queue["input_metadata_receipt_schema_id"],
        },
        {
            "id": "check-every-receipt-template-has-review-item",
            "status": "complete" if schema_receipt_ids <= review_receipt_ids else "open",
            "schema_receipt_ids": sorted(schema_receipt_ids),
            "review_receipt_ids": sorted(review_receipt_ids),
            "missing_receipt_ids": sorted(schema_receipt_ids - review_receipt_ids),
        },
        {
            "id": "check-review-items-require-hash-and-provenance",
            "status": "complete" if len(items_with_required_fields) == len(queue["review_items"]) else "open",
            "review_item_ids": items_with_required_fields,
            "required_review_fields": sorted(required_review_fields),
        },
        {
            "id": "check-receipt-review-still-unperformed",
            "status": "contested" if len(queued_unperformed_items) == len(queue["review_items"]) else "open",
            "review_item_ids": queued_unperformed_items,
            "authorization_state": queue["authorization_state"],
        },
        {
            "id": "check-receipt-review-queue-not-promoted",
            "status": "contested" if queue["verdict"] == "contested" else "open",
            "verdict": queue["verdict"],
            "decision_rule": queue["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_concept_id": queue["target_concept_id"],
        "scope": "metadata_receipt_review_queue_not_performed",
        "checks": checks,
        "remaining_risks": [
            "metadata receipts are still templates",
            "receipt reviews are not performed",
            "receipt approvals are not recorded",
            "proof-graph edge materialization remains unauthorized",
        ],
    }


def _build_human_wisdom_counterpressure_edge_metadata_receipt_review_rubric() -> dict[str, Any]:
    return {
        "status": "contested",
        "rubric": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_REVIEW_RUBRIC,
        "warning": (
            "This rubric records a programmable metadata receipt review schema only. "
            "It is not an applied review, approval, or proof-graph authorization."
        ),
    }


def _build_human_wisdom_counterpressure_edge_metadata_receipt_review_rubric_checks() -> dict[str, Any]:
    rubric = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_REVIEW_RUBRIC
    queue = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_REVIEW_QUEUE
    required_fields = {
        field
        for item in queue["review_items"]
        for field in item["required_review_fields"]
    }
    covered_fields = set(rubric["field_axis_map"])
    decision_schema = rubric["decision_schema"]
    materialization_gate = rubric["materialization_gate"]
    checks = [
        {
            "id": "check-receipt-review-queue-linked",
            "status": "complete"
            if rubric["input_receipt_review_queue_id"] == queue["id"]
            else "open",
            "artifact": "human-wisdom-counterpressure-edge-metadata-receipt-review-queue.json",
            "input_receipt_review_queue_id": rubric["input_receipt_review_queue_id"],
        },
        {
            "id": "check-required-review-fields-covered",
            "status": "complete" if required_fields <= covered_fields else "open",
            "required_fields": sorted(required_fields),
            "covered_fields": sorted(covered_fields),
            "missing_fields": sorted(required_fields - covered_fields),
            "covered_review_axes": rubric["covered_review_axes"],
        },
        {
            "id": "check-receipt-decision-schema-recorded",
            "status": "complete"
            if {"approve", "reject", "defer", "request_metadata_refetch"}
            <= set(decision_schema["allowed_decisions"])
            and {"decision", "receipt_id", "reviewer_rationale"} <= set(decision_schema["required_fields"])
            else "open",
            "decision_schema": decision_schema,
        },
        {
            "id": "check-receipt-rubric-application-still-open",
            "status": "contested"
            if rubric["authorization_state"]["review_items_completed"] is False
            and rubric["authorization_state"]["receipt_approvals_recorded"] is False
            and rubric["authorization_state"]["materialization_authorized"] is False
            and materialization_gate["requires_materialized_receipt"] is True
            and materialization_gate["requires_metadata_hash"] is True
            else "complete",
            "authorization_state": rubric["authorization_state"],
            "materialization_gate": materialization_gate,
        },
        {
            "id": "check-receipt-rubric-not-promoted",
            "status": "contested" if rubric["verdict"] == "contested" else "open",
            "verdict": rubric["verdict"],
            "decision_rule": rubric["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_concept_id": rubric["target_concept_id"],
        "scope": "metadata_receipt_review_rubric_not_applied_review",
        "checks": checks,
        "remaining_risks": [
            "rubric has not been applied to receipt review items",
            "receipt approvals are not recorded",
            "metadata hashes are still absent from receipt templates",
            "proof-graph edge materialization remains unauthorized",
        ],
    }


def _build_human_wisdom_counterpressure_edge_metadata_receipt_review_decisions() -> dict[str, Any]:
    return {
        "status": "contested",
        "decisions": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_REVIEW_DECISIONS,
        "warning": (
            "These are defer-only metadata receipt review decisions. "
            "They do not approve receipts or authorize proof-graph materialization."
        ),
    }


def _build_human_wisdom_counterpressure_edge_metadata_receipt_review_decision_checks() -> dict[str, Any]:
    decisions = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_REVIEW_DECISIONS
    queue = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_REVIEW_QUEUE
    rubric = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_REVIEW_RUBRIC
    review_item_ids = {item["review_item_id"] for item in queue["review_items"]}
    decision_review_item_ids = {item["review_item_id"] for item in decisions["decision_records"]}
    deferred_decision_ids = [
        item["decision_id"] for item in decisions["decision_records"]
        if item["decision"] == "defer"
        and item["approval_status"] == "not_approved"
        and item["metadata_hash"] is None
        and item["materialization_status"] == "deferred_receipt_not_evidence"
        and item["source_text_ingested"] is False
    ]
    approved_or_materialized_decision_ids = [
        item["decision_id"] for item in decisions["decision_records"]
        if item["decision"] in rubric["decision_schema"]["approval_decisions"]
        or item["approval_status"] != "not_approved"
        or item["materialization_status"] != "deferred_receipt_not_evidence"
    ]
    checks = [
        {
            "id": "check-receipt-review-rubric-linked",
            "status": "complete"
            if decisions["input_receipt_review_rubric_id"] == rubric["id"]
            else "open",
            "artifact": "human-wisdom-counterpressure-edge-metadata-receipt-review-rubric.json",
            "input_receipt_review_rubric_id": decisions["input_receipt_review_rubric_id"],
        },
        {
            "id": "check-receipt-review-queue-linked",
            "status": "complete"
            if decisions["input_receipt_review_queue_id"] == queue["id"]
            else "open",
            "artifact": "human-wisdom-counterpressure-edge-metadata-receipt-review-queue.json",
            "input_receipt_review_queue_id": decisions["input_receipt_review_queue_id"],
        },
        {
            "id": "check-every-receipt-review-item-has-defer-decision",
            "status": "complete"
            if review_item_ids <= decision_review_item_ids
            and len(deferred_decision_ids) == len(decisions["decision_records"])
            else "open",
            "review_item_ids": sorted(review_item_ids),
            "decision_review_item_ids": sorted(decision_review_item_ids),
            "missing_review_item_ids": sorted(review_item_ids - decision_review_item_ids),
            "deferred_decision_ids": deferred_decision_ids,
        },
        {
            "id": "check-no-receipt-approval-or-proof-materialization",
            "status": "complete"
            if not approved_or_materialized_decision_ids
            and decisions["authorization_state"]["approved_receipts"] == 0
            and decisions["authorization_state"]["receipt_approvals_recorded"] is False
            and decisions["authorization_state"]["materialization_authorized"] is False
            else "open",
            "approved_or_materialized_decision_ids": approved_or_materialized_decision_ids,
            "authorization_state": decisions["authorization_state"],
        },
        {
            "id": "check-receipt-decision-ledger-still-contested",
            "status": "contested" if decisions["verdict"] == "contested" else "open",
            "verdict": decisions["verdict"],
            "decision_rule": decisions["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_concept_id": decisions["target_concept_id"],
        "scope": "defer_only_receipt_review_decisions_not_evidence",
        "checks": checks,
        "remaining_risks": [
            "metadata receipts are not materialized",
            "metadata hashes are not recorded",
            "receipt approvals are not recorded",
            "proof-graph edge materialization remains unauthorized",
        ],
    }


def _build_human_wisdom_counterpressure_edge_metadata_receipt_resolution_packet() -> dict[str, Any]:
    return {
        "status": "contested",
        "packet": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_RESOLUTION_PACKET,
        "warning": (
            "This packet records metadata receipt resolution tasks only. "
            "It does not materialize receipts, hashes, source text, or proof-graph edges."
        ),
    }


def _build_human_wisdom_counterpressure_edge_metadata_receipt_resolution_checks() -> dict[str, Any]:
    packet = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_RESOLUTION_PACKET
    decisions = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_REVIEW_DECISIONS
    deferred_decision_ids = {
        item["decision_id"] for item in decisions["decision_records"]
        if item["decision"] == "defer"
    }
    task_decision_ids = {item["decision_id"] for item in packet["resolution_tasks"]}
    required_fields = {"passage_locator", "translation_provenance", "license_or_use_basis", "metadata_hash"}
    tasks_with_required_fields = [
        item["task_id"] for item in packet["resolution_tasks"]
        if required_fields <= set(item["required_resolution_fields"])
    ]
    open_unmaterialized_tasks = [
        item["task_id"] for item in packet["resolution_tasks"]
        if item["task_status"] == "open"
        and item["metadata_hash"] is None
        and item["source_text_ingested"] is False
        and item["materialization_status"] == "resolution_task_not_receipt_evidence"
    ]
    checks = [
        {
            "id": "check-receipt-decision-ledger-linked",
            "status": "complete"
            if packet["input_receipt_review_decisions_id"] == decisions["id"]
            else "open",
            "artifact": "human-wisdom-counterpressure-edge-metadata-receipt-review-decisions.json",
            "input_receipt_review_decisions_id": packet["input_receipt_review_decisions_id"],
        },
        {
            "id": "check-every-deferred-receipt-decision-has-resolution-task",
            "status": "complete" if deferred_decision_ids <= task_decision_ids else "open",
            "deferred_decision_ids": sorted(deferred_decision_ids),
            "task_decision_ids": sorted(task_decision_ids),
            "missing_decision_ids": sorted(deferred_decision_ids - task_decision_ids),
        },
        {
            "id": "check-receipt-resolution-fields-required",
            "status": "complete" if len(tasks_with_required_fields) == len(packet["resolution_tasks"]) else "open",
            "task_ids": tasks_with_required_fields,
            "required_fields": sorted(required_fields),
        },
        {
            "id": "check-receipt-resolution-tasks-still-open",
            "status": "contested"
            if len(open_unmaterialized_tasks) == len(packet["resolution_tasks"])
            and packet["authorization_state"]["all_resolution_tasks_complete"] is False
            and packet["authorization_state"]["metadata_hashes_recorded"] is False
            else "open",
            "task_ids": open_unmaterialized_tasks,
            "authorization_state": packet["authorization_state"],
        },
        {
            "id": "check-receipt-resolution-packet-not-promoted",
            "status": "contested" if packet["verdict"] == "contested" else "open",
            "verdict": packet["verdict"],
            "decision_rule": packet["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_concept_id": packet["target_concept_id"],
        "scope": "metadata_receipt_resolution_tasks_not_evidence",
        "checks": checks,
        "remaining_risks": [
            "metadata receipt resolution tasks remain open",
            "metadata hashes are not recorded",
            "receipt approvals are not recorded",
            "proof-graph edge materialization remains unauthorized",
        ],
    }


def _build_human_wisdom_counterpressure_edge_metadata_receipt_evidence_request_queue() -> dict[str, Any]:
    return {
        "status": "contested",
        "queue": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_EVIDENCE_REQUEST_QUEUE,
        "warning": (
            "This queue records planned receipt metadata requests only. "
            "No metadata fetch, hash recording, source text ingestion, or proof-graph write has run."
        ),
    }


def _build_human_wisdom_counterpressure_edge_metadata_receipt_evidence_request_checks() -> dict[str, Any]:
    queue = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_EVIDENCE_REQUEST_QUEUE
    packet = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_RESOLUTION_PACKET
    open_task_ids = {
        item["task_id"] for item in packet["resolution_tasks"]
        if item["task_status"] == "open"
    }
    request_task_ids = {item["task_id"] for item in queue["evidence_requests"]}
    required_fields = {"passage_locator", "translation_provenance", "license_or_use_basis", "metadata_hash"}
    requests_with_required_fields = [
        item["request_id"] for item in queue["evidence_requests"]
        if required_fields <= set(item["requested_evidence_fields"])
    ]
    queued_unfetched_requests = [
        item["request_id"] for item in queue["evidence_requests"]
        if item["request_status"] == "queued_not_fetched"
        and item["metadata_hash"] is None
        and item["source_text_ingested"] is False
        and item["materialization_status"] == "receipt_request_not_evidence"
    ]
    checks = [
        {
            "id": "check-receipt-resolution-packet-linked",
            "status": "complete"
            if queue["input_receipt_resolution_packet_id"] == packet["id"]
            else "open",
            "artifact": "human-wisdom-counterpressure-edge-metadata-receipt-resolution-packet.json",
            "input_receipt_resolution_packet_id": queue["input_receipt_resolution_packet_id"],
        },
        {
            "id": "check-every-open-receipt-resolution-task-has-evidence-request",
            "status": "complete" if open_task_ids <= request_task_ids else "open",
            "open_task_ids": sorted(open_task_ids),
            "request_task_ids": sorted(request_task_ids),
            "missing_task_ids": sorted(open_task_ids - request_task_ids),
        },
        {
            "id": "check-receipt-request-fields-cover-locator-provenance-license-hash",
            "status": "complete"
            if len(requests_with_required_fields) == len(queue["evidence_requests"])
            else "open",
            "request_ids": requests_with_required_fields,
            "required_fields": sorted(required_fields),
        },
        {
            "id": "check-receipt-evidence-requests-not-fetched",
            "status": "contested"
            if len(queued_unfetched_requests) == len(queue["evidence_requests"])
            and queue["authorization_state"]["evidence_fetched"] is False
            and queue["authorization_state"]["metadata_hashes_recorded"] is False
            else "open",
            "request_ids": queued_unfetched_requests,
            "authorization_state": queue["authorization_state"],
        },
        {
            "id": "check-receipt-evidence-request-queue-not-promoted",
            "status": "contested" if queue["verdict"] == "contested" else "open",
            "verdict": queue["verdict"],
            "decision_rule": queue["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_concept_id": queue["target_concept_id"],
        "scope": "metadata_receipt_evidence_requests_not_fetched",
        "checks": checks,
        "remaining_risks": [
            "receipt metadata requests are not fetched",
            "metadata hashes are not recorded",
            "receipt approvals are not recorded",
            "proof-graph edge materialization remains unauthorized",
        ],
    }


def _build_human_wisdom_counterpressure_edge_metadata_receipt_acquisition_manifest() -> dict[str, Any]:
    return {
        "status": "contested",
        "manifest": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_ACQUISITION_MANIFEST,
        "warning": (
            "This manifest records planned receipt metadata acquisition only. "
            "No fetch, hash computation, receipt materialization, source-text ingestion, or proof-graph write has run."
        ),
    }


def _build_human_wisdom_counterpressure_edge_metadata_receipt_acquisition_checks() -> dict[str, Any]:
    manifest = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_ACQUISITION_MANIFEST
    queue = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_EVIDENCE_REQUEST_QUEUE
    request_ids = {item["request_id"] for item in queue["evidence_requests"]}
    acquisition_request_ids = {item["request_id"] for item in manifest["acquisition_items"]}
    items_covering_fields = [
        item["acquisition_id"] for item in manifest["acquisition_items"]
        if set(item["target_fields"]) >= set(
            next(
                request["requested_evidence_fields"]
                for request in queue["evidence_requests"]
                if request["request_id"] == item["request_id"]
            )
        )
        and item["metadata_hash"] is None
        and item["source_text_ingested"] is False
        and item["materialization_status"] == "receipt_acquisition_plan_not_evidence"
    ]
    unexecuted_item_ids = [
        item["acquisition_id"] for item in manifest["acquisition_items"]
        if item["fetch_status"] == "planned_not_executed"
        and item["hash_status"] == "not_computed"
        and item["metadata_hash"] is None
    ]
    checks = [
        {
            "id": "check-receipt-evidence-request-queue-linked",
            "status": "complete"
            if manifest["input_receipt_evidence_request_queue_id"] == queue["id"]
            else "open",
            "artifact": "human-wisdom-counterpressure-edge-metadata-receipt-evidence-request-queue.json",
            "input_receipt_evidence_request_queue_id": manifest["input_receipt_evidence_request_queue_id"],
        },
        {
            "id": "check-every-receipt-request-has-acquisition-item",
            "status": "complete" if request_ids <= acquisition_request_ids else "open",
            "request_ids": sorted(request_ids),
            "acquisition_request_ids": sorted(acquisition_request_ids),
            "missing_request_ids": sorted(request_ids - acquisition_request_ids),
        },
        {
            "id": "check-receipt-acquisition-items-cover-requested-fields",
            "status": "complete" if len(items_covering_fields) == len(manifest["acquisition_items"]) else "open",
            "acquisition_ids": items_covering_fields,
        },
        {
            "id": "check-receipt-fetch-and-hash-still-unexecuted",
            "status": "contested"
            if len(unexecuted_item_ids) == len(manifest["acquisition_items"])
            and manifest["authorization_state"]["fetch_executed"] is False
            and manifest["authorization_state"]["metadata_hashes_computed"] is False
            else "open",
            "unexecuted_item_ids": unexecuted_item_ids,
            "authorization_state": manifest["authorization_state"],
        },
        {
            "id": "check-receipt-acquisition-manifest-not-promoted",
            "status": "contested" if manifest["verdict"] == "contested" else "open",
            "verdict": manifest["verdict"],
            "decision_rule": manifest["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_concept_id": manifest["target_concept_id"],
        "scope": "planned_receipt_metadata_acquisition_not_fetched_evidence",
        "checks": checks,
        "remaining_risks": [
            "receipt metadata fetch has not run",
            "metadata hashes are not computed",
            "metadata receipts are not materialized",
            "proof-graph edge materialization remains unauthorized",
        ],
    }


def _build_human_wisdom_counterpressure_edge_metadata_receipt_acquisition_hash_runbook() -> dict[str, Any]:
    return {
        "status": "contested",
        "runbook": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_ACQUISITION_HASH_RUNBOOK,
        "warning": (
            "This runbook records receipt metadata acquisition and hash command templates only. "
            "No command, fetch, hash manifest write, or proof-graph write has run."
        ),
    }


def _build_human_wisdom_counterpressure_edge_metadata_receipt_acquisition_hash_runbook_checks() -> dict[str, Any]:
    runbook = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_ACQUISITION_HASH_RUNBOOK
    manifest = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_ACQUISITION_MANIFEST
    manifest_acquisition_ids = {item["acquisition_id"] for item in manifest["acquisition_items"]}
    runbook_acquisition_ids = {step["acquisition_id"] for step in runbook["steps"]}
    steps_with_hash_commands = [
        step["acquisition_id"] for step in runbook["steps"]
        if "shasum -a 256" in step["hash_command_template"]
        and step["execution_status"] == "not_executed"
    ]
    steps_with_required_logs = [
        step["acquisition_id"] for step in runbook["steps"]
        if set(step["required_log_events"]) >= {
            "receipt_metadata_authorization_recorded",
            "receipt_metadata_file_acquired",
            "receipt_metadata_hash_recorded",
            "receipt_metadata_cache_pruned_or_retained_with_reason",
        }
    ]
    open_execution_requirement_ids = [
        requirement["id"] for requirement in runbook["execution_requirements"]
        if requirement["status"] == "open"
    ]
    checks = [
        {
            "id": "check-receipt-acquisition-manifest-linked",
            "status": "complete"
            if runbook["input_receipt_acquisition_manifest_id"] == manifest["id"]
            else "open",
            "artifact": "human-wisdom-counterpressure-edge-metadata-receipt-acquisition-manifest.json",
            "input_receipt_acquisition_manifest_id": runbook["input_receipt_acquisition_manifest_id"],
        },
        {
            "id": "check-every-receipt-acquisition-item-has-runbook-step",
            "status": "complete" if manifest_acquisition_ids <= runbook_acquisition_ids else "open",
            "manifest_acquisition_ids": sorted(manifest_acquisition_ids),
            "runbook_acquisition_ids": sorted(runbook_acquisition_ids),
            "missing_acquisition_ids": sorted(manifest_acquisition_ids - runbook_acquisition_ids),
        },
        {
            "id": "check-receipt-hash-manifest-schema-recorded",
            "status": "complete"
            if runbook["hash_manifest_schema"]["hash_algorithm"] == "sha256"
            and "sha256" in runbook["hash_manifest_schema"]["required_fields"]
            else "open",
            "artifact_name": runbook["hash_manifest_schema"]["artifact_name"],
            "required_fields": runbook["hash_manifest_schema"]["required_fields"],
        },
        {
            "id": "check-receipt-hash-command-templates-recorded-not-executed",
            "status": "complete" if len(steps_with_hash_commands) == len(runbook["steps"]) else "open",
            "acquisition_ids": steps_with_hash_commands,
            "result": "hash commands are templates only; every step remains not_executed",
        },
        {
            "id": "check-receipt-required-log-events-recorded",
            "status": "complete" if len(steps_with_required_logs) == len(runbook["steps"]) else "open",
            "acquisition_ids": steps_with_required_logs,
        },
        {
            "id": "check-receipt-cache-retention-and-prune-step-recorded",
            "status": "complete"
            if runbook["cache_policy"]["retention_rule"]
            and runbook["cache_policy"]["prune_step_template"]
            and runbook["cache_policy"]["repo_storage_allowed"] is False
            else "open",
            "cache_policy": runbook["cache_policy"],
        },
        {
            "id": "check-receipt-acquisition-still-open",
            "status": "contested" if open_execution_requirement_ids else "complete",
            "open_execution_requirement_ids": open_execution_requirement_ids,
            "authorization_state": runbook["authorization_state"],
        },
        {
            "id": "check-receipt-acquisition-runbook-not-promoted",
            "status": "contested" if runbook["verdict"] == "contested" else "open",
            "verdict": runbook["verdict"],
            "decision_rule": runbook["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_concept_id": runbook["target_concept_id"],
        "scope": "receipt_metadata_acquisition_hash_runbook_not_executed",
        "checks": checks,
        "remaining_risks": [
            "receipt metadata authorization is not recorded",
            "metadata files are not acquired",
            "receipt metadata hash manifest is not materialized",
            "metadata cache retention is only a candidate policy",
        ],
    }


def _build_human_wisdom_counterpressure_edge_metadata_receipt_authorization_packet() -> dict[str, Any]:
    return {
        "status": "contested",
        "packet": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_AUTHORIZATION_PACKET,
        "warning": (
            "This packet records candidate receipt metadata authorization blockers only. "
            "It does not authorize fetch, hash commands, receipt materialization, or proof-graph writes."
        ),
    }


def _build_human_wisdom_counterpressure_edge_metadata_receipt_authorization_checks() -> dict[str, Any]:
    packet = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_AUTHORIZATION_PACKET
    runbook = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_ACQUISITION_HASH_RUNBOOK
    runbook_acquisition_ids = {step["acquisition_id"] for step in runbook["steps"]}
    authorization_acquisition_ids = {
        record["acquisition_id"] for record in packet["authorization_records"]
    }
    required_action_record_ids = [
        record["authorization_id"] for record in packet["authorization_records"]
        if set(record["required_actions"]) >= {
            "confirm metadata source locator",
            "confirm license or use basis",
            "confirm no raw source text will be retained",
            "confirm hash manifest target path outside shared repo",
            "confirm cache retention and prune step",
        }
    ]
    non_authorized_record_ids = [
        record["authorization_id"] for record in packet["authorization_records"]
        if record["authorization_decision"].startswith("not_authorized_until_")
        and record["fetch_allowed"] is False
        and record["hash_command_allowed"] is False
        and record["receipt_materialization_allowed"] is False
        and record["source_text_ingested"] is False
    ]
    checks = [
        {
            "id": "check-receipt-hash-runbook-linked",
            "status": "complete"
            if packet["input_receipt_hash_runbook_id"] == runbook["id"]
            else "open",
            "artifact": "human-wisdom-counterpressure-edge-metadata-receipt-acquisition-hash-runbook.json",
            "input_receipt_hash_runbook_id": packet["input_receipt_hash_runbook_id"],
        },
        {
            "id": "check-every-runbook-step-has-authorization-record",
            "status": "complete" if runbook_acquisition_ids <= authorization_acquisition_ids else "open",
            "runbook_acquisition_ids": sorted(runbook_acquisition_ids),
            "authorization_acquisition_ids": sorted(authorization_acquisition_ids),
            "missing_acquisition_ids": sorted(runbook_acquisition_ids - authorization_acquisition_ids),
        },
        {
            "id": "check-required-authorization-actions-recorded",
            "status": "complete"
            if len(required_action_record_ids) == len(packet["authorization_records"])
            else "open",
            "authorization_ids": required_action_record_ids,
        },
        {
            "id": "check-receipt-fetch-and-hash-not-authorized",
            "status": "contested"
            if len(non_authorized_record_ids) == len(packet["authorization_records"])
            and packet["authorization_state"]["fetch_allowed"] is False
            and packet["authorization_state"]["hash_commands_allowed"] is False
            else "open",
            "authorization_ids": non_authorized_record_ids,
            "authorization_state": packet["authorization_state"],
        },
        {
            "id": "check-receipt-authorization-packet-not-promoted",
            "status": "contested" if packet["verdict"] == "contested" else "open",
            "verdict": packet["verdict"],
            "decision_rule": packet["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_concept_id": packet["target_concept_id"],
        "scope": "receipt_metadata_authorization_not_granted",
        "checks": checks,
        "remaining_risks": [
            "receipt metadata fetch remains unauthorized",
            "hash commands remain unauthorized",
            "receipt materialization remains unauthorized",
            "proof-graph edge materialization remains unauthorized",
        ],
    }


def _build_human_wisdom_counterpressure_edge_metadata_receipt_authorization_review_queue() -> dict[str, Any]:
    return {
        "status": "contested",
        "queue": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_AUTHORIZATION_REVIEW_QUEUE,
        "warning": (
            "This queue records pending authorization review work only. "
            "It does not approve fetch, hash commands, receipt materialization, or proof-graph writes."
        ),
    }


def _build_human_wisdom_counterpressure_edge_metadata_receipt_authorization_review_checks() -> dict[str, Any]:
    queue = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_AUTHORIZATION_REVIEW_QUEUE
    packet = HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_AUTHORIZATION_PACKET
    authorization_ids = {record["authorization_id"] for record in packet["authorization_records"]}
    review_authorization_ids = {item["authorization_id"] for item in queue["review_items"]}
    unreviewed_review_ids = [
        item["review_id"] for item in queue["review_items"]
        if item["review_status"] == "queued_not_reviewed"
        and item["fetch_allowed"] is False
        and item["hash_command_allowed"] is False
        and item["receipt_materialization_allowed"] is False
        and item["materialization_status"] == "authorization_review_queue_not_evidence"
    ]
    open_authorization_review_ids = [
        item["review_id"] for item in queue["review_items"]
        if item["authorization_decision"].startswith("not_authorized_until_")
        and item["manual_review_required"] is True
        and item["source_text_ingested"] is False
    ]
    checks = [
        {
            "id": "check-authorization-packet-linked",
            "status": "complete"
            if queue["input_authorization_packet_id"] == packet["id"]
            else "open",
            "artifact": "human-wisdom-counterpressure-edge-metadata-receipt-authorization-packet.json",
            "input_authorization_packet_id": queue["input_authorization_packet_id"],
        },
        {
            "id": "check-every-authorization-record-has-review-item",
            "status": "complete" if authorization_ids <= review_authorization_ids else "open",
            "authorization_ids": sorted(authorization_ids),
            "review_authorization_ids": sorted(review_authorization_ids),
            "missing_authorization_ids": sorted(authorization_ids - review_authorization_ids),
        },
        {
            "id": "check-authorization-review-items-remain-unreviewed",
            "status": "complete" if len(unreviewed_review_ids) == len(queue["review_items"]) else "open",
            "review_ids": unreviewed_review_ids,
        },
        {
            "id": "check-receipt-fetch-and-hash-authorization-still-open",
            "status": "contested"
            if len(open_authorization_review_ids) == len(queue["review_items"])
            and queue["authorization_state"]["authorization_reviews_completed"] is False
            and queue["authorization_state"]["fetch_allowed"] is False
            and queue["authorization_state"]["hash_commands_allowed"] is False
            else "open",
            "review_ids": open_authorization_review_ids,
            "authorization_state": queue["authorization_state"],
        },
        {
            "id": "check-authorization-review-queue-not-promoted",
            "status": "contested" if queue["verdict"] == "contested" else "open",
            "verdict": queue["verdict"],
            "decision_rule": queue["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_concept_id": queue["target_concept_id"],
        "scope": "receipt_metadata_authorization_review_queue_not_approved",
        "checks": checks,
        "remaining_risks": [
            "authorization reviews are not complete",
            "receipt metadata fetch remains unauthorized",
            "hash commands remain unauthorized",
            "proof-graph edge materialization remains unauthorized",
        ],
    }


def _build_human_wisdom_primary_source_summary_candidate_checks(
    human_wisdom_counterpressure_edge_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    candidates = HUMAN_WISDOM_PRIMARY_SOURCE_SUMMARY_CANDIDATES
    queue = HUMAN_WISDOM_PRIMARY_SOURCE_EXTRACTION_QUEUE
    human_wisdom_counterpressure_edge_checks = (
        human_wisdom_counterpressure_edge_checks
        or _build_human_wisdom_counterpressure_edge_checks()
    )
    queue_seed_ids = {item["seed_id"] for item in queue["queue_items"]}
    candidate_seed_ids = {item["seed_id"] for item in candidates["summary_candidates"]}
    paraphrase_candidate_ids = [
        item["candidate_id"] for item in candidates["summary_candidates"]
        if item["verbatim_words_stored"] == 0
        and item["materialization_status"] == "candidate_not_in_corpus"
        and item["counterpressure_ids"]
    ]
    open_execution_requirement_ids = [
        requirement["id"] for requirement in candidates["execution_requirements"]
        if requirement["status"] == "open"
    ]
    checks = [
        {
            "id": "check-primary-source-extraction-queue-linked",
            "status": "complete"
            if candidates["input_primary_source_extraction_queue_id"] == queue["id"]
            else "open",
            "artifact": "human-wisdom-primary-source-extraction-queue.json",
            "input_primary_source_extraction_queue_id": candidates["input_primary_source_extraction_queue_id"],
        },
        {
            "id": "check-every-queue-item-has-summary-candidate",
            "status": "complete" if queue_seed_ids <= candidate_seed_ids else "open",
            "queue_seed_ids": sorted(queue_seed_ids),
            "candidate_seed_ids": sorted(candidate_seed_ids),
            "missing_seed_ids": sorted(queue_seed_ids - candidate_seed_ids),
        },
        {
            "id": "check-paraphrase-only-summary-policy",
            "status": "complete"
            if candidates["summary_policy"]["verbatim_source_text_stored"] is False
            and candidates["summary_policy"]["candidate_summaries_are_paraphrases"] is True
            and candidates["summary_policy"]["max_verbatim_words_per_source"] == 0
            else "open",
            "summary_policy": candidates["summary_policy"],
        },
        {
            "id": "check-candidates-not-materialized-in-corpus",
            "status": "complete" if len(paraphrase_candidate_ids) == len(candidates["summary_candidates"]) else "open",
            "candidate_ids": paraphrase_candidate_ids,
        },
        {
            "id": "check-counterpressure-edge-proposals-linked",
            "status": "complete",
            "artifact": "human-wisdom-counterpressure-edge-checks.json",
            "artifact_status": human_wisdom_counterpressure_edge_checks["status"],
        },
        {
            "id": "check-summary-candidate-promotion-still-open",
            "status": "contested" if open_execution_requirement_ids else "complete",
            "open_execution_requirement_ids": open_execution_requirement_ids,
            "authorization_state": candidates["authorization_state"],
        },
        {
            "id": "check-summary-candidates-not-promoted",
            "status": "contested" if candidates["verdict"] == "contested" else "open",
            "verdict": candidates["verdict"],
            "decision_rule": candidates["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_concept_id": candidates["target_concept_id"],
        "scope": "primary_source_summary_candidates_not_corpus_entries",
        "checks": checks,
        "remaining_risks": [
            "passage-level citation locators are not materialized",
            "translation provenance is not materialized",
            "counterpressure edges are not materialized",
            "wisdom corpus extension is not materialized",
        ],
    }


def _build_human_wisdom_primary_source_extraction_checks(
    human_wisdom_primary_source_summary_candidate_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    queue = HUMAN_WISDOM_PRIMARY_SOURCE_EXTRACTION_QUEUE
    ledger = HUMAN_WISDOM_PRIMARY_SOURCE_SEED_LEDGER
    human_wisdom_primary_source_summary_candidate_checks = (
        human_wisdom_primary_source_summary_candidate_checks
        or _build_human_wisdom_primary_source_summary_candidate_checks()
    )
    seed_ids = {record["seed_id"] for record in ledger["source_family_records"]}
    queue_seed_ids = {item["seed_id"] for item in queue["queue_items"]}
    queued_with_counterpressure = [
        item["seed_id"] for item in queue["queue_items"]
        if item["counterpressure_targets"]
        and item["citation_locator_required"] is True
        and item["translation_provenance_required"] is True
        and item["ingestion_status"] == "queued_not_ingested"
    ]
    open_execution_requirement_ids = [
        requirement["id"] for requirement in queue["execution_requirements"]
        if requirement["status"] == "open"
    ]
    checks = [
        {
            "id": "check-primary-source-seed-ledger-linked",
            "status": "complete"
            if queue["input_primary_source_seed_ledger_id"] == ledger["id"]
            else "open",
            "artifact": "human-wisdom-primary-source-seed-ledger.json",
            "input_primary_source_seed_ledger_id": queue["input_primary_source_seed_ledger_id"],
        },
        {
            "id": "check-every-seed-has-extraction-queue-item",
            "status": "complete" if seed_ids <= queue_seed_ids else "open",
            "seed_ids": sorted(seed_ids),
            "queue_seed_ids": sorted(queue_seed_ids),
            "missing_seed_ids": sorted(seed_ids - queue_seed_ids),
        },
        {
            "id": "check-minimized-extraction-policy-recorded",
            "status": "complete"
            if queue["global_extraction_policy"]["prefer_paraphrase"] is True
            and queue["global_extraction_policy"]["raw_text_storage_allowed"] is False
            and queue["global_extraction_policy"]["max_verbatim_words_per_source"] <= 25
            else "open",
            "global_extraction_policy": queue["global_extraction_policy"],
        },
        {
            "id": "check-counterpressure-and-provenance-required",
            "status": "complete" if len(queued_with_counterpressure) == len(queue["queue_items"]) else "open",
            "seed_ids": queued_with_counterpressure,
        },
        {
            "id": "check-summary-candidates-linked",
            "status": "complete",
            "artifact": "human-wisdom-primary-source-summary-candidate-checks.json",
            "artifact_status": human_wisdom_primary_source_summary_candidate_checks["status"],
        },
        {
            "id": "check-primary-source-extraction-still-open",
            "status": "contested" if open_execution_requirement_ids else "complete",
            "open_execution_requirement_ids": open_execution_requirement_ids,
            "authorization_state": queue["authorization_state"],
        },
        {
            "id": "check-extraction-queue-not-promoted",
            "status": "contested" if queue["verdict"] == "contested" else "open",
            "verdict": queue["verdict"],
            "decision_rule": queue["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_concept_id": queue["target_concept_id"],
        "scope": "primary_source_minimized_extraction_queue_not_ingested",
        "checks": checks,
        "remaining_risks": [
            "minimized source summaries are not written",
            "citation locators are not materialized per summary",
            "translation provenance is not recorded per summary",
            "counterpressure links are not materialized",
        ],
    }


def _build_human_wisdom_primary_source_seed_checks(
    human_wisdom_primary_source_extraction_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ledger = HUMAN_WISDOM_PRIMARY_SOURCE_SEED_LEDGER
    human_wisdom_primary_source_extraction_checks = (
        human_wisdom_primary_source_extraction_checks
        or _build_human_wisdom_primary_source_extraction_checks()
    )
    seed_domain_ids = {
        domain
        for record in ledger["source_family_records"]
        for domain in record["target_domains"]
    }
    seed_streams = {record["tradition_or_stream"] for record in ledger["source_family_records"]}
    seeds_with_locators = [
        record["seed_id"] for record in ledger["source_family_records"]
        if record["locator_url"] and record["locator_label"]
        and record["ingestion_status"] == "locator_recorded_not_ingested"
    ]
    open_acceptance_requirement_ids = [
        requirement["id"] for requirement in ledger["acceptance_requirements"]
        if requirement["status"] == "open"
    ]
    checks = [
        {
            "id": "check-primary-source-seed-locators-recorded",
            "status": "complete" if len(seeds_with_locators) == len(ledger["source_family_records"]) else "open",
            "seed_ids": seeds_with_locators,
            "retrieved_at": ledger["retrieved_at"],
        },
        {
            "id": "check-required-domain-seed-coverage",
            "status": "complete" if set(REQUIRED_WISDOM_DOMAINS) <= seed_domain_ids else "open",
            "required_domains": REQUIRED_WISDOM_DOMAINS,
            "seed_domain_ids": sorted(seed_domain_ids),
            "missing_domain_ids": sorted(set(REQUIRED_WISDOM_DOMAINS) - seed_domain_ids),
        },
        {
            "id": "check-tradition-diversity-seeded",
            "status": "complete" if len(seed_streams) >= 8 else "open",
            "tradition_or_stream_count": len(seed_streams),
            "tradition_or_streams": sorted(seed_streams),
        },
        {
            "id": "check-primary-source-extraction-queue-linked",
            "status": "complete",
            "artifact": "human-wisdom-primary-source-extraction-checks.json",
            "artifact_status": human_wisdom_primary_source_extraction_checks["status"],
        },
        {
            "id": "check-primary-source-ingestion-still-open",
            "status": "contested" if open_acceptance_requirement_ids else "complete",
            "open_acceptance_requirement_ids": open_acceptance_requirement_ids,
            "authorization_state": ledger["authorization_state"],
        },
        {
            "id": "check-primary-source-seed-ledger-not-promoted",
            "status": "contested" if ledger["verdict"] == "contested" else "open",
            "verdict": ledger["verdict"],
            "decision_rule": ledger["decision_rule"],
        },
    ]
    return {
        "status": "contested",
        "target_concept_id": ledger["target_concept_id"],
        "scope": "primary_source_seed_locators_not_ingested",
        "checks": checks,
        "remaining_risks": [
            "primary source text is not ingested",
            "translation provenance is not recorded",
            "counterpressure links are not recorded",
            "wisdom corpus is not extended from these seeds",
        ],
    }


def _build_human_wisdom_intake_checks(
    coverage: dict[str, Any] | None = None,
    human_wisdom_primary_source_seed_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    roadmap = HUMAN_WISDOM_INTAKE_ROADMAP
    coverage = coverage or _build_coverage_matrix()
    human_wisdom_primary_source_seed_checks = (
        human_wisdom_primary_source_seed_checks
        or _build_human_wisdom_primary_source_seed_checks()
    )
    coverage_domain_ids = {domain["domain"] for domain in coverage["domains"]}
    roadmap_domain_ids = {
        domain
        for lane in roadmap["intake_lanes"]
        for domain in lane["target_domains"]
    }
    lane_ids_with_acceptance_gates = [
        lane["lane_id"] for lane in roadmap["intake_lanes"]
        if lane["evidence_types"] and lane["acceptance_gate"] and lane["status"] == "open"
    ]
    open_execution_requirement_ids = [
        requirement["id"] for requirement in roadmap["execution_requirements"]
        if requirement["status"] == "open"
    ]
    checks = [
        {
            "id": "check-current-coverage-matrix-linked",
            "status": "complete" if coverage["status"] == "covered" else "open",
            "artifact": "coverage-matrix.json",
            "coverage_status": coverage["status"],
            "coverage_score": coverage["coverage_score"],
        },
        {
            "id": "check-required-domains-covered-by-roadmap",
            "status": "complete" if set(roadmap["current_required_domains"]) <= roadmap_domain_ids else "open",
            "required_domains": roadmap["current_required_domains"],
            "roadmap_domains": sorted(roadmap_domain_ids),
            "missing_domain_ids": sorted(set(roadmap["current_required_domains"]) - roadmap_domain_ids),
        },
        {
            "id": "check-current-corpus-entry-ids-recorded",
            "status": "complete"
            if len(roadmap["current_corpus_entry_ids"]) == len(WISDOM_CORPUS)
            else "open",
            "current_corpus_entry_count": len(roadmap["current_corpus_entry_ids"]),
            "runtime_corpus_entry_count": len(WISDOM_CORPUS),
        },
        {
            "id": "check-primary-source-seed-ledger-linked",
            "status": "complete"
            if roadmap["input_primary_source_seed_ledger_id"] == HUMAN_WISDOM_PRIMARY_SOURCE_SEED_LEDGER["id"]
            else "open",
            "artifact": "human-wisdom-primary-source-seed-checks.json",
            "artifact_status": human_wisdom_primary_source_seed_checks["status"],
        },
        {
            "id": "check-intake-lanes-have-evidence-types-and-gates",
            "status": "complete" if len(lane_ids_with_acceptance_gates) == len(roadmap["intake_lanes"]) else "open",
            "lane_ids": lane_ids_with_acceptance_gates,
        },
        {
            "id": "check-entry-acceptance-schema-recorded",
            "status": "complete"
            if "counterpressure_ids" in roadmap["entry_acceptance_schema"]["required_fields"]
            and roadmap["entry_acceptance_schema"]["source_requirements"]
            else "open",
            "entry_acceptance_schema": roadmap["entry_acceptance_schema"],
        },
        {
            "id": "check-open-intake-requirements-retained",
            "status": "contested" if open_execution_requirement_ids else "complete",
            "open_execution_requirement_ids": open_execution_requirement_ids,
            "authorization_state": roadmap["authorization_state"],
        },
        {
            "id": "check-exhaustive-human-wisdom-not-claimed",
            "status": "contested"
            if roadmap["authorization_state"]["exhaustive_human_wisdom_claim_allowed"] is False
            else "open",
            "decision_rule": roadmap["decision_rule"],
            "verdict": roadmap["verdict"],
        },
    ]
    return {
        "status": "contested",
        "target_concept_id": roadmap["target_concept_id"],
        "scope": "open_ended_human_wisdom_intake_not_exhaustive_claim",
        "checks": checks,
        "coverage_domain_ids": sorted(coverage_domain_ids),
        "roadmap_domain_ids": sorted(roadmap_domain_ids),
        "remaining_risks": [
            "primary-text expansion is open",
            "multilingual source expansion is open",
            "current scholarship refresh is open",
            "counterpressure linking is open",
        ],
    }


def _effective_obligation_status(
    obligation: ProofObligation,
    coverage: dict[str, Any],
    definition_checks: dict[str, Any],
    modal_validity_checks: dict[str, Any],
    modal_consistency_checks: dict[str, Any],
    teleological_bayes_checks: dict[str, Any],
    cosmological_psr_checks: dict[str, Any],
    evil_hiddenness_checks: dict[str, Any],
    ontological_soundness_checks: dict[str, Any],
) -> str:
    if obligation.id == "obl-wisdom-coverage" and coverage["status"] == "covered":
        return "complete"
    if obligation.id == "obl-target-god-concept" and definition_checks["status"] == "complete":
        return "complete"
    if obligation.id == "obl-ontological-validity" and modal_validity_checks["status"] == "complete":
        return "complete"
    if obligation.id == "obl-ontological-consistency" and modal_consistency_checks["status"] == "complete":
        return "complete"
    if obligation.id == "obl-teleological-bayes" and teleological_bayes_checks["status"] == "complete":
        return "complete"
    if obligation.id == "obl-cosmological-psr" and cosmological_psr_checks["status"] == "complete":
        return "complete"
    if obligation.id == "obl-counter-evil-hiddenness" and evil_hiddenness_checks["status"] == "complete":
        return "complete"
    if obligation.id == "obl-ontological-soundness":
        return ontological_soundness_checks["status"]
    return obligation.status


def _obligation_dicts(
    coverage: dict[str, Any],
    definition_checks: dict[str, Any],
    modal_validity_checks: dict[str, Any],
    modal_consistency_checks: dict[str, Any],
    teleological_bayes_checks: dict[str, Any],
    cosmological_psr_checks: dict[str, Any],
    evil_hiddenness_checks: dict[str, Any],
    ontological_soundness_checks: dict[str, Any],
) -> list[dict[str, Any]]:
    obligation_rows = []
    for obligation in PROOF_OBLIGATIONS:
        row = obligation.as_dict()
        row["status"] = _effective_obligation_status(
            obligation,
            coverage,
            definition_checks,
            modal_validity_checks,
            modal_consistency_checks,
            teleological_bayes_checks,
            cosmological_psr_checks,
            evil_hiddenness_checks,
            ontological_soundness_checks,
        )
        if obligation.id == "obl-wisdom-coverage":
            row["evidence_artifact"] = "coverage-matrix.json"
        if obligation.id == "obl-target-god-concept":
            row["evidence_artifact"] = "definition-checks.json"
        if obligation.id == "obl-ontological-validity":
            row["evidence_artifact"] = "modal-validity-checks.json"
        if obligation.id == "obl-ontological-consistency":
            row["evidence_artifact"] = "modal-consistency-checks.json"
        if obligation.id == "obl-teleological-bayes":
            row["evidence_artifact"] = "teleological-bayes-checks.json"
        if obligation.id == "obl-cosmological-psr":
            row["evidence_artifact"] = "cosmological-psr-checks.json"
        if obligation.id == "obl-counter-evil-hiddenness":
            row["evidence_artifact"] = "evil-hiddenness-checks.json"
        if obligation.id == "obl-ontological-soundness":
            row["evidence_artifact"] = "ontological-soundness-checks.json"
        obligation_rows.append(row)
    return obligation_rows


def _build_proof_readiness(
    coverage: dict[str, Any] | None = None,
    definition_checks: dict[str, Any] | None = None,
    modal_validity_checks: dict[str, Any] | None = None,
    modal_consistency_checks: dict[str, Any] | None = None,
    teleological_bayes_checks: dict[str, Any] | None = None,
    cosmological_psr_checks: dict[str, Any] | None = None,
    evil_hiddenness_checks: dict[str, Any] | None = None,
    ontological_soundness_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    coverage = coverage or _build_coverage_matrix()
    definition_checks = definition_checks or _build_definition_checks()
    modal_validity_checks = modal_validity_checks or _build_modal_validity_checks()
    modal_consistency_checks = modal_consistency_checks or _build_modal_consistency_checks()
    teleological_bayes_checks = teleological_bayes_checks or _build_teleological_bayes_checks()
    cosmological_psr_checks = cosmological_psr_checks or _build_cosmological_psr_checks()
    evil_hiddenness_checks = evil_hiddenness_checks or _build_evil_hiddenness_checks()
    ontological_soundness_checks = ontological_soundness_checks or _build_ontological_soundness_checks()
    blocking_open = [
        obligation.id
        for obligation in PROOF_OBLIGATIONS
        if obligation.blocks_proof_claim
        and _effective_obligation_status(
            obligation,
            coverage,
            definition_checks,
            modal_validity_checks,
            modal_consistency_checks,
            teleological_bayes_checks,
            cosmological_psr_checks,
            evil_hiddenness_checks,
            ontological_soundness_checks,
        ) != "complete"
    ]
    nonblocking_open = [
        obligation.id
        for obligation in PROOF_OBLIGATIONS
        if not obligation.blocks_proof_claim
        and _effective_obligation_status(
            obligation,
            coverage,
            definition_checks,
            modal_validity_checks,
            modal_consistency_checks,
            teleological_bayes_checks,
            cosmological_psr_checks,
            evil_hiddenness_checks,
            ontological_soundness_checks,
        ) != "complete"
    ]
    return {
        "proof_claim_allowed": not blocking_open,
        "blocking_open_obligation_ids": blocking_open,
        "nonblocking_open_obligation_ids": nonblocking_open,
        "cosmological_psr_status": cosmological_psr_checks["status"],
        "evil_hiddenness_constraint_status": evil_hiddenness_checks["status"],
        "ontological_soundness_status": ontological_soundness_checks["status"],
        "ontological_consistency_status": modal_consistency_checks["status"],
        "ontological_validity_status": modal_validity_checks["status"],
        "teleological_bayes_status": teleological_bayes_checks["status"],
        "target_definition_status": definition_checks["status"],
        "wisdom_coverage_status": coverage["status"],
        "wisdom_coverage_score": coverage["coverage_score"],
        "readiness_rule": "A proof may be claimed only when every blocking proof obligation is complete and linked to evidence.",
    }


def _build_frontier(
    coverage: dict[str, Any] | None = None,
    definition_checks: dict[str, Any] | None = None,
    modal_validity_checks: dict[str, Any] | None = None,
    modal_consistency_checks: dict[str, Any] | None = None,
    teleological_bayes_checks: dict[str, Any] | None = None,
    cosmological_psr_checks: dict[str, Any] | None = None,
    evil_hiddenness_checks: dict[str, Any] | None = None,
    ontological_soundness_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    counter_index = _counter_index()
    scores = [_argument_score(argument, counter_index) for argument in ARGUMENTS]
    best = max(scores, key=lambda item: item["proof_proximity"])
    readiness = _build_proof_readiness(
        coverage,
        definition_checks,
        modal_validity_checks,
        modal_consistency_checks,
        teleological_bayes_checks,
        cosmological_psr_checks,
        evil_hiddenness_checks,
        ontological_soundness_checks,
    )
    remaining_gate_labels = {
        "obl-wisdom-coverage": "cover every required human-wisdom domain",
        "obl-target-god-concept": "define the target God concept precisely enough for formalization",
        "obl-ontological-validity": "machine-check the modal ontological validity theorem",
        "obl-ontological-consistency": "run consistency and modal-collapse checks",
        "obl-ontological-soundness": "justify the metaphysical possibility premise",
        "obl-cosmological-psr": "settle or replace the strong PSR premise",
        "obl-teleological-bayes": "declare and test fine-tuning Bayesian assumptions",
        "obl-counter-evil-hiddenness": "satisfy evil and hiddenness constraints",
    }
    return {
        "proof_claimed": readiness["proof_claim_allowed"],
        "reason": (
            "No argument family currently clears both validity and soundness gates. "
            "The system therefore records a proof frontier instead of a proof."
        ),
        "best_current_path": best,
        "argument_scores": scores,
        "proof_readiness": readiness,
        "global_missing_gates": [
            remaining_gate_labels[gate_id]
            for gate_id in readiness["blocking_open_obligation_ids"]
            if gate_id in remaining_gate_labels
        ],
    }


def _write_formal_skeleton(session_dir: Path) -> Path:
    out_dir = session_dir / "proof-assistant-skeletons"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / "GodProof_Obligations.thy"
    out.write_text(
        r"""theory GodProof_Obligations
  imports Main
begin

text \<open>
  Generated proof-obligation scaffold.
  This is not a verified proof of God. It records the next formal target:
  encode the modal ontological argument, then separately prove or reject
  the metaphysical soundness premises.
\<close>

typedecl i
typedecl w
type_synonym sigma = "i => w => bool"

consts accessible :: "w => w => bool"
consts positive :: "sigma => bool"

definition Godlike :: "i => w => bool" where
  "Godlike x world \<equiv> (\<forall>P. positive P \<longrightarrow> P x world)"

definition PossiblyGodlike :: bool where
  "PossiblyGodlike \<equiv> (\<exists>x world. Godlike x world)"

theorem obligation_scaffold_is_well_formed:
  assumes "PossiblyGodlike"
  shows "PossiblyGodlike"
  using assms .

text \<open>
  Open obligations:
  1. Select and encode the modal logic.
  2. Add positive-property axioms and necessary-existence semantics.
  3. Check the target conclusion.
  4. Run consistency and modal-collapse checks.
  5. Keep the possibility premise outside the validity theorem.
\<close>

end
""",
        encoding="utf-8",
    )
    return out


def _write_report(session_dir: Path, frontier: dict[str, Any]) -> Path:
    best = frontier["best_current_path"]
    lines = [
        "# God Proof Research Kernel",
        "",
        "Status: no proof is claimed.",
        "",
        "This run converts major God-existence argument families into a proof graph,",
        "premise ledger, counterargument ledger, and machine-next-step frontier.",
        "It is designed to move toward proof by making hidden assumptions explicit.",
        "",
        "## Current Result",
        "",
        f"- proof_claimed: {frontier['proof_claimed']}",
        f"- best_current_path: {best['name']} ({best['argument_id']})",
        f"- proof_proximity: {best['proof_proximity']}",
        "",
        "## Why Not Complete",
        "",
        frontier["reason"],
        "",
        "## Next Machine Steps",
        "",
    ]
    for score in frontier["argument_scores"]:
        lines.append(f"- {score['name']}: {score['machine_next_step']}")
    lines.extend([
        "",
        "## Artifacts",
        "",
        "- `wisdom-map.json`: sources, premises, arguments, and counterarguments.",
        "- `target-concepts.json`: proof target and comparator concept registry.",
        "- `definition-checks.json`: target God concept validation gates.",
        "- `wisdom-corpus.json`: classified human-wisdom entries gathered so far.",
        "- `coverage-matrix.json`: covered, thin, and missing wisdom domains.",
        "- `human-wisdom-primary-source-seed-ledger.json`: primary-source locators for broader wisdom intake.",
        "- `human-wisdom-primary-source-seed-checks.json`: checks that primary sources remain seed-only.",
        "- `human-wisdom-primary-source-extraction-queue.json`: minimized extraction queue for primary sources.",
        "- `human-wisdom-primary-source-extraction-checks.json`: checks that primary-source extraction is unmaterialized.",
        "- `human-wisdom-primary-source-summary-candidates.json`: paraphrase-only source summary candidates.",
        "- `human-wisdom-primary-source-summary-candidate-checks.json`: checks that summary candidates are not corpus entries.",
        "- `human-wisdom-counterpressure-edge-proposals.json`: candidate edges from summaries to proof pressure.",
        "- `human-wisdom-counterpressure-edge-checks.json`: checks that candidate edges are not proof-graph evidence.",
        "- `human-wisdom-counterpressure-edge-review-queue.json`: review queue for candidate counterpressure edges.",
        "- `human-wisdom-counterpressure-edge-review-checks.json`: checks that edge review is not materialization authority.",
        "- `human-wisdom-counterpressure-edge-review-rubric.json`: programmable rubric for edge review.",
        "- `human-wisdom-counterpressure-edge-review-rubric-checks.json`: checks that the rubric is not an applied review.",
        "- `human-wisdom-counterpressure-edge-review-decisions.json`: defer-only edge review decisions.",
        "- `human-wisdom-counterpressure-edge-review-decision-checks.json`: checks that defer decisions are not proof evidence.",
        "- `human-wisdom-counterpressure-edge-resolution-packet.json`: open locator and provenance resolution tasks.",
        "- `human-wisdom-counterpressure-edge-resolution-checks.json`: checks that resolution remains prerequisite work.",
        "- `human-wisdom-counterpressure-edge-evidence-request-queue.json`: queued metadata requests for edge evidence.",
        "- `human-wisdom-counterpressure-edge-evidence-request-checks.json`: checks that evidence requests are not fetched evidence.",
        "- `human-wisdom-counterpressure-edge-evidence-acquisition-manifest.json`: planned metadata acquisition items.",
        "- `human-wisdom-counterpressure-edge-evidence-acquisition-checks.json`: checks that acquisition is unexecuted.",
        "- `human-wisdom-counterpressure-edge-metadata-receipt-schema.json`: metadata receipt templates for acquisition results.",
        "- `human-wisdom-counterpressure-edge-metadata-receipt-checks.json`: checks that receipt templates are not materialized evidence.",
        "- `human-wisdom-counterpressure-edge-metadata-receipt-review-queue.json`: review queue for metadata receipts.",
        "- `human-wisdom-counterpressure-edge-metadata-receipt-review-checks.json`: checks that receipt review is unperformed.",
        "- `human-wisdom-counterpressure-edge-metadata-receipt-review-rubric.json`: programmable rubric for metadata receipt review.",
        "- `human-wisdom-counterpressure-edge-metadata-receipt-review-rubric-checks.json`: checks that receipt rubric is not applied.",
        "- `human-wisdom-counterpressure-edge-metadata-receipt-review-decisions.json`: defer-only receipt review decisions.",
        "- `human-wisdom-counterpressure-edge-metadata-receipt-review-decision-checks.json`: checks that receipt decisions approve nothing.",
        "- `human-wisdom-counterpressure-edge-metadata-receipt-resolution-packet.json`: open receipt metadata resolution tasks.",
        "- `human-wisdom-counterpressure-edge-metadata-receipt-resolution-checks.json`: checks that receipt resolution is prerequisite work.",
        "- `human-wisdom-counterpressure-edge-metadata-receipt-evidence-request-queue.json`: queued receipt metadata requests.",
        "- `human-wisdom-counterpressure-edge-metadata-receipt-evidence-request-checks.json`: checks that receipt metadata requests are not fetched.",
        "- `human-wisdom-counterpressure-edge-metadata-receipt-acquisition-manifest.json`: planned receipt metadata acquisition items.",
        "- `human-wisdom-counterpressure-edge-metadata-receipt-acquisition-checks.json`: checks that receipt acquisition is unexecuted.",
        "- `human-wisdom-counterpressure-edge-metadata-receipt-acquisition-hash-runbook.json`: receipt metadata acquisition and hash command templates.",
        "- `human-wisdom-counterpressure-edge-metadata-receipt-acquisition-hash-runbook-checks.json`: checks that receipt hash commands are not executed.",
        "- `human-wisdom-counterpressure-edge-metadata-receipt-authorization-packet.json`: candidate authorization blockers for receipt metadata acquisition.",
        "- `human-wisdom-counterpressure-edge-metadata-receipt-authorization-checks.json`: checks that receipt fetch and hash remain unauthorized.",
        "- `human-wisdom-counterpressure-edge-metadata-receipt-authorization-review-queue.json`: review queue for receipt metadata authorization blockers.",
        "- `human-wisdom-counterpressure-edge-metadata-receipt-authorization-review-checks.json`: checks that authorization review remains unperformed.",
        "- `human-wisdom-intake-roadmap.json`: open-ended intake lanes beyond current coverage.",
        "- `human-wisdom-intake-checks.json`: checks that exhaustive human wisdom is not claimed.",
        "- `proof-graph.json`: nodes and edges for proof search.",
        "- `modal-derivation.json`: encoded S5 modal bridge derivation.",
        "- `modal-validity-checks.json`: local structural validation of the modal bridge.",
        "- `modal-consistency-checks.json`: finite model and modal-collapse sanity checks.",
        "- `ontological-soundness-dossier.json`: possibility-premise support, objections, and parody tests.",
        "- `ontological-soundness-checks.json`: contested soundness checks that still block proof claim.",
        "- `ontological-soundness-parody-discriminator-matrix.json`: discriminator rows for parody pressure.",
        "- `ontological-soundness-parody-discriminator-checks.json`: checks that parody discriminators remain contested.",
        "- `ontological-soundness-bad-god-discharge-criteria.json`: unresolved requirements for bad-god parody discharge.",
        "- `ontological-soundness-bad-god-discharge-checks.json`: checks that bad-god discharge is not promoted.",
        "- `ontological-soundness-bad-god-discharge-task-queue.json`: queued tasks for bad-god discharge requirements.",
        "- `ontological-soundness-bad-god-discharge-task-checks.json`: checks that bad-god tasks are unexecuted.",
        "- `ontological-soundness-bad-god-task-dependency-graph.json`: dependency ordering for bad-god tasks.",
        "- `ontological-soundness-bad-god-task-dependency-checks.json`: checks that dependency graph is not proof.",
        "- `ontological-soundness-bad-god-evil-hiddenness-pressure-matrix.json`: pressure rows for bad-god first task.",
        "- `ontological-soundness-bad-god-evil-hiddenness-pressure-checks.json`: checks that pressure remains open.",
        "- `ontological-soundness-bad-god-evil-hiddenness-sufficiency-task-queue.json`: queued tasks for open sufficiency tests.",
        "- `ontological-soundness-bad-god-evil-hiddenness-sufficiency-task-checks.json`: checks that sufficiency tasks remain unexecuted.",
        "- `ontological-soundness-bad-god-evidential-probability-pressure-task-scaffold.json`: evaluation scaffold for the first sufficiency task.",
        "- `ontological-soundness-bad-god-evidential-probability-pressure-task-checks.json`: checks that the scaffold is not proof.",
        "- `ontological-soundness-bad-god-evidential-prior-sensitivity-grid.json`: normalized prior profiles for the priors lane.",
        "- `ontological-soundness-bad-god-evidential-prior-sensitivity-checks.json`: checks that prior profiles are not executed proof.",
        "- `ontological-soundness-bad-god-evidential-likelihood-sensitivity-grid.json`: likelihood interval cells for the likelihoods lane.",
        "- `ontological-soundness-bad-god-evidential-likelihood-sensitivity-checks.json`: checks that likelihood projections remain unexecuted.",
        "- `ontological-soundness-bad-god-evidential-response-cost-grid.json`: response penalty intervals for the response-cost lane.",
        "- `ontological-soundness-bad-god-evidential-response-cost-checks.json`: checks that response-cost projections remain unexecuted.",
        "- `ontological-soundness-bad-god-evidential-rival-comparison-grid.json`: rival likelihood rows for the rival-comparison lane.",
        "- `ontological-soundness-bad-god-evidential-rival-comparison-checks.json`: checks that rival comparison remains unexecuted.",
        "- `ontological-soundness-bad-god-evidential-probability-execution-packet.json`: ordered execution packet for evidential probability lanes.",
        "- `ontological-soundness-bad-god-evidential-probability-execution-checks.json`: checks that the execution packet is not run proof.",
        "- `ontological-soundness-bad-god-evidential-posterior-projection-results.json`: candidate posterior projections for evidential probability pressure.",
        "- `ontological-soundness-bad-god-evidential-posterior-projection-checks.json`: checks that posterior projections remain contested.",
        "- `ontological-soundness-bad-god-evidential-projection-outcome-review.json`: outcome review for candidate projection pressure.",
        "- `ontological-soundness-bad-god-evidential-projection-outcome-checks.json`: checks that outcome review remains non-proof.",
        "- `ontological-soundness-bad-god-evidential-projection-remediation-plan.json`: queued remediation plan for projection outcome risks.",
        "- `ontological-soundness-bad-god-evidential-projection-remediation-checks.json`: checks that remediation remains unexecuted non-proof work.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-registry.json`: source-family registry for calibration remediation.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-checks.json`: checks that calibration sources are scoped but not ingested proof.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-acquisition-manifest.json`: queued acquisition manifest for calibration sources.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-acquisition-checks.json`: checks that acquisition remains unfetched non-proof work.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-batch-plan.json`: auditable batch plan for calibration source acquisition.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-batch-checks.json`: checks that source batches remain unexecuted.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-seed-catalog.json`: verified seed URLs for calibration source acquisition.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-seed-checks.json`: checks that seed URLs remain unfetched non-proof work.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-eligibility-matrix.json`: pre-fetch gate classification for seed sources.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-eligibility-checks.json`: checks that eligibility remains unscored non-proof work.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-retrieval-runbook.json`: fetch, hash, and log templates for eligible sources.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-retrieval-checks.json`: checks that retrieval remains unexecuted non-proof work.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-retrieval-log-schema.json`: required retrieval log schema and hash fields.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-retrieval-log-checks.json`: checks that retrieval logs remain unmaterialized.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-retrieval-dry-run-ledger.json`: pre-execution audit of retrieval command wiring.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-retrieval-dry-run-checks.json`: checks that dry-run retrieval remains unexecuted.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-quality-rubric.json`: post-fetch source quality scoring rubric.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-quality-checks.json`: checks that source quality remains unscored.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-quality-score-ledger-schema.json`: schema for post-fetch source quality scores.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-quality-score-ledger-checks.json`: checks that quality score ledger remains empty.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-quality-score-dry-run-ledger.json`: dry-run ledger for source quality scoring.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-quality-score-dry-run-checks.json`: checks that dry-run quality scoring remains unexecuted.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-quality-score-readiness-gate.json`: readiness gate blocking quality scoring until source content exists.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-quality-score-readiness-checks.json`: checks that quality scoring remains blocked before retrieval.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-packet.json`: pre-execution packet for source content, hash, and retrieval log materialization.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-checks.json`: checks that source content materialization remains unexecuted.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-batch-plan.json`: batch plan for source content materialization.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-batch-checks.json`: checks that materialization batches remain unexecuted.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-packet.json`: authorization packet blocking network materialization until approval.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-checks.json`: checks that network materialization remains unauthorized.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-queue.json`: review queue for materialization authorization blockers.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-checks.json`: checks that materialization authorization review remains unperformed.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-rubric.json`: rubric for materialization authorization review.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-rubric-checks.json`: checks that authorization rubric remains unapplied.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-decisions.json`: defer-only decisions for materialization authorization review.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-decision-checks.json`: checks that authorization decisions deny network retrieval.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-resolution-packet.json`: open prerequisite-resolution tasks for deferred authorization decisions.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-resolution-checks.json`: checks that authorization resolution remains open and non-proving.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-operator-approval-request.json`: request packet for the missing operator approval reference.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-operator-approval-checks.json`: checks that operator approval is requested but not granted.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-terms-rate-limit-review.json`: pending terms and rate-limit review for materialization batches.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-terms-rate-limit-checks.json`: checks that terms and rate-limit review still blocks retrieval.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-private-sensitive-risk-review.json`: pending private/sensitive content risk review for materialization batches.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-private-sensitive-risk-checks.json`: checks that private/sensitive content risk review still blocks retrieval.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-retrieval-scope-review.json`: pending retrieval scope review for materialization batches.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-retrieval-scope-checks.json`: checks that retrieval scope review still blocks retrieval.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-logging-hash-plan-review.json`: pending logging/hash plan review for materialization batches.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-logging-hash-plan-checks.json`: checks that logging/hash plan review still blocks retrieval.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-prerequisite-closure-matrix.json`: cross-prerequisite closure matrix for materialization authorization.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-prerequisite-closure-checks.json`: checks that prerequisite closure remains incomplete and non-proving.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-materialization-execution-gate.json`: execution gate denying materialization until prerequisites close.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-materialization-execution-gate-checks.json`: checks that materialization execution remains denied.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-future-command-manifest.json`: future source-fetch command templates kept non-executable.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-future-command-manifest-checks.json`: checks that future materialization commands remain non-executable.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-nonexecution-receipt.json`: receipt that future materialization commands were not executed.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-nonexecution-receipt-checks.json`: checks that no content, retrieval log, or hash outputs were written.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-ledger.json`: ledger of missing content, retrieval log, and hash outputs per command.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-checks.json`: checks that command output gaps remain open and non-proving.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-task-queue.json`: queued tasks for closing each missing command output gap.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-task-checks.json`: checks that gap-closure tasks remain blocked and non-proving.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-plan.json`: command-level batch plan for queued gap-closure tasks.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-checks.json`: checks that gap-closure batches remain blocked and non-proving.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-ledger.json`: ledger recording that gap-closure batch execution has not started.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-checks.json`: checks that no batch execution outputs were materialized.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-matrix.json`: batch-level open prerequisites blocking execution.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-checks.json`: checks that all execution unblockers remain open.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-queue.json`: ordered queue for resolving open batch execution unblockers.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-checks.json`: checks that unblocker resolution tasks remain open.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-batch-plan.json`: prerequisite-type batch plan for resolving open unblockers.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-batch-checks.json`: checks that unblocker resolution batches remain open.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-batch-execution-ledger.json`: ledger recording that unblocker resolution batches have not started.",
        "- `ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-batch-execution-checks.json`: checks that no unblocker resolution was materialized.",
        "- `ontological-soundness-resolution-worklist.json`: queued work items for the remaining soundness blocker.",
        "- `ontological-soundness-resolution-worklist-checks.json`: checks that the worklist is not proof evidence.",
        "- `ontological-soundness-resolution-batches.json`: executable batch plan for soundness-resolution work.",
        "- `ontological-soundness-resolution-batch-checks.json`: checks that batches remain unexecuted plans.",
        "- `ontological-soundness-batch-execution-ledger.json`: execution audit ledger for soundness batches.",
        "- `ontological-soundness-batch-execution-checks.json`: checks that batch execution has not started.",
        "- `attribute-coherence-ledger.json`: target-attribute tension ledger for the possibility premise.",
        "- `attribute-coherence-checks.json`: coherence screening checks tied to the soundness gate.",
        "- `coherent-conceivability-model.json`: candidate repair models for target-attribute tensions.",
        "- `coherent-conceivability-checks.json`: local coherence checks for the conceivability stage.",
        "- `metaphysical-possibility-bridge.json`: support and defeater routes for the conceivability-to-possibility bridge.",
        "- `metaphysical-possibility-checks.json`: bridge checks that keep metaphysical possibility contested.",
        "- `definition-smuggling-audit.json`: audit separating target definition from actuality claims.",
        "- `definition-smuggling-checks.json`: checks for necessary-existence definition smuggling.",
        "- `evidential-evil-probability-audit.json`: probability audit for evidential evil pressure.",
        "- `evidential-evil-likelihood-ledger.json`: candidate interval likelihoods for evidential evil.",
        "- `evidential-evil-dependence-model.json`: dependence and sensitivity model for evidential evil.",
        "- `evidential-evil-case-corpus.json`: mapped case families for evil and hiddenness calibration.",
        "- `evidential-evil-reviewed-case-records.json`: source-backed records for case families.",
        "- `evidential-evil-primary-dataset-selection.json`: official and peer-reviewed dataset candidates.",
        "- `evidential-evil-dataset-ingestion-manifest.json`: planned fetch, hash, parse, and privacy gates.",
        "- `evidential-evil-license-privacy-review.json`: terms and privacy review gate for dataset ingestion.",
        "- `evidential-evil-attribution-template-ledger.json`: draft source attribution templates.",
        "- `evidential-evil-attribution-template-checks.json`: checks that attribution remains non-authorizing.",
        "- `evidential-evil-license-decision-packet.json`: candidate source-specific reuse decisions.",
        "- `evidential-evil-license-decision-checks.json`: checks that reuse decisions remain non-authorizing.",
        "- `evidential-evil-source-acquisition-hash-runbook.json`: acquisition, hash, log, and prune command templates.",
        "- `evidential-evil-source-acquisition-hash-runbook-checks.json`: checks that acquisition remains unexecuted.",
        "- `evidential-evil-suppression-report-template.json`: publication suppression report templates.",
        "- `evidential-evil-suppression-report-template-checks.json`: checks that suppression reports remain unfilled.",
        "- `evidential-evil-source-version-hash-preflight.json`: candidate source version locators and hash targets.",
        "- `evidential-evil-source-version-hash-preflight-checks.json`: checks that source files and hashes remain open.",
        "- `evidential-evil-derived-aggregate-schema.json`: candidate aggregate table schemas and allowlists.",
        "- `evidential-evil-derived-aggregate-schema-checks.json`: checks that schemas remain unmaterialized.",
        "- `evidential-evil-microdata-minimization-policy.json`: policy blocking raw microdata retention.",
        "- `evidential-evil-microdata-minimization-checks.json`: checks that minimization remains non-authorizing.",
        "- `evidential-evil-license-privacy-checks.json`: checks that reuse authorization remains open.",
        "- `evidential-evil-dataset-ingestion-checks.json`: checks that ingestion remains unexecuted.",
        "- `evidential-evil-primary-dataset-selection-checks.json`: checks for selected-source coverage.",
        "- `evidential-evil-empirical-expansion-ledger.json`: empirical record classes still needing data ingestion.",
        "- `evidential-evil-empirical-expansion-checks.json`: checks for empirical expansion coverage and open ingestion.",
        "- `evidential-evil-reviewed-case-records-checks.json`: checks for case-record citation coverage.",
        "- `evidential-evil-case-corpus-checks.json`: checks for case-family dimension and cluster coverage.",
        "- `evidential-evil-calibration-ledger.json`: candidate cluster-weight and dependence-strength calibration.",
        "- `evidential-evil-calibration-checks.json`: checks for open calibration requirements.",
        "- `evidential-evil-dependence-checks.json`: checks that block naive independent aggregation.",
        "- `evidential-evil-likelihood-checks.json`: checks for prior, likelihood, and response-cost intervals.",
        "- `evidential-evil-probability-checks.json`: checks that keep interval likelihoods non-decisive.",
        "- `evil-hiddenness-moral-pressure-audit.json`: audit for evil and hiddenness pressure on perfect goodness.",
        "- `evil-hiddenness-moral-pressure-checks.json`: checks for unresolved moral-pressure responses.",
        "- `moral-perfection-grounding-audit.json`: audit for circularity in moral-perfection grounding.",
        "- `moral-perfection-grounding-checks.json`: checks for unresolved perfect-goodness grounding.",
        "- `positive-grounding-audit.json`: audit for non-arbitrary positive-property grounding.",
        "- `positive-grounding-checks.json`: checks for unresolved grounding and anti-ad-hoc tests.",
        "- `positive-property-filter-audit.json`: audit for the bad-god positive-property filter.",
        "- `positive-property-filter-checks.json`: checks for unresolved positive-property grounding.",
        "- `rival-necessary-parity-audit.json`: rival necessary-concept parity comparison.",
        "- `rival-necessary-parity-checks.json`: checks for unresolved uniqueness filters.",
        "- `possible-necessary-existence-bridge.json`: support and defeater routes before the S5 bridge.",
        "- `possible-necessary-existence-checks.json`: checks that keep possible necessary existence contested.",
        "- `possibility-premise-ladder.json`: stage decomposition of the possibility premise.",
        "- `possibility-premise-checks.json`: checks for blocked bridges in the possibility ladder.",
        "- `teleological-bayes-model.json`: explicit fine-tuning Bayesian model.",
        "- `teleological-bayes-checks.json`: sensitivity and model-completeness checks.",
        "- `cosmological-psr-model.json`: PSR variants, countermodels, and bridge requirements.",
        "- `cosmological-psr-checks.json`: PSR taxonomy and partial-bridge checks.",
        "- `evil-hiddenness-constraints.json`: evil, hiddenness, and diversity constraints.",
        "- `evil-hiddenness-checks.json`: constraint coverage and retained-risk checks.",
        "- `frontier.json`: scored missing gates and next steps.",
        "- `formal-obligations.json`: machine-checkable obligations that block proof claims.",
        "- `proof-readiness.json`: gate result for whether a proof may be claimed.",
        "- `proof-assistant-skeletons/`: formalization starting points.",
        "- `sources.jsonl`: source ledger with retrieval dates.",
        "- `transcript.jsonl`: full event log for this run.",
    ])
    out = session_dir / "report.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def run_godproof(*, sessions_root: Path | None = None, query: str | None = None) -> dict[str, Any]:
    """Run the local God-proof proof-frontier builder."""
    sessions_root = sessions_root or DEFAULT_GODPROOF_ROOT
    query = query or "God proof proof-frontier"
    session_dir = new_session_dir(sessions_root, query)
    transcript_path = session_dir / "transcript.jsonl"
    sources_path = session_dir / "sources.jsonl"
    transcript_path.touch()
    sources_path.touch()

    t0 = time.time()

    def log(event_type: str, payload: dict[str, Any] | None = None) -> None:
        _append_jsonl(transcript_path, {
            "ts": time.time(),
            "elapsed": round(time.time() - t0, 3),
            "type": event_type,
            "payload": payload or {},
        })

    log("session_start", {"query": query, "mode": "local-proof-frontier"})
    for source in SOURCES:
        _append_jsonl(sources_path, source.as_dict())
    log("sources_loaded", {"count": len(SOURCES), "retrieved_at": RETRIEVED_AT})

    wisdom_map = _build_wisdom_map()
    target_concepts = _build_target_concept_registry()
    definition_checks = _build_definition_checks()
    modal_derivation = _build_modal_derivation()
    modal_validity_checks = _build_modal_validity_checks()
    modal_consistency_checks = _build_modal_consistency_checks()
    ontological_soundness_dossier = _build_ontological_soundness_dossier()
    attribute_coherence_ledger = _build_attribute_coherence_ledger()
    attribute_coherence_checks = _build_attribute_coherence_checks()
    coherent_conceivability_model = _build_coherent_conceivability_model()
    coherent_conceivability_checks = _build_coherent_conceivability_checks()
    metaphysical_possibility_bridge = _build_metaphysical_possibility_bridge()
    metaphysical_possibility_checks = _build_metaphysical_possibility_checks(coherent_conceivability_checks)
    definition_smuggling_audit = _build_definition_smuggling_audit()
    definition_smuggling_checks = _build_definition_smuggling_checks()
    evil_hiddenness_moral_pressure_audit = _build_evil_hiddenness_moral_pressure_audit()
    evidential_evil_probability_audit = _build_evidential_evil_probability_audit()
    evidential_evil_likelihood_ledger = _build_evidential_evil_likelihood_ledger()
    evidential_evil_dependence_model = _build_evidential_evil_dependence_model()
    evidential_evil_calibration_ledger = _build_evidential_evil_calibration_ledger()
    evidential_evil_case_corpus = _build_evidential_evil_case_corpus()
    evidential_evil_reviewed_case_records = _build_evidential_evil_reviewed_case_records()
    evidential_evil_empirical_expansion_ledger = _build_evidential_evil_empirical_expansion_ledger()
    evidential_evil_primary_dataset_selection = _build_evidential_evil_primary_dataset_selection()
    evidential_evil_dataset_ingestion_manifest = _build_evidential_evil_dataset_ingestion_manifest()
    evidential_evil_license_privacy_review = _build_evidential_evil_license_privacy_review()
    evidential_evil_attribution_template_ledger = _build_evidential_evil_attribution_template_ledger()
    evidential_evil_attribution_template_checks = _build_evidential_evil_attribution_template_checks()
    evidential_evil_license_decision_packet = _build_evidential_evil_license_decision_packet()
    evidential_evil_license_decision_checks = _build_evidential_evil_license_decision_checks(
        evidential_evil_attribution_template_checks
    )
    evidential_evil_microdata_minimization_policy = _build_evidential_evil_microdata_minimization_policy()
    evidential_evil_derived_aggregate_schema = _build_evidential_evil_derived_aggregate_schema()
    evidential_evil_source_acquisition_hash_runbook = _build_evidential_evil_source_acquisition_hash_runbook()
    evidential_evil_source_acquisition_hash_runbook_checks = (
        _build_evidential_evil_source_acquisition_hash_runbook_checks()
    )
    evidential_evil_suppression_report_template = _build_evidential_evil_suppression_report_template()
    evidential_evil_suppression_report_template_checks = _build_evidential_evil_suppression_report_template_checks(
        evidential_evil_source_acquisition_hash_runbook_checks
    )
    evidential_evil_source_version_hash_preflight = _build_evidential_evil_source_version_hash_preflight()
    evidential_evil_source_version_hash_preflight_checks = (
        _build_evidential_evil_source_version_hash_preflight_checks(
            evidential_evil_source_acquisition_hash_runbook_checks
        )
    )
    evidential_evil_derived_aggregate_schema_checks = _build_evidential_evil_derived_aggregate_schema_checks(
        evidential_evil_source_version_hash_preflight_checks,
        evidential_evil_suppression_report_template_checks,
    )
    evidential_evil_microdata_minimization_checks = _build_evidential_evil_microdata_minimization_checks(
        evidential_evil_license_decision_checks,
        evidential_evil_derived_aggregate_schema_checks,
    )
    evidential_evil_license_privacy_checks = _build_evidential_evil_license_privacy_checks(
        evidential_evil_attribution_template_checks,
        evidential_evil_license_decision_checks,
        evidential_evil_derived_aggregate_schema_checks,
        evidential_evil_microdata_minimization_checks,
    )
    evidential_evil_dataset_ingestion_checks = _build_evidential_evil_dataset_ingestion_checks(
        evidential_evil_license_privacy_checks
    )
    evidential_evil_primary_dataset_selection_checks = _build_evidential_evil_primary_dataset_selection_checks(
        evidential_evil_dataset_ingestion_checks
    )
    evidential_evil_empirical_expansion_checks = _build_evidential_evil_empirical_expansion_checks(
        evidential_evil_primary_dataset_selection_checks
    )
    evidential_evil_reviewed_case_record_checks = _build_evidential_evil_reviewed_case_record_checks(
        evidential_evil_empirical_expansion_checks
    )
    evidential_evil_case_corpus_checks = _build_evidential_evil_case_corpus_checks(
        evidential_evil_reviewed_case_record_checks
    )
    evidential_evil_calibration_checks = _build_evidential_evil_calibration_checks(
        evidential_evil_case_corpus_checks
    )
    evidential_evil_dependence_checks = _build_evidential_evil_dependence_checks(
        evidential_evil_calibration_checks
    )
    evidential_evil_likelihood_checks = _build_evidential_evil_likelihood_checks(
        evidential_evil_dependence_checks
    )
    evidential_evil_probability_checks = _build_evidential_evil_probability_checks(
        evidential_evil_likelihood_checks
    )
    evil_hiddenness_moral_pressure_checks = _build_evil_hiddenness_moral_pressure_checks(
        evidential_evil_probability_checks
    )
    moral_perfection_grounding_audit = _build_moral_perfection_grounding_audit()
    moral_perfection_grounding_checks = _build_moral_perfection_grounding_checks(
        evil_hiddenness_moral_pressure_checks
    )
    positive_grounding_audit = _build_positive_grounding_audit()
    positive_grounding_checks = _build_positive_grounding_checks(
        moral_perfection_grounding_checks,
        evil_hiddenness_moral_pressure_checks,
    )
    positive_property_filter_audit = _build_positive_property_filter_audit()
    positive_property_filter_checks = _build_positive_property_filter_checks(
        positive_grounding_checks,
        moral_perfection_grounding_checks,
        evil_hiddenness_moral_pressure_checks,
    )
    rival_necessary_parity_audit = _build_rival_necessary_parity_audit()
    rival_necessary_parity_checks = _build_rival_necessary_parity_checks(
        positive_property_filter_checks,
        positive_grounding_checks,
        moral_perfection_grounding_checks,
        evil_hiddenness_moral_pressure_checks,
    )
    possible_necessary_existence_bridge = _build_possible_necessary_existence_bridge()
    possible_necessary_existence_checks = _build_possible_necessary_existence_checks(
        metaphysical_possibility_checks,
        modal_validity_checks,
        modal_consistency_checks,
        definition_smuggling_checks,
        rival_necessary_parity_checks,
        positive_property_filter_checks,
        positive_grounding_checks,
        moral_perfection_grounding_checks,
    )
    possibility_premise_ladder = _build_possibility_premise_ladder()
    possibility_premise_checks = _build_possibility_premise_checks(
        coherent_conceivability_checks,
        metaphysical_possibility_checks,
        possible_necessary_existence_checks,
    )
    ontological_soundness_checks = _build_ontological_soundness_checks(
        attribute_coherence_checks,
        coherent_conceivability_checks,
        metaphysical_possibility_checks,
        definition_smuggling_checks,
        evidential_evil_attribution_template_checks,
        evidential_evil_license_decision_checks,
        evidential_evil_source_acquisition_hash_runbook_checks,
        evidential_evil_suppression_report_template_checks,
        evidential_evil_source_version_hash_preflight_checks,
        evidential_evil_derived_aggregate_schema_checks,
        evidential_evil_microdata_minimization_checks,
        evidential_evil_license_privacy_checks,
        evidential_evil_dataset_ingestion_checks,
        evidential_evil_primary_dataset_selection_checks,
        evidential_evil_empirical_expansion_checks,
        evidential_evil_reviewed_case_record_checks,
        evidential_evil_case_corpus_checks,
        evidential_evil_calibration_checks,
        evidential_evil_dependence_checks,
        evidential_evil_likelihood_checks,
        evidential_evil_probability_checks,
        evil_hiddenness_moral_pressure_checks,
        moral_perfection_grounding_checks,
        positive_grounding_checks,
        positive_property_filter_checks,
        rival_necessary_parity_checks,
        possible_necessary_existence_checks,
        possibility_premise_checks,
    )
    ontological_soundness_parody_discriminator_matrix = (
        _build_ontological_soundness_parody_discriminator_matrix()
    )
    ontological_soundness_parody_discriminator_checks = (
        _build_ontological_soundness_parody_discriminator_checks(
            ontological_soundness_parody_discriminator_matrix
        )
    )
    ontological_soundness_bad_god_discharge_criteria = (
        _build_ontological_soundness_bad_god_discharge_criteria(
            ontological_soundness_parody_discriminator_matrix,
            positive_property_filter_checks,
            positive_grounding_checks,
            moral_perfection_grounding_checks,
            evil_hiddenness_moral_pressure_checks,
            rival_necessary_parity_checks,
        )
    )
    ontological_soundness_bad_god_discharge_checks = (
        _build_ontological_soundness_bad_god_discharge_checks(
            ontological_soundness_parody_discriminator_matrix,
            ontological_soundness_bad_god_discharge_criteria,
        )
    )
    ontological_soundness_bad_god_discharge_task_queue = (
        _build_ontological_soundness_bad_god_discharge_task_queue(
            ontological_soundness_bad_god_discharge_criteria
        )
    )
    ontological_soundness_bad_god_discharge_task_checks = (
        _build_ontological_soundness_bad_god_discharge_task_checks(
            ontological_soundness_bad_god_discharge_criteria,
            ontological_soundness_bad_god_discharge_task_queue,
        )
    )
    ontological_soundness_bad_god_task_dependency_graph = (
        _build_ontological_soundness_bad_god_task_dependency_graph(
            ontological_soundness_bad_god_discharge_task_queue
        )
    )
    ontological_soundness_bad_god_task_dependency_checks = (
        _build_ontological_soundness_bad_god_task_dependency_checks(
            ontological_soundness_bad_god_discharge_task_queue,
            ontological_soundness_bad_god_task_dependency_graph,
        )
    )
    ontological_soundness_bad_god_evil_hiddenness_pressure_matrix = (
        _build_ontological_soundness_bad_god_evil_hiddenness_pressure_matrix(
            ontological_soundness_bad_god_task_dependency_graph
        )
    )
    ontological_soundness_bad_god_evil_hiddenness_pressure_checks = (
        _build_ontological_soundness_bad_god_evil_hiddenness_pressure_checks(
            ontological_soundness_bad_god_task_dependency_graph,
            ontological_soundness_bad_god_evil_hiddenness_pressure_matrix,
        )
    )
    ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_queue = (
        _build_ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_queue(
            ontological_soundness_bad_god_evil_hiddenness_pressure_matrix
        )
    )
    ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_checks = (
        _build_ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_checks(
            ontological_soundness_bad_god_evil_hiddenness_pressure_matrix,
            ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_queue,
        )
    )
    ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold = (
        _build_ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold(
            ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_queue,
            evidential_evil_probability_audit,
            evidential_evil_probability_checks,
        )
    )
    ontological_soundness_bad_god_evidential_probability_pressure_task_checks = (
        _build_ontological_soundness_bad_god_evidential_probability_pressure_task_checks(
            ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_queue,
            ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold,
            evidential_evil_probability_audit,
            evidential_evil_probability_checks,
        )
    )
    ontological_soundness_bad_god_evidential_prior_sensitivity_grid = (
        _build_ontological_soundness_bad_god_evidential_prior_sensitivity_grid(
            ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold,
            evidential_evil_likelihood_ledger,
        )
    )
    ontological_soundness_bad_god_evidential_prior_sensitivity_checks = (
        _build_ontological_soundness_bad_god_evidential_prior_sensitivity_checks(
            ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold,
            ontological_soundness_bad_god_evidential_prior_sensitivity_grid,
            evidential_evil_likelihood_ledger,
        )
    )
    ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid = (
        _build_ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid(
            ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold,
            ontological_soundness_bad_god_evidential_prior_sensitivity_grid,
            evidential_evil_likelihood_ledger,
        )
    )
    ontological_soundness_bad_god_evidential_likelihood_sensitivity_checks = (
        _build_ontological_soundness_bad_god_evidential_likelihood_sensitivity_checks(
            ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold,
            ontological_soundness_bad_god_evidential_prior_sensitivity_grid,
            ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid,
            evidential_evil_likelihood_ledger,
        )
    )
    ontological_soundness_bad_god_evidential_response_cost_grid = (
        _build_ontological_soundness_bad_god_evidential_response_cost_grid(
            ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold,
            ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid,
            evidential_evil_likelihood_ledger,
        )
    )
    ontological_soundness_bad_god_evidential_response_cost_checks = (
        _build_ontological_soundness_bad_god_evidential_response_cost_checks(
            ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold,
            ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid,
            ontological_soundness_bad_god_evidential_response_cost_grid,
            evidential_evil_likelihood_ledger,
        )
    )
    ontological_soundness_bad_god_evidential_rival_comparison_grid = (
        _build_ontological_soundness_bad_god_evidential_rival_comparison_grid(
            ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold,
            ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid,
            ontological_soundness_bad_god_evidential_response_cost_grid,
            rival_necessary_parity_checks,
        )
    )
    ontological_soundness_bad_god_evidential_rival_comparison_checks = (
        _build_ontological_soundness_bad_god_evidential_rival_comparison_checks(
            ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold,
            ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid,
            ontological_soundness_bad_god_evidential_response_cost_grid,
            ontological_soundness_bad_god_evidential_rival_comparison_grid,
            rival_necessary_parity_checks,
        )
    )
    ontological_soundness_bad_god_evidential_probability_execution_packet = (
        _build_ontological_soundness_bad_god_evidential_probability_execution_packet(
            ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold,
            ontological_soundness_bad_god_evidential_prior_sensitivity_grid,
            ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid,
            ontological_soundness_bad_god_evidential_response_cost_grid,
            ontological_soundness_bad_god_evidential_rival_comparison_grid,
        )
    )
    ontological_soundness_bad_god_evidential_probability_execution_checks = (
        _build_ontological_soundness_bad_god_evidential_probability_execution_checks(
            ontological_soundness_bad_god_evidential_probability_execution_packet,
            ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold,
            ontological_soundness_bad_god_evidential_prior_sensitivity_grid,
            ontological_soundness_bad_god_evidential_prior_sensitivity_checks,
            ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid,
            ontological_soundness_bad_god_evidential_likelihood_sensitivity_checks,
            ontological_soundness_bad_god_evidential_response_cost_grid,
            ontological_soundness_bad_god_evidential_response_cost_checks,
            ontological_soundness_bad_god_evidential_rival_comparison_grid,
            ontological_soundness_bad_god_evidential_rival_comparison_checks,
        )
    )
    ontological_soundness_bad_god_evidential_posterior_projection_results = (
        _build_ontological_soundness_bad_god_evidential_posterior_projection_results(
            ontological_soundness_bad_god_evidential_probability_execution_packet,
            ontological_soundness_bad_god_evidential_prior_sensitivity_grid,
            ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid,
            ontological_soundness_bad_god_evidential_response_cost_grid,
        )
    )
    ontological_soundness_bad_god_evidential_posterior_projection_checks = (
        _build_ontological_soundness_bad_god_evidential_posterior_projection_checks(
            ontological_soundness_bad_god_evidential_posterior_projection_results,
            ontological_soundness_bad_god_evidential_probability_execution_packet,
        )
    )
    ontological_soundness_bad_god_evidential_projection_outcome_review = (
        _build_ontological_soundness_bad_god_evidential_projection_outcome_review(
            ontological_soundness_bad_god_evidential_posterior_projection_results
        )
    )
    ontological_soundness_bad_god_evidential_projection_outcome_checks = (
        _build_ontological_soundness_bad_god_evidential_projection_outcome_checks(
            ontological_soundness_bad_god_evidential_posterior_projection_results,
            ontological_soundness_bad_god_evidential_projection_outcome_review,
        )
    )
    ontological_soundness_bad_god_evidential_projection_remediation_plan = (
        _build_ontological_soundness_bad_god_evidential_projection_remediation_plan(
            ontological_soundness_bad_god_evidential_projection_outcome_review
        )
    )
    ontological_soundness_bad_god_evidential_projection_remediation_checks = (
        _build_ontological_soundness_bad_god_evidential_projection_remediation_checks(
            ontological_soundness_bad_god_evidential_projection_outcome_review,
            ontological_soundness_bad_god_evidential_projection_remediation_plan,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_registry = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_registry(
            ontological_soundness_bad_god_evidential_projection_remediation_plan
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_checks(
            ontological_soundness_bad_god_evidential_projection_remediation_plan,
            ontological_soundness_bad_god_evidential_calibration_source_registry,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_acquisition_manifest = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_acquisition_manifest(
            ontological_soundness_bad_god_evidential_calibration_source_registry
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_acquisition_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_acquisition_checks(
            ontological_soundness_bad_god_evidential_calibration_source_registry,
            ontological_soundness_bad_god_evidential_calibration_source_acquisition_manifest,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_batch_plan = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_batch_plan(
            ontological_soundness_bad_god_evidential_calibration_source_acquisition_manifest
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_batch_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_batch_checks(
            ontological_soundness_bad_god_evidential_calibration_source_acquisition_manifest,
            ontological_soundness_bad_god_evidential_calibration_source_batch_plan,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_seed_catalog = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_seed_catalog(
            ontological_soundness_bad_god_evidential_calibration_source_batch_plan
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_seed_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_seed_checks(
            ontological_soundness_bad_god_evidential_calibration_source_batch_plan,
            ontological_soundness_bad_god_evidential_calibration_source_seed_catalog,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_eligibility_matrix = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_eligibility_matrix(
            ontological_soundness_bad_god_evidential_calibration_source_seed_catalog
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_eligibility_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_eligibility_checks(
            ontological_soundness_bad_god_evidential_calibration_source_seed_catalog,
            ontological_soundness_bad_god_evidential_calibration_source_eligibility_matrix,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook(
            ontological_soundness_bad_god_evidential_calibration_source_eligibility_matrix
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_retrieval_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_retrieval_checks(
            ontological_soundness_bad_god_evidential_calibration_source_eligibility_matrix,
            ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_schema = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_schema(
            ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_checks(
            ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook,
            ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_schema,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger(
            ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook,
            ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_schema,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_checks(
            ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook,
            ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_schema,
            ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_quality_rubric = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_quality_rubric(
            ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_quality_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_quality_checks(
            ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger,
            ontological_soundness_bad_god_evidential_calibration_source_quality_rubric,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_schema = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_schema(
            ontological_soundness_bad_god_evidential_calibration_source_quality_rubric
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_checks(
            ontological_soundness_bad_god_evidential_calibration_source_quality_rubric,
            ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_schema,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_ledger = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_ledger(
            ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_schema
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_checks(
            ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_schema,
            ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_ledger,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_gate = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_gate(
            ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_ledger
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_checks(
            ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_ledger,
            ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_gate,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_packet = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_packet(
            ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger,
            ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_gate,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_checks(
            ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger,
            ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_gate,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_packet,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_plan = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_plan(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_packet
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_checks(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_packet,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_plan,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_packet = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_packet(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_plan
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_checks(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_plan,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_packet,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_queue = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_queue(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_packet
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_checks(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_packet,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_queue,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_queue
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric_checks(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_queue,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decisions = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decisions(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decision_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decision_checks(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decisions,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decisions
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_checks(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decisions,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_operator_approval_request = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_operator_approval_request(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_operator_approval_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_operator_approval_checks(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_operator_approval_request,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_terms_rate_limit_review = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_terms_rate_limit_review(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_terms_rate_limit_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_terms_rate_limit_checks(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_terms_rate_limit_review,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_private_sensitive_risk_review = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_private_sensitive_risk_review(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_private_sensitive_risk_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_private_sensitive_risk_checks(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_private_sensitive_risk_review,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_retrieval_scope_review = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_retrieval_scope_review(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_retrieval_scope_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_retrieval_scope_checks(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_retrieval_scope_review,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_logging_hash_plan_review = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_logging_hash_plan_review(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_logging_hash_plan_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_logging_hash_plan_checks(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_logging_hash_plan_review,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_matrix = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_matrix(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_operator_approval_request,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_terms_rate_limit_review,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_private_sensitive_risk_review,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_retrieval_scope_review,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_logging_hash_plan_review,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_checks(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_matrix,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_matrix,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate_checks(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_matrix,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest_checks(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt_checks(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_ledger = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_ledger(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_checks(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_ledger,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_queue = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_queue(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_ledger
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_checks(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_ledger,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_queue,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_plan = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_plan(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_queue
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_checks(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_queue,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_plan,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_ledger = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_ledger(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_plan
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_checks(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_plan,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_ledger,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_matrix = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_matrix(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_ledger
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_checks(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_ledger,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_matrix,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_queue = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_queue(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_matrix
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_checks(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_matrix,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_queue,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_queue
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_checks(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_queue,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan,
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_execution_ledger = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_execution_ledger(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan
        )
    )
    ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_execution_checks = (
        _build_ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_execution_checks(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan,
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_execution_ledger,
        )
    )
    ontological_soundness_resolution_worklist = _build_ontological_soundness_resolution_worklist(
        ontological_soundness_checks
    )
    ontological_soundness_resolution_worklist_checks = _build_ontological_soundness_resolution_worklist_checks(
        ontological_soundness_checks,
        ontological_soundness_resolution_worklist,
    )
    ontological_soundness_resolution_batches = _build_ontological_soundness_resolution_batches(
        ontological_soundness_resolution_worklist
    )
    ontological_soundness_resolution_batch_checks = _build_ontological_soundness_resolution_batch_checks(
        ontological_soundness_resolution_worklist,
        ontological_soundness_resolution_batches,
    )
    ontological_soundness_batch_execution_ledger = _build_ontological_soundness_batch_execution_ledger(
        ontological_soundness_resolution_batches
    )
    ontological_soundness_batch_execution_checks = _build_ontological_soundness_batch_execution_checks(
        ontological_soundness_resolution_batches,
        ontological_soundness_batch_execution_ledger,
    )
    teleological_bayes_model = _build_teleological_bayes_model()
    teleological_bayes_checks = _build_teleological_bayes_checks()
    cosmological_psr_model = _build_cosmological_psr_model()
    cosmological_psr_checks = _build_cosmological_psr_checks()
    evil_hiddenness_constraints = _build_evil_hiddenness_constraints()
    evil_hiddenness_checks = _build_evil_hiddenness_checks()
    coverage_matrix = _build_coverage_matrix()
    human_wisdom_primary_source_seed_ledger = _build_human_wisdom_primary_source_seed_ledger()
    human_wisdom_primary_source_extraction_queue = _build_human_wisdom_primary_source_extraction_queue()
    human_wisdom_primary_source_summary_candidates = _build_human_wisdom_primary_source_summary_candidates()
    human_wisdom_counterpressure_edge_proposals = _build_human_wisdom_counterpressure_edge_proposals()
    human_wisdom_counterpressure_edge_checks = _build_human_wisdom_counterpressure_edge_checks()
    human_wisdom_counterpressure_edge_review_queue = _build_human_wisdom_counterpressure_edge_review_queue()
    human_wisdom_counterpressure_edge_review_checks = _build_human_wisdom_counterpressure_edge_review_checks()
    human_wisdom_counterpressure_edge_review_rubric = _build_human_wisdom_counterpressure_edge_review_rubric()
    human_wisdom_counterpressure_edge_review_rubric_checks = (
        _build_human_wisdom_counterpressure_edge_review_rubric_checks()
    )
    human_wisdom_counterpressure_edge_review_decisions = _build_human_wisdom_counterpressure_edge_review_decisions()
    human_wisdom_counterpressure_edge_review_decision_checks = (
        _build_human_wisdom_counterpressure_edge_review_decision_checks()
    )
    human_wisdom_counterpressure_edge_resolution_packet = _build_human_wisdom_counterpressure_edge_resolution_packet()
    human_wisdom_counterpressure_edge_resolution_checks = _build_human_wisdom_counterpressure_edge_resolution_checks()
    human_wisdom_counterpressure_edge_evidence_request_queue = (
        _build_human_wisdom_counterpressure_edge_evidence_request_queue()
    )
    human_wisdom_counterpressure_edge_evidence_request_checks = (
        _build_human_wisdom_counterpressure_edge_evidence_request_checks()
    )
    human_wisdom_counterpressure_edge_evidence_acquisition_manifest = (
        _build_human_wisdom_counterpressure_edge_evidence_acquisition_manifest()
    )
    human_wisdom_counterpressure_edge_evidence_acquisition_checks = (
        _build_human_wisdom_counterpressure_edge_evidence_acquisition_checks()
    )
    human_wisdom_counterpressure_edge_metadata_receipt_schema = (
        _build_human_wisdom_counterpressure_edge_metadata_receipt_schema()
    )
    human_wisdom_counterpressure_edge_metadata_receipt_checks = (
        _build_human_wisdom_counterpressure_edge_metadata_receipt_checks()
    )
    human_wisdom_counterpressure_edge_metadata_receipt_review_queue = (
        _build_human_wisdom_counterpressure_edge_metadata_receipt_review_queue()
    )
    human_wisdom_counterpressure_edge_metadata_receipt_review_checks = (
        _build_human_wisdom_counterpressure_edge_metadata_receipt_review_checks()
    )
    human_wisdom_counterpressure_edge_metadata_receipt_review_rubric = (
        _build_human_wisdom_counterpressure_edge_metadata_receipt_review_rubric()
    )
    human_wisdom_counterpressure_edge_metadata_receipt_review_rubric_checks = (
        _build_human_wisdom_counterpressure_edge_metadata_receipt_review_rubric_checks()
    )
    human_wisdom_counterpressure_edge_metadata_receipt_review_decisions = (
        _build_human_wisdom_counterpressure_edge_metadata_receipt_review_decisions()
    )
    human_wisdom_counterpressure_edge_metadata_receipt_review_decision_checks = (
        _build_human_wisdom_counterpressure_edge_metadata_receipt_review_decision_checks()
    )
    human_wisdom_counterpressure_edge_metadata_receipt_resolution_packet = (
        _build_human_wisdom_counterpressure_edge_metadata_receipt_resolution_packet()
    )
    human_wisdom_counterpressure_edge_metadata_receipt_resolution_checks = (
        _build_human_wisdom_counterpressure_edge_metadata_receipt_resolution_checks()
    )
    human_wisdom_counterpressure_edge_metadata_receipt_evidence_request_queue = (
        _build_human_wisdom_counterpressure_edge_metadata_receipt_evidence_request_queue()
    )
    human_wisdom_counterpressure_edge_metadata_receipt_evidence_request_checks = (
        _build_human_wisdom_counterpressure_edge_metadata_receipt_evidence_request_checks()
    )
    human_wisdom_counterpressure_edge_metadata_receipt_acquisition_manifest = (
        _build_human_wisdom_counterpressure_edge_metadata_receipt_acquisition_manifest()
    )
    human_wisdom_counterpressure_edge_metadata_receipt_acquisition_checks = (
        _build_human_wisdom_counterpressure_edge_metadata_receipt_acquisition_checks()
    )
    human_wisdom_counterpressure_edge_metadata_receipt_acquisition_hash_runbook = (
        _build_human_wisdom_counterpressure_edge_metadata_receipt_acquisition_hash_runbook()
    )
    human_wisdom_counterpressure_edge_metadata_receipt_acquisition_hash_runbook_checks = (
        _build_human_wisdom_counterpressure_edge_metadata_receipt_acquisition_hash_runbook_checks()
    )
    human_wisdom_counterpressure_edge_metadata_receipt_authorization_packet = (
        _build_human_wisdom_counterpressure_edge_metadata_receipt_authorization_packet()
    )
    human_wisdom_counterpressure_edge_metadata_receipt_authorization_checks = (
        _build_human_wisdom_counterpressure_edge_metadata_receipt_authorization_checks()
    )
    human_wisdom_counterpressure_edge_metadata_receipt_authorization_review_queue = (
        _build_human_wisdom_counterpressure_edge_metadata_receipt_authorization_review_queue()
    )
    human_wisdom_counterpressure_edge_metadata_receipt_authorization_review_checks = (
        _build_human_wisdom_counterpressure_edge_metadata_receipt_authorization_review_checks()
    )
    human_wisdom_primary_source_summary_candidate_checks = (
        _build_human_wisdom_primary_source_summary_candidate_checks(human_wisdom_counterpressure_edge_checks)
    )
    human_wisdom_primary_source_extraction_checks = _build_human_wisdom_primary_source_extraction_checks(
        human_wisdom_primary_source_summary_candidate_checks
    )
    human_wisdom_primary_source_seed_checks = _build_human_wisdom_primary_source_seed_checks(
        human_wisdom_primary_source_extraction_checks
    )
    human_wisdom_intake_roadmap = _build_human_wisdom_intake_roadmap()
    human_wisdom_intake_checks = _build_human_wisdom_intake_checks(
        coverage_matrix,
        human_wisdom_primary_source_seed_checks,
    )
    proof_graph = _build_proof_graph()
    proof_readiness = _build_proof_readiness(
        coverage_matrix,
        definition_checks,
        modal_validity_checks,
        modal_consistency_checks,
        teleological_bayes_checks,
        cosmological_psr_checks,
        evil_hiddenness_checks,
        ontological_soundness_checks,
    )
    frontier = _build_frontier(
        coverage_matrix,
        definition_checks,
        modal_validity_checks,
        modal_consistency_checks,
        teleological_bayes_checks,
        cosmological_psr_checks,
        evil_hiddenness_checks,
        ontological_soundness_checks,
    )

    _write_json(session_dir / "wisdom-map.json", wisdom_map)
    log("wisdom_map_written", {
        "arguments": len(ARGUMENTS),
        "premises": len(PREMISES),
        "target_concepts": len(TARGET_CONCEPTS),
        "wisdom_entries": len(WISDOM_CORPUS),
        "proof_obligations": len(PROOF_OBLIGATIONS),
    })
    _write_json(session_dir / "target-concepts.json", target_concepts)
    log("target_concepts_written", {
        "concepts": len(TARGET_CONCEPTS),
        "proof_target_id": TARGET_PROOF_CONCEPT_ID,
    })
    _write_json(session_dir / "definition-checks.json", definition_checks)
    log("definition_checks_written", {
        "status": definition_checks["status"],
        "target_concept_id": definition_checks["target_concept_id"],
    })
    _write_json(session_dir / "wisdom-corpus.json", {
        "status": "partial_human_wisdom_corpus",
        "entries": [entry.as_dict() for entry in WISDOM_CORPUS],
    })
    log("wisdom_corpus_written", {"entries": len(WISDOM_CORPUS)})
    _write_json(session_dir / "coverage-matrix.json", coverage_matrix)
    log("coverage_matrix_written", {
        "status": coverage_matrix["status"],
        "coverage_score": coverage_matrix["coverage_score"],
        "missing_domains": coverage_matrix["missing_domains"],
        "thin_domains": coverage_matrix["thin_domains"],
    })
    _write_json(
        session_dir / "human-wisdom-primary-source-seed-ledger.json",
        human_wisdom_primary_source_seed_ledger,
    )
    log("human_wisdom_primary_source_seed_ledger_written", {
        "status": human_wisdom_primary_source_seed_ledger["status"],
        "ledger_id": HUMAN_WISDOM_PRIMARY_SOURCE_SEED_LEDGER["id"],
    })
    _write_json(
        session_dir / "human-wisdom-primary-source-extraction-queue.json",
        human_wisdom_primary_source_extraction_queue,
    )
    log("human_wisdom_primary_source_extraction_queue_written", {
        "status": human_wisdom_primary_source_extraction_queue["status"],
        "queue_id": HUMAN_WISDOM_PRIMARY_SOURCE_EXTRACTION_QUEUE["id"],
    })
    _write_json(
        session_dir / "human-wisdom-primary-source-summary-candidates.json",
        human_wisdom_primary_source_summary_candidates,
    )
    log("human_wisdom_primary_source_summary_candidates_written", {
        "status": human_wisdom_primary_source_summary_candidates["status"],
        "candidate_id": HUMAN_WISDOM_PRIMARY_SOURCE_SUMMARY_CANDIDATES["id"],
    })
    _write_json(
        session_dir / "human-wisdom-primary-source-summary-candidate-checks.json",
        human_wisdom_primary_source_summary_candidate_checks,
    )
    log("human_wisdom_primary_source_summary_candidate_checks_written", {
        "status": human_wisdom_primary_source_summary_candidate_checks["status"],
        "target_concept_id": human_wisdom_primary_source_summary_candidate_checks["target_concept_id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-proposals.json",
        human_wisdom_counterpressure_edge_proposals,
    )
    log("human_wisdom_counterpressure_edge_proposals_written", {
        "status": human_wisdom_counterpressure_edge_proposals["status"],
        "proposal_id": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_PROPOSALS["id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-checks.json",
        human_wisdom_counterpressure_edge_checks,
    )
    log("human_wisdom_counterpressure_edge_checks_written", {
        "status": human_wisdom_counterpressure_edge_checks["status"],
        "target_concept_id": human_wisdom_counterpressure_edge_checks["target_concept_id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-review-queue.json",
        human_wisdom_counterpressure_edge_review_queue,
    )
    log("human_wisdom_counterpressure_edge_review_queue_written", {
        "status": human_wisdom_counterpressure_edge_review_queue["status"],
        "queue_id": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_REVIEW_QUEUE["id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-review-checks.json",
        human_wisdom_counterpressure_edge_review_checks,
    )
    log("human_wisdom_counterpressure_edge_review_checks_written", {
        "status": human_wisdom_counterpressure_edge_review_checks["status"],
        "target_concept_id": human_wisdom_counterpressure_edge_review_checks["target_concept_id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-review-rubric.json",
        human_wisdom_counterpressure_edge_review_rubric,
    )
    log("human_wisdom_counterpressure_edge_review_rubric_written", {
        "status": human_wisdom_counterpressure_edge_review_rubric["status"],
        "rubric_id": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_REVIEW_RUBRIC["id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-review-rubric-checks.json",
        human_wisdom_counterpressure_edge_review_rubric_checks,
    )
    log("human_wisdom_counterpressure_edge_review_rubric_checks_written", {
        "status": human_wisdom_counterpressure_edge_review_rubric_checks["status"],
        "target_concept_id": human_wisdom_counterpressure_edge_review_rubric_checks["target_concept_id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-review-decisions.json",
        human_wisdom_counterpressure_edge_review_decisions,
    )
    log("human_wisdom_counterpressure_edge_review_decisions_written", {
        "status": human_wisdom_counterpressure_edge_review_decisions["status"],
        "decision_id": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_REVIEW_DECISIONS["id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-review-decision-checks.json",
        human_wisdom_counterpressure_edge_review_decision_checks,
    )
    log("human_wisdom_counterpressure_edge_review_decision_checks_written", {
        "status": human_wisdom_counterpressure_edge_review_decision_checks["status"],
        "target_concept_id": human_wisdom_counterpressure_edge_review_decision_checks["target_concept_id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-resolution-packet.json",
        human_wisdom_counterpressure_edge_resolution_packet,
    )
    log("human_wisdom_counterpressure_edge_resolution_packet_written", {
        "status": human_wisdom_counterpressure_edge_resolution_packet["status"],
        "packet_id": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_RESOLUTION_PACKET["id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-resolution-checks.json",
        human_wisdom_counterpressure_edge_resolution_checks,
    )
    log("human_wisdom_counterpressure_edge_resolution_checks_written", {
        "status": human_wisdom_counterpressure_edge_resolution_checks["status"],
        "target_concept_id": human_wisdom_counterpressure_edge_resolution_checks["target_concept_id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-evidence-request-queue.json",
        human_wisdom_counterpressure_edge_evidence_request_queue,
    )
    log("human_wisdom_counterpressure_edge_evidence_request_queue_written", {
        "status": human_wisdom_counterpressure_edge_evidence_request_queue["status"],
        "queue_id": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_EVIDENCE_REQUEST_QUEUE["id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-evidence-request-checks.json",
        human_wisdom_counterpressure_edge_evidence_request_checks,
    )
    log("human_wisdom_counterpressure_edge_evidence_request_checks_written", {
        "status": human_wisdom_counterpressure_edge_evidence_request_checks["status"],
        "target_concept_id": human_wisdom_counterpressure_edge_evidence_request_checks["target_concept_id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-evidence-acquisition-manifest.json",
        human_wisdom_counterpressure_edge_evidence_acquisition_manifest,
    )
    log("human_wisdom_counterpressure_edge_evidence_acquisition_manifest_written", {
        "status": human_wisdom_counterpressure_edge_evidence_acquisition_manifest["status"],
        "manifest_id": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_EVIDENCE_ACQUISITION_MANIFEST["id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-evidence-acquisition-checks.json",
        human_wisdom_counterpressure_edge_evidence_acquisition_checks,
    )
    log("human_wisdom_counterpressure_edge_evidence_acquisition_checks_written", {
        "status": human_wisdom_counterpressure_edge_evidence_acquisition_checks["status"],
        "target_concept_id": human_wisdom_counterpressure_edge_evidence_acquisition_checks["target_concept_id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-schema.json",
        human_wisdom_counterpressure_edge_metadata_receipt_schema,
    )
    log("human_wisdom_counterpressure_edge_metadata_receipt_schema_written", {
        "status": human_wisdom_counterpressure_edge_metadata_receipt_schema["status"],
        "schema_id": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_SCHEMA["id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-checks.json",
        human_wisdom_counterpressure_edge_metadata_receipt_checks,
    )
    log("human_wisdom_counterpressure_edge_metadata_receipt_checks_written", {
        "status": human_wisdom_counterpressure_edge_metadata_receipt_checks["status"],
        "target_concept_id": human_wisdom_counterpressure_edge_metadata_receipt_checks["target_concept_id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-review-queue.json",
        human_wisdom_counterpressure_edge_metadata_receipt_review_queue,
    )
    log("human_wisdom_counterpressure_edge_metadata_receipt_review_queue_written", {
        "status": human_wisdom_counterpressure_edge_metadata_receipt_review_queue["status"],
        "queue_id": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_REVIEW_QUEUE["id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-review-checks.json",
        human_wisdom_counterpressure_edge_metadata_receipt_review_checks,
    )
    log("human_wisdom_counterpressure_edge_metadata_receipt_review_checks_written", {
        "status": human_wisdom_counterpressure_edge_metadata_receipt_review_checks["status"],
        "target_concept_id": human_wisdom_counterpressure_edge_metadata_receipt_review_checks["target_concept_id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-review-rubric.json",
        human_wisdom_counterpressure_edge_metadata_receipt_review_rubric,
    )
    log("human_wisdom_counterpressure_edge_metadata_receipt_review_rubric_written", {
        "status": human_wisdom_counterpressure_edge_metadata_receipt_review_rubric["status"],
        "rubric_id": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_REVIEW_RUBRIC["id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-review-rubric-checks.json",
        human_wisdom_counterpressure_edge_metadata_receipt_review_rubric_checks,
    )
    log("human_wisdom_counterpressure_edge_metadata_receipt_review_rubric_checks_written", {
        "status": human_wisdom_counterpressure_edge_metadata_receipt_review_rubric_checks["status"],
        "target_concept_id": human_wisdom_counterpressure_edge_metadata_receipt_review_rubric_checks[
            "target_concept_id"
        ],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-review-decisions.json",
        human_wisdom_counterpressure_edge_metadata_receipt_review_decisions,
    )
    log("human_wisdom_counterpressure_edge_metadata_receipt_review_decisions_written", {
        "status": human_wisdom_counterpressure_edge_metadata_receipt_review_decisions["status"],
        "decision_id": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_REVIEW_DECISIONS["id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-review-decision-checks.json",
        human_wisdom_counterpressure_edge_metadata_receipt_review_decision_checks,
    )
    log("human_wisdom_counterpressure_edge_metadata_receipt_review_decision_checks_written", {
        "status": human_wisdom_counterpressure_edge_metadata_receipt_review_decision_checks["status"],
        "target_concept_id": human_wisdom_counterpressure_edge_metadata_receipt_review_decision_checks[
            "target_concept_id"
        ],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-resolution-packet.json",
        human_wisdom_counterpressure_edge_metadata_receipt_resolution_packet,
    )
    log("human_wisdom_counterpressure_edge_metadata_receipt_resolution_packet_written", {
        "status": human_wisdom_counterpressure_edge_metadata_receipt_resolution_packet["status"],
        "packet_id": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_RESOLUTION_PACKET["id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-resolution-checks.json",
        human_wisdom_counterpressure_edge_metadata_receipt_resolution_checks,
    )
    log("human_wisdom_counterpressure_edge_metadata_receipt_resolution_checks_written", {
        "status": human_wisdom_counterpressure_edge_metadata_receipt_resolution_checks["status"],
        "target_concept_id": human_wisdom_counterpressure_edge_metadata_receipt_resolution_checks[
            "target_concept_id"
        ],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-evidence-request-queue.json",
        human_wisdom_counterpressure_edge_metadata_receipt_evidence_request_queue,
    )
    log("human_wisdom_counterpressure_edge_metadata_receipt_evidence_request_queue_written", {
        "status": human_wisdom_counterpressure_edge_metadata_receipt_evidence_request_queue["status"],
        "queue_id": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_EVIDENCE_REQUEST_QUEUE["id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-evidence-request-checks.json",
        human_wisdom_counterpressure_edge_metadata_receipt_evidence_request_checks,
    )
    log("human_wisdom_counterpressure_edge_metadata_receipt_evidence_request_checks_written", {
        "status": human_wisdom_counterpressure_edge_metadata_receipt_evidence_request_checks["status"],
        "target_concept_id": human_wisdom_counterpressure_edge_metadata_receipt_evidence_request_checks[
            "target_concept_id"
        ],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-acquisition-manifest.json",
        human_wisdom_counterpressure_edge_metadata_receipt_acquisition_manifest,
    )
    log("human_wisdom_counterpressure_edge_metadata_receipt_acquisition_manifest_written", {
        "status": human_wisdom_counterpressure_edge_metadata_receipt_acquisition_manifest["status"],
        "manifest_id": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_ACQUISITION_MANIFEST["id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-acquisition-checks.json",
        human_wisdom_counterpressure_edge_metadata_receipt_acquisition_checks,
    )
    log("human_wisdom_counterpressure_edge_metadata_receipt_acquisition_checks_written", {
        "status": human_wisdom_counterpressure_edge_metadata_receipt_acquisition_checks["status"],
        "target_concept_id": human_wisdom_counterpressure_edge_metadata_receipt_acquisition_checks[
            "target_concept_id"
        ],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-acquisition-hash-runbook.json",
        human_wisdom_counterpressure_edge_metadata_receipt_acquisition_hash_runbook,
    )
    log("human_wisdom_counterpressure_edge_metadata_receipt_acquisition_hash_runbook_written", {
        "status": human_wisdom_counterpressure_edge_metadata_receipt_acquisition_hash_runbook["status"],
        "runbook_id": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_ACQUISITION_HASH_RUNBOOK["id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-acquisition-hash-runbook-checks.json",
        human_wisdom_counterpressure_edge_metadata_receipt_acquisition_hash_runbook_checks,
    )
    log("human_wisdom_counterpressure_edge_metadata_receipt_acquisition_hash_runbook_checks_written", {
        "status": human_wisdom_counterpressure_edge_metadata_receipt_acquisition_hash_runbook_checks["status"],
        "target_concept_id": human_wisdom_counterpressure_edge_metadata_receipt_acquisition_hash_runbook_checks[
            "target_concept_id"
        ],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-authorization-packet.json",
        human_wisdom_counterpressure_edge_metadata_receipt_authorization_packet,
    )
    log("human_wisdom_counterpressure_edge_metadata_receipt_authorization_packet_written", {
        "status": human_wisdom_counterpressure_edge_metadata_receipt_authorization_packet["status"],
        "packet_id": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_AUTHORIZATION_PACKET["id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-authorization-checks.json",
        human_wisdom_counterpressure_edge_metadata_receipt_authorization_checks,
    )
    log("human_wisdom_counterpressure_edge_metadata_receipt_authorization_checks_written", {
        "status": human_wisdom_counterpressure_edge_metadata_receipt_authorization_checks["status"],
        "target_concept_id": human_wisdom_counterpressure_edge_metadata_receipt_authorization_checks[
            "target_concept_id"
        ],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-authorization-review-queue.json",
        human_wisdom_counterpressure_edge_metadata_receipt_authorization_review_queue,
    )
    log("human_wisdom_counterpressure_edge_metadata_receipt_authorization_review_queue_written", {
        "status": human_wisdom_counterpressure_edge_metadata_receipt_authorization_review_queue["status"],
        "queue_id": HUMAN_WISDOM_COUNTERPRESSURE_EDGE_METADATA_RECEIPT_AUTHORIZATION_REVIEW_QUEUE["id"],
    })
    _write_json(
        session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-authorization-review-checks.json",
        human_wisdom_counterpressure_edge_metadata_receipt_authorization_review_checks,
    )
    log("human_wisdom_counterpressure_edge_metadata_receipt_authorization_review_checks_written", {
        "status": human_wisdom_counterpressure_edge_metadata_receipt_authorization_review_checks["status"],
        "target_concept_id": human_wisdom_counterpressure_edge_metadata_receipt_authorization_review_checks[
            "target_concept_id"
        ],
    })
    _write_json(
        session_dir / "human-wisdom-primary-source-extraction-checks.json",
        human_wisdom_primary_source_extraction_checks,
    )
    log("human_wisdom_primary_source_extraction_checks_written", {
        "status": human_wisdom_primary_source_extraction_checks["status"],
        "target_concept_id": human_wisdom_primary_source_extraction_checks["target_concept_id"],
    })
    _write_json(
        session_dir / "human-wisdom-primary-source-seed-checks.json",
        human_wisdom_primary_source_seed_checks,
    )
    log("human_wisdom_primary_source_seed_checks_written", {
        "status": human_wisdom_primary_source_seed_checks["status"],
        "target_concept_id": human_wisdom_primary_source_seed_checks["target_concept_id"],
    })
    _write_json(session_dir / "human-wisdom-intake-roadmap.json", human_wisdom_intake_roadmap)
    log("human_wisdom_intake_roadmap_written", {
        "status": human_wisdom_intake_roadmap["status"],
        "roadmap_id": HUMAN_WISDOM_INTAKE_ROADMAP["id"],
    })
    _write_json(session_dir / "human-wisdom-intake-checks.json", human_wisdom_intake_checks)
    log("human_wisdom_intake_checks_written", {
        "status": human_wisdom_intake_checks["status"],
        "target_concept_id": human_wisdom_intake_checks["target_concept_id"],
    })
    _write_json(session_dir / "proof-graph.json", proof_graph)
    log("proof_graph_written", {"nodes": len(proof_graph["nodes"]), "edges": len(proof_graph["edges"])})
    _write_json(session_dir / "modal-derivation.json", modal_derivation)
    log("modal_derivation_written", {
        "argument_id": MODAL_DERIVATION["argument_id"],
        "steps": len(MODAL_DERIVATION["steps"]),
    })
    _write_json(session_dir / "modal-validity-checks.json", modal_validity_checks)
    log("modal_validity_checks_written", {
        "status": modal_validity_checks["status"],
        "argument_id": modal_validity_checks["argument_id"],
    })
    _write_json(session_dir / "modal-consistency-checks.json", modal_consistency_checks)
    log("modal_consistency_checks_written", {
        "status": modal_consistency_checks["status"],
        "argument_id": modal_consistency_checks["argument_id"],
        "model_id": modal_consistency_checks["model"]["id"],
    })
    _write_json(session_dir / "ontological-soundness-dossier.json", ontological_soundness_dossier)
    log("ontological_soundness_dossier_written", {
        "status": ontological_soundness_dossier["status"],
        "dossier_id": ONTOLOGICAL_SOUNDNESS_DOSSIER["id"],
    })
    _write_json(session_dir / "ontological-soundness-checks.json", ontological_soundness_checks)
    log("ontological_soundness_checks_written", {
        "status": ontological_soundness_checks["status"],
        "argument_id": ontological_soundness_checks["argument_id"],
    })
    _write_json(
        session_dir / "ontological-soundness-parody-discriminator-matrix.json",
        ontological_soundness_parody_discriminator_matrix,
    )
    log("ontological_soundness_parody_discriminator_matrix_written", {
        "status": ontological_soundness_parody_discriminator_matrix["status"],
        "row_count": len(ontological_soundness_parody_discriminator_matrix["matrix"]["discriminator_rows"]),
    })
    _write_json(
        session_dir / "ontological-soundness-parody-discriminator-checks.json",
        ontological_soundness_parody_discriminator_checks,
    )
    log("ontological_soundness_parody_discriminator_checks_written", {
        "status": ontological_soundness_parody_discriminator_checks["status"],
        "target_obligation_id": ontological_soundness_parody_discriminator_checks["target_obligation_id"],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-discharge-criteria.json",
        ontological_soundness_bad_god_discharge_criteria,
    )
    log("ontological_soundness_bad_god_discharge_criteria_written", {
        "status": ontological_soundness_bad_god_discharge_criteria["status"],
        "requirement_count": len(
            ontological_soundness_bad_god_discharge_criteria["criteria"]["discharge_requirements"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-discharge-checks.json",
        ontological_soundness_bad_god_discharge_checks,
    )
    log("ontological_soundness_bad_god_discharge_checks_written", {
        "status": ontological_soundness_bad_god_discharge_checks["status"],
        "target_parody_test_id": ontological_soundness_bad_god_discharge_checks["target_parody_test_id"],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-discharge-task-queue.json",
        ontological_soundness_bad_god_discharge_task_queue,
    )
    log("ontological_soundness_bad_god_discharge_task_queue_written", {
        "status": ontological_soundness_bad_god_discharge_task_queue["status"],
        "task_count": len(ontological_soundness_bad_god_discharge_task_queue["queue"]["task_items"]),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-discharge-task-checks.json",
        ontological_soundness_bad_god_discharge_task_checks,
    )
    log("ontological_soundness_bad_god_discharge_task_checks_written", {
        "status": ontological_soundness_bad_god_discharge_task_checks["status"],
        "target_parody_test_id": ontological_soundness_bad_god_discharge_task_checks["target_parody_test_id"],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-task-dependency-graph.json",
        ontological_soundness_bad_god_task_dependency_graph,
    )
    log("ontological_soundness_bad_god_task_dependency_graph_written", {
        "status": ontological_soundness_bad_god_task_dependency_graph["status"],
        "edge_count": len(ontological_soundness_bad_god_task_dependency_graph["graph"]["edges"]),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-task-dependency-checks.json",
        ontological_soundness_bad_god_task_dependency_checks,
    )
    log("ontological_soundness_bad_god_task_dependency_checks_written", {
        "status": ontological_soundness_bad_god_task_dependency_checks["status"],
        "target_parody_test_id": ontological_soundness_bad_god_task_dependency_checks["target_parody_test_id"],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evil-hiddenness-pressure-matrix.json",
        ontological_soundness_bad_god_evil_hiddenness_pressure_matrix,
    )
    log("ontological_soundness_bad_god_evil_hiddenness_pressure_matrix_written", {
        "status": ontological_soundness_bad_god_evil_hiddenness_pressure_matrix["status"],
        "pressure_count": len(
            ontological_soundness_bad_god_evil_hiddenness_pressure_matrix["matrix"]["pressure_rows"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evil-hiddenness-pressure-checks.json",
        ontological_soundness_bad_god_evil_hiddenness_pressure_checks,
    )
    log("ontological_soundness_bad_god_evil_hiddenness_pressure_checks_written", {
        "status": ontological_soundness_bad_god_evil_hiddenness_pressure_checks["status"],
        "target_task_id": ontological_soundness_bad_god_evil_hiddenness_pressure_checks["target_task_id"],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evil-hiddenness-sufficiency-task-queue.json",
        ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_queue,
    )
    log("ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_queue_written", {
        "status": ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_queue["status"],
        "task_count": len(
            ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_queue["queue"]["task_items"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evil-hiddenness-sufficiency-task-checks.json",
        ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_checks,
    )
    log("ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_checks_written", {
        "status": ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_checks["status"],
        "target_task_id": (
            ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_checks["target_task_id"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-probability-pressure-task-scaffold.json",
        ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold,
    )
    log("ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold_written", {
        "status": ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold["status"],
        "target_task_id": (
            ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold["scaffold"][
                "target_task_id"
            ]
        ),
        "lane_count": len(
            ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold["scaffold"][
                "evaluation_lanes"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-probability-pressure-task-checks.json",
        ontological_soundness_bad_god_evidential_probability_pressure_task_checks,
    )
    log("ontological_soundness_bad_god_evidential_probability_pressure_task_checks_written", {
        "status": ontological_soundness_bad_god_evidential_probability_pressure_task_checks["status"],
        "target_task_id": ontological_soundness_bad_god_evidential_probability_pressure_task_checks[
            "target_task_id"
        ],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-prior-sensitivity-grid.json",
        ontological_soundness_bad_god_evidential_prior_sensitivity_grid,
    )
    log("ontological_soundness_bad_god_evidential_prior_sensitivity_grid_written", {
        "status": ontological_soundness_bad_god_evidential_prior_sensitivity_grid["status"],
        "target_lane_id": ontological_soundness_bad_god_evidential_prior_sensitivity_grid["grid"][
            "target_lane_id"
        ],
        "profile_count": len(
            ontological_soundness_bad_god_evidential_prior_sensitivity_grid["grid"][
                "normalized_prior_profiles"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-prior-sensitivity-checks.json",
        ontological_soundness_bad_god_evidential_prior_sensitivity_checks,
    )
    log("ontological_soundness_bad_god_evidential_prior_sensitivity_checks_written", {
        "status": ontological_soundness_bad_god_evidential_prior_sensitivity_checks["status"],
        "target_requirement_id": ontological_soundness_bad_god_evidential_prior_sensitivity_checks[
            "target_requirement_id"
        ],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-likelihood-sensitivity-grid.json",
        ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid,
    )
    log("ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid_written", {
        "status": ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid["status"],
        "target_lane_id": ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid["grid"][
            "target_lane_id"
        ],
        "likelihood_cell_count": len(
            ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid["grid"][
                "likelihood_cells"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-likelihood-sensitivity-checks.json",
        ontological_soundness_bad_god_evidential_likelihood_sensitivity_checks,
    )
    log("ontological_soundness_bad_god_evidential_likelihood_sensitivity_checks_written", {
        "status": ontological_soundness_bad_god_evidential_likelihood_sensitivity_checks["status"],
        "target_requirement_id": ontological_soundness_bad_god_evidential_likelihood_sensitivity_checks[
            "target_requirement_id"
        ],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-response-cost-grid.json",
        ontological_soundness_bad_god_evidential_response_cost_grid,
    )
    log("ontological_soundness_bad_god_evidential_response_cost_grid_written", {
        "status": ontological_soundness_bad_god_evidential_response_cost_grid["status"],
        "target_lane_id": ontological_soundness_bad_god_evidential_response_cost_grid["grid"][
            "target_lane_id"
        ],
        "response_cost_count": len(
            ontological_soundness_bad_god_evidential_response_cost_grid["grid"]["response_cost_rows"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-response-cost-checks.json",
        ontological_soundness_bad_god_evidential_response_cost_checks,
    )
    log("ontological_soundness_bad_god_evidential_response_cost_checks_written", {
        "status": ontological_soundness_bad_god_evidential_response_cost_checks["status"],
        "target_requirement_id": ontological_soundness_bad_god_evidential_response_cost_checks[
            "target_requirement_id"
        ],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-rival-comparison-grid.json",
        ontological_soundness_bad_god_evidential_rival_comparison_grid,
    )
    log("ontological_soundness_bad_god_evidential_rival_comparison_grid_written", {
        "status": ontological_soundness_bad_god_evidential_rival_comparison_grid["status"],
        "target_lane_id": ontological_soundness_bad_god_evidential_rival_comparison_grid["grid"][
            "target_lane_id"
        ],
        "rival_likelihood_count": len(
            ontological_soundness_bad_god_evidential_rival_comparison_grid["grid"]["rival_likelihood_rows"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-rival-comparison-checks.json",
        ontological_soundness_bad_god_evidential_rival_comparison_checks,
    )
    log("ontological_soundness_bad_god_evidential_rival_comparison_checks_written", {
        "status": ontological_soundness_bad_god_evidential_rival_comparison_checks["status"],
        "target_requirement_id": ontological_soundness_bad_god_evidential_rival_comparison_checks[
            "target_requirement_id"
        ],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-probability-execution-packet.json",
        ontological_soundness_bad_god_evidential_probability_execution_packet,
    )
    log("ontological_soundness_bad_god_evidential_probability_execution_packet_written", {
        "status": ontological_soundness_bad_god_evidential_probability_execution_packet["status"],
        "target_task_id": ontological_soundness_bad_god_evidential_probability_execution_packet["packet"][
            "target_task_id"
        ],
        "step_count": len(
            ontological_soundness_bad_god_evidential_probability_execution_packet["packet"]["execution_steps"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-probability-execution-checks.json",
        ontological_soundness_bad_god_evidential_probability_execution_checks,
    )
    log("ontological_soundness_bad_god_evidential_probability_execution_checks_written", {
        "status": ontological_soundness_bad_god_evidential_probability_execution_checks["status"],
        "target_task_id": ontological_soundness_bad_god_evidential_probability_execution_checks[
            "target_task_id"
        ],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-posterior-projection-results.json",
        ontological_soundness_bad_god_evidential_posterior_projection_results,
    )
    log("ontological_soundness_bad_god_evidential_posterior_projection_results_written", {
        "status": ontological_soundness_bad_god_evidential_posterior_projection_results["status"],
        "projection_count": len(
            ontological_soundness_bad_god_evidential_posterior_projection_results["results"][
                "projection_results"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-posterior-projection-checks.json",
        ontological_soundness_bad_god_evidential_posterior_projection_checks,
    )
    log("ontological_soundness_bad_god_evidential_posterior_projection_checks_written", {
        "status": ontological_soundness_bad_god_evidential_posterior_projection_checks["status"],
        "target_task_id": ontological_soundness_bad_god_evidential_posterior_projection_checks[
            "target_task_id"
        ],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-projection-outcome-review.json",
        ontological_soundness_bad_god_evidential_projection_outcome_review,
    )
    log("ontological_soundness_bad_god_evidential_projection_outcome_review_written", {
        "status": ontological_soundness_bad_god_evidential_projection_outcome_review["status"],
        "top_hypothesis_tally": ontological_soundness_bad_god_evidential_projection_outcome_review[
            "review"
        ]["top_hypothesis_tally"],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-projection-outcome-checks.json",
        ontological_soundness_bad_god_evidential_projection_outcome_checks,
    )
    log("ontological_soundness_bad_god_evidential_projection_outcome_checks_written", {
        "status": ontological_soundness_bad_god_evidential_projection_outcome_checks["status"],
        "target_task_id": ontological_soundness_bad_god_evidential_projection_outcome_checks[
            "target_task_id"
        ],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-projection-remediation-plan.json",
        ontological_soundness_bad_god_evidential_projection_remediation_plan,
    )
    log("ontological_soundness_bad_god_evidential_projection_remediation_plan_written", {
        "status": ontological_soundness_bad_god_evidential_projection_remediation_plan["status"],
        "remediation_count": len(
            ontological_soundness_bad_god_evidential_projection_remediation_plan["plan"][
                "remediation_items"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-projection-remediation-checks.json",
        ontological_soundness_bad_god_evidential_projection_remediation_checks,
    )
    log("ontological_soundness_bad_god_evidential_projection_remediation_checks_written", {
        "status": ontological_soundness_bad_god_evidential_projection_remediation_checks["status"],
        "target_task_id": ontological_soundness_bad_god_evidential_projection_remediation_checks[
            "target_task_id"
        ],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-registry.json",
        ontological_soundness_bad_god_evidential_calibration_source_registry,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_registry_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_registry["status"],
        "source_family_count": len(
            ontological_soundness_bad_god_evidential_calibration_source_registry["registry"][
                "source_families"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_checks_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_checks["status"],
        "target_task_id": ontological_soundness_bad_god_evidential_calibration_source_checks[
            "target_task_id"
        ],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-acquisition-manifest.json",
        ontological_soundness_bad_god_evidential_calibration_source_acquisition_manifest,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_acquisition_manifest_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_acquisition_manifest[
            "status"
        ],
        "acquisition_item_count": len(
            ontological_soundness_bad_god_evidential_calibration_source_acquisition_manifest[
                "manifest"
            ]["acquisition_items"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-acquisition-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_acquisition_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_acquisition_checks_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_acquisition_checks[
            "status"
        ],
        "target_task_id": ontological_soundness_bad_god_evidential_calibration_source_acquisition_checks[
            "target_task_id"
        ],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-batch-plan.json",
        ontological_soundness_bad_god_evidential_calibration_source_batch_plan,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_batch_plan_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_batch_plan["status"],
        "batch_count": len(
            ontological_soundness_bad_god_evidential_calibration_source_batch_plan["batch_plan"][
                "batches"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-batch-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_batch_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_batch_checks_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_batch_checks["status"],
        "target_task_id": ontological_soundness_bad_god_evidential_calibration_source_batch_checks[
            "target_task_id"
        ],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-seed-catalog.json",
        ontological_soundness_bad_god_evidential_calibration_source_seed_catalog,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_seed_catalog_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_seed_catalog["status"],
        "candidate_source_count": len(
            ontological_soundness_bad_god_evidential_calibration_source_seed_catalog["catalog"][
                "candidate_sources"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-seed-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_seed_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_seed_checks_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_seed_checks["status"],
        "target_task_id": ontological_soundness_bad_god_evidential_calibration_source_seed_checks[
            "target_task_id"
        ],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-eligibility-matrix.json",
        ontological_soundness_bad_god_evidential_calibration_source_eligibility_matrix,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_eligibility_matrix_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_eligibility_matrix[
            "status"
        ],
        "eligible_pending_fetch_count": ontological_soundness_bad_god_evidential_calibration_source_eligibility_matrix[
            "matrix"
        ]["gate_summary"]["eligible_pending_fetch_count"],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-eligibility-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_eligibility_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_eligibility_checks_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_eligibility_checks[
            "status"
        ],
        "target_task_id": ontological_soundness_bad_god_evidential_calibration_source_eligibility_checks[
            "target_task_id"
        ],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-retrieval-runbook.json",
        ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook[
            "status"
        ],
        "retrieval_step_count": len(
            ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook[
                "runbook"
            ]["retrieval_steps"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-retrieval-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_retrieval_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_retrieval_checks_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_retrieval_checks[
            "status"
        ],
        "target_task_id": ontological_soundness_bad_god_evidential_calibration_source_retrieval_checks[
            "target_task_id"
        ],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-retrieval-log-schema.json",
        ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_schema,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_schema_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_schema[
            "status"
        ],
        "log_template_count": len(
            ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_schema[
                "schema"
            ]["log_templates"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-retrieval-log-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_checks_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_checks[
            "status"
        ],
        "target_task_id": ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_checks[
            "target_task_id"
        ],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-retrieval-dry-run-ledger.json",
        ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger[
            "status"
        ],
        "dry_run_count": len(
            ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger[
                "ledger"
            ]["dry_run_rows"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-retrieval-dry-run-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_checks_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_checks[
            "status"
        ],
        "target_task_id": ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_checks[
            "target_task_id"
        ],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-quality-rubric.json",
        ontological_soundness_bad_god_evidential_calibration_source_quality_rubric,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_quality_rubric_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_quality_rubric["status"],
        "source_score_template_count": len(
            ontological_soundness_bad_god_evidential_calibration_source_quality_rubric["rubric"][
                "source_score_templates"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-quality-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_quality_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_quality_checks_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_quality_checks["status"],
        "target_task_id": ontological_soundness_bad_god_evidential_calibration_source_quality_checks[
            "target_task_id"
        ],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-quality-score-ledger-schema.json",
        ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_schema,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_schema_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_schema["status"],
        "score_row_count": len(
            ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_schema["schema"][
                "score_rows"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-quality-score-ledger-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_checks_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_checks["status"],
        "target_task_id": ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_checks[
            "target_task_id"
        ],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-quality-score-dry-run-ledger.json",
        ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_ledger,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_ledger_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_ledger["status"],
        "dry_run_row_count": len(
            ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_ledger["ledger"][
                "dry_run_rows"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-quality-score-dry-run-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_checks_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_checks["status"],
        "target_task_id": ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_checks[
            "target_task_id"
        ],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-quality-score-readiness-gate.json",
        ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_gate,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_gate_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_gate["status"],
        "ready_for_quality_scoring": (
            ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_gate["gate"][
                "ready_for_quality_scoring"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-quality-score-readiness-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_checks_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_checks["status"],
        "target_task_id": ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_checks[
            "target_task_id"
        ],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-packet.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_packet,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_packet_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_content_materialization_packet["status"],
        "materialization_row_count": len(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_packet["packet"][
                "materialization_rows"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_checks_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_content_materialization_checks["status"],
        "target_task_id": ontological_soundness_bad_god_evidential_calibration_source_content_materialization_checks[
            "target_task_id"
        ],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-batch-plan.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_plan,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_plan_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_plan[
            "status"
        ],
        "batch_count": len(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_plan[
                "batch_plan"
            ]["batches"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-batch-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_checks_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_checks[
            "status"
        ],
        "target_task_id": ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_checks[
            "target_task_id"
        ],
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-packet.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_packet,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_packet_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_packet[
            "status"
        ],
        "authorization_granted": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_packet[
                "authorization"
            ]["authorization_granted"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_checks_written", {
        "status": ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_checks[
            "status"
        ],
        "target_task_id": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_checks[
                "target_task_id"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-queue.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_queue,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_queue_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_queue[
                "status"
            ]
        ),
        "review_item_count": len(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_queue[
                "queue"
            ]["review_items"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_checks_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_checks[
                "status"
            ]
        ),
        "target_task_id": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_checks[
                "target_task_id"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-rubric.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric[
                "status"
            ]
        ),
        "criterion_count": len(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric[
                "rubric"
            ]["review_criteria"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-rubric-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric_checks_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric_checks[
                "status"
            ]
        ),
        "target_task_id": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric_checks[
                "target_task_id"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-decisions.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decisions,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decisions_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decisions[
                "status"
            ]
        ),
        "decision_count": len(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decisions[
                "decisions"
            ]["decision_rows"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-decision-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decision_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decision_checks_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decision_checks[
                "status"
            ]
        ),
        "target_task_id": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decision_checks[
                "target_task_id"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-resolution-packet.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet[
                "status"
            ]
        ),
        "resolution_item_count": len(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet[
                "resolution"
            ]["resolution_items"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-resolution-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_checks_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_checks[
                "status"
            ]
        ),
        "target_task_id": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_checks[
                "target_task_id"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-operator-approval-request.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_operator_approval_request,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_operator_approval_request_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_operator_approval_request[
                "status"
            ]
        ),
        "approval_item_count": len(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_operator_approval_request[
                "approval_request"
            ]["approval_items"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-operator-approval-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_operator_approval_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_operator_approval_checks_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_operator_approval_checks[
                "status"
            ]
        ),
        "target_task_id": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_operator_approval_checks[
                "target_task_id"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-terms-rate-limit-review.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_terms_rate_limit_review,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_terms_rate_limit_review_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_terms_rate_limit_review[
                "status"
            ]
        ),
        "review_item_count": len(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_terms_rate_limit_review[
                "terms_rate_limit_review"
            ]["review_items"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-terms-rate-limit-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_terms_rate_limit_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_terms_rate_limit_checks_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_terms_rate_limit_checks[
                "status"
            ]
        ),
        "target_task_id": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_terms_rate_limit_checks[
                "target_task_id"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-private-sensitive-risk-review.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_private_sensitive_risk_review,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_private_sensitive_risk_review_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_private_sensitive_risk_review[
                "status"
            ]
        ),
        "review_item_count": len(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_private_sensitive_risk_review[
                "private_sensitive_risk_review"
            ]["review_items"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-private-sensitive-risk-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_private_sensitive_risk_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_private_sensitive_risk_checks_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_private_sensitive_risk_checks[
                "status"
            ]
        ),
        "target_task_id": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_private_sensitive_risk_checks[
                "target_task_id"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-retrieval-scope-review.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_retrieval_scope_review,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_retrieval_scope_review_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_retrieval_scope_review[
                "status"
            ]
        ),
        "review_item_count": len(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_retrieval_scope_review[
                "retrieval_scope_review"
            ]["review_items"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-retrieval-scope-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_retrieval_scope_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_retrieval_scope_checks_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_retrieval_scope_checks[
                "status"
            ]
        ),
        "target_task_id": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_retrieval_scope_checks[
                "target_task_id"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-logging-hash-plan-review.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_logging_hash_plan_review,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_logging_hash_plan_review_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_logging_hash_plan_review[
                "status"
            ]
        ),
        "review_item_count": len(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_logging_hash_plan_review[
                "logging_hash_plan_review"
            ]["review_items"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-logging-hash-plan-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_logging_hash_plan_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_logging_hash_plan_checks_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_logging_hash_plan_checks[
                "status"
            ]
        ),
        "target_task_id": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_logging_hash_plan_checks[
                "target_task_id"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-prerequisite-closure-matrix.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_matrix,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_matrix_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_matrix[
                "status"
            ]
        ),
        "closure_row_count": len(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_matrix[
                "prerequisite_closure_matrix"
            ]["closure_rows"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-prerequisite-closure-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_checks_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_checks[
                "status"
            ]
        ),
        "target_task_id": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_checks[
                "target_task_id"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-materialization-execution-gate.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate[
                "status"
            ]
        ),
        "gate_row_count": len(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate[
                "materialization_execution_gate"
            ]["gate_rows"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-materialization-execution-gate-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate_checks_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate_checks[
                "status"
            ]
        ),
        "target_task_id": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate_checks[
                "target_task_id"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-future-command-manifest.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest[
                "status"
            ]
        ),
        "command_count": len(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest[
                "future_command_manifest"
            ]["commands"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-future-command-manifest-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest_checks_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest_checks[
                "status"
            ]
        ),
        "target_task_id": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest_checks[
                "target_task_id"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-nonexecution-receipt.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt[
                "status"
            ]
        ),
        "receipt_row_count": len(
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt[
                "command_nonexecution_receipt"
            ]["receipt_rows"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-nonexecution-receipt-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt_checks_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt_checks[
                "status"
            ]
        ),
        "target_task_id": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt_checks[
                "target_task_id"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-ledger.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_ledger,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_ledger_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_ledger[
                "status"
            ]
        ),
        "open_gap_count": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_ledger[
                "command_output_gap_ledger"
            ]["open_gap_count"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_checks_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_checks[
                "status"
            ]
        ),
        "target_task_id": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_checks[
                "target_task_id"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-task-queue.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_queue,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_queue_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_queue[
                "status"
            ]
        ),
        "task_count": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_queue[
                "command_output_gap_closure_task_queue"
            ]["task_count"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-task-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_checks_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_checks[
                "status"
            ]
        ),
        "target_task_id": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_checks[
                "target_task_id"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-plan.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_plan,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_plan_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_plan[
                "status"
            ]
        ),
        "batch_count": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_plan[
                "command_output_gap_closure_batch_plan"
            ]["batch_count"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_checks_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_checks[
                "status"
            ]
        ),
        "target_task_id": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_checks[
                "target_task_id"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-ledger.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_ledger,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_ledger_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_ledger[
                "status"
            ]
        ),
        "executed_batch_count": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_ledger[
                "command_output_gap_closure_batch_execution_ledger"
            ]["executed_batch_count"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_checks_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_checks[
                "status"
            ]
        ),
        "target_task_id": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_checks[
                "target_task_id"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-matrix.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_matrix,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_matrix_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_matrix[
                "status"
            ]
        ),
        "open_unblocker_count": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_matrix[
                "command_output_gap_closure_batch_execution_unblocker_matrix"
            ]["open_unblocker_count"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_checks_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_checks[
                "status"
            ]
        ),
        "target_task_id": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_checks[
                "target_task_id"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-queue.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_queue,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_queue_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_queue[
                "status"
            ]
        ),
        "resolution_task_count": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_queue[
                "command_output_gap_closure_batch_execution_unblocker_resolution_queue"
            ]["resolution_task_count"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_checks_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_checks[
                "status"
            ]
        ),
        "target_task_id": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_checks[
                "target_task_id"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-batch-plan.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan[
                "status"
            ]
        ),
        "resolution_batch_count": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan[
                "command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan"
            ]["resolution_batch_count"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-batch-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_checks_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_checks[
                "status"
            ]
        ),
        "target_task_id": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_checks[
                "target_task_id"
            ]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-batch-execution-ledger.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_execution_ledger,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_execution_ledger_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_execution_ledger[
                "status"
            ]
        ),
        "executed_resolution_batch_count": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_execution_ledger[
                "command_output_gap_closure_batch_execution_unblocker_resolution_batch_execution_ledger"
            ]["executed_resolution_batch_count"]
        ),
    })
    _write_json(
        session_dir / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-batch-execution-checks.json",
        ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_execution_checks,
    )
    log("ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_execution_checks_written", {
        "status": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_execution_checks[
                "status"
            ]
        ),
        "target_task_id": (
            ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_execution_checks[
                "target_task_id"
            ]
        ),
    })
    _write_json(session_dir / "ontological-soundness-resolution-worklist.json", ontological_soundness_resolution_worklist)
    log("ontological_soundness_resolution_worklist_written", {
        "status": ontological_soundness_resolution_worklist["status"],
        "work_item_count": len(ontological_soundness_resolution_worklist["worklist"]["work_items"]),
    })
    _write_json(
        session_dir / "ontological-soundness-resolution-worklist-checks.json",
        ontological_soundness_resolution_worklist_checks,
    )
    log("ontological_soundness_resolution_worklist_checks_written", {
        "status": ontological_soundness_resolution_worklist_checks["status"],
        "target_obligation_id": ontological_soundness_resolution_worklist_checks["target_obligation_id"],
    })
    _write_json(session_dir / "ontological-soundness-resolution-batches.json", ontological_soundness_resolution_batches)
    log("ontological_soundness_resolution_batches_written", {
        "status": ontological_soundness_resolution_batches["status"],
        "batch_count": len(ontological_soundness_resolution_batches["batch_plan"]["batches"]),
    })
    _write_json(
        session_dir / "ontological-soundness-resolution-batch-checks.json",
        ontological_soundness_resolution_batch_checks,
    )
    log("ontological_soundness_resolution_batch_checks_written", {
        "status": ontological_soundness_resolution_batch_checks["status"],
        "target_obligation_id": ontological_soundness_resolution_batch_checks["target_obligation_id"],
    })
    _write_json(session_dir / "ontological-soundness-batch-execution-ledger.json", ontological_soundness_batch_execution_ledger)
    log("ontological_soundness_batch_execution_ledger_written", {
        "status": ontological_soundness_batch_execution_ledger["status"],
        "execution_record_count": len(ontological_soundness_batch_execution_ledger["ledger"]["execution_records"]),
    })
    _write_json(
        session_dir / "ontological-soundness-batch-execution-checks.json",
        ontological_soundness_batch_execution_checks,
    )
    log("ontological_soundness_batch_execution_checks_written", {
        "status": ontological_soundness_batch_execution_checks["status"],
        "target_obligation_id": ontological_soundness_batch_execution_checks["target_obligation_id"],
    })
    _write_json(session_dir / "attribute-coherence-ledger.json", attribute_coherence_ledger)
    log("attribute_coherence_ledger_written", {
        "status": attribute_coherence_ledger["status"],
        "ledger_id": ATTRIBUTE_COHERENCE_LEDGER["id"],
    })
    _write_json(session_dir / "attribute-coherence-checks.json", attribute_coherence_checks)
    log("attribute_coherence_checks_written", {
        "status": attribute_coherence_checks["status"],
        "argument_id": attribute_coherence_checks["argument_id"],
    })
    _write_json(session_dir / "coherent-conceivability-model.json", coherent_conceivability_model)
    log("coherent_conceivability_model_written", {
        "status": coherent_conceivability_model["status"],
        "model_id": COHERENT_CONCEIVABILITY_MODEL["id"],
    })
    _write_json(session_dir / "coherent-conceivability-checks.json", coherent_conceivability_checks)
    log("coherent_conceivability_checks_written", {
        "status": coherent_conceivability_checks["status"],
        "argument_id": coherent_conceivability_checks["argument_id"],
    })
    _write_json(session_dir / "metaphysical-possibility-bridge.json", metaphysical_possibility_bridge)
    log("metaphysical_possibility_bridge_written", {
        "status": metaphysical_possibility_bridge["status"],
        "bridge_id": METAPHYSICAL_POSSIBILITY_BRIDGE["id"],
    })
    _write_json(session_dir / "metaphysical-possibility-checks.json", metaphysical_possibility_checks)
    log("metaphysical_possibility_checks_written", {
        "status": metaphysical_possibility_checks["status"],
        "argument_id": metaphysical_possibility_checks["argument_id"],
    })
    _write_json(session_dir / "definition-smuggling-audit.json", definition_smuggling_audit)
    log("definition_smuggling_audit_written", {
        "status": definition_smuggling_audit["status"],
        "audit_id": DEFINITION_SMUGGLING_AUDIT["id"],
    })
    _write_json(session_dir / "definition-smuggling-checks.json", definition_smuggling_checks)
    log("definition_smuggling_checks_written", {
        "status": definition_smuggling_checks["status"],
        "argument_id": definition_smuggling_checks["argument_id"],
    })
    _write_json(session_dir / "evidential-evil-probability-audit.json", evidential_evil_probability_audit)
    log("evidential_evil_probability_audit_written", {
        "status": evidential_evil_probability_audit["status"],
        "audit_id": EVIDENTIAL_EVIL_PROBABILITY_AUDIT["id"],
    })
    _write_json(session_dir / "evidential-evil-likelihood-ledger.json", evidential_evil_likelihood_ledger)
    log("evidential_evil_likelihood_ledger_written", {
        "status": evidential_evil_likelihood_ledger["status"],
        "ledger_id": EVIDENTIAL_EVIL_LIKELIHOOD_LEDGER["id"],
    })
    _write_json(session_dir / "evidential-evil-dependence-model.json", evidential_evil_dependence_model)
    log("evidential_evil_dependence_model_written", {
        "status": evidential_evil_dependence_model["status"],
        "model_id": EVIDENTIAL_EVIL_DEPENDENCE_MODEL["id"],
    })
    _write_json(session_dir / "evidential-evil-calibration-ledger.json", evidential_evil_calibration_ledger)
    log("evidential_evil_calibration_ledger_written", {
        "status": evidential_evil_calibration_ledger["status"],
        "ledger_id": EVIDENTIAL_EVIL_CALIBRATION_LEDGER["id"],
    })
    _write_json(session_dir / "evidential-evil-case-corpus.json", evidential_evil_case_corpus)
    log("evidential_evil_case_corpus_written", {
        "status": evidential_evil_case_corpus["status"],
        "corpus_id": EVIDENTIAL_EVIL_CASE_CORPUS["id"],
    })
    _write_json(session_dir / "evidential-evil-reviewed-case-records.json", evidential_evil_reviewed_case_records)
    log("evidential_evil_reviewed_case_records_written", {
        "status": evidential_evil_reviewed_case_records["status"],
        "records_id": EVIDENTIAL_EVIL_REVIEWED_CASE_RECORDS["id"],
    })
    _write_json(
        session_dir / "evidential-evil-empirical-expansion-ledger.json",
        evidential_evil_empirical_expansion_ledger,
    )
    log("evidential_evil_empirical_expansion_ledger_written", {
        "status": evidential_evil_empirical_expansion_ledger["status"],
        "ledger_id": EVIDENTIAL_EVIL_EMPIRICAL_EXPANSION_LEDGER["id"],
    })
    _write_json(
        session_dir / "evidential-evil-primary-dataset-selection.json",
        evidential_evil_primary_dataset_selection,
    )
    log("evidential_evil_primary_dataset_selection_written", {
        "status": evidential_evil_primary_dataset_selection["status"],
        "selection_id": EVIDENTIAL_EVIL_PRIMARY_DATASET_SELECTION["id"],
    })
    _write_json(
        session_dir / "evidential-evil-dataset-ingestion-manifest.json",
        evidential_evil_dataset_ingestion_manifest,
    )
    log("evidential_evil_dataset_ingestion_manifest_written", {
        "status": evidential_evil_dataset_ingestion_manifest["status"],
        "manifest_id": EVIDENTIAL_EVIL_DATASET_INGESTION_MANIFEST["id"],
    })
    _write_json(session_dir / "evidential-evil-license-privacy-review.json", evidential_evil_license_privacy_review)
    log("evidential_evil_license_privacy_review_written", {
        "status": evidential_evil_license_privacy_review["status"],
        "review_id": EVIDENTIAL_EVIL_LICENSE_PRIVACY_REVIEW["id"],
    })
    _write_json(
        session_dir / "evidential-evil-attribution-template-ledger.json",
        evidential_evil_attribution_template_ledger,
    )
    log("evidential_evil_attribution_template_ledger_written", {
        "status": evidential_evil_attribution_template_ledger["status"],
        "ledger_id": EVIDENTIAL_EVIL_ATTRIBUTION_TEMPLATE_LEDGER["id"],
    })
    _write_json(
        session_dir / "evidential-evil-attribution-template-checks.json",
        evidential_evil_attribution_template_checks,
    )
    log("evidential_evil_attribution_template_checks_written", {
        "status": evidential_evil_attribution_template_checks["status"],
        "argument_id": evidential_evil_attribution_template_checks["argument_id"],
    })
    _write_json(
        session_dir / "evidential-evil-license-decision-packet.json",
        evidential_evil_license_decision_packet,
    )
    log("evidential_evil_license_decision_packet_written", {
        "status": evidential_evil_license_decision_packet["status"],
        "packet_id": EVIDENTIAL_EVIL_LICENSE_DECISION_PACKET["id"],
    })
    _write_json(
        session_dir / "evidential-evil-license-decision-checks.json",
        evidential_evil_license_decision_checks,
    )
    log("evidential_evil_license_decision_checks_written", {
        "status": evidential_evil_license_decision_checks["status"],
        "argument_id": evidential_evil_license_decision_checks["argument_id"],
    })
    _write_json(
        session_dir / "evidential-evil-source-acquisition-hash-runbook.json",
        evidential_evil_source_acquisition_hash_runbook,
    )
    log("evidential_evil_source_acquisition_hash_runbook_written", {
        "status": evidential_evil_source_acquisition_hash_runbook["status"],
        "runbook_id": EVIDENTIAL_EVIL_SOURCE_ACQUISITION_HASH_RUNBOOK["id"],
    })
    _write_json(
        session_dir / "evidential-evil-source-acquisition-hash-runbook-checks.json",
        evidential_evil_source_acquisition_hash_runbook_checks,
    )
    log("evidential_evil_source_acquisition_hash_runbook_checks_written", {
        "status": evidential_evil_source_acquisition_hash_runbook_checks["status"],
        "argument_id": evidential_evil_source_acquisition_hash_runbook_checks["argument_id"],
    })
    _write_json(
        session_dir / "evidential-evil-suppression-report-template.json",
        evidential_evil_suppression_report_template,
    )
    log("evidential_evil_suppression_report_template_written", {
        "status": evidential_evil_suppression_report_template["status"],
        "template_id": EVIDENTIAL_EVIL_SUPPRESSION_REPORT_TEMPLATE["id"],
    })
    _write_json(
        session_dir / "evidential-evil-suppression-report-template-checks.json",
        evidential_evil_suppression_report_template_checks,
    )
    log("evidential_evil_suppression_report_template_checks_written", {
        "status": evidential_evil_suppression_report_template_checks["status"],
        "argument_id": evidential_evil_suppression_report_template_checks["argument_id"],
    })
    _write_json(
        session_dir / "evidential-evil-source-version-hash-preflight.json",
        evidential_evil_source_version_hash_preflight,
    )
    log("evidential_evil_source_version_hash_preflight_written", {
        "status": evidential_evil_source_version_hash_preflight["status"],
        "preflight_id": EVIDENTIAL_EVIL_SOURCE_VERSION_HASH_PREFLIGHT["id"],
    })
    _write_json(
        session_dir / "evidential-evil-source-version-hash-preflight-checks.json",
        evidential_evil_source_version_hash_preflight_checks,
    )
    log("evidential_evil_source_version_hash_preflight_checks_written", {
        "status": evidential_evil_source_version_hash_preflight_checks["status"],
        "argument_id": evidential_evil_source_version_hash_preflight_checks["argument_id"],
    })
    _write_json(
        session_dir / "evidential-evil-derived-aggregate-schema.json",
        evidential_evil_derived_aggregate_schema,
    )
    log("evidential_evil_derived_aggregate_schema_written", {
        "status": evidential_evil_derived_aggregate_schema["status"],
        "schema_id": EVIDENTIAL_EVIL_DERIVED_AGGREGATE_SCHEMA["id"],
    })
    _write_json(
        session_dir / "evidential-evil-derived-aggregate-schema-checks.json",
        evidential_evil_derived_aggregate_schema_checks,
    )
    log("evidential_evil_derived_aggregate_schema_checks_written", {
        "status": evidential_evil_derived_aggregate_schema_checks["status"],
        "argument_id": evidential_evil_derived_aggregate_schema_checks["argument_id"],
    })
    _write_json(
        session_dir / "evidential-evil-microdata-minimization-policy.json",
        evidential_evil_microdata_minimization_policy,
    )
    log("evidential_evil_microdata_minimization_policy_written", {
        "status": evidential_evil_microdata_minimization_policy["status"],
        "policy_id": EVIDENTIAL_EVIL_MICRODATA_MINIMIZATION_POLICY["id"],
    })
    _write_json(
        session_dir / "evidential-evil-microdata-minimization-checks.json",
        evidential_evil_microdata_minimization_checks,
    )
    log("evidential_evil_microdata_minimization_checks_written", {
        "status": evidential_evil_microdata_minimization_checks["status"],
        "argument_id": evidential_evil_microdata_minimization_checks["argument_id"],
    })
    _write_json(session_dir / "evidential-evil-license-privacy-checks.json", evidential_evil_license_privacy_checks)
    log("evidential_evil_license_privacy_checks_written", {
        "status": evidential_evil_license_privacy_checks["status"],
        "argument_id": evidential_evil_license_privacy_checks["argument_id"],
    })
    _write_json(
        session_dir / "evidential-evil-dataset-ingestion-checks.json",
        evidential_evil_dataset_ingestion_checks,
    )
    log("evidential_evil_dataset_ingestion_checks_written", {
        "status": evidential_evil_dataset_ingestion_checks["status"],
        "argument_id": evidential_evil_dataset_ingestion_checks["argument_id"],
    })
    _write_json(
        session_dir / "evidential-evil-primary-dataset-selection-checks.json",
        evidential_evil_primary_dataset_selection_checks,
    )
    log("evidential_evil_primary_dataset_selection_checks_written", {
        "status": evidential_evil_primary_dataset_selection_checks["status"],
        "argument_id": evidential_evil_primary_dataset_selection_checks["argument_id"],
    })
    _write_json(
        session_dir / "evidential-evil-empirical-expansion-checks.json",
        evidential_evil_empirical_expansion_checks,
    )
    log("evidential_evil_empirical_expansion_checks_written", {
        "status": evidential_evil_empirical_expansion_checks["status"],
        "argument_id": evidential_evil_empirical_expansion_checks["argument_id"],
    })
    _write_json(
        session_dir / "evidential-evil-reviewed-case-records-checks.json",
        evidential_evil_reviewed_case_record_checks,
    )
    log("evidential_evil_reviewed_case_records_checks_written", {
        "status": evidential_evil_reviewed_case_record_checks["status"],
        "argument_id": evidential_evil_reviewed_case_record_checks["argument_id"],
    })
    _write_json(session_dir / "evidential-evil-case-corpus-checks.json", evidential_evil_case_corpus_checks)
    log("evidential_evil_case_corpus_checks_written", {
        "status": evidential_evil_case_corpus_checks["status"],
        "argument_id": evidential_evil_case_corpus_checks["argument_id"],
    })
    _write_json(session_dir / "evidential-evil-calibration-checks.json", evidential_evil_calibration_checks)
    log("evidential_evil_calibration_checks_written", {
        "status": evidential_evil_calibration_checks["status"],
        "argument_id": evidential_evil_calibration_checks["argument_id"],
    })
    _write_json(session_dir / "evidential-evil-dependence-checks.json", evidential_evil_dependence_checks)
    log("evidential_evil_dependence_checks_written", {
        "status": evidential_evil_dependence_checks["status"],
        "argument_id": evidential_evil_dependence_checks["argument_id"],
    })
    _write_json(session_dir / "evidential-evil-likelihood-checks.json", evidential_evil_likelihood_checks)
    log("evidential_evil_likelihood_checks_written", {
        "status": evidential_evil_likelihood_checks["status"],
        "argument_id": evidential_evil_likelihood_checks["argument_id"],
    })
    _write_json(session_dir / "evidential-evil-probability-checks.json", evidential_evil_probability_checks)
    log("evidential_evil_probability_checks_written", {
        "status": evidential_evil_probability_checks["status"],
        "argument_id": evidential_evil_probability_checks["argument_id"],
    })
    _write_json(session_dir / "evil-hiddenness-moral-pressure-audit.json", evil_hiddenness_moral_pressure_audit)
    log("evil_hiddenness_moral_pressure_audit_written", {
        "status": evil_hiddenness_moral_pressure_audit["status"],
        "audit_id": EVIL_HIDDENNESS_MORAL_PRESSURE_AUDIT["id"],
    })
    _write_json(session_dir / "evil-hiddenness-moral-pressure-checks.json", evil_hiddenness_moral_pressure_checks)
    log("evil_hiddenness_moral_pressure_checks_written", {
        "status": evil_hiddenness_moral_pressure_checks["status"],
        "argument_id": evil_hiddenness_moral_pressure_checks["argument_id"],
    })
    _write_json(session_dir / "moral-perfection-grounding-audit.json", moral_perfection_grounding_audit)
    log("moral_perfection_grounding_audit_written", {
        "status": moral_perfection_grounding_audit["status"],
        "audit_id": MORAL_PERFECTION_GROUNDING_AUDIT["id"],
    })
    _write_json(session_dir / "moral-perfection-grounding-checks.json", moral_perfection_grounding_checks)
    log("moral_perfection_grounding_checks_written", {
        "status": moral_perfection_grounding_checks["status"],
        "argument_id": moral_perfection_grounding_checks["argument_id"],
    })
    _write_json(session_dir / "positive-grounding-audit.json", positive_grounding_audit)
    log("positive_grounding_audit_written", {
        "status": positive_grounding_audit["status"],
        "audit_id": POSITIVE_GROUNDING_AUDIT["id"],
    })
    _write_json(session_dir / "positive-grounding-checks.json", positive_grounding_checks)
    log("positive_grounding_checks_written", {
        "status": positive_grounding_checks["status"],
        "argument_id": positive_grounding_checks["argument_id"],
    })
    _write_json(session_dir / "positive-property-filter-audit.json", positive_property_filter_audit)
    log("positive_property_filter_audit_written", {
        "status": positive_property_filter_audit["status"],
        "audit_id": POSITIVE_PROPERTY_FILTER_AUDIT["id"],
    })
    _write_json(session_dir / "positive-property-filter-checks.json", positive_property_filter_checks)
    log("positive_property_filter_checks_written", {
        "status": positive_property_filter_checks["status"],
        "argument_id": positive_property_filter_checks["argument_id"],
    })
    _write_json(session_dir / "rival-necessary-parity-audit.json", rival_necessary_parity_audit)
    log("rival_necessary_parity_audit_written", {
        "status": rival_necessary_parity_audit["status"],
        "audit_id": RIVAL_NECESSARY_PARITY_AUDIT["id"],
    })
    _write_json(session_dir / "rival-necessary-parity-checks.json", rival_necessary_parity_checks)
    log("rival_necessary_parity_checks_written", {
        "status": rival_necessary_parity_checks["status"],
        "argument_id": rival_necessary_parity_checks["argument_id"],
    })
    _write_json(session_dir / "possible-necessary-existence-bridge.json", possible_necessary_existence_bridge)
    log("possible_necessary_existence_bridge_written", {
        "status": possible_necessary_existence_bridge["status"],
        "bridge_id": POSSIBLE_NECESSARY_EXISTENCE_BRIDGE["id"],
    })
    _write_json(session_dir / "possible-necessary-existence-checks.json", possible_necessary_existence_checks)
    log("possible_necessary_existence_checks_written", {
        "status": possible_necessary_existence_checks["status"],
        "argument_id": possible_necessary_existence_checks["argument_id"],
    })
    _write_json(session_dir / "possibility-premise-ladder.json", possibility_premise_ladder)
    log("possibility_premise_ladder_written", {
        "status": possibility_premise_ladder["status"],
        "ladder_id": POSSIBILITY_PREMISE_LADDER["id"],
    })
    _write_json(session_dir / "possibility-premise-checks.json", possibility_premise_checks)
    log("possibility_premise_checks_written", {
        "status": possibility_premise_checks["status"],
        "argument_id": possibility_premise_checks["argument_id"],
    })
    _write_json(session_dir / "teleological-bayes-model.json", teleological_bayes_model)
    log("teleological_bayes_model_written", {
        "status": teleological_bayes_model["status"],
        "model_id": TELEOLOGICAL_BAYES_MODEL["id"],
    })
    _write_json(session_dir / "teleological-bayes-checks.json", teleological_bayes_checks)
    log("teleological_bayes_checks_written", {
        "status": teleological_bayes_checks["status"],
        "argument_id": teleological_bayes_checks["argument_id"],
    })
    _write_json(session_dir / "cosmological-psr-model.json", cosmological_psr_model)
    log("cosmological_psr_model_written", {
        "status": cosmological_psr_model["status"],
        "model_id": COSMOLOGICAL_PSR_MODEL["id"],
    })
    _write_json(session_dir / "cosmological-psr-checks.json", cosmological_psr_checks)
    log("cosmological_psr_checks_written", {
        "status": cosmological_psr_checks["status"],
        "argument_id": cosmological_psr_checks["argument_id"],
    })
    _write_json(session_dir / "evil-hiddenness-constraints.json", evil_hiddenness_constraints)
    log("evil_hiddenness_constraints_written", {
        "status": evil_hiddenness_constraints["status"],
        "model_id": EVIL_HIDDENNESS_CONSTRAINT_MODEL["id"],
    })
    _write_json(session_dir / "evil-hiddenness-checks.json", evil_hiddenness_checks)
    log("evil_hiddenness_checks_written", {
        "status": evil_hiddenness_checks["status"],
        "argument_id": evil_hiddenness_checks["argument_id"],
    })
    _write_json(session_dir / "formal-obligations.json", {
        "status": "open_obligations_block_proof_claim",
        "obligations": _obligation_dicts(
            coverage_matrix,
            definition_checks,
            modal_validity_checks,
            modal_consistency_checks,
            teleological_bayes_checks,
            cosmological_psr_checks,
            evil_hiddenness_checks,
            ontological_soundness_checks,
        ),
    })
    log("formal_obligations_written", {"count": len(PROOF_OBLIGATIONS)})
    _write_json(session_dir / "proof-readiness.json", proof_readiness)
    log("proof_readiness_written", proof_readiness)
    skeleton_path = _write_formal_skeleton(session_dir)
    log("formal_skeleton_written", {"path": str(skeleton_path)})
    _write_json(session_dir / "frontier.json", frontier)
    log("frontier_written", {"proof_claimed": frontier["proof_claimed"]})
    report_path = _write_report(session_dir, frontier)
    log("report_written", {"path": str(report_path)})
    log("session_end", {"proof_claimed": frontier["proof_claimed"]})

    return {
        "session_dir": str(session_dir),
        "report_path": str(report_path),
        "proof_claimed": frontier["proof_claimed"],
        "best_current_path": frontier["best_current_path"]["argument_id"],
        "elapsed_seconds": round(time.time() - t0, 2),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }
