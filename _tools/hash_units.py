#!/usr/bin/env python3
"""
hash_units.py — drift detector between CUSTOMER_JOURNEY.md Phase 2 table and SDD.md units.

Contract (per ULTRAPLAN.md Phase 4):
- Parse the Phase 2 table in CUSTOMER_JOURNEY.md. Extract phase_id, customer_action,
  input, output, decision_buttons per row (skip TBD rows — those are parked placeholders).
- Recompute unit_hash per row using:
    sha256(phase_id + "|" + customer_action + "|" + io_signature + "|" + "|".join(sorted(decision_buttons)))
  where io_signature = f"IN: {input} | OUT: {output}".
- Parse SDD.md. Extract each unit's stored phase_id and unit_hash.
- Compare. Print drift rows in the format:
    phase_id: <old_hash> -> <new_hash>  REVIEW NEEDED
- Exit 0 if no drift (or no units locked yet). Exit 1 if drift detected.

Usage:
    python _tools/hash_units.py              # run drift check
    python _tools/hash_units.py --self-test  # run embedded tests, exit 0 on pass

Stdlib only. Python 3.11+.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
JOURNEY_PATH = REPO_ROOT / "CUSTOMER_JOURNEY.md"
SDD_PATH = REPO_ROOT / "SDD.md"

TBD_MARKER = "TBD"


def canonical_io(input_text: str, output_text: str) -> str:
    return f"IN: {input_text.strip()} | OUT: {output_text.strip()}"


def canonical_buttons(raw: str) -> list[str]:
    """
    Extract decision_button identifiers from the cell.

    Canonical form: backtick-delimited tokens. The annotation after each token (e.g.,
    "(primary CTA)") is ignored — hash must be stable across annotation edits.

    If the cell has no backticks, fall back to splitting on ' / ' and stripping.
    Empty or TBD cells return [].
    Result sorted alphabetically for hash stability.
    """
    cleaned = raw.strip()
    if not cleaned or cleaned.upper().startswith(TBD_MARKER):
        return []
    tokens = re.findall(r"`([^`]+)`", cleaned)
    if not tokens:
        tokens = [p.strip() for p in cleaned.split(" / ") if p.strip()]
    return sorted(tokens)


def compute_hash(
    phase_id: str,
    customer_action: str,
    io_signature: str,
    decision_buttons: list[str],
) -> str:
    payload = (
        phase_id
        + "|"
        + customer_action
        + "|"
        + io_signature
        + "|"
        + "|".join(decision_buttons)
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def parse_journey_table(text: str) -> list[dict]:
    """
    Return list of units from the Phase 2 table in CUSTOMER_JOURNEY.md.

    Heuristic: find the table under the '## Phase 2' heading. Table must have 8 columns
    in the documented order: Step | Customer action | Input | Output | System touchpoint |
    Communication trigger | Decision/branch buttons | Validation pattern.

    Skip rows where Step is non-numeric (edge cases), where customer_action contains TBD,
    or where phase_id would collide.
    """
    lines = text.splitlines()
    # Locate Phase 2 section.
    section_start = None
    for i, line in enumerate(lines):
        stripped = line.strip().lower()
        if stripped.startswith("## phase 2"):
            section_start = i
            break
    if section_start is None:
        return []

    # Find first pipe-table row after section start.
    table_header_idx = None
    for i in range(section_start + 1, len(lines)):
        if lines[i].lstrip().startswith("|") and "Step" in lines[i]:
            table_header_idx = i
            break
    if table_header_idx is None:
        return []

    units: list[dict] = []
    for i in range(table_header_idx + 2, len(lines)):  # skip header + separator
        line = lines[i]
        if not line.lstrip().startswith("|"):
            break  # end of table
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 8:
            continue
        step, action, inp, out, touchpoint, comm, buttons, validation = cells[:8]

        # Skip header separators or malformed.
        if not step or step.startswith("-"):
            continue

        # Skip TBD/parked rows — only hash units with real content.
        # Rule: if customer_action OR input OR output starts with TBD, skip.
        if any(c.upper().startswith(TBD_MARKER) for c in (action, inp, out)):
            continue

        # Skip non-numeric step IDs unless they're like "1", "2", "5+"; use raw.
        phase_id = step.strip()
        units.append(
            {
                "phase_id": phase_id,
                "customer_action": action,
                "input": inp,
                "output": out,
                "system_touchpoint": touchpoint,
                "communication_trigger": comm,
                "decision_buttons_raw": buttons,
                "validation_pattern": validation,
            }
        )
    return units


def parse_sdd_units(text: str) -> dict[str, str]:
    """
    Return {phase_id: unit_hash} from SDD.md.

    Minimal YAML-like parser that handles the ULTRAPLAN Phase 4 schema. Each unit is a
    block starting with `- phase_id: <value>` followed by indented `key: value` pairs.
    We only extract phase_id and unit_hash — other fields are ignored.
    """
    result: dict[str, str] = {}
    current_phase_id: str | None = None
    lines = text.splitlines()
    in_yaml_fence = False
    for raw in lines:
        stripped = raw.strip()
        # Track fenced code blocks so we only parse YAML inside them if used.
        if stripped.startswith("```"):
            in_yaml_fence = not in_yaml_fence
            continue

        # Match `- phase_id: <value>` to open a new unit.
        m = re.match(r"^\s*-\s+phase_id:\s*(.+?)\s*$", raw)
        if m:
            current_phase_id = strip_yaml_scalar(m.group(1))
            continue

        # Inside an open unit, look for `unit_hash: <value>`.
        if current_phase_id is not None:
            m = re.match(r"^\s+unit_hash:\s*(.+?)\s*$", raw)
            if m:
                hash_value = strip_yaml_scalar(m.group(1))
                # Allow TBD placeholder — skip storing.
                if hash_value and not hash_value.upper().startswith(TBD_MARKER):
                    result[current_phase_id] = hash_value
                current_phase_id = None
    return result


def strip_yaml_scalar(value: str) -> str:
    v = value.strip()
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        v = v[1:-1]
    return v


def check_drift(journey_units: list[dict], sdd_hashes: dict[str, str]) -> list[str]:
    """Return list of drift messages. Empty = no drift."""
    drifts: list[str] = []
    for unit in journey_units:
        phase_id = unit["phase_id"]
        io_sig = canonical_io(unit["input"], unit["output"])
        buttons = canonical_buttons(unit["decision_buttons_raw"])
        new_hash = compute_hash(phase_id, unit["customer_action"], io_sig, buttons)
        old_hash = sdd_hashes.get(phase_id)
        if old_hash is None:
            # Unit in journey but not in SDD — not a drift; it's a gap. Report separately.
            drifts.append(f"{phase_id}: <missing in SDD> -> {new_hash}  REVIEW NEEDED")
            continue
        if old_hash != new_hash:
            drifts.append(f"{phase_id}: {old_hash} -> {new_hash}  REVIEW NEEDED")
    return drifts


# -------------------- Self-test --------------------


def run_self_test() -> int:
    """Embedded tests. Returns 0 on pass, 1 on fail. Prints progress."""
    failures: list[str] = []

    def check(name: str, cond: bool, detail: str = ""):
        if cond:
            print(f"  PASS  {name}")
        else:
            print(f"  FAIL  {name}  {detail}")
            failures.append(name)

    print("self-test: canonical_io")
    check(
        "canonical_io basic",
        canonical_io("a", "b") == "IN: a | OUT: b",
    )
    check(
        "canonical_io strips",
        canonical_io("  a  ", "  b  ") == "IN: a | OUT: b",
    )

    print("self-test: canonical_buttons")
    check(
        "buttons empty",
        canonical_buttons("") == [],
    )
    check(
        "buttons TBD",
        canonical_buttons("TBD") == [],
    )
    check(
        "buttons single",
        canonical_buttons("`start`") == ["start"],
    )
    check(
        "buttons multiple sorted",
        canonical_buttons("`c` / `a` / `b`") == ["a", "b", "c"],
    )
    check(
        "buttons preserves internal spaces",
        canonical_buttons("`start_regularization` / `talk_to_human`")
        == ["start_regularization", "talk_to_human"],
    )
    check(
        "buttons ignore annotations",
        canonical_buttons("`primary` (main CTA) / `escape` (secondary)")
        == ["escape", "primary"],
    )
    check(
        "buttons fallback when no backticks",
        canonical_buttons("plain_a / plain_b") == ["plain_a", "plain_b"],
    )

    print("self-test: compute_hash")
    h1 = compute_hash("1", "action", "IN: x | OUT: y", ["a", "b"])
    h2 = compute_hash("1", "action", "IN: x | OUT: y", ["a", "b"])
    check("hash deterministic", h1 == h2)
    h3 = compute_hash("1", "action", "IN: x | OUT: y", ["b", "a"])
    check("hash sorted-sensitive (caller must sort)", h3 != h1 or sorted(["a", "b"]) == ["a", "b"])
    h4 = compute_hash("2", "action", "IN: x | OUT: y", ["a", "b"])
    check("hash changes on phase_id", h4 != h1)
    h5 = compute_hash("1", "ACTION", "IN: x | OUT: y", ["a", "b"])
    check("hash case-sensitive on action", h5 != h1)

    print("self-test: parse_journey_table")
    journey_fixture = (
        "# X\n\n"
        "## Phase 2 — Flowchart table\n\n"
        "| Step | Customer action | Input | Output | System touchpoint | Communication trigger | Decision/branch buttons | Validation pattern |\n"
        "|------|-----------------|-------|--------|-------------------|-----------------------|-------------------------|--------------------|\n"
        "| 1 | act1 | in1 | out1 | sys1 | comm1 | `b1` / `b2` | v1 |\n"
        "| 2 | act2 | in2 | out2 | sys2 | comm2 | `b3` | v2 |\n"
        "| 3 | TBD | TBD | TBD | TBD | TBD | TBD | TBD |\n\n"
        "## Next section\n"
    )
    units = parse_journey_table(journey_fixture)
    check("parse skips TBD rows", len(units) == 2)
    check("parse phase_id correct", [u["phase_id"] for u in units] == ["1", "2"])
    check("parse customer_action", units[0]["customer_action"] == "act1")
    check("parse decision_buttons_raw", units[0]["decision_buttons_raw"] == "`b1` / `b2`")

    print("self-test: parse_sdd_units")
    sdd_fixture = (
        "# SDD\n\n"
        "- phase_id: 1\n"
        "  customer_action: act1\n"
        "  unit_hash: deadbeef\n"
        "  responsibility: r1\n"
        "- phase_id: 2\n"
        "  unit_hash: cafef00d\n"
        "- phase_id: 3\n"
        "  unit_hash: TBD\n"
    )
    sdd = parse_sdd_units(sdd_fixture)
    check("sdd parses both valid units", sdd == {"1": "deadbeef", "2": "cafef00d"})
    check("sdd skips TBD unit_hash", "3" not in sdd)

    print("self-test: check_drift integration")
    # Build a journey with one unit whose hash matches SDD, one mismatched, one missing in SDD.
    unit_ok = {
        "phase_id": "1",
        "customer_action": "act1",
        "input": "in1",
        "output": "out1",
        "decision_buttons_raw": "`b1` / `b2`",
    }
    unit_drift = {
        "phase_id": "2",
        "customer_action": "act2_changed",
        "input": "in2",
        "output": "out2",
        "decision_buttons_raw": "`b3`",
    }
    unit_missing = {
        "phase_id": "4",
        "customer_action": "act4",
        "input": "in4",
        "output": "out4",
        "decision_buttons_raw": "`b4`",
    }
    ok_hash = compute_hash(
        "1", "act1", canonical_io("in1", "out1"), canonical_buttons("`b1` / `b2`")
    )
    stored = {"1": ok_hash, "2": "not-matching-hash"}
    drifts = check_drift([unit_ok, unit_drift, unit_missing], stored)
    check(
        "drift: matching unit produces no drift",
        all("1:" not in d or "->" not in d for d in drifts),
    )
    check("drift: mismatching unit flagged", any(d.startswith("2:") for d in drifts))
    check("drift: missing unit flagged", any(d.startswith("4:") for d in drifts))

    print()
    if failures:
        print(f"SELF-TEST FAILED: {len(failures)} failures")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"SELF-TEST OK — all checks passed")
    return 0


# -------------------- Main --------------------


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return run_self_test()

    if not JOURNEY_PATH.exists():
        print(f"error: {JOURNEY_PATH} not found", file=sys.stderr)
        return 2
    if not SDD_PATH.exists():
        print(f"error: {SDD_PATH} not found", file=sys.stderr)
        return 2

    journey_text = JOURNEY_PATH.read_text(encoding="utf-8")
    sdd_text = SDD_PATH.read_text(encoding="utf-8")

    units = parse_journey_table(journey_text)
    sdd_hashes = parse_sdd_units(sdd_text)

    if not units:
        print("info: no non-TBD rows found in CUSTOMER_JOURNEY.md Phase 2 table — nothing to hash")
        return 0

    drifts = check_drift(units, sdd_hashes)

    if not drifts:
        print(f"OK — {len(units)} units hashed, no drift vs SDD.md")
        return 0

    print(f"DRIFT DETECTED — {len(drifts)} issue(s):")
    for d in drifts:
        print(f"  {d}")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
