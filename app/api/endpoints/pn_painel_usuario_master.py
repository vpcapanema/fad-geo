from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date
from app.database.session import get_db
from app.models.cd_usuario_sistema import UsuarioSistema

# ✅ Padrão de roteador aplicado
from fastapi import APIRouter

router = APIRouter(
    prefix='/painel/master',
    tags=['Painel Master']
)
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def painel_master(request: Request, db: Session = Depends(get_db)):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return RedirectResponse(url="/login", status_code=302)
    usuario = db.query(UsuarioSistema).filter(UsuarioSistema.id == usuario_id).first()
    if not usuario:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("pn_painel_usuario_master.html", {
        "request": request,
        "usuario": usuario,
        "data_hoje": date.today().strftime("%d/%m/%Y")
    })

@router.get("/es")
def listar_administradores(db: Session = Depends(get_db)):
    admins = db.query(UsuarioSistema).filter(UsuarioSistema.tipo == "administrador").all()
    return [
        {
            "id": admin.id,
            "nome": admin.nome,
            "cpf": admin.cpf,
            "email": admin.email,
            "tipo_usuario": admin.tipo,
            "status": admin.status,
            "ativo": admin.ativo
        }
        for admin in admins
    ]

@router.post("/es/aprovar/{usuario_id}")
def aprovar_administrador(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioSistema).filter(UsuarioSistema.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    usuario.status = "Aprovado"
    usuario.ativo = True
    db.commit()
    return {"mensagem": "Administrador aprovado com sucesso."}

@router.post("/es/reprovar/{usuario_id}")
def reprovar_administrador(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioSistema).filter(UsuarioSistema.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    usuario.status = "Reprovado"
    usuario.ativo = False
    db.commit()
    return {"mensagem": "Administrador reprovado com sucesso."}

@router.get("/usuarios")
def listar_usuarios_comuns(db: Session = Depends(get_db)):
    usuarios = db.query(UsuarioSistema).filter(UsuarioSistema.tipo == "comum").all()
    return [
        {
            "id": u.id,
            "nome": u.nome,
            "cpf": u.cpf,
            "email": u.email,
            "solicitacao": getattr(u, "solicitacao", "-"),
            "tipo_usuario": u.tipo,
            "status": u.status,
            "ativo": u.ativo
        }
        for u in usuarios
    ]



