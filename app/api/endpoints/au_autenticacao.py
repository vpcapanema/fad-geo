from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from app.database.session import get_db
from app.models.cd_usuario_sistema import UsuarioSistema
from app.security.hashing import verificar_senha
from fastapi.templating import Jinja2Templates
from passlib.hash import bcrypt

router = APIRouter(
    prefix="/login",
    tags=["Login"]
)

templates = Jinja2Templates(directory="app/templates")

# ✅ Processa os dados do formulário de login
@router.post("")
@router.post("/")
def login_usuario(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    tipo: str = Form(...),
    db: Session = Depends(get_db)
):
    usuario = db.query(UsuarioSistema).filter(UsuarioSistema.email == email).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="E-mail inválido.")

    if not bcrypt.verify(senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Senha inválida.")

    if usuario.status != "aprovado" or not usuario.ativo:
        raise HTTPException(status_code=403, detail="Aguardando aprovação do coordenador.")

    if usuario.tipo != tipo:
        raise HTTPException(status_code=401, detail="Tipo de acesso incorreto.")

    request.session["usuario_id"] = usuario.id
    request.session["usuario_tipo"] = usuario.tipo
    request.session["usuario_nome"] = usuario.nome
    request.session["usuario_email"] = usuario.email

    if usuario.tipo == "master":
        return RedirectResponse(url="/painel-master", status_code=302)
    elif usuario.tipo == "administrador":
        return RedirectResponse(url="/painel-coordenador", status_code=302)
    else:
        return RedirectResponse(url="/painel-analista", status_code=302)

# ❎ Rota de logout (encerra a sessão e redireciona para login)
@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=302)
