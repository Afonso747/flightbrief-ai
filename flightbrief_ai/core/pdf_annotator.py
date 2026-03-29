from __future__ import annotations

from pathlib import Path
from typing import Iterable

import fitz

from .threat_models import Threat


class PDFAnnotator:
    def annotate(self, source_pdf: str | Path, threats: Iterable[Threat], output_pdf: str | Path) -> None:
        doc = fitz.open(str(source_pdf))
        for threat in threats:
            page_index = max(0, threat.page_number - 1)
            if page_index >= len(doc):
                continue
            page = doc[page_index]
            snippets = [threat.highlight_text]
            if len(threat.highlight_text) > 80:
                snippets.append(threat.highlight_text[:80])
            for snippet in snippets:
                rects = page.search_for(snippet)
                if rects:
                    annot = page.add_highlight_annot(rects)
                    annot.set_info(content=f"{threat.priority} | {threat.threat_title}: {threat.why_it_matters}")
                    annot.update()
                    break
        doc.save(str(output_pdf))
        doc.close()
