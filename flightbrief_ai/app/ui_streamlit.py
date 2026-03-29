from __future__ import annotations

import tempfile
from pathlib import Path

import streamlit as st

from core.engine import FlightBriefEngine
from core.pdf_annotator import PDFAnnotator
from core.summary_pdf import ThreatSummaryPDF


def run_app() -> None:
    st.set_page_config(page_title="FlightBrief AI", layout="wide")

    st.title("FlightBrief AI")
    st.write(
        "Carrega um plano de voo em PDF e obtém dois PDFs: o briefing anotado e o threat summary."
    )

    uploaded_file = st.file_uploader(
        "Plano de voo PDF",
        type=["pdf"],
        help="Carrega um único briefing pack em PDF.",
    )

    if uploaded_file is None:
        st.info("Faz upload de um PDF para iniciar a análise.")
        return

    st.success(f"Ficheiro recebido: {uploaded_file.name}")

    if not st.button("Analyze", type="primary"):
        return

    engine = FlightBriefEngine()
    annotator = PDFAnnotator()
    summary_builder = ThreatSummaryPDF()

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        input_path = tmpdir_path / uploaded_file.name
        input_path.write_bytes(uploaded_file.getvalue())

        threats = engine.analyze(input_path)

        highlighted_path = tmpdir_path / f"highlighted_{uploaded_file.name}"
        summary_path = tmpdir_path / f"threat_summary_{input_path.stem}.pdf"

        annotator.annotate(input_path, threats, highlighted_path)
        summary_builder.build(
            summary_path,
            title="FlightBrief AI — Threat Summary",
            metadata={
                "Source file": uploaded_file.name,
                "Threat count": str(len(threats)),
                "P1": str(sum(1 for t in threats if t.priority == "P1")),
                "P2": str(sum(1 for t in threats if t.priority == "P2")),
                "P3": str(sum(1 for t in threats if t.priority == "P3")),
            },
            threats=threats,
        )

        st.subheader("Threats found")
        if not threats:
            st.info("Nenhuma ameaça foi identificada pelas regras atuais.")
        else:
            for threat in threats:
                st.markdown(
                    f"**{threat.priority} — {threat.threat_title}**  \n"
                    f"Categoria: {threat.category} | Secção: {threat.source_section} | Página: {threat.page_number}  \n"
                    f"Porque importa: {threat.why_it_matters}  \n"
                    f"Crew action: {threat.expected_crew_action}"
                )

        st.download_button(
            label="Download highlighted PDF",
            data=highlighted_path.read_bytes(),
            file_name=highlighted_path.name,
            mime="application/pdf",
        )
        st.download_button(
            label="Download threat summary PDF",
            data=summary_path.read_bytes(),
            file_name=summary_path.name,
            mime="application/pdf",
        )


if __name__ == "__main__":
    run_app()
