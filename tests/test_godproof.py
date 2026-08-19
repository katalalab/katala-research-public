"""God-proof frontier kernel tests."""
from __future__ import annotations

import json
from pathlib import Path

from katala_research.godproof import run_godproof


def test_godproof_writes_auditable_artifacts(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path, query="God proof smoke")
    session_dir = Path(summary["session_dir"])

    expected = [
        "wisdom-map.json",
        "target-concepts.json",
        "definition-checks.json",
        "wisdom-corpus.json",
        "coverage-matrix.json",
        "human-wisdom-primary-source-seed-ledger.json",
        "human-wisdom-primary-source-seed-checks.json",
        "human-wisdom-primary-source-extraction-queue.json",
        "human-wisdom-primary-source-extraction-checks.json",
        "human-wisdom-primary-source-summary-candidates.json",
        "human-wisdom-primary-source-summary-candidate-checks.json",
        "human-wisdom-counterpressure-edge-proposals.json",
        "human-wisdom-counterpressure-edge-checks.json",
        "human-wisdom-counterpressure-edge-review-queue.json",
        "human-wisdom-counterpressure-edge-review-checks.json",
        "human-wisdom-counterpressure-edge-review-rubric.json",
        "human-wisdom-counterpressure-edge-review-rubric-checks.json",
        "human-wisdom-counterpressure-edge-review-decisions.json",
        "human-wisdom-counterpressure-edge-review-decision-checks.json",
        "human-wisdom-counterpressure-edge-resolution-packet.json",
        "human-wisdom-counterpressure-edge-resolution-checks.json",
        "human-wisdom-counterpressure-edge-evidence-request-queue.json",
        "human-wisdom-counterpressure-edge-evidence-request-checks.json",
        "human-wisdom-counterpressure-edge-evidence-acquisition-manifest.json",
        "human-wisdom-counterpressure-edge-evidence-acquisition-checks.json",
        "human-wisdom-counterpressure-edge-metadata-receipt-schema.json",
        "human-wisdom-counterpressure-edge-metadata-receipt-checks.json",
        "human-wisdom-counterpressure-edge-metadata-receipt-review-queue.json",
        "human-wisdom-counterpressure-edge-metadata-receipt-review-checks.json",
        "human-wisdom-counterpressure-edge-metadata-receipt-review-rubric.json",
        "human-wisdom-counterpressure-edge-metadata-receipt-review-rubric-checks.json",
        "human-wisdom-counterpressure-edge-metadata-receipt-review-decisions.json",
        "human-wisdom-counterpressure-edge-metadata-receipt-review-decision-checks.json",
        "human-wisdom-counterpressure-edge-metadata-receipt-resolution-packet.json",
        "human-wisdom-counterpressure-edge-metadata-receipt-resolution-checks.json",
        "human-wisdom-counterpressure-edge-metadata-receipt-evidence-request-queue.json",
        "human-wisdom-counterpressure-edge-metadata-receipt-evidence-request-checks.json",
        "human-wisdom-counterpressure-edge-metadata-receipt-acquisition-manifest.json",
        "human-wisdom-counterpressure-edge-metadata-receipt-acquisition-checks.json",
        "human-wisdom-counterpressure-edge-metadata-receipt-acquisition-hash-runbook.json",
        "human-wisdom-counterpressure-edge-metadata-receipt-acquisition-hash-runbook-checks.json",
        "human-wisdom-counterpressure-edge-metadata-receipt-authorization-packet.json",
        "human-wisdom-counterpressure-edge-metadata-receipt-authorization-checks.json",
        "human-wisdom-counterpressure-edge-metadata-receipt-authorization-review-queue.json",
        "human-wisdom-counterpressure-edge-metadata-receipt-authorization-review-checks.json",
        "human-wisdom-intake-roadmap.json",
        "human-wisdom-intake-checks.json",
        "proof-graph.json",
        "modal-derivation.json",
        "modal-validity-checks.json",
        "modal-consistency-checks.json",
        "ontological-soundness-dossier.json",
        "ontological-soundness-checks.json",
        "ontological-soundness-parody-discriminator-matrix.json",
        "ontological-soundness-parody-discriminator-checks.json",
        "ontological-soundness-bad-god-discharge-criteria.json",
        "ontological-soundness-bad-god-discharge-checks.json",
        "ontological-soundness-bad-god-discharge-task-queue.json",
        "ontological-soundness-bad-god-discharge-task-checks.json",
        "ontological-soundness-bad-god-task-dependency-graph.json",
        "ontological-soundness-bad-god-task-dependency-checks.json",
        "ontological-soundness-bad-god-evil-hiddenness-pressure-matrix.json",
        "ontological-soundness-bad-god-evil-hiddenness-pressure-checks.json",
        "ontological-soundness-bad-god-evil-hiddenness-sufficiency-task-queue.json",
        "ontological-soundness-bad-god-evil-hiddenness-sufficiency-task-checks.json",
        "ontological-soundness-bad-god-evidential-probability-pressure-task-scaffold.json",
        "ontological-soundness-bad-god-evidential-probability-pressure-task-checks.json",
        "ontological-soundness-bad-god-evidential-prior-sensitivity-grid.json",
        "ontological-soundness-bad-god-evidential-prior-sensitivity-checks.json",
        "ontological-soundness-bad-god-evidential-likelihood-sensitivity-grid.json",
        "ontological-soundness-bad-god-evidential-likelihood-sensitivity-checks.json",
        "ontological-soundness-bad-god-evidential-response-cost-grid.json",
        "ontological-soundness-bad-god-evidential-response-cost-checks.json",
        "ontological-soundness-bad-god-evidential-rival-comparison-grid.json",
        "ontological-soundness-bad-god-evidential-rival-comparison-checks.json",
        "ontological-soundness-bad-god-evidential-probability-execution-packet.json",
        "ontological-soundness-bad-god-evidential-probability-execution-checks.json",
        "ontological-soundness-bad-god-evidential-posterior-projection-results.json",
        "ontological-soundness-bad-god-evidential-posterior-projection-checks.json",
        "ontological-soundness-bad-god-evidential-projection-outcome-review.json",
        "ontological-soundness-bad-god-evidential-projection-outcome-checks.json",
        "ontological-soundness-bad-god-evidential-projection-remediation-plan.json",
        "ontological-soundness-bad-god-evidential-projection-remediation-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-registry.json",
        "ontological-soundness-bad-god-evidential-calibration-source-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-acquisition-manifest.json",
        "ontological-soundness-bad-god-evidential-calibration-source-acquisition-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-batch-plan.json",
        "ontological-soundness-bad-god-evidential-calibration-source-batch-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-seed-catalog.json",
        "ontological-soundness-bad-god-evidential-calibration-source-seed-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-eligibility-matrix.json",
        "ontological-soundness-bad-god-evidential-calibration-source-eligibility-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-retrieval-runbook.json",
        "ontological-soundness-bad-god-evidential-calibration-source-retrieval-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-retrieval-log-schema.json",
        "ontological-soundness-bad-god-evidential-calibration-source-retrieval-log-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-retrieval-dry-run-ledger.json",
        "ontological-soundness-bad-god-evidential-calibration-source-retrieval-dry-run-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-quality-rubric.json",
        "ontological-soundness-bad-god-evidential-calibration-source-quality-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-quality-score-ledger-schema.json",
        "ontological-soundness-bad-god-evidential-calibration-source-quality-score-ledger-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-quality-score-dry-run-ledger.json",
        "ontological-soundness-bad-god-evidential-calibration-source-quality-score-dry-run-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-quality-score-readiness-gate.json",
        "ontological-soundness-bad-god-evidential-calibration-source-quality-score-readiness-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-packet.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-batch-plan.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-batch-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-packet.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-queue.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-rubric.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-rubric-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-decisions.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-decision-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-resolution-packet.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-resolution-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-operator-approval-request.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-operator-approval-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-terms-rate-limit-review.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-terms-rate-limit-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-private-sensitive-risk-review.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-private-sensitive-risk-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-retrieval-scope-review.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-retrieval-scope-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-logging-hash-plan-review.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-logging-hash-plan-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-prerequisite-closure-matrix.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-prerequisite-closure-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-materialization-execution-gate.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-materialization-execution-gate-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-future-command-manifest.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-future-command-manifest-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-nonexecution-receipt.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-nonexecution-receipt-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-ledger.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-task-queue.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-task-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-plan.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-ledger.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-matrix.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-queue.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-batch-plan.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-batch-checks.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-batch-execution-ledger.json",
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-batch-execution-checks.json",
        "ontological-soundness-resolution-worklist.json",
        "ontological-soundness-resolution-worklist-checks.json",
        "ontological-soundness-resolution-batches.json",
        "ontological-soundness-resolution-batch-checks.json",
        "ontological-soundness-batch-execution-ledger.json",
        "ontological-soundness-batch-execution-checks.json",
        "attribute-coherence-ledger.json",
        "attribute-coherence-checks.json",
        "coherent-conceivability-model.json",
        "coherent-conceivability-checks.json",
        "metaphysical-possibility-bridge.json",
        "metaphysical-possibility-checks.json",
        "definition-smuggling-audit.json",
        "definition-smuggling-checks.json",
        "evidential-evil-probability-audit.json",
        "evidential-evil-likelihood-ledger.json",
        "evidential-evil-dependence-model.json",
        "evidential-evil-case-corpus.json",
        "evidential-evil-reviewed-case-records.json",
        "evidential-evil-primary-dataset-selection.json",
        "evidential-evil-dataset-ingestion-manifest.json",
        "evidential-evil-license-privacy-review.json",
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
        "evidential-evil-license-privacy-checks.json",
        "evidential-evil-dataset-ingestion-checks.json",
        "evidential-evil-primary-dataset-selection-checks.json",
        "evidential-evil-empirical-expansion-ledger.json",
        "evidential-evil-empirical-expansion-checks.json",
        "evidential-evil-reviewed-case-records-checks.json",
        "evidential-evil-case-corpus-checks.json",
        "evidential-evil-calibration-ledger.json",
        "evidential-evil-calibration-checks.json",
        "evidential-evil-dependence-checks.json",
        "evidential-evil-likelihood-checks.json",
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
        "teleological-bayes-model.json",
        "teleological-bayes-checks.json",
        "cosmological-psr-model.json",
        "cosmological-psr-checks.json",
        "evil-hiddenness-constraints.json",
        "evil-hiddenness-checks.json",
        "formal-obligations.json",
        "proof-readiness.json",
        "frontier.json",
        "sources.jsonl",
        "transcript.jsonl",
        "report.md",
    ]
    for artifact in expected:
        assert (session_dir / artifact).exists(), f"missing {artifact}"

    frontier = json.loads((session_dir / "frontier.json").read_text(encoding="utf-8"))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    coverage = json.loads((session_dir / "coverage-matrix.json").read_text(encoding="utf-8"))
    assert frontier["proof_claimed"] is False
    assert readiness["proof_claim_allowed"] is False
    assert readiness["wisdom_coverage_status"] == coverage["status"]
    assert readiness["target_definition_status"] == "complete"
    assert readiness["ontological_validity_status"] == "complete"
    assert readiness["ontological_consistency_status"] == "complete"
    assert readiness["ontological_soundness_status"] == "contested"
    assert readiness["teleological_bayes_status"] == "complete"
    assert readiness["cosmological_psr_status"] == "complete"
    assert readiness["evil_hiddenness_constraint_status"] == "complete"
    assert readiness["blocking_open_obligation_ids"]
    assert frontier["best_current_path"]["argument_id"]
    assert frontier["global_missing_gates"]
    assert "obl-wisdom-coverage" not in readiness["blocking_open_obligation_ids"]
    assert "obl-target-god-concept" not in readiness["blocking_open_obligation_ids"]
    assert "obl-ontological-validity" not in readiness["blocking_open_obligation_ids"]
    assert "obl-ontological-consistency" not in readiness["blocking_open_obligation_ids"]
    assert "obl-teleological-bayes" not in readiness["blocking_open_obligation_ids"]
    assert "obl-cosmological-psr" not in readiness["blocking_open_obligation_ids"]
    assert "obl-counter-evil-hiddenness" not in readiness["blocking_open_obligation_ids"]
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]


def test_godproof_graph_tracks_sources_premises_and_counters(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    wisdom = json.loads((session_dir / "wisdom-map.json").read_text(encoding="utf-8"))
    graph = json.loads((session_dir / "proof-graph.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert len(wisdom["sources"]) >= 6
    assert len(wisdom["target_concepts"]) >= 3
    assert len(wisdom["wisdom_corpus"]) >= 8
    assert len(wisdom["arguments"]) >= 6
    assert len(wisdom["counterarguments"]) >= 3
    assert len(wisdom["proof_obligations"]) >= 6
    assert any(node["kind"] == "target" and node["id"] == "claim-god-exists" for node in graph["nodes"])
    assert any(node["kind"] == "proof_obligation" for node in graph["nodes"])
    assert "session_start" in transcript
    assert "session_end" in transcript


def test_godproof_tracks_human_wisdom_coverage(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    corpus = json.loads((session_dir / "wisdom-corpus.json").read_text(encoding="utf-8"))
    coverage = json.loads((session_dir / "coverage-matrix.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert corpus["status"] == "partial_human_wisdom_corpus"
    assert coverage["status"] == "covered"
    assert coverage["coverage_score"] == 1
    assert coverage["missing_domains"] == []
    assert coverage["thin_domains"] == []
    domains = {entry["domain"]: entry for entry in coverage["domains"]}
    assert domains["comparative_religion"]["status"] == "covered"
    assert domains["non_theistic_alternatives"]["status"] == "covered"
    assert domains["science_and_cosmology"]["status"] == "covered"
    assert "coverage_matrix_written" in transcript


def test_godproof_records_human_wisdom_intake_roadmap(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    roadmap = json.loads((session_dir / "human-wisdom-intake-roadmap.json").read_text(encoding="utf-8"))
    checks = json.loads((session_dir / "human-wisdom-intake-checks.json").read_text(encoding="utf-8"))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert roadmap["status"] == "contested"
    assert roadmap["roadmap"]["authorization_state"]["roadmap_recorded"] is True
    assert roadmap["roadmap"]["authorization_state"]["exhaustive_human_wisdom_claim_allowed"] is False
    assert roadmap["roadmap"]["authorization_state"]["proof_claim_allowed"] is False
    assert len(roadmap["roadmap"]["intake_lanes"]) == 7
    assert "counterpressure_ids" in roadmap["roadmap"]["entry_acceptance_schema"]["required_fields"]
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-current-coverage-matrix-linked"]["status"] == "complete"
    assert check_rows["check-required-domains-covered-by-roadmap"]["status"] == "complete"
    assert check_rows["check-current-corpus-entry-ids-recorded"]["status"] == "complete"
    assert check_rows["check-primary-source-seed-ledger-linked"]["status"] == "complete"
    assert check_rows["check-intake-lanes-have-evidence-types-and-gates"]["status"] == "complete"
    assert check_rows["check-entry-acceptance-schema-recorded"]["status"] == "complete"
    assert check_rows["check-open-intake-requirements-retained"]["status"] == "contested"
    assert check_rows["check-exhaustive-human-wisdom-not-claimed"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "human_wisdom_intake_checks_written" in transcript


def test_godproof_records_human_wisdom_primary_source_seed_ledger(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    ledger = json.loads(
        (session_dir / "human-wisdom-primary-source-seed-ledger.json").read_text(encoding="utf-8")
    )
    checks = json.loads((session_dir / "human-wisdom-primary-source-seed-checks.json").read_text(encoding="utf-8"))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert ledger["status"] == "contested"
    assert ledger["ledger"]["authorization_state"]["seed_locators_recorded"] is True
    assert ledger["ledger"]["authorization_state"]["primary_texts_ingested"] is False
    assert ledger["ledger"]["authorization_state"]["wisdom_corpus_extended"] is False
    assert ledger["ledger"]["authorization_state"]["exhaustive_human_wisdom_claim_allowed"] is False
    assert len(ledger["ledger"]["source_family_records"]) == 12
    assert all(
        row["ingestion_status"] == "locator_recorded_not_ingested"
        for row in ledger["ledger"]["source_family_records"]
    )
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-primary-source-seed-locators-recorded"]["status"] == "complete"
    assert check_rows["check-required-domain-seed-coverage"]["status"] == "complete"
    assert check_rows["check-tradition-diversity-seeded"]["status"] == "complete"
    assert check_rows["check-primary-source-extraction-queue-linked"]["status"] == "complete"
    assert check_rows["check-primary-source-ingestion-still-open"]["status"] == "contested"
    assert check_rows["check-primary-source-seed-ledger-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "human_wisdom_primary_source_seed_checks_written" in transcript


def test_godproof_records_human_wisdom_primary_source_extraction_queue(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    queue = json.loads(
        (session_dir / "human-wisdom-primary-source-extraction-queue.json").read_text(encoding="utf-8")
    )
    checks = json.loads(
        (session_dir / "human-wisdom-primary-source-extraction-checks.json").read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert queue["status"] == "contested"
    assert queue["queue"]["authorization_state"]["queue_recorded"] is True
    assert queue["queue"]["authorization_state"]["source_text_ingested"] is False
    assert queue["queue"]["authorization_state"]["wisdom_entries_materialized"] is False
    assert queue["queue"]["global_extraction_policy"]["raw_text_storage_allowed"] is False
    assert queue["queue"]["global_extraction_policy"]["max_verbatim_words_per_source"] == 25
    assert len(queue["queue"]["queue_items"]) == 12
    assert all(row["ingestion_status"] == "queued_not_ingested" for row in queue["queue"]["queue_items"])
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-primary-source-seed-ledger-linked"]["status"] == "complete"
    assert check_rows["check-every-seed-has-extraction-queue-item"]["status"] == "complete"
    assert check_rows["check-minimized-extraction-policy-recorded"]["status"] == "complete"
    assert check_rows["check-counterpressure-and-provenance-required"]["status"] == "complete"
    assert check_rows["check-summary-candidates-linked"]["status"] == "complete"
    assert check_rows["check-primary-source-extraction-still-open"]["status"] == "contested"
    assert check_rows["check-extraction-queue-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "human_wisdom_primary_source_extraction_checks_written" in transcript


def test_godproof_records_human_wisdom_primary_source_summary_candidates(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    candidates = json.loads(
        (session_dir / "human-wisdom-primary-source-summary-candidates.json").read_text(encoding="utf-8")
    )
    checks = json.loads(
        (session_dir / "human-wisdom-primary-source-summary-candidate-checks.json").read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert candidates["status"] == "contested"
    assert candidates["candidates"]["summary_policy"]["verbatim_source_text_stored"] is False
    assert candidates["candidates"]["summary_policy"]["max_verbatim_words_per_source"] == 0
    assert candidates["candidates"]["authorization_state"]["summary_candidates_recorded"] is True
    assert candidates["candidates"]["authorization_state"]["source_text_ingested"] is False
    assert candidates["candidates"]["authorization_state"]["wisdom_corpus_extended"] is False
    assert len(candidates["candidates"]["summary_candidates"]) == 12
    assert all(row["verbatim_words_stored"] == 0 for row in candidates["candidates"]["summary_candidates"])
    assert all(
        row["materialization_status"] == "candidate_not_in_corpus"
        for row in candidates["candidates"]["summary_candidates"]
    )
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-primary-source-extraction-queue-linked"]["status"] == "complete"
    assert check_rows["check-every-queue-item-has-summary-candidate"]["status"] == "complete"
    assert check_rows["check-paraphrase-only-summary-policy"]["status"] == "complete"
    assert check_rows["check-candidates-not-materialized-in-corpus"]["status"] == "complete"
    assert check_rows["check-counterpressure-edge-proposals-linked"]["status"] == "complete"
    assert check_rows["check-summary-candidate-promotion-still-open"]["status"] == "contested"
    assert check_rows["check-summary-candidates-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "human_wisdom_primary_source_summary_candidate_checks_written" in transcript


def test_godproof_records_human_wisdom_counterpressure_edge_proposals(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    proposals = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-proposals.json").read_text(encoding="utf-8")
    )
    checks = json.loads((session_dir / "human-wisdom-counterpressure-edge-checks.json").read_text(encoding="utf-8"))
    graph = json.loads((session_dir / "proof-graph.json").read_text(encoding="utf-8"))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert proposals["status"] == "contested"
    assert proposals["proposals"]["proposal_policy"]["proof_graph_write_allowed"] is False
    assert proposals["proposals"]["authorization_state"]["edge_proposals_recorded"] is True
    assert proposals["proposals"]["authorization_state"]["proof_graph_edges_materialized"] is False
    assert len(proposals["proposals"]["edge_proposals"]) == 12
    assert all(
        row["materialization_status"] == "proposal_not_in_proof_graph"
        for row in proposals["proposals"]["edge_proposals"]
    )
    graph_edge_sources = {edge["from"] for edge in graph["edges"]}
    assert all(
        row["source_node_id"] not in graph_edge_sources
        for row in proposals["proposals"]["edge_proposals"]
    )
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-summary-candidates-linked"]["status"] == "complete"
    assert check_rows["check-every-summary-candidate-has-edge-proposal"]["status"] == "complete"
    assert check_rows["check-counterpressure-targets-present"]["status"] == "complete"
    assert check_rows["check-proof-graph-materialization-still-open"]["status"] == "contested"
    assert check_rows["check-counterpressure-edge-proposals-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "human_wisdom_counterpressure_edge_proposals_written" in transcript
    assert "human_wisdom_counterpressure_edge_checks_written" in transcript


def test_godproof_records_human_wisdom_counterpressure_edge_review_queue(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    queue = json.loads((session_dir / "human-wisdom-counterpressure-edge-review-queue.json").read_text(encoding="utf-8"))
    checks = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-review-checks.json").read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert queue["status"] == "contested"
    assert queue["queue"]["authorization_state"]["review_queue_recorded"] is True
    assert queue["queue"]["authorization_state"]["proof_graph_edges_materialized"] is False
    assert queue["queue"]["authorization_state"]["materialization_authorized"] is False
    assert len(queue["queue"]["review_items"]) == 12
    assert all(row["review_status"] == "queued_not_reviewed" for row in queue["queue"]["review_items"])
    assert all(row["source_text_ingested"] is False for row in queue["queue"]["review_items"])
    assert all("relation_type" in row["required_review_axes"] for row in queue["queue"]["review_items"])
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-edge-proposals-linked"]["status"] == "complete"
    assert check_rows["check-every-edge-proposal-has-review-item"]["status"] == "complete"
    assert check_rows["check-review-items-remain-unreviewed"]["status"] == "complete"
    assert check_rows["check-edge-materialization-authorization-still-open"]["status"] == "contested"
    assert check_rows["check-review-queue-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "human_wisdom_counterpressure_edge_review_queue_written" in transcript
    assert "human_wisdom_counterpressure_edge_review_checks_written" in transcript


def test_godproof_records_human_wisdom_counterpressure_edge_review_rubric(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    rubric = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-review-rubric.json").read_text(encoding="utf-8")
    )
    checks = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-review-rubric-checks.json").read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert rubric["status"] == "contested"
    assert rubric["rubric"]["authorization_state"]["rubric_recorded"] is True
    assert rubric["rubric"]["authorization_state"]["review_items_completed"] is False
    assert rubric["rubric"]["authorization_state"]["materialization_authorized"] is False
    assert set(rubric["rubric"]["allowed_relation_types"]) >= {
        "supports",
        "pressures",
        "rebuts",
        "undercuts",
        "contextualizes",
        "irrelevant",
    }
    assert "accept" in rubric["rubric"]["decision_schema"]["allowed_decisions"]
    assert "reject" in rubric["rubric"]["decision_schema"]["allowed_decisions"]
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-review-queue-linked"]["status"] == "complete"
    assert check_rows["check-required-review-axes-covered"]["status"] == "complete"
    assert check_rows["check-decision-schema-recorded"]["status"] == "complete"
    assert check_rows["check-rubric-application-still-open"]["status"] == "contested"
    assert check_rows["check-rubric-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "human_wisdom_counterpressure_edge_review_rubric_written" in transcript
    assert "human_wisdom_counterpressure_edge_review_rubric_checks_written" in transcript


def test_godproof_records_human_wisdom_counterpressure_edge_review_defer_decisions(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    decisions = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-review-decisions.json").read_text(encoding="utf-8")
    )
    checks = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-review-decision-checks.json").read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert decisions["status"] == "contested"
    assert decisions["decisions"]["authorization_state"]["rubric_applied"] is True
    assert decisions["decisions"]["authorization_state"]["accepted_edges"] == 0
    assert decisions["decisions"]["authorization_state"]["materialization_authorized"] is False
    assert len(decisions["decisions"]["decision_records"]) == 12
    assert all(row["decision"] == "defer" for row in decisions["decisions"]["decision_records"])
    assert all(row["materialization_status"] == "deferred_not_in_proof_graph" for row in decisions["decisions"]["decision_records"])
    assert all(row["source_text_ingested"] is False for row in decisions["decisions"]["decision_records"])
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-review-rubric-linked"]["status"] == "complete"
    assert check_rows["check-review-queue-linked"]["status"] == "complete"
    assert check_rows["check-every-review-item-has-defer-decision"]["status"] == "complete"
    assert check_rows["check-no-proof-graph-materialization-from-decisions"]["status"] == "complete"
    assert check_rows["check-decision-ledger-still-contested"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "human_wisdom_counterpressure_edge_review_decisions_written" in transcript
    assert "human_wisdom_counterpressure_edge_review_decision_checks_written" in transcript


def test_godproof_records_human_wisdom_counterpressure_edge_resolution_packet(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    packet = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-resolution-packet.json").read_text(encoding="utf-8")
    )
    checks = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-resolution-checks.json").read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert packet["status"] == "contested"
    assert packet["packet"]["authorization_state"]["resolution_packet_recorded"] is True
    assert packet["packet"]["authorization_state"]["source_text_ingested"] is False
    assert packet["packet"]["authorization_state"]["all_resolution_tasks_complete"] is False
    assert packet["packet"]["authorization_state"]["materialization_authorized"] is False
    assert len(packet["packet"]["resolution_tasks"]) == 12
    assert all(row["task_status"] == "open" for row in packet["packet"]["resolution_tasks"])
    assert all("passage_locator" in row["required_resolution_fields"] for row in packet["packet"]["resolution_tasks"])
    assert all(
        "translation_provenance" in row["required_resolution_fields"]
        for row in packet["packet"]["resolution_tasks"]
    )
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-decision-ledger-linked"]["status"] == "complete"
    assert check_rows["check-every-defer-decision-has-resolution-task"]["status"] == "complete"
    assert check_rows["check-locator-and-provenance-fields-required"]["status"] == "complete"
    assert check_rows["check-resolution-tasks-still-open"]["status"] == "contested"
    assert check_rows["check-resolution-packet-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "human_wisdom_counterpressure_edge_resolution_packet_written" in transcript
    assert "human_wisdom_counterpressure_edge_resolution_checks_written" in transcript


def test_godproof_records_human_wisdom_counterpressure_edge_evidence_requests(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    queue = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-evidence-request-queue.json").read_text(encoding="utf-8")
    )
    checks = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-evidence-request-checks.json").read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert queue["status"] == "contested"
    assert queue["queue"]["authorization_state"]["request_queue_recorded"] is True
    assert queue["queue"]["authorization_state"]["evidence_fetched"] is False
    assert queue["queue"]["authorization_state"]["source_text_ingested"] is False
    assert queue["queue"]["authorization_state"]["materialization_authorized"] is False
    assert len(queue["queue"]["evidence_requests"]) == 12
    assert all(row["request_status"] == "queued_not_fetched" for row in queue["queue"]["evidence_requests"])
    assert all(row["source_text_ingested"] is False for row in queue["queue"]["evidence_requests"])
    assert all(
        {"passage_locator", "translation_provenance", "license_or_use_basis"}
        <= set(row["requested_evidence_fields"])
        for row in queue["queue"]["evidence_requests"]
    )
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-resolution-packet-linked"]["status"] == "complete"
    assert check_rows["check-every-open-resolution-task-has-evidence-request"]["status"] == "complete"
    assert check_rows["check-request-fields-cover-locator-provenance-license"]["status"] == "complete"
    assert check_rows["check-evidence-requests-not-fetched"]["status"] == "contested"
    assert check_rows["check-evidence-request-queue-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "human_wisdom_counterpressure_edge_evidence_request_queue_written" in transcript
    assert "human_wisdom_counterpressure_edge_evidence_request_checks_written" in transcript


def test_godproof_records_human_wisdom_counterpressure_edge_evidence_acquisition_manifest(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    manifest = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-evidence-acquisition-manifest.json").read_text(
            encoding="utf-8"
        )
    )
    checks = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-evidence-acquisition-checks.json").read_text(
            encoding="utf-8"
        )
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert manifest["status"] == "contested"
    assert manifest["manifest"]["authorization_state"]["acquisition_manifest_recorded"] is True
    assert manifest["manifest"]["authorization_state"]["fetch_executed"] is False
    assert manifest["manifest"]["authorization_state"]["hashes_computed"] is False
    assert manifest["manifest"]["authorization_state"]["source_text_ingested"] is False
    assert manifest["manifest"]["authorization_state"]["materialization_authorized"] is False
    assert len(manifest["manifest"]["acquisition_items"]) == 12
    assert all(row["fetch_status"] == "planned_not_executed" for row in manifest["manifest"]["acquisition_items"])
    assert all(row["hash_status"] == "not_computed" for row in manifest["manifest"]["acquisition_items"])
    assert all(row["source_text_ingested"] is False for row in manifest["manifest"]["acquisition_items"])
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-evidence-request-queue-linked"]["status"] == "complete"
    assert check_rows["check-every-request-has-acquisition-item"]["status"] == "complete"
    assert check_rows["check-acquisition-items-cover-requested-fields"]["status"] == "complete"
    assert check_rows["check-fetch-and-hash-still-unexecuted"]["status"] == "contested"
    assert check_rows["check-acquisition-manifest-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "human_wisdom_counterpressure_edge_evidence_acquisition_manifest_written" in transcript
    assert "human_wisdom_counterpressure_edge_evidence_acquisition_checks_written" in transcript


def test_godproof_records_human_wisdom_counterpressure_edge_metadata_receipt_schema(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    schema = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-schema.json").read_text(encoding="utf-8")
    )
    checks = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-checks.json").read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert schema["status"] == "contested"
    assert schema["schema"]["authorization_state"]["schema_recorded"] is True
    assert schema["schema"]["authorization_state"]["receipts_materialized"] is False
    assert schema["schema"]["authorization_state"]["source_text_ingested"] is False
    assert schema["schema"]["authorization_state"]["materialization_authorized"] is False
    assert len(schema["schema"]["receipt_templates"]) == 12
    assert all(row["receipt_status"] == "template_not_materialized" for row in schema["schema"]["receipt_templates"])
    assert all(row["metadata_hash"] is None for row in schema["schema"]["receipt_templates"])
    required_fields = set(schema["schema"]["receipt_schema"]["required_fields"])
    assert {"passage_locator", "translation_provenance", "metadata_hash", "license_or_use_basis"} <= required_fields
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-acquisition-manifest-linked"]["status"] == "complete"
    assert check_rows["check-every-acquisition-item-has-receipt-template"]["status"] == "complete"
    assert check_rows["check-receipt-schema-requires-locator-provenance-hash"]["status"] == "complete"
    assert check_rows["check-receipts-still-unmaterialized"]["status"] == "contested"
    assert check_rows["check-receipt-schema-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "human_wisdom_counterpressure_edge_metadata_receipt_schema_written" in transcript
    assert "human_wisdom_counterpressure_edge_metadata_receipt_checks_written" in transcript


def test_godproof_queues_human_wisdom_counterpressure_edge_metadata_receipt_review(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    queue = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-review-queue.json").read_text(
            encoding="utf-8"
        )
    )
    checks = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-review-checks.json").read_text(
            encoding="utf-8"
        )
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert queue["status"] == "contested"
    assert queue["queue"]["authorization_state"]["review_queue_recorded"] is True
    assert queue["queue"]["authorization_state"]["receipts_reviewed"] is False
    assert queue["queue"]["authorization_state"]["receipts_approved"] is False
    assert queue["queue"]["authorization_state"]["proof_graph_edges_materialized"] is False
    assert queue["queue"]["authorization_state"]["materialization_authorized"] is False
    assert len(queue["queue"]["review_items"]) == 12
    assert all(row["review_status"] == "queued_not_reviewed" for row in queue["queue"]["review_items"])
    assert all(row["receipt_status"] == "template_not_materialized" for row in queue["queue"]["review_items"])
    assert all(row["metadata_hash"] is None for row in queue["queue"]["review_items"])
    assert all(row["approval_status"] == "not_approved" for row in queue["queue"]["review_items"])
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-receipt-schema-linked"]["status"] == "complete"
    assert check_rows["check-every-receipt-template-has-review-item"]["status"] == "complete"
    assert check_rows["check-review-items-require-hash-and-provenance"]["status"] == "complete"
    assert check_rows["check-receipt-review-still-unperformed"]["status"] == "contested"
    assert check_rows["check-receipt-review-queue-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "human_wisdom_counterpressure_edge_metadata_receipt_review_queue_written" in transcript
    assert "human_wisdom_counterpressure_edge_metadata_receipt_review_checks_written" in transcript


def test_godproof_records_human_wisdom_counterpressure_edge_metadata_receipt_review_rubric(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    rubric = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-review-rubric.json").read_text(
            encoding="utf-8"
        )
    )
    checks = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-review-rubric-checks.json").read_text(
            encoding="utf-8"
        )
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert rubric["status"] == "contested"
    assert rubric["rubric"]["authorization_state"]["rubric_recorded"] is True
    assert rubric["rubric"]["authorization_state"]["review_items_completed"] is False
    assert rubric["rubric"]["authorization_state"]["receipt_approvals_recorded"] is False
    assert rubric["rubric"]["authorization_state"]["proof_graph_edges_materialized"] is False
    assert rubric["rubric"]["authorization_state"]["materialization_authorized"] is False
    covered_axes = set(rubric["rubric"]["covered_review_axes"])
    assert {"metadata_hash_integrity", "locator_sufficiency", "translation_provenance", "license_or_use_basis"} <= covered_axes
    assert {"approve", "reject", "defer", "request_metadata_refetch"} <= set(
        rubric["rubric"]["decision_schema"]["allowed_decisions"]
    )
    assert rubric["rubric"]["materialization_gate"]["requires_materialized_receipt"] is True
    assert rubric["rubric"]["materialization_gate"]["requires_metadata_hash"] is True
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-receipt-review-queue-linked"]["status"] == "complete"
    assert check_rows["check-required-review-fields-covered"]["status"] == "complete"
    assert check_rows["check-receipt-decision-schema-recorded"]["status"] == "complete"
    assert check_rows["check-receipt-rubric-application-still-open"]["status"] == "contested"
    assert check_rows["check-receipt-rubric-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "human_wisdom_counterpressure_edge_metadata_receipt_review_rubric_written" in transcript
    assert "human_wisdom_counterpressure_edge_metadata_receipt_review_rubric_checks_written" in transcript


def test_godproof_records_human_wisdom_counterpressure_edge_metadata_receipt_review_defer_decisions(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    decisions = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-review-decisions.json").read_text(
            encoding="utf-8"
        )
    )
    checks = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-review-decision-checks.json").read_text(
            encoding="utf-8"
        )
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert decisions["status"] == "contested"
    assert decisions["decisions"]["authorization_state"]["rubric_applied"] is True
    assert decisions["decisions"]["authorization_state"]["approved_receipts"] == 0
    assert decisions["decisions"]["authorization_state"]["receipt_approvals_recorded"] is False
    assert decisions["decisions"]["authorization_state"]["proof_graph_edges_materialized"] is False
    assert decisions["decisions"]["authorization_state"]["materialization_authorized"] is False
    assert len(decisions["decisions"]["decision_records"]) == 12
    assert all(row["decision"] == "defer" for row in decisions["decisions"]["decision_records"])
    assert all(row["approval_status"] == "not_approved" for row in decisions["decisions"]["decision_records"])
    assert all(row["metadata_hash"] is None for row in decisions["decisions"]["decision_records"])
    assert all(
        row["materialization_status"] == "deferred_receipt_not_evidence"
        for row in decisions["decisions"]["decision_records"]
    )
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-receipt-review-rubric-linked"]["status"] == "complete"
    assert check_rows["check-receipt-review-queue-linked"]["status"] == "complete"
    assert check_rows["check-every-receipt-review-item-has-defer-decision"]["status"] == "complete"
    assert check_rows["check-no-receipt-approval-or-proof-materialization"]["status"] == "complete"
    assert check_rows["check-receipt-decision-ledger-still-contested"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "human_wisdom_counterpressure_edge_metadata_receipt_review_decisions_written" in transcript
    assert "human_wisdom_counterpressure_edge_metadata_receipt_review_decision_checks_written" in transcript


def test_godproof_records_human_wisdom_counterpressure_edge_metadata_receipt_resolution_packet(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    packet = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-resolution-packet.json").read_text(
            encoding="utf-8"
        )
    )
    checks = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-resolution-checks.json").read_text(
            encoding="utf-8"
        )
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert packet["status"] == "contested"
    assert packet["packet"]["authorization_state"]["resolution_packet_recorded"] is True
    assert packet["packet"]["authorization_state"]["metadata_receipts_materialized"] is False
    assert packet["packet"]["authorization_state"]["metadata_hashes_recorded"] is False
    assert packet["packet"]["authorization_state"]["all_resolution_tasks_complete"] is False
    assert packet["packet"]["authorization_state"]["materialization_authorized"] is False
    assert len(packet["packet"]["resolution_tasks"]) == 12
    assert all(row["task_status"] == "open" for row in packet["packet"]["resolution_tasks"])
    assert all(row["metadata_hash"] is None for row in packet["packet"]["resolution_tasks"])
    assert all("metadata_hash" in row["required_resolution_fields"] for row in packet["packet"]["resolution_tasks"])
    assert all("passage_locator" in row["required_resolution_fields"] for row in packet["packet"]["resolution_tasks"])
    assert all(
        "translation_provenance" in row["required_resolution_fields"]
        for row in packet["packet"]["resolution_tasks"]
    )
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-receipt-decision-ledger-linked"]["status"] == "complete"
    assert check_rows["check-every-deferred-receipt-decision-has-resolution-task"]["status"] == "complete"
    assert check_rows["check-receipt-resolution-fields-required"]["status"] == "complete"
    assert check_rows["check-receipt-resolution-tasks-still-open"]["status"] == "contested"
    assert check_rows["check-receipt-resolution-packet-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "human_wisdom_counterpressure_edge_metadata_receipt_resolution_packet_written" in transcript
    assert "human_wisdom_counterpressure_edge_metadata_receipt_resolution_checks_written" in transcript


def test_godproof_records_human_wisdom_counterpressure_edge_metadata_receipt_evidence_requests(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    queue = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-evidence-request-queue.json").read_text(
            encoding="utf-8"
        )
    )
    checks = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-evidence-request-checks.json").read_text(
            encoding="utf-8"
        )
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert queue["status"] == "contested"
    assert queue["queue"]["authorization_state"]["request_queue_recorded"] is True
    assert queue["queue"]["authorization_state"]["evidence_fetched"] is False
    assert queue["queue"]["authorization_state"]["metadata_hashes_recorded"] is False
    assert queue["queue"]["authorization_state"]["source_text_ingested"] is False
    assert queue["queue"]["authorization_state"]["materialization_authorized"] is False
    assert len(queue["queue"]["evidence_requests"]) == 12
    assert all(row["request_status"] == "queued_not_fetched" for row in queue["queue"]["evidence_requests"])
    assert all(row["metadata_hash"] is None for row in queue["queue"]["evidence_requests"])
    assert all(row["source_text_ingested"] is False for row in queue["queue"]["evidence_requests"])
    assert all(
        {"passage_locator", "translation_provenance", "license_or_use_basis", "metadata_hash"}
        <= set(row["requested_evidence_fields"])
        for row in queue["queue"]["evidence_requests"]
    )
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-receipt-resolution-packet-linked"]["status"] == "complete"
    assert check_rows["check-every-open-receipt-resolution-task-has-evidence-request"]["status"] == "complete"
    assert check_rows["check-receipt-request-fields-cover-locator-provenance-license-hash"]["status"] == "complete"
    assert check_rows["check-receipt-evidence-requests-not-fetched"]["status"] == "contested"
    assert check_rows["check-receipt-evidence-request-queue-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "human_wisdom_counterpressure_edge_metadata_receipt_evidence_request_queue_written" in transcript
    assert "human_wisdom_counterpressure_edge_metadata_receipt_evidence_request_checks_written" in transcript


def test_godproof_records_human_wisdom_counterpressure_edge_metadata_receipt_acquisition_manifest(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    manifest = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-acquisition-manifest.json").read_text(
            encoding="utf-8"
        )
    )
    checks = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-acquisition-checks.json").read_text(
            encoding="utf-8"
        )
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert manifest["status"] == "contested"
    assert manifest["manifest"]["authorization_state"]["acquisition_manifest_recorded"] is True
    assert manifest["manifest"]["authorization_state"]["fetch_executed"] is False
    assert manifest["manifest"]["authorization_state"]["metadata_hashes_computed"] is False
    assert manifest["manifest"]["authorization_state"]["source_text_ingested"] is False
    assert manifest["manifest"]["authorization_state"]["materialization_authorized"] is False
    assert len(manifest["manifest"]["acquisition_items"]) == 12
    assert all(row["fetch_status"] == "planned_not_executed" for row in manifest["manifest"]["acquisition_items"])
    assert all(row["hash_status"] == "not_computed" for row in manifest["manifest"]["acquisition_items"])
    assert all(row["metadata_hash"] is None for row in manifest["manifest"]["acquisition_items"])
    assert all(row["source_text_ingested"] is False for row in manifest["manifest"]["acquisition_items"])
    assert all(
        "compute metadata hash after fetch" in row["acquisition_steps"]
        for row in manifest["manifest"]["acquisition_items"]
    )
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-receipt-evidence-request-queue-linked"]["status"] == "complete"
    assert check_rows["check-every-receipt-request-has-acquisition-item"]["status"] == "complete"
    assert check_rows["check-receipt-acquisition-items-cover-requested-fields"]["status"] == "complete"
    assert check_rows["check-receipt-fetch-and-hash-still-unexecuted"]["status"] == "contested"
    assert check_rows["check-receipt-acquisition-manifest-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "human_wisdom_counterpressure_edge_metadata_receipt_acquisition_manifest_written" in transcript
    assert "human_wisdom_counterpressure_edge_metadata_receipt_acquisition_checks_written" in transcript


def test_godproof_records_human_wisdom_counterpressure_edge_metadata_receipt_acquisition_hash_runbook(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    runbook = json.loads(
        (
            session_dir
            / "human-wisdom-counterpressure-edge-metadata-receipt-acquisition-hash-runbook.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "human-wisdom-counterpressure-edge-metadata-receipt-acquisition-hash-runbook-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert runbook["status"] == "contested"
    assert runbook["runbook"]["authorization_state"]["commands_recorded"] is True
    assert runbook["runbook"]["authorization_state"]["commands_executed"] is False
    assert runbook["runbook"]["authorization_state"]["fetch_allowed"] is False
    assert runbook["runbook"]["cache_policy"]["repo_storage_allowed"] is False
    assert runbook["runbook"]["hash_manifest_schema"]["manifest_status"] == "not_materialized"
    assert len(runbook["runbook"]["steps"]) == 12
    assert all(step["execution_status"] == "not_executed" for step in runbook["runbook"]["steps"])
    assert all("shasum -a 256" in step["hash_command_template"] for step in runbook["runbook"]["steps"])
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-receipt-acquisition-manifest-linked"]["status"] == "complete"
    assert check_rows["check-every-receipt-acquisition-item-has-runbook-step"]["status"] == "complete"
    assert check_rows["check-receipt-hash-manifest-schema-recorded"]["status"] == "complete"
    assert check_rows["check-receipt-hash-command-templates-recorded-not-executed"]["status"] == "complete"
    assert check_rows["check-receipt-required-log-events-recorded"]["status"] == "complete"
    assert check_rows["check-receipt-cache-retention-and-prune-step-recorded"]["status"] == "complete"
    assert check_rows["check-receipt-acquisition-still-open"]["status"] == "contested"
    assert check_rows["check-receipt-acquisition-runbook-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "human_wisdom_counterpressure_edge_metadata_receipt_acquisition_hash_runbook_written" in transcript
    assert "human_wisdom_counterpressure_edge_metadata_receipt_acquisition_hash_runbook_checks_written" in transcript


def test_godproof_records_human_wisdom_counterpressure_edge_metadata_receipt_authorization_packet(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    packet = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-authorization-packet.json").read_text(
            encoding="utf-8"
        )
    )
    checks = json.loads(
        (session_dir / "human-wisdom-counterpressure-edge-metadata-receipt-authorization-checks.json").read_text(
            encoding="utf-8"
        )
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert packet["status"] == "contested"
    assert packet["packet"]["authorization_state"]["authorization_packet_recorded"] is True
    assert packet["packet"]["authorization_state"]["fetch_allowed"] is False
    assert packet["packet"]["authorization_state"]["hash_commands_allowed"] is False
    assert packet["packet"]["authorization_state"]["receipt_materialization_allowed"] is False
    assert packet["packet"]["authorization_state"]["proof_graph_edges_materialized"] is False
    assert len(packet["packet"]["authorization_records"]) == 12
    assert all(
        row["authorization_decision"].startswith("not_authorized_until_")
        for row in packet["packet"]["authorization_records"]
    )
    assert all(row["manual_review_required"] is True for row in packet["packet"]["authorization_records"])
    assert all(row["source_text_ingested"] is False for row in packet["packet"]["authorization_records"])
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-receipt-hash-runbook-linked"]["status"] == "complete"
    assert check_rows["check-every-runbook-step-has-authorization-record"]["status"] == "complete"
    assert check_rows["check-required-authorization-actions-recorded"]["status"] == "complete"
    assert check_rows["check-receipt-fetch-and-hash-not-authorized"]["status"] == "contested"
    assert check_rows["check-receipt-authorization-packet-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "human_wisdom_counterpressure_edge_metadata_receipt_authorization_packet_written" in transcript
    assert "human_wisdom_counterpressure_edge_metadata_receipt_authorization_checks_written" in transcript


def test_godproof_queues_human_wisdom_counterpressure_edge_metadata_receipt_authorization_review(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    queue = json.loads(
        (
            session_dir
            / "human-wisdom-counterpressure-edge-metadata-receipt-authorization-review-queue.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "human-wisdom-counterpressure-edge-metadata-receipt-authorization-review-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert queue["status"] == "contested"
    assert queue["queue"]["authorization_state"]["review_queue_recorded"] is True
    assert queue["queue"]["authorization_state"]["authorization_reviews_completed"] is False
    assert queue["queue"]["authorization_state"]["fetch_allowed"] is False
    assert queue["queue"]["authorization_state"]["hash_commands_allowed"] is False
    assert queue["queue"]["authorization_state"]["receipt_materialization_allowed"] is False
    assert len(queue["queue"]["review_items"]) == 12
    assert all(row["review_status"] == "queued_not_reviewed" for row in queue["queue"]["review_items"])
    assert all(
        row["authorization_decision"].startswith("not_authorized_until_")
        for row in queue["queue"]["review_items"]
    )
    assert all("license_or_use_basis" in row["required_review_fields"] for row in queue["queue"]["review_items"])
    assert all("cache_retention_rule" in row["required_review_fields"] for row in queue["queue"]["review_items"])
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-authorization-packet-linked"]["status"] == "complete"
    assert check_rows["check-every-authorization-record-has-review-item"]["status"] == "complete"
    assert check_rows["check-authorization-review-items-remain-unreviewed"]["status"] == "complete"
    assert check_rows["check-receipt-fetch-and-hash-authorization-still-open"]["status"] == "contested"
    assert check_rows["check-authorization-review-queue-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "human_wisdom_counterpressure_edge_metadata_receipt_authorization_review_queue_written" in transcript
    assert "human_wisdom_counterpressure_edge_metadata_receipt_authorization_review_checks_written" in transcript


def test_godproof_defines_target_concept_and_updates_obligation(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    concepts = json.loads((session_dir / "target-concepts.json").read_text(encoding="utf-8"))
    checks = json.loads((session_dir / "definition-checks.json").read_text(encoding="utf-8"))
    obligations = json.loads((session_dir / "formal-obligations.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    target = next(c for c in concepts["concepts"] if c["id"] == concepts["proof_target_id"])
    assert target["attributes"]["personhood"] is True
    assert checks["status"] == "complete"
    rows = {row["id"]: row for row in obligations["obligations"]}
    assert rows["obl-target-god-concept"]["status"] == "complete"
    assert rows["obl-target-god-concept"]["evidence_artifact"] == "definition-checks.json"
    assert "definition_checks_written" in transcript


def test_godproof_checks_modal_validity_bridge(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    derivation = json.loads((session_dir / "modal-derivation.json").read_text(encoding="utf-8"))
    checks = json.loads((session_dir / "modal-validity-checks.json").read_text(encoding="utf-8"))
    obligations = json.loads((session_dir / "formal-obligations.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert derivation["status"] == "encoded"
    assert derivation["derivation"]["conclusion"] == "G"
    assert checks["status"] == "complete"
    assert checks["scope"] == "conditional_validity_not_soundness"
    rows = {row["id"]: row for row in obligations["obligations"]}
    assert rows["obl-ontological-validity"]["status"] == "complete"
    assert rows["obl-ontological-validity"]["evidence_artifact"] == "modal-validity-checks.json"
    assert "modal_validity_checks_written" in transcript


def test_godproof_checks_modal_consistency_and_collapse(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    checks = json.loads((session_dir / "modal-consistency-checks.json").read_text(encoding="utf-8"))
    obligations = json.loads((session_dir / "formal-obligations.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert checks["status"] == "complete"
    assert checks["scope"] == "minimal_modal_bridge_consistency"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-s5-frame"]["status"] == "complete"
    assert check_rows["check-assumption-satisfiable"]["result"] is True
    assert check_rows["check-minimal-modal-collapse-not-introduced"]["status"] == "complete"
    rows = {row["id"]: row for row in obligations["obligations"]}
    assert rows["obl-ontological-consistency"]["status"] == "complete"
    assert rows["obl-ontological-consistency"]["evidence_artifact"] == "modal-consistency-checks.json"
    assert "modal_consistency_checks_written" in transcript


def test_godproof_records_ontological_soundness_as_contested(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    dossier = json.loads((session_dir / "ontological-soundness-dossier.json").read_text(encoding="utf-8"))
    checks = json.loads((session_dir / "ontological-soundness-checks.json").read_text(encoding="utf-8"))
    obligations = json.loads((session_dir / "formal-obligations.json").read_text(encoding="utf-8"))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert dossier["status"] == "contested"
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-supporting-considerations-present"]["status"] == "complete"
    assert check_rows["check-critical-considerations-present"]["status"] == "complete"
    assert check_rows["check-unresolved-parodies-retained"]["status"] == "contested"
    assert check_rows["check-soundness-not-promoted"]["status"] == "contested"
    assert check_rows["check-attribute-coherence-ledger-linked"]["status"] == "complete"
    assert check_rows["check-possibility-premise-ladder-linked"]["status"] == "complete"
    assert check_rows["check-coherent-conceivability-model-linked"]["status"] == "complete"
    assert check_rows["check-metaphysical-possibility-bridge-linked"]["status"] == "complete"
    assert check_rows["check-possible-necessary-existence-bridge-linked"]["status"] == "complete"
    assert check_rows["check-definition-smuggling-audit-linked"]["status"] == "complete"
    assert check_rows["check-rival-necessary-parity-audit-linked"]["status"] == "complete"
    assert check_rows["check-positive-property-filter-audit-linked"]["status"] == "complete"
    assert check_rows["check-positive-grounding-audit-linked"]["status"] == "complete"
    assert check_rows["check-moral-perfection-grounding-audit-linked"]["status"] == "complete"
    assert check_rows["check-evil-hiddenness-moral-pressure-audit-linked"]["status"] == "complete"
    assert check_rows["check-evidential-evil-probability-audit-linked"]["status"] == "complete"
    assert check_rows["check-evidential-evil-likelihood-ledger-linked"]["status"] == "complete"
    assert check_rows["check-evidential-evil-dependence-model-linked"]["status"] == "complete"
    assert check_rows["check-evidential-evil-calibration-ledger-linked"]["status"] == "complete"
    assert check_rows["check-evidential-evil-case-corpus-linked"]["status"] == "complete"
    assert check_rows["check-evidential-evil-reviewed-case-records-linked"]["status"] == "complete"
    assert check_rows["check-evidential-evil-empirical-expansion-linked"]["status"] == "complete"
    assert check_rows["check-evidential-evil-primary-dataset-selection-linked"]["status"] == "complete"
    assert check_rows["check-evidential-evil-dataset-ingestion-manifest-linked"]["status"] == "complete"
    assert check_rows["check-evidential-evil-attribution-template-linked"]["status"] == "complete"
    assert check_rows["check-evidential-evil-license-decision-packet-linked"]["status"] == "complete"
    assert check_rows["check-evidential-evil-source-acquisition-hash-runbook-linked"]["status"] == "complete"
    assert check_rows["check-evidential-evil-suppression-report-template-linked"]["status"] == "complete"
    assert check_rows["check-evidential-evil-source-version-hash-preflight-linked"]["status"] == "complete"
    assert check_rows["check-evidential-evil-derived-aggregate-schema-linked"]["status"] == "complete"
    assert check_rows["check-evidential-evil-microdata-minimization-linked"]["status"] == "complete"
    assert check_rows["check-evidential-evil-license-privacy-review-linked"]["status"] == "complete"
    assert "attribute-coherence-checks.json" in checks["related_artifacts"]
    assert "coherent-conceivability-checks.json" in checks["related_artifacts"]
    assert "metaphysical-possibility-checks.json" in checks["related_artifacts"]
    assert "definition-smuggling-checks.json" in checks["related_artifacts"]
    assert "evidential-evil-attribution-template-checks.json" in checks["related_artifacts"]
    assert "evidential-evil-license-decision-checks.json" in checks["related_artifacts"]
    assert "evidential-evil-source-acquisition-hash-runbook-checks.json" in checks["related_artifacts"]
    assert "evidential-evil-suppression-report-template-checks.json" in checks["related_artifacts"]
    assert "evidential-evil-source-version-hash-preflight-checks.json" in checks["related_artifacts"]
    assert "evidential-evil-derived-aggregate-schema-checks.json" in checks["related_artifacts"]
    assert "evidential-evil-microdata-minimization-checks.json" in checks["related_artifacts"]
    assert "evidential-evil-license-privacy-checks.json" in checks["related_artifacts"]
    assert "evidential-evil-dataset-ingestion-checks.json" in checks["related_artifacts"]
    assert "evidential-evil-primary-dataset-selection-checks.json" in checks["related_artifacts"]
    assert "evidential-evil-empirical-expansion-checks.json" in checks["related_artifacts"]
    assert "evidential-evil-reviewed-case-records-checks.json" in checks["related_artifacts"]
    assert "evidential-evil-case-corpus-checks.json" in checks["related_artifacts"]
    assert "evidential-evil-calibration-checks.json" in checks["related_artifacts"]
    assert "evidential-evil-dependence-checks.json" in checks["related_artifacts"]
    assert "evidential-evil-likelihood-checks.json" in checks["related_artifacts"]
    assert "evidential-evil-probability-checks.json" in checks["related_artifacts"]
    assert "evil-hiddenness-moral-pressure-checks.json" in checks["related_artifacts"]
    assert "moral-perfection-grounding-checks.json" in checks["related_artifacts"]
    assert "positive-grounding-checks.json" in checks["related_artifacts"]
    assert "positive-property-filter-checks.json" in checks["related_artifacts"]
    assert "rival-necessary-parity-checks.json" in checks["related_artifacts"]
    assert "possible-necessary-existence-checks.json" in checks["related_artifacts"]
    assert "possibility-premise-checks.json" in checks["related_artifacts"]
    rows = {row["id"]: row for row in obligations["obligations"]}
    assert rows["obl-ontological-soundness"]["status"] == "contested"
    assert rows["obl-ontological-soundness"]["evidence_artifact"] == "ontological-soundness-checks.json"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_checks_written" in transcript


def test_godproof_builds_ontological_soundness_parody_discriminator_matrix(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    matrix = json.loads((session_dir / "ontological-soundness-parody-discriminator-matrix.json").read_text(
        encoding="utf-8"
    ))
    checks = json.loads((session_dir / "ontological-soundness-parody-discriminator-checks.json").read_text(
        encoding="utf-8"
    ))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert matrix["status"] == "contested"
    assert matrix["matrix"]["input_dossier_id"] == "ontological-soundness-dossier-v0"
    assert matrix["matrix"]["target_obligation_id"] == "obl-ontological-soundness"
    assert matrix["matrix"]["authorization_state"]["matrix_recorded"] is True
    assert matrix["matrix"]["authorization_state"]["parody_pressure_resolved"] is False
    assert matrix["matrix"]["authorization_state"]["proof_claim_allowed"] is False
    assert len(matrix["matrix"]["discriminator_rows"]) == 3
    rows = {row["parody_test_id"]: row for row in matrix["matrix"]["discriminator_rows"]}
    assert rows["maximally_great_island"]["discriminator_status"] == "candidate_resolved"
    assert rows["necessarily_existing_bad_god"]["discriminator_status"] == "contested"
    assert rows["necessary_impersonal_ultimate"]["discriminator_status"] == "contested"
    assert "positive-property-filter-checks.json" in rows["necessarily_existing_bad_god"]["required_artifacts"]
    assert all(row["proof_evidence_materialized"] is False for row in matrix["matrix"]["discriminator_rows"])
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-soundness-dossier-linked"]["status"] == "complete"
    assert check_rows["check-every-parody-test-has-discriminator-row"]["status"] == "complete"
    assert check_rows["check-unresolved-parodies-have-contested-discriminators"]["status"] == "complete"
    assert check_rows["check-open-discriminators-retained"]["status"] == "contested"
    assert check_rows["check-discriminator-matrix-not-promoted-to-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_parody_discriminator_matrix_written" in transcript
    assert "ontological_soundness_parody_discriminator_checks_written" in transcript


def test_godproof_records_bad_god_discharge_criteria(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    criteria = json.loads((session_dir / "ontological-soundness-bad-god-discharge-criteria.json").read_text(
        encoding="utf-8"
    ))
    checks = json.loads((session_dir / "ontological-soundness-bad-god-discharge-checks.json").read_text(
        encoding="utf-8"
    ))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert criteria["status"] == "contested"
    assert criteria["criteria"]["target_parody_test_id"] == "necessarily_existing_bad_god"
    assert criteria["criteria"]["input_discriminator_matrix_id"] == (
        "ontological-soundness-parody-discriminator-matrix-v0"
    )
    assert criteria["criteria"]["authorization_state"]["criteria_recorded"] is True
    assert criteria["criteria"]["authorization_state"]["bad_god_parody_discharged"] is False
    assert criteria["criteria"]["authorization_state"]["proof_claim_allowed"] is False
    assert len(criteria["criteria"]["discharge_requirements"]) == 5
    requirement_ids = {row["requirement_id"] for row in criteria["criteria"]["discharge_requirements"]}
    assert {
        "positive-property-filter-complete",
        "positive-grounding-complete",
        "moral-perfection-grounding-complete",
        "evil-hiddenness-pressure-complete",
        "rival-parity-complete",
    } <= requirement_ids
    assert all(row["requirement_status"] == "contested" for row in criteria["criteria"]["discharge_requirements"])
    assert all(row["proof_evidence_materialized"] is False for row in criteria["criteria"]["discharge_requirements"])
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-parody-discriminator-linked"]["status"] == "complete"
    assert check_rows["check-bad-god-row-selected"]["status"] == "complete"
    assert check_rows["check-required-artifacts-covered"]["status"] == "complete"
    assert check_rows["check-discharge-requirements-remain-contested"]["status"] == "contested"
    assert check_rows["check-bad-god-discharge-not-promoted-to-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_discharge_criteria_written" in transcript
    assert "ontological_soundness_bad_god_discharge_checks_written" in transcript


def test_godproof_queues_bad_god_discharge_tasks(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    queue = json.loads((session_dir / "ontological-soundness-bad-god-discharge-task-queue.json").read_text(
        encoding="utf-8"
    ))
    checks = json.loads((session_dir / "ontological-soundness-bad-god-discharge-task-checks.json").read_text(
        encoding="utf-8"
    ))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert queue["status"] == "contested"
    assert queue["queue"]["input_criteria_id"] == "ontological-soundness-bad-god-discharge-criteria-v0"
    assert queue["queue"]["target_parody_test_id"] == "necessarily_existing_bad_god"
    assert queue["queue"]["authorization_state"]["task_queue_recorded"] is True
    assert queue["queue"]["authorization_state"]["tasks_executed"] is False
    assert queue["queue"]["authorization_state"]["bad_god_parody_discharged"] is False
    assert queue["queue"]["authorization_state"]["proof_claim_allowed"] is False
    assert len(queue["queue"]["task_items"]) == 5
    assert all(row["task_status"] == "queued_not_executed" for row in queue["queue"]["task_items"])
    assert all(row["proof_evidence_materialized"] is False for row in queue["queue"]["task_items"])
    assert all(row["verifier_commands"] for row in queue["queue"]["task_items"])
    assert all(row["acceptance_criteria"] for row in queue["queue"]["task_items"])
    task_ids = {row["task_id"] for row in queue["queue"]["task_items"]}
    assert {
        "task-positive-property-filter-complete",
        "task-positive-grounding-complete",
        "task-moral-perfection-grounding-complete",
        "task-evil-hiddenness-pressure-complete",
        "task-rival-parity-complete",
    } <= task_ids
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-bad-god-criteria-linked"]["status"] == "complete"
    assert check_rows["check-every-discharge-requirement-has-task"]["status"] == "complete"
    assert check_rows["check-tasks-have-verifiers-and-acceptance-criteria"]["status"] == "complete"
    assert check_rows["check-bad-god-tasks-remain-unexecuted"]["status"] == "complete"
    assert check_rows["check-task-queue-not-promoted-to-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_discharge_task_queue_written" in transcript
    assert "ontological_soundness_bad_god_discharge_task_checks_written" in transcript


def test_godproof_builds_bad_god_task_dependency_graph(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    graph = json.loads((session_dir / "ontological-soundness-bad-god-task-dependency-graph.json").read_text(
        encoding="utf-8"
    ))
    checks = json.loads((session_dir / "ontological-soundness-bad-god-task-dependency-checks.json").read_text(
        encoding="utf-8"
    ))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert graph["status"] == "contested"
    assert graph["graph"]["input_task_queue_id"] == "ontological-soundness-bad-god-discharge-task-queue-v0"
    assert graph["graph"]["target_parody_test_id"] == "necessarily_existing_bad_god"
    assert graph["graph"]["authorization_state"]["dependency_graph_recorded"] is True
    assert graph["graph"]["authorization_state"]["tasks_executed"] is False
    assert graph["graph"]["authorization_state"]["proof_claim_allowed"] is False
    assert len(graph["graph"]["nodes"]) == 5
    assert len(graph["graph"]["edges"]) >= 4
    assert all(node["task_status"] == "queued_not_executed" for node in graph["graph"]["nodes"])
    assert all(node["proof_evidence_materialized"] is False for node in graph["graph"]["nodes"])
    edge_pairs = {(edge["from_task_id"], edge["to_task_id"]) for edge in graph["graph"]["edges"]}
    assert (
        "task-moral-perfection-grounding-complete",
        "task-positive-grounding-complete",
    ) in edge_pairs
    assert (
        "task-positive-grounding-complete",
        "task-positive-property-filter-complete",
    ) in edge_pairs
    assert (
        "task-positive-property-filter-complete",
        "task-rival-parity-complete",
    ) in edge_pairs
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-task-queue-linked"]["status"] == "complete"
    assert check_rows["check-every-task-has-graph-node"]["status"] == "complete"
    assert check_rows["check-required-dependency-edges-present"]["status"] == "complete"
    assert check_rows["check-graph-remains-unexecuted"]["status"] == "complete"
    assert check_rows["check-dependency-graph-not-promoted-to-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_task_dependency_graph_written" in transcript
    assert "ontological_soundness_bad_god_task_dependency_checks_written" in transcript


def test_godproof_maps_bad_god_evil_hiddenness_pressure(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    matrix = json.loads(
        (session_dir / "ontological-soundness-bad-god-evil-hiddenness-pressure-matrix.json").read_text(
            encoding="utf-8"
        )
    )
    checks = json.loads(
        (session_dir / "ontological-soundness-bad-god-evil-hiddenness-pressure-checks.json").read_text(
            encoding="utf-8"
        )
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert matrix["status"] == "contested"
    assert matrix["matrix"]["input_dependency_graph_id"] == "ontological-soundness-bad-god-task-dependency-graph-v0"
    assert matrix["matrix"]["target_task_id"] == "task-evil-hiddenness-pressure-complete"
    assert matrix["matrix"]["authorization_state"]["pressure_matrix_recorded"] is True
    assert matrix["matrix"]["authorization_state"]["pressure_resolved"] is False
    assert matrix["matrix"]["authorization_state"]["proof_claim_allowed"] is False
    assert len(matrix["matrix"]["pressure_rows"]) == 4
    assert len(matrix["matrix"]["sufficiency_rows"]) == 4
    assert all(row["pressure_status"] == "candidate_response_present" for row in matrix["matrix"]["pressure_rows"])
    assert any(row["sufficiency_status"] == "open" for row in matrix["matrix"]["sufficiency_rows"])
    assert all(row["proof_evidence_materialized"] is False for row in matrix["matrix"]["sufficiency_rows"])
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-bad-god-dependency-graph-linked"]["status"] == "complete"
    assert check_rows["check-evil-hiddenness-task-selected"]["status"] == "complete"
    assert check_rows["check-pressure-constraints-covered"]["status"] == "complete"
    assert check_rows["check-sufficiency-tests-retain-open-pressure"]["status"] == "contested"
    assert check_rows["check-pressure-matrix-not-promoted-to-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evil_hiddenness_pressure_matrix_written" in transcript
    assert "ontological_soundness_bad_god_evil_hiddenness_pressure_checks_written" in transcript


def test_godproof_queues_bad_god_evil_hiddenness_sufficiency_tasks(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    queue = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evil-hiddenness-sufficiency-task-queue.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evil-hiddenness-sufficiency-task-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert queue["status"] == "contested"
    assert queue["queue"]["input_pressure_matrix_id"] == (
        "ontological-soundness-bad-god-evil-hiddenness-pressure-matrix-v0"
    )
    assert queue["queue"]["target_task_id"] == "task-evil-hiddenness-pressure-complete"
    assert queue["queue"]["authorization_state"]["sufficiency_task_queue_recorded"] is True
    assert queue["queue"]["authorization_state"]["sufficiency_tasks_executed"] is False
    assert queue["queue"]["authorization_state"]["pressure_resolved"] is False
    assert queue["queue"]["authorization_state"]["proof_claim_allowed"] is False
    task_items = queue["queue"]["task_items"]
    assert len(task_items) == 3
    assert {row["task_id"] for row in task_items} == {
        "task-evidential-probability-pressure",
        "task-non-resistant-nonbelief-pressure",
        "task-moral-reasoning-preservation",
    }
    assert all(row["task_status"] == "queued_not_executed" for row in task_items)
    assert all(row["proof_evidence_materialized"] is False for row in task_items)
    assert all(row["verifier_commands"] for row in task_items)
    assert all(row["acceptance_criteria"] for row in task_items)
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-pressure-matrix-linked"]["status"] == "complete"
    assert check_rows["check-every-open-sufficiency-test-has-task"]["status"] == "complete"
    assert (
        check_rows["check-sufficiency-tasks-have-verifiers-and-acceptance-criteria"]["status"]
        == "complete"
    )
    assert check_rows["check-sufficiency-tasks-remain-unexecuted"]["status"] == "complete"
    assert check_rows["check-sufficiency-task-queue-not-promoted-to-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_queue_written" in transcript
    assert "ontological_soundness_bad_god_evil_hiddenness_sufficiency_task_checks_written" in transcript


def test_godproof_scaffolds_bad_god_evidential_probability_pressure_task(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    scaffold = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-probability-pressure-task-scaffold.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-probability-pressure-task-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert scaffold["status"] == "contested"
    assert scaffold["scaffold"]["input_task_queue_id"] == (
        "ontological-soundness-bad-god-evil-hiddenness-sufficiency-task-queue-v0"
    )
    assert scaffold["scaffold"]["target_task_id"] == "task-evidential-probability-pressure"
    assert scaffold["scaffold"]["parent_task_id"] == "task-evil-hiddenness-pressure-complete"
    assert scaffold["scaffold"]["target_pressure_test_id"] == "evidential-probability-pressure"
    assert scaffold["scaffold"]["input_probability_audit_id"] == "evidential-evil-probability-audit-v0"
    assert scaffold["scaffold"]["execution_state"]["scaffold_recorded"] is True
    assert scaffold["scaffold"]["execution_state"]["evidence_gathering_executed"] is False
    assert scaffold["scaffold"]["execution_state"]["probability_pressure_resolved"] is False
    assert scaffold["scaffold"]["execution_state"]["proof_claim_allowed"] is False
    assert len(scaffold["scaffold"]["evaluation_lanes"]) == 4
    assert len(scaffold["scaffold"]["evidence_dimension_ids"]) >= 6
    assert set(scaffold["scaffold"]["live_objection_ids"]) == {
        "gratuitous-suffering-objection",
        "inscrutability-cost-objection",
        "moral-reasoning-preservation-objection",
        "hiddenness-coupling-objection",
    }
    assert all(row["lane_status"] == "ready_not_executed" for row in scaffold["scaffold"]["evaluation_lanes"])
    assert all(row["verifier_commands"] for row in scaffold["scaffold"]["evaluation_lanes"])
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-sufficiency-task-linked"]["status"] == "complete"
    assert check_rows["check-probability-audit-linked"]["status"] == "complete"
    assert check_rows["check-probability-checks-linked"]["status"] == "complete"
    assert check_rows["check-evaluation-lanes-cover-probability-requirements"]["status"] == "complete"
    assert check_rows["check-live-objections-retained"]["status"] == "contested"
    assert check_rows["check-scaffold-not-executed-or-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_probability_pressure_task_scaffold_written" in transcript
    assert "ontological_soundness_bad_god_evidential_probability_pressure_task_checks_written" in transcript


def test_godproof_builds_bad_god_evidential_prior_sensitivity_grid(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    grid = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-prior-sensitivity-grid.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-prior-sensitivity-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert grid["status"] == "contested"
    assert grid["grid"]["input_task_scaffold_id"] == (
        "ontological-soundness-bad-god-evidential-probability-pressure-task-scaffold-v0"
    )
    assert grid["grid"]["input_likelihood_ledger_id"] == "evidential-evil-likelihood-ledger-v0"
    assert grid["grid"]["target_task_id"] == "task-evidential-probability-pressure"
    assert grid["grid"]["target_lane_id"] == "lane-priors_declared"
    assert grid["grid"]["target_requirement_id"] == "priors_declared"
    assert len(grid["grid"]["prior_rows"]) == 4
    assert {row["hypothesis_id"] for row in grid["grid"]["prior_rows"]} == {
        "classical_theism",
        "skeptical_theism_compatible_theism",
        "soul_making_theism",
        "non_theistic_indifference",
    }
    assert all(0 <= row["lower"] <= row["upper"] <= 1 for row in grid["grid"]["prior_rows"])
    assert len(grid["grid"]["normalized_prior_profiles"]) == 3
    assert all(
        abs(sum(profile["weights"].values()) - 1.0) < 1e-6
        for profile in grid["grid"]["normalized_prior_profiles"]
    )
    assert grid["grid"]["execution_state"]["prior_grid_recorded"] is True
    assert grid["grid"]["execution_state"]["prior_grid_executed"] is False
    assert grid["grid"]["execution_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-task-scaffold-linked"]["status"] == "complete"
    assert check_rows["check-likelihood-ledger-linked"]["status"] == "complete"
    assert check_rows["check-prior-hypotheses-covered"]["status"] == "complete"
    assert check_rows["check-normalized-prior-profiles"]["status"] == "complete"
    assert check_rows["check-prior-grid-not-executed-or-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_prior_sensitivity_grid_written" in transcript
    assert "ontological_soundness_bad_god_evidential_prior_sensitivity_checks_written" in transcript


def test_godproof_builds_bad_god_evidential_likelihood_sensitivity_grid(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    grid = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-likelihood-sensitivity-grid.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-likelihood-sensitivity-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert grid["status"] == "contested"
    assert grid["grid"]["input_task_scaffold_id"] == (
        "ontological-soundness-bad-god-evidential-probability-pressure-task-scaffold-v0"
    )
    assert grid["grid"]["input_prior_grid_id"] == (
        "ontological-soundness-bad-god-evidential-prior-sensitivity-grid-v0"
    )
    assert grid["grid"]["input_likelihood_ledger_id"] == "evidential-evil-likelihood-ledger-v0"
    assert grid["grid"]["target_task_id"] == "task-evidential-probability-pressure"
    assert grid["grid"]["target_lane_id"] == "lane-likelihoods_quantified"
    assert grid["grid"]["target_requirement_id"] == "likelihoods_quantified"
    assert len(grid["grid"]["likelihood_cells"]) == 24
    assert len(grid["grid"]["evidence_dimension_ids"]) == 6
    assert len(grid["grid"]["hypothesis_ids"]) == 4
    assert all(0 <= row["lower"] <= row["upper"] <= 1 for row in grid["grid"]["likelihood_cells"])
    assert len(grid["grid"]["prior_profile_projection_inputs"]) == 3
    assert all(
        row["likelihood_cell_count"] == 24 and row["projection_status"] == "ready_not_executed"
        for row in grid["grid"]["prior_profile_projection_inputs"]
    )
    assert grid["grid"]["execution_state"]["likelihood_grid_recorded"] is True
    assert grid["grid"]["execution_state"]["likelihood_grid_executed"] is False
    assert grid["grid"]["execution_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-task-scaffold-linked"]["status"] == "complete"
    assert check_rows["check-prior-grid-linked"]["status"] == "complete"
    assert check_rows["check-likelihood-ledger-linked"]["status"] == "complete"
    assert check_rows["check-likelihood-cells-cover-grid"]["status"] == "complete"
    assert check_rows["check-prior-profile-projections-ready"]["status"] == "complete"
    assert check_rows["check-likelihood-grid-not-executed-or-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_likelihood_sensitivity_grid_written" in transcript
    assert "ontological_soundness_bad_god_evidential_likelihood_sensitivity_checks_written" in transcript


def test_godproof_builds_bad_god_evidential_response_cost_grid(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    grid = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-response-cost-grid.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-response-cost-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert grid["status"] == "contested"
    assert grid["grid"]["input_task_scaffold_id"] == (
        "ontological-soundness-bad-god-evidential-probability-pressure-task-scaffold-v0"
    )
    assert grid["grid"]["input_likelihood_grid_id"] == (
        "ontological-soundness-bad-god-evidential-likelihood-sensitivity-grid-v0"
    )
    assert grid["grid"]["input_likelihood_ledger_id"] == "evidential-evil-likelihood-ledger-v0"
    assert grid["grid"]["target_task_id"] == "task-evidential-probability-pressure"
    assert grid["grid"]["target_lane_id"] == "lane-response_costs_declared"
    assert grid["grid"]["target_requirement_id"] == "response_costs_declared"
    assert len(grid["grid"]["response_cost_rows"]) == 4
    assert {row["response_model_id"] for row in grid["grid"]["response_cost_rows"]} == {
        "free_will_defense",
        "soul_making_theodicy",
        "skeptical_theism",
        "greater_good_unknown",
    }
    assert all(0 <= row["penalty_lower"] <= row["penalty_upper"] <= 1 for row in grid["grid"]["response_cost_rows"])
    assert len(grid["grid"]["cost_projection_inputs"]) == 3
    assert all(
        row["response_cost_count"] == 4 and row["projection_status"] == "ready_not_executed"
        for row in grid["grid"]["cost_projection_inputs"]
    )
    assert grid["grid"]["execution_state"]["response_cost_grid_recorded"] is True
    assert grid["grid"]["execution_state"]["response_cost_grid_executed"] is False
    assert grid["grid"]["execution_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-task-scaffold-linked"]["status"] == "complete"
    assert check_rows["check-likelihood-grid-linked"]["status"] == "complete"
    assert check_rows["check-likelihood-ledger-linked"]["status"] == "complete"
    assert check_rows["check-response-costs-covered"]["status"] == "complete"
    assert check_rows["check-cost-projections-ready"]["status"] == "complete"
    assert check_rows["check-response-cost-grid-not-executed-or-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_response_cost_grid_written" in transcript
    assert "ontological_soundness_bad_god_evidential_response_cost_checks_written" in transcript


def test_godproof_builds_bad_god_evidential_rival_comparison_grid(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    grid = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-rival-comparison-grid.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-rival-comparison-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert grid["status"] == "contested"
    assert grid["grid"]["input_task_scaffold_id"] == (
        "ontological-soundness-bad-god-evidential-probability-pressure-task-scaffold-v0"
    )
    assert grid["grid"]["input_response_cost_grid_id"] == (
        "ontological-soundness-bad-god-evidential-response-cost-grid-v0"
    )
    assert grid["grid"]["input_likelihood_grid_id"] == (
        "ontological-soundness-bad-god-evidential-likelihood-sensitivity-grid-v0"
    )
    assert grid["grid"]["input_rival_parity_scope"] == "rival_necessary_concepts_parity_audit_not_uniqueness_proof"
    assert grid["grid"]["target_task_id"] == "task-evidential-probability-pressure"
    assert grid["grid"]["target_lane_id"] == "lane-rival_likelihoods_compared"
    assert grid["grid"]["target_requirement_id"] == "rival_likelihoods_compared"
    assert grid["grid"]["rival_hypothesis_id"] == "non_theistic_indifference"
    assert len(grid["grid"]["rival_likelihood_rows"]) == 6
    assert len(grid["grid"]["required_evidence_dimension_ids"]) == 6
    assert all(row["rival_hypothesis_id"] == "non_theistic_indifference" for row in grid["grid"]["rival_likelihood_rows"])
    assert len(grid["grid"]["necessary_rival_bridge_rows"]) >= 2
    assert grid["grid"]["execution_state"]["rival_comparison_grid_recorded"] is True
    assert grid["grid"]["execution_state"]["rival_comparison_executed"] is False
    assert grid["grid"]["execution_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-task-scaffold-linked"]["status"] == "complete"
    assert check_rows["check-response-cost-grid-linked"]["status"] == "complete"
    assert check_rows["check-likelihood-grid-linked"]["status"] == "complete"
    assert check_rows["check-non-theistic-rival-covers-evidence-dimensions"]["status"] == "complete"
    assert check_rows["check-necessary-rival-parity-linked"]["status"] == "complete"
    assert check_rows["check-rival-comparison-not-executed-or-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_rival_comparison_grid_written" in transcript
    assert "ontological_soundness_bad_god_evidential_rival_comparison_checks_written" in transcript


def test_godproof_builds_bad_god_evidential_probability_execution_packet(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    packet = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-probability-execution-packet.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-probability-execution-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert packet["status"] == "contested"
    assert packet["packet"]["target_task_id"] == "task-evidential-probability-pressure"
    assert packet["packet"]["input_task_scaffold_id"] == (
        "ontological-soundness-bad-god-evidential-probability-pressure-task-scaffold-v0"
    )
    assert packet["packet"]["input_grid_ids"] == [
        "ontological-soundness-bad-god-evidential-prior-sensitivity-grid-v0",
        "ontological-soundness-bad-god-evidential-likelihood-sensitivity-grid-v0",
        "ontological-soundness-bad-god-evidential-response-cost-grid-v0",
        "ontological-soundness-bad-god-evidential-rival-comparison-grid-v0",
    ]
    assert [row["lane_id"] for row in packet["packet"]["execution_steps"]] == [
        "lane-priors_declared",
        "lane-likelihoods_quantified",
        "lane-response_costs_declared",
        "lane-rival_likelihoods_compared",
    ]
    assert all(row["step_status"] == "ready_not_executed" for row in packet["packet"]["execution_steps"])
    assert packet["packet"]["execution_state"]["execution_packet_recorded"] is True
    assert packet["packet"]["execution_state"]["posterior_projection_executed"] is False
    assert packet["packet"]["execution_state"]["probability_pressure_resolved"] is False
    assert packet["packet"]["execution_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-all-lane-grids-linked"]["status"] == "complete"
    assert check_rows["check-all-lane-checks-linked"]["status"] == "complete"
    assert check_rows["check-execution-order-complete"]["status"] == "complete"
    assert check_rows["check-execution-packet-not-run-or-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_probability_execution_packet_written" in transcript
    assert "ontological_soundness_bad_god_evidential_probability_execution_checks_written" in transcript


def test_godproof_runs_bad_god_evidential_posterior_projection_candidates(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    results = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-posterior-projection-results.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-posterior-projection-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert results["status"] == "contested"
    assert results["results"]["input_execution_packet_id"] == (
        "ontological-soundness-bad-god-evidential-probability-execution-packet-v0"
    )
    assert results["results"]["target_task_id"] == "task-evidential-probability-pressure"
    assert results["results"]["projection_mode"] == "midpoint_average_cost_adjusted_candidate"
    assert len(results["results"]["projection_results"]) == 3
    assert all(row["projection_status"] == "executed_candidate" for row in results["results"]["projection_results"])
    assert all(
        abs(sum(row["posterior"].values()) - 1.0) < 1e-6
        for row in results["results"]["projection_results"]
    )
    assert all(row["top_hypothesis_id"] in row["posterior"] for row in results["results"]["projection_results"])
    assert results["results"]["execution_state"]["posterior_projection_executed"] is True
    assert results["results"]["execution_state"]["probability_pressure_resolved"] is False
    assert results["results"]["execution_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-execution-packet-linked"]["status"] == "complete"
    assert check_rows["check-projection-results-present"]["status"] == "complete"
    assert check_rows["check-posteriors-normalized"]["status"] == "complete"
    assert check_rows["check-projection-remains-contested"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_posterior_projection_results_written" in transcript
    assert "ontological_soundness_bad_god_evidential_posterior_projection_checks_written" in transcript


def test_godproof_reviews_bad_god_evidential_projection_outcome(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    review = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-projection-outcome-review.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-projection-outcome-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert review["status"] == "contested"
    assert review["review"]["input_projection_results_id"] == (
        "ontological-soundness-bad-god-evidential-posterior-projection-results-v0"
    )
    assert review["review"]["target_task_id"] == "task-evidential-probability-pressure"
    assert review["review"]["target_pressure_test_id"] == "evidential-probability-pressure"
    assert review["review"]["projection_mode"] == "midpoint_average_cost_adjusted_candidate"
    assert review["review"]["projection_count"] == 3
    assert review["review"]["top_hypothesis_tally"] == {"non_theistic_indifference": 3}
    assert len(review["review"]["outcome_rows"]) == 3
    assert all(row["result_status"] == "candidate_pressure_recorded" for row in review["review"]["outcome_rows"])
    assert all(row["top_hypothesis_id"] == "non_theistic_indifference" for row in review["review"]["outcome_rows"])
    assert review["review"]["pressure_assessment"]["candidate_result"] == (
        "non_theistic_indifference_top_in_all_profiles"
    )
    assert review["review"]["pressure_assessment"]["probability_pressure_resolved"] is False
    assert review["review"]["pressure_assessment"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-posterior-projection-linked"]["status"] == "complete"
    assert check_rows["check-outcome-rows-cover-projections"]["status"] == "complete"
    assert check_rows["check-top-hypothesis-tally-recorded"]["status"] == "complete"
    assert check_rows["check-pressure-remains-unresolved"]["status"] == "contested"
    assert check_rows["check-outcome-review-not-promoted-to-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_projection_outcome_review_written" in transcript
    assert "ontological_soundness_bad_god_evidential_projection_outcome_checks_written" in transcript


def test_godproof_plans_bad_god_evidential_projection_remediation(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    plan = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-projection-remediation-plan.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-projection-remediation-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert plan["status"] == "contested"
    assert plan["plan"]["input_outcome_review_id"] == (
        "ontological-soundness-bad-god-evidential-projection-outcome-review-v0"
    )
    assert plan["plan"]["target_task_id"] == "task-evidential-probability-pressure"
    assert plan["plan"]["target_pressure_test_id"] == "evidential-probability-pressure"
    assert plan["plan"]["source_candidate_result"] == "non_theistic_indifference_top_in_all_profiles"
    expected_categories = {
        "calibration",
        "dependence",
        "response_cost",
        "rival_hypothesis",
    }
    assert {row["remediation_category"] for row in plan["plan"]["remediation_items"]} == expected_categories
    assert all(row["work_status"] == "queued_not_executed" for row in plan["plan"]["remediation_items"])
    assert all(row["proof_evidence_materialized"] is False for row in plan["plan"]["remediation_items"])
    assert plan["plan"]["execution_state"]["remediation_plan_recorded"] is True
    assert plan["plan"]["execution_state"]["remediation_executed"] is False
    assert plan["plan"]["execution_state"]["probability_pressure_resolved"] is False
    assert plan["plan"]["execution_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-outcome-review-linked"]["status"] == "complete"
    assert check_rows["check-remediation-items-cover-open-risks"]["status"] == "complete"
    assert check_rows["check-remediation-items-not-executed"]["status"] == "complete"
    assert check_rows["check-pressure-still-unresolved"]["status"] == "contested"
    assert check_rows["check-remediation-plan-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_projection_remediation_plan_written" in transcript
    assert "ontological_soundness_bad_god_evidential_projection_remediation_checks_written" in transcript


def test_godproof_scopes_bad_god_evidential_calibration_sources(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    registry = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-registry.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert registry["status"] == "contested"
    assert registry["registry"]["input_remediation_plan_id"] == (
        "ontological-soundness-bad-god-evidential-projection-remediation-plan-v0"
    )
    assert registry["registry"]["target_remediation_id"] == "remediate-calibration-intervals"
    assert registry["registry"]["target_remediation_category"] == "calibration"
    expected_families = {
        "analytic_philosophy",
        "philosophy_of_religion",
        "probability_theory",
        "empirical_suffering_data",
        "religious_experience_hiddenness_data",
        "comparative_theology",
    }
    assert {row["source_family_id"] for row in registry["registry"]["source_families"]} == expected_families
    assert all(row["collection_status"] == "scoped_not_ingested" for row in registry["registry"]["source_families"])
    assert all(row["required_for_interval_calibration"] is True for row in registry["registry"]["source_families"])
    assert registry["registry"]["execution_state"]["source_registry_recorded"] is True
    assert registry["registry"]["execution_state"]["sources_ingested"] is False
    assert registry["registry"]["execution_state"]["calibration_intervals_computed"] is False
    assert registry["registry"]["execution_state"]["probability_pressure_resolved"] is False
    assert registry["registry"]["execution_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-remediation-plan-linked"]["status"] == "complete"
    assert check_rows["check-calibration-item-selected"]["status"] == "complete"
    assert check_rows["check-source-families-cover-calibration-domains"]["status"] == "complete"
    assert check_rows["check-sources-not-ingested"]["status"] == "complete"
    assert check_rows["check-calibration-registry-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_registry_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_checks_written" in transcript


def test_godproof_prepares_bad_god_evidential_calibration_source_acquisition(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    manifest = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-acquisition-manifest.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-acquisition-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert manifest["status"] == "contested"
    assert manifest["manifest"]["input_source_registry_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-registry-v0"
    )
    assert manifest["manifest"]["target_remediation_id"] == "remediate-calibration-intervals"
    assert manifest["manifest"]["acquisition_scope"] == "calibration_source_collection"
    expected_families = {
        "analytic_philosophy",
        "philosophy_of_religion",
        "probability_theory",
        "empirical_suffering_data",
        "religious_experience_hiddenness_data",
        "comparative_theology",
    }
    assert {row["source_family_id"] for row in manifest["manifest"]["acquisition_items"]} == expected_families
    assert all(row["acquisition_status"] == "queued_not_fetched" for row in manifest["manifest"]["acquisition_items"])
    assert all(len(row["query_intents"]) >= 2 for row in manifest["manifest"]["acquisition_items"])
    assert all(len(row["acceptance_gates"]) >= 3 for row in manifest["manifest"]["acquisition_items"])
    assert manifest["manifest"]["execution_state"]["acquisition_manifest_recorded"] is True
    assert manifest["manifest"]["execution_state"]["sources_fetched"] is False
    assert manifest["manifest"]["execution_state"]["sources_ingested"] is False
    assert manifest["manifest"]["execution_state"]["source_quality_scored"] is False
    assert manifest["manifest"]["execution_state"]["calibration_intervals_computed"] is False
    assert manifest["manifest"]["execution_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-source-registry-linked"]["status"] == "complete"
    assert check_rows["check-acquisition-items-cover-source-families"]["status"] == "complete"
    assert check_rows["check-acquisition-queries-present"]["status"] == "complete"
    assert check_rows["check-sources-not-fetched"]["status"] == "complete"
    assert check_rows["check-acquisition-manifest-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_acquisition_manifest_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_acquisition_checks_written" in transcript


def test_godproof_batches_bad_god_evidential_calibration_source_acquisition(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    batch_plan = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-batch-plan.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-batch-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert batch_plan["status"] == "contested"
    assert batch_plan["batch_plan"]["input_acquisition_manifest_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-acquisition-manifest-v0"
    )
    assert batch_plan["batch_plan"]["target_remediation_id"] == "remediate-calibration-intervals"
    assert batch_plan["batch_plan"]["batch_scope"] == "calibration_source_acquisition_batches"
    expected_families = {
        "analytic_philosophy",
        "philosophy_of_religion",
        "probability_theory",
        "empirical_suffering_data",
        "religious_experience_hiddenness_data",
        "comparative_theology",
    }
    assert {row["source_family_id"] for row in batch_plan["batch_plan"]["batches"]} == expected_families
    assert len(batch_plan["batch_plan"]["batches"]) == 6
    assert all(row["batch_status"] == "queued_not_started" for row in batch_plan["batch_plan"]["batches"])
    assert all(row["logging_requirements"]["hash_algorithm"] == "sha256" for row in batch_plan["batch_plan"]["batches"])
    assert all(
        row["logging_requirements"]["transcript_event_required"] is True
        for row in batch_plan["batch_plan"]["batches"]
    )
    assert batch_plan["batch_plan"]["execution_state"]["batch_plan_recorded"] is True
    assert batch_plan["batch_plan"]["execution_state"]["batches_executed"] is False
    assert batch_plan["batch_plan"]["execution_state"]["sources_fetched"] is False
    assert batch_plan["batch_plan"]["execution_state"]["acquisition_log_materialized"] is False
    assert batch_plan["batch_plan"]["execution_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-acquisition-manifest-linked"]["status"] == "complete"
    assert check_rows["check-batches-cover-acquisition-items"]["status"] == "complete"
    assert check_rows["check-batches-include-logging-requirements"]["status"] == "complete"
    assert check_rows["check-batches-not-executed"]["status"] == "complete"
    assert check_rows["check-batch-plan-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_batch_plan_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_batch_checks_written" in transcript


def test_godproof_seeds_bad_god_evidential_calibration_source_candidates(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    catalog = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-seed-catalog.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-seed-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert catalog["status"] == "contested"
    assert catalog["catalog"]["input_batch_plan_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-batch-plan-v0"
    )
    assert catalog["catalog"]["candidate_scope"] == "calibration_source_seed_candidates"
    candidates = catalog["catalog"]["candidate_sources"]
    expected_families = {
        "analytic_philosophy",
        "philosophy_of_religion",
        "probability_theory",
        "empirical_suffering_data",
        "religious_experience_hiddenness_data",
        "comparative_theology",
    }
    assert len(candidates) >= 12
    assert {row["source_family_id"] for row in candidates} == expected_families
    assert all(sum(1 for row in candidates if row["source_family_id"] == family_id) >= 2 for family_id in expected_families)
    assert all(row["source_status"] == "seeded_not_fetched" for row in candidates)
    assert all(row["url"].startswith("https://") for row in candidates)
    assert all(row["url_verified_at"] == "2026-05-24" for row in candidates)
    assert any("plato.stanford.edu/entries/ontological-arguments/" in row["url"] for row in candidates)
    assert any("ghdx.healthdata.org/gbd-results-tool" in row["url"] for row in candidates)
    assert any("pewresearch.org/about-the-religious-landscape-study" in row["url"] for row in candidates)
    assert catalog["catalog"]["execution_state"]["seed_catalog_recorded"] is True
    assert catalog["catalog"]["execution_state"]["source_candidates_fetched"] is False
    assert catalog["catalog"]["execution_state"]["source_hashes_materialized"] is False
    assert catalog["catalog"]["execution_state"]["calibration_intervals_computed"] is False
    assert catalog["catalog"]["execution_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-batch-plan-linked"]["status"] == "complete"
    assert check_rows["check-seeds-cover-batch-families"]["status"] == "complete"
    assert check_rows["check-seed-counts-per-family"]["status"] == "complete"
    assert check_rows["check-seeds-not-fetched"]["status"] == "complete"
    assert check_rows["check-seed-catalog-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_seed_catalog_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_seed_checks_written" in transcript


def test_godproof_classifies_bad_god_evidential_calibration_source_eligibility(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    matrix = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-eligibility-matrix.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-eligibility-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert matrix["status"] == "contested"
    assert matrix["matrix"]["input_seed_catalog_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-seed-catalog-v0"
    )
    assert matrix["matrix"]["eligibility_scope"] == "pre_fetch_source_gate_classification"
    rows = matrix["matrix"]["eligibility_rows"]
    assert len(rows) == 12
    assert all(row["eligibility_status"] == "eligible_pending_fetch" for row in rows)
    assert all(row["content_fetched"] is False for row in rows)
    assert all(row["content_quality_scored"] is False for row in rows)
    assert all(row["proof_evidence_materialized"] is False for row in rows)
    assert any(row["source_kind"] == "official_dataset_tool" for row in rows)
    assert any(row["source_kind"] == "peer_reviewed_reference" for row in rows)
    assert any("primary_or_peer_reviewed_or_official_dataset" in row["satisfied_pre_fetch_gates"] for row in rows)
    assert matrix["matrix"]["gate_summary"]["candidate_count"] == 12
    assert matrix["matrix"]["gate_summary"]["eligible_pending_fetch_count"] == 12
    assert matrix["matrix"]["gate_summary"]["content_quality_scored_count"] == 0
    assert matrix["matrix"]["execution_state"]["eligibility_matrix_recorded"] is True
    assert matrix["matrix"]["execution_state"]["source_content_fetched"] is False
    assert matrix["matrix"]["execution_state"]["source_quality_scored"] is False
    assert matrix["matrix"]["execution_state"]["calibration_intervals_computed"] is False
    assert matrix["matrix"]["execution_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-seed-catalog-linked"]["status"] == "complete"
    assert check_rows["check-eligibility-rows-cover-seeds"]["status"] == "complete"
    assert check_rows["check-pre-fetch-gates-classified"]["status"] == "complete"
    assert check_rows["check-content-not-scored"]["status"] == "complete"
    assert check_rows["check-eligibility-matrix-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_eligibility_matrix_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_eligibility_checks_written" in transcript


def test_godproof_writes_bad_god_evidential_calibration_source_retrieval_runbook(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    runbook = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-retrieval-runbook.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-retrieval-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert runbook["status"] == "contested"
    assert runbook["runbook"]["input_eligibility_matrix_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-eligibility-matrix-v0"
    )
    assert runbook["runbook"]["retrieval_scope"] == "auditable_candidate_fetch_hash_log"
    steps = runbook["runbook"]["retrieval_steps"]
    assert len(steps) == 12
    assert all(row["step_status"] == "queued_not_executed" for row in steps)
    assert all(row["source_status"] == "eligible_pending_fetch" for row in steps)
    assert all(row["fetch_command_template"].startswith("rtk curl -L --fail") for row in steps)
    assert all(row["hash_command_template"].startswith("rtk shasum -a 256") for row in steps)
    assert all(row["log_event_name"] == "calibration_source_candidate_retrieved" for row in steps)
    assert all(row["expected_hash_algorithm"] == "sha256" for row in steps)
    assert all(row["proof_evidence_materialized"] is False for row in steps)
    assert runbook["runbook"]["execution_state"]["retrieval_runbook_recorded"] is True
    assert runbook["runbook"]["execution_state"]["retrieval_executed"] is False
    assert runbook["runbook"]["execution_state"]["source_hashes_materialized"] is False
    assert runbook["runbook"]["execution_state"]["retrieval_logs_materialized"] is False
    assert runbook["runbook"]["execution_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-eligibility-matrix-linked"]["status"] == "complete"
    assert check_rows["check-retrieval-steps-cover-eligible-sources"]["status"] == "complete"
    assert check_rows["check-fetch-hash-log-templates-present"]["status"] == "complete"
    assert check_rows["check-retrieval-not-executed"]["status"] == "complete"
    assert check_rows["check-retrieval-runbook-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_retrieval_runbook_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_retrieval_checks_written" in transcript


def test_godproof_defines_bad_god_evidential_calibration_source_retrieval_log_schema(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    schema = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-retrieval-log-schema.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-retrieval-log-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert schema["status"] == "contested"
    assert schema["schema"]["input_retrieval_runbook_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-retrieval-runbook-v0"
    )
    assert schema["schema"]["log_scope"] == "retrieval_execution_log_schema"
    required_fields = schema["schema"]["required_log_fields"]
    for field in [
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
    ]:
        assert field in required_fields
    assert schema["schema"]["hash_validation"]["algorithm"] == "sha256"
    assert schema["schema"]["hash_validation"]["required"] is True
    assert schema["schema"]["transcript_event_name"] == "calibration_source_candidate_retrieved"
    assert len(schema["schema"]["log_templates"]) == 12
    assert all(row["log_status"] == "schema_defined_not_materialized" for row in schema["schema"]["log_templates"])
    assert all(row["transcript_event_name"] == "calibration_source_candidate_retrieved" for row in schema["schema"]["log_templates"])
    assert schema["schema"]["execution_state"]["retrieval_log_schema_recorded"] is True
    assert schema["schema"]["execution_state"]["retrieval_logs_materialized"] is False
    assert schema["schema"]["execution_state"]["hashes_verified"] is False
    assert schema["schema"]["execution_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-retrieval-runbook-linked"]["status"] == "complete"
    assert check_rows["check-log-templates-cover-retrieval-steps"]["status"] == "complete"
    assert check_rows["check-required-log-fields-present"]["status"] == "complete"
    assert check_rows["check-logs-not-materialized"]["status"] == "complete"
    assert check_rows["check-retrieval-log-schema-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_schema_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_retrieval_log_checks_written" in transcript


def test_godproof_records_bad_god_evidential_calibration_source_retrieval_dry_run_ledger(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    ledger = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-retrieval-dry-run-ledger.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-retrieval-dry-run-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert ledger["status"] == "contested"
    assert ledger["ledger"]["input_retrieval_runbook_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-retrieval-runbook-v0"
    )
    assert ledger["ledger"]["input_retrieval_log_schema_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-retrieval-log-schema-v0"
    )
    assert ledger["ledger"]["ledger_scope"] == "retrieval_pre_execution_dry_run"
    dry_run_rows = ledger["ledger"]["dry_run_rows"]
    assert len(dry_run_rows) == 12
    assert all(row["dry_run_status"] == "validated_not_executed" for row in dry_run_rows)
    assert all(row["retrieval_step_status"] == "queued_not_executed" for row in dry_run_rows)
    assert all(row["log_status"] == "schema_defined_not_materialized" for row in dry_run_rows)
    assert all(row["fetch_command_template"].startswith("rtk curl -L --fail") for row in dry_run_rows)
    assert all(row["hash_command_template"].startswith("rtk shasum -a 256") for row in dry_run_rows)
    assert all(row["proof_evidence_materialized"] is False for row in dry_run_rows)
    assert ledger["ledger"]["execution_state"]["dry_run_ledger_recorded"] is True
    assert ledger["ledger"]["execution_state"]["retrieval_executed"] is False
    assert ledger["ledger"]["execution_state"]["retrieval_logs_materialized"] is False
    assert ledger["ledger"]["execution_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-retrieval-runbook-linked"]["status"] == "complete"
    assert check_rows["check-retrieval-log-schema-linked"]["status"] == "complete"
    assert check_rows["check-dry-run-rows-cover-retrieval-steps"]["status"] == "complete"
    assert check_rows["check-dry-run-not-executed"]["status"] == "complete"
    assert check_rows["check-dry-run-ledger-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_ledger_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_retrieval_dry_run_checks_written" in transcript


def test_godproof_defines_bad_god_evidential_calibration_source_quality_rubric(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    rubric = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-quality-rubric.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-quality-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert rubric["status"] == "contested"
    assert rubric["rubric"]["input_dry_run_ledger_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-retrieval-dry-run-ledger-v0"
    )
    assert rubric["rubric"]["rubric_scope"] == "post_fetch_source_quality_scoring"
    dimensions = rubric["rubric"]["scoring_dimensions"]
    expected_dimensions = {
        "authority",
        "calibration_relevance",
        "counterevidence_signal",
        "uncertainty_signal",
        "extractability",
        "bias_risk",
    }
    assert {row["dimension_id"] for row in dimensions} == expected_dimensions
    assert round(sum(row["weight"] for row in dimensions), 6) == 1.0
    assert rubric["rubric"]["score_range"] == {"min": 0.0, "max": 1.0}
    assert len(rubric["rubric"]["source_score_templates"]) == 12
    assert all(row["score_status"] == "not_scored" for row in rubric["rubric"]["source_score_templates"])
    assert all(row["content_required_before_scoring"] is True for row in rubric["rubric"]["source_score_templates"])
    assert rubric["rubric"]["execution_state"]["quality_rubric_recorded"] is True
    assert rubric["rubric"]["execution_state"]["source_content_fetched"] is False
    assert rubric["rubric"]["execution_state"]["source_quality_scored"] is False
    assert rubric["rubric"]["execution_state"]["calibration_intervals_computed"] is False
    assert rubric["rubric"]["execution_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-dry-run-ledger-linked"]["status"] == "complete"
    assert check_rows["check-scoring-dimensions-complete"]["status"] == "complete"
    assert check_rows["check-scoring-weights-normalized"]["status"] == "complete"
    assert check_rows["check-score-templates-not-scored"]["status"] == "complete"
    assert check_rows["check-quality-rubric-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_quality_rubric_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_quality_checks_written" in transcript


def test_godproof_defines_bad_god_evidential_calibration_source_quality_score_ledger_schema(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    schema = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-quality-score-ledger-schema.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-quality-score-ledger-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert schema["status"] == "contested"
    assert schema["schema"]["input_quality_rubric_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-quality-rubric-v0"
    )
    assert schema["schema"]["ledger_scope"] == "post_fetch_quality_score_ledger_schema"
    assert schema["schema"]["score_thresholds"]["minimum_usable_quality_score"] == 0.6
    assert schema["schema"]["score_thresholds"]["minimum_counterevidence_signal"] == 0.25
    assert schema["schema"]["score_thresholds"]["maximum_bias_risk"] == 0.75
    required_fields = schema["schema"]["required_score_fields"]
    for field in [
        "source_id",
        "source_family_id",
        "dimension_scores",
        "weighted_quality_score",
        "usable_for_calibration",
        "score_rationale",
        "scored_at",
    ]:
        assert field in required_fields
    assert len(schema["schema"]["score_rows"]) == 12
    assert all(row["score_status"] == "schema_defined_not_scored" for row in schema["schema"]["score_rows"])
    assert all(row["weighted_quality_score"] is None for row in schema["schema"]["score_rows"])
    assert all(row["usable_for_calibration"] is False for row in schema["schema"]["score_rows"])
    assert schema["schema"]["execution_state"]["quality_score_ledger_schema_recorded"] is True
    assert schema["schema"]["execution_state"]["source_quality_scored"] is False
    assert schema["schema"]["execution_state"]["calibration_usable_sources_selected"] is False
    assert schema["schema"]["execution_state"]["calibration_intervals_computed"] is False
    assert schema["schema"]["execution_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-quality-rubric-linked"]["status"] == "complete"
    assert check_rows["check-score-rows-cover-rubric-templates"]["status"] == "complete"
    assert check_rows["check-required-score-fields-present"]["status"] == "complete"
    assert check_rows["check-score-ledger-not-scored"]["status"] == "complete"
    assert check_rows["check-quality-score-ledger-schema-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_schema_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_quality_score_ledger_checks_written" in transcript


def test_godproof_writes_bad_god_evidential_calibration_source_quality_score_dry_run_ledger(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    ledger = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-quality-score-dry-run-ledger.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-quality-score-dry-run-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert ledger["status"] == "contested"
    assert ledger["ledger"]["input_quality_score_schema_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-quality-score-ledger-schema-v0"
    )
    assert ledger["ledger"]["ledger_scope"] == "quality_score_execution_dry_run"
    assert len(ledger["ledger"]["dry_run_rows"]) == 12
    assert all(row["scoring_status"] == "dry_run_not_scored" for row in ledger["ledger"]["dry_run_rows"])
    assert all(row["score_input_ready"] is False for row in ledger["ledger"]["dry_run_rows"])
    assert all(row["weighted_quality_score"] is None for row in ledger["ledger"]["dry_run_rows"])
    assert all(row["usable_for_calibration"] is False for row in ledger["ledger"]["dry_run_rows"])
    assert ledger["ledger"]["execution_state"]["quality_score_dry_run_recorded"] is True
    assert ledger["ledger"]["execution_state"]["source_content_fetched"] is False
    assert ledger["ledger"]["execution_state"]["source_quality_scored"] is False
    assert ledger["ledger"]["execution_state"]["calibration_intervals_computed"] is False
    assert ledger["ledger"]["execution_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-quality-score-schema-linked"]["status"] == "complete"
    assert check_rows["check-dry-run-rows-cover-score-schema"]["status"] == "complete"
    assert check_rows["check-score-inputs-not-ready"]["status"] == "complete"
    assert check_rows["check-quality-score-dry-run-not-scored"]["status"] == "complete"
    assert check_rows["check-quality-score-dry-run-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_ledger_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_quality_score_dry_run_checks_written" in transcript


def test_godproof_blocks_bad_god_evidential_calibration_source_quality_scoring_until_sources_exist(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    gate = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-quality-score-readiness-gate.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-quality-score-readiness-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert gate["status"] == "blocked"
    assert gate["gate"]["input_quality_score_dry_run_ledger_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-quality-score-dry-run-ledger-v0"
    )
    assert gate["gate"]["gate_scope"] == "quality_score_execution_readiness"
    assert gate["gate"]["ready_for_quality_scoring"] is False
    assert gate["gate"]["blocking_reason"] == "source_content_not_fetched"
    assert gate["gate"]["required_materialized_inputs"] == [
        "retrieval_log_id",
        "content_sha256",
        "content_path",
        "fetched_at",
    ]
    assert len(gate["gate"]["readiness_rows"]) == 12
    assert all(row["ready_for_scoring"] is False for row in gate["gate"]["readiness_rows"])
    assert all(row["missing_materialized_inputs"] for row in gate["gate"]["readiness_rows"])
    assert gate["gate"]["execution_state"]["quality_score_readiness_gate_recorded"] is True
    assert gate["gate"]["execution_state"]["source_content_fetched"] is False
    assert gate["gate"]["execution_state"]["source_quality_scored"] is False
    assert gate["gate"]["execution_state"]["calibration_intervals_computed"] is False
    assert gate["gate"]["execution_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "blocked"
    assert check_rows["check-quality-score-dry-run-linked"]["status"] == "complete"
    assert check_rows["check-readiness-rows-cover-dry-run"]["status"] == "complete"
    assert check_rows["check-materialized-inputs-missing"]["status"] == "blocked"
    assert check_rows["check-quality-scoring-blocked"]["status"] == "blocked"
    assert check_rows["check-readiness-gate-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_gate_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_quality_score_readiness_checks_written" in transcript


def test_godproof_prepares_bad_god_evidential_calibration_source_content_materialization_packet(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    packet = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-packet.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert packet["status"] == "contested"
    assert packet["packet"]["input_retrieval_dry_run_ledger_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-retrieval-dry-run-ledger-v0"
    )
    assert packet["packet"]["input_quality_score_readiness_gate_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-quality-score-readiness-gate-v0"
    )
    assert packet["packet"]["packet_scope"] == "retrieval_content_materialization_pre_execution_packet"
    assert packet["packet"]["required_materialized_outputs"] == [
        "retrieval_log_id",
        "content_sha256",
        "content_path",
        "fetched_at",
    ]
    rows = packet["packet"]["materialization_rows"]
    assert len(rows) == 12
    assert all(row["materialization_status"] == "queued_not_materialized" for row in rows)
    assert all(row["retrieval_log_id"] is None for row in rows)
    assert all(row["content_sha256"] is None for row in rows)
    assert all(row["content_path"] is None for row in rows)
    assert all(row["fetched_at"] is None for row in rows)
    assert packet["packet"]["execution_state"]["content_materialization_packet_recorded"] is True
    assert packet["packet"]["execution_state"]["retrieval_executed"] is False
    assert packet["packet"]["execution_state"]["source_content_fetched"] is False
    assert packet["packet"]["execution_state"]["source_quality_scored"] is False
    assert packet["packet"]["execution_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-retrieval-dry-run-linked"]["status"] == "complete"
    assert check_rows["check-readiness-gate-linked"]["status"] == "complete"
    assert check_rows["check-materialization-rows-cover-readiness-gate"]["status"] == "complete"
    assert check_rows["check-materialization-packet-not-executed"]["status"] == "complete"
    assert check_rows["check-materialization-packet-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_packet_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_checks_written" in transcript


def test_godproof_batches_bad_god_evidential_calibration_source_content_materialization(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    plan = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-batch-plan.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-batch-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert plan["status"] == "contested"
    assert plan["batch_plan"]["input_content_materialization_packet_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-packet-v0"
    )
    assert plan["batch_plan"]["batch_scope"] == "retrieval_content_materialization_batches"
    assert plan["batch_plan"]["max_batch_size"] == 3
    batches = plan["batch_plan"]["batches"]
    assert len(batches) == 4
    assert all(1 <= len(batch["source_ids"]) <= 3 for batch in batches)
    assert sum(len(batch["source_ids"]) for batch in batches) == 12
    assert all(batch["batch_status"] == "batch_queued_not_executed" for batch in batches)
    assert all(batch["proof_evidence_materialized"] is False for batch in batches)
    assert plan["batch_plan"]["execution_state"]["content_materialization_batch_plan_recorded"] is True
    assert plan["batch_plan"]["execution_state"]["retrieval_executed"] is False
    assert plan["batch_plan"]["execution_state"]["source_content_fetched"] is False
    assert plan["batch_plan"]["execution_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-content-materialization-packet-linked"]["status"] == "complete"
    assert check_rows["check-batches-cover-materialization-rows"]["status"] == "complete"
    assert check_rows["check-batch-size-limit"]["status"] == "complete"
    assert check_rows["check-materialization-batches-not-executed"]["status"] == "complete"
    assert check_rows["check-materialization-batch-plan-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_plan_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_batch_checks_written" in transcript


def test_godproof_requires_authorization_before_bad_god_evidential_calibration_source_content_materialization(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    packet = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-packet.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert packet["status"] == "blocked"
    assert packet["authorization"]["input_content_materialization_batch_plan_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-batch-plan-v0"
    )
    assert packet["authorization"]["authorization_scope"] == "content_materialization_network_authorization"
    assert packet["authorization"]["authorization_required"] is True
    assert packet["authorization"]["authorization_granted"] is False
    assert packet["authorization"]["blocking_reason"] == "network_access_requires_explicit_user_approval"
    rows = packet["authorization"]["authorization_rows"]
    assert len(rows) == 4
    assert all(row["authorization_status"] == "authorization_pending" for row in rows)
    assert all(row["network_access_allowed"] is False for row in rows)
    assert all(row["batch_status"] == "batch_queued_not_executed" for row in rows)
    assert packet["authorization"]["execution_state"]["content_materialization_authorization_packet_recorded"] is True
    assert packet["authorization"]["execution_state"]["network_access_authorized"] is False
    assert packet["authorization"]["execution_state"]["retrieval_executed"] is False
    assert packet["authorization"]["execution_state"]["source_content_fetched"] is False
    assert packet["authorization"]["execution_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "blocked"
    assert check_rows["check-content-materialization-batch-plan-linked"]["status"] == "complete"
    assert check_rows["check-authorization-rows-cover-batches"]["status"] == "complete"
    assert check_rows["check-network-authorization-pending"]["status"] == "blocked"
    assert check_rows["check-content-materialization-not-authorized"]["status"] == "blocked"
    assert check_rows["check-content-materialization-authorization-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_packet_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_checks_written" in transcript


def test_godproof_queues_bad_god_evidential_calibration_source_content_materialization_authorization_review(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    queue = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-queue.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert queue["status"] == "blocked"
    assert queue["queue"]["input_authorization_packet_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-packet-v0"
    )
    assert queue["queue"]["review_scope"] == "content_materialization_authorization_review"
    assert queue["queue"]["review_mode"] == "queued_authorization_review_not_performed_not_approved"
    assert queue["queue"]["authorization_state"]["review_queue_recorded"] is True
    assert queue["queue"]["authorization_state"]["authorization_reviews_completed"] is False
    assert queue["queue"]["authorization_state"]["authorization_granted"] is False
    assert queue["queue"]["authorization_state"]["network_access_authorized"] is False
    review_items = queue["queue"]["review_items"]
    assert len(review_items) == 4
    assert all(item["review_status"] == "pending_review" for item in review_items)
    assert all(item["proposed_decision"] == "defer_authorization" for item in review_items)
    assert all(item["network_access_allowed"] is False for item in review_items)
    assert all(item["materialization_status"] == "authorization_review_queue_not_evidence" for item in review_items)
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "blocked"
    assert check_rows["check-authorization-packet-linked"]["status"] == "complete"
    assert check_rows["check-review-items-cover-authorization-rows"]["status"] == "complete"
    assert check_rows["check-authorization-review-items-remain-unreviewed"]["status"] == "complete"
    assert check_rows["check-authorization-review-not-granted"]["status"] == "blocked"
    assert check_rows["check-authorization-review-queue-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_queue_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_checks_written" in transcript


def test_godproof_defines_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    rubric = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-rubric.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-rubric-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert rubric["status"] == "contested"
    assert rubric["rubric"]["input_authorization_review_queue_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-queue-v0"
    )
    assert rubric["rubric"]["rubric_scope"] == "content_materialization_authorization_review_scoring"
    criteria_ids = {row["criterion_id"] for row in rubric["rubric"]["review_criteria"]}
    assert criteria_ids == {
        "terms_or_rate_limit_checked",
        "private_or_sensitive_content_risk_checked",
        "retrieval_scope_confirmed",
        "logging_and_hashing_plan_verified",
        "operator_approval_reference_present",
    }
    assert all(row["required_for_authorization"] is True for row in rubric["rubric"]["review_criteria"])
    templates = rubric["rubric"]["review_templates"]
    assert len(templates) == 4
    assert all(row["rubric_status"] == "rubric_defined_not_applied" for row in templates)
    assert all(row["authorization_decision"] is None for row in templates)
    assert all(row["network_access_allowed"] is False for row in templates)
    assert rubric["rubric"]["execution_state"]["authorization_review_rubric_recorded"] is True
    assert rubric["rubric"]["execution_state"]["authorization_reviews_completed"] is False
    assert rubric["rubric"]["execution_state"]["authorization_granted"] is False
    assert rubric["rubric"]["execution_state"]["network_access_authorized"] is False
    assert rubric["rubric"]["execution_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-authorization-review-queue-linked"]["status"] == "complete"
    assert check_rows["check-review-criteria-complete"]["status"] == "complete"
    assert check_rows["check-review-templates-cover-queue"]["status"] == "complete"
    assert check_rows["check-authorization-rubric-not-applied"]["status"] == "complete"
    assert check_rows["check-authorization-review-rubric-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_rubric_checks_written" in transcript


def test_godproof_defers_bad_god_evidential_calibration_source_content_materialization_authorization_review_decisions(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    decisions = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-decisions.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-decision-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert decisions["status"] == "blocked"
    assert decisions["decisions"]["input_authorization_review_rubric_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-rubric-v0"
    )
    assert decisions["decisions"]["decision_scope"] == "content_materialization_authorization_review_decisions"
    decision_rows = decisions["decisions"]["decision_rows"]
    assert len(decision_rows) == 4
    assert all(row["decision_status"] == "review_deferred" for row in decision_rows)
    assert all(row["authorization_decision"].startswith("not_authorized_until_") for row in decision_rows)
    assert all(row["network_access_allowed"] is False for row in decision_rows)
    assert all(row["retrieval_may_execute"] is False for row in decision_rows)
    assert all(row["rubric_applied"] is True for row in decision_rows)
    assert decisions["decisions"]["authorization_state"]["authorization_review_decisions_recorded"] is True
    assert decisions["decisions"]["authorization_state"]["authorization_granted"] is False
    assert decisions["decisions"]["authorization_state"]["network_access_authorized"] is False
    assert decisions["decisions"]["authorization_state"]["retrieval_executed"] is False
    assert decisions["decisions"]["authorization_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "blocked"
    assert check_rows["check-authorization-review-rubric-linked"]["status"] == "complete"
    assert check_rows["check-decision-rows-cover-rubric-templates"]["status"] == "complete"
    assert check_rows["check-authorization-decisions-defer-network"]["status"] == "blocked"
    assert check_rows["check-network-access-remains-denied"]["status"] == "blocked"
    assert check_rows["check-authorization-review-decisions-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decisions_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_decision_checks_written" in transcript


def test_godproof_prepares_bad_god_evidential_calibration_source_content_materialization_authorization_resolution_packet(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    packet = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-resolution-packet.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-resolution-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert packet["status"] == "blocked"
    assert packet["resolution"]["input_authorization_review_decisions_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-decisions-v0"
    )
    assert packet["resolution"]["resolution_scope"] == "content_materialization_authorization_prerequisite_resolution"
    assert packet["resolution"]["required_resolution_actions"] == [
        "operator_approval_reference_present",
        "terms_or_rate_limit_checked",
        "private_or_sensitive_content_risk_checked",
        "retrieval_scope_confirmed",
        "logging_and_hashing_plan_verified",
    ]
    items = packet["resolution"]["resolution_items"]
    assert len(items) == 4
    assert all(item["resolution_status"] == "open" for item in items)
    assert all(item["authorization_decision"].startswith("not_authorized_until_") for item in items)
    assert all(item["network_access_allowed"] is False for item in items)
    assert all(item["retrieval_may_execute"] is False for item in items)
    assert packet["resolution"]["authorization_state"]["authorization_resolution_packet_recorded"] is True
    assert packet["resolution"]["authorization_state"]["authorization_prerequisites_resolved"] is False
    assert packet["resolution"]["authorization_state"]["authorization_granted"] is False
    assert packet["resolution"]["authorization_state"]["network_access_authorized"] is False
    assert packet["resolution"]["authorization_state"]["retrieval_executed"] is False
    assert packet["resolution"]["authorization_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "blocked"
    assert check_rows["check-authorization-review-decisions-linked"]["status"] == "complete"
    assert check_rows["check-resolution-items-cover-decisions"]["status"] == "complete"
    assert check_rows["check-required-resolution-actions-present"]["status"] == "complete"
    assert check_rows["check-authorization-resolution-open"]["status"] == "blocked"
    assert check_rows["check-authorization-resolution-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_packet_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_review_resolution_checks_written" in transcript


def test_godproof_requests_bad_god_evidential_calibration_source_content_materialization_operator_approval(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    request = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-operator-approval-request.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-operator-approval-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert request["status"] == "blocked"
    assert request["approval_request"]["input_authorization_resolution_packet_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-resolution-packet-v0"
    )
    assert request["approval_request"]["request_scope"] == "content_materialization_operator_approval_reference"
    assert request["approval_request"]["operator_approval_reference"] is None
    assert request["approval_request"]["approval_status"] == "requested_not_granted"
    approval_items = request["approval_request"]["approval_items"]
    assert len(approval_items) == 4
    assert all(item["approval_status"] == "requested_not_granted" for item in approval_items)
    assert all(item["required_action"] == "record_operator_approval_reference" for item in approval_items)
    assert all(item["authorization_ready"] is False for item in approval_items)
    assert all(item["network_access_allowed"] is False for item in approval_items)
    assert all(item["retrieval_may_execute"] is False for item in approval_items)
    assert request["approval_request"]["authorization_state"]["operator_approval_requested"] is True
    assert request["approval_request"]["authorization_state"]["operator_approval_reference_recorded"] is False
    assert request["approval_request"]["authorization_state"]["authorization_granted"] is False
    assert request["approval_request"]["authorization_state"]["network_access_authorized"] is False
    assert request["approval_request"]["authorization_state"]["retrieval_executed"] is False
    assert request["approval_request"]["authorization_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "blocked"
    assert check_rows["check-authorization-resolution-packet-linked"]["status"] == "complete"
    assert check_rows["check-operator-approval-items-cover-resolution-items"]["status"] == "complete"
    assert check_rows["check-operator-approval-reference-missing"]["status"] == "blocked"
    assert check_rows["check-operator-approval-denies-network"]["status"] == "blocked"
    assert check_rows["check-operator-approval-request-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_operator_approval_request_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_operator_approval_checks_written" in transcript


def test_godproof_records_bad_god_evidential_calibration_source_content_materialization_terms_rate_limit_review(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    review = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-terms-rate-limit-review.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-terms-rate-limit-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert review["status"] == "blocked"
    assert review["terms_rate_limit_review"]["input_authorization_resolution_packet_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-resolution-packet-v0"
    )
    assert review["terms_rate_limit_review"]["review_scope"] == "content_materialization_terms_rate_limit_review"
    assert review["terms_rate_limit_review"]["terms_or_rate_limit_checked"] is False
    review_items = review["terms_rate_limit_review"]["review_items"]
    assert len(review_items) == 4
    assert all(item["review_status"] == "pending_not_checked" for item in review_items)
    assert all(item["required_action"] == "verify_terms_or_rate_limit" for item in review_items)
    assert all(item["terms_or_rate_limit_checked"] is False for item in review_items)
    assert all(item["authorization_ready"] is False for item in review_items)
    assert all(item["network_access_allowed"] is False for item in review_items)
    assert all(item["retrieval_may_execute"] is False for item in review_items)
    assert review["terms_rate_limit_review"]["authorization_state"]["terms_rate_limit_review_recorded"] is True
    assert review["terms_rate_limit_review"]["authorization_state"]["terms_or_rate_limit_checked"] is False
    assert review["terms_rate_limit_review"]["authorization_state"]["authorization_granted"] is False
    assert review["terms_rate_limit_review"]["authorization_state"]["network_access_authorized"] is False
    assert review["terms_rate_limit_review"]["authorization_state"]["retrieval_executed"] is False
    assert review["terms_rate_limit_review"]["authorization_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "blocked"
    assert check_rows["check-authorization-resolution-packet-linked"]["status"] == "complete"
    assert check_rows["check-terms-rate-limit-items-cover-resolution-items"]["status"] == "complete"
    assert check_rows["check-terms-rate-limit-review-pending"]["status"] == "blocked"
    assert check_rows["check-terms-rate-limit-denies-network"]["status"] == "blocked"
    assert check_rows["check-terms-rate-limit-review-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_terms_rate_limit_review_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_terms_rate_limit_checks_written" in transcript


def test_godproof_records_bad_god_evidential_calibration_source_content_materialization_private_sensitive_risk_review(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    review = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-private-sensitive-risk-review.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-private-sensitive-risk-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert review["status"] == "blocked"
    assert review["private_sensitive_risk_review"]["input_authorization_resolution_packet_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-resolution-packet-v0"
    )
    assert review["private_sensitive_risk_review"]["review_scope"] == (
        "content_materialization_private_sensitive_risk_review"
    )
    assert review["private_sensitive_risk_review"]["private_or_sensitive_content_risk_checked"] is False
    review_items = review["private_sensitive_risk_review"]["review_items"]
    assert len(review_items) == 4
    assert all(item["review_status"] == "pending_not_checked" for item in review_items)
    assert all(item["required_action"] == "check_private_or_sensitive_content_risk" for item in review_items)
    assert all(item["private_or_sensitive_content_risk_checked"] is False for item in review_items)
    assert all(item["authorization_ready"] is False for item in review_items)
    assert all(item["network_access_allowed"] is False for item in review_items)
    assert all(item["retrieval_may_execute"] is False for item in review_items)
    assert review["private_sensitive_risk_review"]["authorization_state"]["private_sensitive_risk_review_recorded"] is True
    assert review["private_sensitive_risk_review"]["authorization_state"]["private_or_sensitive_content_risk_checked"] is False
    assert review["private_sensitive_risk_review"]["authorization_state"]["authorization_granted"] is False
    assert review["private_sensitive_risk_review"]["authorization_state"]["network_access_authorized"] is False
    assert review["private_sensitive_risk_review"]["authorization_state"]["retrieval_executed"] is False
    assert review["private_sensitive_risk_review"]["authorization_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "blocked"
    assert check_rows["check-authorization-resolution-packet-linked"]["status"] == "complete"
    assert check_rows["check-private-sensitive-risk-items-cover-resolution-items"]["status"] == "complete"
    assert check_rows["check-private-sensitive-risk-review-pending"]["status"] == "blocked"
    assert check_rows["check-private-sensitive-risk-denies-network"]["status"] == "blocked"
    assert check_rows["check-private-sensitive-risk-review-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_private_sensitive_risk_review_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_private_sensitive_risk_checks_written" in transcript


def test_godproof_records_bad_god_evidential_calibration_source_content_materialization_retrieval_scope_review(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    review = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-retrieval-scope-review.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-retrieval-scope-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert review["status"] == "blocked"
    assert review["retrieval_scope_review"]["input_authorization_resolution_packet_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-resolution-packet-v0"
    )
    assert review["retrieval_scope_review"]["review_scope"] == "content_materialization_retrieval_scope_review"
    assert review["retrieval_scope_review"]["retrieval_scope_confirmed"] is False
    review_items = review["retrieval_scope_review"]["review_items"]
    assert len(review_items) == 4
    assert all(item["review_status"] == "pending_not_confirmed" for item in review_items)
    assert all(item["required_action"] == "confirm_retrieval_scope" for item in review_items)
    assert all(item["retrieval_scope_confirmed"] is False for item in review_items)
    assert all(item["authorization_ready"] is False for item in review_items)
    assert all(item["network_access_allowed"] is False for item in review_items)
    assert all(item["retrieval_may_execute"] is False for item in review_items)
    assert review["retrieval_scope_review"]["authorization_state"]["retrieval_scope_review_recorded"] is True
    assert review["retrieval_scope_review"]["authorization_state"]["retrieval_scope_confirmed"] is False
    assert review["retrieval_scope_review"]["authorization_state"]["authorization_granted"] is False
    assert review["retrieval_scope_review"]["authorization_state"]["network_access_authorized"] is False
    assert review["retrieval_scope_review"]["authorization_state"]["retrieval_executed"] is False
    assert review["retrieval_scope_review"]["authorization_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "blocked"
    assert check_rows["check-authorization-resolution-packet-linked"]["status"] == "complete"
    assert check_rows["check-retrieval-scope-items-cover-resolution-items"]["status"] == "complete"
    assert check_rows["check-retrieval-scope-review-pending"]["status"] == "blocked"
    assert check_rows["check-retrieval-scope-denies-network"]["status"] == "blocked"
    assert check_rows["check-retrieval-scope-review-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_retrieval_scope_review_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_retrieval_scope_checks_written" in transcript


def test_godproof_records_bad_god_evidential_calibration_source_content_materialization_logging_hash_plan_review(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    review = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-logging-hash-plan-review.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-logging-hash-plan-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert review["status"] == "blocked"
    assert review["logging_hash_plan_review"]["input_authorization_resolution_packet_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-resolution-packet-v0"
    )
    assert review["logging_hash_plan_review"]["review_scope"] == (
        "content_materialization_logging_and_hashing_plan_review"
    )
    assert review["logging_hash_plan_review"]["logging_and_hashing_plan_verified"] is False
    review_items = review["logging_hash_plan_review"]["review_items"]
    assert len(review_items) == 4
    assert all(item["review_status"] == "pending_not_verified" for item in review_items)
    assert all(item["required_action"] == "verify_logging_and_hashing_targets" for item in review_items)
    assert all(item["logging_and_hashing_plan_verified"] is False for item in review_items)
    assert all(item["authorization_ready"] is False for item in review_items)
    assert all(item["network_access_allowed"] is False for item in review_items)
    assert all(item["retrieval_may_execute"] is False for item in review_items)
    assert review["logging_hash_plan_review"]["authorization_state"]["logging_hash_plan_review_recorded"] is True
    assert review["logging_hash_plan_review"]["authorization_state"]["logging_and_hashing_plan_verified"] is False
    assert review["logging_hash_plan_review"]["authorization_state"]["authorization_granted"] is False
    assert review["logging_hash_plan_review"]["authorization_state"]["network_access_authorized"] is False
    assert review["logging_hash_plan_review"]["authorization_state"]["retrieval_executed"] is False
    assert review["logging_hash_plan_review"]["authorization_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "blocked"
    assert check_rows["check-authorization-resolution-packet-linked"]["status"] == "complete"
    assert check_rows["check-logging-hash-plan-items-cover-resolution-items"]["status"] == "complete"
    assert check_rows["check-logging-hash-plan-review-pending"]["status"] == "blocked"
    assert check_rows["check-logging-hash-plan-denies-network"]["status"] == "blocked"
    assert check_rows["check-logging-hash-plan-review-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_logging_hash_plan_review_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_logging_hash_plan_checks_written" in transcript


def test_godproof_records_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_matrix(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    matrix = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-prerequisite-closure-matrix.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-prerequisite-closure-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    closure = matrix["prerequisite_closure_matrix"]
    assert matrix["status"] == "blocked"
    assert closure["input_authorization_resolution_packet_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-review-resolution-packet-v0"
    )
    assert closure["matrix_scope"] == "content_materialization_authorization_prerequisite_closure"
    assert closure["required_prerequisites"] == [
        "operator_approval_reference_recorded",
        "terms_or_rate_limit_checked",
        "private_or_sensitive_content_risk_checked",
        "retrieval_scope_confirmed",
        "logging_and_hashing_plan_verified",
    ]
    rows = closure["closure_rows"]
    assert len(rows) == 5
    assert all(row["closure_status"] == "open" for row in rows)
    assert all(row["satisfied"] is False for row in rows)
    assert all(row["network_access_allowed"] is False for row in rows)
    assert all(row["retrieval_may_execute"] is False for row in rows)
    assert all(row["proof_evidence_materialized"] is False for row in rows)
    assert closure["authorization_state"]["authorization_prerequisite_closure_matrix_recorded"] is True
    assert closure["authorization_state"]["all_authorization_prerequisites_closed"] is False
    assert closure["authorization_state"]["authorization_granted"] is False
    assert closure["authorization_state"]["network_access_authorized"] is False
    assert closure["authorization_state"]["retrieval_executed"] is False
    assert closure["authorization_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "blocked"
    assert check_rows["check-authorization-resolution-packet-linked"]["status"] == "complete"
    assert check_rows["check-prerequisite-closure-rows-cover-required-prerequisites"]["status"] == "complete"
    assert check_rows["check-authorization-prerequisites-remain-open"]["status"] == "blocked"
    assert check_rows["check-prerequisite-closure-denies-network"]["status"] == "blocked"
    assert check_rows["check-prerequisite-closure-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_matrix_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_prerequisite_closure_checks_written" in transcript


def test_godproof_blocks_bad_god_evidential_calibration_source_content_materialization_execution_gate(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    gate = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-materialization-execution-gate.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-materialization-execution-gate-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    execution_gate = gate["materialization_execution_gate"]
    assert gate["status"] == "blocked"
    assert execution_gate["input_prerequisite_closure_matrix_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-prerequisite-closure-matrix-v0"
    )
    assert execution_gate["execution_scope"] == "content_materialization_execution_authorization_gate"
    assert execution_gate["gate_decision"] == "deny_execution_until_authorization_prerequisites_closed"
    gate_rows = execution_gate["gate_rows"]
    assert len(gate_rows) == 4
    assert all(row["execution_status"] == "blocked_by_open_authorization_prerequisites" for row in gate_rows)
    assert all(row["open_prerequisite_count"] == 5 for row in gate_rows)
    assert all(row["network_access_allowed"] is False for row in gate_rows)
    assert all(row["retrieval_may_execute"] is False for row in gate_rows)
    assert all(row["source_content_may_be_fetched"] is False for row in gate_rows)
    assert execution_gate["authorization_state"]["materialization_execution_gate_recorded"] is True
    assert execution_gate["authorization_state"]["all_authorization_prerequisites_closed"] is False
    assert execution_gate["authorization_state"]["materialization_execution_authorized"] is False
    assert execution_gate["authorization_state"]["network_access_authorized"] is False
    assert execution_gate["authorization_state"]["retrieval_executed"] is False
    assert execution_gate["authorization_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "blocked"
    assert check_rows["check-prerequisite-closure-matrix-linked"]["status"] == "complete"
    assert check_rows["check-execution-gate-rows-cover-materialization-batches"]["status"] == "complete"
    assert check_rows["check-materialization-execution-denied"]["status"] == "blocked"
    assert check_rows["check-execution-gate-denies-network"]["status"] == "blocked"
    assert check_rows["check-materialization-execution-gate-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_authorization_materialization_execution_gate_checks_written" in transcript


def test_godproof_records_bad_god_evidential_calibration_source_content_materialization_future_command_manifest(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    manifest = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-future-command-manifest.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-future-command-manifest-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    command_manifest = manifest["future_command_manifest"]
    assert manifest["status"] == "blocked"
    assert command_manifest["input_materialization_execution_gate_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-authorization-materialization-execution-gate-v0"
    )
    assert command_manifest["manifest_scope"] == "future_content_materialization_fetch_commands"
    assert command_manifest["commands_executable"] is False
    commands = command_manifest["commands"]
    assert len(commands) == 4
    assert all(row["command_status"] == "not_executable_authorization_gate_blocked" for row in commands)
    assert all(row["network_access_allowed"] is False for row in commands)
    assert all(row["retrieval_may_execute"] is False for row in commands)
    assert all(row["command_executed"] is False for row in commands)
    assert all(row["source_content_fetched"] is False for row in commands)
    assert all(row["command_template"].startswith("kr materialize-source-content") for row in commands)
    assert command_manifest["authorization_state"]["future_command_manifest_recorded"] is True
    assert command_manifest["authorization_state"]["materialization_execution_authorized"] is False
    assert command_manifest["authorization_state"]["network_access_authorized"] is False
    assert command_manifest["authorization_state"]["retrieval_executed"] is False
    assert command_manifest["authorization_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "blocked"
    assert check_rows["check-materialization-execution-gate-linked"]["status"] == "complete"
    assert check_rows["check-future-commands-cover-gate-rows"]["status"] == "complete"
    assert check_rows["check-future-commands-not-executable"]["status"] == "blocked"
    assert check_rows["check-future-commands-deny-network"]["status"] == "blocked"
    assert check_rows["check-future-command-manifest-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_future_command_manifest_checks_written" in transcript


def test_godproof_records_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    receipt = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-nonexecution-receipt.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-nonexecution-receipt-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    nonexecution = receipt["command_nonexecution_receipt"]
    assert receipt["status"] == "blocked"
    assert nonexecution["input_future_command_manifest_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-future-command-manifest-v0"
    )
    assert nonexecution["receipt_scope"] == "content_materialization_command_nonexecution_receipt"
    assert nonexecution["command_count"] == 4
    assert nonexecution["executed_command_count"] == 0
    assert nonexecution["source_content_file_count"] == 0
    assert nonexecution["retrieval_log_count"] == 0
    assert nonexecution["content_hash_count"] == 0
    receipt_rows = nonexecution["receipt_rows"]
    assert len(receipt_rows) == 4
    assert all(row["receipt_status"] == "not_executed" for row in receipt_rows)
    assert all(row["command_executed"] is False for row in receipt_rows)
    assert all(row["source_content_fetched"] is False for row in receipt_rows)
    assert all(row["retrieval_log_written"] is False for row in receipt_rows)
    assert all(row["content_hash_written"] is False for row in receipt_rows)
    assert nonexecution["authorization_state"]["command_nonexecution_receipt_recorded"] is True
    assert nonexecution["authorization_state"]["network_access_authorized"] is False
    assert nonexecution["authorization_state"]["retrieval_executed"] is False
    assert nonexecution["authorization_state"]["source_content_fetched"] is False
    assert nonexecution["authorization_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "blocked"
    assert check_rows["check-future-command-manifest-linked"]["status"] == "complete"
    assert check_rows["check-nonexecution-rows-cover-future-commands"]["status"] == "complete"
    assert check_rows["check-commands-remain-unexecuted"]["status"] == "blocked"
    assert check_rows["check-no-content-outputs-written"]["status"] == "blocked"
    assert check_rows["check-command-nonexecution-receipt-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_nonexecution_receipt_checks_written" in transcript


def test_godproof_records_bad_god_evidential_calibration_source_content_materialization_command_output_gap_ledger(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    ledger = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-ledger.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    output_gaps = ledger["command_output_gap_ledger"]
    assert ledger["status"] == "blocked"
    assert output_gaps["input_command_nonexecution_receipt_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-nonexecution-receipt-v0"
    )
    assert output_gaps["gap_scope"] == "content_materialization_command_output_gaps"
    assert output_gaps["command_count"] == 4
    assert output_gaps["missing_source_content_file_count"] == 4
    assert output_gaps["missing_retrieval_log_count"] == 4
    assert output_gaps["missing_content_hash_count"] == 4
    assert output_gaps["open_gap_count"] == 12
    gap_rows = output_gaps["gap_rows"]
    assert len(gap_rows) == 4
    assert all(row["command_executed"] is False for row in gap_rows)
    assert all(row["source_content_file_status"] == "missing" for row in gap_rows)
    assert all(row["retrieval_log_status"] == "missing" for row in gap_rows)
    assert all(row["content_hash_status"] == "missing" for row in gap_rows)
    assert all(
        row["missing_output_types"] == ["source_content_file", "retrieval_log", "content_hash"]
        for row in gap_rows
    )
    assert output_gaps["authorization_state"]["command_output_gap_ledger_recorded"] is True
    assert output_gaps["authorization_state"]["network_access_authorized"] is False
    assert output_gaps["authorization_state"]["retrieval_executed"] is False
    assert output_gaps["authorization_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "blocked"
    assert check_rows["check-command-nonexecution-receipt-linked"]["status"] == "complete"
    assert check_rows["check-gap-rows-cover-receipt-commands"]["status"] == "complete"
    assert check_rows["check-all-content-outputs-missing"]["status"] == "blocked"
    assert check_rows["check-output-gap-ledger-keeps-network-denied"]["status"] == "blocked"
    assert check_rows["check-command-output-gap-ledger-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_ledger_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_checks_written" in transcript


def test_godproof_records_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_queue(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    queue = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-task-queue.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-task-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    closure_queue = queue["command_output_gap_closure_task_queue"]
    assert queue["status"] == "blocked"
    assert closure_queue["input_command_output_gap_ledger_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-ledger-v0"
    )
    assert closure_queue["queue_scope"] == "content_materialization_command_output_gap_closure_tasks"
    assert closure_queue["command_count"] == 4
    assert closure_queue["gap_row_count"] == 4
    assert closure_queue["task_count"] == 12
    assert closure_queue["open_task_count"] == 12
    assert closure_queue["output_types"] == ["source_content_file", "retrieval_log", "content_hash"]
    task_rows = closure_queue["task_rows"]
    assert len(task_rows) == 12
    assert {row["output_type"] for row in task_rows} == {
        "source_content_file",
        "retrieval_log",
        "content_hash",
    }
    assert all(row["task_status"] == "queued_blocked_by_authorization" for row in task_rows)
    assert all(row["closure_authorized"] is False for row in task_rows)
    assert all(row["output_materialized"] is False for row in task_rows)
    assert all(row["proof_evidence_materialized"] is False for row in task_rows)
    assert closure_queue["authorization_state"]["gap_closure_task_queue_recorded"] is True
    assert closure_queue["authorization_state"]["materialization_execution_authorized"] is False
    assert closure_queue["authorization_state"]["network_access_authorized"] is False
    assert closure_queue["authorization_state"]["retrieval_executed"] is False
    assert closure_queue["authorization_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "blocked"
    assert check_rows["check-output-gap-ledger-linked"]["status"] == "complete"
    assert check_rows["check-closure-tasks-cover-output-gaps"]["status"] == "complete"
    assert check_rows["check-closure-tasks-remain-blocked"]["status"] == "blocked"
    assert check_rows["check-no-gap-closures-materialized"]["status"] == "blocked"
    assert check_rows["check-output-gap-closure-task-queue-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_queue_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_task_checks_written" in transcript


def test_godproof_records_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_plan(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    plan = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-plan.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    batch_plan = plan["command_output_gap_closure_batch_plan"]
    assert plan["status"] == "blocked"
    assert batch_plan["input_command_output_gap_closure_task_queue_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-task-queue-v0"
    )
    assert batch_plan["plan_scope"] == "content_materialization_command_output_gap_closure_batches"
    assert batch_plan["command_count"] == 4
    assert batch_plan["batch_count"] == 4
    assert batch_plan["task_count"] == 12
    assert batch_plan["open_batch_count"] == 4
    batches = batch_plan["batches"]
    assert len(batches) == 4
    assert [row["batch_order"] for row in batches] == [1, 2, 3, 4]
    assert all(row["batch_status"] == "queued_blocked_by_authorization" for row in batches)
    assert all(row["execution_allowed"] is False for row in batches)
    assert all(row["task_count"] == 3 for row in batches)
    assert all(row["outputs_to_materialize"] == ["source_content_file", "retrieval_log", "content_hash"] for row in batches)
    assert all(row["proof_evidence_materialized"] is False for row in batches)
    assert batch_plan["authorization_state"]["gap_closure_batch_plan_recorded"] is True
    assert batch_plan["authorization_state"]["materialization_execution_authorized"] is False
    assert batch_plan["authorization_state"]["network_access_authorized"] is False
    assert batch_plan["authorization_state"]["retrieval_executed"] is False
    assert batch_plan["authorization_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "blocked"
    assert check_rows["check-closure-task-queue-linked"]["status"] == "complete"
    assert check_rows["check-batches-cover-closure-tasks"]["status"] == "complete"
    assert check_rows["check-batches-remain-blocked"]["status"] == "blocked"
    assert check_rows["check-no-batch-output-materialized"]["status"] == "blocked"
    assert check_rows["check-gap-closure-batch-plan-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_plan_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_checks_written" in transcript


def test_godproof_records_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_ledger(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    ledger = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-ledger.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    execution_ledger = ledger["command_output_gap_closure_batch_execution_ledger"]
    assert ledger["status"] == "blocked"
    assert execution_ledger["input_command_output_gap_closure_batch_plan_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-plan-v0"
    )
    assert execution_ledger["ledger_scope"] == "content_materialization_command_output_gap_closure_batch_execution"
    assert execution_ledger["batch_count"] == 4
    assert execution_ledger["task_count"] == 12
    assert execution_ledger["executed_batch_count"] == 0
    assert execution_ledger["materialized_output_count"] == 0
    execution_rows = execution_ledger["execution_rows"]
    assert len(execution_rows) == 4
    assert all(row["execution_status"] == "not_started_authorization_blocked" for row in execution_rows)
    assert all(row["execution_started"] is False for row in execution_rows)
    assert all(row["execution_completed"] is False for row in execution_rows)
    assert all(row["outputs_materialized"] is False for row in execution_rows)
    assert all(row["retrieval_log_written"] is False for row in execution_rows)
    assert all(row["content_hash_written"] is False for row in execution_rows)
    assert all(row["proof_evidence_materialized"] is False for row in execution_rows)
    assert execution_ledger["authorization_state"]["batch_execution_ledger_recorded"] is True
    assert execution_ledger["authorization_state"]["materialization_execution_authorized"] is False
    assert execution_ledger["authorization_state"]["network_access_authorized"] is False
    assert execution_ledger["authorization_state"]["retrieval_executed"] is False
    assert execution_ledger["authorization_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "blocked"
    assert check_rows["check-gap-closure-batch-plan-linked"]["status"] == "complete"
    assert check_rows["check-execution-rows-cover-batches"]["status"] == "complete"
    assert check_rows["check-batch-execution-not-started"]["status"] == "blocked"
    assert check_rows["check-no-execution-outputs-materialized"]["status"] == "blocked"
    assert check_rows["check-gap-closure-batch-execution-ledger-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_ledger_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_checks_written" in transcript


def test_godproof_records_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_matrix(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    matrix = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-matrix.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    unblockers = matrix["command_output_gap_closure_batch_execution_unblocker_matrix"]
    assert matrix["status"] == "blocked"
    assert unblockers["input_command_output_gap_closure_batch_execution_ledger_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-ledger-v0"
    )
    assert unblockers["matrix_scope"] == "content_materialization_command_output_gap_closure_batch_execution_unblockers"
    assert unblockers["batch_count"] == 4
    assert unblockers["unblocker_type_count"] == 5
    assert unblockers["unblocker_cell_count"] == 20
    assert unblockers["open_unblocker_count"] == 20
    assert unblockers["unblocker_types"] == [
        "operator_approval_reference",
        "terms_rate_limit_clearance",
        "private_sensitive_risk_clearance",
        "retrieval_scope_clearance",
        "logging_hash_plan_clearance",
    ]
    matrix_rows = unblockers["matrix_rows"]
    assert len(matrix_rows) == 4
    assert all(row["execution_started"] is False for row in matrix_rows)
    assert all(len(row["unblockers"]) == 5 for row in matrix_rows)
    assert all(
        cell["unblocker_status"] == "open"
        for row in matrix_rows
        for cell in row["unblockers"]
    )
    assert all(
        cell["authorization_required"] is True
        for row in matrix_rows
        for cell in row["unblockers"]
    )
    assert all(
        cell["resolved"] is False
        for row in matrix_rows
        for cell in row["unblockers"]
    )
    assert unblockers["authorization_state"]["unblocker_matrix_recorded"] is True
    assert unblockers["authorization_state"]["materialization_execution_authorized"] is False
    assert unblockers["authorization_state"]["network_access_authorized"] is False
    assert unblockers["authorization_state"]["retrieval_executed"] is False
    assert unblockers["authorization_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "blocked"
    assert check_rows["check-batch-execution-ledger-linked"]["status"] == "complete"
    assert check_rows["check-unblocker-rows-cover-execution-batches"]["status"] == "complete"
    assert check_rows["check-unblocker-cells-cover-required-prerequisites"]["status"] == "complete"
    assert check_rows["check-all-unblockers-remain-open"]["status"] == "blocked"
    assert check_rows["check-batch-execution-unblocker-matrix-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_matrix_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_checks_written" in transcript


def test_godproof_records_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_queue(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    queue = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-queue.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    resolution_queue = queue["command_output_gap_closure_batch_execution_unblocker_resolution_queue"]
    assert queue["status"] == "blocked"
    assert resolution_queue["input_command_output_gap_closure_batch_execution_unblocker_matrix_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-matrix-v0"
    )
    assert resolution_queue["queue_scope"] == "content_materialization_batch_execution_unblocker_resolution"
    assert resolution_queue["batch_count"] == 4
    assert resolution_queue["unblocker_cell_count"] == 20
    assert resolution_queue["resolution_task_count"] == 20
    assert resolution_queue["open_resolution_task_count"] == 20
    assert resolution_queue["priority_order"] == [
        "operator_approval_reference",
        "terms_rate_limit_clearance",
        "private_sensitive_risk_clearance",
        "retrieval_scope_clearance",
        "logging_hash_plan_clearance",
    ]
    task_rows = resolution_queue["resolution_tasks"]
    assert len(task_rows) == 20
    assert {row["resolution_status"] for row in task_rows} == {"queued_open"}
    assert all(row["resolution_authorized"] is False for row in task_rows)
    assert all(row["unblocker_resolved"] is False for row in task_rows)
    assert [row["resolution_order"] for row in task_rows] == list(range(1, 21))
    assert resolution_queue["authorization_state"]["unblocker_resolution_queue_recorded"] is True
    assert resolution_queue["authorization_state"]["materialization_execution_authorized"] is False
    assert resolution_queue["authorization_state"]["network_access_authorized"] is False
    assert resolution_queue["authorization_state"]["retrieval_executed"] is False
    assert resolution_queue["authorization_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "blocked"
    assert check_rows["check-unblocker-matrix-linked"]["status"] == "complete"
    assert check_rows["check-resolution-tasks-cover-open-unblockers"]["status"] == "complete"
    assert check_rows["check-resolution-task-order-complete"]["status"] == "complete"
    assert check_rows["check-resolution-tasks-remain-open"]["status"] == "blocked"
    assert check_rows["check-unblocker-resolution-queue-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_queue_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_checks_written" in transcript


def test_godproof_records_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    plan = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-batch-plan.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-batch-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    batch_plan = plan["command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan"]
    assert plan["status"] == "blocked"
    assert batch_plan["input_command_output_gap_closure_batch_execution_unblocker_resolution_queue_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-queue-v0"
    )
    assert batch_plan["plan_scope"] == "content_materialization_batch_execution_unblocker_resolution_batches"
    assert batch_plan["resolution_task_count"] == 20
    assert batch_plan["resolution_batch_count"] == 5
    assert batch_plan["open_resolution_batch_count"] == 5
    batches = batch_plan["resolution_batches"]
    assert len(batches) == 5
    assert [row["resolution_batch_order"] for row in batches] == [1, 2, 3, 4, 5]
    assert [row["unblocker_type"] for row in batches] == batch_plan["priority_order"]
    assert all(row["resolution_task_count"] == 4 for row in batches)
    assert all(row["batch_status"] == "queued_open" for row in batches)
    assert all(row["resolution_authorized"] is False for row in batches)
    assert all(row["unblockers_resolved"] is False for row in batches)
    assert batch_plan["authorization_state"]["unblocker_resolution_batch_plan_recorded"] is True
    assert batch_plan["authorization_state"]["unblocker_resolution_authorized"] is False
    assert batch_plan["authorization_state"]["materialization_execution_authorized"] is False
    assert batch_plan["authorization_state"]["network_access_authorized"] is False
    assert batch_plan["authorization_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "blocked"
    assert check_rows["check-unblocker-resolution-queue-linked"]["status"] == "complete"
    assert check_rows["check-resolution-batches-cover-tasks"]["status"] == "complete"
    assert check_rows["check-resolution-batches-follow-priority-order"]["status"] == "complete"
    assert check_rows["check-resolution-batches-remain-open"]["status"] == "blocked"
    assert check_rows["check-unblocker-resolution-batch-plan-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_checks_written" in transcript


def test_godproof_records_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_execution_ledger(
    tmp_path: Path,
):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    ledger = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-batch-execution-ledger.json"
        ).read_text(encoding="utf-8")
    )
    checks = json.loads(
        (
            session_dir
            / "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-batch-execution-checks.json"
        ).read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    execution_ledger = ledger["command_output_gap_closure_batch_execution_unblocker_resolution_batch_execution_ledger"]
    assert ledger["status"] == "blocked"
    assert execution_ledger["input_command_output_gap_closure_batch_execution_unblocker_resolution_batch_plan_id"] == (
        "ontological-soundness-bad-god-evidential-calibration-source-content-materialization-command-output-gap-closure-batch-execution-unblocker-resolution-batch-plan-v0"
    )
    assert execution_ledger["ledger_scope"] == "content_materialization_unblocker_resolution_batch_execution"
    assert execution_ledger["resolution_batch_count"] == 5
    assert execution_ledger["resolution_task_count"] == 20
    assert execution_ledger["executed_resolution_batch_count"] == 0
    assert execution_ledger["resolved_unblocker_count"] == 0
    execution_rows = execution_ledger["execution_rows"]
    assert len(execution_rows) == 5
    assert all(row["execution_status"] == "not_started_authorization_blocked" for row in execution_rows)
    assert all(row["execution_started"] is False for row in execution_rows)
    assert all(row["execution_completed"] is False for row in execution_rows)
    assert all(row["unblockers_resolved"] is False for row in execution_rows)
    assert all(row["resolution_evidence_materialized"] is False for row in execution_rows)
    assert execution_ledger["authorization_state"]["unblocker_resolution_batch_execution_ledger_recorded"] is True
    assert execution_ledger["authorization_state"]["unblocker_resolution_authorized"] is False
    assert execution_ledger["authorization_state"]["materialization_execution_authorized"] is False
    assert execution_ledger["authorization_state"]["network_access_authorized"] is False
    assert execution_ledger["authorization_state"]["proof_claim_allowed"] is False
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "blocked"
    assert check_rows["check-resolution-batch-plan-linked"]["status"] == "complete"
    assert check_rows["check-execution-rows-cover-resolution-batches"]["status"] == "complete"
    assert check_rows["check-resolution-batch-execution-not-started"]["status"] == "blocked"
    assert check_rows["check-no-unblocker-resolution-materialized"]["status"] == "blocked"
    assert check_rows["check-unblocker-resolution-batch-execution-ledger-not-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_execution_ledger_written" in transcript
    assert "ontological_soundness_bad_god_evidential_calibration_source_content_materialization_command_output_gap_closure_batch_execution_unblocker_resolution_batch_execution_checks_written" in transcript


def test_godproof_writes_ontological_soundness_resolution_worklist(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    worklist = json.loads((session_dir / "ontological-soundness-resolution-worklist.json").read_text(
        encoding="utf-8"
    ))
    checks = json.loads((session_dir / "ontological-soundness-resolution-worklist-checks.json").read_text(
        encoding="utf-8"
    ))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert worklist["status"] == "contested"
    assert worklist["worklist"]["target_obligation_id"] == "obl-ontological-soundness"
    assert worklist["worklist"]["input_artifact"] == "ontological-soundness-checks.json"
    assert worklist["worklist"]["authorization_state"]["worklist_recorded"] is True
    assert worklist["worklist"]["authorization_state"]["soundness_proof_completed"] is False
    assert worklist["worklist"]["authorization_state"]["proof_claim_allowed"] is False
    assert len(worklist["worklist"]["work_items"]) >= 20
    assert all(row["work_status"] == "queued_not_executed" for row in worklist["worklist"]["work_items"])
    assert all(row["proof_evidence_materialized"] is False for row in worklist["worklist"]["work_items"])
    assert any(
        row["source_check_id"] == "check-unresolved-parodies-retained"
        for row in worklist["worklist"]["work_items"]
    )
    assert any(
        row["source_artifact"] == "possible-necessary-existence-checks.json"
        for row in worklist["worklist"]["work_items"]
    )
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-ontological-soundness-checks-linked"]["status"] == "complete"
    assert check_rows["check-contested-soundness-checks-have-work-items"]["status"] == "complete"
    assert check_rows["check-contested-linked-artifacts-have-work-items"]["status"] == "complete"
    assert check_rows["check-work-items-remain-unexecuted"]["status"] == "complete"
    assert check_rows["check-worklist-not-promoted-to-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_resolution_worklist_written" in transcript
    assert "ontological_soundness_resolution_worklist_checks_written" in transcript


def test_godproof_batches_ontological_soundness_resolution_work(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    batches = json.loads((session_dir / "ontological-soundness-resolution-batches.json").read_text(
        encoding="utf-8"
    ))
    checks = json.loads((session_dir / "ontological-soundness-resolution-batch-checks.json").read_text(
        encoding="utf-8"
    ))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert batches["status"] == "contested"
    assert batches["batch_plan"]["input_worklist_id"] == "ontological-soundness-resolution-worklist-v0"
    assert batches["batch_plan"]["target_obligation_id"] == "obl-ontological-soundness"
    assert batches["batch_plan"]["authorization_state"]["batches_recorded"] is True
    assert batches["batch_plan"]["authorization_state"]["batch_execution_completed"] is False
    assert batches["batch_plan"]["authorization_state"]["proof_claim_allowed"] is False
    assert len(batches["batch_plan"]["batches"]) >= 6
    assert all(row["batch_status"] == "queued_not_executed" for row in batches["batch_plan"]["batches"])
    assert all(row["proof_evidence_materialized"] is False for row in batches["batch_plan"]["batches"])
    assert all("rtk env PYTHONPATH=src python3 -m pytest tests/test_godproof.py -q" in row["verifier_commands"] for row in batches["batch_plan"]["batches"])
    assert {
        "resolve-dossier-direct-blockers",
        "resolve-possibility-bridge-chain",
        "resolve-rival-and-positive-property-chain",
        "resolve-evidential-evil-and-moral-pressure-chain",
    } <= {row["batch_id"] for row in batches["batch_plan"]["batches"]}
    batch_work_item_ids = {
        work_item_id
        for row in batches["batch_plan"]["batches"]
        for work_item_id in row["work_item_ids"]
    }
    assert len(batch_work_item_ids) == 30
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-resolution-worklist-linked"]["status"] == "complete"
    assert check_rows["check-every-work-item-assigned-to-batch"]["status"] == "complete"
    assert check_rows["check-batches-have-verifiers-and-acceptance-gates"]["status"] == "complete"
    assert check_rows["check-batches-remain-unexecuted"]["status"] == "complete"
    assert check_rows["check-batches-not-promoted-to-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_resolution_batches_written" in transcript
    assert "ontological_soundness_resolution_batch_checks_written" in transcript


def test_godproof_records_ontological_soundness_batch_execution_ledger(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    ledger = json.loads((session_dir / "ontological-soundness-batch-execution-ledger.json").read_text(
        encoding="utf-8"
    ))
    checks = json.loads((session_dir / "ontological-soundness-batch-execution-checks.json").read_text(
        encoding="utf-8"
    ))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert ledger["status"] == "contested"
    assert ledger["ledger"]["input_batch_plan_id"] == "ontological-soundness-resolution-batches-v0"
    assert ledger["ledger"]["target_obligation_id"] == "obl-ontological-soundness"
    assert ledger["ledger"]["authorization_state"]["execution_ledger_recorded"] is True
    assert ledger["ledger"]["authorization_state"]["batch_execution_started"] is False
    assert ledger["ledger"]["authorization_state"]["batch_execution_completed"] is False
    assert ledger["ledger"]["authorization_state"]["proof_claim_allowed"] is False
    assert len(ledger["ledger"]["execution_records"]) == 6
    assert all(row["execution_status"] == "not_started" for row in ledger["ledger"]["execution_records"])
    assert all(row["proof_evidence_materialized"] is False for row in ledger["ledger"]["execution_records"])
    assert all(row["future_log_event_types"] for row in ledger["ledger"]["execution_records"])
    assert all(row["output_artifact_targets"] for row in ledger["ledger"]["execution_records"])
    assert all("rtk env PYTHONPATH=src python3 -m pytest -q" in row["verifier_commands"] for row in ledger["ledger"]["execution_records"])
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert checks["status"] == "contested"
    assert check_rows["check-batch-plan-linked"]["status"] == "complete"
    assert check_rows["check-every-batch-has-execution-record"]["status"] == "complete"
    assert check_rows["check-execution-records-have-logs-verifiers-and-targets"]["status"] == "complete"
    assert check_rows["check-execution-not-started"]["status"] == "complete"
    assert check_rows["check-execution-ledger-not-promoted-to-proof"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "ontological_soundness_batch_execution_ledger_written" in transcript
    assert "ontological_soundness_batch_execution_checks_written" in transcript


def test_godproof_screens_target_attribute_coherence(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    ledger = json.loads((session_dir / "attribute-coherence-ledger.json").read_text(encoding="utf-8"))
    checks = json.loads((session_dir / "attribute-coherence-checks.json").read_text(encoding="utf-8"))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert ledger["status"] == "contested"
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-target-attribute-coverage"]["status"] == "complete"
    assert check_rows["check-defeater-tests-present"]["status"] == "complete"
    assert check_rows["check-direct-definition-contradiction"]["status"] == "complete"
    assert check_rows["check-unresolved-attribute-tensions-retained"]["status"] == "contested"
    assert check_rows["check-possibility-not-established"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["ontological_soundness_status"] == "contested"
    assert "attribute_coherence_checks_written" in transcript


def test_godproof_models_coherent_conceivability_repairs(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    model = json.loads((session_dir / "coherent-conceivability-model.json").read_text(encoding="utf-8"))
    checks = json.loads((session_dir / "coherent-conceivability-checks.json").read_text(encoding="utf-8"))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert model["status"] == "candidate_supported_contested"
    assert checks["status"] == "candidate_supported_contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-every-tension-has-repair-model"]["status"] == "complete"
    assert check_rows["check-repair-models-are-candidates"]["status"] == "complete"
    assert check_rows["check-explicit-contradiction-not-found"]["status"] == "complete"
    assert check_rows["check-live-defeaters-retained"]["status"] == "contested"
    assert check_rows["check-not-promoted-to-metaphysical-possibility"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "coherent_conceivability_checks_written" in transcript


def test_godproof_evaluates_metaphysical_possibility_bridge(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    bridge = json.loads((session_dir / "metaphysical-possibility-bridge.json").read_text(encoding="utf-8"))
    checks = json.loads((session_dir / "metaphysical-possibility-checks.json").read_text(encoding="utf-8"))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert bridge["status"] == "contested"
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-coherent-conceivability-input-linked"]["status"] == "complete"
    assert check_rows["check-support-routes-present"]["status"] == "complete"
    assert check_rows["check-defeater-routes-present"]["status"] == "complete"
    assert check_rows["check-independent-complete-route-missing"]["status"] == "contested"
    assert check_rows["check-live-defeaters-block-bridge"]["status"] == "contested"
    assert check_rows["check-bridge-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "metaphysical_possibility_checks_written" in transcript


def test_godproof_audits_definition_smuggling(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    audit = json.loads((session_dir / "definition-smuggling-audit.json").read_text(encoding="utf-8"))
    checks = json.loads((session_dir / "definition-smuggling-checks.json").read_text(encoding="utf-8"))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert audit["status"] == "contested"
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-distinction-rules-present"]["status"] == "complete"
    assert check_rows["check-smuggling-tests-present"]["status"] == "complete"
    assert check_rows["check-no-syntactic-actuality-smuggling"]["status"] == "complete"
    assert check_rows["check-independent-support-still-fails"]["status"] == "contested"
    assert check_rows["check-live-objections-retained"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "definition_smuggling_checks_written" in transcript


def test_godproof_writes_evidential_evil_attribution_templates(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    ledger = json.loads(
        (session_dir / "evidential-evil-attribution-template-ledger.json").read_text(encoding="utf-8")
    )
    checks = json.loads(
        (session_dir / "evidential-evil-attribution-template-checks.json").read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert ledger["status"] == "contested"
    assert ledger["ledger"]["input_license_privacy_review_id"] == "evidential-evil-license-privacy-review-v0"
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-license-privacy-review-linked"]["status"] == "complete"
    assert check_rows["check-every-reviewed-source-has-template"]["status"] == "complete"
    assert check_rows["check-required-attribution-fields-present"]["status"] == "complete"
    assert check_rows["check-templates-remain-draft"]["status"] == "contested"
    assert check_rows["check-publication-requirements-still-open"]["status"] == "contested"
    assert check_rows["check-attribution-templates-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "evidential_evil_attribution_template_checks_written" in transcript


def test_godproof_writes_evidential_evil_license_decision_packet(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    packet = json.loads((session_dir / "evidential-evil-license-decision-packet.json").read_text(encoding="utf-8"))
    checks = json.loads((session_dir / "evidential-evil-license-decision-checks.json").read_text(encoding="utf-8"))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert packet["status"] == "contested"
    assert packet["packet"]["authorization_state"]["retained_ingestion_allowed"] is False
    assert packet["packet"]["input_license_privacy_review_id"] == "evidential-evil-license-privacy-review-v0"
    assert packet["packet"]["input_attribution_template_ledger_id"] == (
        "evidential-evil-attribution-template-ledger-v0"
    )
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-license-privacy-review-linked"]["status"] == "complete"
    assert check_rows["check-attribution-template-ledger-linked"]["status"] == "complete"
    assert check_rows["check-every-reviewed-source-has-license-decision-record"]["status"] == "complete"
    assert check_rows["check-evidence-and-required-actions-recorded"]["status"] == "complete"
    assert check_rows["check-retained-ingestion-not-authorized"]["status"] == "contested"
    assert check_rows["check-manual-review-risks-retained"]["status"] == "contested"
    assert check_rows["check-license-decisions-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "evidential_evil_license_decision_checks_written" in transcript


def test_godproof_writes_evidential_evil_microdata_minimization_policy(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    policy = json.loads(
        (session_dir / "evidential-evil-microdata-minimization-policy.json").read_text(encoding="utf-8")
    )
    checks = json.loads(
        (session_dir / "evidential-evil-microdata-minimization-checks.json").read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert policy["status"] == "contested"
    assert policy["policy"]["authorization_state"]["raw_microdata_storage_allowed"] is False
    assert policy["policy"]["authorization_state"]["derived_aggregate_storage_allowed"] is False
    assert policy["policy"]["global_controls"]["raw_microdata_retention_allowed"] is False
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-license-privacy-review-linked"]["status"] == "complete"
    assert check_rows["check-license-decision-packet-linked"]["status"] == "complete"
    assert check_rows["check-every-reviewed-source-has-minimization-policy"]["status"] == "complete"
    assert check_rows["check-raw-retention-disabled"]["status"] == "complete"
    assert check_rows["check-source-evidence-and-blocked-fields-recorded"]["status"] == "complete"
    assert check_rows["check-survey-microdata-minimized"]["status"] == "complete"
    assert check_rows["check-derived-aggregate-schema-linked"]["status"] == "complete"
    assert check_rows["check-derived-aggregate-execution-requirements-open"]["status"] == "contested"
    assert check_rows["check-minimization-policy-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "evidential_evil_microdata_minimization_checks_written" in transcript


def test_godproof_writes_evidential_evil_derived_aggregate_schema(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    schema = json.loads((session_dir / "evidential-evil-derived-aggregate-schema.json").read_text(encoding="utf-8"))
    checks = json.loads(
        (session_dir / "evidential-evil-derived-aggregate-schema-checks.json").read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert schema["status"] == "contested"
    assert schema["schema"]["authorization_state"]["materialization_allowed"] is False
    assert schema["schema"]["input_microdata_minimization_policy_id"] == (
        "evidential-evil-microdata-minimization-policy-v0"
    )
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-microdata-policy-linked"]["status"] == "complete"
    assert check_rows["check-every-policy-source-has-derived-table"]["status"] == "complete"
    assert check_rows["check-table-allowlists-and-suppression-templates-present"]["status"] == "complete"
    assert check_rows["check-source-hash-placeholders-present"]["status"] == "complete"
    assert check_rows["check-raw-identifiers-blocked"]["status"] == "complete"
    assert check_rows["check-source-version-hash-preflight-linked"]["status"] == "complete"
    assert check_rows["check-suppression-report-template-linked"]["status"] == "complete"
    assert check_rows["check-materialization-requirements-still-open"]["status"] == "contested"
    assert check_rows["check-derived-schema-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "evidential_evil_derived_aggregate_schema_checks_written" in transcript


def test_godproof_writes_evidential_evil_source_version_hash_preflight(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    preflight = json.loads(
        (session_dir / "evidential-evil-source-version-hash-preflight.json").read_text(encoding="utf-8")
    )
    checks = json.loads(
        (session_dir / "evidential-evil-source-version-hash-preflight-checks.json").read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert preflight["status"] == "contested"
    assert preflight["preflight"]["authorization_state"]["download_allowed"] is False
    assert preflight["preflight"]["authorization_state"]["materialization_allowed"] is False
    assert len(preflight["preflight"]["source_records"]) == 8
    source_rows = {
        row["source_id"]: row
        for row in preflight["preflight"]["source_records"]
    }
    assert source_rows["gbif-occurrence-data"]["candidate_version_label"] == "GBIF download DOI required per query"
    assert source_rows["ucdp-conflict-data"]["candidate_version_label"] == "UCDP version 25.1 locator"
    assert all(row["hash_status"] == "not_recorded" for row in source_rows.values())
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-derived-aggregate-schema-linked"]["status"] == "complete"
    assert check_rows["check-every-schema-source-has-preflight-record"]["status"] == "complete"
    assert check_rows["check-version-locators-recorded"]["status"] == "complete"
    assert check_rows["check-hash-algorithm-and-targets-recorded"]["status"] == "complete"
    assert check_rows["check-table-bindings-present"]["status"] == "complete"
    assert check_rows["check-source-acquisition-hash-runbook-linked"]["status"] == "complete"
    assert check_rows["check-downloads-and-hashes-still-open"]["status"] == "contested"
    assert check_rows["check-source-version-hash-preflight-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "evidential_evil_source_version_hash_preflight_checks_written" in transcript


def test_godproof_writes_evidential_evil_source_acquisition_hash_runbook(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    runbook = json.loads(
        (session_dir / "evidential-evil-source-acquisition-hash-runbook.json").read_text(encoding="utf-8")
    )
    checks = json.loads(
        (session_dir / "evidential-evil-source-acquisition-hash-runbook-checks.json").read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert runbook["status"] == "contested"
    assert runbook["runbook"]["authorization_state"]["commands_recorded"] is True
    assert runbook["runbook"]["authorization_state"]["commands_executed"] is False
    assert runbook["runbook"]["authorization_state"]["download_allowed"] is False
    assert runbook["runbook"]["cache_policy"]["repo_storage_allowed"] is False
    assert runbook["runbook"]["hash_manifest_schema"]["manifest_status"] == "not_materialized"
    assert len(runbook["runbook"]["steps"]) == 8
    assert all(step["execution_status"] == "not_executed" for step in runbook["runbook"]["steps"])
    assert all("shasum -a 256" in step["hash_command_template"] for step in runbook["runbook"]["steps"])
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-source-version-hash-preflight-linked"]["status"] == "complete"
    assert check_rows["check-every-preflight-source-has-acquisition-step"]["status"] == "complete"
    assert check_rows["check-hash-manifest-schema-recorded"]["status"] == "complete"
    assert check_rows["check-hash-command-templates-recorded-not-executed"]["status"] == "complete"
    assert check_rows["check-required-log-events-recorded"]["status"] == "complete"
    assert check_rows["check-cache-retention-and-prune-step-recorded"]["status"] == "complete"
    assert check_rows["check-source-acquisition-still-open"]["status"] == "contested"
    assert check_rows["check-source-acquisition-runbook-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "evidential_evil_source_acquisition_hash_runbook_checks_written" in transcript


def test_godproof_writes_evidential_evil_suppression_report_template(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    template = json.loads(
        (session_dir / "evidential-evil-suppression-report-template.json").read_text(encoding="utf-8")
    )
    checks = json.loads(
        (session_dir / "evidential-evil-suppression-report-template-checks.json").read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert template["status"] == "contested"
    assert template["template"]["authorization_state"]["template_recorded"] is True
    assert template["template"]["authorization_state"]["suppression_reports_materialized"] is False
    assert template["template"]["authorization_state"]["publication_allowed"] is False
    assert template["template"]["report_schema"]["materialization_status"] == "not_materialized"
    assert len(template["template"]["table_templates"]) == 5
    assert all(row["minimum_cell_threshold"] == 10 for row in template["template"]["table_templates"])
    assert all(row["materialization_status"] == "not_materialized" for row in template["template"]["table_templates"])
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-derived-aggregate-schema-linked"]["status"] == "complete"
    assert check_rows["check-source-acquisition-hash-runbook-linked"]["status"] == "complete"
    assert check_rows["check-every-schema-table-has-suppression-template"]["status"] == "complete"
    assert check_rows["check-report-schema-recorded"]["status"] == "complete"
    assert check_rows["check-required-pre-publication-checks-recorded"]["status"] == "complete"
    assert check_rows["check-small-cell-thresholds-recorded"]["status"] == "complete"
    assert check_rows["check-suppression-reports-still-open"]["status"] == "contested"
    assert check_rows["check-suppression-template-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "evidential_evil_suppression_report_template_checks_written" in transcript


def test_godproof_reviews_evidential_evil_license_privacy_gates(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    review = json.loads((session_dir / "evidential-evil-license-privacy-review.json").read_text(encoding="utf-8"))
    checks = json.loads((session_dir / "evidential-evil-license-privacy-checks.json").read_text(encoding="utf-8"))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert review["status"] == "contested"
    assert review["review"]["input_ingestion_manifest_id"] == "evidential-evil-dataset-ingestion-manifest-v0"
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-ingestion-manifest-linked"]["status"] == "complete"
    assert check_rows["check-every-ingestion-source-has-review-item"]["status"] == "complete"
    assert check_rows["check-terms-urls-recorded"]["status"] == "complete"
    assert check_rows["check-privacy-tiers-recorded"]["status"] == "complete"
    assert check_rows["check-license-decisions-still-open"]["status"] == "contested"
    assert check_rows["check-license-decision-packet-linked"]["status"] == "complete"
    assert check_rows["check-attribution-template-linked"]["status"] == "complete"
    assert check_rows["check-microdata-minimization-policy-linked"]["status"] == "complete"
    assert check_rows["check-review-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "evidential_evil_license_privacy_checks_written" in transcript


def test_godproof_manifests_evidential_evil_dataset_ingestion(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    manifest = json.loads(
        (session_dir / "evidential-evil-dataset-ingestion-manifest.json").read_text(encoding="utf-8")
    )
    checks = json.loads(
        (session_dir / "evidential-evil-dataset-ingestion-checks.json").read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert manifest["status"] == "contested"
    assert manifest["manifest"]["input_selection_id"] == "evidential-evil-primary-dataset-selection-v0"
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-primary-selection-linked"]["status"] == "complete"
    assert check_rows["check-every-selected-source-has-ingestion-plan"]["status"] == "complete"
    assert check_rows["check-fetch-parse-specs-present"]["status"] == "complete"
    assert check_rows["check-storage-policy-present"]["status"] == "complete"
    assert check_rows["check-license-privacy-gates-present"]["status"] == "complete"
    assert check_rows["check-license-privacy-review-linked"]["status"] == "complete"
    assert check_rows["check-ingestion-not-executed"]["status"] == "contested"
    assert check_rows["check-ingestion-manifest-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "evidential_evil_dataset_ingestion_checks_written" in transcript


def test_godproof_selects_evidential_evil_primary_datasets(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    selection = json.loads(
        (session_dir / "evidential-evil-primary-dataset-selection.json").read_text(encoding="utf-8")
    )
    checks = json.loads(
        (session_dir / "evidential-evil-primary-dataset-selection-checks.json").read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert selection["status"] == "contested"
    assert selection["selection"]["input_empirical_expansion_id"] == "evidential-evil-empirical-expansion-ledger-v0"
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-empirical-expansion-linked"]["status"] == "complete"
    assert check_rows["check-selected-sources-known"]["status"] == "complete"
    assert check_rows["check-every-record-class-has-source"]["status"] == "complete"
    assert check_rows["check-dataset-requirements-covered"]["status"] == "complete"
    assert check_rows["check-coverage-limits-recorded"]["status"] == "complete"
    assert check_rows["check-ingestion-manifest-linked"]["status"] == "complete"
    assert check_rows["check-license-review-still-open"]["status"] == "contested"
    assert check_rows["check-selection-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "evidential_evil_primary_dataset_selection_checks_written" in transcript


def test_godproof_scaffolds_evidential_evil_empirical_expansion(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    ledger = json.loads(
        (session_dir / "evidential-evil-empirical-expansion-ledger.json").read_text(encoding="utf-8")
    )
    checks = json.loads(
        (session_dir / "evidential-evil-empirical-expansion-checks.json").read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert ledger["status"] == "contested"
    assert ledger["ledger"]["input_reviewed_records_id"] == "evidential-evil-reviewed-case-records-v0"
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-reviewed-records-linked"]["status"] == "complete"
    assert check_rows["check-every-case-family-has-empirical-class"]["status"] == "complete"
    assert check_rows["check-every-dimension-has-empirical-class"]["status"] == "complete"
    assert check_rows["check-dataset-requirements-present"]["status"] == "complete"
    assert check_rows["check-ingestion-requirements-present"]["status"] == "complete"
    assert check_rows["check-primary-dataset-selection-linked"]["status"] == "complete"
    assert check_rows["check-primary-data-not-ingested"]["status"] == "contested"
    assert check_rows["check-empirical-expansion-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "evidential_evil_empirical_expansion_checks_written" in transcript


def test_godproof_adds_reviewed_evidential_evil_case_records(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    records = json.loads((session_dir / "evidential-evil-reviewed-case-records.json").read_text(encoding="utf-8"))
    checks = json.loads(
        (session_dir / "evidential-evil-reviewed-case-records-checks.json").read_text(encoding="utf-8")
    )
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert records["status"] == "contested"
    assert records["records"]["input_case_corpus_id"] == "evidential-evil-case-corpus-v0"
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-case-corpus-linked"]["status"] == "complete"
    assert check_rows["check-every-case-family-has-record"]["status"] == "complete"
    assert check_rows["check-record-sources-known"]["status"] == "complete"
    assert check_rows["check-records-source-backed"]["status"] == "complete"
    assert check_rows["check-record-mapping-preserved"]["status"] == "complete"
    assert check_rows["check-empirical-expansion-linked"]["status"] == "complete"
    assert check_rows["check-severity-calibration-open"]["status"] == "contested"
    assert check_rows["check-reviewed-records-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "evidential_evil_reviewed_case_records_checks_written" in transcript


def test_godproof_maps_evidential_evil_case_corpus(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    corpus = json.loads((session_dir / "evidential-evil-case-corpus.json").read_text(encoding="utf-8"))
    checks = json.loads((session_dir / "evidential-evil-case-corpus-checks.json").read_text(encoding="utf-8"))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert corpus["status"] == "contested"
    assert corpus["corpus"]["input_calibration_id"] == "evidential-evil-calibration-ledger-v0"
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-calibration-ledger-linked"]["status"] == "complete"
    assert check_rows["check-case-families-present"]["status"] == "complete"
    assert check_rows["check-dimension-coverage"]["status"] == "complete"
    assert check_rows["check-cluster-coverage"]["status"] == "complete"
    assert check_rows["check-perspective-diversity"]["status"] == "complete"
    assert check_rows["check-reviewed-case-records-linked"]["status"] == "complete"
    assert check_rows["check-exhaustive-case-database-open"]["status"] == "contested"
    assert check_rows["check-case-corpus-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "evidential_evil_case_corpus_checks_written" in transcript


def test_godproof_calibrates_evidential_evil_clusters(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    ledger = json.loads((session_dir / "evidential-evil-calibration-ledger.json").read_text(encoding="utf-8"))
    checks = json.loads((session_dir / "evidential-evil-calibration-checks.json").read_text(encoding="utf-8"))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert ledger["status"] == "contested"
    assert ledger["ledger"]["input_model_id"] == "evidential-evil-dependence-model-v0"
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-dependence-model-linked"]["status"] == "complete"
    assert check_rows["check-cluster-weights-present"]["status"] == "complete"
    assert check_rows["check-dependence-strengths-present"]["status"] == "complete"
    assert check_rows["check-scenario-weight-profiles-present"]["status"] == "complete"
    assert check_rows["check-calibration-intervals-in-unit-range"]["status"] == "complete"
    assert check_rows["check-calibration-requirements-present"]["status"] == "complete"
    assert check_rows["check-case-corpus-linked"]["status"] == "complete"
    assert check_rows["check-calibration-requirements-open"]["status"] == "contested"
    assert check_rows["check-calibration-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "evidential_evil_calibration_checks_written" in transcript


def test_godproof_models_evidential_evil_dependence(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    model = json.loads((session_dir / "evidential-evil-dependence-model.json").read_text(encoding="utf-8"))
    checks = json.loads((session_dir / "evidential-evil-dependence-checks.json").read_text(encoding="utf-8"))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert model["status"] == "contested"
    assert model["model"]["input_ledger_id"] == "evidential-evil-likelihood-ledger-v0"
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-likelihood-ledger-linked"]["status"] == "complete"
    assert check_rows["check-all-dimensions-clustered"]["status"] == "complete"
    assert check_rows["check-aggregation-profiles-present"]["status"] == "complete"
    assert check_rows["check-naive-independence-rejected"]["status"] == "complete"
    assert check_rows["check-sensitivity-scenarios-present"]["status"] == "complete"
    assert check_rows["check-guardrails-active"]["status"] == "complete"
    assert check_rows["check-calibration-ledger-linked"]["status"] == "complete"
    assert check_rows["check-scenarios-remain-contested"]["status"] == "contested"
    assert check_rows["check-dependence-model-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "evidential_evil_dependence_checks_written" in transcript


def test_godproof_builds_evidential_evil_likelihood_ledger(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    ledger = json.loads((session_dir / "evidential-evil-likelihood-ledger.json").read_text(encoding="utf-8"))
    checks = json.loads((session_dir / "evidential-evil-likelihood-checks.json").read_text(encoding="utf-8"))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert ledger["status"] == "contested"
    assert ledger["ledger"]["probability_mode"] == "candidate_interval_model"
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-probability-audit-linked"]["status"] == "complete"
    assert check_rows["check-prior-intervals-declared"]["status"] == "complete"
    assert check_rows["check-likelihood-grid-complete"]["status"] == "complete"
    assert check_rows["check-intervals-in-unit-range"]["status"] == "complete"
    assert check_rows["check-rival-likelihoods-compared"]["status"] == "complete"
    assert check_rows["check-response-costs-declared"]["status"] == "complete"
    assert check_rows["check-dependence-model-linked"]["status"] == "complete"
    assert check_rows["check-wide-intervals-retained"]["status"] == "contested"
    assert check_rows["check-aggregation-not-final"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "evidential_evil_likelihood_checks_written" in transcript


def test_godproof_audits_evidential_evil_probability(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    audit = json.loads((session_dir / "evidential-evil-probability-audit.json").read_text(encoding="utf-8"))
    checks = json.loads((session_dir / "evidential-evil-probability-checks.json").read_text(encoding="utf-8"))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert audit["status"] == "contested"
    assert audit["audit"]["target_pressure_test_id"] == "evidential-probability-pressure"
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-pressure-input-linked"]["status"] == "complete"
    assert check_rows["check-hypotheses-present"]["status"] == "complete"
    assert check_rows["check-evidence-dimensions-present"]["status"] == "complete"
    assert check_rows["check-response-models-present"]["status"] == "complete"
    assert check_rows["check-likelihood-ledger-linked"]["status"] == "complete"
    assert check_rows["check-probability-requirements-candidate-addressed"]["status"] == "complete"
    assert check_rows["check-likelihoods-not-decisive"]["status"] == "contested"
    assert check_rows["check-live-objections-retained"]["status"] == "contested"
    assert check_rows["check-not-promoted-to-theodicy"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "evidential_evil_probability_checks_written" in transcript


def test_godproof_audits_evil_hiddenness_moral_pressure(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    audit = json.loads((session_dir / "evil-hiddenness-moral-pressure-audit.json").read_text(encoding="utf-8"))
    checks = json.loads((session_dir / "evil-hiddenness-moral-pressure-checks.json").read_text(encoding="utf-8"))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert audit["status"] == "contested"
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-all-evil-hiddenness-constraints-linked"]["status"] == "complete"
    assert check_rows["check-candidate-responses-present"]["status"] == "complete"
    assert check_rows["check-response-sufficiency-tests-present"]["status"] == "complete"
    assert check_rows["check-evidential-evil-probability-audit-linked"]["status"] == "complete"
    assert check_rows["check-substantive-pressure-tests-open"]["status"] == "contested"
    assert check_rows["check-not-promoted-to-solution"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "evil_hiddenness_moral_pressure_checks_written" in transcript


def test_godproof_audits_moral_perfection_grounding(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    audit = json.loads((session_dir / "moral-perfection-grounding-audit.json").read_text(encoding="utf-8"))
    checks = json.loads((session_dir / "moral-perfection-grounding-checks.json").read_text(encoding="utf-8"))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert audit["status"] == "contested"
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-candidate-groundings-present"]["status"] == "complete"
    assert check_rows["check-circularity-tests-present"]["status"] == "complete"
    assert check_rows["check-explicit-godlike-definition-avoided"]["status"] == "complete"
    assert check_rows["check-evil-hiddenness-moral-pressure-linked"]["status"] == "complete"
    assert check_rows["check-circularity-tests-still-open"]["status"] == "contested"
    assert check_rows["check-live-objections-retained"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "moral_perfection_grounding_checks_written" in transcript


def test_godproof_audits_positive_grounding(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    audit = json.loads((session_dir / "positive-grounding-audit.json").read_text(encoding="utf-8"))
    checks = json.loads((session_dir / "positive-grounding-checks.json").read_text(encoding="utf-8"))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert audit["status"] == "contested"
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-grounding-routes-present"]["status"] == "complete"
    assert check_rows["check-anti-ad-hoc-tests-present"]["status"] == "complete"
    assert check_rows["check-moral-perfection-grounding-audit-linked"]["status"] == "complete"
    assert check_rows["check-no-independent-complete-route"]["status"] == "contested"
    assert check_rows["check-open-anti-ad-hoc-tests-retained"]["status"] == "contested"
    assert check_rows["check-live-objections-retained"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "positive_grounding_checks_written" in transcript


def test_godproof_audits_positive_property_filter(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    audit = json.loads((session_dir / "positive-property-filter-audit.json").read_text(encoding="utf-8"))
    checks = json.loads((session_dir / "positive-property-filter-checks.json").read_text(encoding="utf-8"))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert audit["status"] == "contested"
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-positive-criteria-present"]["status"] == "complete"
    assert check_rows["check-bad-god-tests-present"]["status"] == "complete"
    assert check_rows["check-bad-god-candidates-screened"]["status"] == "complete"
    assert check_rows["check-positive-grounding-audit-linked"]["status"] == "complete"
    assert check_rows["check-non-arbitrary-grounding-open"]["status"] == "contested"
    assert check_rows["check-live-objections-retained"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "positive_property_filter_checks_written" in transcript


def test_godproof_audits_rival_necessary_parity(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    audit = json.loads((session_dir / "rival-necessary-parity-audit.json").read_text(encoding="utf-8"))
    checks = json.loads((session_dir / "rival-necessary-parity-checks.json").read_text(encoding="utf-8"))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert audit["status"] == "contested"
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-rival-concepts-present"]["status"] == "complete"
    assert check_rows["check-uniqueness-filters-present"]["status"] == "complete"
    assert check_rows["check-every-rival-has-some-filter"]["status"] == "complete"
    assert check_rows["check-positive-property-filter-audit-linked"]["status"] == "complete"
    assert check_rows["check-filters-not-independent-complete"]["status"] == "contested"
    assert check_rows["check-rival-parity-not-discharged"]["status"] == "contested"
    assert "necessary-impersonal-ultimate" in check_rows["check-rival-parity-not-discharged"]["unresolved_rival_ids"]
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "rival_necessary_parity_checks_written" in transcript


def test_godproof_evaluates_possible_necessary_existence_bridge(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    bridge = json.loads((session_dir / "possible-necessary-existence-bridge.json").read_text(encoding="utf-8"))
    checks = json.loads((session_dir / "possible-necessary-existence-checks.json").read_text(encoding="utf-8"))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert bridge["status"] == "contested"
    assert checks["status"] == "contested"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-metaphysical-possibility-input-linked"]["status"] == "complete"
    assert check_rows["check-modal-validity-linked"]["status"] == "complete"
    assert check_rows["check-modal-consistency-linked"]["status"] == "complete"
    assert check_rows["check-support-routes-complete"]["status"] == "complete"
    assert check_rows["check-definition-smuggling-audit-linked"]["status"] == "complete"
    assert check_rows["check-rival-necessary-parity-audit-linked"]["status"] == "complete"
    assert check_rows["check-soundness-defeaters-retained"]["status"] == "contested"
    assert check_rows["check-bridge-not-promoted"]["status"] == "contested"
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "possible_necessary_existence_checks_written" in transcript


def test_godproof_decomposes_possibility_premise_ladder(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    ladder = json.loads((session_dir / "possibility-premise-ladder.json").read_text(encoding="utf-8"))
    checks = json.loads((session_dir / "possibility-premise-checks.json").read_text(encoding="utf-8"))
    readiness = json.loads((session_dir / "proof-readiness.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert ladder["status"] == "contested"
    assert checks["status"] == "contested"
    stage_ids = [stage["id"] for stage in ladder["ladder"]["stages"]]
    assert stage_ids == [
        "target-schema-defined",
        "no-direct-schema-contradiction",
        "coherent-conceivability",
        "metaphysical-possibility",
        "possible-necessary-existence",
    ]
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-ladder-stage-order"]["status"] == "complete"
    assert check_rows["check-transition-chain-complete"]["status"] == "complete"
    assert check_rows["check-completed-foundation-stages"]["status"] == "complete"
    assert check_rows["check-coherent-conceivability-model-linked"]["status"] == "complete"
    assert check_rows["check-metaphysical-possibility-bridge-linked"]["status"] == "complete"
    assert check_rows["check-possible-necessary-existence-bridge-linked"]["status"] == "complete"
    assert check_rows["check-blocked-bridges-localized"]["status"] == "contested"
    assert check_rows["check-ladder-not-promoted-to-proof"]["status"] == "contested"
    assert "metaphysical-possibility" in check_rows["check-blocked-bridges-localized"]["blocked_stage_ids"]
    assert readiness["proof_claim_allowed"] is False
    assert readiness["blocking_open_obligation_ids"] == ["obl-ontological-soundness"]
    assert "possibility_premise_checks_written" in transcript


def test_godproof_builds_teleological_bayes_model(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    model = json.loads((session_dir / "teleological-bayes-model.json").read_text(encoding="utf-8"))
    checks = json.loads((session_dir / "teleological-bayes-checks.json").read_text(encoding="utf-8"))
    obligations = json.loads((session_dir / "formal-obligations.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert model["status"] == "encoded"
    hypothesis_ids = {h["id"] for h in model["model"]["hypotheses"]}
    assert model["base_case"]["top_hypothesis"] in hypothesis_ids
    assert checks["status"] == "complete"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-hypothesis-set"]["status"] == "complete"
    assert check_rows["check-anthropic-conditioning-declared"]["status"] == "complete"
    assert check_rows["check-multiverse-alternative-present"]["status"] == "complete"
    assert len(check_rows["check-sensitivity-varies"]["top_hypotheses"]) >= 2
    rows = {row["id"]: row for row in obligations["obligations"]}
    assert rows["obl-teleological-bayes"]["status"] == "complete"
    assert rows["obl-teleological-bayes"]["evidence_artifact"] == "teleological-bayes-checks.json"
    assert "teleological_bayes_checks_written" in transcript


def test_godproof_builds_cosmological_psr_model(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    model = json.loads((session_dir / "cosmological-psr-model.json").read_text(encoding="utf-8"))
    checks = json.loads((session_dir / "cosmological-psr-checks.json").read_text(encoding="utf-8"))
    obligations = json.loads((session_dir / "formal-obligations.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert model["status"] == "encoded"
    assert checks["status"] == "complete"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-psr-variant-taxonomy"]["status"] == "complete"
    assert check_rows["check-strong-psr-not-smuggled"]["status"] == "complete"
    assert "brute_fact" in check_rows["check-countermodels-present"]["countermodel_ids"]
    assert check_rows["check-necessary-ground-bridge-partial"]["status"] == "complete"
    assert check_rows["check-necessary-ground-bridge-partial"]["missing_attributes"]
    rows = {row["id"]: row for row in obligations["obligations"]}
    assert rows["obl-cosmological-psr"]["status"] == "complete"
    assert rows["obl-cosmological-psr"]["evidence_artifact"] == "cosmological-psr-checks.json"
    assert "cosmological_psr_checks_written" in transcript


def test_godproof_builds_evil_hiddenness_constraints(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    model = json.loads((session_dir / "evil-hiddenness-constraints.json").read_text(encoding="utf-8"))
    checks = json.loads((session_dir / "evil-hiddenness-checks.json").read_text(encoding="utf-8"))
    obligations = json.loads((session_dir / "formal-obligations.json").read_text(encoding="utf-8"))
    transcript = (session_dir / "transcript.jsonl").read_text(encoding="utf-8")

    assert model["status"] == "encoded"
    assert checks["status"] == "complete"
    check_rows = {row["id"]: row for row in checks["checks"]}
    assert check_rows["check-constraint-taxonomy"]["status"] == "complete"
    assert check_rows["check-target-attribute-links"]["status"] == "complete"
    assert check_rows["check-candidate-response-coverage"]["status"] == "complete"
    assert check_rows["check-unresolved-risks-retained"]["status"] == "complete"
    rows = {row["id"]: row for row in obligations["obligations"]}
    assert rows["obl-counter-evil-hiddenness"]["status"] == "complete"
    assert rows["obl-counter-evil-hiddenness"]["evidence_artifact"] == "evil-hiddenness-checks.json"
    assert "evil_hiddenness_checks_written" in transcript


def test_godproof_writes_formalization_skeleton(tmp_path: Path):
    summary = run_godproof(sessions_root=tmp_path)
    session_dir = Path(summary["session_dir"])

    skeleton = session_dir / "proof-assistant-skeletons" / "GodProof_Obligations.thy"
    text = skeleton.read_text(encoding="utf-8")

    assert "theory GodProof_Obligations" in text
    assert "This is not a verified proof of God" in text
    assert "PossiblyGodlike" in text
