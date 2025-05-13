from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database.session import get_db

router = APIRouter(
    prefix='/painel/coordenador',
    tags=['Painel do Coordenador']
)

@router.get('/projetos')
def listar_projetos(db: Session = Depends(get_db)):
    query = text("""
        SELECT p.id, p.nome,
               COALESCE(pj.razao_social, pf.nome) AS interessado,
               rep.nome AS representante,
               cad.nome AS cadastrante,
               COALESCE(p.status, 'rascunho') AS status
        FROM projeto p
        LEFT JOIN "Cadastro".pessoa_juridica pj ON pj.id = p.pessoa_juridica_id
        LEFT JOIN "Cadastro".pessoa_fisica pf ON pf.id = p.pessoa_fisica_id
        LEFT JOIN "Cadastro".usuario_sistema rep ON rep.id = p.representante_id
        LEFT JOIN "Cadastro".usuario_sistema cad ON cad.id = p.usuario_id
        ORDER BY p.id DESC
    """)
    projetos = db.execute(query).fetchall()
    return [dict(row) for row in projetos]
