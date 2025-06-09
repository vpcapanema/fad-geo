from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database.session import get_db
from app.models.painel_administrador import UsuarioAprovado, ProjetoRecebido

router = APIRouter(
    prefix='/painel/coordenador',
    tags=['Painel do Coordenador']
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/painel-usuario-coordenador", response_class=HTMLResponse)
def painel_coordenador(request: Request, db: Session = Depends(get_db)):
    try:
        # 🧑‍💼 Usuários aprovados
        usuarios = db.execute(text("""
            SELECT id, nome, cpf, email, telefone,
                   CASE WHEN status = 'aprovado' THEN 'Aprovado' ELSE 'Pendente' END AS status
            FROM "Cadastro".usuario_sistema
            WHERE status = 'aprovado'
            ORDER BY nome
        """)).fetchall()

        # 📋 Projetos recebidos
        projetos = db.execute(text("""
            SELECT p.id, p.nome, p.municipio AS municipio,
                   COALESCE(pj.razao_social, pf.nome) AS interessado,
                   rep.nome AS representante,
                   cad.nome AS cadastrante,
                   COALESCE(p.status, 'Rascunho') AS status
            FROM projeto p
            LEFT JOIN "Cadastro".pessoa_juridica pj ON pj.id = p.pessoa_juridica_id
            LEFT JOIN "Cadastro".pessoa_fisica pf ON pf.id = p.pessoa_fisica_id
            LEFT JOIN "Cadastro".usuario_sistema rep ON rep.id = p.representante_id
            LEFT JOIN "Cadastro".usuario_sistema cad ON cad.id = p.usuario_id
            ORDER BY p.id DESC
        """)).fetchall()

        return templates.TemplateResponse("cd_painel_administrador.html", {
            "request": request,
            "usuarios": [UsuarioAprovado(**dict(row)) for row in usuarios],
            "projetos": [ProjetoRecebido(**dict(row)) for row in projetos]
        })

    except Exception as e:
        print("❌ ERRO NO PAINEL COORDENADOR:", e)
        raise HTTPException(status_code=500, detail="Erro ao carregar dados do painel coordenador")
