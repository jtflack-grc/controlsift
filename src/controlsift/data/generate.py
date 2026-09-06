"""Deterministic synthetic evidence generator (charter §17)."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import re
from pathlib import Path
from typing import Any, Optional

import yaml

from controlsift import CANONICAL_SEED, LABELS
from controlsift.data.schema import EvidenceCase
from controlsift.data.split import apply_splits, assign_family_splits

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SCENARIOS = REPO_ROOT / "data" / "scenarios" / "scenario_families.yaml"
DEFAULT_OUT = REPO_ROOT / "data" / "processed"
DEFAULT_MANIFEST = REPO_ROOT / "data" / "manifests" / "dataset_manifest.json"
DEFAULT_REVIEW = REPO_ROOT / "data" / "review_log.csv"

ORGS = [
    "Northwind Health",
    "Cedar Ridge Logistics",
    "Blue Harbor Financial",
    "Summit Peak Utilities",
    "Harborline Retail",
    "Atlas Cloud Services",
    "Pinecrest Manufacturing",
    "Lumen Transit Group",
]

SYSTEMS = [
    "IdP-Prod",
    "SIEM-Core",
    "BackupVault",
    "PatchOrchestrator",
    "EndpointFleet",
    "ChangeMgmt",
    "VulnScanner",
    "NetFirewall",
    "KeyVault",
    "HRIS-Bridge",
]

ENVIRONMENTS = [
    "production identity platform",
    "production cloud tenancy",
    "enterprise SIEM",
    "production backup estate",
    "corporate endpoint management",
    "change management system",
    "vulnerability management platform",
    "production network edge",
    "encryption key management service",
    "privileged access workstation fleet",
]

FIRST_NAMES = ["Ava", "Noah", "Mia", "Liam", "Sofia", "Ethan", "Harper", "Owen"]
LAST_NAMES = ["Chen", "Patel", "Nguyen", "Brooks", "Okoro", "Silva", "Kim", "Garcia"]


def _rng(seed: int) -> random.Random:
    return random.Random(seed)


def _pick(rng: random.Random, items: list[Any]) -> Any:
    return items[rng.randrange(len(items))]


def _ticket(rng: random.Random) -> str:
    return f"CHG-{rng.randint(10000, 99999)}"


def _date(rng: random.Random, *, stale: bool = False) -> str:
    year = 2023 if stale else 2025
    month = rng.randint(1, 12)
    day = rng.randint(1, 28)
    return f"{year}-{month:02d}-{day:02d}"


def _account(rng: random.Random) -> str:
    return f"{_pick(rng, FIRST_NAMES).lower()}.{_pick(rng, LAST_NAMES).lower()}"


def _hash_id(family_id: str, variant_id: str) -> str:
    digest = hashlib.sha256(f"{family_id}:{variant_id}".encode()).hexdigest()[:8].upper()
    prefix = re.sub(r"[^A-Z0-9]+", "-", family_id.upper())[:12].strip("-")
    return f"CS-{prefix}-{digest}"


def load_scenario_families(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    families = data.get("families", data)
    if not isinstance(families, list):
        raise ValueError("scenario_families.yaml must contain a list under 'families'")
    return families


def _sufficient_text(family: dict[str, Any], ctx: dict[str, Any]) -> str:
    tmpl = family["sufficient_template"]
    return tmpl.format(**ctx)


_SYNONYM_PAIRS = [
    ("export", "extract"),
    ("report", "summary"),
    ("shows", "indicates"),
    ("lists", "enumerates"),
    ("successful", "completed"),
    ("failed", "unsuccessful"),
    ("disabled", "turned off"),
    ("enabled", "turned on"),
    ("accounts", "identities"),
    ("servers", "hosts"),
    ("during the", "for the"),
    ("production", "prod"),
    ("generated", "produced"),
    ("including", "with"),
]


def _surface_noise(text: str, rng: random.Random, *, p: float = 0.7) -> str:
    out = text
    for a, b in _SYNONYM_PAIRS:
        if rng.random() < p and a in out.lower():
            pattern = re.compile(re.escape(a), re.I)
            out = pattern.sub(b if rng.random() < 0.5 else a, out, count=1)
    return out


def _universal_decoy_block(
    family: dict[str, Any],
    ctx: dict[str, Any],
    rng: random.Random,
) -> str:
    """Append one line from every failure lexicon to EVERY case.

    This destroys label-unique n-gram shortcuts: TF-IDF sees the same cue phrases
    on SUFFICIENT through CONTRADICTORY. The true label lives in the core claim only.
    """
    distractor = family.get(
        "irrelevant_artifact",
        "a neighboring control export from the same platform",
    )
    who = _account(rng)
    decoys = [
        # partial-flavored
        _pick(
            rng,
            [
                f"Appendix note (ignore unless primary claim is incomplete): first query returned a subset of {ctx['unit']}s.",
                f"Planning memo mentions {ctx['pop_expected']} {ctx['unit']}s; do not treat planning memos as coverage proof.",
                "Cover sheet language about 'full population' appears in many binders and is not decisive alone.",
            ],
        ),
        # insufficient-flavored
        _pick(
            rng,
            [
                f"Policy/attestation excerpt for '{family['control_statement']}' is zipped for context only.",
                f"Signed note from {who} exists in the packet; whether it is the relied-upon artifact depends on the primary claim.",
                f"Collection runbook for {family['evidence_type'].lower()} may be present beside operational rows.",
                "Interpretation lines about intended state, empty fields, or procedure targets appear in many packets.",
                "Parenthetical hedges such as policy restatement only, attestation, intended state, or missing timestamp appear widely.",
                "Some numeric fields in side documents are blank placeholders and must not be confused with the primary extract.",
            ],
        ),
        # irrelevant-flavored
        _pick(
            rng,
            [
                f"Misfile risk: unrelated material such as '{distractor}' sometimes shares this binder tab.",
                f"Intake metadata always quotes the control and {ctx['system']} even when the binary is off-objective.",
                "Recycled binder/OCR text frequently restates a sufficient-looking claim beside off-objective substance.",
                "Sufficient-looking headers are frequently copied during upload and are not proof of relevance.",
            ],
        ),
        # contradictory-flavored
        _pick(
            rng,
            [
                "Exception discussion appears in reviewer chat; chat alone does not establish a control failure in the artifact.",
                "Cover memos often assert 'no open exceptions' irrespective of row-level values.",
                "Row detail lines must be read carefully; similar phrasing appears in clean and failing packets.",
                f"Conflict language is common in working papers for {ctx['org']} and requires checking the primary rows.",
            ],
        ),
        # sufficient-flavored
        _pick(
            rng,
            [
                f"Primary file date on the intake form is {ctx['date']}; older {ctx['stale_date']} material may be superseded.",
                "Reviewer sticky: classify from substance of the primary claim, not binder vocabulary.",
                f"Ticket {ctx['ticket']} cross-links exist for nearly every packet in this sample.",
            ],
        ),
    ]
    # Literal failure lexemes (not just mentions) so INSUFFICIENT/CONTRADICTORY n-grams collide.
    decoys.extend(
        [
            (
                f"(policy restatement only; {ctx['system']} executed values absent) "
                f"(attestation by {who}; field values unpopulated) "
                f"(intended post-{ctx['ticket']} state, not observed on {ctx['date']}) "
                f"(collection procedure target, not period output) "
                f"(capture lacks verifiable timestamp/boundary for {ctx['org']})"
            ),
            (
                f"Chat-only failure talk (not ROW_DETAIL): account {who} still active / Disabled / "
                f"Still Pending / status Still Open appeared in reviewer notes dated {ctx['stale_date']}."
            ),
            f"Period marker examples from other binders: {ctx['stale_date']} and on 2023-06-15.",
        ]
    )
    rng.shuffle(decoys)
    return " ".join(decoys)


def _benign_row_detail(family: dict[str, Any], ctx: dict[str, Any], rng: random.Random) -> str:
    """Compliant-looking row line; shares shape with contradiction templates."""
    return _pick(
        rng,
        [
            (
                f"Sampled {ctx['unit']} record for {ctx['account']} in {ctx['env']} on {ctx['date']} "
                f"shows expected compliant status at {ctx['org']}."
            ),
            (
                f"Spot check on {ctx['system']} for {ctx['org']} dated {ctx['date']} "
                f"aligns with '{family['control_statement']}' in {ctx['env']}."
            ),
            (
                f"No failing {ctx['unit']} rows were highlighted in the reviewer excerpt for {ctx['org']} "
                f"on {ctx['date']}."
            ),
        ],
    )


def _modalize_base(
    base: str,
    family: dict[str, Any],
    ctx: dict[str, Any],
    rng: random.Random,
) -> tuple[str, list[str]]:
    """Make the claim non-evidential while preserving most tokens."""
    control = family["control_statement"]
    who = _account(rng)
    mode = _pick(rng, ["policy", "attestation", "intent", "procedure", "undated"])
    # Insert a short hedge after the first clause-like break when possible.
    hedge = {
        "policy": (
            f"(policy restatement only; {ctx['system']} executed values absent for '{control}') ",
            ["policy_only"],
        ),
        "attestation": (
            f"(attestation by {who}; field values unpopulated) ",
            ["self_attestation"],
        ),
        "intent": (
            f"(intended post-{ctx['ticket']} state, not observed on {ctx['date']}) ",
            ["missing_execution_proof"],
        ),
        "procedure": (
            "(collection procedure target, not period output) ",
            ["procedure_only"],
        ),
        "undated": (
            f"(capture lacks verifiable timestamp/boundary for {ctx['org']}) ",
            ["missing_timestamp", "unverifiable_screenshot"],
        ),
    }[mode]
    insert, tags = hedge
    # Place hedge near the start so the sufficient skeleton remains intact after it.
    return f"{insert}{base}", tags


def _pack_packet(
    *,
    claim_text: str,
    distractor: str,
    expected: int,
    file_rows: int,
    row_detail: str,
    substance_is_distractor: bool,
    family: dict[str, Any],
    ctx: dict[str, Any],
    rng: random.Random,
) -> str:
    """Pack claim + distractor under random section names (order-sensitive signal).

    Bag-of-words baselines see both texts on every label; the substance pointer
    plus SCOPE integers / ROW_DETAIL carry the class signal.
    """
    names = ["Mercury", "Neon"]
    if rng.random() < 0.5:
        names = ["Neon", "Mercury"]
    if rng.random() < 0.5:
        mercury_content, neon_content = claim_text, distractor
    else:
        mercury_content, neon_content = distractor, claim_text

    if substance_is_distractor:
        substance = "Mercury" if mercury_content == distractor else "Neon"
    else:
        substance = "Mercury" if mercury_content == claim_text else "Neon"

    opener = _pick(
        rng,
        [
            f"Evidence package for {ctx['org']} ({ctx['env']}), collected {ctx['date']}.",
            f"Working paper — {ctx['org']} / {ctx['system']} / {ctx['date']}.",
            f"Uploaded artifact linked to ticket {ctx['ticket']} for {ctx['org']}.",
        ],
    )
    body = (
        f"{opener} Substance section: {substance}. "
        f"Section Mercury: {mercury_content} "
        f"Section Neon: {neon_content} "
        f"SCOPE: inventory={expected}; file_rows={file_rows}. "
        f"ROW_DETAIL: {row_detail} "
        f"Decoy context (present on all classes): {_universal_decoy_block(family, ctx, rng)}"
    )
    return body


def _mutate(
    label: str,
    family: dict[str, Any],
    ctx: dict[str, Any],
    rng: random.Random,
) -> tuple[str, list[str], str, dict[str, Any]]:
    """Compositional packet packing — denies label-unique cue phrases."""
    control = family["control_statement"]
    base = _sufficient_text(family, ctx).strip()
    meta: dict[str, Any] = {
        "population_expected": ctx.get("pop_expected"),
        "population_observed": ctx.get("pop_observed"),
        "artifact_age_days": 0,
        "source_system": ctx["system"],
        "control_objective": family.get("control_objective", control),
    }
    expected = int(ctx["pop_expected"])
    distractor = family.get(
        "irrelevant_artifact",
        "A neighboring control's configuration export from the same platform",
    )
    # Hedge phrases also appear inside decoys via universal block; claim uses them only when needed.

    if label == "SUFFICIENT":
        meta["population_observed"] = expected
        text = _pack_packet(
            claim_text=base,
            distractor=distractor,
            expected=expected,
            file_rows=expected,
            row_detail=_benign_row_detail(family, ctx, rng),
            substance_is_distractor=False,
            family=family,
            ctx=ctx,
            rng=rng,
        )
        return text, [], _pick(rng, ["easy", "medium"]), meta

    if label == "PARTIAL":
        observed = max(1, int(expected * rng.uniform(0.55, 0.85)))
        meta["population_observed"] = observed
        claim = base.replace(str(expected), str(observed), 1) if str(expected) in base else base
        tags = ["population_gap", "incomplete_export"]
        # Keep PARTIAL signal numeric (file_rows < inventory). Period noise lives in decoys.
        row_detail = _benign_row_detail(family, ctx, rng)
        if rng.random() < 0.15:
            meta["artifact_age_days"] = 400
            tags = tags + ["wrong_period"]
        text = _pack_packet(
            claim_text=claim,
            distractor=distractor,
            expected=expected,
            file_rows=observed,
            row_detail=row_detail,
            substance_is_distractor=False,
            family=family,
            ctx=ctx,
            rng=rng,
        )
        return text, tags, _pick(rng, ["medium", "hard"]), meta

    if label == "INSUFFICIENT":
        claim, tags = _modalize_base(base, family, ctx, rng)
        if rng.random() < 0.1:
            tags = list(tags) + ["stale_evidence"]
            meta["artifact_age_days"] = 500
        if "missing_timestamp" in tags:
            meta["artifact_age_days"] = None
        text = _pack_packet(
            claim_text=claim,
            distractor=distractor,
            expected=expected,
            file_rows=expected,
            row_detail=_benign_row_detail(family, ctx, rng),
            substance_is_distractor=False,
            family=family,
            ctx=ctx,
            rng=rng,
        )
        return text, tags, _pick(rng, ["medium", "hard"]), meta

    if label == "IRRELEVANT":
        text = _pack_packet(
            claim_text=base,
            distractor=distractor,
            expected=expected,
            file_rows=expected,
            row_detail=_benign_row_detail(family, ctx, rng),
            substance_is_distractor=True,
            family=family,
            ctx=ctx,
            rng=rng,
        )
        return text, ["wrong_system", "evidence_not_traceable"], "hard", meta

    contradiction = family["contradiction_template"].format(**ctx).strip()
    meta["population_observed"] = expected
    text = _pack_packet(
        claim_text=base,
        distractor=distractor,
        expected=expected,
        file_rows=expected,
        row_detail=contradiction,
        substance_is_distractor=False,
        family=family,
        ctx=ctx,
        rng=rng,
    )
    tags = list(family.get("contradiction_tags", ["control_failure", "contradictory_configuration"]))
    return text, tags, "hard", meta


def _build_context(
    family: dict[str, Any],
    rng: random.Random,
    *,
    family_id: str,
    variant_id: str,
) -> dict[str, Any]:
    pop = family.get("typical_population", rng.randint(20, 120))
    # Unique report token prevents accidental duplicate evidence strings across instances.
    report_id = f"RPT-{family_id}-{variant_id}-{rng.randint(1000, 9999)}"
    return {
        "org": _pick(rng, ORGS),
        "system": _pick(rng, SYSTEMS),
        "env": family.get("environment", _pick(rng, ENVIRONMENTS)),
        "date": _date(rng, stale=False),
        "stale_date": _date(rng, stale=True),
        "ticket": _ticket(rng),
        "account": _account(rng),
        "pop_expected": pop,
        "pop_observed": pop,
        "unit": family.get("population_unit", "account"),
        "pct": rng.randint(60, 95),
        "count_fail": rng.randint(1, 5),
        "report_id": report_id,
        "family_id": family_id,
    }


def generate_cases(
    families: list[dict[str, Any]],
    *,
    seed: int = CANONICAL_SEED,
    per_class_train: int = 200,
    per_class_val: int = 40,
    per_class_test: int = 40,
    per_class_challenge: int = 20,
) -> list[dict[str, Any]]:
    """Generate a balanced benchmark with family-level split isolation.

    Strategy: create many scenario families; each family produces one variant per
    label (5 variants). Families are assigned wholly to one split. We generate
    enough families so each split×label cell meets targets, then subsample
    deterministically to exact counts.
    """
    # Need enough families: challenge needs 20/class → ≥20 families in challenge, etc.
    # Total cases target 1500 = 300 families × 5 labels if one variant/label/family.
    n_families_needed = 300
    if len(families) < 10:
        raise ValueError("Need at least 10 scenario family templates for domain coverage")

    # Expand templates into concrete family instances
    concrete: list[dict[str, Any]] = []
    for i in range(n_families_needed):
        template = families[i % len(families)]
        family_id = f"{template['id_prefix']}-{i:03d}"
        concrete.append({**template, "scenario_family_id": family_id, "_instance": i})

    family_ids = [c["scenario_family_id"] for c in concrete]
    family_to_split = assign_family_splits(family_ids, seed=seed)

    raw_cases: list[dict[str, Any]] = []
    for fam in concrete:
        split = family_to_split[fam["scenario_family_id"]]
        for label_idx, label in enumerate(LABELS):
            variant_id = chr(ord("A") + label_idx)
            case_rng = _rng(
                seed
                + int(hashlib.sha256(f"{fam['scenario_family_id']}:{variant_id}".encode()).hexdigest()[:8], 16)
            )
            ctx = _build_context(
                fam,
                case_rng,
                family_id=fam["scenario_family_id"],
                variant_id=variant_id,
            )
            text, tags, difficulty, meta = _mutate(label, fam, ctx, case_rng)
            # Anchor uniqueness without becoming a label shortcut keyword.
            text = f"{text.strip()} Reference: {ctx['report_id']}."
            # Light surface noise (synonym swaps) to reduce trivial n-gram memorization.
            text = _surface_noise(text, case_rng)

            case = {
                "id": _hash_id(fam["scenario_family_id"], variant_id),
                "scenario_family_id": fam["scenario_family_id"],
                "variant_id": variant_id,
                "control_domain": fam["control_domain"],
                "control_statement": fam["control_statement"],
                "environment": ctx["env"],
                "evidence_type": fam["evidence_type"],
                "evidence_text": text,
                "label": label,
                "failure_tags": tags,
                "difficulty": difficulty,
                "generation_method": "synthetic_rule_based",
                "review_status": "unreviewed",
                "split": split,
                **{k: v for k, v in meta.items() if v is not None},
            }
            # Validate early
            EvidenceCase.model_validate(case)
            raw_cases.append(case)

    # Subsample to exact per-split per-class targets
    targets = {
        "train": per_class_train,
        "validation": per_class_val,
        "test": per_class_test,
        "challenge": per_class_challenge,
    }
    selected: list[dict[str, Any]] = []
    for split, per_class in targets.items():
        for label in LABELS:
            pool = [
                c
                for c in raw_cases
                if c["split"] == split and c["label"] == label
            ]
            pool.sort(key=lambda c: c["id"])
            if len(pool) < per_class:
                raise RuntimeError(
                    f"Not enough cases for {split}/{label}: have {len(pool)}, need {per_class}"
                )
            selected.extend(pool[:per_class])

    selected.sort(key=lambda c: (c["split"], c["id"]))
    # Re-validate family isolation on selected set
    selected = apply_splits(selected, {c["scenario_family_id"]: c["split"] for c in selected})
    return selected


def write_jsonl(path: Path, cases: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for case in cases:
            f.write(json.dumps(case, ensure_ascii=False) + "\n")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def write_manifest(cases: list[dict[str, Any]], out_dir: Path, manifest_path: Path) -> dict[str, Any]:
    from collections import Counter

    split_files = {
        "train": out_dir / "train.jsonl",
        "validation": out_dir / "validation.jsonl",
        "test": out_dir / "test.jsonl",
        "challenge": out_dir / "challenge.jsonl",
    }
    label_counts = Counter(c["label"] for c in cases)
    split_counts = Counter(c["split"] for c in cases)
    def _rel(path: Path) -> str:
        try:
            return str(path.relative_to(REPO_ROOT)).replace("\\", "/")
        except ValueError:
            return str(path).replace("\\", "/")

    manifest = {
        "dataset_version": "1.1.0",
        "seed": CANONICAL_SEED,
        "total_cases": len(cases),
        "label_counts": dict(label_counts),
        "split_counts": dict(split_counts),
        "files": {
            name: {
                "path": _rel(path),
                "sha256": sha256_file(path) if path.exists() else None,
                "n": split_counts.get(name, 0),
            }
            for name, path in split_files.items()
        },
        "generation_method": "synthetic_rule_based",
        "notes": "Labels are rule-derived. See governance/DATA_CARD.md and review_log.csv.",
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")
    return manifest


def init_review_log(cases: list[dict[str, Any]], path: Path, seed: int = CANONICAL_SEED) -> None:
    """Mark 100% of challenge + ~10% stratified development sample for review."""
    rng = _rng(seed + 7)
    rows: list[dict[str, str]] = []
    for c in cases:
        if c["split"] == "challenge":
            rows.append(
                {
                    "id": c["id"],
                    "split": c["split"],
                    "label": c["label"],
                    "control_domain": c["control_domain"],
                    "review_status": "unreviewed",
                    "priority": "challenge_required",
                }
            )
    dev = [c for c in cases if c["split"] != "challenge"]
    # Stratified ~10%
    by_key: dict[tuple[str, str], list[dict]] = {}
    for c in dev:
        key = (c["label"], c["control_domain"])
        by_key.setdefault(key, []).append(c)
    for key, pool in sorted(by_key.items()):
        pool = sorted(pool, key=lambda x: x["id"])
        k = max(1, int(round(len(pool) * 0.10)))
        sample = pool[:k] if len(pool) <= k else [pool[i] for i in sorted(rng.sample(range(len(pool)), k))]
        for c in sample:
            rows.append(
                {
                    "id": c["id"],
                    "split": c["split"],
                    "label": c["label"],
                    "control_domain": c["control_domain"],
                    "review_status": "unreviewed",
                    "priority": "dev_sample",
                }
            )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "split", "label", "control_domain", "review_status", "priority"],
        )
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda r: r["id"]))


def adversarial_surface_harden(
    cases: list[dict[str, Any]],
    seed: int = CANONICAL_SEED,
    *,
    n_candidates: int = 8,
) -> list[dict[str, Any]]:
    """Resample synonym/decoy surface forms to reduce TF-IDF confidence on the true class.

    Protocol: fit TF-IDF on train surfaces; for every case, try several seeded
    synonym passes and keep the surface with lowest true-class probability.
    Does not change labels or structured SCOPE semantics — only surface noise.
    """
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import Pipeline
    except ImportError:
        return cases

    def _case_text(c: dict[str, Any]) -> str:
        return "\n".join([c["control_statement"], c["evidence_type"], c["evidence_text"]])

    train = [c for c in cases if c["split"] == "train"]
    if len(train) < 50:
        return cases

    pipe = Pipeline(
        [
            ("tfidf", TfidfVectorizer(max_features=20000, ngram_range=(1, 2), min_df=2)),
            ("lr", LogisticRegression(max_iter=2000, class_weight="balanced", C=1.0)),
        ]
    )
    pipe.fit([_case_text(c) for c in train], [c["label"] for c in train])
    classes = list(pipe.named_steps["lr"].classes_)
    hardened: list[dict[str, Any]] = []
    for c in cases:
        best_text = c["evidence_text"]
        proba = pipe.predict_proba([_case_text(c)])[0]
        best_p = float(proba[classes.index(c["label"])])
        for k in range(n_candidates):
            rng = _rng(seed + 991 + k + int(hashlib.sha256(c["id"].encode()).hexdigest()[:6], 16))
            # Synonym noise only — do not permute section names (would break substance pointer).
            cand = _surface_noise(c["evidence_text"], rng, p=0.95)
            proba = pipe.predict_proba(
                ["\n".join([c["control_statement"], c["evidence_type"], cand])]
            )[0]
            p_true = float(proba[classes.index(c["label"])])
            if p_true < best_p:
                best_p = p_true
                best_text = cand
        out = dict(c)
        out["evidence_text"] = best_text
        hardened.append(out)
    return hardened


def generate_dataset(
    scenarios_path: Path = DEFAULT_SCENARIOS,
    out_dir: Path = DEFAULT_OUT,
    manifest_path: Path = DEFAULT_MANIFEST,
    review_path: Path = DEFAULT_REVIEW,
    seed: int = CANONICAL_SEED,
    *,
    adversarial: bool = True,
) -> dict[str, Any]:
    families = load_scenario_families(scenarios_path)
    cases = generate_cases(families, seed=seed)
    if adversarial:
        cases = adversarial_surface_harden(cases, seed=seed)
    by_split: dict[str, list[dict[str, Any]]] = {
        "train": [],
        "validation": [],
        "test": [],
        "challenge": [],
    }
    for c in cases:
        by_split[c["split"]].append(c)
    for name, rows in by_split.items():
        write_jsonl(out_dir / f"{name}.jsonl", rows)
    manifest = write_manifest(cases, out_dir, manifest_path)
    init_review_log(cases, review_path, seed=seed)
    return manifest


def main_cli(argv: Optional[list[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Generate ControlSift synthetic benchmark")
    parser.add_argument("--scenarios", type=Path, default=DEFAULT_SCENARIOS)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--review-log", type=Path, default=DEFAULT_REVIEW)
    parser.add_argument("--seed", type=int, default=CANONICAL_SEED)
    args = parser.parse_args(argv)
    manifest = generate_dataset(
        scenarios_path=args.scenarios,
        out_dir=args.out,
        manifest_path=args.manifest,
        review_path=args.review_log,
        seed=args.seed,
    )
    print(json.dumps({"ok": True, "total_cases": manifest["total_cases"]}, indent=2))


if __name__ == "__main__":
    main_cli()
