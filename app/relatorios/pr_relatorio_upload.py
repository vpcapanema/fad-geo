from fpdf import FPDF
import os
from datetime import datetime

def gerar_relatorio_upload(nome_projeto: str, id_projeto: int, id_arquivo, resultados: dict, erros: list, nome_arquivo: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)

    pdf.set_text_color(0, 0, 128)
    pdf.cell(0, 10, "FAD - Ferramenta de Análise Dinamizada", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "Módulo: Validação do Upload de Geometria", ln=True, align="C")
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Nome do Projeto: {nome_projeto}", ln=True)
    pdf.cell(0, 8, f"ID do Projeto: {id_projeto}", ln=True)
    pdf.cell(0, 8, f"ID do Arquivo: {id_arquivo}", ln=True)
    pdf.ln(8)

    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(130, 8, "Critério Avaliado", border=1, fill=True)
    pdf.cell(30, 8, "Status", border=1, ln=True)

    def linha(titulo, ok):
        simbolo = "✔️" if ok else "❌"
        cor = (0, 153, 0) if ok else (200, 0, 0)
        pdf.set_text_color(*cor)
        pdf.set_font("Arial", "", 11)
        pdf.cell(130, 8, titulo, border=1)
        pdf.cell(30, 8, simbolo, border=1, ln=True)

    for chave in ["A3.shp", "A3.shx", "A3.dbf", "A3.prj"]:
        linha(f"Arquivo {chave} presente", resultados.get(chave, False))

    pdf.ln(5)
    pdf.set_text_color(200, 0, 0)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "ARQUIVO REPROVADO", ln=True, align="C")
    pdf.set_font("Arial", "", 11)
    pdf.ln(5)
    for e in erros:
        pdf.cell(0, 8, f"- {e}", ln=True)

    pdf.set_text_color(100, 100, 100)
    pdf.set_y(-20)
    datahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 10, f"Relatório gerado em {datahora}", align="C")

    caminho = f"app/static/relatorios/{nome_arquivo}"
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    pdf.output(caminho, "F")
