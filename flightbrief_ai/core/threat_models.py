from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class DocumentPage:
    page_number: int
    text: str


@dataclass
class DocumentSection:
    name: str
    pages: List[int] = field(default_factory=list)
    text: str = ""


@dataclass
class Threat:
    threat_title: str
    priority: str
    category: str
    source_section: str
    page_number: int
    highlight_text: str
    why_it_matters: str
    expected_crew_action: str
    affected_phase: str
    affected_area: str
    confidence: str = "Medium"
