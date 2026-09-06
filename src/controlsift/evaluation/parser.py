"""Robust parser for model JSON / JSON-like classification outputs (§26)."""

from __future__ import annotations

import json
import re
from typing import Any, Optional

from controlsift import LABELS, UNPARSEABLE

_LABEL_SET = set(LABELS)
_LABEL_RE = re.compile(
    r"\b(SUFFICIENT|PARTIAL|INSUFFICIENT|IRRELEVANT|CONTRADICTORY)\b",
    re.IGNORECASE,
)
_JSON_BLOCK_RE = re.compile(r"\{[^{}]*\}", re.DOTALL)


def _normalize_label(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip().upper().replace(" ", "_")
    if text in _LABEL_SET:
        return text
    return None


def parse_model_output(text: str) -> dict[str, Any]:
    """Parse model output into label + rationale.

    Never silently converts ambiguous output into a correct-looking label.
    Unknown / malformed → UNPARSEABLE.
    """
    if text is None:
        return {"label": UNPARSEABLE, "rationale": "", "raw": "", "parse_status": "empty"}

    raw = str(text).strip()
    if not raw:
        return {"label": UNPARSEABLE, "rationale": "", "raw": raw, "parse_status": "empty"}

    lowered = raw.lower()
    if any(x in lowered for x in ("i can't", "i cannot", "as an ai", "refuse")):
        # Still try to extract a label if present; else unparseable.
        pass

    # 1) Direct JSON
    try:
        obj = json.loads(raw)
        if isinstance(obj, dict):
            label = _normalize_label(obj.get("label"))
            rationale = str(obj.get("rationale", "")).strip()
            if label:
                return {
                    "label": label,
                    "rationale": rationale,
                    "raw": raw,
                    "parse_status": "json",
                }
    except json.JSONDecodeError:
        pass

    # 2) First JSON-like object in prose
    for match in _JSON_BLOCK_RE.finditer(raw):
        snippet = match.group(0)
        try:
            # Tolerate single quotes lightly
            candidate = snippet.replace("'", '"')
            obj = json.loads(candidate)
            if isinstance(obj, dict):
                label = _normalize_label(obj.get("label"))
                rationale = str(obj.get("rationale", "")).strip()
                if label:
                    return {
                        "label": label,
                        "rationale": rationale,
                        "raw": raw,
                        "parse_status": "json_embedded",
                    }
        except json.JSONDecodeError:
            continue

    # 3) Bare label only if unambiguous single match
    matches = _LABEL_RE.findall(raw)
    uniq = {_normalize_label(m) for m in matches}
    uniq.discard(None)
    if len(uniq) == 1:
        label = next(iter(uniq))
        return {
            "label": label,
            "rationale": raw[:500],
            "raw": raw,
            "parse_status": "label_regex",
        }

    return {
        "label": UNPARSEABLE,
        "rationale": raw[:500],
        "raw": raw,
        "parse_status": "unparseable",
    }
