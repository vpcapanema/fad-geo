
from fpdf import FPDF
from datetime import datetime

class PDFRelatorio(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.set_fill_color(0, 102, 204)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, "FAD - Ferramenta de Análise Dinamizada", 0, 1, "C", 1)
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Módulo 1 - Validação de GeometriaValidada", 0, 1, "C", 0)
        self.ln(5)

    def tabela_validacao(self, resultados):
        self.set_font("Arial", "B", 11)
        self.set_fill_color(230, 230, 230)
        self.set_text_color(0)
        self.cell(140, 8, "Critério", 1, 0, "L", 1)
        self.cell(40, 8, "Status", 1, 1, "C", 1)

        self.set_font("Arial", "", 11)
        for criterio, status in resultados.items():
            self.cell(140, 8, criterio, 1)
            if status:
                self.set_text_color(0, 153, 0)
                self.cell(40, 8, "✔️", 1, 1, "C")
            else:
                self.set_text_color(255, 0, 0)
                self.cell(40, 8, "❌", 1, 1, "C")
            self.set_text_color(0)

    def mensagem_final(self, aprovado):
        self.ln(5)
        self.set_font("Arial", "B", 12)
        if aprovado:
            self.set_text_color(0, 102, 0)
            self.cell(0, 10, "GeometriaValidada VALIDADA COM SUCESSO!", 0, 1, "C")
        else:
            self.set_text_color(204, 0, 0)
            self.cell(0, 10, "GeometriaValidada REPROVADA", 0, 1, "C")
        self.set_text_color(0)

    def rodape_autor(self, usuario):
        self.set_y(-30)
        self.set_font("Arial", "", 10)
        self.cell(0, 6, f"Usuário: {usuario.nome} | E-mail: {usuario.email}", 0, 1, "L")
        self.cell(0, 6, f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", 0, 1, "L")

def gerar_relatorio_validacao(usuario, resultados_dict, erros, aprovado, nome_pdf):
    resultados_legiveis = {
        "EPSG correto (4674)": resultados_dict.get("V1", False),
        "Tipo LineString": resultados_dict.get("V2", False),
        "Campo Cod preenchido": resultados_dict.get("V3", False),
        "Possui feição": resultados_dict.get("V4", False),
        "GeometriaValidada não vazia": resultados_dict.get("V5", False),
        "GeometriaValidada válida (topologia)": resultados_dict.get("V6", False),
        "Dentro do estado de SP": resultados_dict.get("V7", False),
        "Sem sobreposição de feições": resultados_dict.get("V8", False),
        "Comprimento > 10m": resultados_dict.get("V9", False),
    }

    pdf = PDFRelatorio()
    pdf.add_page()
    pdf.tabela_validacao(resultados_legiveis)
    pdf.mensagem_final(aprovado)
    pdf.rodape_autor(usuario)
    pdf.output(f"app/static/relatorios/{nome_pdf}")
