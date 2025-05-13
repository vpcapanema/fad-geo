from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database.session import get_db

router = APIRouter()

@router.get("/painel/analista/usuarios")
def listar_usuarios_comuns(db: Session = Depends(get_db)):
    try:
        query = text("""
            SELECT id, nome, cpf, email, telefone, status
            FROM "Cadastro".usuario_sistema
            WHERE tipo = 'comum'
            ORDER BY nome
        """)
        resultados = db.execute(query).mappings().all()
        return list(resultados)
    except Exception as e:
        return {"erro": str(e)}

@router.get("/painel/coordenador/usuarios")
def listar_usuarios_administradores(db: Session = Depends(get_db)):
    try:
        query = text("""
            SELECT id, nome, cpf, email, telefone, status
            FROM "Cadastro".usuario_sistema
            WHERE tipo = 'administrador'
            ORDER BY nome
        """)
        resultados = db.execute(query).mappings().all()
        return list(resultados)
    except Exception as e:
        return {"erro": str(e)}
