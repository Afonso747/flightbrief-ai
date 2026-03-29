from __future__ import annotations

import re
from typing import List

from core.threat_models import DocumentSection, Threat
from core.scoring import decide_priority


def _first_match(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
    if match:
        return match.group(0).strip()
    return None


def detect_mel(section: DocumentSection) -> List[Threat]:
    threats: List[Threat] = []
    if "MEL/CDL DESCRIPTION" in section.text.upper():
        mel_line = _first_match(r"MEL/CDL DESCRIPTION\s*\n?([A-Z0-9\- ]+)", section.text)
        addt_fuel = "ADDT FUEL DUE TO MEL" in section.text.upper()
        if mel_line or addt_fuel:
            title = "MEL item with operational impact"
            highlight = mel_line or "ADDT FUEL DUE TO MEL"
            threats.append(
                Threat(
                    threat_title=title,
                    priority=decide_priority("MEL_CDL", 3, 3, True),
                    category="MEL_CDL",
                    source_section=section.name,
                    page_number=section.pages[0],
                    highlight_text=highlight,
                    why_it_matters="Há um item MEL/CDL ativo no OFP e isso merece consciência operacional no briefing.",
                    expected_crew_action="Rever limitações e implicações operacionais do item MEL/CDL.",
                    affected_phase="General",
                    affected_area="General",
                    confidence="High",
                )
            )
    return threats


def detect_callsign_letter(section: DocumentSection) -> List[Threat]:
    threats: List[Threat] = []
    fpl = _first_match(r"\(FPL-([A-Z]{3}\d+[A-Z])", section.text)
    if fpl:
        callsign = fpl.split("-")[-1]
        threats.append(
            Threat(
                threat_title="Callsign with appended letter",
                priority="P3",
                category="CALLSIGN",
                source_section=section.name,
                page_number=section.pages[0],
                highlight_text=callsign,
                why_it_matters="Callsign com letra appended exige atenção adicional em comunicações.",
                expected_crew_action="Reforçar listening e readback discipline.",
                affected_phase="General",
                affected_area="General",
                confidence="High",
            )
        )
    return threats


def detect_etops_weather(section: DocumentSection) -> List[Threat]:
    threats: List[Threat] = []
    if "WEATHER SUITABILITY PERIOD" not in section.text.upper():
        return threats
    for apt in ["DGAA", "DAAT", "LPLA", "CYHZ", "LPPD", "LPAZ"]:
        if apt in section.text:
            continue
    return threats


def detect_weather_patterns(section: DocumentSection) -> List[Threat]:
    threats: List[Threat] = []
    weather_patterns = [
        (r"WINDSHEAR", "Possible windshear", "MET", 3, 3),
        (r"TSRA|\bTS\b|VCTS", "Thunderstorm or convective activity", "MET", 3, 3),
        (r"CB", "Convective cloud / CB activity", "MET", 2, 3),
        (r"GNSS SEV|SWX EFFECT: GNSS SEV", "Space weather / GNSS severe advisory", "NAV", 3, 3),
        (r"PROB30.*TS|PROB40.*TS", "Thunderstorm risk in forecast", "ALT_ETOPS", 2, 3),
        (r"G\d{2}KT", "Gusty wind conditions", "MET", 2, 3),
    ]

    upper_text = section.text.upper()
    for pattern, title, category, sev, op in weather_patterns:
        match = _first_match(pattern, upper_text)
        if match:
            threats.append(
                Threat(
                    threat_title=title,
                    priority=decide_priority(category, sev, op, True),
                    category=category,
                    source_section=section.name,
                    page_number=section.pages[0],
                    highlight_text=match,
                    why_it_matters="Condição meteorológica ou de navegação que pode aumentar complexidade, workload ou necessidade de mitigação.",
                    expected_crew_action="Briefar mitigação e manter monitorização operacional adequada.",
                    affected_phase="Departure" if "Destination:" not in section.text else "General",
                    affected_area="General",
                    confidence="Medium",
                )
            )
    return threats


def detect_notam_patterns(section: DocumentSection) -> List[Threat]:
    threats: List[Threat] = []
    patterns = [
        (r"RUNWAY\s+\d+[A-Z]?\s+VOR/DME PROCEDURE CANCELED", "Departure/arrival procedure canceled"),
        (r"RFF\s+DOWNGRADED|CATEGORY\s+DOWNGRADED", "RFF downgraded"),
        (r"RUNWAY CLOSED|RWY CLOSED", "Runway closure"),
    ]
    for pattern, title in patterns:
        match = _first_match(pattern, section.text)
        if match:
            threats.append(
                Threat(
                    threat_title=title,
                    priority=decide_priority("NOTAM_ADX", 2, 3, True),
                    category="NOTAM_ADX",
                    source_section=section.name,
                    page_number=section.pages[0],
                    highlight_text=match,
                    why_it_matters="NOTAM com impacto operacional relevante para briefing.",
                    expected_crew_action="Confirmar implicação prática no procedimento ou estratégia operacional.",
                    affected_phase="General",
                    affected_area="General",
                    confidence="Medium",
                )
            )
    return threats
