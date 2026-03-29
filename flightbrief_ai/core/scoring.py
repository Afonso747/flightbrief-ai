from __future__ import annotations


def decide_priority(
    category: str,
    severity_score: int,
    operational_impact_score: int,
    briefing_required: bool,
    callsign_has_letter: bool = False,
) -> str:
    if callsign_has_letter and category == "CALLSIGN":
        return "P3"

    total = severity_score + operational_impact_score
    if total >= 8:
        return "P1"
    if total >= 5 or briefing_required:
        return "P2"
    return "P3"
