from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date
from app.database.session import get_db
from app.models.cd_usuario_sistema import UsuarioSistema

router = APIRouter(
    prefix='/painel-master',
    tags=['Painel Master']
)
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def painel_master(request: Request, db: Session = Depends(get_db)):
    print(f"[DEBUG PAINEL MASTER] Acessando painel master")
    usuario_id = request.session.get("usuario_id")
    usuario_tipo = request.session.get("usuario_tipo")
    print(f"[DEBUG PAINEL MASTER] usuario_id: {usuario_id}, usuario_tipo: {usuario_tipo}")
    
    if not usuario_id:
        print(f"[DEBUG PAINEL MASTER] Redirecionando para login: sem usuario_id")
        return RedirectResponse(url="/login", status_code=302)
    
    usuario = db.query(UsuarioSistema).filter(UsuarioSistema.id == usuario_id).first()
    if not usuario:
        print(f"[DEBUG PAINEL MASTER] Redirecionando para login: usuário não encontrado")
        return RedirectResponse(url="/login", status_code=302)
    
    if usuario.tipo != "master":
        print(f"[DEBUG PAINEL MASTER] Redirecionando para login: tipo incorreto {usuario.tipo}")
        return RedirectResponse(url="/login", status_code=302)    
    print(f"[DEBUG PAINEL MASTER] Carregando painel para usuário: {usuario.nome}")
    return templates.TemplateResponse("pn_painel_usuario_master.html", {
        "request": request,
        "usuario": usuario,
        "data_hoje": date.today().strftime("%d/%m/%Y"),
        "tempo_restante": 15 * 60  # 15 minutos em segundos
    })

@router.get("/usuarios", response_class=JSONResponse)
def listar_usuarios_comuns(db: Session = Depends(get_db)):
    usuarios = db.query(UsuarioSistema).filter(UsuarioSistema.tipo == "analista").all()
    return [
        {
            "id": u.id,
            "nome": u.nome,
            "cpf": u.cpf,
            "email": u.email,
            "telefone": u.telefone,
            "instituicao": u.instituicao,
            "tipo_lotacao": u.tipo_lotacao,
            "email_institucional": u.email_institucional,
            "telefone_institucional": u.telefone_institucional,
            "ramal": u.ramal,
            "criado_em": u.criado_em.strftime("%Y-%m-%d") if u.criado_em else "",
            "aprovado_em": u.aprovado_em.strftime("%Y-%m-%d") if u.aprovado_em else "",
            "aprovador_id": u.aprovador_id,            "sede_hierarquia": u.sede_hierarquia,
            "sede_coordenadoria": u.sede_coordenadoria,
            "sede_assistencia": u.sede_assistencia,
            "regional_nome": u.regional_nome,
            "regional_coordenadoria": u.regional_coordenadoria,
            "regional_setor": u.regional_setor,
            "pessoa_fisica_id": u.pessoa_fisica_id,
            "tipo_usuario": u.tipo,
            "status": u.status,
            "ativo": u.ativo
        }
        for u in usuarios
    ]

@router.get("/es", response_class=JSONResponse)
def listar_coordenadores(db: Session = Depends(get_db)):
    admins = db.query(UsuarioSistema).filter(UsuarioSistema.tipo == "coordenador").all()
    return [
        {
            "id": admin.id,
            "nome": admin.nome,
            "cpf": admin.cpf,
            "email": admin.email,
            "telefone": admin.telefone,
            "instituicao": admin.instituicao,
            "tipo_lotacao": admin.tipo_lotacao,
            "email_institucional": admin.email_institucional,
            "telefone_institucional": admin.telefone_institucional,
            "ramal": admin.ramal,
            "criado_em": admin.criado_em.strftime("%Y-%m-%d") if admin.criado_em else "",
            "aprovado_em": admin.aprovado_em.strftime("%Y-%m-%d") if admin.aprovado_em else "",
            "aprovador_id": admin.aprovador_id,            "sede_hierarquia": admin.sede_hierarquia,
            "sede_coordenadoria": admin.sede_coordenadoria,
            "sede_assistencia": admin.sede_assistencia,
            "regional_nome": admin.regional_nome,
            "regional_coordenadoria": admin.regional_coordenadoria,
            "regional_setor": admin.regional_setor,
            "pessoa_fisica_id": admin.pessoa_fisica_id,
            "tipo_usuario": admin.tipo,
            "status": admin.status,
            "ativo": admin.ativo
        }
        for admin in admins
    ]

@router.post("/es/aprovar/{usuario_id}")
def aprovar_coordenador(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioSistema).filter(UsuarioSistema.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    usuario.status = "Aprovado"
    usuario.ativo = True
    db.commit()
    return {"mensagem": "Coordenador aprovado com sucesso."}

@router.post("/es/reprovar/{usuario_id}")
def reprovar_coordenador(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioSistema).filter(UsuarioSistema.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    usuario.status = "Reprovado"
    usuario.ativo = False
    db.commit()
    return {"mensagem": "Coordenador reprovado com sucesso."}

@router.post("/ativar/{usuario_id}", response_class=JSONResponse)
def ativar_usuario_master(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioSistema).filter(UsuarioSistema.id == usuario_id).first()
    if not usuario:
        return JSONResponse(status_code=404, content={"detail": "Usuário não encontrado."})
    usuario.ativo = True
    db.commit()
    return {"detail": "Usuário ativado com sucesso"}

@router.get("/painel-master", response_class=HTMLResponse)
def painel_master():
    return "This is the painel-master page!"



