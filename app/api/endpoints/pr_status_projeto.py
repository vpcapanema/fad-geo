# app/api/endpoints/cd_projeto_status.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.session import SessionLocal
# ✅ Padrão de roteador aplicado
from fastapi import APIRouter

router = APIRouter(
    prefix='/projeto/status',
    tags=['Status de Projetos']
)
from app.models.pr_projeto import Projeto
from app.api.dependencies import get_current_user

router = APIRouter()

# 🔁 Enviar projeto (usuário comum)
@router.post("/projetos/{id}/enviar")
def enviar_projeto(id: int, current_user=Depends(get_current_user)):
    if current_user.tipo_usuario != "comum":
        raise HTTPException(status_code=403, detail="Apenas usuários comuns podem enviar projeto.")
    
    db: Session = SessionLocal()
    projeto = db.query(Projeto).filter(Projeto.id == id).first()

    if not projeto or projeto.status != "em edição":
        raise HTTPException(status_code=400, detail="Projeto não está em edição ou não existe.")

    projeto.status = "enviado"
    projeto.enviado_em = datetime.utcnow()
    db.commit()
    return {"mensagem": "Projeto enviado com sucesso."}

# ✅ Aprovar projeto (admin)
@router.post("/projetos/{id}/aprovar")
def aprovar_projeto(id: int, current_user=Depends(get_current_user)):
    if current_user.tipo_usuario != "administrador":
        raise HTTPException(status_code=403, detail="Apenas administradores podem aprovar projeto.")

    db: Session = SessionLocal()
    projeto = db.query(Projeto).filter(Projeto.id == id).first()

    if not projeto or projeto.status != "enviado":
        raise HTTPException(status_code=400, detail="Projeto não está no status 'enviado'.")

    projeto.status = "finalizado"
    projeto.aprovado_em = datetime.utcnow()
    projeto.aprovador_id = current_user.id_usuario
    db.commit()
    return {"mensagem": "Projeto aprovado com sucesso."}

# ❌ Reprovar projeto (admin)
@router.post("/projetos/{id}/reprovar")
def reprovar_projeto(id: int, current_user=Depends(get_current_user)):
    if current_user.tipo_usuario != "administrador":
        raise HTTPException(status_code=403, detail="Apenas administradores podem reprovar projeto.")

    db: Session = SessionLocal()
    projeto = db.query(Projeto).filter(Projeto.id == id).first()

    if not projeto or projeto.status != "enviado":
        raise HTTPException(status_code=400, detail="Projeto não está no status 'enviado'.")

    projeto.status = "em edição"
    projeto.aprovador_id = current_user.id_usuario
    db.commit()
    return {"mensagem": "Projeto reprovado. Retornado para edição do usuário comum."}

# 🔁 Corrigir status (master)
@router.post("/projetos/{id}/corrigir-status")
def master_corrige_status(id: int, novo_status: str, current_user=Depends(get_current_user)):
    if current_user.tipo_usuario != "master":
        raise HTTPException(status_code=403, detail="Apenas o usuário master pode corrigir status.")

    if novo_status not in ["em edição", "enviado", "finalizado"]:
        raise HTTPException(status_code=400, detail="Status inválido.")

    db: Session = SessionLocal()
    projeto = db.query(Projeto).filter(Projeto.id == id).first()
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")

    projeto.status = novo_status
    db.commit()
    return {"mensagem": f"Status alterado para '{novo_status}' com sucesso pelo master."}
