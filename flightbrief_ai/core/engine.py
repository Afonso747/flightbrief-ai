from __future__ import annotations

from pathlib import Path
from typing import List

from .parser import PDFParser
from .sections import detect_sections
from .threat_models import Threat
from rules.base_rules import (
    detect_callsign_letter,
    detect_mel,
    detect_notam_patterns,
    detect_weather_patterns,
)


class FlightBriefEngine:
    def __init__(self) -> None:
        self.parser = PDFParser()

    def analyze(self, pdf_path: str | Path) -> List[Threat]:
        pages = self.parser.parse(pdf_path)
        sections = detect_sections(pages)

        threats: List[Threat] = []
        for section in sections:
            if section.name == "Operational Flight Plan":
                threats.extend(detect_mel(section))
            if section.name == "ATC Flight Plan":
                threats.extend(detect_callsign_letter(section))
            if section.name in {"Airport Weather List", "ETOPS Summary"}:
                threats.extend(detect_weather_patterns(section))
            if section.name == "NOTAM Information":
                threats.extend(detect_notam_patterns(section))

        # de-duplicate on title + page + text
        unique: dict[tuple[str, int, str], Threat] = {}
        for threat in threats:
            key = (threat.threat_title, threat.page_number, threat.highlight_text)
            unique[key] = threat

        return sorted(unique.values(), key=lambda t: (t.priority, t.page_number, t.threat_title))
