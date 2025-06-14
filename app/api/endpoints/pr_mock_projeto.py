from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/projeto/mock")
def projeto_mock(request: Request):
    # Dados fictícios para desenvolvimento offline
    pfs = [
        type('PF', (), {'id_pf': 1, 'nome': 'João da Silva', 'cpf': '123.456.789-00'})(),
        type('PF', (), {'id_pf': 2, 'nome': 'Maria Oliveira', 'cpf': '987.654.321-00'})(),
    ]
    pjs = [
        type('PJ', (), {'id_pj': 1, 'razao_social': 'Construtora Fictícia Ltda', 'cnpj': '12.345.678/0001-99'})(),
        type('PJ', (), {'id_pj': 2, 'razao_social': 'Engenharia Exemplo S/A', 'cnpj': '98.765.432/0001-11'})(),
    ]
    elementos = [
        type('EL', (), {'id': 1, 'nome': 'Rodovia Fictícia 001'})(),
        type('EL', (), {'id': 2, 'nome': 'Trecho Exemplo 002'})(),
    ]
    trechos = [
        type('TR', (), {'id': 1, 'codigo': 'TR-001', 'denominacao': 'Trecho Norte', 'municipio': 'Município A'})(),
        type('TR', (), {'id': 2, 'codigo': 'TR-002', 'denominacao': 'Trecho Sul', 'municipio': 'Município B'})(),
    ]
    usuario = type('Usuario', (), {'nome': 'Usuário Mock'})()
    return templates.TemplateResponse("pr_cadastro_projeto.html", {
        "request": request,
        "pfs": pfs,
        "pjs": pjs,
        "elementos": elementos,
        "trechos": trechos,
        "usuario": usuario
    })
