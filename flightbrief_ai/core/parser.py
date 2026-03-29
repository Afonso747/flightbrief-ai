from __future__ import annotations

from pathlib import Path
from typing import List

import fitz

from .threat_models import DocumentPage


class PDFParser:
    def parse(self, pdf_path: str | Path) -> List[DocumentPage]:
        doc = fitz.open(str(pdf_path))
        pages: List[DocumentPage] = []
        for idx, page in enumerate(doc):
            text = page.get_text("text") or ""
            pages.append(DocumentPage(page_number=idx + 1, text=text))
        doc.close()
        return pages
