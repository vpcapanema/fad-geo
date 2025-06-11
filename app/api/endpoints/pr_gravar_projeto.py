from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.session import get_db
from app.models.cd_pessoa_fisica import PessoaFisica
from app.models.cd_pessoa_juridica import PessoaJuridica
from app.models.cd_trecho_estadualizacao import TrechoEstadualizacao
from app.models.pr_projeto import Projeto

router = APIRouter(
    prefix="/projeto",
    tags=["Cadastro de Projeto"]
)

templates = Jinja2Templates(directory="app/templates")

# ================== Página de cadastro ==================
@router.get("/")
def carregar_pagina_projeto(request: Request, db: Session = Depends(get_db)):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return RedirectResponse(url="/login", status_code=302)
    pfs = db.query(PessoaFisica).all()
    pjs = db.query(PessoaJuridica).all()
    trechos = db.query(TrechoEstadualizacao).all()
    return templates.TemplateResponse("pr_cadastro_projeto.html", {
        "request": request,
        "pfs": pfs,
        "pjs": pjs,
        "trechos": trechos
    })


# ================== Salvar projeto (etapa 1) ==================
@router.post("/salvar", response_class=HTMLResponse)
async def salvar_projeto(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    nome = form.get("nome")
    interessado_id = form.get("interessado_id")
    representante_id = form.get("representante_id")
    trecho_id = form.get("trecho_id")
    usuario_id = request.session.get("usuario_id")

    # DEBUG: impressões explícitas no terminal
    print("\n🔎 DEBUG - VALORES RECEBIDOS NO FORMULÁRIO:")
    print("📝 nome:", repr(nome))
    print("🏢 interessado_id (PJ):", repr(interessado_id))
    print("👤 representante_id (PF):", repr(representante_id))
    print("🛣️ trecho_id:", repr(trecho_id))
    print("👨‍💼 usuario_id (da sessão):", repr(usuario_id))

    if not all([nome, interessado_id, representante_id, trecho_id, usuario_id]):
        print("❌ Dados incompletos recebidos, abortando gravação.")
        return HTMLResponse(content="❌ Dados incompletos para salvar projeto.", status_code=422)

    try:
        novo = Projeto(
            nome=nome,
            pessoa_juridica_id=int(interessado_id),
            pessoa_fisica_id=int(representante_id),
            trecho_id=int(trecho_id),
            usuario_id=int(usuario_id),
            status="em cadastramento",  # ⚠️ EXATAMENTE como está no CHECK do banco
            enviado_em=None,
            aprovado_em=None,
            aprovador_id=None,
            observacao=None,
            geometria_id=None
        )

        db.add(novo)
        db.commit()
        db.refresh(novo)

        print(f"✅ Projeto salvo com sucesso! ID: {novo.id}")
        return RedirectResponse(url="/projeto", status_code=302)

    except Exception as e:
        print("❌ ERRO ao salvar projeto no banco:", str(e))
        return HTMLResponse(content="❌ ERRO ao salvar projeto. Verifique os dados e tente novamente.", status_code=500)


# ================== Selects dinâmicos ==================
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

@router.get("/cadastro/pjs/json")
def listar_pjs_json(db: Session = Depends(get_db)):
    try:
        pjs = db.query(PessoaJuridica).all()
        return [{"id": pj.id, "razao_social": pj.razao_social, "cnpj": pj.cnpj} for pj in pjs]
    except SQLAlchemyError as e:
        print("❌ ERRO SQL:", e)
        return JSONResponse(
            status_code=500,
            content={"erro": "Erro ao carregar lista de Pessoas Jurídicas."}
        )


    pjs = db.query(PessoaJuridica).all()
    return [{"id": pj.id, "razao_social": pj.razao_social, "cnpj": pj.cnpj} for pj in pjs]

@router.get("/cadastro/pfs/json")
def listar_pfs_json(db: Session = Depends(get_db)):
    pfs = db.query(PessoaFisica).all()
    return [{"id": pf.id, "nome": pf.nome, "cpf": pf.cpf} for pf in pfs]

@router.get("/cadastro/trechos/json")
def listar_trechos_json(db: Session = Depends(get_db)):
    trechos = db.query(TrechoEstadualizacao).all()
    return [{"id": t.id, "codigo": t.codigo, "denominacao": t.denominacao, "municipio": t.municipio} for t in trechos]
