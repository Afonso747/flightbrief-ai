from __future__ import annotations

from pathlib import Path
from typing import Iterable

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from .threat_models import Threat


class ThreatSummaryPDF:
    def build(
        self,
        output_pdf: str | Path,
        title: str,
        metadata: dict[str, str],
        threats: Iterable[Threat],
    ) -> None:
        c = canvas.Canvas(str(output_pdf), pagesize=A4)
        width, height = A4
        y = height - 20 * mm

        def new_page() -> float:
            c.showPage()
            return height - 20 * mm

        c.setFont("Helvetica-Bold", 16)
        c.drawString(20 * mm, y, title)
        y_local = y - 10 * mm

        c.setFont("Helvetica", 10)
        for key, value in metadata.items():
            c.drawString(20 * mm, y_local, f"{key}: {value}")
            y_local -= 5 * mm

        grouped = {"P1": [], "P2": [], "P3": []}
        for threat in threats:
            grouped.setdefault(threat.priority, []).append(threat)

        y_local -= 5 * mm
        for priority in ["P1", "P2", "P3"]:
            if y_local < 40 * mm:
                y_local = new_page()
            c.setFont("Helvetica-Bold", 13)
            c.drawString(20 * mm, y_local, f"Priority {priority[-1]}")
            y_local -= 7 * mm
            entries = grouped.get(priority, [])
            if not entries:
                c.setFont("Helvetica", 10)
                c.drawString(25 * mm, y_local, "Nil")
                y_local -= 6 * mm
                continue

            for idx, threat in enumerate(entries, start=1):
                if y_local < 45 * mm:
                    y_local = new_page()
                c.setFont("Helvetica-Bold", 11)
                c.drawString(25 * mm, y_local, f"{idx}. {threat.threat_title}")
                y_local -= 5 * mm

                c.setFont("Helvetica", 10)
                lines = [
                    f"Category: {threat.category}",
                    f"Source: {threat.source_section} | Page: {threat.page_number}",
                    f"Why it matters: {threat.why_it_matters}",
                    f"Crew action: {threat.expected_crew_action}",
                    f"Highlight: {threat.highlight_text}",
                ]
                for line in lines:
                    wrapped = self._wrap(line, 95)
                    for part in wrapped:
                        if y_local < 25 * mm:
                            y_local = new_page()
                        c.drawString(30 * mm, y_local, part)
                        y_local -= 4.5 * mm
                y_local -= 2 * mm

        c.save()

    @staticmethod
    def _wrap(text: str, width: int) -> list[str]:
        words = text.split()
        lines: list[str] = []
        current = ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if len(candidate) <= width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines
