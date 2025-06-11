from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.cd_pessoa_fisica import PessoaFisica
from app.models.cd_pessoa_juridica import PessoaJuridica
from app.models.cd_trecho_estadualizacao import TrechoEstadualizacao

router = APIRouter(prefix="/projeto", tags=["Cadastro de Projeto"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/cadastrar-projeto")
def carregar_pagina_projeto(request: Request, db: Session = Depends(get_db)):
    pfs = db.query(PessoaFisica).all()
    pjs = db.query(PessoaJuridica).all()
    trechos = db.query(TrechoEstadualizacao).all()

    print(f"🧾 Lista de PFs: {[(pf.id, pf.nome) for pf in pfs]}")
    print(f"🧾 Lista de PJs: {[(pj.id, pj.razao_social) for pj in pjs]}")
    print(f"🧾 Lista de Trechos: {[(t.id, t.codigo, t.municipio) for t in trechos]}")

    return templates.TemplateResponse("pr_cadastro_projeto.html", {
        "request": request,
        "pfs": pfs,
        "pjs": pjs,
        "trechos": trechos
    })
