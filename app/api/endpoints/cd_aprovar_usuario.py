# app/api/endpoints/cd_aprovar_usuario.py

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.session import get_db
# ✅ Padrão de roteador aplicado
from fastapi import APIRouter

router = APIRouter(
    prefix='/usuario/aprovacao',
    tags=['Aprovação de Usuários']
)
from app.models.cd_usuario_sistema import UsuarioSistema
from app.api.dependencies import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/painel-usuario-aprovacao")
def exibir_painel_aprovacao(request: Request, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.tipo != "master":
        raise HTTPException(status_code=403, detail="Acesso negado.")
    usuarios = db.query(UsuarioSistema).filter(UsuarioSistema.tipo == "analista").all()
    return templates.TemplateResponse("cd_painel_aprovacao.html", {"request": request, "usuarios": usuarios})


@router.post("/usuarios/{usuario_id}/aprovar")
def aprovar_usuario(usuario_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.tipo != "master":
        raise HTTPException(status_code=403, detail="Permissão negada.")

    usuario = db.query(UsuarioSistema).filter(UsuarioSistema.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    usuario.ativo = True
    usuario.status = "aprovado"
    usuario.aprovado_em = datetime.utcnow()
    usuario.aprovador_id = current_user.id
    db.commit()
    return RedirectResponse(url="/painel-usuario-aprovacao", status_code=303)


@router.post("/usuarios/{usuario_id}/reprovar")
def reprovar_usuario(usuario_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.tipo != "master":
        raise HTTPException(status_code=403, detail="Permissão negada.")

    usuario = db.query(UsuarioSistema).filter(UsuarioSistema.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    usuario.ativo = False
    usuario.status = "reprovado"
    usuario.aprovado_em = datetime.utcnow()
    usuario.aprovador_id = current_user.id
    db.commit()
    return RedirectResponse(url="/painel-usuario-aprovacao", status_code=303)

