from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database.session import SessionLocal, get_db
from app.modules.conformidade_ambiental.ca_processador import processar_conformidade
from app.models.pr_projeto import Projeto

# ✅ Padrão de roteador aplicado
from fastapi import APIRouter

router = APIRouter(
    prefix='/analise/conformidade',
    tags=['Conformidade Ambiental']
)
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# Rota para exibir a interface com os projetos
@router.get("/importar-validar", response_class=HTMLResponse)
def exibir_interface_validacao(request: Request, db: Session = Depends(get_db)):
    projetos = db.query(Projeto).order_by(Projeto.nome.asc()).all()
    return templates.TemplateResponse("iv_interface.html", {
        "request": request,
        "projetos": projetos
    })


# Rota para executar a análise de conformidade (POST)
@router.post("/", response_class=JSONResponse)
async def executar_conformidade(request: Request):
    data = await request.json()
    camadas = data.get("camadas", [])
    tipo_laudo = data.get("tipo_laudo", "analitico")

    resultado = processar_conformidade({
        "camadas": camadas,
        "tipo_laudo": tipo_laudo
    })

    return JSONResponse(content=resultado)


# Rota para buscar o nome do último arquivo validado
@router.get("/arquivo-atual")
def nome_arquivo_validado():
    session = SessionLocal()
    try:
        resultado = session.execute(text("""
            SELECT nome_arquivo
            FROM validacao_geometria
            WHERE geometria_valida = TRUE
            ORDER BY data_validacao DESC
            LIMIT 1
        """)).fetchone()

        if resultado:
            return {"arquivo": resultado[0]}
        else:
            return {"arquivo": "Nenhum arquivo validado encontrado"}

    finally:
        session.close()
@router.get("/conformidade/laudo-sintetico", response_class=HTMLResponse)
def gerar_laudo_sintetico(request: Request):
    conserva = obter_dados_conformidade()
    return templates.TemplateResponse("ca_laudo_sintetico_template.html", {
        "request": request,
        "conserva": conserva,
        "data": "2024-01-01",
        "diretoria": "DER-SP",
        "horario": "12:00",
        "item": "Trecho",
        "municipio": "São Paulo",
        "nome": "Usuário de Teste"
    })
@router.get("/conformidade/laudo-analitico", response_class=HTMLResponse)
def gerar_laudo_analitico(request: Request):
    return templates.TemplateResponse("ca_laudo_template.html", {
        "request": request,
        "data": "2024-01-01",
        "municipio": "São Paulo",
        "nome": "Usuário de Teste",
        "trecho": "Rodovia XPTO"
    })
@router.get("/conformidade/relatorio-processamento", response_class=HTMLResponse)
def relatorio_processamento(request: Request):
    return templates.TemplateResponse("ca_relatorio_processamento.html", {
        "request": request,
        "buffer_km": 10,
        "camada": "APP",
        "data": "2024-01-01",
        "horario": "12:00",
        "municipio": "São Paulo",
        "nome": "Usuário de Teste",
        "tipo": "Restrição"
    })

