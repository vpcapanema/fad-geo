# app/api/endpoints/vw_projetos_usuario_comum.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List

# ✅ Padrão de roteador aplicado
from fastapi import APIRouter

router = APIRouter(
    prefix='/painel/analista',
    tags=['Painel do Analista']
)
from app.database.session import get_db
from app.models.vw_projetos_usuario_comum import ProjetoResumo

router = APIRouter()

@router.get("/projetos/usuario/{usuario_id}", response_model=List[ProjetoResumo])
def listar_projetos_usuario(usuario_id: int, db: Session = Depends(get_db)):
    query = """
        SELECT
            id AS id,
            nome AS nome,
            interessado AS interessado,
            representante AS representante,
            geometria_status AS geometria_status,
            conformidade_status AS conformidade_status,
            favorabilidade_fm AS favorabilidade_fm,
            favorabilidade_fs AS favorabilidade_fs,
            favorabilidade_fi AS favorabilidade_fi,
            status AS status
        FROM vw_projetos_usuario_comum
        WHERE usuario_id = :usuario_id
        ORDER BY id DESC
    """
    resultados = db.execute(text(query, {"usuario_id": usuario_id})).fetchall()
    if not resultados:
        raise HTTPException(status_code=404, detail="Nenhum projeto encontrado para este usuário.")
    
    return [ProjetoResumo(**dict(r)) for r in resultados]