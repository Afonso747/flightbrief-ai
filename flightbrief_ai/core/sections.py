from __future__ import annotations

from typing import Dict, List

from .threat_models import DocumentPage, DocumentSection

SECTION_KEYWORDS: Dict[str, List[str]] = {
    "Operational Flight Plan": ["OFP", "FLIGHT PLAN ROUTE", "REMARKS:", "MEL/CDL DESCRIPTION"],
    "ETOPS Summary": ["ETOPS SUMMARY", "ENRTE ALTNS", "WEATHER SUITABILITY PERIOD"],
    "Airport Weather List": ["LIDO/WEATHER SERVICE", "Destination:", "Alternate", "SIGMETs:"],
    "NOTAM Information": ["NOTAM", "AERODROME", "RUNWAY", "PROCEDURE CANCELED"],
    "ATC Flight Plan": ["(FPL-", "RALT/", "DOF/", "RMK/"],
    "Dispatch Information": ["Dispatch", "INCAD", "DISPATCH INFORMATION"],
}


def detect_sections(pages: List[DocumentPage]) -> List[DocumentSection]:
    sections: Dict[str, DocumentSection] = {
        name: DocumentSection(name=name) for name in SECTION_KEYWORDS
    }

    for page in pages:
        upper = page.text.upper()
        for name, keywords in SECTION_KEYWORDS.items():
            if any(keyword.upper() in upper for keyword in keywords):
                sections[name].pages.append(page.page_number)
                sections[name].text += f"\n\n--- PAGE {page.page_number} ---\n{page.text}"

    return [section for section in sections.values() if section.pages]
