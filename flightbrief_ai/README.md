# FlightBrief AI — deploy-ready prototype

Protótipo funcional para:
- receber um briefing pack em PDF
- identificar ameaças operacionais com regras iniciais
- gerar o mesmo PDF com highlights
- gerar um segundo PDF com o threat summary

## Stack
- Python 3.11
- Streamlit
- PyMuPDF
- ReportLab

## Ficheiro principal
- `streamlit_app.py`

## Run local
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy no Streamlit Community Cloud
1. Cria um repositório no GitHub e envia esta pasta inteira.
2. No Streamlit Community Cloud, escolhe **Create app**.
3. Seleciona o repositório, a branch e o ficheiro principal `streamlit_app.py`.
4. Faz deploy.

## Ficheiros de deploy incluídos
- `.streamlit/config.toml` — aumenta o limite de upload e define configuração básica
- `requirements.txt` — dependências Python
- `runtime.txt` — versão do Python
- `.gitignore` — limpeza do repositório

## Estrutura
- `streamlit_app.py` — entrypoint de deploy
- `app/ui_streamlit.py` — interface Streamlit
- `core/parser.py` — leitura do PDF e extração de texto por página
- `core/sections.py` — deteção simples de secções do briefing
- `core/threat_models.py` — modelos de dados
- `core/engine.py` — motor principal de análise
- `core/scoring.py` — heurística P1/P2/P3
- `core/pdf_annotator.py` — highlights no PDF
- `core/summary_pdf.py` — geração do threat summary em PDF
- `rules/base_rules.py` — regras iniciais de deteção

## Estado atual
Esta v1 é um MVP rule-based. O foco é ter o pipeline completo a funcionar.
A versão inteligente ficará para a calibragem com mais exemplos anotados.
