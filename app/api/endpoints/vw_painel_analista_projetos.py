from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from app.database.session import get_db

router = APIRouter(
    prefix='/painel-analista',
    tags=['Painel do Analista']
)

@router.get('/projetos/{usuario_id}')
def listar_projetos_usuario(usuario_id: int, db: Session = Depends(get_db)):
    query = '''
        SELECT id, nome, status
        FROM projeto
        WHERE usuario_id = :usuario_id
        ORDER BY id DESC
    '''
    projetos = db.execute(text(query, {{'usuario_id': usuario_id}})).fetchall()
    if not projetos:
        raise HTTPException(status_code=404, detail='Nenhum projeto encontrado.')
    return [dict(row) for row in projetos]