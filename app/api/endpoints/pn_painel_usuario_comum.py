from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.cd_usuario_sistema import UsuarioSistema

# ✅ Padrão de roteador aplicado
from fastapi import APIRouter

router = APIRouter(
    prefix='/painel/analista',
    tags=['Painel do Analista']
)
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def painel_usuario_comum(request: Request, db: Session = Depends(get_db)):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return HTMLResponse(status_code=401, content="Não autorizado.")

    usuario = db.query(UsuarioSistema).filter(UsuarioSistema.id == usuario_id).first()
    return templates.TemplateResponse("pn_painel_usuario_comum.html", {
        "request": request,
        "usuario": usuario
    })

@router.get("/usuarios", response_class=JSONResponse)
def listar_usuarios_comuns(db: Session = Depends(get_db)):
    usuarios = db.query(UsuarioSistema).filter(UsuarioSistema.tipo == "comum").all()
    return [
        {
            "id": u.id,
            "nome": u.nome,
            "cpf": u.cpf,
            "email": u.email,
            "telefone": u.telefone,
            "criado_em": u.criado_em.strftime("%Y-%m-%d") if u.criado_em else "",
            "aprovado_em": u.aprovado_em.strftime("%Y-%m-%d") if u.aprovado_em else "",
            "aprovado_por": u.aprovado_por,
            "tipo_usuario": u.tipo,
            "status": u.status,
            "ativo": u.ativo
        }
        for u in usuarios
    ]

@router.post("/ativar/{usuario_id}", response_class=JSONResponse)
def ativar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioSistema).filter(UsuarioSistema.id == usuario_id).first()
    if not usuario:
        return JSONResponse(status_code=404, content={"detail": "Usuário não encontrado."})

    usuario.ativo = True
    db.commit()
    return {"detail": "Usuário ativado com sucesso"}




