# app/api/dependencies.py

from fastapi import Request, HTTPException
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.models.cd_usuario_sistema import UsuarioSistema

def get_current_user(request: Request):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        raise HTTPException(status_code=403, detail="Não autenticado.")

    db: Session = SessionLocal()
    usuario = db.query(UsuarioSistema).filter(UsuarioSistema.id == usuario_id).first()
    db.close()

    if not usuario or not usuario.ativo:
        raise HTTPException(status_code=403, detail="Usuário inválido ou não aprovado.")

    return usuario
