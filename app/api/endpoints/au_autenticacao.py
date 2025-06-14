from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from app.database.session import get_db
from app.models.cd_usuario_sistema import UsuarioSistema
from app.security.hashing import verificar_senha
from fastapi.templating import Jinja2Templates
from passlib.hash import bcrypt
import time

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
    start = time.time()
    print(f"[DEBUG LOGIN] Tentativa de login para: {email} como {tipo}")
    
    # Busca apenas os campos necessários para autenticação
    usuario = db.query(UsuarioSistema.id, UsuarioSistema.email, UsuarioSistema.senha_hash, UsuarioSistema.status, UsuarioSistema.ativo, UsuarioSistema.tipo, UsuarioSistema.nome).filter(UsuarioSistema.email == email).first()

    if not usuario:
        print(f"[DEBUG LOGIN] Usuário não encontrado para email: {email}")
        return JSONResponse(status_code=401, content={"detail": "email"})

    print(f"[DEBUG LOGIN] Usuário encontrado: {usuario.nome}, Status: {usuario.status}, Ativo: {usuario.ativo}, Tipo: {usuario.tipo}")

    # bcrypt é seguro, mas pode ser lento. Se possível, use um custo menor ao gerar os hashes.
    if not bcrypt.verify(senha, usuario.senha_hash):
        print(f"[DEBUG LOGIN] Senha incorreta para: {email}")
        return JSONResponse(status_code=401, content={"detail": "senha"})

    if usuario.status != "aprovado":
        print(f"[DEBUG LOGIN] Status não aprovado: {usuario.status}")
        return JSONResponse(status_code=403, content={"detail": "status", "motivo": usuario.status})
    if not usuario.ativo:
        print(f"[DEBUG LOGIN] Usuário inativo")
        return JSONResponse(status_code=403, content={"detail": "ativo", "motivo": "Usuário inativo"})

    if usuario.tipo != tipo:
        print(f"[DEBUG LOGIN] Tipo incorreto. Esperado: {tipo}, Encontrado: {usuario.tipo}")
        return JSONResponse(status_code=401, content={"detail": "tipo"})

    print(f"[DEBUG LOGIN] Login validado com sucesso para: {email}")

    # Verifica se o SessionMiddleware está presente
    if not hasattr(request, "session"):
        return JSONResponse(status_code=500, content={"detail": "SessionMiddleware não configurado"})

    request.session["usuario_id"] = usuario.id
    request.session["usuario_tipo"] = usuario.tipo
    request.session["usuario_nome"] = usuario.nome
    request.session["usuario_email"] = usuario.email

    # Redireciona conforme o tipo
    if usuario.tipo == "master":
        destino = "/painel-master"
    elif usuario.tipo == "coordenador":
        destino = "/painel-coordenador"
    else:
        destino = "/painel-analista"

    tempo = round((time.time() - start)*1000)
    print(f"Login processado em {tempo} ms para {email}")
    return JSONResponse(status_code=200, content={"redirect": destino})

# ❎ Rota de logout (encerra a sessão e redireciona para login)
@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=302)
