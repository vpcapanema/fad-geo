import os
from pathlib import Path

# Caminho da pasta de templates
TEMPLATES_DIR = Path("app/templates")

ROTAS_HTML = {
    "home.html": ("/", "Página de abertura da FAD"),
    "au_login.html": ("/login", "Tela de login de usuário"),
    "cd_cadastro_usuario.html": ("/cadastro-usuario", "Cadastro de novo usuário do sistema"),
    "cd_interessado_pf.html": ("/cadastro-interessado-pf", "Cadastro de pessoa física interessada"),
    "cd_interessado_pj.html": ("/cadastro-interessado-pj", "Cadastro de pessoa jurídica interessada"),
    "cd_interessado_trecho.html": ("/cadastro-interessado-trecho", "Cadastro de trecho vinculado ao interessado"),
    "ca_interface.html": ("/conformidade", "Tela do módulo de Conformidade Ambiental"),
    "ca_laudo_template.html": ("/conformidade/laudo-analitico", "Template do Laudo Analítico"),
    "ca_laudo_sintetico_template.html": ("/conformidade/laudo-sintetico", "Template do Laudo Sintético"),
    "ca_processamento_template.html": ("/conformidade/relatorio-processamento", "Template de relatório técnico do processamento"),
    "ca_relatorio_processamento.html": ("/conformidade/relatorio-processamento-pdf", "Relatório de Processamento em PDF"),
    "iv_interface.html": ("/importar", "Upload e validação de shapefile para análise"),
    "pr_cadastro_projeto.html": ("/cadastro-projeto", "Formulário de criação e vínculo de projeto"),
    "pn_painel_usuario_comum.html": ("/painel-analista", "Painel do Analista (usuário comum)"),
    "pn_painel_usuario_adm.html": ("/painel-coordenador", "Painel do Coordenador (administrador)"),
    "pn_painel_usuario_master.html": ("/painel-master", "Painel do usuário master com acesso total"),
    "pagina_em_construcao.html": ("/em-breve", "Página de funcionalidade em construção"),
}

# Gerar HTML dinamicamente
linhas = ""
for arquivo in sorted(os.listdir(TEMPLATES_DIR)):
    if arquivo.endswith(".html") and arquivo in ROTAS_HTML:
        rota, descricao = ROTAS_HTML[arquivo]
        linhas += f"<tr><td>{arquivo}</td><td><a href='http://127.0.0.1:8000{rota}' target='_blank'>http://127.0.0.1:8000{rota}</a></td><td>{descricao}</td></tr>\n"

html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Mapa de Rotas - FAD</title>
    <style>
        body {{ font-family: Arial; background: #f4f7fa; padding: 30px; }}
        table {{ width: 90%; margin: auto; border-collapse: collapse; }}
        th, td {{ border: 1px solid #ccc; padding: 12px; text-align: left; }}
        th {{ background-color: #e8f0fe; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        a {{ color: #0066cc; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>🌐 Mapa de Rotas HTML - FAD</h1>
    <table>
        <thead>
            <tr><th>Template</th><th>URL</th><th>Descrição</th></tr>
        </thead>
        <tbody>
            {linhas}
        </tbody>
    </table>
</body>
</html>"""

# Salvar
Path("app/static").mkdir(parents=True, exist_ok=True)
with open("app/static/mapa_rotas_fad.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Mapa de rotas atualizado com sucesso.")
print("📂 Arquivo salvo em: app/static/mapa_rotas_fad.html")