from fpdf import FPDF
from pathlib import Path

def gerar_relatorio_validacao(usuario, resultados_dict: dict, erros: list, aprovado: bool, nome_pdf: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="FAD - Relatório de Validação de Geometria", ln=True, align="C")
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Usuário: {usuario.usuario_id}", ln=True)
    pdf.cell(200, 10, txt=f"Projeto: {usuario.projeto_id}", ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", size=11, style='B')
    pdf.cell(200, 10, txt="Critérios Avaliados:", ln=True)
    pdf.set_font("Arial", size=11)

    for key, resultado in resultados_dict.items():
        status = "✔️" if resultado else "❌"
        pdf.cell(200, 8, txt=f"{key}: {status}", ln=True)

    pdf.ln(10)

    if not aprovado:
        pdf.set_text_color(220, 50, 50)
        pdf.multi_cell(0, 10, txt="Motivo(s) da reprovação:")
        for erro in erros:
            pdf.multi_cell(0, 8, txt=f"- {erro}")
    else:
        pdf.set_text_color(0, 128, 0)
        pdf.cell(200, 10, txt="GEOMETRIA VALIDADA COM SUCESSO", ln=True)

    pdf.set_text_color(0, 0, 0)

    relatorio_path = Path(__file__).resolve().parent.parent / "static" / "relatorios"
    relatorio_path.mkdir(parents=True, exist_ok=True)
    pdf.output(str(relatorio_path / nome_pdf))
