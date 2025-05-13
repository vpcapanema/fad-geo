from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database.session import get_db

router = APIRouter()

@router.get("/painel/coordenador/projetos")
def listar_projetos(db: Session = Depends(get_db)):
    try:
        query = text("""
            SELECT p.id, p.nome, pj.razao_social, pj.cnpj,
                   pf.nome AS representante, pf.cpf,
                   t.denominacao AS trecho, t.municipio, t.extensao_km,
                   u.nome AS analista, p.enviado_em
            FROM public.projeto p
            LEFT JOIN "Cadastro".pessoa_juridica pj ON p.pessoa_juridica_id = pj.id
            LEFT JOIN "Cadastro".pessoa_fisica pf ON p.pessoa_fisica_id = pf.id
            LEFT JOIN "Elementos_rodoviarios".trechos_estadualizacao t ON p.trecho_id = t.id
            LEFT JOIN "Cadastro".usuario_sistema u ON u.id = p.usuario_id
        """)
        projetos = db.execute(query).fetchall()
        return [dict(row) for row in projetos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar projetos: {str(e)}")